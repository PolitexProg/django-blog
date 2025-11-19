# blog/admin.py

from django.contrib import admin
from .models import Post, Category, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('author', 'content', 'created_at',)
    can_delete = False


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'category',
        'is_approved',
        'views_count',
        'created_at'
    )
    list_filter = ('is_approved', 'category', 'created_at',)
    search_fields = ('title', 'content', 'author__username',)
    readonly_fields = ('created_at', 'updated_at', 'views_count',)
    fields = (
        ('title', 'category', 'is_approved'),
        'image',
        'content',
        'tags',
        ('author', 'views_count'),
        ('created_at', 'updated_at')
    )
    inlines = [CommentInline]

    actions = ['approve_posts', 'disapprove_posts']

    @admin.action(description='Approve selected posts')
    def approve_posts(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} posts have been successfully approved.")

    @admin.action(description='Submit for revision (Not approve)')
    def disapprove_posts(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f"{queryset.count()} posts have not been successfully approved.")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'author', 'content_snippet', 'created_at',)
    list_filter = ('created_at', 'author',)
    search_fields = ('content', 'author__username',)
    readonly_fields = ('post', 'author', 'created_at', 'content',)

    def post_title(self, obj):
        return obj.post.title

    post_title.short_description = 'Post'

    def content_snippet(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_snippet.short_description = 'Comments'