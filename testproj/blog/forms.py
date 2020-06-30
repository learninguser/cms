from django import forms
from blog import models
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from account.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title','content','status','category','image']
        widgets={
            'content': SummernoteWidget(attrs={'class': 'form-control',}),
            'image': forms.FileInput(attrs={'class':'custom-file'}),
        }