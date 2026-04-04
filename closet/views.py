from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import Item

def top(request):
    # closet/templates/closet/top.html を探しに行って表示する
    return render(request, 'closet/top.html')

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def password_reset_view(request):
    return render(request, 'password_reset.html')

def password_reset_done_view(request):
    return render(request, 'password_reset_done.html')

def password_reset_confirm_view(request):
    return render(request, 'password_reset_confirm.html')

    
def signup_complete(request):
    return render(request, 'signup_complete.html')

def mypage(request):
    return render(request, 'mypage.html')    

def email_change(request):
    return render(request, 'email_change.html')

def password_change(request):
    return render(request, 'password_change.html')
    
def item_search(request):
    return render(request, 'item_search.html')
    
def admin_login(request):
    return render(request, 'admin_login.html')

def admin_menu(request):
    return render(request, 'admin_menu.html')

def inventory_manage(request):
    return render(request, 'inventory_manage.html')


def admin_item_list(request):
    return render(request, 'admin_item_list.html')
    
def inventory_manage(request):
    return render(request, 'inventory_manage.html')

def admin_item_list(request):
    return render(request, 'admin_item_list.html')


def item_register(request):
    if request.method == 'POST':
        name_value = request.POST.get('name')
        brand_value = request.POST.get('brand')
        price_value = request.POST.get('price')
        color_value = request.POST.get('color')
        image_file = request.FILES.get('image')

        styles = request.POST.getlist('style')
        kokkakus = request.POST.getlist('kokkaku')
        pc_colors = request.POST.getlist('personal_color')
        free_tags_value = request.POST.get('free_tags', "")

        item = Item.objects.create(
            item_name=name_value,
            brand_name=brand_value,
            price=price_value,
            color=color_value,
            image=image_file,
            style=",".join(styles),
            kokkaku=",".join(kokkakus),
            personal_color=",".join(pc_colors),
            free_tags=free_tags_value
        )
        return redirect('inventory_manage')

    return render(request, 'item_register.html')

from django.shortcuts import render, get_object_or_404
from .models import Item


def item_search(request):
    return render(request, 'item_search.html')

def search_results(request):

    query = request.GET.get('q', '')
    
    if query:
        items = Item.objects.filter(tags__contains=query)
    else:
        
        items = Item.objects.all()
        
    return render(request, 'search_results.html', {
        'items': items,
        'query': query
    })

def search_results(request):
    items = Item.objects.all() 
   
    return render(request, 'search_results.html', {'items': items})