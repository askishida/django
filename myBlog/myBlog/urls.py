"""myBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url, include
from posts import views as posts_views
from django.contrib.sitemaps.views import sitemap

from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from .sitemaps import ArticleSitemap


sitemaps = {
    'posts': ArticleSitemap,
}



urlpatterns = [
    #path(r'^admin/', admin.site.urls),
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^froala_editor/', include('froala_editor.urls')), 
    path('locationmap/', include('locationmap.urls')),
    path('api/', include('todos.urls')),
    re_path(r'^members/', include('members.urls')),
    path('', views.home,name='home'),
    path('posts/', include('posts.urls')),
    path('hello/', include('helloworld.urls')),
    #path(r'^$',posts.views.home,name='home'),
    #path(r'^$', views.home),
   # path('post2/<int:id>/', posts_views.post2, name='post2'),
    #re_path(r'post2/(?P<int:id>.*)$', posts_views.post2, name='post2'),


    path('feedreader/', include('feedreader.urls')),
    path('search/', include('search.urls')),
    #path('add/post',posts_views.post,name='post'),

    #path('add/post',posts_views.post,name='post'),
    #path('add/post',posts_views.add_post,name='add_post'),
   # path('edit/post/<int:post_id>/',posts_views.edit_post,name='edit_post'),
    #path(r'^about/$', views.about),
  
    path('about/', views.about,name='about'),
    path('contact/', include('contact.urls')),
   # path('sidebar/', include('sidebar.urls')),
    #path('posts/', include('posts.urls')),
  
]




urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
