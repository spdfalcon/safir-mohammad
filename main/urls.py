from django.urls import path
from .views import HomeView, AboutView, CategoriesView, CategoryDetailView, SearchView, ContactView , RulesView, OthersView, SearchResultsAjax

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('rules/', RulesView.as_view(), name='rules'),
    path('search/', SearchView.as_view(), name='search'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('category/<str:category_slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('others/', OthersView.as_view(), name='others'),
    path('search_results_ajax/', SearchResultsAjax.as_view(), name='search_results_ajax'), 

]
