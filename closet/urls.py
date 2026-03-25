from django.urls import path
from . import views  
urlpatterns = [

    path('', views.top, name='top'),
    
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-menu/', views.admin_menu, name='admin_menu'),
    path('admin-inventory/', views.inventory_manage, name='inventory_manage'),
    path('admin-inventory/add/', views.item_register, name='item_register'),
]
