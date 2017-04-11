from django.shortcuts import render

from .classifier import classify, get_cat

# urlの入力フォーム
def index(request):
    article_url = request.GET.get('article_url')
    context = {}
    context['article_cat'] = None

    if article_url:
        context['article_cat'] = get_cat(article_url)

    return render(request, 'app/index.html', context)
