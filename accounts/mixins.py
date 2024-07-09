from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages


# Only superusers
class AdminAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_superuser:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

class AdminPanelAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_panel_admin:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

# Only users that verify their phone number and email address
class UserVerificationMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not (user.valid_phone and user.valid_email):
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)


# Only superusers, managers and users who are members of the organization that has access to the report.
class DashboardAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not (user.is_superuser or user.is_panel_admin):
            if user.is_active:
                if request.path not in user.dashboards.values_list('path', flat=True):
                        return render(request, 'error_pages/page_403.html',status=403)
            else:
                return render(request, 'error_pages/page_403.html',status=403)
        return super().dispatch(request, *args, **kwargs)
    
class PurchaseRequiredMixin:
    purchase_redirect = reverse_lazy('accounts:not_access')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            # Check if the user has purchased the course or any related package
            has_purchased_part = user.user_orders.filter(is_paid=True, items__part__isnull=False).exists()
            has_purchased_course = user.user_orders.filter(is_paid=True, items__course__isnull=False).exists()
            has_purchased_package = user.user_orders.filter(is_paid=True, items__package__isnull=False).exists()
            if not (has_purchased_part or has_purchased_course or has_purchased_package):
                messages.warning(request, "شما باید ابتدا مجموعه‌ها یا دسته بندی‌های مربوطه را خریداری کنید.")
                return redirect(self.purchase_redirect)
            else:
                # At least one of course or package is paid, so the user should have access
                return super().dispatch(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)