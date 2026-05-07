from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout  # 追加
from django.contrib import messages
from django.http import JsonResponse
from .models import Item, ConsiderationItem, PurchaseItem

# --- 1. 認証・トップページ ---

def top(request):
    if request.user.is_authenticated:
        # ログインしているならログイン後のページへ
        return render(request, 'closet/top_logged_in.html')
    else:
        # 未ログインなら通常のトップページへ
        return render(request, 'closet/top.html')

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        # Djangoの標準認証機能でチェック
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            login(request, user)
            messages.success(request, "ログインしました！")
            return redirect('closet:top')  # 成功したらトップへ
        else:
            messages.error(request, "ユーザー名またはパスワードが正しくありません。")
            
    # GETの時、または失敗時はログイン画面を表示
    return render(request, 'admin_login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if username and password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "このユーザー名は既に使用されています。")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "会員登録が完了しました。ログインしてください。")
                return redirect('closet:login')
                
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('closet:top')


# --- 2. 検索・詳細機能 ---

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    # 既にお気に入り登録されているかチェック（ハートの色のため）
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = ConsiderationItem.objects.filter(user=request.user, item=item).exists()
    
    return render(request, 'closet/item_detail.html', {
        'item': item,
        'is_favorite': is_favorite
    })

def search_results(request):
    query = request.GET.get('q') 
    if query:
        items = Item.objects.filter(
            Q(item_name__icontains=query) | Q(brand_name__icontains=query)
        )
    else:
        items = Item.objects.all() 
    return render(request, 'search_results.html', {'items': items, 'query': query})

# お気に入り登録（これ1つにまとめました！）
@login_required
def toggle_favorite(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Item, id=item_id)
        
        # すでに検討リストにあるか確認
        consideration, created = ConsiderationItem.objects.get_or_create(
            user=request.user,
            item=item
        )
        
        if not created:
            # すでにある場合は削除（お気に入り解除）
            consideration.delete()
            status = 'removed'
        else:
            # 新しく作った場合はそのまま（お気に入り登録）
            status = 'added'
            
        return JsonResponse({'status': 'ok', 'action': status})
    
    return JsonResponse({'status': 'error'}, status=400)


# --- 3. 検討リスト・購入フロー ---

def consideration_list(request):
    # ログインユーザーのアイテムだけを表示
    if request.user.is_authenticated:
        items = ConsiderationItem.objects.filter(user=request.user).order_by('-added_at')
    else:
        items = ConsiderationItem.objects.none()
    return render(request, 'closet/consideration_list.html', {'items': items})

def move_to_purchase(request, item_id):
    c_item = get_object_or_404(ConsiderationItem, id=item_id)
    PurchaseItem.objects.create(
        user=c_item.user, item=c_item.item, size=c_item.size,
        color=c_item.color, quantity=c_item.quantity
    )
    c_item.delete()
    return redirect('closet:purchase_list')

def purchase_list(request):
    if request.user.is_authenticated:
        items = PurchaseItem.objects.filter(user=request.user).order_by('-added_at')
    else:
        items = PurchaseItem.objects.none()
    return render(request, 'closet/purchase_list.html', {'items': items})

def purchase_complete(request):
    if request.user.is_authenticated:
        items_to_buy = PurchaseItem.objects.filter(user=request.user)
        bought_items = list(items_to_buy) 
        items_to_buy.delete()
        return render(request, 'closet/purchase_complete.html', {'items': bought_items})
    return redirect('closet:top')

# --- 4. 管理者・ユーザー設定 ---

def my_page(request):
    return render(request, 'closet/my_page.html', {'user': request.user})

def inventory_manage(request):
    items = Item.objects.all()
    return render(request, 'inventory_manage.html', {'items': items})

def item_search(request):
    return render(request, 'item_search.html')

def password_change(request):
    return render(request, 'password_change.html')

def email_change(request):
    return render(request, 'email_change.html')

def admin_login(request):
    return login_view(request)

def admin_menu(request):
    return render(request, 'admin_menu.html')

def admin_item_list(request):
    return render(request, 'admin_item_list.html')


def search_by_tag(request, tag_name=None):
    tag = tag_name or request.GET.get('tag')
    if tag:
        items = Item.objects.filter(free_tags__icontains=tag)
    else:
        items = Item.objects.none()
    return render(request, 'search_results.html', {'items': items, 'tag': tag})

def add_to_consideration(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Item, id=item_id)
        ConsiderationItem.objects.get_or_create(user=request.user, item=item)
        return redirect('closet:consideration_list')
    return redirect('closet:top')

def remove_from_consideration(request, item_id):
    c_item = get_object_or_404(ConsiderationItem, id=item_id, user=request.user)
    c_item.delete()
    return redirect('closet:consideration_list')



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

def inventory_manage(request):
    items = Item.objects.all()
    return render(request, 'inventory_manage.html', {'items': items})

def mypage(request):
    return render(request, 'mypage.html')