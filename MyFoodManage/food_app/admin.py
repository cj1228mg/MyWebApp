from django.contrib import admin
from .models import Food, Category

class FoodAdmin(admin.ModelAdmin):
    list_display = ("uuid", "name", "category", "expiry_date", "expiration_date", "memo", "created_date", "updated_date")

admin.site.register(Category)
admin.site.register(Food, FoodAdmin)