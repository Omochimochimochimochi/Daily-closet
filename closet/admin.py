from django.contrib import admin
from .models import Item, ItemAdditionalImage, ConsiderationItem, Tag, Order, OrderItem

admin.site.register(Item)
admin.site.register(ItemAdditionalImage)
admin.site.register(ConsiderationItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Tag)