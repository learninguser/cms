from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django import forms
import re
# from django.conf import settings
from account.models import User

class SignUpForm(UserCreationForm):

    email = forms.EmailField()
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    
    def clean_username(self):
        data = self.cleaned_data['username']
        regex="^[a-zA-z0-9._]{5,20}$"
        pattern = re.compile(regex)
        res = bool(re.search(pattern, data))
        if not res:
            raise forms.ValidationError("Invalid username",code ="invalid")
        return data

    class Meta:
        model = User
        fields = ('username','password1', 'password2', 'email', 'pic')

class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        for fieldname in ['username']:
            self.fields[fieldname].help_text = None
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')