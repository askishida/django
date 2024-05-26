from django.contrib import admin
from .models import Article, Category, ParentCategory





admin.site.register(ParentCategory)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug','parent')
    prepopulated_fields = {'slug': ('name','parent')}
    
admin.site.register(Category, CategoryAdmin)





class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    search_fields = ('title','description')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields =('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
admin.site.register(Article, ArticleAdmin)




# Register your models here.
#from .models import Post

#admin管理画面でさわれるようにする。
#admin.site.register(Post)
# Register your models here.
