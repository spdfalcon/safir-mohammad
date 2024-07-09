from django.urls import path
from .views import PaymentProcessView, callback_gateway_view, payment_for_zero_price, ChargeUserWalletView, callback_gateway_charge_view

app_name = 'payment'

urlpatterns = [
    path('payment/', PaymentProcessView.as_view(), name='payment_process'),
    path('verify', callback_gateway_view, name='callback_gateway'), 
    path('zero-price/', payment_for_zero_price, name='zero_price_payment'),
    path('wallet-charge/', ChargeUserWalletView.as_view(), name='charge_wallet_by_user'),
    path('callback-gateway-charge/', callback_gateway_charge_view, name='callback_gateway-charge'),
]