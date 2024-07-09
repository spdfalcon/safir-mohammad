from django.urls import path
from .views import OrderCreateView, OrderProcessView


app_name = 'order'


urlpatterns = [
    path('order_create/', OrderCreateView.as_view(), name='order_create'), 
    path('order_process/', OrderProcessView.as_view(), name='order_process'), 

]