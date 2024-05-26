#from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from froala_editor.fields import FroalaField
from django.utils.text import slugify
import re
#from django.urls import reverse
from django.utils import dateformat


from django_pandas.managers import DataFrameManager
from taggit.managers import TaggableManager
from django.utils import timezone 


class Page(models.Model):
    content = FroalaField()

class ParentCategory(models.Model):
    name = models.CharField('親カテゴリ名', max_length=255)
 
    def __str__(self):
        return self.name

 
#category 
class Category(models.Model):
    name = models.CharField('カテゴリ名', max_length=255)
    slug = models.SlugField(max_length=250, unique=True)
    parent = models.ForeignKey(ParentCategory, verbose_name='親カテゴリ', on_delete=models.PROTECT)    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
   
    def __str__(self):
        return self.name

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset().filter(status='published')     


#article
class Article(models.Model):
    '''
    記事の内容を管理するクラスと思われる。  

    modelの定義はここに詳しく書いてある。
    https://docs.djangoproject.com/ja/1.11/ref/models/fields/
    '''
    #タイトル
    STATUS_CHOICES = (
        ('draft','下書き'),
        ('published','公開する'),
    )
    title = models.CharField(max_length=100, default='')
    category = models.ForeignKey(Category, verbose_name='カテゴリ', on_delete=models.PROTECT)
    slug = models.SlugField(max_length=250,unique=True,unique_for_date='publish')
    #body = models.TextField()
    #description = RichTextField(blank=True, null=True)    


    
    description = RichTextUploadingField(blank=True, null=True, external_plugin_resources=[(
                                                                     'youtube',
                                                                     '/static/posts/vendor/ckeditor_plugins/youtube/youtube/',
                                                                     'plugin.js',
                                                                 ),
                                                                                           ( 
                                                                     'locationmap',
                                                                     '/static/posts/vendor/ckeditor_plugins/locationmap/',
                                                                     'plugin.js',
                                                                                        
                                                            
                                                                 )],
                                                                 


                                                                )
    tags = TaggableManager()
    objects = models.Manager()
    published = PublishedManager()
    
    
    description2 = RichTextUploadingField(blank=True, null=True, config_name="special",
                                                                 external_plugin_resources=[(
                                                                     'youtube',
                                                                     '/static/posts/vendor/ckeditor_plugins/youtube/youtube/',
                                                                     'plugin.js',
                                                                 )],
                                                                 )

   
    body = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    #year=publish.strftime('%Y')
    #month=models.IntegerField(max_length=2)
    #month=publish.strftime('%m')
    #day=models.IntegerField(max_length=2)
    #day=publish.strftime('%d')
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft',
                              )
    thumb = models.ImageField(default='default.png',blank=True)
    author = models.ForeignKey(User, default=None,on_delete=models.CASCADE,related_name='posts')
    visitors = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
      #return '%s' % self.title
      #self.slug = slugify(self.title)
      return self.title 

    def save(self):
      #self.slug = slugify(self.title)
      super(Article, self).save()
    def snippet(self):
      p1=re.compile(r"<[^>]*?>")
      p2=re.compile(r"/^\xC2\xA0/")
      d1=p1.sub("", self.description)
      d2=d1.replace("&nbsp;","")
     # return self.body[:50]+'...'
      #return self.description[:50]+'...'
      return d2[:50]+'...'

#ここは消してはいけない。前提ファイル。
# Create your models here.

    '''
    def year(self):
    #year=publish.strftime('%Y')
    #month=models.IntegerField(max_length=2)
    #month=publish.strftime('%m')
    #day=models.IntegerField(max_length=2)
    #day=publish.strftime('%d')
      y=publish.strftime('%Y')
      return y
    def month(self):
      m=publish.strftime('%m')
      return m
    def day(self):
      d=publish.strftime('%d')
      return d
    '''
    def get_absolute_url(self):
      from django.urls import reverse 
    # return reverse('post2', args=[str(self.id)])
      url = reverse('posts:detail', 
                     #args=[self.publish.year,
                      #     self.publish.month,
                      #     self.publish.day,
                          args = [str(self.slug)]
                           )              
      url1 = reverse('posts:detail',
                     args=[
                           self.slug
                           ])



      url2 = reverse('posts:detail',
                     kwargs={"year":self.publish.year,
                             "month":self.publish.month,
                             "day":self.publish.day,
                             "slug":self.slug})



     # url3 = "/posts/{0}/{1}/{2}/{3}/"  %(self.publish.year,self.publish.month,self.publish.day,self.slug)
      return url
'''    
class Publish(models.Model):
    #publish = models.DateTimeField(default=timezone.now)
    publish = models.ForeignKey(Article,on_delete=models.PROTECT)
    #year=models.IntegerField(max_length=4)
    year=publish.strftime('%Y')
    #month=models.IntegerField(max_length=2)
    month=publish.strftime('%m')
    #day=models.IntegerField(max_length=2)
    day=publish.strftime('%d')
'''
