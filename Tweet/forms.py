from django.forms import ModelForm
from .models import Post, Retweet,Reply
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 30, 'rows': 10}))
    profile_image = forms.ImageField(required=False)
    cover_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'bio', 'profile_image', 'cover_picture']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username.startswith('@'):
            raise forms.ValidationError("Username must start with '@'")
        return username
    
    

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body', 'image']
        widgets = {
            'body': forms.Textarea(attrs={'cols': 70, 'rows': 2}),
        }
        labels = {
            'body': ''
        }
        
        
class ReplyForm(ModelForm):
    class Meta:
        model= Reply
        fields=['content']
        widgets={
            'content':forms.Textarea(attrs={'cols':70, 'rows':1})
        }
        labels={
            'content':''
        }
        
        
class SearchQueryForm(forms.Form):
    search_query= forms.CharField(max_length='80',label='search', required=False)
    
class DMForm(ModelForm):
    class meta:
        fields=['body', 'receiver']
        
    