from django.views import View
from django.shortcuts import render, redirect
from accounts.models import Wallet, TransactionHistory
from order.models import Order
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib import messages
from profiles.models import Scores
from django.urls import reverse
from django.http import HttpResponse
from django.urls import reverse
from .models import PaymentSession, WalletAmountSession
import requests
import time
import math
import json
import uuid


# token_api_url = "https://sep.shaparak.ir/onlinepg/onlinepg"
# verify_url = "https://sep.shaparak.ir/verifyTxnRandomSessionkey/ipg/VerifyTransaction"

# TerminalId = "14181170"
RedirectURL = "https://app.safirmall.com/payment/verify"


token_api_url = "https://sep.shaparak.ir/onlinepg/onlinepg"
verify_url = "https://sep.shaparak.ir/verifyTxnRandomSessionkey/ipg/VerifyTransaction"

TerminalId = "14181170"



class PaymentProcessView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        use_wallet = request.GET.get('use_wallet_flag')
        order = get_object_or_404(Order, id=request.session.get('order_id'))
        request.session['order'] = order.id 
        request.session['order_id'] = order.id  
        request.session.modified = True
        session_key = str(uuid.uuid4())
        ResNum = math.floor(time.time()*1000)
        # Store the order ID in the PaymentSession model
        PaymentSession.objects.create(user=request.user, order=order, session_key=session_key, type='payment')
        wallet = Wallet.objects.get(user=order.user)
        

        wallet_balance = None
        final_order_price = None

        if use_wallet == 'ON':
            order_price = order.get_price_after_discount()

            if wallet.balance >= order_price:
                wallet_balance = wallet.balance - order_price
                final_order_price = 0

            elif wallet.balance < order_price:
                final_order_price = order_price - wallet.balance

        else:
            final_order_price = order.get_price_after_discount()


        
        if final_order_price == 0:
            result = payment_for_zero_price(order, wallet_balance)
            return redirect(reverse('profiles:myedu') + result)

        data = {
            "Action": "Token",
            "Amount": final_order_price * 10, #convert to rial
            "Wage": 0,
            "TerminalId": TerminalId,
            "ResNum": ResNum,
            "RedirectURL": f"{RedirectURL}?session_key={session_key}", 
            "CellNumber": order.user.phone
        }

        print("data: ", data)

        result = requests.post(token_api_url, data)
        resObj = json.loads(result.text)

        WalletAmountSession.objects.create(user=request.user, amount=final_order_price, type='payment')

        if "status" not in resObj:
            return HttpResponse("ERROR : " + result.text)
        
        if resObj["status"] == 1:
            return redirect("https://sep.shaparak.ir/OnlinePG/SendToken?token=" + str(resObj['token']))
        
        return HttpResponse("ERROR CODE : " + str(resObj['status']))

@csrf_exempt
def callback_gateway_view(request):
    session_key = request.GET.get('session_key')  
    payment_session = get_object_or_404(PaymentSession, session_key=session_key)
    
    if payment_session.is_expired():
        return redirect(reverse('profiles:factors') + '?message=پرداخت ناموفق بود. لطفا پس از چند دقیقه مجددا امتحان کنید')

    order = payment_session.order
    state = request.POST.get("State", "Failed")

    if state != "OK":
        return redirect(reverse('profiles:factors') + '?message=پرداخت ناموفق بود. لطفا پس از چند دقیقه مجددا امتحان کنید')
        
    RefNum = request.POST.get("RefNum")

    data = {
        "TerminalNumber": TerminalId,
        "RefNum": RefNum
    }

    result = requests.post(verify_url, data)
    resObj = json.loads(result.text)

    if "Success" not in resObj:
        return redirect(reverse('profiles:factors') + '?message=پرداخت ناموفق بود. لطفا پس از چند دقیقه مجددا امتحان کنید')

    if resObj["Success"] == False:
        return redirect(reverse('profiles:factors') + '?message=پرداخت ناموفق بود. لطفا پس از چند دقیقه مجددا امتحان کنید')

    order.is_paid = True
    wallet = Wallet.objects.get(user=order.user)
    wallet.balance = 0
    wallet.save()

    order.paid_at = timezone.now()
    order.save()

    last_amount_session = WalletAmountSession.objects.filter(user=order.user, type='payment').last()

    message = f'پرداخت {last_amount_session.amount} از کیف پول جهت خرید محصول'

    TransactionHistory.objects.create(
        wallet=wallet,
        amount=last_amount_session.amount,
        transaction_type='C2',
        message=message
    )

    # Create scores for the user
    item_names = ', '.join(item.get_title() for item in order.items.all())
    description = f"پرداخت برای سفارش شماره {order.id} برای موارد: {item_names}"
    Scores.objects.create(user=order.user, score=1, description=description)
    
    for item in order.items.all():
        if item.package:
            item.package.increment_student_count()
        elif item.course:
            item.course.increment_student_count()
        else:
            item.part.increment_student_count()

    item_titles = ', '.join(item.get_title() for item in order.items.all())
    success_message = f'خرید {item_titles}" با موفقیت برای شما ثبت شد.'
    return redirect(reverse('profiles:myedu') + f'?message={success_message}')


@csrf_exempt
def payment_for_zero_price(order, wallet_balance):
    order.is_paid = True
    wallet = Wallet.objects.get(user=order.user)
    wallet.balance = wallet_balance
    wallet.save()
    order.paid_at = timezone.now()
    order.save()

    amount = order.get_price_after_discount()
    message = f'پرداخت {amount} از کیف پول جهت خرید محصول'
    TransactionHistory.objects.create(
        wallet=wallet,
        amount=amount,
        transaction_type='C2',
        message=message
    )
    # Create scores for the user
    item_names = ', '.join(item.get_title() for item in order.items.all())
    description = f"پرداخت برای سفارش شماره {order.id} برای موارد: {item_names}"
    Scores.objects.create(user=order.user, score=1, description=description)

    for item in order.items.all():
        if item.package:
            item.package.increment_student_count()
        elif item.course:
            item.course.increment_student_count()
        else:
            item.part.increment_student_count()

    item_titles = ', '.join(item.get_title() for item in order.items.all())
    success_message = f'خرید {item_titles}" با موفقیت برای شما ثبت شد.'
    return f'?message={success_message}'


class ChargeUserWalletView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        try:
            amount = int(amount)
        except Exception as e:
            messages.error(request, 'فیلد شرح تراکنش نمیتواند غیر عددی باشد.')
            return render(request, 'profiles/wallet_transaction.html')
            
        print(description)
        print("amount: ", amount)

        session_key = str(uuid.uuid4())
        ResNum = math.floor(time.time()*1000)
        # Store the order ID in the PaymentSession model
        PaymentSession.objects.create(user=request.user, session_key=session_key, type='charge')

        if not description:
            messages.error(request, 'فیلد شرح تراکنش نمیتواند خالی باشد.')
            return render(request, 'profiles/wallet_transaction.html')

        if not amount:
            messages.error(request, 'فیلد مبلغ نمیتواند خالی باشد.')
            return render(request, 'profiles/wallet_transaction.html')


        data = {
            "Action": "Token",
            "Amount": amount * 10,  # convert to rial
            "Wage": 0,
            "TerminalId": TerminalId,
            "ResNum": ResNum,
            "RedirectURL": f'https://app.safirmall.com/payment/callback-gateway-charge/?session_key={session_key}',
            "CellNumber": request.user.phone
        }

        print("data: ", data)

        result = requests.post(token_api_url, data)
        resObj = json.loads(result.text)

        WalletAmountSession.objects.create(user=request.user, amount=amount, type='charge', description=description)

        if "status" not in resObj:
            print("status not in resObj")
            return HttpResponse("ERROR : " + result.text)
        
        if resObj["status"] == 1:
            print("resObj['status'] == 1")
            return redirect("https://sep.shaparak.ir/OnlinePG/SendToken?token=" + str(resObj['token']))

        print('HttpResponse(ERROR CODE :  + str(resObj[status]))')
        return HttpResponse("ERROR CODE : " + str(resObj['status']))

@csrf_exempt
def callback_gateway_charge_view(request):
    session_key = request.GET.get('session_key') 
    payment_session = get_object_or_404(PaymentSession, session_key=session_key)

    if payment_session.is_expired():
        return redirect(reverse('profiles:factors') + '?message=پرداخت ناموفق بود. لطفا پس از چند دقیقه مجددا امتحان کنید')
    
    state = request.POST.get("State", "Failed")

    if state != "OK":
        return redirect(reverse('profiles:factors') + '?message=پرداخت ناموفق بود. لطفا پس از چند دقیقه مجددا امتحان کنید')

    RefNum = request.POST.get("RefNum")

    data = {
        "TerminalNumber": TerminalId,
        "RefNum": RefNum
    }

    result = requests.post(verify_url, data)
    resObj = json.loads(result.text)

    if "Success" not in resObj:
        return redirect(reverse('profiles:factors') + '?message=پرداخت ناموفق بود. لطفا پس از چند دقیقه مجددا امتحان کنید')

    if resObj["Success"] == False:
        return redirect(reverse('profiles:factors') + '?message=پرداخت ناموفق بود. لطفا پس از چند دقیقه مجددا امتحان کنید')


    
    last_amount_session = WalletAmountSession.objects.filter(user=payment_session.user, type='charge').last()

    wallet = Wallet.objects.get(user=payment_session.user)
    wallet.balance += last_amount_session.amount
    wallet.save()
    TransactionHistory.objects.create(
        wallet=wallet,
        amount=last_amount_session.amount,
        transaction_type='C1',
        charge_by='U',
        message=last_amount_session.description
    )

    messages.success(request, 'کیف پول شما به موقعیت شارژ شد')
    return redirect('profiles:home')