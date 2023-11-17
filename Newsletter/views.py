from django.shortcuts import render, redirect
from .models import News
from django.views.generic.edit import FormView
from .forms import Subscription
from django.urls import reverse


def news_list(request):
    news_articles = News.objects.all().order_by('-pub_date')
    context = {
        "news": news_articles
    }
    return render(request, 'newsletter/news_list.html', context)


def success_view(request):
    return render(request, 'newsletter/success.html')


def subscribe(request):
    if request.method == 'POST':
        form = Subscription(request.POST)
        if form.is_valid():
            form.save()
            # return super().form_valid(form)
            return redirect(reverse('success'))

    else:
        form = Subscription()

    return render(request, 'newsletter/subscribe.html', {'form': form})
