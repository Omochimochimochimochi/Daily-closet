from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# 1. Tagモデル
class Tag(models.Model):
    name = models.CharField("タグ名", max_length=50, unique=True)
    def __str__(self):
        return self.name

# 2. Itemモデル
class Item(models.Model):
    brand_name = models.CharField("ブランド名", max_length=100, blank=True)
    item_name = models.CharField("アイテム名", max_length=100)
    price = models.IntegerField("金額", default=0)
    color = models.CharField("カラー", max_length=50, blank=True)
    image = models.ImageField("アイテム画像", upload_to='items/', blank=True, null=True)
    stock = models.IntegerField(default=0)

    # tags はここに1つだけ残します
    tags = models.ManyToManyField(Tag, verbose_name="タグ", blank=True)

    style = models.CharField("スタイル", max_length=100, blank=True)
    kokkaku = models.CharField("骨格タイプ", max_length=100, blank=True)
    personal_color = models.CharField("パーソナルカラー", max_length=100, blank=True)
    free_tags = models.TextField("自由記入タグ", blank=True)

    description = models.TextField("アイテム説明", blank=True)
    details_text = models.TextField("アイテム詳細", blank=True)
    detail_image = models.ImageField("詳細画像", upload_to='details/', blank=True, null=True)

    def __str__(self):
        return self.item_name
   
# 3. 追加画像
class ItemAdditionalImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField("追加詳細画像", upload_to='items/extra/')

    def __str__(self):
        return f"{self.item.item_name} の追加画像"

# 4. 検討リスト（お気に入り）
# models.py
class ConsiderationItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    size = models.CharField(max_length=50)   # これが必要！
    color = models.CharField(max_length=50)  # これが必要！
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.user.username}の検討リスト: {self.item.item_name}"
    
class Favorite(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# 5. 注文の「親」（レシート本体）
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="購入者")
    created_at = models.DateTimeField("購入日時", auto_now_add=True)

    def __str__(self):
        return f"注文ID:{self.id} - {self.user.username}"

# 6. 注文の「子」（レシートの明細）
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="注文")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="商品")
    size = models.CharField("サイズ", max_length=10)
    color = models.CharField("カラー", max_length=20)
    quantity = models.PositiveIntegerField("数量", default=1)
    price_at_purchase = models.IntegerField("購入時の価格") # 必須：価格変動に備える

    def __str__(self):
        return f"{self.item.item_name} ({self.quantity})"
    

class PurchaseItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField("購入日時", auto_now_add=True)
    size = models.CharField("サイズ", max_length=50, default="未選択")
    color = models.CharField("カラー", max_length=50, default="未選択")

    def __str__(self):
        return f"{self.user.username} - {self.item.item_name}"
    

