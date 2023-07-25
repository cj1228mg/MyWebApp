from django.contrib import admin

from .models import Category, IncorrectJP, Words

class WordsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'english', 'japanese', 'category', 'created_at', 'updated_at')

admin.site.register(Category)
admin.site.register(IncorrectJP)
admin.site.register(Words, WordsAdmin)
