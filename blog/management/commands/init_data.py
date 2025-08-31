from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag
from django.utils import timezone


class Command(BaseCommand):
    help = '初始化博客数据'

    def handle(self, *args, **options):
        # 创建分类
        tech_category, created = Category.objects.get_or_create(
            name='技术分享',
            defaults={'slug': 'tech', 'description': '技术相关文章'}
        )
        
        life_category, created = Category.objects.get_or_create(
            name='生活随笔', 
            defaults={'slug': 'life', 'description': '生活感悟和随想'}
        )

        # 创建标签
        django_tag, created = Tag.objects.get_or_create(
            name='Django',
            defaults={'slug': 'django'}
        )
        
        python_tag, created = Tag.objects.get_or_create(
            name='Python',
            defaults={'slug': 'python'}
        )
        
        web_tag, created = Tag.objects.get_or_create(
            name='Web开发',
            defaults={'slug': 'web-dev'}
        )

        # 获取或创建作者
        try:
            author = User.objects.get(username='admin')
        except User.DoesNotExist:
            author = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )

        # 创建示例文章
        posts_data = [
            {
                'title': '欢迎来到我的博客！',
                'content': '''# 欢迎！

这是我的第一篇博客文章。在这里我会分享一些关于编程、技术和生活的想法。

## 关于这个博客

这个博客是用Django框架搭建的，部署在Render平台上。

### 功能特性

- 文章发布和管理
- 分类和标签系统  
- 搜索功能
- 响应式设计

希望你会喜欢这里的内容！''',
                'category': life_category,
                'tags': [web_tag],
                'status': 'published'
            },
            {
                'title': 'Django博客搭建教程',
                'content': '''# Django博客搭建指南

今天分享一下如何用Django搭建一个完整的博客系统。

## 主要步骤

1. **环境准备**
   - 安装Python和Django
   - 创建虚拟环境

2. **模型设计**
   - Post模型（文章）
   - Category模型（分类）
   - Tag模型（标签）

3. **视图和模板**
   - 文章列表页
   - 文章详情页
   - 搜索功能

4. **部署上线**
   - 使用Render平台
   - 配置环境变量
   - 数据库迁移

这个过程虽然有些复杂，但一步步来就不难了！''',
                'category': tech_category,
                'tags': [django_tag, python_tag, web_tag],
                'status': 'published'
            },
            {
                'title': 'Python编程小技巧',
                'content': '''# Python实用技巧分享

作为一个Python爱好者，这里分享一些日常编程中的小技巧。

## 1. 列表推导式

```python
# 传统方法
squares = []
for i in range(10):
    squares.append(i**2)

# 列表推导式
squares = [i**2 for i in range(10)]
```

## 2. 字典推导式

```python
# 创建字典
word_lengths = {word: len(word) for word in ['hello', 'world', 'python']}
```

## 3. 使用enumerate

```python
# 获取索引和值
for index, value in enumerate(['a', 'b', 'c']):
    print(f"{index}: {value}")
```

这些小技巧能让代码更加简洁优雅！''',
                'category': tech_category,
                'tags': [python_tag],
                'status': 'published'
            }
        ]

        # 创建文章
        for post_data in posts_data:
            tags = post_data.pop('tags')
            post, created = Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    **post_data,
                    'author': author,
                    'created_at': timezone.now()
                }
            )
            if created:
                post.tags.set(tags)
                self.stdout.write(
                    self.style.SUCCESS(f'创建文章: {post.title}')
                )

        self.stdout.write(
            self.style.SUCCESS('数据初始化完成！')
        )