""" core URL Configuration """

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from azbankgateways.urls import az_bank_gateways_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Accounts Urls 
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    
    # Main Urls
    path('', include('main.urls', namespace='main')),
    path('products/', include('products.urls', namespace='products')),
    path('panel/', include('panel.urls', namespace='panel')),
    path('edu/', include('edu.urls', namespace='edu')),
    path('order/', include('order.urls', namespace='order')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('ticket/', include('ticket.urls', namespace='ticket')),
    path('wishlist/', include('wishlist.urls', namespace='wishlist')),
    path('cart/', include('cart.urls', namespace='cart')),  

    path('bankgateways/', az_bank_gateways_urls()),

    path("", include("pwa.urls")),
]


# Development
if bool(settings.DEBUG):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)