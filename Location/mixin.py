from django.http import QueryDict
from rest_framework.response import Response

class RequestCustom:
    data = {}

    def __init__(self, data: dict) -> None:
        self.data = QueryDict.copy(data)


class CustomCreateModelMixin:
    object_class = None

    def get_mutable_with_user(self, request):
        new_request = RequestCustom(request.data)
        new_request.data['user'] = request.user.id
        return new_request

    def create_custom(self, request, *args, **kwargs):
        new_request = self.get_mutable_with_user(request)
        return self.create(new_request, *args, **kwargs)

    def review_create(self, request, field_name, *args, **kwargs):
        new_request = self.get_mutable_with_user(request)
        object = self.object_class.objects.filter(
            user=request.user,
            specialist_id=new_request.data[field_name]
        )
        if object.exists(): 
            instance = object.first()
            serializer = self.get_serializer(instance, data=new_request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return self.create(new_request, *args,**kwargs)
class WithReviewMixin:
    review_serializer_class = None

    def retrieve(self, request, *arg,**kwargs):
        instance = self.get_object()
        review = instance.reviews.filter(user=request.user)
        serializer = {}
        if review.exists():
            serializer = self.serializer_class(review.first())
        return Response(serializer.data)