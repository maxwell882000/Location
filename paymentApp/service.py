import json
from abc import ABC, abstractmethod

import requests
from django.conf import settings

from paymentApp.models import OrderStatus


class PaymentError(Exception):
    LOGICAL_MAP = {
        'URL_FORGET': "Забыли ввести URL"
    }

    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code


class PaymentOrderError(PaymentError):
    MAP = {
        0: "Заказ зарегистрирован, но не оплачен",
        1: "Предавторизованная сумма захолдирована (для двухстадийных платежей)",
        2: "Проведена полная авторизация суммы заказа",
        3: "Авторизация отменена",
        4: "По транзакции была проведена операция возврата",
        5: "Инициирована авторизация через ACS банка-эмитента",
        6: "Авторизация отклонена",
        "NOT FOUND": "Заказ не был найден."
    }


class PaymentClasses(ABC):
    URL = ""

    @abstractmethod
    def as_dict(self) -> dict:
        pass

    @abstractmethod
    def finishTransaction(self, response: dict):
        pass

    def checkOnError(self, response: dict):
        if response['errorCode'] != 0:
            raise PaymentError(message=response['errorMessage'], code=response['errorCode'])


class RegisterObject(PaymentClasses):
    URL = "register.do"

    def __init__(self, order_unique, clientId):
        self.orderNumber = order_unique.id
        self.amount = order_unique.amount * 100
        self.returnUrl = self.url("/success_payment")
        self.failUrl = self.url("/fail_payment")
        self.clientId = clientId
        self.features = "AUTO_PAYMENT"
        self.order_unique = order_unique

    def url(self, query):
        return "https://sportandthecity.page.link/?" \
               "link=https://sportandthecity.page.com/?path=" + query + \
               "path=&apn=com.location_specialist.location_specialist&isi=1619132873&" \
               "ibi=com.location.sportandthecity"

    def as_dict(self) -> dict:
        as_dict = dict(self.__dict__)
        del as_dict['order_unique']
        # del as_dict['some key']
        # remove the object which is required for finishing the transaction
        return as_dict

    def finishTransaction(self, response: dict) -> dict:
        # store orderId here
        self.order_unique.orderId = response['orderId']
        return {"formUrl": response['formUrl']}


class OrderStatusObject(PaymentClasses):
    URL = "getOrderStatus.do"

    def __init__(self, user):
        self.orderId = user.user_specialist.order_user.order_unique.orderId
        self.order_user = user.user_specialist.order_user

    def checkOnError(self, response: dict):
        super().checkOnError(response)
        orderStatus = response['orderStatus']
        if 'orderStatus' not in orderStatus:
            raise PaymentOrderError(message=PaymentOrderError.MAP['NOT_FOUND'], code=-1)
        if orderStatus != 2:
            raise PaymentOrderError(message=PaymentOrderError.MAP[orderStatus], code=orderStatus)

    def finishTransaction(self, response: dict):

        OrderStatus.objects.create(order_id=self.order_user.id,
                                   ip=response['ip'],
                                   bindingId=response['bindingId'])
        return {"status": True}

    def as_dict(self) -> dict:
        as_dict = dict(self.__dict__)
        del as_dict['order_user']
        return as_dict


class BindingObject(PaymentClasses, ABC):
    def __init__(self, user):
        self.bindingId = user.user_specialist.order_user.order_status.bindingId

    def as_dict(self) -> dict:
        return self.__dict__


class UnBindingObject(BindingObject):
    URL = 'unBindCard.do'

    def finishTransaction(self, response: dict):
        return response


class ReBindingObject(BindingObject):
    URL = "bindCard.do"

    def finishTransaction(self, response: dict):
        return response


class BindPaymentObject(PaymentClasses):
    URL = "paymentOrderBinding.do"

    def __init__(self, mdOrder, bindingId, ip):
        self.mdOrder = mdOrder,
        self.bindingId = bindingId,
        self.ip = ip

    def as_dict(self) -> dict:
        return self.__dict__

    def finishTransaction(self, response: dict):
        pass


class PaymentService:
    URL = "https://web.rbsuat.com/ab/rest/"

    def __init__(self):
        self.userName = settings.PAYMENT['LOGIN']
        self.password = settings.PAYMENT['PASSWORD']
        self.merchantLogin = settings.PAYMENT['MERCHANT']

    def _toDict(self, obj: PaymentClasses):
        conct_dict = dict(self.__dict__)
        conct_dict.update(obj.as_dict())
        return conct_dict

    def _url(self, obj: PaymentClasses):
        if obj.URL == "":
            raise PaymentError(message=PaymentError.LOGICAL_MAP['URL_FORGET'], code=-1)
        return self.URL + obj.URL

    def _makeRequest(self, payment_object: PaymentClasses):
        conct_dict = self._toDict(payment_object)
        request_json = json.dumps(conct_dict)
        response = requests.post(url=self._url(payment_object), json=request_json)
        res_json = response.json()
        payment_object.checkOnError(res_json)
        return payment_object.finishTransaction(res_json)

    def registerOrder(self, register: RegisterObject) -> str:
        return self._makeRequest(register)

    def statusOrder(self, status: OrderStatusObject):
        return self._makeRequest(status)

    def bindingPayment(self, binding: BindPaymentObject):
        return self._makeRequest(binding)

    def unBind(self, bind: UnBindingObject):
        return self._makeRequest(bind)

    def reBind(self, reBind: ReBindingObject):
        return self._makeRequest(reBind)
