from django.contrib import admin
from .models import Item, ItemAdditionalImage, ConsiderationItem, Order, OrderItem, Tag, Favorite


class ItemAdditionalImageInline(admin.TabularInline):
    model = ItemAdditionalImage
    extra = 3  # 最初から表示しておく入力欄の数（お好みで！）

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemAdditionalImageInline]
    
    # 一覧に表示する項目（モデルにある実際のフィールド名に合わせてください）
    list_display = ('item_name', 'price') 
    
    # ★ 右側に「絞り込み」メニューを出す（カテゴリーに相当するフィールド名を指定）
    # もしモデルの項目名が 'category' ならこれで動きます
    # list_filter = ('category',)
    
admin.site.register(ConsiderationItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Tag)
admin.site.register(Favorite)