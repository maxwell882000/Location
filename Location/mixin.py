from django.http import QueryDict
from rest_framework.response import Response

import copy

from commonApp.models import TempImage


class RequestCustom:
    data = None

    def __init__(self, data: dict) -> None:
        self.data = copy.deepcopy(data)


class CustomCreateModelMixin:
    object_class = None

    def get_mutable_with_user(self, request):
        new_request = RequestCustom(request.data)
        new_request.data['user'] = request.user.id
        return new_request

    def create_temp(self, request, field_name, *args, **kwargs):
        new_request = RequestCustom(request.data)
        new_request.data[field_name] = TempImage.objects.get(
            id=request.data[field_name]).temp
        return self.create(new_request, *args, **kwargs)

    def update_temp(self, request, field_name, *args, **kwargs):
        new_request = RequestCustom(request.data)
        if field_name in new_request.data:
            new_request.data[field_name] = TempImage.objects.get(
                id=request.data[field_name]).temp
        return self.partial_update(new_request, *args, **kwargs)

    def create_custom(self, request, *args, **kwargs):
        new_request = self.get_mutable_with_user(request)
        return self.create(new_request, *args, **kwargs)
    
    def review_create(self, request, field_name, *args, **kwargs):
        new_request = self.get_mutable_with_user(request)
        filters = {
            "user": request.user,
            "{}_id".format(field_name): new_request.data[field_name]
        }
        object = self.object_class.objects.filter(**filters)
        #     """   user=request.user,
        # specialist_id=new_request.data[field_name] """
        if object.exists():
            instance = object.first()
            serializer = self.get_serializer(
                instance,
                data=new_request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return self.create(new_request, *args, **kwargs)


class WithReviewMixin:
    review_serializer_class = None

    def retrieve(self, request, *arg, **kwargs):
        instance = self.get_object()
        review = instance.reviews.filter(user=request.user)
        if review.exists():
            serializer = self.serializer_class(review.first())
            return Response(serializer.data)
        return Response({})
