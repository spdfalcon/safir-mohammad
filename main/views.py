from typing import Any
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from products.models import Category, Course, Package, Part
from .models import MainBanner, WebSites
from itertools import chain
from django.shortcuts import get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.http import JsonResponse
import json



class HomeView(LoginRequiredMixin, generic.View):
    template_name = 'main/home.html'

    def get(self, request, *args, **kwargs):
        context = {}
        context['top_categories'] = Category.objects.order_by('-student_count')[0:12]
        context['top_courses'] = Course.objects.order_by('-student_count')[0:10]
        context['free_courses'] = Course.objects.filter(Q(price=0))[0:10]
        context['main_banner'] = MainBanner.objects.first()
        context['websites'] = WebSites.objects.all()
        return render(request, self.template_name, context)
    
class AboutView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'main/about.html'
    
class ContactView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'main/contact.html'
    
class RulesView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'main/rules.html'
    
class SearchView(LoginRequiredMixin, generic.View):
    template_name = 'main/search.html'

    def get(self, request, *args, **kwargs):
        context = {}
        search = self.request.GET.get('search', '')
        context['search'] = search
        if search:
            packages = Package.objects.filter(Q(title__contains=search) | Q(description__contains=search) | Q(meta_title__contains=search) | Q(meta_description__contains=search))
            courses = Course.objects.filter(Q(title__contains=search) | Q(description__contains=search))
        else:
            packages = []
            courses = []
        context['search_result'] = chain(packages, courses)
        return render(request, self.template_name, context)
    
class CategoriesView(LoginRequiredMixin, generic.ListView):
    template_name = 'main/categories.html'
    model = Category
    context_object_name = 'categories'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        categories_with_packages = Category.objects.filter(packages__isnull=False).distinct()
        context['categories_wtih_package'] = categories_with_packages
        categories_with_courses = Category.objects.filter(courses__isnull=False).distinct()
        context['categories_with_courses'] = categories_with_courses
        categories_with_parts = Category.objects.filter(parts__isnull=False).distinct()
        context['categories_with_parts'] = categories_with_parts
        return context

class CategoryDetailView(LoginRequiredMixin, generic.View):
    template_name = 'main/category_detail.html'

    def get(self, request, *args, **kwargs):
        context = {}
        category_slug = self.kwargs.get('category_slug') 
        category = get_object_or_404(Category, slug=category_slug)
        context['category'] = category
        context['packages'] = Package.objects.filter(categories__in=[category])
        context['courses'] = Course.objects.filter(categories__in=[category])
        context['parts'] = Part.objects.filter(category=category)
        return render(request, self.template_name, context)

class OthersView(LoginRequiredMixin, generic.View):
    template_name = 'main/others.html'
    
    def get(self, request, *args, **kwargs):
        objects = None
        packages = Package.objects.filter(categories__isnull=True)
        courses = Course.objects.filter(Q(package=None))
        # courses_without_chapters = Course.objects.annotate(num_chapters=Count('chapters')).filter(num_chapters=0)

        objects = chain(packages, courses)
        return render(request, self.template_name, {'objects': objects})

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'get_absolute_url'):
            data = {
                'url': obj.get_absolute_url(),
                'title': obj.title,
            }
            data['img'] = None
            if hasattr(obj, 'image'):
                if obj.image:
                    data['img'] = obj.image.url
            
            return data
        return super().default(obj)

class SearchResultsAjax(generic.View):

    def get(self, request, *args, **kwargs):
        search_filter = self.request.GET.get('search', None)
        packages = Package.objects.none()
        courses = Course.objects.none()
        parts = Part.objects.none()

        if search_filter:
            packages = Package.published.filter(Q(title__contains=search_filter) | Q(description__contains=search_filter)).distinct()
            courses = Course.published.filter(Q(title__contains=search_filter) | Q(description__contains=search_filter)).distinct()
            parts = Part.published.filter(Q(title__contains=search_filter) | Q(description__contains=search_filter)).distinct()
        

        # Serializing the querysets
        packages_serialized = json.dumps(list(packages), cls=CustomJSONEncoder)
        courses_serialized = json.dumps(list(courses), cls=CustomJSONEncoder)
        parts_serialized = json.dumps(list(parts), cls=CustomJSONEncoder)

        default_icon_path = settings.STATIC_URL + 'img/default.png'
        # Constructing context with serialized data
        context = {
            'packages': packages_serialized,
            'packages_count': packages.count(),
            'courses': courses_serialized,
            'courses_count': courses.count(),
            'parts': parts_serialized,
            'parts_count': parts.count(),
            'default_icon_path': default_icon_path,
        }
        
        # Returning JsonResponse with context
        return JsonResponse(context)
