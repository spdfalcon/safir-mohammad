from django.shortcuts import render, redirect
from products.models import *
from django.views.generic import ListView, View
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import PurchaseRequiredMixin
from django.db.models import Q
from order.models import Order
from django.contrib import messages
from django.http import JsonResponse


# ----------------------- Packages list ---------------------------------------
class PackagesView(LoginRequiredMixin, ListView):
    model = Package
    context_object_name = 'packages'
    template_name = 'edu/packages.html'


    def get(self, request, *args, **kwargs):
        if request.GET.get('export', None):
            return export_excel(self.get_queryset())
        return super().get(request, *args, **kwargs)
    
    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('paginate_by', None)
        if paginate_by:
            return paginate_by
        return 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects_count"] = self.get_queryset().count()
        categories_with_packages = Category.objects.filter(packages__isnull=False).distinct()
        context['categories'] = categories_with_packages
        return context
    
    def get_queryset(self):
        object_list = self.model.objects.all()
        
        # filters
        category_slug = self.request.GET.get('category_slug', None)
        order_by = self.request.GET.get('order_by', None)
        ordering = self.request.GET.get('ordering', None)

        
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            object_list = object_list.filter(categories=category)

        if order_by and ordering:
            if ordering == "asc":
                object_list = object_list.order_by(f"{order_by}")
            elif ordering == "desc":
                object_list = object_list.order_by(f"-{order_by}")

        return object_list 
    
# ----------------------- Package detail/list of course -----------------------
class PackageDetailView(LoginRequiredMixin, View):
    template_name = 'edu/package_detail.html'

    def get(self, request, *args, **kwargs):
        context = {}
        package_slug = self.kwargs.get('package_slug') 
        package = get_object_or_404(Package, slug=package_slug)
        context['package'] = package
        context['comments'] = package.package_comments.filter(is_active=True)
        
        # Check if the user has purchased the package or any course in the package
        user = request.user
        has_purchased = Order.objects.filter(
            Q(user=user, items__package=package) |
            Q(user=user, items__course__in=package.courses.all()), 
            is_paid=True
        ).exists()

        if not has_purchased:
            context['show_buy_link'] = True

        if package.price == 0:
            context['show_buy_link'] = False


        # Check if the package has chapters
        package_has_chapters = any(course.chapters.exists() for course in package.courses.all())
        context['package_has_chapters'] = package_has_chapters

        if not package_has_chapters:
            # If the package has no chapters, retrieve the parts
            parts = Part.objects.filter(course__in=package.courses.all())
            context['parts'] = parts

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        rate = request.POST.get('rating')
        package_slug = self.kwargs.get('package_slug') 
        content = request.POST.get('content')
        package = get_object_or_404(Package, slug=package_slug)
        if not Comment.objects.filter(user=request.user, package=package, course=None, rate=rate, content=content):
            Comment.objects.create(user=request.user, package=package, course=None, rate=rate, content=content)
            messages.success(request, 'نظر شما ثبت گردید.')
        return redirect('edu:package_detail', package_slug=package_slug)

# ----------------------- Course detail/list of chapters ----------------------
class CourseDetailView(LoginRequiredMixin, View):
    template_name = 'edu/course_detail.html'

    def get(self, request, *args, **kwargs):
        context = {}
        course_slug = self.kwargs.get('course_slug') 
        course = get_object_or_404(Course, slug=course_slug)
        context['course'] = course
        user = request.user
        if user.is_authenticated:
            has_purchased = Order.objects.filter(Q(user=user, items__course=course), is_paid=True).exists()
            if has_purchased:
                # Check if any related package has been purchased
                related_packages = Package.objects.filter(courses=course)
                for package in related_packages:
                    if Order.objects.filter(user=user, items__package=package, is_paid=True).exists():
                        break
            else:
                # Neither course nor related package has been purchased
                context['show_buy_link'] = True

            if course.price == 0:
                context['show_buy_link'] = False

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        rate = request.POST.get('rating')
        course_slug = self.kwargs.get('course_slug') 
        content = request.POST.get('content')
        course = get_object_or_404(Course, slug=course_slug)
        if not Comment.objects.filter(user=request.user, package=None, course=course, rate=rate, content=content):
            Comment.objects.create(user=request.user, package=None, course=course, rate=rate, content=content)
            messages.success(request, 'نظر شما ثبت گردید.')
        return redirect('edu:course_detail', course_slug=course_slug)

# ----------------------- Chapter detail/list of parts ------------------------
class ChapterDetailView(LoginRequiredMixin, PurchaseRequiredMixin, View):
    template_name = 'edu/chapter_detail.html'

    def get(self, request, *args, **kwargs):
        context = {}
        chapter_slug = self.kwargs.get('chapter_slug') 
        chapter = get_object_or_404(Chapter, slug=chapter_slug)
        context['chapter'] = chapter
        return render(request, self.template_name, context)

# ----------------------- Part detail -----------------------------------------
class PartDetailView(LoginRequiredMixin, View):
    template_name = 'edu/part_detail.html'

    def get(self, request, *args, **kwargs):
        context = {}
        part_slug = self.kwargs.get('part_slug') 
        part = get_object_or_404(Part, slug=part_slug)
        context['part'] = part
        user = request.user
        
        
        has_purchased = Order.objects.filter(
                Q(user=user) & Q(is_paid=True) & (
                    Q(items__part=part) |
                    Q(items__course=part.course)
                )
            ).exists()

        if not has_purchased:
            context['show_buy_link'] = True
        
        if part.price == 0:
            context['show_buy_link'] = False

        return render(request, self.template_name, context)

# ----------------------- Courses list ---------------------------------------
class CoursesView(LoginRequiredMixin, ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'edu/courses.html'


    def get(self, request, *args, **kwargs):
        if request.GET.get('export', None):
            return export_excel(self.get_queryset())
        return super().get(request, *args, **kwargs)
    
    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('paginate_by', None)
        if paginate_by:
            return paginate_by
        return 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects_count"] = self.get_queryset().count()
        categories_with_courses = Category.objects.filter(courses__isnull=False).distinct()
        context['categories'] = categories_with_courses
        return context
    
    def get_queryset(self):
        object_list = self.model.objects.all()
        
        # filters
        category_slug = self.request.GET.get('category_slug', None)
        search = self.request.GET.get('search', None)
        order_by = self.request.GET.get('order_by', None)
        ordering = self.request.GET.get('ordering', None)


        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            object_list = object_list.filter(Q(categories=category) | Q(package__categories=category))

        if search and 'all' not in search:
            object_list = object_list.filter(Q(title__icontains=search) | Q(description__icontains=search))
        
        if order_by and ordering:
            if ordering == "asc":
                object_list = object_list.order_by(f"{order_by}")
            elif ordering == "desc":
                object_list = object_list.order_by(f"-{order_by}")

        return object_list 
    
# ----------------------- Parts list ---------------------------------------
class PartsView(LoginRequiredMixin, ListView):
    model = Part
    context_object_name = 'parts'
    template_name = 'edu/parts.html'


    def get(self, request, *args, **kwargs):
        if request.GET.get('export', None):
            return export_excel(self.get_queryset())
        return super().get(request, *args, **kwargs)
    
    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('paginate_by', None)
        if paginate_by:
            return paginate_by
        return 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects_count"] = self.get_queryset().count()
        categories_with_parts = Category.objects.filter(parts__isnull=False).distinct()
        context['categories'] = categories_with_parts
        return context
    
    def get_queryset(self):
        object_list = self.model.objects.all()
        
        # filters
        category_slug = self.request.GET.get('category_slug', None)
        order_by = self.request.GET.get('order_by', None)
        ordering = self.request.GET.get('ordering', None)

        
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            object_list = object_list.filter(category=category)

        if order_by and ordering:
            if ordering == "asc":
                object_list = object_list.order_by(f"{order_by}")
            elif ordering == "desc":
                object_list = object_list.order_by(f"-{order_by}")

        return object_list 
    
