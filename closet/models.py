from django.db import models  

class Item(models.Model):
    # 基本情報
    brand_name = models.CharField("ブランド名", max_length=100, blank=True)
    item_name = models.CharField("アイテム名", max_length=100)
    price = models.IntegerField("金額", default=0)
    color = models.CharField("カラー", max_length=50, blank=True)
    image = models.ImageField("アイテム画像", upload_to='items/', blank=True, null=True)

  
    STYLE_CHOICES = [
        ('simple', '#シンプル'),
        ('kireime', '#きれいめ'),
        ('aline', '#Aライン'),
        ('iline', '#Iライン'),
        ('sale', '#セール'),
    ]
    style = models.CharField("スタイル", max_length=20, choices=STYLE_CHOICES, blank=True)

    KOKKAKU_CHOICES = [
        ('straight', '#ストレート'),
        ('wave', '#ウェーブ'),
        ('natural', '#ナチュラル'),
    ]
    kokkaku = models.CharField("骨格タイプ", max_length=20, choices=KOKKAKU_CHOICES, blank=True)

    COLOR_TYPE_CHOICES = [
        ('yebe', '#イエベ'),
        ('burube', '#ブルベ'),
        ('neutral', '#ニュートラル'),
    ]
    personal_color = models.CharField("パーソナルカラー", max_length=20, choices=COLOR_TYPE_CHOICES, blank=True)

    free_tags = models.TextField("自由記入タグ", blank=True)

    def __str__(self):
        return self.item_name