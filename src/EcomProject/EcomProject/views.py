from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ContactForm

def home_page(request):
    # a session variable has been created and stored in the cart_home() view in carts app which we can retrieve here as well.
    #print(request.session.get('first_name', 'Unknown')) # the second value is the default value that we have given which will be displayed by default in case no login is detected

    # create a python dictionary "context" and pass an arbitrary field value with a name ex: title
    context = {
        'title': 'We are in the Home Page.',
        'premium_content': 'This content is only available for people who have registered with us and logged in.'
    }
    return render(request, "home.html", context)    #passing context to customize web pages

def about_page(request):
    context = {
        'title': 'We are in the About Page.'
    }
    return render(request, "home.html", context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)    #create instance of form class; passing data through ContactForm
    context = {
        'title': 'We are in the Contact Page.',
        'desc': 'Fill the below form to reach out to us.',
        'form': contact_form        # form is  a context variable
    }

    if contact_form.is_valid():
        print(contact_form.cleaned_data)

    # if request.method == 'POST':
    #     print(request.POST.get('fullname'))
    #     print(request.POST.get('email'))
    #     print(request.POST.get('content'))
    return render(request, "contact.html", context)