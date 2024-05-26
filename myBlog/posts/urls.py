from .import views


from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path,reverse
from django.conf.urls import url, include
#from posts import views as posts_views
from django.views.generic import ListView

from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from .views import (
    article_detail, 
    article_list
)
from django.utils import timezone

app_name = 'posts'
urlpatterns = [
   re_path('^post/$', views.post, name='post'),
   re_path('^$', views.article_list, name='list'),
   #path('', views.ArticleListView.as_view(), name='list'),
   #path('<int:year>/', views.article_list, name='article_list_by_year'),
   re_path(r'^(?P<year>[0-9]{4})/$', views.article_list, name='article_list_by_year'),
   re_path(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.article_list, name='article_list_by_month'),
   #re_path('(?P<year>([12][0-9]{3}))/(?<month>(0[0-9]|1[0-2]))/(?<day>([0-2][0-9]|3[01]))/$', views.article_list, name='article_list_by_day'),
   re_path(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/$', views.article_list, name='article_list_by_day'),
   #path('<slug:slug>/share/',views.share, name='share'),
   path('<slug:slug>/share/',views.share, name='share'),
   path('<slug:slug>/', views.article_detail, name='detail'),  
   #path('<slug:slug>/share/',views.share, name='share'),
   #re_path(r'^(?P<slug>[\w-]+)/$', views.article_detail, name='detail'),
   #path('<slug:slug>/', views.article_detail, name='detail'),
   path('category/<slug:category_slug>', views.article_list, name='article_list_by_category'),
   path('tag/<slug:tag_slug>', views.article_list, name='article_list_by_tag'),
  
  # re_path(r'^tag/(?P<slug:tag_slug>[\w-]+)/$', views.article_list, name='article_list_by_tag'),
  # path('<int:id>', views.post2, name='post2'),

   #path('contact/', views.contact, name='contact'),
  # re_path(r'^results/$', search, name="search"),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
