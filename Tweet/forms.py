from django.forms import ModelForm
from .models import Post, Retweet,Reply
from django import forms

class PostForm(ModelForm):
    class Meta:
        model= Post
        fields=['body']
        widgets = {
            'body': forms.Textarea(attrs={'cols': 70, 'rows': 2}), 
        }
        labels={
            'body':''
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
        
    