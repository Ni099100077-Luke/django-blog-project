from django.urls import path
from django.contrib.syndication.views import Feed
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('search/', views.search_posts, name='search_posts'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('drafts/', views.draft_list, name='draft_list'),
    path('<int:post_id>/publish/', views.publish_post, name='publish_post'),
    path('<int:post_id>/archive/', views.archive_post, name='archive_post'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('tag/<slug:slug>/', views.tag_posts, name='tag_posts'),
    path('activity-log/', views.activity_log, name='activity_log'),
    path('rss/', LatestPostsFeed(), name='rss_feed'),
]