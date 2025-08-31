from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post

class LatestPostsFeed(Feed):
    """最新文章RSS Feed"""
    title = "我的博客 - 最新文章"
    link = "/rss/"
    description = "我的博客的最新文章更新"
    
    def items(self):
        """返回最新的20篇已发布文章"""
        return Post.objects.filter(status='published').order_by('-created_at')[:20]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.content
    
    def item_author_name(self, item):
        return item.author.username
    
    def item_pubdate(self, item):
        return item.created_at
    
    def item_link(self, item):
        return reverse('blog:post_detail', args=[item.id])