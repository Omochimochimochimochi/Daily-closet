from django.urls import path
from . import views  
# closet/urls.py

urlpatterns = [
    path('', views.top, name='top'),
    
    path('admin-login/', views.admin_login, name='login'), 
    
    path('signup/', views.admin_menu, name='signup'), 
    
    path('admin-menu/', views.admin_menu, name='admin_menu'),
    path('admin-inventory/', views.inventory_manage, name='inventory_manage'),
    path('admin-inventory/add/', views.item_register, name='item_register'),
    path('admin-items/', views.admin_item_list, name='admin_item_list'),
]

