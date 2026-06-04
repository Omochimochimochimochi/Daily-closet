from django.contrib import admin
from .models import Item, ItemAdditionalImage, ConsiderationItem, Order, OrderItem, Tag, Favorite, PurchaseItem

# --- インライン定義 ---
class ItemAdditionalImageInline(admin.TabularInline):
    model = ItemAdditionalImage
    extra = 3

# --- 便利な機能付きでモデルを登録 ---
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemAdditionalImageInline]
    list_display = ('item_name', 'brand_name', 'price', 'is_published', 'stock') 
    list_filter = ('is_published', 'brand_name', 'tags')
    list_editable = ('is_published', 'stock')
    search_fields = ('item_name', 'brand_name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    list_filter = ('created_at',)

@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'price_at_purchase', 'purchased_at')
    list_filter = ('purchased_at',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'created_at')

# --- @admin.register を使わないモデルだけをシンプルに登録 ---
admin.site.register(ConsiderationItem)
admin.site.register(OrderItem)