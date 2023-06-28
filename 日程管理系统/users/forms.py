from django import forms
from django.contrib.auth.models import User

from .models import Profile

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length = 100, required = True, widget = forms.TextInput(attrs = {'class': 'form-control2'}))
    email = forms.EmailField(required = True, widget = forms.TextInput(attrs = {'class': 'form-control2'}))
    first_name = forms.CharField(required = False, max_length = 100, widget = forms.TextInput(attrs = {'class': 'form-control2'}))
    last_name = forms.CharField(required = False, max_length = 100, widget = forms.TextInput(attrs = {'class': 'form-control2'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget = forms.FileInput(attrs = {'class': 'form-control-file'}))
    bio = forms.CharField(required = False, widget = forms.Textarea(attrs = {'class': 'form-control', 'rows': 5, 'max-width': 96, 'max-height': 20}))
# style="max-width: 900px; max-height: 200px;"
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']