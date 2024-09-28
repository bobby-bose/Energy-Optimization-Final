from django.urls import path
from . import views
from . import ac
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),

    path('register/', views.register, name='register'),
    path('calculate_carbon_footprint/', views.calculate_carbon_footprint, name='calculate_carbon_footprint'),
    path('add_appliance/', views.add_appliance, name='add_appliance'),
    path('list_appliances/', views.appliance_list, name='list_appliances'),
    path('profile/', views.profile, name='profile'),
    path('ac/', ac.ac, name='ac'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('submit_profile/', views.submit_profile, name='submit_profile'),
    path('success/<int:pk>/', views.success, name='success'),
    path('optimized-graphs/', views.optimized_graphs, name='optimized_graphs'),
    path('appliance_list/', views.appliance_list, name='appliance_list'),
    path('contact/', views.contact, name='contact'),
    path('bathroom/create/', bathroom_create, name='bathroom_create'),
    path('kitchen-appliance/create/', kitchen_appliance_create, name='kitchen_appliance_create'),
    path('kitchen/appliance/list/', kitchen_appliance_list, name='kitchen_appliance_list'),
path('livingroom/appliance/list/',livingroom_appliance_list, name='livingroom_appliance_list'),
    path('kitchen_delete/<int:pk>/', views.kitchen_delete, name='kitchen_delete'),
    path('bedroom/<int:bedroom_id>/', bedroom_delete, name='bedroom_delete'),
 path('dining_delete/<int:pk>/', views.dining_delete, name='dining_delete'),
  path('bathroom_delete/<int:bathroom_id>/', views.bathroom_delete, name='bathroom_delete'),
path('livingroom/<int:livingroom_id>/delete/', livingroom_delete, name='livingroom_delete'),
path('livingroom/create/', livingroom_appliance, name='livingroom_create'),
    
    path('bedroom/create/', bedroom_appliance_create, name='bedroom_create'),

path('bedroom/list/', bedroom_appliance_list, name='bedroom_appliance_list'),
    path('dininghall/create/', dininghall, name='dininghall_create'),
    path('dininghall_appliance_list', dininghall_appliance_list, name='dininghall_appliance_list'),
    path('livingroom/create/', livingroom_appliance, name='livingroom_create'),
    path('bathroom/list/', bathroom_list, name='bathroom_list'),
path('logout/', logout_view, name='logout'),
path('billings/', billings, name='billings'),
path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

path('get_all_details/', get_all_details, name='get_all_details'),
]
