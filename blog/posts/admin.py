from django.contrib import admin

from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'publish_date', 'author']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'connected_post', 'author', 'comments', 'date_of_comment']

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
