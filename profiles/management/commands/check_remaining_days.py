from django.core.management.base import BaseCommand
from django.utils import timezone
from main.utils import send_sms
from order.models import Order

class Command(BaseCommand):
    help = 'Checks remaining days for paid packages/courses and sends SMS notifications'

    def handle(self, *args, **options):
        # Get all paid orders
        paid_orders = Order.objects.filter(is_paid=True)

        for order in paid_orders:
            for item in order.items.all():
                remaining_days = item.calculate_remaining_days()
                if remaining_days is not None and remaining_days <= 15:
                    user = order.user
                    phone = user.phone  

                    # Send SMS notification
                    message = f''
                    text = f"""{ user.get_full_name } عزیز، کمتر از ۱۵ روز تا پایان مهلت استفاده از { item.get_title() } باقی مانده است.

                        لغو11
                    """
                    data = {
                        "phone": phone,
                        "text": text,
                    }
                    send_sms(data, 'course_expiration', user)
