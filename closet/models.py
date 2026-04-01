# views.py の中身を以下のように修正
def item_register(request):
    if request.method == 'POST':

        name_val = request.POST.get('name')   
        brand_val = request.POST.get('brand')
        price_val = request.POST.get('price')
        color_val = request.POST.get('color')
        image_file = request.FILES.get('image')

        styles = request.POST.getlist('style')
        kokkakus = request.POST.getlist('kokkaku')
        colors = request.POST.getlist('personal_color')
        free_tags_val = request.POST.get('free_tags', "")

        item = Item.objects.create(
            item_name=name_val,        
            brand_name=brand_val,      
            price=price_val,           
            color=color_val,          
            image=image_file,        
            style=",".join(styles),
            kokkaku=",".join(kokkakus),
            personal_color=",".join(colors),
            free_tags=free_tags_val
        )
        
        return redirect('inventory_manage')

    return render(request, 'item_register.html')