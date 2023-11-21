# menu/admin.py
from django.contrib import admin
from .models import Menu
from apps.branches.models import Branch
from apps.storage.models import Category, Item, Ingredient

class MenuAdmin(admin.ModelAdmin):
    list_display = ('branch', 'category', 'item', 'ingredient')

admin.site.register(Menu, MenuAdmin)
admin.site.register(Branch)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Ingredient)
