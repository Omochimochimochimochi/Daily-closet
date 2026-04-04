from django.db import models

class Item(models.Model):
    brand_name = models.CharField("ブランド名", max_length=100, blank=True)
    item_name = models.CharField("アイテム名", max_length=100)
    price = models.IntegerField("金額", default=0)
    color = models.CharField("カラー", max_length=50, blank=True)
    image = models.ImageField("アイテム画像", upload_to='items/', blank=True, null=True)

    style = models.CharField("スタイル", max_length=100, blank=True)
    kokkaku = models.CharField("骨格タイプ", max_length=100, blank=True)
    personal_color = models.CharField("パーソナルカラー", max_length=100, blank=True)
    free_tags = models.TextField("自由記入タグ", blank=True)

    description = models.TextField("アイテム説明", blank=True)
    details_text = models.TextField("アイテム詳細", blank=True)
    detail_image = models.ImageField("詳細画像", upload_to='details/', blank=True, null=True)

    def __str__(self):
        return self.item_name
    
   
class ItemAdditionalImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField("追加詳細画像", upload_to='items/extra/')

    def __str__(self):
        return f"{self.item.item_name} の追加画像"