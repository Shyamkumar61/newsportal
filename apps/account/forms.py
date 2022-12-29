from django.forms import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm as CorePasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms
from .utils import generate_username

User = get_user_model()


class SingUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            'email', 'first_name', 'last_name', 'password1', 'password2'
        ]
        labels = {
            'email': 'Email',
            'username': 'Username',
            'password1': 'Password',
            'password2': 'Confirm Password'
        }

    def __init__(self, *args, **kwargs):
        super(SingUpForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-control-lg'})

    def save(self, commit=False):
        user = super(SingUpForm, self).save(commit=False)
        user.username = generate_username()
        user.save()
        return user


class EditProfile(ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',

        }

    def __init__(self, *args, **kwargs):
        super(EditProfile, self).__init__(*args, **kwargs)
        for name, fields in self.fields.items():
            fields.widget.attrs.update({'class': 'form-control form-control-lg'})


class PasswordChangeForm(CorePasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control form-control-lg', 'placeholder': self.fields[field].label
            })
