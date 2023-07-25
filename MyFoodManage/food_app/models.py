import uuid
from django.db import models

class Category(models.Model):
    class Meta:
        db_table = "category"
        verbose_name = "カテゴリー"
        verbose_name_plural = "カテゴリー"

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    category = models.CharField(verbose_name="カテゴリー", max_length=25, unique=True)
    created_date = models.DateTimeField(verbose_name="作成日", auto_now_add=True)
    updated_date = models.DateTimeField(verbose_name="更新日", auto_now=True)

    def __str__(self):
        return self.category

class Food(models.Model):
    class Meta:
        db_table = "food"
        verbose_name = "食材"
        verbose_name_plural = "食材"

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(verbose_name="食材名", max_length=50)
    category = models.ForeignKey(Category, verbose_name="カテゴリー", on_delete=models.PROTECT)
    expiry_date = models.DateField(verbose_name="賞味期限", null=True, blank=True)
    expiration_date = models.DateField(verbose_name="消費期限", null=True, blank=True)

    # ToDo: commentをmemoに変更する
    memo = models.TextField(verbose_name="メモ", null=True, blank=True)
    created_date = models.DateTimeField(verbose_name="作成日", auto_now_add=True)
    updated_date = models.DateTimeField(verbose_name="更新日", auto_now=True)

    def __str__(self):
        return self.name