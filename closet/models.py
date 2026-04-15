from django.conf import settings
from django.db import models

from django.contrib.auth.models import User

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
    

class ConsiderationItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # 商品と紐付け（Itemモデルを参照）
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    
    # 詳細画面で選んだ特定の情報を保存
    size = models.CharField("サイズ", max_length=50)
    color = models.CharField("カラー", max_length=50)
    quantity = models.IntegerField("数量", default=1)
    
    added_at = models.DateTimeField("登録日時", auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}の検討リスト: {self.item.item_name}"
    
   

class PurchaseItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.item.item_name} (Purchase)"