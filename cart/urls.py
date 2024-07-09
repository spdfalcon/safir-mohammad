from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('item_add/<int:id>/', views.item_add, name='item_add'),
    path('item_clear/<int:id>/<str:product_type>/', views.item_clear, name='item_clear'),
    path('cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart_detail/', views.cart_detail, name='cart_detail'),
]
