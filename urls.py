from django.urls import path
from . import views

urlpatterns = [
    # トップ画面（今まで作っていたものがあれば）
    path('', views.top, name='top'),
    
    # --- 今回作った管理画面シリーズ ---
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-menu/', views.admin_menu, name='admin_menu'),
    path('admin-inventory/', views.inventory_manage, name='inventory_manage'),
]
