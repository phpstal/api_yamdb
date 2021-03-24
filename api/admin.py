from django.contrib import admin

from .models import Comment, Review


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'pub_date', 'review')
    
admin.site.register(Comment, CommentsAdmin)


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date') 

admin.site.register(Review, ReviewsAdmin)   