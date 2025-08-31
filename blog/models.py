from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="分类名称")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL标识")
    description = models.TextField(blank=True, verbose_name="分类描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = "文章分类"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_posts', kwargs={'slug': self.slug})

class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="标签名称")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="URL标识")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
        verbose_name = "文章标签"
        verbose_name_plural = "文章标签"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('tag_posts', kwargs={'slug': self.slug})

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    status = models.CharField(
        max_length=20, 
        choices=[('draft', '草稿'), ('published', '已发布')], 
        default='draft',
        verbose_name="状态"
    )
    
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="文章分类"
    )
    
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="文章标签")
    
    view_count = models.PositiveIntegerField(default=0, verbose_name="浏览次数")
    
    class Meta:
        verbose_name = "博客文章"
        verbose_name_plural = "博客文章"
        ordering = ['-created_at']
    
    #def __str__(self):
    #    return self.title
    def __str__(self):
        return f"{self.title} - {self.author.username}"
    
    def publish(self):
        """发布文章：草稿 → 已发布"""
        if self.status == 'draft':
            self.status = 'published'
            self.save()
            return True
        return False
    
    def archive(self):
        """归档文章：已发布 → 已归档"""
        if self.status == 'published':
            self.status = 'archived'
            self.save()
            return True
        return False
    
    def back_to_draft(self):
        """撤回文章：已发布 → 草稿"""
        if self.status == 'published':
            self.status = 'draft'
            self.save()
            return True
        return False
    
    def is_published(self):
        """检查文章是否已发布"""
        return self.status == 'published'
    
    def is_draft(self):
        """检查文章是否为草稿"""
        return self.status == 'draft'
    
    def increment_view_count(self):
        """增加浏览次数"""
        self.view_count += 1
        self.save(update_fields=['view_count'])


class ActivityLog(models.Model):
    """活动日志模型 - 记录博客系统中的操作"""
    ACTION_CHOICES = [
        ('create_post', '创建文章'),
        ('update_post', '更新文章'),
        ('delete_post', '删除文章'),
        ('create_user', '用户注册'),
    ]
    
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name="操作类型")
    description = models.CharField(max_length=200, verbose_name="操作描述")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="操作用户")
    target_title = models.CharField(max_length=200, blank=True, verbose_name="目标对象标题")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="操作时间")
    
    class Meta:
        verbose_name = "活动日志"
        verbose_name_plural = "活动日志"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_action_display()} - {self.description}"


class Comment(models.Model):
    """文章评论模型"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="文章")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="评论作者")
    content = models.TextField(max_length=1000, verbose_name="评论内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_active = models.BooleanField(default=True, verbose_name="是否有效")
    
    class Meta:
        verbose_name = "文章评论"
        verbose_name_plural = "文章评论"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.author.username} 评论了 {self.post.title}"