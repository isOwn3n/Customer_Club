from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from . import serializers
from . import models



class CustomerView(ModelViewSet):
    serializer_class = serializers.CustomerSerializer
    queryset = models.Customer.objects.all()
    authentication_classes = (JWTAuthentication,)

    def create_customer(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(f"DATA: {request.data}")
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=201)

# @api_view(["POST"])
# def create_customer(request):
#     serializer = serializers.CustomerSerializer("ali", "ezati", "all", 10)

#     return Response("OK", 200)
