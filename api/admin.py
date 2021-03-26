from django.contrib import admin
from .models import YamdbUser


class YamdbUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password',)
        }),
        ('Персональная информация', {
            'classes': ('wide'),
            'fields': (('last_name', 'first_name'), 'bio'),
        }),
        ('Права доступа', {
            'classes': ('wide',),
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser'),
        }),
        ('Важные даты', {
            'classes': ('collapse',),
            'fields': ('last_login', 'date_joined'),
        })
    )    
    list_display = ('email', 'username', 'last_name', 'first_name')
    search_fields = ('text',)
    list_filter = ('date_joined',)
    empty_value_display = '-пусто-'


admin.site.register(YamdbUser, YamdbUserAdmin)