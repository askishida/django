from django.contrib import admin
from members.models import Members  
# Register your models here.


class MembersAdmin(admin.ModelAdmin): 
    pass

admin.site.register(Members, MembersAdmin)  # 決まった書き方
# Register your models here.
