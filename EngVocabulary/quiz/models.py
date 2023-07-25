from django.db import models

class Category(models.Model):
    class Meta:
        db_table = 'category'
        verbose_name = 'カテゴリー'
        verbose_name_plural = 'カテゴリー'

    category = models.CharField(verbose_name='カテゴリー', max_length=50, unique=True)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    def __str__(self):
        return self.category

class IncorrectJP(models.Model):
    class Meta:
        db_table = 'incorrect_jp'
        verbose_name = '不正解日本語'
        verbose_name_plural = '不正解日本語'

    japanese = models.CharField(verbose_name='日本語', max_length=100, unique=True)
    category = models.ForeignKey(Category, verbose_name='カテゴリー', on_delete=models.PROTECT)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    def __str__(self):
        return self.japanese

class Words(models.Model):
    class Meta:
        db_table = 'words'
        verbose_name = '単語'
        verbose_name_plural = '単語'

    english = models.CharField(verbose_name='英語', max_length=100, unique=True)
    japanese = models.OneToOneField(IncorrectJP, verbose_name='日本語', on_delete=models.PROTECT, max_length=100, unique=True)
    category = models.ForeignKey(Category, verbose_name='カテゴリー', on_delete=models.PROTECT)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    def __str__(self):
        return self.english

    def get_previous_by_pk(self):
        return type(self).objects.filter(pk__lt=self.pk, category=self.category).order_by('pk').last()

    def get_next_by_pk(self):
        return type(self).objects.filter(pk__gt=self.pk, category=self.category).order_by('pk').first()
