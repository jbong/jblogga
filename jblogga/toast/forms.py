__author__ = 'jez'

from django import forms

class AddBlogEntryForm(forms.Form):

    title = forms.CharField(max_length=128, label='Title: ', widget=forms.TextInput(attrs={'class' : 'input title'}))
    body = forms.CharField(label='Body: ', widget=forms.Textarea(attrs={'class' : 'input tinyedit'}))

class DeleteBlogEntryForm(forms.Form):

    key = forms.CharField(max_length=128, widget=forms.HiddenInput())
