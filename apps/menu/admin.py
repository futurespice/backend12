from django.contrib import admin
from .models import Menu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('branch', 'category', 'item', 'ingredient')
    search_fields = ('branch__name_of_shop', 'category__name', 'item__name', 'ingredient__name')