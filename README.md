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


### 7. 앱에서 urls 관리

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


### 8. 