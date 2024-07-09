from django.contrib import admin
from .models import (
    Comment,
    Category, 
    Package, 
    Course, 
    Chapter, 
    Part, 
    Professor,
)

from import_export.admin import ImportExportModelAdmin

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class PackageInline(admin.TabularInline):
    model = Package.categories.through
    extra = 1

class CourseInline(admin.TabularInline):
    model = Course
    extra = 1

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1

class PartInline(admin.TabularInline):
    model = Part
    extra = 1


@admin.register(Professor)
class ProfessorAdmin(ImportExportModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'is_active')
    list_filter = ('created_at', 'updated_at', 'is_active')
    search_fields = ('first_name', 'last_name', 'speciality')


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    inlines = [PackageInline]
    list_display = ('title', 'created_at', 'is_active', 'parent_category')
    list_filter = ('created_at', 'updated_at', 'is_active', 'parent_category')
    search_fields = ('title', 'slug', 'description')


@admin.register(Package)
class PackageAdmin(ImportExportModelAdmin):
    inlines = [CourseInline]
    list_display = ('title', 'created_at', 'price', 'is_active')
    filter_horizontal = ('categories',)  # Allows selecting multiple categories in admin
    list_filter = ('created_at', 'updated_at', 'is_active', )
    search_fields = ('title', 'slug', 'description')

@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    inlines = [ChapterInline, CommentInline]
    list_display = ('professor', 'title', 'created_at', 'price', 'is_active', 'package')
    list_filter = ('created_at', 'updated_at', 'is_active', )
    search_fields = ('title', 'slug', 'description')


@admin.register(Chapter)
class ChapterAdmin(ImportExportModelAdmin):
    inlines = [PartInline]
    list_display = ('title', 'created_at', 'is_active', 'course')
    list_filter = ('created_at', 'updated_at', 'is_active', )
    search_fields = ('title', 'slug', 'description')


@admin.register(Part)
class PartAdmin(ImportExportModelAdmin):
    list_display = ('title', 'created_at', 'is_active', 'chapter', 'course')
    list_filter = ('created_at', 'updated_at', 'is_active', )
    search_fields = ('title', 'slug', 'description')

@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    list_display = ('user', 'rate', 'content', 'created_at', 'is_active')
    list_filter = ('created_at', 'updated_at', 'is_active')
    search_fields = ('user__username', 'content')

