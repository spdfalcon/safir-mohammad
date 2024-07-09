from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F
from django.views import generic
from django.urls import reverse_lazy,reverse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from accounts.mixins import *
from accounts.models import *
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from products.models import Category, Package, Course, Chapter, Part, Professor, Comment
from main.models import MainBanner, WebSites
from ticket.models import Ticket, Message, DefaultMessage
from order.models import Order, OrderItem, Discount
from accounts.mixins import DashboardAccessMixin
from ticket.utils import TICKET_PRIORITY_CHOICES, TICKET_STATUS_CHOICES
from ticket.forms import MessageForm, DefaultMessageForm, MainBannerForm
from datetime import datetime
from django.http import JsonResponse
import uuid
import json 
import requests
from .models import NotificationLog, MinimumCartCost
from main.utils import export_excel

#------------------------ Panel View ------------------------
class PanelView(LoginRequiredMixin, DashboardAccessMixin, generic.View):
    template_name = 'panel/home.html'

    def get(self, request, *args, **kwargs):
        context = {}
        context["packages_count"] = Package.objects.count()
        context["courses_count"] = Course.objects.count()
        context["users_count"] = User.objects.count()
        context["parts_count"] = Part.objects.count()
        context["count_of_user_buy"] = Order.objects.values('user').distinct().count()
        paid_orders = Order.objects.filter(is_paid=True)
        total_sell_price = sum(order.get_price_after_discount() for order in paid_orders)
        context["total_sell_price"] = total_sell_price
        return render(request, self.template_name, context)

# ----------------------- User List -----------------------
class UserView(LoginRequiredMixin, DashboardAccessMixin, generic.ListView):
    model = User
    context_object_name = 'users'
    template_name = 'panel/user/users.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('export', None):
            return export_excel(self.get_queryset())
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects_count"] = self.get_queryset().count()
        return context

#------------------------ Create User ------------------------
class UserCreateView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.CreateView):
    model = User
    context_object_name = 'user'
    fields = ('username', 'first_name', 'last_name', 'phone', 'email', 'valid_phone', 'valid_email', 
              'date_of_birth', 'is_panel_admin', 'dashboards', )
    success_message = 'کاربر ایجاد گردید.'
    template_name = 'panel/user/user_create.html'

    def get_success_url(self):
        return reverse('panel:users')
    
#------------------------ Edit User ------------------------
class UserEditView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.UpdateView):
    model = User
    context_object_name = 'user'
    fields = ('username', 'first_name', 'last_name', 'phone', 'email', 'valid_phone', 'valid_email', 
              'date_of_birth', 'is_panel_admin', 'dashboards')
    success_message = 'کاربر ویرایش شد.'
    template_name = 'panel/user/user_edit.html'

    def get_success_url(self):
        return reverse('panel:users')
    
#------------------------ Delete User ------------------------
class UserDeleteView(LoginRequiredMixin, DashboardAccessMixin,  SuccessMessageMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy('panel:users')
    success_message = "کاربر حذف گردید"  

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        messages.success(request, self.success_message)
        self.object.delete()
        return HttpResponseRedirect(success_url)
    
# ----------------------- Professor List -----------------------
class ProfessorView(LoginRequiredMixin, DashboardAccessMixin, generic.ListView):
    model = Professor
    context_object_name = 'professors'
    template_name = 'panel/professor/professors.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('export', None):
            return export_excel(self.get_queryset())
        return super().get(request, *args, **kwargs)
    
#------------------------ Create Professor ------------------------
class ProfessorCreateView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.CreateView):
    model = Professor
    context_object_name = 'professor'
    fields = ('user', 'first_name', 'last_name', 'slug', 'phone', 'image', 'specialty', 'is_active')
    success_message = 'استاد ایجاد گردید.'
    template_name = 'panel/professor/professor_create.html'

    def get_success_url(self):
        return reverse('panel:professors')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['users'] = User.objects.all()
        return context
    
#------------------------ Edit Professor ------------------------
class ProfessorEditView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.UpdateView):
    model = Professor
    context_object_name = 'professor'
    fields = ('user', 'first_name', 'last_name', 'slug', 'phone', 'image', 'specialty', 'is_active')
    success_message = 'استاد ویرایش شد.'
    template_name = 'panel/professor/professor_edit.html'

    def get_success_url(self):
        return reverse('panel:professors')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context
    
#------------------------ Delete Professor ------------------------
class ProfessorDeleteView(LoginRequiredMixin, DashboardAccessMixin,  SuccessMessageMixin, generic.DeleteView):
    model = Professor
    success_url = reverse_lazy('panel:professors')
    success_message = "استاد حذف گردید"  

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        messages.success(request, self.success_message)
        self.object.delete()
        return HttpResponseRedirect(success_url)
    
# ----------------------- Category List -----------------------
class CategoryView(LoginRequiredMixin, DashboardAccessMixin, generic.ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'panel/category/categories.html'


    def get(self, request, *args, **kwargs):
        if request.GET.get('export', None):
            return export_excel(self.get_queryset())
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects_count"] = self.get_queryset().count()
        return context

#------------------------ Create Category ------------------------
class CategoryCreateView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.CreateView):
    model = Category
    context_object_name = 'category'
    fields = ('parent_category', 'title', 'slug', 'description',  'meta_title', 
              'meta_description', 'is_active', 'picture')
    success_message = 'دسته بندی ایجاد گردید.'
    template_name = 'panel/category/category_create.html'

    def get_success_url(self):
        return reverse('panel:categories')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
#------------------------ Edit Category ------------------------
class CategoryEditView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.UpdateView):
    model = Category
    context_object_name = 'category'
    fields = ('parent_category', 'title', 'slug', 'description',  'meta_title', 
              'meta_description', 'is_active', 'picture')
    success_message = 'دسته بندی ویرایش شد.'
    template_name = 'panel/category/category_edit.html'

    def get_success_url(self):
        return reverse('panel:categories')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
#------------------------ Delete Category ------------------------
class CategoryDeleteView(LoginRequiredMixin, DashboardAccessMixin,  SuccessMessageMixin, generic.DeleteView):
    model = Category
    success_url = reverse_lazy('panel:categories')
    success_message = "دسته بندی حذف گردید"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        messages.success(request, self.success_message)
        self.object.delete()
        return HttpResponseRedirect(success_url)

# ----------------------- Package List -----------------------
class PackagesView(LoginRequiredMixin, DashboardAccessMixin, generic.ListView):
    model = Package
    context_object_name = 'packages'
    template_name = 'panel/package/packages.html'


    def get(self, request, *args, **kwargs):
        if request.GET.get('export', None):
            return export_excel(self.get_queryset())
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects_count"] = self.get_queryset().count()
        return context
    
    def get_queryset(self):
        object_list = self.model.objects.all()
        category_filter_slug = self.request.GET.get('category_filter_slug')
        if category_filter_slug:
            category = get_object_or_404(Category, slug=category_filter_slug)
            object_list = object_list.filter(categories=category)
        
        return object_list

#------------------------ Create Package ------------------------
class PackageCreateView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.CreateView):
    model = Package
    context_object_name = 'package'
    fields = ('categories', 'title', 'slug', 'description',  'meta_title', 'meta_description', 
              'is_active', 'price', 'price_with_discount', 'is_active', 'image', 'pre_video', 'day_limit')
    success_message = 'دسته بندی ایجاد گردید.'
    template_name = 'panel/package/package_create.html'

    def get_success_url(self):
        return reverse('panel:packages')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.request.GET.get('category')
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        self.object = form.save()
        categories_ids = self.request.POST.getlist('categories')
        self.object.categories.add(*categories_ids)
        return super().form_valid(form)
    
#------------------------ Edit Package ------------------------
class PackageEditView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.UpdateView):
    model = Package
    context_object_name = 'package'
    fields = ('categories', 'title', 'slug', 'description',  'meta_title', 'meta_description', 
              'is_active', 'price', 'price_with_discount', 'is_active', 'image', 'pre_video', 'day_limit')
    success_message = 'دسته بندی ویرایش شد.'
    template_name = 'panel/package/package_edit.html'

    def get_success_url(self):
        return reverse('panel:packages')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
#------------------------ Delete Package ------------------------
class PackageDeleteView(LoginRequiredMixin, DashboardAccessMixin,  SuccessMessageMixin, generic.DeleteView):
    model = Package
    success_url = reverse_lazy('panel:packages')
    success_message = "دسته بندی حذف گردید"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        messages.success(request, self.success_message)
        self.object.delete()
        return HttpResponseRedirect(success_url)

# ----------------------- Course List -----------------------
class CoursesView(LoginRequiredMixin, DashboardAccessMixin, generic.ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'panel/course/courses.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('export', None):
            return export_excel(self.get_queryset())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects_count"] = self.get_queryset().count()
        return context
    
    def get_queryset(self):
        object_list = self.model.objects.all()
        package_filter_slug = self.request.GET.get('package_filter_slug')
        professor_filter_slug = self.request.GET.get('professor_filter_slug')
        if package_filter_slug:
            package = get_object_or_404(Package, slug=package_filter_slug)
            object_list = object_list.filter(package=package)
        
        if professor_filter_slug:
            professor = get_object_or_404(Professor, slug=professor_filter_slug)
            object_list = object_list.filter(professor=professor)

        return object_list

#------------------------ Create Course ------------------------
class CourseCreateView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.CreateView):
    model = Course
    context_object_name = 'course'
    fields = ('categories', 'professor', 'package', 'title', 'slug', 'description', 'meta_title', 
              'meta_description', 'is_active', 'price', 'price_with_discount', 'image', 'pre_video', 'day_limit')
    success_message = 'دوره ایجاد گردید.'
    success_url = reverse_lazy('panel:courses')
    template_name = 'panel/course/course_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.request.GET.get('category')
        context['categories'] = Category.objects.all()
        context['packages'] = Package.objects.all()
        context['professor'] = Professor.objects.all()
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        categories_ids = self.request.POST.getlist('categories')
        print(categories_ids)
        self.object.categories.add(*categories_ids)
        professor_id = self.request.POST.get('professor')
        package_id = self.request.POST.get('package')

        if professor_id:
            professor = get_object_or_404(Professor, id=professor_id)
            self.object.professor = professor
        if package_id:
            package = get_object_or_404(Package, id=package_id)
            self.object.package = package

        self.object.save()
        return super().form_valid(form)

#------------------------ Edit Course ------------------------
class CourseEditView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.UpdateView):
    model = Course
    context_object_name = 'course'
    fields = ('categories', 'professor', 'package', 'title', 'slug', 'description', 'meta_title', 
              'meta_description', 'is_active', 'price', 'price_with_discount', 'image', 'pre_video', 'day_limit')
    success_message = 'دوره ویرایش شد.'
    template_name = 'panel/course/course_edit.html'

    def get_success_url(self):
        return reverse('panel:courses')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['packages'] = Package.objects.all()
        context['professor'] = Professor.objects.all()
        return context
    
#------------------------ Delete Course ------------------------
class CourseDeleteView(LoginRequiredMixin, DashboardAccessMixin,  SuccessMessageMixin, generic.DeleteView):
    model = Course
    success_url = reverse_lazy('panel:courses')
    success_message = "مجموعه حذف گردید"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        messages.success(request, self.success_message)
        self.object.delete()
        return HttpResponseRedirect(success_url)
       
# ----------------------- Chapter List -----------------------
class ChaptersView(LoginRequiredMixin, DashboardAccessMixin, generic.ListView):
    model = Chapter
    context_object_name = 'chapters'
    template_name = 'panel/chapter/chapters.html'


    def get(self, request, *args, **kwargs):
        if request.GET.get('export', None):
            return export_excel(self.get_queryset())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects_count"] = self.get_queryset().count()
        return context
    
    def get_queryset(self):
        object_list = self.model.objects.all()
        course_filter_slug = self.request.GET.get('course_filter_slug')
        if course_filter_slug:
            course = get_object_or_404(Course, slug=course_filter_slug)
            object_list = object_list.filter(course=course)
        
        return object_list
    
#------------------------ Create Chapter ------------------------
class ChapterCreateView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.CreateView):
    model = Chapter
    context_object_name = 'chapter'
    fields = ('course', 'title', 'slug', 'description', 'meta_title', 
              'meta_description', 'is_active', 'image')
    success_message = 'فصل ایجاد گردید.'
    success_url = reverse_lazy('panel:chapters')
    template_name = 'panel/chapter/chapter_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        course_id = self.request.POST.get('course')
        if course_id:
            course = get_object_or_404(Course, id=course_id)
            self.object.course = course
        
        self.object.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context
    
#------------------------ Edit Chapter ------------------------
class ChapterEditView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.UpdateView):
    model = Chapter
    context_object_name = 'chapter'
    fields = ('course', 'title', 'slug', 'description', 'meta_title', 
              'meta_description', 'is_active', 'image')
    success_message = 'فصل ویرایش شد.'
    template_name = 'panel/chapter/chapter_edit.html'

    def get_success_url(self):
        return reverse('panel:chapters')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context
    
#------------------------ Delete Chapter ------------------------
class ChapterDeleteView(LoginRequiredMixin, DashboardAccessMixin,  SuccessMessageMixin, generic.DeleteView):
    model = Chapter
    success_url = reverse_lazy('panel:chapters')
    success_message = "فصل حذف گردید"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        messages.success(request, self.success_message)
        self.object.delete()
        return HttpResponseRedirect(success_url)

# ----------------------- Part(list/create/edit) -----------------------
class PartsView(LoginRequiredMixin, DashboardAccessMixin, generic.ListView):
    model = Part
    context_object_name = 'parts'
    template_name = 'panel/part/parts.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('export', None):
            return export_excel(self.get_queryset())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects_count"] = self.get_queryset().count()
        return context
    
    def get_queryset(self):
        object_list = self.model.objects.all()
        chapter_filter_slug = self.request.GET.get('chapter_filter_slug')
        if chapter_filter_slug:
            chapter = get_object_or_404(Chapter, slug=chapter_filter_slug)
            object_list = object_list.filter(chapter=chapter)
        
        return object_list
    
#------------------------ Create Part ------------------------
class PartCreateView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.CreateView):
    model = Part
    context_object_name = 'part'
    fields = ('category', 'course', 'chapter', 'title', 'slug', 'description', 'meta_title', 
              'meta_description', 'is_active', 'image', 'image_2', 'part_index', 'part_time', 
              'video_link', 'price')
    success_message = 'قسمت ایجاد گردید.'
    template_name = 'panel/part/part_create.html'

    def get_success_url(self):
        return reverse('panel:parts')

    def form_valid(self, form):
        category_id = self.request.POST.get('category')
        course_id = self.request.POST.get('course')
        chapter_id = self.request.POST.get('chapter')

        if category_id and course_id and chapter_id:
            messages.error(self.request, 'فقط یکی از موارد دسته بندی یا فصل یا مجموعه را انتخاب کنید.')
            return render(self.request, self.template_name, {'form': form})

        if not category_id and not course_id and not chapter_id:
            messages.error(self.request, 'حداقل یکی از موارد دسته بندی یا فصل یا مجموعه را انتخاب کنید.')
            return render(self.request, self.template_name, {'form': form})

        form.instance.category = None
        form.instance.course = None
        form.instance.chapter = None

        if category_id:
            category = get_object_or_404(Category, id=category_id)
            form.instance.category = category

        if course_id:
            course = get_object_or_404(Course, id=course_id)
            form.instance.course = course
        
        if chapter_id:
            chapter = get_object_or_404(Chapter, id=chapter_id)
            form.instance.chapter = chapter

        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['courses'] = Course.objects.all()
        context['chapters'] = Chapter.objects.all()
        return context

#------------------------ Edit Part ------------------------
class PartEditView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.UpdateView):
    model = Part
    context_object_name = 'part'
    fields = ('category', 'course', 'chapter', 'title', 'slug', 'description', 'meta_title', 
              'meta_description', 'is_active', 'image', 'image_2', 'part_index', 'part_time', 
              'video_link', 'price')
    success_message = 'قسمت ویرایش شد.'
    template_name = 'panel/part/part_edit.html'

    def get_success_url(self):
        return reverse('panel:parts')
    
    def form_valid(self, form):
        category_id = self.request.POST.get('category')
        course_id = self.request.POST.get('course')
        chapter_id = self.request.POST.get('chapter')


        if category_id and course_id and chapter_id:
            messages.error(self.request, 'فقط یکی از موارد دسته بندی یا فصل یا مجموعه را انتخاب کنید.')
            return render(self.request, self.template_name, {'part': self.get_object()})

        if not category_id and not course_id and not chapter_id:
            messages.error(self.request, 'حداقل یکی از موارد دسته بندی یا فصل یا مجموعه را انتخاب کنید.')
            return render(self.request, self.template_name, {'part': self.get_object()})

        form.instance.category = None
        form.instance.course = None
        form.instance.chapter = None

        if category_id:
            category = get_object_or_404(Category, id=category_id)
            form.instance.category = category

        if course_id:
            course = get_object_or_404(Course, id=course_id)
            form.instance.course = course

        if chapter_id:
            chapter = get_object_or_404(Chapter, id=chapter_id)
            form.instance.chapter = chapter

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['courses'] = Course.objects.all()
        context['chapters'] = Chapter.objects.all()
        return context
    
#------------------------ Delete Part ------------------------
class PartDeleteView(LoginRequiredMixin, DashboardAccessMixin,  SuccessMessageMixin, generic.DeleteView):
    model = Part
    success_url = reverse_lazy('panel:parts')
    success_message = "محصول حذف گردید"  

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        messages.success(request, self.success_message)
        self.object.delete()
        return HttpResponseRedirect(success_url)
    
# ----------------------- Comment List -----------------------
class CommentView(LoginRequiredMixin, DashboardAccessMixin, generic.ListView):
    model = Comment
    context_object_name = 'comments'
    template_name = 'panel/comment/comments.html'


    def get(self, request, *args, **kwargs):
        if request.GET.get('export', None):
            return export_excel(self.get_queryset())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects_count"] = self.get_queryset().count()
        context['packages'] = Package.objects.all()
        context['courses'] = Course.objects.all()
        context['users'] = User.objects.all()
        return context
    
    def get_queryset(self):
        object_list = self.model.objects.all()
        user_filter_slug = self.request.GET.get('user_filter_slug')
        package_filter_slug = self.request.GET.get('package_filter_slug')
        course_filter_slug = self.request.GET.get('course_filter_slug')
        if user_filter_slug:
            user = get_object_or_404(User, username=user_filter_slug)
            object_list = object_list.filter(user=user)
        
        if package_filter_slug:
            package = get_object_or_404(Package, slug=package_filter_slug)
            object_list = object_list.filter(package=package)

        if course_filter_slug:
            course = get_object_or_404(Course, slug=course_filter_slug)
            object_list = object_list.filter(course=course)
        
        return object_list
    
#------------------------ Create Comment ------------------------
class CommentCreateView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.CreateView):
    model = Comment
    context_object_name = 'comment'
    fields = ('package', 'course', 'user', 'rate', 'content', 'is_active')
    success_message = 'نظر ایجاد گردید.'
    template_name = 'panel/comment/comment_create.html'

    def get_success_url(self):
        return reverse('panel:comments')

    def form_valid(self, form):
        package_id = self.request.POST.get('package')
        course_id = self.request.POST.get('course')
        user_id = self.request.POST.get('user')

        if package_id and course_id:
            messages.error(self.request, 'فقط یکی از موارد دسته بندی یا مجموعه را انتخاب کنید.')
            return render(self.request, self.template_name, {'form': form})

        if not package_id and not course_id:
            messages.error(self.request, 'حداقل یکی از موارد دسته بندی یا مجموعه را انتخاب کنید.')
            return render(self.request, self.template_name, {'form': form})
       
        if not user_id:
            messages.error(self.request, 'حداقل یک کاربر را انتخاب کنید.')
            return render(self.request, self.template_name, {'form': form})
        
        form.instance.course = None
        form.instance.chapter = None
        form.instance.user = None

        if package_id:
            package = get_object_or_404(Package, id=package_id)
            form.instance.package = package
        
        if course_id:
            course = get_object_or_404(Course, id=course_id)
            form.instance.course = course
        
        if user_id:
            user = get_object_or_404(User, id=user_id)
            form.instance.user = user
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        context['chapters'] = Chapter.objects.all()
        context['users'] = User.objects.all()
        return context

#------------------------ Edit Comment ------------------------
class CommentEditView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.UpdateView):
    model = Comment
    context_object_name = 'comment'
    fields = ('package', 'course', 'user', 'rate', 'content', 'is_active')
    success_message = 'نظر ویرایش شد.'
    template_name = 'panel/comment/comment_edit.html'

    def get_success_url(self):
        return reverse('panel:comments')
    
    def form_valid(self, form):
        package_id = self.request.POST.get('package')
        course_id = self.request.POST.get('course')
        user_id = self.request.POST.get('user')

        if package_id and course_id:
            messages.error(self.request, 'فقط یکی از موارد دسته بندی یا مجموعه را انتخاب کنید.')
            return render(self.request, self.template_name, {'comment': self.get_object()})

        if not package_id and not course_id:
            messages.error(self.request, 'حداقل یکی از موارد دسته بندی یا مجموعه را انتخاب کنید.')
            return render(self.request, self.template_name, {'comment': self.get_object()})
       
        if not user_id:
            messages.error(self.request, 'حداقل یک کاربر را انتخاب کنید.')
            return render(self.request, self.template_name, {'comment': self.get_object()})
        
        form.instance.course = None
        form.instance.chapter = None
        form.instance.user = None

        if package_id:
            package = get_object_or_404(Package, id=package_id)
            form.instance.package = package
        
        if course_id:
            course = get_object_or_404(Course, id=course_id)
            form.instance.course = course
        
        if user_id:
            user = get_object_or_404(User, id=user_id)
            form.instance.user = user
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        context['chapters'] = Chapter.objects.all()
        context['users'] = User.objects.all()
        return context
    
#------------------------ Delete Comment ------------------------
class CommentDeleteView(LoginRequiredMixin, DashboardAccessMixin,  SuccessMessageMixin, generic.DeleteView):
    model = Comment
    success_url = reverse_lazy('panel:comments')
    success_message = "نظر حذف گردید"  

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        messages.success(request, self.success_message)
        self.object.delete()
        return HttpResponseRedirect(success_url)
    
# ----------------------- Ticket List -----------------------
class TicketView(LoginRequiredMixin, DashboardAccessMixin, generic.ListView):
    model = Ticket
    context_object_name = 'tickets'
    template_name = 'panel/ticket/tickets.html'


    def get(self, request, *args, **kwargs):
        if request.GET.get('export', None):
            return export_excel(self.get_queryset())
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects_count"] = self.get_queryset().count()
        return context
    
    def get_queryset(self):
        object_list = self.model.objects.all()
        user_filter_slug = self.request.GET.get('user_filter_slug')
        course_filter_slug = self.request.GET.get('course_filter_slug')
        if user_filter_slug:
            user = get_object_or_404(User, username=user_filter_slug)
            object_list = object_list.filter(user=user)
        
        if course_filter_slug:
            course = get_object_or_404(Course, slug=course_filter_slug)
            object_list = object_list.filter(course=course)
        
        return object_list

#------------------------ Create Ticket ------------------------
class TicketCreateView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.CreateView):
    model = Ticket
    context_object_name = 'ticket'
    fields = ('user', 'title', 'description', 'priority', 'status')
    success_message = 'تیکت ایجاد گردید.'
    template_name = 'panel/ticket/ticket_create.html'

    def get_success_url(self):
        return reverse('panel:tickets')

    def form_valid(self, form):
        user_id = self.request.POST.get('user')

        if not user_id:
            messages.error(self.request, 'حداقل یک کاربر را انتخاب کنید.')
            return render(self.request, self.template_name, {'form': form})
        
        form.instance.user = None

        if user_id:
            user = get_object_or_404(User, id=user_id)
            form.instance.user = user
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['priorities'] = TICKET_PRIORITY_CHOICES
        context['statuses'] = TICKET_STATUS_CHOICES
        return context

#------------------------ Edit Ticket ------------------------
class TicketEditView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.UpdateView):
    model = Ticket
    context_object_name = 'ticket'
    fields = ('user', 'title', 'description', 'priority', 'status')
    success_message = 'تیکت ویرایش شد.'
    template_name = 'panel/ticket/ticket_edit.html'

    def get_success_url(self):
        return reverse('panel:tickets')
    
    def form_valid(self, form):
        user_id = self.request.POST.get('user')

        if not user_id:
            messages.error(self.request, 'حداقل یک کاربر را انتخاب کنید.')
            return render(self.request, self.template_name, {'ticket': self.get_object()})
        
        form.instance.user = None

        if user_id:
            user = get_object_or_404(User, id=user_id)
            form.instance.user = user
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['priorities'] = TICKET_PRIORITY_CHOICES
        context['statuses'] = TICKET_STATUS_CHOICES
        return context

#------------------------ Delete Ticket ------------------------
class TicketDeleteView(LoginRequiredMixin, DashboardAccessMixin,  SuccessMessageMixin, generic.DeleteView):
    model = Ticket
    success_url = reverse_lazy('panel:tickets')
    success_message = "تیکت حذف گردید"  

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        messages.success(request, self.success_message)
        self.object.delete()
        return HttpResponseRedirect(success_url)
    
# ----------------------- Ticket Detail/Message List(list/create/edit) -----------------------
class TicketDetailView(LoginRequiredMixin, DashboardAccessMixin, generic.ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'panel/ticket/ticket_detail.html'


    def get(self, request, *args, **kwargs):
        form = MessageForm()
        ticket = get_object_or_404(Ticket, id=kwargs.get('pk'))
        return render(request, self.template_name, {"ticket": ticket, "form": form})

    def post(self, request, *args, **kwargs):
        ticket = get_object_or_404(Ticket, id=kwargs.get('pk'))
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.ticket = ticket
            message.admin_reply = True
            message.save()
            messages.success(request, "پیام با موفقیت ارسال شد.")
            return redirect("panel:ticket_detail", pk=ticket.pk)
        return render(request, self.template_name, {"ticket": ticket, "form": form})
    

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('paginate_by', None)
        if paginate_by:
            return paginate_by
        return 20


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects_count"] = self.get_queryset().count()
        return context

# ----------------------- Default Message Create/Edit -----------------------
class DefaultMessageCreateEditView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.View):
    model = DefaultMessage
    form_class = DefaultMessageForm
    template_name = 'panel/ticket/default_message_create_edit.html'
    success_message = 'پیام پیشفرض با موفقیت ذخیره شد.'

    def get(self, request, *args, **kwargs):
        first_default_message = DefaultMessage.objects.first()
        if first_default_message:
            form = self.form_class(instance=first_default_message)
        else:
            form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        first_default_message = DefaultMessage.objects.first()
        if first_default_message:
            form = self.form_class(request.POST, instance=first_default_message)
        else:
            form = self.form_class(request.POST)
        
        if form.is_valid():
            form.save()
            if first_default_message:
                messages.success(request, 'پیام پیشفرض با موفقیت ویرایش شد.')
            else:
                messages.success(request, 'پیام پیشفرض با موفقیت ایجاد شد.')
            return redirect(reverse('panel:default_message_create_edit'))
        else:
            return render(request, self.template_name, {'form': form})

#------------------------ Delete Message ------------------------
class MessageDeleteView(LoginRequiredMixin, DashboardAccessMixin,  SuccessMessageMixin, generic.DeleteView):
    model = Message
    success_url = reverse_lazy('panel:ticket_detail')
    success_message = "پیام حذف گردید"  

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        messages.success(request, self.success_message)
        self.object.delete()
        return HttpResponseRedirect(success_url)
    
# ----------------------- Order(list/create/edit) -----------------------
class OrderView(LoginRequiredMixin, DashboardAccessMixin, generic.ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'panel/order/orders.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('export', None):
            return export_excel(self.get_queryset())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects_count"] = self.get_queryset().count()
        return context
    
    def get_queryset(self):
        object_list = self.model.objects.all()
        user_filter_slug = self.request.GET.get('user_filter_slug')
        if user_filter_slug:
            user = get_object_or_404(User, username=user_filter_slug)
            object_list = object_list.filter(user=user)
        
        return object_list
    
#------------------------ Create Order ------------------------
class OrderCreateView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.CreateView):
    model = Order
    context_object_name = 'order'
    fields = ('user', 'is_paid', 'paid_at', 'ref_id')
    success_message = 'سفارش ایجاد گردید.'
    template_name = 'panel/order/order_create.html'

    def get_success_url(self):
        return reverse('panel:orders')

    def form_valid(self, form):
        user_id = self.request.POST.get('user')
        package_ids = self.request.POST.getlist('package_ids')
        course_ids = self.request.POST.getlist('course_ids')
        part_ids = self.request.POST.getlist('part_ids')

        if not package_ids and not course_ids and not part_ids:
            messages.error(self.request, 'حداقل یک ایتم را از بین دسته بندی یا مجموعه یا محصولانتخاب کنید.')
            return render(self.request, self.template_name, {'form': form})

        order = form.save(commit=False)  # Save the form to create the order object
        order.user = None
        
        if user_id:
            user = get_object_or_404(User, id=user_id)
            order.user = user

        order.save()  # Save the order object first

        for package_id in package_ids:
            package = get_object_or_404(Package, id=package_id)
            OrderItem.objects.create(order=order, package=package, price=package.price)

        for course_id in course_ids:
            course = get_object_or_404(Course, id=course_id)
            OrderItem.objects.create(order=order, course=course, price=course.price)

        for part_id in part_ids:
            part = get_object_or_404(Part, id=part_id)
            OrderItem.objects.create(order=order, part=part, price=part.price)

        return super().form_valid(form)

        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

#------------------------ Edit Order ------------------------
class OrderEditView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.UpdateView):
    model = Order
    context_object_name = 'order'
    fields = ('user', 'is_paid', 'paid_at', 'ref_id')
    success_message = 'سفارش ویرایش شد.'
    template_name = 'panel/order/order_edit.html'

    def get_success_url(self):
        return reverse('panel:orders')
    
    def form_valid(self, form):
        # Save the form to create the order object
        user_id = self.request.POST.get('user')
        package_ids = self.request.POST.getlist('package_ids')
        course_ids = self.request.POST.getlist('course_ids')
        part_ids = self.request.POST.getlist('part_ids')

        order_items = OrderItem.objects.filter(order=self.get_object())
        for order_item in order_items:
            order_item.delete()

        if not part_ids and not package_ids and not course_ids:
            messages.error(self.request, 'حداقل یک ایتم را از بین دسته بندی یا مجموعه یا محصول انتخاب کنید.')
            return render(self.request, self.template_name, {'order': self.get_object()})
        
        if package_ids:
            for package_id in package_ids:
                package = get_object_or_404(Package, id=package_id)
                OrderItem.objects.create(order=self.get_object(), package=package, price=package.price)
            
        if course_ids:
            for course_id in course_ids:
                course = get_object_or_404(Course, id=course_id)
                OrderItem.objects.create(order=self.get_object(), course=course, price=course.price)

        if part_ids:
            for part_id in part_ids:
                part = get_object_or_404(Part, id=part_id)
                OrderItem.objects.create(order=self.get_object(), part=part, price=part.price)


        if not user_id:
            messages.error(self.request, 'حداقل یک کاربر را انتخاب کنید.')
            return render(self.request, self.template_name, {'order': self.get_object()})
        
        form.instance.user = None

        if user_id:
            user = get_object_or_404(User, id=user_id)
            form.instance.user = user
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

#------------------------ Delete Order ------------------------
class OrderDeleteView(LoginRequiredMixin, DashboardAccessMixin,  SuccessMessageMixin, generic.DeleteView):
    model = Order
    success_url = reverse_lazy('panel:orders')
    success_message = "سفارش حذف گردید"  

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        messages.success(request, self.success_message)
        self.object.delete()
        return HttpResponseRedirect(success_url)
    
# ----------------------- Discount(list/create/edit) -----------------------
class DiscountView(LoginRequiredMixin, DashboardAccessMixin, generic.ListView):
    model = Discount
    context_object_name = 'discounts'
    template_name = 'panel/discount/discounts.html'


    def get(self, request, *args, **kwargs):
        if request.GET.get('export', None):
            return export_excel(self.get_queryset())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects_count"] = self.get_queryset().count()
        return context
    
#------------------------ Create Discount ------------------------
class DiscountCreateView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.CreateView):
    model = Discount
    context_object_name = 'discount'
    fields = ('code', 'value', 'is_active', 'start_date', 'end_date')
    success_message = 'کد تخفیف ایجاد گردید.'
    template_name = 'panel/discount/discount_create.html'

    def get_success_url(self):
        return reverse('panel:discounts')

    def form_valid(self, form):
        context = {}
        context['categories'] = Category.objects.all()
        context['orders'] = Order.objects.all()
        context['form'] = form
        start_date = self.request.POST.get('start_date')
        end_date = self.request.POST.get('end_date')
        categories = self.request.POST.getlist('categories[]')

        if start_date and end_date:
            try:
                start_date_datetime = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
                end_date_datetime = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')

                start_date_formatted = start_date_datetime.strftime('%Y-%m-%d %H:%M:%S')
                end_date_formatted = end_date_datetime.strftime('%Y-%m-%d %H:%M:%S')

                form.instance.start_date = start_date_formatted
                form.instance.end_date = end_date_formatted

            except ValueError:
                messages.error(self.request, 'تاریخ شروع یا پایان کد تخفیف نامعتبر است.')
                return render(self.request, self.template_name, context)
        else:
            messages.error(self.request, 'تاریخ شروع و پایان تخفیف نمیتواند خالی باشد.')
            return render(self.request, self.template_name, context)

        form.save()

        if not categories:
            messages.error(self.request, 'حداقل یک دسته بندی انتخاب کنید')
            return render(self.request, self.template_name, {'form': form})

        form.instance.categories.add(*categories)

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        context['categories'] = Category.objects.all()
        return context

#------------------------ Edit Discount ------------------------
class DiscountEditView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.UpdateView):
    model = Discount
    context_object_name = 'discount'
    fields = ('code', 'value', 'is_active', 'start_date', 'end_date', 'order')
    success_message = 'کد تخفیف ویرایش شد.'
    template_name = 'panel/discount/discount_edit.html'

    def get_success_url(self):
        return reverse('panel:discounts')
    
    def form_valid(self, form):
        context = {}
        context['categories'] = Category.objects.all()
        context['orders'] = Order.objects.all()
        context['discount'] = self.get_object()
        start_date = self.request.POST.get('start_date')
        end_date = self.request.POST.get('end_date')
        categories = self.request.POST.getlist('categories[]')
        
        if start_date and end_date:
            try:
                start_date_datetime = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
                end_date_datetime = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')

                start_date_formatted = start_date_datetime.strftime('%Y-%m-%d %H:%M:%S')
                end_date_formatted = end_date_datetime.strftime('%Y-%m-%d %H:%M:%S')

                form.instance.start_date = start_date_formatted
                form.instance.end_date = end_date_formatted

            except ValueError:
                messages.error(self.request, 'تاریخ شروع یا پایان کد تخفیف نامعتبر است.')
                return render(self.request, self.template_name, context)
        else:
            messages.error(self.request, 'تاریخ شروع و پایان تخفیف نمیتواند خالی باشد.')
            return render(self.request, self.template_name, {'discount': context})

        form.save()

        if not categories:
            messages.error(self.request, 'حداقل یک دسته بندی انتخاب کنید')
            return render(self.request, self.template_name, context)

        cats = Category.objects.all()
        form.instance.categories.remove(*cats)
        form.instance.categories.add(*categories)
            
        return super().form_valid(form)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        context['categories'] = Category.objects.all()
        return context

#------------------------ Delete Discount ------------------------
class DiscountDeleteView(LoginRequiredMixin, DashboardAccessMixin,  SuccessMessageMixin, generic.DeleteView):
    model = Discount
    success_url = reverse_lazy('panel:discounts')
    success_message = "کد تخفیف حذف گردید"  

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        messages.success(request, self.success_message)
        self.object.delete()
        return HttpResponseRedirect(success_url)
 
#------------------------ Duplicate a Package ------------------------
def duplicate_package(request, package_id):
    original_object = Package.objects.get(pk=package_id)
    random_title = uuid.uuid4().hex[:6]
    # Create a copy of the original object
    new_object = Package.objects.create(
        title=f'{original_object.title}-{random_title}',
        description=original_object.description, 
        meta_title=original_object.meta_title,
        meta_description=original_object.meta_description,
        is_active=original_object.is_active,
        pre_video=original_object.pre_video,
        image=original_object.image,
        price=original_object.price,
        day_limit=original_object.day_limit
    )
    
    new_object.categories.set(original_object.categories.all())
    messages.success(request, 'دسته بندی با موفقیت کپی شد.')
    return redirect(reverse('panel:packages'))

#------------------------ Duplicate a Course ------------------------
def duplicate_course(request, course_id):
    original_object = Course.objects.get(pk=course_id)
    random_title = uuid.uuid4().hex[:6]
    # Create a copy of the original object
    new_object = Course.objects.create(
        title=f'{original_object.title}-{random_title}',
        description=original_object.description, 
        meta_title=original_object.meta_title,
        meta_description=original_object.meta_description,
        is_active=original_object.is_active,
        pre_video=original_object.pre_video,
        image=original_object.image,
        price=original_object.price,
        day_limit=original_object.day_limit
    )
    messages.success(request, 'مجموعه با موفقیت کپی شد.')
    return redirect(reverse('panel:courses'))

#------------------------ Duplicate a Chapter ------------------------
def duplicate_chapter(request, chapter_id):
    original_object = Chapter.objects.get(pk=chapter_id)
    random_title = uuid.uuid4().hex[:6]
    # Create a copy of the original object
    new_object = Chapter.objects.create(
        title=f'{original_object.title}-{random_title}',
        description=original_object.description, 
        meta_title=original_object.meta_title,
        meta_description=original_object.meta_description,
        is_active=original_object.is_active,
        image=original_object.image,
    )
    messages.success(request, 'فصل با موفقیت کپی شد.')
    return redirect(reverse('panel:chapters'))

#------------------------ Duplicate a Part ------------------------
def duplicate_part(request, part_id):
    original_object = Part.objects.get(pk=part_id)
    random_title = uuid.uuid4().hex[:6]
    # Create a copy of the original object
    new_object = Part.objects.create(
        title=f'{original_object.title}-{random_title}',
        description=original_object.description, 
        meta_title=original_object.meta_title,
        meta_description=original_object.meta_description,
        is_active=original_object.is_active,
        part_index=original_object.part_index,
        part_time=original_object.part_index,
        image=original_object.image,
        video_link=original_object.video_link,
        price=original_object.price
    )
    messages.success(request, 'محصول با موفقیت کپی شد.')
    return redirect(reverse('panel:parts'))

# ----------------------- Main Banner Create/Edit -----------------------
class MainBannerCreateEditView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.View):
    model = MainBanner
    form_class = MainBannerForm
    template_name = 'panel/main_banner/banner_create_edit.html'
    success_message = 'بنر صفحه اصلی با موفقیت ذخیره شد.'

    def get(self, request, *args, **kwargs):
        first_main_banner = MainBanner.objects.first()
        if first_main_banner:
            form = self.form_class(instance=first_main_banner)
        else:
            form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        first_main_banner = MainBanner.objects.first()
        if first_main_banner:
            form = self.form_class(request.POST, request.FILES, instance=first_main_banner)
        else:
            form = self.form_class(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            if first_main_banner:
                messages.success(request, 'بنر با موفقیت ویرایش شد.')
            else:
                messages.success(request, 'بنر با موفقیت ایجاد شد.')
            return redirect(reverse('panel:main_banner_create_edit'))
        else:
            return render(request, self.template_name, {'form': form})

# ----------------------- view for update ordering -----------------------
def update_index(request):
    MODEL_MAP = {
        'Professor': Professor,
        'Category': Category,
        'Package': Package, 
        'Course': Course, 
        'Chapter': Chapter, 
        'Part': Part, 
        'Comment': Comment, 
        'Discount': Discount,
        'Order': Order,
        'Ticket': Ticket
    }
    if request.method == 'POST':
        new_index_str = request.POST.getlist('index')[0]
        model_name = request.POST.get('modelName')
        model_class = MODEL_MAP[model_name]
        new_index = json.loads(new_index_str)
        try:
            if model_class:
                for index, id in enumerate(new_index, start=1):
                    obj = model_class.objects.get(id=id)
                    obj.index = index
                    obj.save()
                
                return JsonResponse({'success': True})
            else:
                raise ValueError(f"Model '{model_name}' not found")
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# ----------------------- Websites List -----------------------
class WebsiteView(LoginRequiredMixin, DashboardAccessMixin, generic.ListView):
    model = WebSites
    context_object_name = 'websites'
    template_name = 'panel/websites/websites.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('export', None):
            return export_excel(self.get_queryset())
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects_count"] = self.get_queryset().count()
        return context

#------------------------ Create Website ------------------------
class WebsiteCreateView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.CreateView):
    model = WebSites
    context_object_name = 'website'
    fields = ('title', 'link', 'image')
    success_message = 'وبسایت ایجاد گردید.'
    template_name = 'panel/websites/website_create.html'

    def get_success_url(self):
        return reverse('panel:websites')
    
#------------------------ Edit Website ------------------------
class WebsiteEditView(LoginRequiredMixin, DashboardAccessMixin, SuccessMessageMixin, generic.UpdateView):
    model = WebSites
    context_object_name = 'website'
    fields = ('title', 'link', 'image')
    success_message = 'وبسایت ویرایش شد.'
    template_name = 'panel/websites/website_edit.html'

    def get_success_url(self):
        return reverse('panel:websites')
    
#------------------------ Delete Website ------------------------
class WebsiteDeleteView(LoginRequiredMixin, DashboardAccessMixin,  SuccessMessageMixin, generic.DeleteView):
    model = WebSites
    success_url = reverse_lazy('panel:websites')
    success_message = "وبسایت حذف گردید"  

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        messages.success(request, self.success_message)
        self.object.delete()
        return HttpResponseRedirect(success_url)
    
# ----------------------- Notification -----------------------
class NotificationView(LoginRequiredMixin, DashboardAccessMixin, generic.ListView):
    model = NotificationLog
    context_object_name = 'notifications'
    template_name = 'panel/notification/notifications.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('export', None):
            return export_excel(self.get_queryset())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects_count"] = self.get_queryset().count()
        return context

# ----------------------- Send Notification -----------------------
def send_notification(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        link = request.POST.get('link')
        notification_log_object = NotificationLog.objects.create(title=title, body=body, link=link, status='failure')
        server_key = 'AAAA73hWHS4:APA91bHEHQtVPlNTnx6QHT3wctjxGm3S1yGCpVpMWL5YMSwMGZIzpLks-8cG5Jh0A9BxA-xhbiqDNcdq4L_VfCCIGpcdtLQNFn9o8db3vERdeMnNpHmpFJm1Bm7KKXk2Dbse0DVzoigF'

        # Combined payload
        payload = {
            'to': '/topics/user',
            'priority': 'high',
            'notification': {
                'title': title,
                'body': body,
                'sound': 'default',
                'icon': 'static/logo-red.png',

            }, 
            'data': {
                'url': link  
            }
            
        }

        # Set headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'key={server_key}'
        }

        # Make the POST request to Firebase Cloud Messaging
        response = requests.post('https://fcm.googleapis.com/fcm/send', headers=headers, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            if 'message_id' in response_data:
                messages.success(request, 'نوتیفیکیشن ارسال شد.')
                notification_log_object.status = 'success'
                notification_log_object.save()
            else:
                messages.error(request, 'نوتیفیکیشن ارسال نشد.')
            return redirect('panel:notifications')
        else:
            return JsonResponse({'success': False, 'message': 'Error: Unable to reach FCM', 'status_code': response.status_code, 'error': response.text})

    return render(request, 'panel/notification/send_notification.html')

# ----------------------- Wallet -----------------------
class WalletView(generic.View):
    def get(self, request):
        return render(request, 'panel/wallet/wallet.html')

# ----------------------- Wallet Charge -----------------------
class WalletChargeView(generic.View):
    def post(self, request):
        users = request.POST.get('user_ids')
        message = request.POST.get('description')
        amount = request.POST.get('amount')

        if not users:
            messages.error(self.request, 'حداقل باید یک کاربر انتخاب شود.')
            return render(request, 'panel/wallet/wallet.html')
        if not message:
            messages.error(self.request, 'فیلد پیام نمیتواند خالی باشد')
            return render(request, 'panel/wallet/wallet.html')
        if not amount or isinstance(amount, int):
            messages.error(self.request, 'فیلد مبلغ نمیتواند خالی باشد.')
            return render(request, 'panel/wallet/wallet.html')

        user_ids = json.loads(users)
        amount = int(amount)

        Wallet.objects.filter(user_id__in=user_ids).update(balance=F('balance') + amount)
        transaction_histories = [
            TransactionHistory(
                wallet_id=wallet.id,
                amount=amount,
                transaction_type='C1',
                charge_by='A',
                message=message
            )
            for wallet in Wallet.objects.filter(user_id__in=user_ids)
        ]
        TransactionHistory.objects.bulk_create(transaction_histories)

        messages.success(self.request, 'کیف پول کاربران انتخاب شده با موفقیت شارژ شد')
        return render(request, 'panel/wallet/wallet.html')

# ----------------------- MinimumCartCost  -----------------------
class CreateOrUpdateMinimumCartCostView(LoginRequiredMixin, generic.View):
    template_name = 'panel/minimum_cart_cost/create_or_edit_mcc.html'

    def get(self, request):
        mcc = None
        if MinimumCartCost.objects.all().first():
            mcc = MinimumCartCost.objects.first()
        return render(request, self.template_name, {'mcc': mcc})

    def post(self, request):
        price = request.POST.get('price')
        mcc = None
        if price:
            if MinimumCartCost.objects.all().first():
                mcc = MinimumCartCost.objects.first()
                mcc.minimum_cart_cost = int(price)
                mcc.save()
                messages.success(request, 'حداقل مبلغ سفارش با موفقیت ویرایش شد.')
            else:
                mcc = MinimumCartCost.objects.create(minimum_cart_cost=price)
                messages.success(request, 'حداقل مبلغ سفارش با موفقیت ویرایش شد. ')
        else:
            mcc = MinimumCartCost.objects.all().first()
        return render(request, self.template_name, {'mcc': mcc})

