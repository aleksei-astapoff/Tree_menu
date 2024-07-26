from django.contrib import admin

from .models import MenuItem

admin.site.empty_value_display = '-Не задано-'


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """Администрирование пунктов меню"""

    list_display = ('name', 'parent', 'menu_name')
    list_filter = ('menu_name',)
    search_fields = ('name', 'url', 'named_url')
