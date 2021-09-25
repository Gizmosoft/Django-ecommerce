from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import ContactForm, LoginForm

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

def login_page(request):
    if request.user.is_authenticated:
        logout(request)
        
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }
    print(request.user.is_authenticated)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(request, username=username, password=password)
        print(request.user.is_authenticated)    # Check auth status again
        if user is not None:
            print(request.user.is_authenticated)    # Check auth status again
            print(user)
            login(request, user)
            return redirect("/")
        else:
            context['form'] = LoginForm()
            print("Error logging in.")
    
    return render(request, "auth/login.html", context)

def register_page(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
    return render(request, "auth/register.html", {})