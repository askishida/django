from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from posts.models import Article,Category,ParentCategory
from posts import forms
from taggit.models import Tag
from django.db.models import Count
from django.views.generic import ListView


def home(request,tag_slug=None,category_slug=None):
  # return HttpResponse('home.html')
   posts2 = Article.published.all().order_by('-date').first()
   posts = Article.published.all().order_by('-date')[:5]
   pop_posts =Article.published.all().order_by('visitors').reverse()[:5];
   #return render(request, 'home.html', {'posts','posts2':posts})
   posts3 = Article.published.all().order_by('date').reverse();
   posts4 = Article.published.all().order_by('date').reverse();
   # df_posts3 =read_frame(posts3)
   tag = None
   if tag_slug:
      tag = get_object_or_404(Tag, slug=tag_slug)
      posts3 = posts3.filter(tags__in=[tag])
     # tags = posts3.tags.all()
   tags3=[]
   for article in posts3:
      tags3 += article.tags.all()

   category = None
   if category_slug:
      category = get_object_or_404(Category, slug=category_slug)

     #posts3 = posts3.filter(categories__in=[category]) 
      posts4 = posts4.filter(category__in=[category])
   categories3=[]
   for article in posts4:
      categories3 += [article.category]

   result = sorted({i: tags3.count(i) for i in set(tags3)}.items(), key=lambda x: x[1], reverse=True)
   result2 = sorted({i: categories3.count(i) for i in set(categories3)}.items(), key=lambda x: x[1], reverse=True)


   return render(request, 'home.html', {'posts':posts,'posts4':posts4,'pop_posts':pop_posts,'result':result,'result2':result2})




def about(request):
  # return HttpResponse('about.html')
   return render(request, 'about.html')

