from django import forms

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
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

