# Django를 이용한 Web 다루기

- 전체적인 흐름을 공부하고, 세세한 부분은 뒷부분에 기록

## Web Service 구축 순서


### 1. 가상환경 

```bash
# 가상환경 만들기
$ python -m venv venv

# 가상환경 적용
$ source venv/Scripts/activate

# 패키지 다운
$ pip install django

# 패키지 저장
$ pip freeze > requiremenets.txt
```


### 2. 버전 관리
- .gitignore 파일 생성
  
    git으로 관리하지 않을 때의 파일 목록을 작성해서 관리

```bash
# git 파일 생성
$ git init
```


### 3. 프로젝트 생성
   
```bash
# 프로젝트 폴더 생성 
$ django-admin startproject {프로젝트 이름} {프로젝트 위치}

# 서버 실행
$ python manage.py runserver
```


### 4. App생성 및 등록과 설정

- app을 반드시 생성후에 등록 해야 한다. (생성 전에 등록 X)
  
```bash
# app 생성
$ python manage.py startapp {앱 이름}
```

```python
# crud/settings.py

INSTALLED_APPS = [
    ...
    'articles',
    'accounts',
    ...
]
```


### 5. 프로젝트의 urls 관리

- 앱마다 분리해서 관리할 수 있도록 하자

```python
# crud/urls.py

from django.contrib import admin
from django.urls import path, include
# include를 가져와서 앱마다 분리해서 관리하자

urlpatterns = [
    path('admin/', admin.site.urls),
    # 각 app에 앱에 urls파일을 만들어서 관리
    path('articles/', include('articles.urls')),
    path('accounts/', include('accounts.urls')),
]
```


### 6. 모델 정의

- Python 문법만으로도 편하게 Database를 조작하기 위해 model 제공

1. 모델정의

```python
# articles/models.py

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # 작성시간, 수정시간 : 사용자가 직접 입력 X
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# ----------------------------------------------------------
# accounts/models.py

from django.contrib.auth.models import AbstractUser

# django가 제공해주는 user data
class User(AbstractUser):
    # django가 제공해주는 이외의 column이 필요하다면
    # 여기에 정의
    pass


# ----------------------------------------------------------
# settings.py

AUTH_USER_MODEL = 'accounts.User'
# django에서 지원해주는 기본 설정을 만지기 위해 추가 해준다.

```


2. 모델을 정의 했다면 table을 생성하기

```bash
# 적절한 table이 될 수 있도록 각종 데이터 타입들을 설정(설계도 작성)
$ python manage.py makemigrations

# 설계도 기반으로 table 작성
$ python manage.py migrate

```


### 7. 화면 구성을 위한 BASE.HTML 만들기

- 한 서비스 내의 화면 구성을 동일하게 작성하기 위해 만든다.

- 매번 똑같은 코드를 반복하지 않기 위해 사용

- base.html의 위치 (사용 용도에 따라 변경)
    1. articles app의 화면 구성만을 위한 base이면 articles app 폴더에 생성
    2. 모든 app이 공통적으로 사용할 것이면, 최상위 폴더에 생성

```python
# crud/settings.py

# base파일을 찾을 수 있게 settings.py안의 TEMPLATES에 작성
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates'],
        ...
    }
]
```

```html
# templates/base.html

# 모든 template들이 사용할 베이스
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <!-- 각 문서마다 고유한 내용을 입력할 영역 -->
  {% block content %}
  {% endblock content %}
</body>
</html>
```


### 8. 앱에서 urls 관리

```python
# articles/urls.py

# urls를 관리하기 위해 path를 가져온다
from django.urls import path
# view와 urls를 연결
from . import views

# 하드 코딩을 피하기 위해 app_name과 urlpattern을 정의해 준다.
app_name = 'articles'
urlpatterns = [
    path('{위치}/', views.{함수이름}, name='{이름}')
]
```


### 9. views 함수 생성

```python
# articles/views.py

# 페이지를 리턴 해줄 redirect 가져오기
from django.shortcuts import render, redirect
# 사용할 모델을 가져온다
from .models import Article

def main(request):
    # 변수에 설정해놓은 모델 가져오기
    articles = Article.objects.all().order_by('-pk')    
    # order_by 할때
    context = {
        'articles': articles,
    }
    return render(request, 'articles/main.html', context)

```


### 10. views와 연결된 html 작성
```html
<!-- articles/main.html-->

{% extends "base.html" %}

{% block content %}
<h1>Main Page</h1>
{% endblock content %}
```


## 게시글 만들기

### 1. create 만들기

1. urls 경로 만들어주기

``` python
# articles/urls.py

urlpatterns = [
    ...
    path('create/', views.create, name='create'),
]
```

2. forms 만들기

    - 모델을 폼으로 만들어서 가져다 쓴다.

        1. articles/ 에 forms.py 파일 생성

        2. 장고에서 지원하는 폼과 model.py에서 만들어놓은 구조를 가져오자

            ```python
            # articles/forms.py

            from django import forms    # 장고에서 기본적으로 제공하는 폼 형태
            from .models import Article # 모델에서 설정한 값 가져오기

            class ArticleForm(forms.ModelForm):

                class Meta:
                    model = Article
                    fields = ('title', 'content',)          # 가져올 필드만 정할 수 있다.
                    # exclude = ('user', 'like_user',)      # 제외할 필드만 정할 수도 있음
                    # fields = '__all__'                    # 모든 필드 가져오기

            ```

3. views 설정 만들기

```python
# articles/views.py

from .forms import ArticleForm      # forms.py에서 만들어 놓은 형식 가져오기


def create(request):
    # 유저 정보 확인하고 생성
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)   # article 생성은 하지만, db에는 아직 담지 않는다
            article.user = request.user         # user속성에 request.user 정보를 담는다
            article.save()                      # db에 반영
            return redirect('articles:main')    # 작성하면 메인페이지로 돌려보낸다.
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)

```

4. html 만들기

- create.html 생성

```html
<!-- articles/create.html -->

{% extends "base.html" %}   <!-- base 템플릿 상속 받기 -->

{% block content %}
<h1>CREATE PAGE</h1>

<!-- form 작성 -->
<form action="{% url "articles:create" %}" method='POST'>   

  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit" value='게시글 생성'>

</form>

{% endblock content %}
```

- base 템플릿에서 게시글 생성 버튼 만들기

```html

<body>
  ...
  <a href="{% url "articles:create" %}">게시글 생성</a>
  ...
</body>
```


### 2. detail 페이지 만들기

1. url 경로 만들어주기

``` python
# articles/urls.py

urlpatterns = [
    ...
    # detail 페이지에선 게시글의 pk를 사용하므로 
    # <int:article_pk>를 넣어준다.
    path('<int:article_pk>', views.detail, name='detail'),
    
]
```