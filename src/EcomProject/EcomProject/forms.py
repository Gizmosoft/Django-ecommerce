from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactForm(forms.Form):
    fullname = forms.CharField(
                widget=forms.TextInput(
                    attrs={
                        "class":"form-control", 
                        "id":"form_full_name", 
                        "placeholder":"Full Name"
                        }
                    )
                )
    email    = forms.EmailField(
                widget=forms.EmailInput(
                    attrs={
                        "class":"form-control",  
                        "placeholder":"E-mail"
                        }
                    )
                )
    content  = forms.CharField(
                widget=forms.Textarea(
                    attrs={
                        "class":"form-control",
                        "placeholder":"Your Message",
                        }
                    )
                )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not "@" in email:
            raise forms.ValidationError("Invalid email entered!")
        return email


class LoginForm(forms.Form):
    username = forms.CharField(
                widget=forms.TextInput(
                    attrs={
                        "class":"form-control", 
                        "id":"form_full_name", 
                        "placeholder":"Username"
                        }
                    )
                )
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(
                widget=forms.TextInput(
                    attrs={
                        "class":"form-control", 
                        "id":"form_full_name", 
                        "placeholder":"Username"
                        }
                    )
                )
    
    email    = forms.EmailField(
                widget=forms.EmailInput(
                    attrs={
                        "class":"form-control",  
                        "placeholder":"E-mail"
                        }
                    )
                )
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password' ,widget=forms.PasswordInput)

    # Validate is username already exists
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # using querysets to filter out usernames
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username

    # Validate is email already exists
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # using querysets to filter out usernames
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is taken")
        return email

    # Validate if both passwords are matching
    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2!= password:
            raise forms.ValidationError("Passwords must match!")
        return data