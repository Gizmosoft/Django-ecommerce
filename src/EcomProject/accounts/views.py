from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from django.utils.http import is_safe_url

# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "User already logged in.") # Sending message to the user
        return redirect('/')
        
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }

# Handling correct redirection after auth
    # This is to handle authentication in between some transactions. This will enable users to resume where they left off before trying to login ex: checkout page
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
        else:
            context = {
                'form': LoginForm,
                'error_message':"Error logging in!"
            }
            #context['form'] = LoginForm()
            print("The given username or password is incorrect. Error Logging in!")
    
    return render(request, "accounts/login.html", context)

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
    return render(request, "accounts/register.html", context)

def logout_operation(request):
    logout(request)
    messages.add_message(request, messages.INFO, "User Logged out. Please login again to access content") # Sending message to the user
    return redirect('/')