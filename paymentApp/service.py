import json
from abc import ABC, abstractmethod

import requests
from django.conf import settings

from paymentApp.models import OrderStatus
from specialistApp.models import Specialist


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
        "NOT_FOUND": "Заказ не был найден."
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
        if 'errorCode' in response and response['errorCode'] != 0:
            print(response)
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
               "link=https://sportandthecity.page.com/?route=" + query + \
               "&path=&apn=com.location_specialist.location_specialist&isi=1619132873&" \
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
        self.order_unique.save()
        return {"formUrl": response['formUrl']}


class OrderStatusObject(PaymentClasses):
    URL = "getOrderStatus.do"

    def __init__(self, user_specialist):
        self.specialist = user_specialist
        self.orderId = user_specialist.order_unique.last().orderId

    def checkOnError(self, response: dict):
        super().checkOnError(response)
        if 'OrderStatus' not in response:
            raise PaymentOrderError(message=PaymentOrderError.MAP["NOT_FOUND"], code=-1)
        else:
            orderStatus = response['OrderStatus']
            if response['OrderStatus'] != 2:
                raise PaymentOrderError(message=PaymentOrderError.MAP[orderStatus], code=orderStatus)

    def finishTransaction(self, response: dict):
        bindingId = response['bindingId'] if 'bindingId' in response else None
        OrderStatus.objects.update_or_create(order_id=self.specialist.id,
                                             defaults={
                                                 'ip': response['Ip'],
                                                 'bindingId': bindingId
                                             })
        self.specialist.days_activated += self.specialist.plan.days
        self.specialist.save()
        return {"is_auto_payment": bindingId is not None}

    def as_dict(self) -> dict:
        as_dict = dict(self.__dict__)
        del as_dict['specialist']
        print(as_dict)
        return as_dict


class BindingObject(PaymentClasses, ABC):
    def __init__(self, user):
        self.order_status = user.user_specialist.order_status
        self.bindingId = self.order_status.bindingId

    def as_dict(self) -> dict:
        as_dict = dict(self.__dict__)
        del as_dict['order_status']
        return as_dict


class UnBindingObject(BindingObject):
    URL = 'unBindCard.do'

    def finishTransaction(self, response: dict):
        self.order_status.bindingId = None
        self.order_status.save()
        return response


class ReBindingObject(BindingObject):
    URL = "bindCard.do"

    def finishTransaction(self, response: dict):
        return response


class BindPaymentObject(PaymentClasses):
    URL = "paymentOrderBinding.do"

    def __init__(self, specialist: Specialist):
        self.mdOrder = specialist.order_unique.last().orderId,
        self.bindingId = specialist.order_status.bindingId,
        self.ip = specialist.order_status.ip
        self.specialist = specialist

    def as_dict(self) -> dict:
        as_dict = dict(self.__dict__)
        del as_dict['specialist']
        return as_dict

    def finishTransaction(self, response: dict):
        self.specialist.days_activated += self.specialist.plan.days
        self.specialist.save()


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
        print(conct_dict)
        request_json = json.dumps(conct_dict)
        response = requests.post(url=self._url(payment_object), params=conct_dict)
        res_json = response.json()
        print(res_json)
        try:
            payment_object.checkOnError(res_json)
            return payment_object.finishTransaction(res_json)
        except PaymentError as e:
            print(e.message)
            return {
                "errors": e.message,
                "payment": True,
            }

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
