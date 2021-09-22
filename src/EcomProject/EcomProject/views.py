from django.http import HttpResponse
from django.shortcuts import render

from .forms import ContactForm

def home_page(request):
    # create a python dictionary "context" and pass an arbitrary field value with a name ex: title
    context = {
        'title': 'We are in the Home Page.'
    }
    return render(request, "home.html", context)    #passing context to customize web pages

def about_page(request):
    context = {
        'title': 'We are in the About Page.'
    }
    return render(request, "home.html", context)

def contact_page(request):
    contact_form = ContactForm()    #create instance of form class
    context = {
        'title': 'We are in the Contact Page.',
        'desc': 'Fill the below form to reach out to us.',
        'form': contact_form        # form is  a context variable
    }

    if request.method == 'POST':
        print(request.POST.get('fullname'))
        print(request.POST.get('email'))
        print(request.POST.get('content'))
    return render(request, "contact.html", context)