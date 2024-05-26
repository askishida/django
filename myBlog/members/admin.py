from django.contrib import admin
from members.models import Members  # Seiyuuクラスをimportする
# Register your models here.


class MembersAdmin(admin.ModelAdmin):  # 声優アドミンのクラスを宣言
    pass

admin.site.register(Members, MembersAdmin)  # 決まった書き方
# Register your models here.
