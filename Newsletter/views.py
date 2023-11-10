from django.shortcuts import render
from .models import News


def news_list(request):
    # news_articles = News.objects.all().order_by('-pub_date')
    news = [
        {
            "Title": "Bitcoin",
            "Content": "Trending news for Bitcoin",
            "Publish_date": "1/1/23"
        },
        {
            "Title": "Crypto",
            "Content": "Trending news for Crypto",
            "Publish_date": "1/1/24"
        }]
    context = {
        "news": news
    }
    return render(request, 'newsletter/news_list.html', context)
