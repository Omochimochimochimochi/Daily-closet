from django.contrib import admin
from .models import Item, ItemAdditionalImage, ConsiderationItem, PurchaseItem, Tag

admin.site.register(Item)
admin.site.register(ItemAdditionalImage)
admin.site.register(ConsiderationItem)
admin.site.register(PurchaseItem)
admin.site.register(Tag)