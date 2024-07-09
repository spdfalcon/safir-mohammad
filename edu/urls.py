from django.urls import path
from .views import *

app_name = 'edu'


urlpatterns = [
    path('packages/', PackagesView.as_view(), name='packages'),
    path('course_detail/<str:course_slug>/', CourseDetailView.as_view(), name='course_detail'), 
    path('package_detail/<str:package_slug>/', PackageDetailView.as_view(), name='package_detail'), 
    path('chapter_detail/<str:chapter_slug>/', ChapterDetailView.as_view(), name='chapter_detail'),
    path('part_detail/<str:part_slug>/', PartDetailView.as_view(), name='part_detail'),
    path('courses/', CoursesView.as_view(), name='courses'),
    path('parts/', PartsView.as_view(), name='parts'),

]