from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from .models import Item, ConsiderationItem, Order, OrderItem, Favorite

# 認証・トップ
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

# 詳細・検索
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    is_favorite = Favorite.objects.filter(user=request.user, item=item).exists() if request.user.is_authenticated else False
    return render(request, 'closet/item_detail.html', {'item': item, 'is_favorite': is_favorite})

def search_results(request):
    items = Item.objects.all()
    tag = request.GET.get('tag')
    if tag:
        items = items.filter(Q(item_name__icontains=tag) | Q(free_tags__icontains=tag))
    return render(request, 'closet/search_results.html', {'items': items})

def item_search(request):
    return render(request, 'closet/item_search.html')

def search_by_tag(request, tag_name=None):
    tag = tag_name or request.GET.get('tag')
    items = Item.objects.filter(free_tags__icontains=tag) if tag else Item.objects.none()
    return render(request, 'closet/search_results.html', {'items': items, 'tag': tag})

# お気に入り
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

# 検討リスト
@login_required
def add_to_consideration(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Item, id=item_id)
        ConsiderationItem.objects.get_or_create(user=request.user, item=item)
    return redirect('closet:consideration_list')

@login_required
def remove_from_consideration(request, item_id):
    ConsiderationItem.objects.filter(id=item_id, user=request.user).delete()
    return redirect('closet:consideration_list')

@login_required
def consideration_list(request):
    considerations = ConsiderationItem.objects.filter(user=request.user).order_by('-added_at')
    total_price = sum(c.item.price * c.quantity for c in considerations)
    return render(request, 'closet/consideration_list.html', {'considerations': considerations, 'total_price': total_price})

# 管理・その他
def inventory_manage(request):
    return render(request, 'inventory_manage.html', {'items': Item.objects.all()})

def mypage(request):
    return render(request, 'mypage.html')

@login_required
def purchase_list(request):
    # 購入履歴などのデータを取得して表示する関数
    # ※もし PurchaseItem というモデルがない場合は、一旦空のリストを渡すだけでもエラーは消えます
    from .models import PurchaseItem # モデルが別にある場合はインポートが必要
    items = PurchaseItem.objects.filter(user=request.user).order_by('-added_at')
    return render(request, 'closet/purchase_list.html', {'items': items})

# 検討リストから購入リストへ移動する処理
@login_required
def move_to_purchase(request, item_id):
    from .models import PurchaseItem # 購入モデルのインポート
    c_item = get_object_or_404(ConsiderationItem, id=item_id, user=request.user)
    # 検討リストのデータを購入モデルにコピーして作成
    PurchaseItem.objects.create(
        user=c_item.user, 
        item=c_item.item, 
        size=c_item.size,
        color=c_item.color, 
        quantity=c_item.quantity
    )
    c_item.delete() # 検討リストからは削除
    return redirect('closet:purchase_list')

@login_required
def purchase_complete(request):
    return render(request, 'closet/purchase_complete.html')


def admin_login(request):
    return login_view(request)

def admin_menu(request):
    return render(request, 'admin_menu.html')

# アイテム登録用
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

# 念のため追加（urls.pyにありそうなもの）
def admin_item_list(request):
    return render(request, 'admin_item_list.html', {'items': Item.objects.all()})

def password_change(request):
    return render(request, 'password_change.html')

def email_change(request):
    return render(request, 'email_change.html')