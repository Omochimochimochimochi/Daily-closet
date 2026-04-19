from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Item, ConsiderationItem, PurchaseItem
from django.contrib.auth.models import User
from django.contrib import messages

# --- 1. トップページ・基本 ---
def top(request):
    return render(request, 'closet/top.html')

def login_view(request):
    return render(request, 'admin_login.html')

def signup(request):
    if request.method == 'POST':
        # 送られてきたデータを受け取る
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # 簡易的なユーザー作成処理（本来はフォームを使うのがベスト）
        if username and password:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('closet:top') # 登録後にトップへ移動
            
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

# --- 3. 検討リスト・購入フロー ---
def consideration_list(request):
    items = ConsiderationItem.objects.all().order_by('-added_at')
    return render(request, 'closet/consideration_list.html', {'items': items})

def add_to_consideration(request, item_id):
    if request.method == 'POST':
        user = request.user if request.user.is_authenticated else User.objects.first()
        if not user:
            user = User.objects.create_user(username='testuser', password='password123')
        item = get_object_or_404(Item, id=item_id)
        ConsiderationItem.objects.create(
            user=user, item=item, size=request.POST.get('size'),
            color=request.POST.get('color'), quantity=request.POST.get('count', 1)
        )
        return redirect('closet:consideration_list')

def remove_from_consideration(request, item_id):
    c_item = get_object_or_404(ConsiderationItem, id=item_id)
    c_item.delete()
    return redirect('closet:consideration_list')

def move_to_purchase(request, item_id):
    c_item = get_object_or_404(ConsiderationItem, id=item_id)
    PurchaseItem.objects.create(
        user=c_item.user, item=c_item.item, size=c_item.size,
        color=c_item.color, quantity=c_item.quantity
    )
    c_item.delete()
    return redirect('closet:purchase_list')

def purchase_list(request):
    items = PurchaseItem.objects.all().order_by('-added_at')
    return render(request, 'closet/purchase_list.html', {'items': items})

def purchase_complete(request):
    items_to_buy = PurchaseItem.objects.all()
    bought_items = list(items_to_buy) 
    items_to_buy.delete()
    return render(request, 'closet/purchase_complete.html', {'items': bought_items})

def email_change(request):
    # とりあえずマイページに戻すか、空のページを表示する
    return render(request, 'mypage.html') # もしくは適切なテンプレートへ

# --- 4. 管理者画面 ---
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

def password_change(request):
    # パスワード変更画面を表示するだけの仮の関数
    return render(request, 'password_change.html')

def email_change(request):
    # メール変更画面を表示するだけの仮の関数
    return render(request, 'email_change.html')

def search_by_tag(request):
    tag = request.GET.get('tag')
    if tag:
        items = Item.objects.filter(free_tags__icontains=tag)
    else:
        items = Item.objects.none()
    return render(request, 'search_results.html', {'items': items, 'tag': tag})