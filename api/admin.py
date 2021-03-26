from django.contrib import admin
from .models import YamdbUser, Comment, Review


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
            'fields': ('role', 'is_active', 'is_superuser'),
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


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'pub_date', 'review')

admin.site.register(Comment, CommentsAdmin)

              
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date') 


admin.site.register(Review, ReviewsAdmin)