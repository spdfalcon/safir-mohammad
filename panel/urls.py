from django.urls import path
from .views import *

app_name = 'panel'
urlpatterns = [
    path('', PanelView.as_view(), name='dashboard'),

    path('users/', UserView.as_view(), name='users'),
    path('user_create/', UserCreateView.as_view(), name='user_create'),
    path('user_edit/<int:pk>', UserEditView.as_view(), name='user_edit'),
    path('user_delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),

    path('professor/', ProfessorView.as_view(), name='professors'),
    path('professor_create/', ProfessorCreateView.as_view(), name='professor_create'),
    path('professor_edut/<int:pk>/', ProfessorEditView.as_view(), name='professor_edit'),
    path('professor_delete/<int:pk>/', ProfessorDeleteView.as_view(), name='professor_delete'),

    path('categories/', CategoryView.as_view(), name='categories'),
    path('category_create/', CategoryCreateView.as_view(), name='category_create'),
    path('category_edut/<int:pk>/', CategoryEditView.as_view(), name='category_edit'),
    path('category_delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),

    path('packages', PackagesView.as_view(), name='packages'),
    path('package_create/', PackageCreateView.as_view(), name='package_create'),
    path('package_edit/<int:pk>/', PackageEditView.as_view(), name='package_edit'),
    path('package_delete/<int:pk>/', PackageDeleteView.as_view(), name='package_delete'),

    path('courses', CoursesView.as_view(), name='courses'),
    path('course_edit/<int:pk>/', CourseEditView.as_view(), name='course_edit'),
    path('course_create/', CourseCreateView.as_view(), name='course_create'),
    path('course_delete/<int:pk>/', CourseDeleteView.as_view(), name='course_delete'),


    path('chapters', ChaptersView.as_view(), name='chapters'),
    path('chapter_create/', ChapterCreateView.as_view(), name='chapter_create'),
    path('chapter_edit/<int:pk>/', ChapterEditView.as_view(), name='chapter_edit'),
    path('chapter_delete/<int:pk>/', ChapterDeleteView.as_view(), name='chapter_delete'),

    path('parts', PartsView.as_view(), name='parts'),
    path('part_create/', PartCreateView.as_view(), name='part_create'),
    path('part_edit/<int:pk>/', PartEditView.as_view(), name='part_edit'),
    path('part_delete/<int:pk>/', PartDeleteView.as_view(), name='part_delete'),

    path('comments/', CommentView.as_view(), name='comments'),
    path('comment_create/', CommentCreateView.as_view(), name='comment_create'),
    path('comment_edit/<int:pk>/', CommentEditView.as_view(), name='comment_edit'),
    path('comment_delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),

    path('tickets/', TicketView.as_view(), name='tickets'),
    path('ticket_create/', TicketCreateView.as_view(), name='ticket_create'),
    path('ticket_edit/<int:pk>/', TicketEditView.as_view(), name='ticket_edit'),
    path('ticket_delete/<int:pk>/', TicketDeleteView.as_view(), name='ticket_delete'),
    path('ticket_detail/<int:pk>', TicketDetailView.as_view(), name='ticket_detail'),

    path('default_message/<int:pk>', DefaultMessageCreateEditView.as_view(), name='default_message_create_edit'),
    path('default_message/', DefaultMessageCreateEditView.as_view(), name='default_message_create_edit'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('orders/', OrderView.as_view(), name='orders'),
    path('order_create/', OrderCreateView.as_view(), name='order_create'),
    path('order_edit/<int:pk>/', OrderEditView.as_view(), name='order_edit'),
    path('order_delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),

    path('discounts/', DiscountView.as_view(), name='discounts'),
    path('discount_create/', DiscountCreateView.as_view(), name='discount_create'),
    path('discount_edit/<int:pk>/', DiscountEditView.as_view(), name='discount_edit'),
    path('discount_delete/<int:pk>/', DiscountDeleteView.as_view(), name='discount_delete'),

    path('packages/<int:package_id>/duplicate/', duplicate_package, name='duplicate-package'),
    path('courses/<int:course_id>/duplicate/', duplicate_course, name='duplicate-course'),
    path('chapters/<int:chapter_id>/duplicate/', duplicate_chapter, name='duplicate-chapter'),
    path('parts/<int:part_id>/duplicate/', duplicate_part, name='duplicate-part'),


    path('main_banner/<int:pk>', MainBannerCreateEditView.as_view(), name='main_banner_create_edit'),
    path('main_banner/', MainBannerCreateEditView.as_view(), name='main_banner_create_edit'),

    path('update_index/', update_index, name='update_index'),

    path('websites/', WebsiteView.as_view(), name='websites'),
    path('website_create/', WebsiteCreateView.as_view(), name='website_create'),
    path('website_edit/<int:pk>', WebsiteEditView.as_view(), name='website_edit'),
    path('website_delete/<int:pk>/', WebsiteDeleteView.as_view(), name='website_delete'),

    path('notifications/', NotificationView.as_view(), name='notifications'),
    path('send_notification/', send_notification, name='send_notification'),

    path('wallet/', WalletView.as_view(), name='wallet'),
    path('wallet/charge/', WalletChargeView.as_view(), name='wallet-charge'),

    path('minimum_cart_cost/', CreateOrUpdateMinimumCartCostView.as_view(), name='mcc'),
    path('minimum_cart_cost_create/', CreateOrUpdateMinimumCartCostView.as_view(), name='create_mcc'),

]
