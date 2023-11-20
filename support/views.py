# your_app/views.py
from django.shortcuts import render, redirect
from core.models import User
from .forms import SupportForm
from .models import SupportIssue


def issue_creation(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = SupportForm(request.POST, request.FILES, user=user)
        file = request.FILES['file']
        if form.is_valid():
            support_issue = form.save(commit=False)
            support_issue.user = user
            support_issue.save()
            return redirect('support:list_issues')  # Redirect to a success page
    else:
        form = SupportForm(user=user)

    return render(request, 'support/issue_creation.html', {'form': form})


def list_issues(request):
    user_id = request.user.id
    user_issues = SupportIssue.objects.filter(user_id=user_id)
    return render(request, 'support/list_support_issues.html', {'user_issues': user_issues})
