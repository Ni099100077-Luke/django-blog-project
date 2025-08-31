"""
博客应用的信号处理器
用于在模型事件发生时自动执行特定操作
"""
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Post, Category, ActivityLog


@receiver(post_save, sender=Post)
def post_saved_handler(sender, instance, created, **kwargs):
    """文章保存后的处理器"""
    if created:
        # 新创建文章时的操作
        print(f"📝 新文章已创建：{instance.title}")
        ActivityLog.objects.create(
            action='create_post',
            description=f"创建了新文章：{instance.title}",
            user=instance.author,
            target_title=instance.title
        )
    else:
        # 文章更新时的操作
        print(f"✏️ 文章已更新：{instance.title}")
        ActivityLog.objects.create(
            action='update_post',
            description=f"更新了文章：{instance.title}",
            user=instance.author,
            target_title=instance.title
        )


@receiver(post_save, sender=User)
def user_created_handler(sender, instance, created, **kwargs):
    """用户创建后的处理器"""
    if created:
        print(f"👤 新用户已注册：{instance.username}")
        ActivityLog.objects.create(
            action='create_user',
            description=f"新用户注册：{instance.username}",
            user=instance,
            target_title=instance.username
        )


@receiver(pre_delete, sender=Post)
def post_delete_handler(sender, instance, **kwargs):
    """文章删除前的处理器"""
    print(f"🗑️ 即将删除文章：{instance.title}")
    ActivityLog.objects.create(
        action='delete_post',
        description=f"删除了文章：{instance.title}",
        user=instance.author,
        target_title=instance.title
    )


# 您可以在这里添加更多信号处理器
# 比如：自动创建分类、发送邮件通知、清理缓存等
