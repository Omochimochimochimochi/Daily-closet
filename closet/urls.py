from django.urls import path
from . import views

app_name = 'closet'

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
    path('consideration/', views.consideration_list, name='consideration_list'),
    
    # --- ここから下の2行が重要です！ ---
    # 1. 検討リストに追加する処理
    path('consideration/add/<int:item_id>/', views.add_to_consideration, name='add_to_consideration'),
    
    # 2. 検討リストを表示する画面
    path('consideration/', views.consideration_list, name='consideration_list'),
    
    # 3. 検討リストから削除する処理
    path('consideration/remove/<int:item_id>/', views.remove_from_consideration, name='remove_from_consideration'),


    path('purchase/', views.purchase_list, name='purchase_list'),
    path('move-to-purchase/<int:item_id>/', views.move_to_purchase, name='move_to_purchase'),
]