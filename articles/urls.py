from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.main, name='main'),
    path('create/', views.create, name='create'),
    path('<int:article_pk>', views.detail, name='detail'),
]
