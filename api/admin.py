from django.contrib import admin
from .models import YamdbUser, Genre, Category, Title, Review, Comment


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
    list_display = ('email', 'username', 'is_staff', 'last_name', 'first_name')
    search_fields = ('text',)
    list_filter = ('date_joined',)
    empty_value_display = '-пусто-'


admin.site.register(YamdbUser, YamdbUserAdmin)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


admin.site.register(Genre, GenreAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


admin.site.register(Category, CategoryAdmin)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'description')


admin.site.register(Title, TitleAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')


admin.site.register(Review, ReviewAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'text', 'author', 'pub_date')


admin.site.register(Comment, CommentAdmin)
