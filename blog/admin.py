from django.contrib import admin
from .models import Post, Category, Tag, ActivityLog, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'get_status_actions')
    list_filter = ('status', 'created_at', 'author')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
    
    def get_status_actions(self, obj):
        """在列表页面显示状态操作按钮"""
        if obj.status == 'draft':
            return '<a href="/admin/blog/post/{}/publish/">发布</a>'.format(obj.id)
        elif obj.status == 'published':
            return '<a href="/admin/blog/post/{}/archive/">归档</a>'.format(obj.id)
        return '-'
    
    get_status_actions.short_description = '操作'
    get_status_actions.allow_tags = True
    
    def publish_post(self, request, queryset):
        """批量发布文章"""
        updated = queryset.filter(status='draft').update(status='published')
        self.message_user(request, f'成功发布 {updated} 篇文章')
    
    def archive_post(self, request, queryset):
        """批量归档文章"""
        updated = queryset.filter(status='published').update(status='archived')
        self.message_user(request, f'成功归档 {updated} 篇文章')
    
    publish_post.short_description = "发布选中的文章"
    archive_post.short_description = "归档选中的文章"
    
    actions = [publish_post, archive_post]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'description', 'user', 'target_title', 'created_at')
    list_filter = ('action', 'created_at', 'user')
    search_fields = ('description', 'target_title')
    readonly_fields = ('action', 'description', 'user', 'target_title', 'created_at')
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        # 不允许手动添加日志记录
        return False
    
    def has_change_permission(self, request, obj=None):
        # 不允许修改日志记录
        return False

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at', 'author')
    search_fields = ('content', 'author__username', 'post__title')
    list_editable = ('is_active',)
    date_hierarchy = 'created_at'
    
    def approve_comments(self, request, queryset):
        """批量批准评论"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'成功批准 {updated} 条评论')
    
    def disapprove_comments(self, request, queryset):
        """批量禁用评论"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'成功禁用 {updated} 条评论')
    
    approve_comments.short_description = "批准选中的评论"
    disapprove_comments.short_description = "禁用选中的评论"
    
    actions = [approve_comments, disapprove_comments]