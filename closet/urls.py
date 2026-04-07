from django.urls import path
from . import views  
from . import views

urlpatterns = [
    path('', views.top, name='top'),
    
    path('admin-login/', views.admin_login, name='login'), 
    
    path('signup/', views.admin_menu, name='signup'), 
    
    path('admin-menu/', views.admin_menu, name='admin_menu'),
    path('admin-inventory/', views.inventory_manage, name='inventory_manage'),
    path('admin-inventory/add/', views.item_register, name='item_register'),
    path('admin-items/', views.admin_item_list, name='admin_item_list'),
    path('search_results/', views.search_results, name='search_results'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
]

