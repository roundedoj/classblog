from django.contrib import admin

from .models import Comment, Post

admin.site.site_header = 'GIZ Python Class Blog Administration'
admin.site.site_title = 'Blog Admin'
admin.site.index_title = 'Manage your blog'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('likes',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('body', 'user__username')
    actions = ['hide_comments', 'show_comments']

    @admin.action(description='Hide selected comments')
    def hide_comments(self, request, queryset):
        queryset.update(active=False)

    @admin.action(description='Show selected comments')
    def show_comments(self, request, queryset):
        queryset.update(active=True)