from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.utils import timezone
from accounts.models import User, Wallet
from ticket.models import Ticket, DefaultMessage
from order.models import Order
from ticket.forms import MessageForm
from .models import Scores
from django.contrib import messages
from jdatetime import datetime as jdatetime



# ------------------------------ Profile Show/Edit Views --------------------
class ProfileHomeView(LoginRequiredMixin, SuccessMessageMixin, generic.View):
    model = User
    template_name = 'profiles/profile.html'
    success_url = reverse_lazy('profiles:home')
    success_message = 'به‌روزرسانی انجام گردید.'

    def get(self, request, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, **kwargs):
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        date_of_birth = request.POST.get('date_of_birth', None)

        context = {
            'first_name': first_name, 
            'last_name': last_name, 
            'date_of_birth': date_of_birth
        }

        errors = []

        if not first_name:
            errors.append('نام خود را وارد کنید.')
        
        if not last_name:
            errors.append('نام خانوادگی خود را وارد کنید.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'profiles/profile.html', context)
        
        new_date_of_birth = None
      
        j_date_of_birth = None
        if date_of_birth:
            print(date_of_birth)

            # Parse Jalali date using jdatetime constructor
            j_date_of_birth = jdatetime.strptime(date_of_birth, '%Y/%m/%d')
            # Convert to Gregorian date
            new_date_of_birth = j_date_of_birth.togregorian().date()
            
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.date_of_birth = new_date_of_birth
        request.user.save()

        messages.success(request, 'تغییرات انجام شد.')
        return redirect('profiles:home')



    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['orders_paid'] = self.get_object().user_orders.filter(is_paid=True)
        context['orders_not_paid'] = self.get_object().user_orders.filter(is_paid=False)
        context['tickets'] = self.get_object().user_tickets.all()
        return context
    
# ------------------------------ MyEdu(order paid) List Views --------------------
class MyEduView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'profiles/myedu.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_paid=True)
    
        
# ------------------------------ Factors(Order not paid) List Views --------------------
class Factors(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'profiles/factors.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
        
# ------------------------------ Scores List Views --------------------
class ScoresView(LoginRequiredMixin, generic.View):
    template_name = 'profiles/scores.html'

    def get(self, request, *args, **kwargs):
        context = {}
        scores = Scores.objects.filter(user=request.user)
        context['scores'] = scores
        context['total_user_scores'] = scores.aggregate(total=Sum('score'))['total']


        return render(request, self.template_name, context)

    

# ------------------------------ Ticket List Views --------------------
class MyTicketsView(LoginRequiredMixin, generic.ListView):
    model = Ticket
    template_name = 'profiles/my_tickets.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)
    
        

# ----------------------- Ticket list -----------------------
class TicketView(LoginRequiredMixin, generic.ListView):
    model = Ticket
    context_object_name = "tickets"
    template_name = "profiles/tickets.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get("paginate_by", None)
        if paginate_by:
            return paginate_by
        return 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects_count"] = self.get_queryset().count()
        return context

    def get_queryset(self):
        object_list = self.model.objects.filter(user=self.request.user)
        return object_list

# ----------------------- Detail Ticket -----------------------
class TicketDetailView(LoginRequiredMixin, generic.View):
    model = Ticket
    template_name = "profiles/ticket_detail.html"

    def get(self, request, *args, **kwargs):
        form = MessageForm()
        ticket = get_object_or_404(Ticket, pk=kwargs["pk"])
        default_message = self.get_default_message()
        admin_message = ticket.messages.filter(admin_reply=True)
        print(admin_message)
        return render(request, self.template_name, {"ticket": ticket, "form": form, 'default_message': default_message})

    def post(self, request, *args, **kwargs):
        ticket = get_object_or_404(Ticket, pk=kwargs["pk"])
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.ticket = ticket
            message.save()
            return redirect("profiles:ticket_detail", pk=ticket.pk)
        return render(request, self.template_name, {"ticket": ticket, "form": form})
    
    def get_default_message(self):
        current_time = timezone.now().time()
        current_day = timezone.now().date().weekday()  # Monday is 0 and Sunday is 6
        if current_time.hour >= 18 or current_time.hour < 8 or current_day in [3, 4]:  # Thursday is 3, Friday is 4
            return DefaultMessage.objects.first()
        return None

# ----------------------- Create Ticket -----------------------
class TicketCreateView(LoginRequiredMixin, generic.CreateView, SuccessMessageMixin):
    model = Ticket
    fields = ("title", "description", "priority")
    template_name = "profiles/create_ticket.html"
    success_url = reverse_lazy("profiles:tickets")
    success_message = "تیکت جدید ایجاد گردید"


    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.user = self.request.user
        ticket.save()
        return super().form_valid(form)


class UserWalletView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        user = request.user
        wallet = get_object_or_404(Wallet, user=user)
        transactions = wallet.transactions.all().order_by('-created_at')
        return render(
            request,
            'profiles/wallet_transaction.html',
            context={'wallet': wallet, 'transactions': transactions}
        )


class ChargeUserWalletView(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        if not description:
            messages.error(request, 'فیلد شرح تراکنش نمیتواند خالی باشد')
            return render(request, 'profiles/wallet_transaction.html')

        if not amount:
            messages.error(request, 'فیلد مبلغ نمیتواند خالی باشد')
            return render(request, 'profiles/wallet_transaction.html')

        print('hello', amount, description)
        return redirect(request, 'profiles/wallet_transaction.html', )
