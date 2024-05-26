from django.contrib.sitemaps import Sitemap
from posts.models import Article

class ArticleSitemap(Sitemap):
    def posts(self):
        return Article.objects.all()
