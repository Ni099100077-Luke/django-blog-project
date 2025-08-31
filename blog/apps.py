from django.apps import AppConfig
from django.core.checks import register, Error


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = "博客管理"  # 在Django后台显示的中文名称
    
    def ready(self):
        """应用准备就绪时执行的初始化代码"""
        # 导入信号处理器（如果有的话）
        try:
            import blog.signals
        except ImportError:
            pass  # 如果没有signals.py文件，就跳过
        
        # 打印应用启动信息（开发时有用）
        print(f"✅ {self.verbose_name} 应用已成功加载")


@register()
def check_blog_settings(app_configs, **kwargs):
    """自定义系统检查：确保博客应用配置正确"""
    errors = []
    
    # 检查是否有必要的设置
    from django.conf import settings
    
    # 例子：检查是否配置了邮件设置（用于发送通知）
    if not hasattr(settings, 'EMAIL_BACKEND'):
        errors.append(
            Error(
                '建议配置邮件后端以发送博客通知',
                hint='在settings.py中添加EMAIL_BACKEND设置',
                id='blog.E001',
            )
        )
    
    return errors
