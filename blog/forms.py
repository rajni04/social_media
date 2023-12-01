from .models import *
from django import forms

class blogForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields='__all__'
        exclude=['likes','date','author']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)
