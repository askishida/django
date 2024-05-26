from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout,forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

#class LoginForm(forms.Form) :
#  def __init__(self, *args, **kwargs):

class LoginForm(forms.AuthenticationForm):

    #class Meta:
      #model = models.Members
      #fields = ['title','body','slug','thumb']
      #fields = ['userid','username']

  def __init__(self, *args, **kwargs):
     super().__init__(*args, **kwargs)
     self.helper = FormHelper(self)
     self.helper.layout.append(Submit('submit','Submit'))

class SignupForm(forms.UserCreationForm):

    #class Meta:
      #model = models.Members
      #fields = ['title','body','slug','thumb']
      #fields = ['userid','username']

  def __init__(self, *args, **kwargs):
     super().__init__(*args, **kwargs)
     self.helper = FormHelper(self)
     self.helper.layout.append(Submit('submit','Submit'))





def signup_view(request):
  if request.method == 'POST':
     form = SignupForm(request.POST)
     if form.is_valid():
        user = form.save()

        login(request, user)
        return redirect('posts:list')
  else:
#ブランク　インスタンス
     form = UserCreationForm()
  return render(request, 'members/signup.html', {'form':form })

def login_view(request):
  #def __init__(self, *args, **kwargs):
  #   super().__init__(*args, **kwargs)
  #   self.helper = FormHelper(self)
  #   self.helper.layout.append(Submit('submit','Submit'))
  if request.method == 'POST':
     form = LoginForm(data=request.POST)
     if form.is_valid():
	
      # log in the user
        user = form.get_user()
        login(request, user)
        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        else:
            return redirect('posts:post')
        
        #return redirect('posts:list')
        #この場合は社内掲示板か会員掲示板かも。
        #投稿者の名前の表記も欲しいかも？
        #Blogの場合は記事作成画面に飛ぶのが適切かも？
  else:
     form = AuthenticationForm()
  return render(request, 'members/login.html', {'form':form })


def logout_view(request):
  if request.method == 'POST':
     logout(request)
     return redirect('posts:list')






# Create your views here.
