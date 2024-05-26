#coding:utf-8
from django.shortcuts import render, redirect,render_to_response, get_object_or_404
from .models import Article,Category,ParentCategory
from django.http import HttpResponse
from . import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from taggit.models import Tag
from django.db.models import Count
from .forms import EmailPostForm 
from django.utils import timezone
import datetime
from datetime import date
import locale
from dateutil.relativedelta import relativedelta
#from django_pandas.io import read_frame

#from django.template.context_processors import csrf
from django.views.generic import ListView
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd

# Create your views here.
class ArticleListView(ListView):
  model = Article
  query_set = Article.published.all()
  context_object_name = 'posts'
  paginate_by = 3
  template_name = 'posts/article_list.html'

def share(request, slug):
  post = get_object_or_404(Article, slug=slug, status='published')
  sent = False
  if request.method == 'POST':
      form = EmailPostForm(request.POST)
      if form.is_valid():
          cd = form.cleaned_data
          post_url = request.build_absolute_uri(
                                        post.get_absolute_url())
          subject = '{}  ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
          message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
          send_mail(subject, message, 'totinoki@mqb.biglobe.ne.jp',[cd['to']])
          sent = True
  else:
      form = EmailPostForm()
  return render(request, 'posts/share.html', {'post': post,'form': form,'sent':sent})   
#pagenation


def article_list5(request):
  posts = Article.published.all().order_by('publish').reverse()[:5];
  pop_posts =Article.published.all().order_by('visitors').reverse()[:5];
  return render(request, 'posts/article_list5.html', {'posts':posts,'pop_posts':pop_posts})
def article_list(request, year=None, month=None,day=None,tag_slug=None, category_slug=None):  
  #pop_posts =Article.objects.all().order_by('visitors').reverse()[:5];
  pop_posts =Article.published.all().order_by('visitors').reverse()[:5];
  #posts2 = Article.objects.all().order_by('date').reverse();
  posts2 = Article.published.all().order_by('publish').reverse();
  #posts3 = Article.objects.all().order_by('date').reverse();
  posts3 = Article.published.all().order_by('publish').reverse();
  # df_posts2 =read_frame(posts2)
 
  posts4 = Article.published.all().order_by('publish').reverse();
  #件数を調べる方法は？
  df_c = Article.published.count();
  df = pd.DataFrame(np.random.random([df_c, 3]), columns=['foo', 'bar', 'baz'])
  post_df = pd.DataFrame(index=df.index, columns=[])
  titles=[]
  publishs=[]
  snippets=[]
  categorys=[]
  p_categorys=[]
  dftags=[]
  for p4 in posts4:
      titles    += [p4.title]
      snippets  += [p4.snippet]
      publishs  += [p4.publish.strftime("%Y-%m-%d %H:%M:%S")]
      categorys += [p4.category]
      p_categorys += [p4.category.parent]
      #dftags += [p4.tags]
  post_df['title'] = titles
  post_df['snippet'] = snippets
  post_df['publish'] = publishs
  post_df['category'] = categorys
  post_df['p_category'] = p_categorys
  #post_df['tags'] = dftags
  post_df = post_df.query('"2018-10-01"<= publish < "2018-11-01"') 

  #tag = None
  #if tag_slug:
      #tag = get_object_or_404(Tag, slug=tag_slug)
      #posts2 = posts2.filter(tags__in=[tag])
     # tags = posts2.tags.all()
  #tags3=[]
  #for article in posts2:  
      #tags3 += article.tags.all()
  #category = None
  #if category_slug:
     #catn = get_object_or_404(Category, slug=category_slug)
     #postsに統一すること！！！ 
     #posts3 = posts3.filter(categories__in=[category]) 
     #posts = posts3.filter(category__in=[catn]) 
  #categories3=[]
  #categories_family=[]
  #for article in posts3:
  #   categories3 += [article.category]
  #   categories_family += [article.category.parent]  
  #result = sorted({i: tags3.count(i) for i in set(tags3)}.items(), key=lambda x: x[1], reverse=True)

  #result2 = sorted({i: categories3.count(i) for i in set(categories3)}.items(), key=lambda x: x[1], reverse=True)
  #result_f = sorted({i: categories_family.count(i) for i in set(categories_family)}.items(), key=lambda x: x[1], reverse=True)

  year2=[]
  for article in posts4:
     year2 += [article.publish.year]
  month2=[]
  for article in posts4:
     month2 += [(article.publish.year,article.publish.month)]

  day2=[]
  for article in posts4:
     day2 += [(article.publish.year,article.publish.month,article.publish.day)]

  # 時間情報に関するロケール設定を変更する
  locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
  day2_1=[]
  for article in posts4:
     day2_1 += [(article.publish.year,article.publish.month,article.publish.day,date(article.publish.year,article.publish.month,article.publish.day).strftime('%a'))]


 
  result_y = sorted({i: year2.count(i) for i in set(year2)}.items(), key=lambda x: x[0], reverse=True)
  result_m = sorted({i: month2.count(i) for i in set(month2)}.items(), key=lambda x: x[0][1], reverse=True) 
  result_d = sorted({i: day2.count(i) for i in set(day2)}.items(), key=lambda x: x[0][2], reverse=True)
  result_d1 = sorted({i: day2_1.count(i) for i in set(day2_1)}.items(), key=lambda x: x[0][2], reverse=True)
  #ここからは共通事項？
  categories3=[]
  categories_family=[]
  for article in posts3:
      categories3 += [article.category]
      categories_family += [article.category.parent]


  result2 = sorted({i: categories3.count(i) for i in set(categories3)}.items(), key=lambda x: x[1], reverse=True)
  result_f = sorted({i: categories_family.count(i) for i in set(categories_family)}.items(), key=lambda x: x[1], reverse=True)



  tags3=[]
  for article in posts2:
      tags3 += article.tags.all()
  result = sorted({i: tags3.count(i) for i in set(tags3)}.items(), key=lambda x: x[1], reverse=True)

  #if year and month and day:
     #posts = get_object_or_404(Article, status='published',
      #                                  publish__year=year,
      #                                  publish__month=month,
      #                                  publish__day=day).order_by('date').reverse();
  #   posts=Article.published.filter(publish__year=year,publish__month=month,publish__day=day).order_by('date').reverse();
  #elif year and month:
     #posts = get_object_or_404(Article, status='published',
     #                                   publish__year=year,
     #                                   publish__month=month)
     #posts = posts.order_by('date').reverse()
   #  posts=Article.published.filter(publish__year=year,publish__month=month).order_by('date').reverse();
  


  if year:
     #ここからは共通事項？
     #categories3=[]
     #categories_family=[]
     #for article in posts3:
     #   categories3 += [article.category]
     #   categories_family += [article.category.parent]


     #result2 = sorted({i: categories3.count(i) for i in set(categories3)}.items(), key=lambda x: x[1], reverse=True)
     #result_f = sorted({i: categories_family.count(i) for i in set(categories_family)}.items(), key=lambda x: x[1], reverse=True)



     #tags3=[]
     #for article in posts2:
     #   tags3 += article.tags.all()
     #result = sorted({i: tags3.count(i) for i in set(tags3)}.items(), key=lambda x: x[1], reverse=True)
    #以下１行追加。
     #result=[]
     #result2=[]
     #result_f=[]
    # posts = get_object_or_404.order_by('date')(Article, status='published',
      #                                  publish__year=year)
    
     if month:
#        posts=Article.published.filter(publish__year=year & publish__month=month).order_by('published').reverse();
       
        if day:
         
           #動かない。
           #posts=Article.published.filter(publish__year=year,publish__month=month,publish__day=day).order_by('publish').reverse();
           ymd = datetime.datetime(int(year),int(month),int(day))
           ymd_n = ymd + relativedelta(days=1) 
           posts = Article.published.filter(publish__range=(ymd, ymd_n)).order_by('publish').reverse()
        else:
           #動かない。
           #posts=Article.published.filter(publish__gt=add_months('year-month',-1),publish__lte='year-month').order_by('publish').reverse();
           ym = datetime.datetime(int(year),int(month),1)
           ym_n = ym + relativedelta(months=1)

           posts = Article.published.filter(publish__range=(ym, ym_n)).order_by('publish').reverse()
     else:
        posts=Article.published.filter(publish__year=year).order_by('publish').reverse()
  else:
     category = None
     if category_slug:
        catn = get_object_or_404(Category, slug=category_slug)
        #postsに統一すること！！！ 
        #posts3 = posts3.filter(categories__in=[category]) 
        posts = posts3.filter(category__in=[catn])
        #categories3=[]
        #categories_family=[]
        #for article in posts3:
        #   categories3 += [article.category]
        #   categories_family += [article.category.parent]
 

        #result2 = sorted({i: categories3.count(i) for i in set(categories3)}.items(), key=lambda x: x[1], reverse=True)
        #result_f = sorted({i: categories_family.count(i) for i in set(categories_family)}.items(), key=lambda x: x[1], reverse=True)






     else:
        tag = None
        if tag_slug:

           tag = get_object_or_404(Tag, slug=tag_slug)
           posts = posts2.filter(tags__in=[tag])
           # tags = posts2.tags.all()
           #tags3=[]
           #for article in posts2:
              #tags3 += article.tags.all()
           #result = sorted({i: tags3.count(i) for i in set(tags3)}.items(), key=lambda x: x[1], reverse=True)



        else:
           posts = Article.published.all().order_by('publish').reverse()

     #categories3=[]
     #categories_family=[]
     #for article in posts3:
     #   categories3 += [article.category]
     #   categories_family += [article.category.parent]


     #result2 = sorted({i: categories3.count(i) for i in set(categories3)}.items(), key=lambda x: x[1], reverse=True)
     #result_f = sorted({i: categories_family.count(i) for i in set(categories_family)}.items(), key=lambda x: x[1], reverse=True)



     #tags3=[]
     #for article in posts2:
     #   tags3 += article.tags.all()
     #result = sorted({i: tags3.count(i) for i in set(tags3)}.items(), key=lambda x: x[1], reverse=True)




  paginator = Paginator(posts,3)
  page = request.GET.get('page')

  try:
      posts = paginator.get_page(page)
  except PageNotAnInteger:
      posts = paginator.get_page(1)
  except EmptyPage:
      posts = paginator.page(paginator.num_pages)      


  return render(request, 'posts/article_list.html', {'posts':posts,'posts2':posts2,'page':page,'pop_posts':pop_posts,'result':result,'result2':result2,"result_f":result_f,'result_y':result_y,'result_m':result_m,'result_d':result_d,'result_d1':result_d1,'post_df':post_df}) 

#def post2(request, post2_id=id):
#  item = get_object_or_404(Article, id=post2_id)
#  return render(request, 'posts/post2.html', {'item': item})


 # return render(request, 'posts:list', {'posts':posts}) 

#def search(request):
#   template = 'posts/article_list.html'
#   query = request.GET.get('q')
#   if query:
#      results = Post.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))  
#
#   else:
#        
#      results = Post.objects.filter(status='published')
#   pages = article_list(request, results, num=1)
#
#   context = {
#            'items': pages[0],
#            'page_range': pages[1],
#            'query': query,
#    }
#
#   return render(request, template, context)




def article_detail(request, slug,tag_slug=None):


  

  #article = get_object_or_404(Article,status='published',
  #                                    slug=slug,
  #                                    publish__year = year,
  #                                    publish__month = month,                 
  #                                    publish__day = day)
  #article = Article.objects.get(slug=slug)
  article = get_object_or_404(Article, slug=slug,
                                       status='published')
  
  #article = get_object_or_404(Article, slug=slug)


  article.visitors += 1
  article.save()

 # article = article.filter(publish__year=year,publish__month=month,publish__day=day,slug=slug)
 
  posts = Article.published.all().order_by('date').reverse()[:5];
  pop_posts =Article.published.all().order_by('visitors').reverse()[:5];
  post_tags_ids = Article.tags.values_list('id', flat=True)
  similar_posts = Article.published.filter(tags__in=post_tags_ids).exclude(id=article.id)
  similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-date')[:4]

  #posts2 = Article.objects.all().order_by('date').reverse();
  # df_posts2 =read_frame(posts2)
  #tag = None
  #if tag_slug:
  #    tag = get_object_or_404(Tag, slug=tag_slug)
  #    posts2 = posts2.filter(tags__in=[tag])
     # tags = posts2.tags.all()
  #tags3=[]
  #for article in posts2:
  #    tags3 += article.tags.all()
#
  #result=article_list.result

  #result = sorted({i: tags3.count(i) for i in set(tags3)}.items(), key=lambda x: x[1], reverse=True)


  soup = BeautifulSoup(article.description, "html.parser")
  soup_h1 = soup.find_all("h1") 
  soup_h2 = soup.find_all("h2")
  soup_h2_1 = soup.find_all("h2")
  

  # sub_des = []
  sub_title = []
  for ht in soup_h2:
     sub_title += [ht.text]
     #sub_des += ht.next_siblings
  soup_h2 = sub_title
  #sub_des =[]
  #sub_desm = []

  #for ht in soup_h2_1:
    #while (not ht.next_sibling in soup_h2_1):
        #nameでタグ名前を取得するがht.next_sibling.nameが意味なさない
        #ここをループさせたい。
     #while True: 
   #     sub_desm += ht.next_sibling + ht.next_sibling.next_sibling
        #ht = ht.next_sibling 
       # if ht.name =="h2":
       #    break 

        #sub_desm += ht.next_sibling
        #ht = ht.next_sibling
        #sub_desm += ht.next_sibling
  #sub_des = sub_desm
        

  #for item1, item2 in zip(sub_title, sub_desm):
  #   sub_des += [item1,item2]
  return render(request, 'posts/article_detail.html', {'article':article,'posts':posts,'pop_posts':pop_posts,'similar_posts':similar_posts,'soup_h2':soup_h2})




@login_required(login_url="/members/login/")
def post(request):
  if request.method == 'POST':  
    #Postオブジェクトを取得
    
      form = forms.CreateArticle(request.POST, request.FILES)
    #home.htmlにはディクショナリ形式の引数を与えることでデータを渡すことができる！
      if form.is_valid():
         # save article to db
         instance = form.save(commit=False)
         instance.author = request.user
         instance.save()
         return redirect('posts:list')
  else:
      form = forms.CreateArticle()
  return render(request, 'posts/post.html',{'form':form})









#def contact(request):

    #Postオブジェクトを取得
#    posts =  Post.objects.order_by('pub_date')

    #home.htmlにはディクショナリ形式の引数を与えることでデータを渡すことができる！
    #return render(request, 'posts/contact.html',{'posts':posts})
#    return render(request, 'posts/contact.html',{'posts':posts})
'''
    ・GETで送信（初めてページを表示）された場合にはelse内で空のフォームインスタンスを作成。
      contextにフォームインスタンスをセットしテンプレートにてレンダリング。

    ・POSTで送信された場合には入力されたデータがくくりつけられたフォームインスタンスを作成。
      is_valid()でフォームの検証。問題がなければフォームに入力されたcharactフィールドの内容を取
      得し、test_indexに値を持って移動。未入力等で問題が検出された場合はテンプレートに戻って再
      表示される。
'''







# Create your views here.
