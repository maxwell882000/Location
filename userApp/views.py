import sys

from django.shortcuts import render
from rest_framework import parsers, renderers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from logApp.models import AppLog
from userApp.serializers import *

# import module
import traceback


class VerifyCode(APIView):
    def post(self, request):
        pass


class UserView(APIView):
    serializer_class = UserSerilalizer
    def get(self, request, *args, **kwargs):
        serializers = self.serializer_class(request.user)
        return Response(serializers.data)



class RegisterUser(APIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'token': serializer.token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(AppLog.object.create(request, traceback.format_exc(), self),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

user_view = UserView.as_view()
register = RegisterUser.as_view()



class VerifyPhone(APIView):
    pass


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser,
                      parsers.MultiPartParser, parsers.JSONParser,)
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
        token, created = user.token
        return Response({'token': token.key}, status=status.HTTP_200_OK)


obtain_token = ObtainAuthToken.as_view()
