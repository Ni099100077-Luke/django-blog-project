from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post, Category, Tag, ActivityLog, Comment
from .forms import CommentForm

def post_list(request):
    """显示已发布的文章列表"""
    # 只显示已发布的文章
    posts_list = Post.objects.filter(status='published')
    
    # 分页处理
    paginator = Paginator(posts_list, 10)  # 每页显示10篇文章
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    # 获取所有分类和标签用于侧边栏
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'categories': categories,
        'tags': tags
    })

def post_detail(request, post_id):
    """显示文章详情"""
    post = get_object_or_404(Post, id=post_id)
    
    # 权限控制：只有已发布的文章才能被普通用户查看
    if post.status != 'published' and not request.user.is_staff:
        raise Http404("文章不存在或未发布")
    
    # 检查是否为最后一篇已发布的文章
    # 获取所有已发布文章的最大ID
    max_published_id = Post.objects.filter(status='published').aggregate(
        max_id=models.Max('id')
    )['max_id']
    
    # 判断当前文章是否为最后一篇
    is_last_post = post.id == max_published_id if max_published_id else False
    
    # 增加浏览次数
    post.increment_view_count()
    
    # 获取文章评论
    comments = post.comments.filter(is_active=True).order_by('-created_at')
    
    # 处理评论提交
    comment_form = CommentForm()
    if request.method == 'POST' and 'comment' in request.POST:
        if not request.user.is_authenticated:
            messages.error(request, '请先登录后再发表评论')
            return redirect('login')
        
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, '评论发表成功！')
            return redirect('blog:post_detail', post_id=post.id)
    
    # 获取所有分类和标签用于侧边栏
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'is_last_post': is_last_post,
        'comments': comments,
        'comment_form': comment_form,
        'categories': categories,
        'tags': tags
    })

def draft_list(request):
    """显示草稿列表（仅管理员可见）"""
    if not request.user.is_staff:
        raise Http404("权限不足")
    
    drafts = Post.objects.filter(status='draft')
    return render(request, 'blog/draft_list.html', {'drafts': drafts})

def publish_post(request, post_id):
    """发布文章"""
    if not request.user.is_staff:
        raise Http404("权限不足")
    
    post = get_object_or_404(Post, id=post_id)
    
    # 状态转换：草稿 → 已发布
    if post.publish():
        return render(request, 'blog/publish_success.html', {'post': post})
    else:
        return render(request, 'blog/error.html', {'message': '只能发布草稿状态的文章'})

def archive_post(request, post_id):
    """归档文章"""
    if not request.user.is_staff:
        raise Http404("权限不足")
    
    post = get_object_or_404(Post, id=post_id)
    
    # 状态转换：已发布 → 已归档
    if post.archive():
        return render(request, 'blog/archive_success.html', {'post': post})
    else:
        return render(request, 'blog/error.html', {'message': '只能归档已发布状态的文章'})

def search_posts(request):
    """搜索文章"""
    query = request.GET.get('q', '').strip()
    posts_list = Post.objects.none()  # 使用空的QuerySet而不是空列表
    
    if query:
        from django.db.models import Q, Case, When, Value, IntegerField
        
        # 使用Q对象进行更智能的搜索
        # 标题匹配权重更高，内容匹配权重较低
        posts_list = Post.objects.filter(
            status='published'
        ).filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).annotate(
            search_rank=Case(
                When(title__icontains=query, then=Value(2)),  # 标题匹配权重为2
                When(content__icontains=query, then=Value(1)),  # 内容匹配权重为1
                default=Value(0),
                output_field=IntegerField()
            )
        ).order_by('-search_rank', '-created_at')  # 先按匹配权重排序，再按时间排序
    
    # 分页处理
    paginator = Paginator(posts_list, 10)  # 每页显示10篇文章
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    # 获取所有分类和标签用于侧边栏
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    return render(request, 'blog/search_results.html', {
        'posts': posts,
        'query': query,
        'results_count': posts_list.count(),
        'categories': categories,
        'tags': tags
    })

def category_posts(request, slug):
    """显示特定分类下的文章"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(status='published', category=category)
    
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    return render(request, 'blog/category_posts.html', {
        'category': category,
        'posts': posts,
        'categories': categories,
        'tags': tags
    })

def tag_posts(request, slug):
    """显示特定标签下的文章"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(status='published', tags=tag)
    
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    return render(request, 'blog/tag_posts.html', {
        'tag': tag,
        'posts': posts,
        'categories': categories,
        'tags': tags
    })


def activity_log(request):
    """显示活动日志页面"""
    # 获取最近的50条活动记录
    logs = ActivityLog.objects.all()[:50]
    
    # 获取侧边栏数据
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    return render(request, 'blog/activity_log.html', {
        'logs': logs,
        'categories': categories,
        'tags': tags
    })