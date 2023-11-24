from django.contrib import admin
from .models import Menu

class MenuAdmin(admin.ModelAdmin):
    list_display = ('branch', 'category', 'item', 'ingredient')

admin.site.register(Menu, MenuAdmin)