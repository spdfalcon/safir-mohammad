from django.urls import path
from .views import *

app_name = 'profiles'

urlpatterns = [ 
    path('', ProfileHomeView.as_view(), name='home'),
    path('scores/', ScoresView.as_view(), name='scores'),
    path('my_tickets/', MyTicketsView.as_view(), name='my_tickets'),
    path('myedu/', MyEduView.as_view(), name='myedu'),
    path('factors/', Factors.as_view(), name='factors'),
    path("tickets/", TicketView.as_view(), name="tickets"),
    path("ticket_detail/<int:pk>/", TicketDetailView.as_view(), name="ticket_detail"),
    path("ticket_create/", TicketCreateView.as_view(), name="ticket_create"),
    path("wallet/", UserWalletView.as_view(), name="user_wallet"),
]