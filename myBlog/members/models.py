from django.db import models  # お決まり


class Members(models.Model):  # 頭文字は大文字
    """メンバーの一覧"""

    #  性別を選択する選択肢を宣言
   # GENDER_CHOICES = (
   #     (1, '男性'),
   #     (2, '女性'),
   #     (3, 'その他'),
   # )

    # フィールドを定義します
    # verbose_name：人間に表示する名前を決める、adminサイトとかで使う
    name = models.CharField(max_length=255, verbose_name='Name or お名前')  # max_lengthは長さの最大値
    # choicesにタプルを指定することで選択肢のエリアにできる、
    # blankやnullをOKにするかどうか
    #gender = models.IntegerField(verbose_name='URL', choices=GENDER_CHOICES, blank=True, null=True)
    email = models.DateField(verbose_name='email', blank=True, null=True)
    url = models.DateField(verbose_name='URL', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)  # レコードが追加された時にその時間を保存します
    updated_at = models.DateTimeField(auto_now=True)  # レコードが更新されたタイミングで現在時間が保存されます。

    def __str__(self):  # クラスを呼び出したときに何が帰るか？(基本何でも良いです)
        return self.name






# Create your models here.
