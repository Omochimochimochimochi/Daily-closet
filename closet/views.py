from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from .models import Item, ConsiderationItem, Favorite, PurchaseItem
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required


# --- 認証・トップ ---
def top(request):
    if request.user.is_authenticated:
        return render(request, 'closet/top_logged_in.html')
    return render(request, 'closet/top.html')

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('closet:top')
        messages.error(request, "ログイン失敗")
    return render(request, 'closet/admin_login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            User.objects.create_user(username=username, password=password)
            return redirect('closet:login')
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('closet:top')

# --- 詳細・検索・お気に入り ---
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    is_favorite = Favorite.objects.filter(user=request.user, item=item).exists() if request.user.is_authenticated else False
    return render(request, 'closet/item_detail.html', {'item': item, 'is_favorite': is_favorite})

def search_results(request):
    items = Item.objects.all()
    raw_tag = request.GET.get('tag')
    
    if raw_tag:
        # 1. 全角スペースも考慮してリスト化
        tags = raw_tag.replace(' ', ' ').split(' ')
        
        # 2. 各タグごとにフィルタリング
        for tag in tags:
            if tag:
                # '#' を含めて検索できるようにする、あるいはタグから '#' を除いて検索するなど統一が必要
                # ここでは「タグ名そのもの」が含まれているかで絞り込みます
                clean_tag = tag.replace('#', '') # '#'を除去して検索文字列をクリーンに
                items = items.filter(Q(item_name__icontains=clean_tag) | Q(free_tags__icontains=clean_tag))
            
def item_search(request):
    context = {
        'trending_tags': ["セール", "アウター", "シャツ", "ワイドパンツ"],
        'category_tags': ["洗濯可", "ブルベ", "ミニ丈", "2026SS"]
    }
    return render(request, 'closet/item_search.html', context)

def search_results(request):
    items = Item.objects.all()
    raw_tag = request.GET.get('tag')
    
    if raw_tag:
        tags = raw_tag.replace(' ', ' ').split(' ')
        for tag in tags:
            if tag:
                clean_tag = tag.replace('#', '')
                items = items.filter(Q(item_name__icontains=clean_tag) | Q(free_tags__icontains=clean_tag))
    
    return render(request, 'closet/search_results.html', {'items': items, 'tag': raw_tag})

def search_by_tag(request, tag_name=None):
    tag = tag_name or request.GET.get('tag')
    # search_resultsとロジックを統一するため、clean_tag化
    clean_tag = tag.replace('#', '') if tag else ""
    items = Item.objects.filter(Q(item_name__icontains=clean_tag) | Q(free_tags__icontains=clean_tag)) if clean_tag else Item.objects.none()
    return render(request, 'closet/search_results.html', {'items': items, 'tag': tag})
@login_required
def toggle_favorite(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, item=item)
    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True
    return JsonResponse({'status': 'success', 'is_favorite': is_favorite})

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'closet/favorite_list.html', {'favorites': favorites})

@login_required
def remove_favorite(request, item_id):
    Favorite.objects.filter(user=request.user, item_id=item_id).delete()
    return redirect('closet:favorite_list')

# --- 検討リスト ---
@login_required
def add_to_consideration(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Item, id=item_id)
        size = request.POST.get('size') or '未選択'
        color = request.POST.get('color') or '未選択'
        quantity = request.POST.get('quantity') or 1
        ConsiderationItem.objects.create(
            user=request.user,
            item=item,
            size=size,
            color=color,
            quantity=quantity
        )
    return redirect('closet:consideration_list')

@login_required
def remove_from_consideration(request, item_id):
    ConsiderationItem.objects.filter(item_id=item_id, user=request.user).delete()
    return redirect('closet:consideration_list')

@login_required
def consideration_list(request):
    considerations = ConsiderationItem.objects.filter(user=request.user).order_by('-id')
    total_price = sum(c.item.price * int(c.quantity) for c in considerations)
    return render(request, 'closet/consideration_list.html', {'considerations': considerations, 'total_price': total_price})

# --- 購入処理 ---
@login_required
def buy_items(request):
    considerations = ConsiderationItem.objects.filter(user=request.user)
    if not considerations.exists():
        return redirect('closet:consideration_list')
    
    with transaction.atomic():
        for c_item in considerations:
            PurchaseItem.objects.create(
                user=request.user,
                item=c_item.item,
                size=c_item.size,
                color=c_item.color,
                quantity=c_item.quantity ,
                price_at_purchase=c_item.item.price
            )
        considerations.delete()
    return redirect('closet:purchase_list')

@login_required
def move_to_purchase(request, item_id):
    c_item = get_object_or_404(ConsiderationItem, id=item_id, user=request.user)
    PurchaseItem.objects.create(
        user=c_item.user, 
        item=c_item.item, 
        size=c_item.size,
        color=c_item.color, 
        quantity=c_item.quantity
    )
    c_item.delete()
    return redirect('closet:purchase_list')

@login_required
def purchase_list(request):
    items = PurchaseItem.objects.filter(user=request.user).order_by('-id')
    return render(request, 'closet/purchase_list.html', {'items': items})

@login_required
def purchase_complete(request):
    return render(request, 'closet/purchase_complete.html')

# --- その他 ---
@staff_member_required
def item_register(request):
    if request.method == 'POST':
        # データを保存
        Item.objects.create(
            item_name=request.POST.get('name'),
            brand_name=request.POST.get('brand'),
            price=request.POST.get('price'),
            color=request.POST.get('color'),
            image=request.FILES.get('image'),
            free_tags=request.POST.get('free_tags', "")
        )
       
        return redirect('inventory_manage') 
    
    return render(request, 'closet/item_register.html')

@staff_member_required
def inventory_manage(request):
    items = Item.objects.all()
    return render(request, 'inventory_manage.html', {'items': items})

@staff_member_required
def admin_login(request):
    return login_view(request)

@staff_member_required
def admin_menu(request):
    return render(request, 'admin_menu.html')

@staff_member_required
def admin_item_list(request):
    return render(request, 'admin_item_list.html', {'items': Item.objects.all()})

@login_required
def password_change(request):
    return render(request, 'password_change.html')

@login_required
def email_change(request):
    return render(request, 'email_change.html')

@login_required
def mypage(request):
    return render(request, 'mypage.html')


def item_edit(request, pk):
    return render(request, 'closet/item_edit.html') 

@login_required
def update_username(request):
    if request.method == 'POST':
        new_name = request.POST.get('new_username')
        request.user.username = new_name
        request.user.save()
        return redirect('closet:mypage')