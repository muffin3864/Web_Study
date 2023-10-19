from django.shortcuts import render, redirect

from .models import Article

# Create your views here.
def main(request):
    articles = Article.objects.all().order_by('-pk')
    context = {
        'articles': articles,
    }
    return render(request, 'articles/main.html', context)