from django.urls import path
from .views import WishListView, WishListDeleteView, WishListAddView

app_name = 'wishlist'

urlpatterns = [
    path('', WishListView.as_view(), name='wishlist'),
    path('delete_item/<int:item_id>/', WishListDeleteView.as_view(), name='delete_item'),
    path('add_item/<int:part_id>/', WishListAddView.as_view(), name='add_part_item'),
    path('add_item/<int:package_id>/', WishListAddView.as_view(), name='add_package_item'),
    path('add_item/<int:course_id>/', WishListAddView.as_view(), name='add_course_item'),
    
]