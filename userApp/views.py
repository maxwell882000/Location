from functools import partial
import sys

from django.shortcuts import render
from rest_framework import mixins, parsers, renderers, status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from logApp.models import AppLog
from userApp.serializers import *

# import module
import traceback
from Location.permissions import phone_permission


class VerifyCode(generics.GenericAPIView):
    permission_classes = [AllowAny]
    model = User
    lookup_field = 'phone'
    queryset = User.object.order_by("-id")

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            user = self.get_object()
        user.phone_validation.save()
        return Response({
            'status': True
        })

    def post(self, request, *args, **kwargs):
        code = request.data['code']
        user = request.user
        if not user.is_authenticated:
            user = self.get_object()
            is_valid = user.phone_validation.password_validate(code)
        else:
            is_valid = user.phone_validation.validate(code)
        return Response({
            'status': is_valid
        })

    def put(self, request, *args, **kwargs):
        code = request.data['code']
        is_valid = self.get_object().phone_validation.password_validate(code)
        return Response({
            'status': is_valid
        })


class CheckPhone(APIView):
    permission_classes = phone_permission

    def get(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)


check_view = CheckPhone.as_view()
verify_code = VerifyCode.as_view()


class UserView(APIView):
    serializer_class = UserSerilalizer

    def get(self, request, *args, **kwargs):
        serializers = self.serializer_class(request.user)
        return Response(serializers.data)


class RegisterUser(APIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class UpdateUser(APIView, ):
    serializer_class = UpdateUserSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


update = UpdateUser.as_view()
user_view = UserView.as_view()
register = RegisterUser.as_view()


class ForgetPasswordView(generics.GenericAPIView, mixins.UpdateModelMixin):
    serializer_class = NewPasswordSerializer
    permission_classes = [AllowAny]
    lookup_field = 'phone'
    queryset = User.object.order_by("-id")

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        if not user.is_phone_reset_validate:
            return Response({
                'status': False,
                'error': "Код не был подтвержден",
            })
        self.partial_update(request, *args, **kwargs)
        return Response({
            'status': True
        })


forget_password = ForgetPasswordView.as_view()


class ChangePasswordView(APIView):
    """
    An endpoint for changing password.
    """
    serializer_class = PasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


password_change = ChangePasswordView.as_view()


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser,
                      parsers.MultiPartParser, parsers.JSONParser)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = TokenSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response({'token': user.token}, status=status.HTTP_200_OK)


obtain_token = ObtainAuthToken.as_view()
