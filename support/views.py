# your_app/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from core.models import User
from .forms import SupportForm
from .models import SupportIssue


def issue_creation(request):
    issue_types = [
        ('Currency Exchange', 'fa-exchange-alt'),
        ('Buy/Sell Orders', 'fa-money-check-alt'),
        ('Portfolio', 'fa-chart-pie'),
        ('Purchase', 'fa-credit-card'),
        ('Unauthorized Charge', 'fa-exclamation-triangle'),
        ('Refunds', 'fa-undo'),
    ]

    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        form = SupportForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            support_issue = form.save(commit=False)
            support_issue.user = user
            support_issue.save()
            return redirect('support:list_issues')  # Redirect to a success page
    else:
        if request.user.is_authenticated:
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            form = SupportForm(user=user)
        else:
            return render(request, 'support/issue_creation.html', {'issue_types': issue_types})

    return render(request, 'support/issue_creation.html', {'form': form, 'issue_types': issue_types})


def list_issues(request):
    user_id = request.user.id
    user_issues = SupportIssue.objects.filter(user_id=user_id)
    return render(request, 'support/list_support_issues.html', {'user_issues': user_issues})
