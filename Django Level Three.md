##### MTV--Django
- https://blog.csdn.net/dbanote/article/details/11338953
- M 代表模型（Model）：负责业务对象和数据库的关系映射(ORM)
- T 代表模板 (Template)：负责如何把页面展示给用户(html)
- V 代表视图（View）：负责业务逻辑，并在适当时候调用Model和Template
- 除了以上三层之外，还需要一个URL分发器，它的作用是将一个个URL的页面请求分发给不同的View处理，View再调用相应的Model和Template
1. Web服务器（中间件）收到一个http请求
2. Django在URLconf里查找对应的视图(View)函数来处理http请求
3. 视图函数调用相应的数据模型来存取数据、调用相应的模板向用户展示页面
4. 视图函数处理结束后返回一个http的响应给Web服务器
5. Web服务器将响应发送给客户端

##### Django forms
0. Preperation
- create project and app
- create Templates folder and appName folder inside it
- index.html and form.html in the appName folder
- registry the Templates in the settings.py:

```
#set up path first
TEMPLATE_DIR = os.path.join(BASE_DIR,"templates")
#add app name in the app list
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'basicapp'
]
#add TEMPLATE_DIR into template list
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
1. Create forms.py inside the app

2. Call build in formss classes inside the forms.py, just like how we build the models

```
from django import forms
class FormName(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    text = forms.CharField(widget=forms.Textarea)
    # This would specify a form with a comment that
    # uses a larger Textarea widget,
    # rather than the default TextInput widget.

```
3. Import the forms into view.py

```
from django.shortcuts import render
from . import forms
```

4. Create a new view for the form

```
# Create your views here.
def index(request):
    return render(request,'basicapp/index.html')

def form_name_view(request):
    form = forms.FormName()# forms.className()
    return render(request,'basic/form.html',{'form':form})
    # {}is the content to pass in
```

5. Add the view to the app's urls in the urls.py in the basicforms folder:

```
from django.conf.urls import url
from django.contrib import admin
from basicapp import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index,name='index'),
    url(r'^formpage/',views.form_name_view,name='form_name')
]
```

6. Insert forms into the form template and styling

```
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>Forms</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
  </head>
  <body>
    <div class="container">
      <h1>Fill the form</h1>
      <form method="post">
        {{form.as_p}}
        <input type="submit" class="btn btn-primary" value="submit">
        {% csrf_token %}
      </form>
    </div>
  </body>
</html>
```
- `{{form.as_p}}` put the form in <p> tag
- `{% csrf_token %}` necessary

7. How to deal with the user post:
- in views.py:

```
def form_name_view(request):
    form = forms.FormName()# forms.className()
    if request.method == 'POST': # if user post somthing
        form = forms.FormName(request.POST)
        if form.is_valid():
            # do something
            print("validation success")
            print("name: "+form.cleaned_data['name'])#print data of name in the console
    return render(request,'basicapp/form.html',{'form':form})
    # {}is the content to pass in
```
##### Form validation
- mainly in the forms.py

```
from django import forms
from django.core import validators

# custom validator, def before class
def check_for_z(value):
    if value[0].lower() != 'z':
        raise forms.ValidationError("needs to start with z")
class FormName(forms.Form):
    name = forms.CharField(validators=[check_for_z])#use the validator
    email = forms.EmailField()
    verify_email = forms.EmailField(label="enter email again")
    text = forms.CharField(widget=forms.Textarea)
    # This would specify a form with a comment that
    # uses a larger Textarea widget,
    # rather than the default TextInput widget.
    botcatcher = forms.CharField(required=False,widget=forms.HiddenInput,validators=[validators.MaxLengthValidator(0)])
# field in not required and is HiddenInput
# "robot" visitor will fill in this HiddenInput, but real user won't
#  MaxLengthValidator(max_length, message=None) is the build in validator
# if length of value>max_length, raise  validation error
# i.e. robot will fill sth in botcatcher, once botcatcher length > 0, nothing will be posted
# an error will also shown on the page

    # clean the entire form
    def clean(self):
        all_clean_data = super().clean()
# The call to super().clean() in the example code ensures that
# any validation logic in parent classes is maintained

# Cleaning and validating fields that depend on each other
# get email and verify_email contents, compare them
        email = all_clean_data['email']
        vmail = all_clean_data['verify_email']
        if email != vmail:
            raise forms.ValidationError("Make sure emails match")

```
