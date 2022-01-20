from django.shortcuts import render
from rest_framework import generics, mixins, views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from commonApp.models import CommonIcon, CommonLogo, TempImage
from commonApp.serializers import CommonIconSerializer, CommonLogoSerializer, TempSerializer


class CommonApiView(views.APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        icon = CommonIcon.objects.all()
        logo = CommonLogo.objects.first()

        serialized_icon = CommonIconSerializer(icon, many=True)
        serialized_logo = CommonLogoSerializer(logo)
        response = {
            'logo': serialized_logo.data,
            'icon': serialized_icon.data
        }
        return Response(response, status=status.HTTP_200_OK)


common = CommonApiView.as_view()


class TempImageStore(generics.GenericAPIView, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = TempImage.objects.all().order_by('-id')
    permission_classes = [AllowAny]
    serializer_class = TempSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request,*args,**kwargs)

temp_view = TempImageStore.as_view()
