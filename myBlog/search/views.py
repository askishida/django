from django.core.paginator import Paginator
from django.shortcuts import render

from posts.models import Article
from taggit.models import Tag

# Create your views here.


def search(request,tag_slug=None):

   pop_posts =Article.objects.all().order_by('visitors').reverse()[:5];

   posts3 = Article.objects.all().order_by('date').reverse();
   # df_posts3 =read_frame(posts3)
   tag = None
   if tag_slug:
       tag = get_object_or_404(Tag, slug=tag_slug)
       posts3 = posts3.filter(tags__in=[tag])
      # tags = posts3.tags.all()
   tags3=[]
   for article in posts3:
       tags3 += article.tags.all()

  

   result = sorted({i: tags3.count(i) for i in set(tags3)}.items(), key=lambda x: x[1], reverse=True)


   q = request.GET.get('q', None)
   posts = ''
    
   if q is None or q is "":
       posts = Article.objects.all()
   elif q is not None:
       posts = Article.objects.filter(title__contains=q)

   paginator = Paginator(posts, 3)
   page = request.GET.get('page')
   posts = paginator.get_page(page)
       


   title = "Search"
   return render(request, 'search/search.html', {'posts': posts, 'title':title,'pop_posts':pop_posts,'result':result})




