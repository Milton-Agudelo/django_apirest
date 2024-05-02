from django.urls import path
from rest_framework.routers import DefaultRouter
from customer import views

app_name = 'customer'

router = DefaultRouter()
router.register('', views.CustomerViewSet, basename='customer')

urlpatterns = [
    path('<str:id_number>',
         views.CustomerViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}),
         name='customer-handle'),
    path('',
         views.CustomerViewSet.as_view({'get': 'list', 'post': 'create'}))
]
