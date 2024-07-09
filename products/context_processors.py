from .models import Professor, Package, Course, Category, Chapter, Part
from django.db.models import Count
from order.models import Order
from accounts.models import User


def top_professors(request):
    top_professors = Professor.objects.annotate(course_count=Count('courses')).order_by('-course_count')[:10]
    return {'top_professors': top_professors}    

def categories(request):
    categories = Category.objects.all()
    return {'categories': categories}

def professors(request):
    professors = Professor.objects.all()
    return {'professors': professors}

def packages(request):
    packages = Package.objects.all()
    return {'packages': packages}

def courses(request):
    courses = Course.objects.all()
    return {'courses': courses}

def chapters(request):
    chapters = Chapter.objects.all()
    return {'chapters': chapters}

def parts(request):
    parts = Part.objects.all()
    return {'parts': parts}

def users(request):
    users = User.objects.all()
    return {'users': users}

def packages_in_orders(request):
    return {
        'packages_in_orders': Package.objects.filter(
            order_items__order__is_paid=True
        ).annotate(
            num_orders=Count('order_items__order', distinct=True)
        ).filter(
            num_orders__gt=0
        ).distinct()
    }

def courses_in_orders(request):
    return {
        'courses_in_orders': Course.objects.filter(
            order_items__order__is_paid=True
        ).annotate(
            num_orders=Count('order_items__order', distinct=True)
        ).filter(
            num_orders__gt=0
        ).distinct()
    }