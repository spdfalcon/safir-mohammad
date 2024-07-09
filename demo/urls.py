from django.urls import path, include
from .views import DemoView

app_name = 'demo'

urlpatterns = [
    path('', DemoView.as_view(), name='demo'),
]
