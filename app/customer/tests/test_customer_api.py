from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Customer
from customer.serializers import CustomerSerializer

CREATE_CUSTOMER_URL = reverse('customer:create')
ALL_URL = reverse('customer:all')


def create_customer(**params):
    return get_user_model().objects.create_user(**params)


class PublicCustomerApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_customer_success(self):
        payload = {
            'email': 'customerapi1@email.com',
            'name': 'Test Customer 1',
            'age': '19',
            'phone': '5731245673829',
            'gender': 'M',
            'idType': 'C',
            'idNumber': '12342355'
        }
        res = self.client.post(CREATE_CUSTOMER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        customer = Customer.objects.get(email=payload['email'])
        # self.assertTrue(customer.check_password(payload['password']))
        # self.assertNotIn('password', res.data)

    def test_customer_with_email_exists_error(self):
        payload = {
            'email': 'customertwo@mail.com',
            'name': 'Test Customer 2',
            'age': '42',
            'phone': '11234235346234',
            'gender': 'F',
            'idType': 'E',
            'idNumber': '8214123553'
        }
        create_customer(**payload)
        res = self.client.post(CREATE_CUSTOMER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def setUp(self):
        self.user = create_customer(
            email='customerpu@mail.com',
            name='Test Customer 3',
            age='30',
            phone='423124893821',
            gender='M',
            idType='P',
            idNumber='734265476'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_all_customers(self):
        Customer.objects.create(
            email='test1@mail.com',
            name='Test Customer 4',
            age='1',
            phone='912390878049',
            gender='F',
            idType='C',
            idNumber='432154353'
        )
        Customer.objects.create(
            email='test2@mail.com',
            name='Test Customer 5',
            age='',
            phone='',
            gender='',
            idType='',
            idNumber=''
        )

        res = self.client.get(ALL_URL)

        customers = Customer.objects.all().order_by('-id')
        serializer = CustomerSerializer(customers, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_customer_not_allowed(self):
        payload = {
            'email': 'test@mail.com',
            'name': 'Test Customer 6',
            'age': '17',
            'phone': '567881389724',
            'gender': 'F',
            'idType': 'T',
            'idNumber': '1012331234543'
        }
        res = self.client.post(ALL_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_customer_not_allowed(self):
        payload = {
            'name': 'Updated Name',
            'email': 'Test Customer 6',
            'age': '29',
            'phone': '513436547368',
            'gender': 'I',
            'idType': 'E',
            'idNumber': '6534979900'
        }
        res = self.client.patch(ALL_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_customer_not_allowed(self):
        res = self.client.delete(ALL_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
