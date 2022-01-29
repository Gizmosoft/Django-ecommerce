from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model

from .forms import ContactForm, LoginForm, RegisterForm

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

def login_page(request):
    if request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "User already logged in.") # Sending message to the user
        return redirect('/')
        
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }

    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            context['form'] = LoginForm()
            print("Error logging in.")
    
    return render(request, "auth/login.html", context)

User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        
        new_user = User.objects.create_user(username, email, password)
        print(new_user)
        messages.add_message(request, messages.INFO, "User Registered successfully!") # Sending message to the user
        return redirect('/')
    return render(request, "auth/register.html", context)

def logout_operation(request):
    logout(request)
    messages.add_message(request, messages.INFO, "User Logged out. Please login again to access content") # Sending message to the user
    return redirect('/')