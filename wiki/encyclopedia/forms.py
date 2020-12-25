from django import forms

class NewWikiForm(forms.Form):
    title = forms.CharField(label='Title', max_length=25)
    content= forms.CharField(widget=forms.Textarea , max_length=500)

class EditWikiForm(forms.Form):
    content= forms.CharField(widget=forms.Textarea , max_length=500)