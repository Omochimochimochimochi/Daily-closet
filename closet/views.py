from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from .models import Item, ConsiderationItem, Favorite, PurchaseItem, ItemAdditionalImage
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

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
    return render(request, 'closet/login.html')

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
    items = Item.objects.filter(is_published=True)

    raw_tag = request.GET.get("tag", "").strip()
    category = request.GET.get("category", "").strip()

    tags = []

    if raw_tag:
        tags = raw_tag.replace("　", " ").split()

        for tag in tags:
            items = items.filter(
                Q(item_name__icontains=tag) |
                Q(brand_name__icontains=tag) |
                Q(description__icontains=tag) |
                Q(details_text__icontains=tag) |
                Q(kokkaku__icontains=tag) |
                Q(personal_color__icontains=tag) |
                Q(style__icontains=tag) |
                Q(free_tags__icontains=tag)
            )

    if category:
        items = items.filter(category=category)

    # 新しい順
    items = items.order_by("-id")

    # 10件ずつ
    paginator = Paginator(items, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "closet/search_results.html", {
        "items": page_obj,
        "page_obj": page_obj,
        "tags": tags,
        "category": category,
    })            
def item_search(request):
    context = {
        'trending_tags': ["セール", "アウター", "シャツ", "ワイドパンツ"],
        'category_tags': ["洗濯可", "ブルベ", "ミニ丈", "2026SS"]
    }
    return render(request, 'closet/item_search.html', context)



def search_by_tag(request, tag_name=None):
    tag = tag_name or request.GET.get("tag", "")
    clean_tag = tag.replace("#", "").strip()

    items = Item.objects.filter(is_published=True)

    if clean_tag:
        items = items.filter(
            Q(item_name__icontains=clean_tag) |
            Q(free_tags__icontains=clean_tag)
        )
    else:
        items = Item.objects.none()

    return render(request, "closet/search_results.html", {
        "items": items,
        "tags": [clean_tag] if clean_tag else [],
        "category": "",
    })

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
        name = request.POST.get('name')
        price_text = request.POST.get('price')
        image = request.FILES.get('image')

        if not name:
            messages.error(request, "商品名を入力してください")
            return redirect('closet:item_register')

        if not price_text:
            messages.error(request, "価格を入力してください")
            return render(request, 'closet/item_register.html')

        if not image:
            messages.error(request, "商品画像を登録してください")
            return render(request, 'closet/item_register.html')

        try:
            price = int(price_text)
        except ValueError:
            messages.error(request, "価格は数字で入力してください")
            return render(request, 'closet/item_register.html')


        # ここから通常保存処理
        kokkaku_value = ','.join(request.POST.getlist('kokkaku'))
        personal_color_value = ','.join(request.POST.getlist('personal_color'))
        style_value = ','.join(request.POST.getlist('style'))
        free_tags_value = request.POST.get('free_tags', '')

        print("personal_color =", personal_color_value)

        item = Item.objects.create(
            item_name=name,
            brand_name=request.POST.get('brand'),
            price=price,
            color=request.POST.get('color'),
            image=image,
            category=request.POST.get("category"),
            description=request.POST.get('description', ''),
            details_text=request.POST.get('details_text', ''),
            detail_image=request.FILES.get('detail_image'),
            free_tags=free_tags_value,
            personal_color=personal_color_value,
            style=style_value,
            kokkaku=kokkaku_value,
            
        )

        print("保存カテゴリ:", item.category)

        return redirect('closet:inventory_manage')

    return render(request, 'closet/item_register.html')

@staff_member_required
def inventory_manage(request):
    items = Item.objects.filter(is_published=True)
    return render(request, 'inventory_manage.html', {'items': items})

@staff_member_required
def update_publish_status(request, item_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)

    item = get_object_or_404(Item, id=item_id)

    item.is_published = request.POST.get('is_published') == 'true'
    print("保存する値:", item.is_published)

    item.save()

    item.refresh_from_db()
    print("DBの値:", item.is_published)

    return JsonResponse({
        'status': 'success',
        'is_published': item.is_published
    })

@staff_member_required
def admin_login(request):
    return login_view(request)

@staff_member_required
def admin_menu(request):
    return render(request, 'admin_menu.html')

@staff_member_required
@require_POST  # POST通信のみ許可
def item_delete(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return JsonResponse({'status': 'success'})

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


@staff_member_required
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'POST':

        name = request.POST.get('name')
        price_text = request.POST.get('price')

        if not name:
            messages.error(request, "商品名を入力してください")
            return redirect('closet:item_edit', pk=item.pk)

        if not price_text:
            messages.error(request, "価格を入力してください")
            return redirect('closet:item_edit', pk=item.pk)

        try:
            price = int(price_text)
        except ValueError:
            messages.error(request, "価格は数字で入力してください")
            return redirect('closet:item_edit', pk=item.pk)


        item.item_name = name
        item.brand_name = request.POST.get('brand')
        item.price = price
        item.color = request.POST.get('color')
        item.description = request.POST.get('description', '')
        item.details_text = request.POST.get('details_text', '')
        item.category = request.POST.get("category")

        item.kokkaku = ','.join(request.POST.getlist('kokkaku'))
        item.personal_color = ','.join(request.POST.getlist('personal_color'))
        item.style = ','.join(request.POST.getlist('style'))
        item.free_tags = request.POST.get('free_tags', '')


        if request.FILES.get('image'):
            item.image = request.FILES.get('image')

        if request.FILES.get('detail_image'):
            item.detail_image = request.FILES.get('detail_image')


        item.save()


        # 詳細画像追加
        for image_file in request.FILES.getlist('additional_images'):
            ItemAdditionalImage.objects.create(
                item=item,
                image=image_file,
                image_type=1,
            )


        return redirect('closet:inventory_manage')


    return render(request, 'closet/item_edit.html', {'item': item})



@login_required
def update_username(request):
    if request.method == 'POST':
        new_name = request.POST.get('new_username')
        request.user.username = new_name
        request.user.save()
        return redirect('closet:mypage')

@staff_member_required
@require_POST
def delete_additional_image(request, image_id):
    image = get_object_or_404(ItemAdditionalImage, id=image_id)
    image.delete()
    return JsonResponse({'status': 'success'})

# views.py に追加
@staff_member_required
@require_POST
def delete_item_image(request, image_id):
    image = get_object_or_404(ItemAdditionalImage, pk=image_id)
    image.delete()
    return JsonResponse({'status': 'success'})