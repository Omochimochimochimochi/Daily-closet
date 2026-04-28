from django.conf import settings  
from django.conf.urls.static import static  
from django.urls import path
from . import views

app_name = 'closet'

urlpatterns = [
    # ユーザー用：メイン画面
    path('', views.top, name='top'),
    
    # 検索関連：整理しました
    path('search/', views.item_search, name='item_search'),              # 検索画面（フォーム）
    path('search_results/', views.search_results, name='search_results'), # 検索結果一覧
    path('search/tag/<str:tag_name>/', views.search_by_tag, name='search_by_tag'), # タグ用

    path('item/<int:pk>/', views.item_detail, name='item_detail'),

    # ユーザー用：検討リスト
    path('consideration/', views.consideration_list, name='consideration_list'),
    path('consideration/add/<int:item_id>/', views.add_to_consideration, name='add_to_consideration'),
    path('consideration/remove/<int:item_id>/', views.remove_from_consideration, name='remove_from_consideration'),

    # ユーザー用：購入フロー
    path('purchase/', views.purchase_list, name='purchase_list'),
    path('move-to-purchase/<int:item_id>/', views.move_to_purchase, name='move_to_purchase'),
    path('purchase/complete/', views.purchase_complete, name='purchase_complete'),

    # 管理用・ユーザーアカウント関連
    path('admin-login/', views.admin_login, name='admin_login'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('admin-menu/', views.admin_menu, name='admin_menu'),
    path('admin-inventory/', views.inventory_manage, name='inventory_manage'),
    path('admin-inventory/add/', views.item_register, name='item_register'),
    path('admin-items/', views.admin_item_list, name='admin_item_list'),
    path('mypage/', views.mypage, name='mypage'),
    path('email-change/', views.email_change, name='email_change'),
    path('password-change/', views.password_change, name='password_change'),
]

