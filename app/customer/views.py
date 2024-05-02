from rest_framework import viewsets, status
from rest_framework.response import Response
from core.models import Customer
from .serializers import CustomerSerializer
from django.shortcuts import get_object_or_404


# Customer View Set
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def list(self, request):
        customers = self.get_queryset()
        serializer = self.get_serializer(customers, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, id_number=None):
        customer = get_object_or_404(Customer, idNumber=id_number)
        serializer = self.get_serializer(customer)
        return Response(serializer.data)

    def update(self, request, id_number=None):
        customer = get_object_or_404(Customer, idNumber=id_number)
        serializer = self.get_serializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, id_number=None):
        customer = get_object_or_404(Customer, idNumber=id_number)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
