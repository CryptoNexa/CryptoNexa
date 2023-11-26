from django.shortcuts import render, redirect
from .forms import ContactForm
from django.urls import reverse


def contact_us_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('contact-success'))
    else:
        form = ContactForm()
    return render(request, 'ContactUs/Contact_us.html', {'form': form})

def success_view(request):
    return render(request, 'ContactUs/success.html')
