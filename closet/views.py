from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Item, ConsiderationItem

# --- 1. トップページ・基本 ---
def top(request):
    return render(request, 'closet/top.html')

def login_view(request):
    return render(request, 'admin_login.html') # フォルダ外にあるため

def signup_view(request):
    return render(request, 'signup.html')

def mypage(request):
    return render(request, 'mypage.html')

# --- 2. 検索・詳細機能 ---
def item_search(request):
    return render(request, 'item_search.html')

def search_results(request):
    query = request.GET.get('q') 
    if query:
        items = Item.objects.filter(
            Q(item_name__icontains=query) | Q(brand_name__icontains=query)
        )
    else:
        items = Item.objects.all() 
    return render(request, 'search_results.html', {'items': items, 'query': query})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'closet/item_detail.html', {'item': item})

# --- 3. 検討リスト機能 (エラー修正済み) ---
def add_to_consideration(request, item_id):
    if request.method == 'POST':
        # ログインしてなければテストユーザーを割り当て
        user = request.user if request.user.is_authenticated else User.objects.first()
        if not user:
            user = User.objects.create_user(username='testuser', password='password123')
            
        item = get_object_or_404(Item, id=item_id)
        
        ConsiderationItem.objects.create(
            user=user,
            item=item,
            size=request.POST.get('size'),
            color=request.POST.get('color'),
            quantity=request.POST.get('count', 1) # モデル名に合わせてquantity
        )
        return redirect('closet:consideration_list')

def consideration_list(request):
    # closetフォルダの中に移動したので 'closet/' を付ける
    items = ConsiderationItem.objects.all().order_by('-added_at')
    return render(request, 'closet/consideration_list.html', {'items': items})

def remove_from_consideration(request, item_id):
    c_item = get_object_or_404(ConsiderationItem, id=item_id)
    c_item.delete()
    return redirect('closet:consideration_list')

# --- 4. 管理者画面・設定系 ---
def admin_login(request):
    return render(request, 'admin_login.html')

def admin_menu(request):
    return render(request, 'admin_menu.html')

def admin_item_list(request):
    return render(request, 'admin_item_list.html')

def inventory_manage(request):
    return render(request, 'inventory_manage.html')

def item_register(request):
    if request.method == 'POST':
        Item.objects.create(
            item_name=request.POST.get('name'),
            brand_name=request.POST.get('brand'),
            price=request.POST.get('price'),
            color=request.POST.get('color'),
            image=request.FILES.get('image'),
            style=",".join(request.POST.getlist('style')),
            kokkaku=",".join(request.POST.getlist('kokkaku')),
            personal_color=",".join(request.POST.getlist('personal_color')),
            free_tags=request.POST.get('free_tags', "")
        )
        return redirect('closet:inventory_manage')
    return render(request, 'item_register.html')

def email_change(request):
    return render(request, 'email_change.html')

def password_change(request):
    return render(request, 'password_change.html')

def signup_complete(request):
    return render(request, 'signup_complete.html')