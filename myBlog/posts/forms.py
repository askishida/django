from django import forms
#from django.forms import ModelForm
from .import models 
#from .models import Post
from froala_editor.widgets import FroalaEditor
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class CreateArticle(forms.ModelForm):

    class Meta:
      model = models.Article
      #fields = ['title','body','slug','thumb']
      fields = ['title','category','description','slug','thumb']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('submit','Submit'))

class PageForm(forms.ModelForm):
    content = forms.CharField(widget=FroalaEditor)


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)
