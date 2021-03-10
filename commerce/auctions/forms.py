from django import forms

CATEGORIES_CHOICES= [
    ('fashion', 'Fashion'),
    ('toys', 'Toys'),
    ('electronics', 'Electronics'),
    ('home', 'Home'),
    ]

class Listingform(forms.Form):

    title = forms.CharField(max_length=25 , required=True)
    description= forms.CharField(widget=forms.Textarea , max_length=2000 , required=True)
    bid= forms.DecimalField(max_digits=8, decimal_places=2,required=True , min_value=0)
    url = forms.URLField (max_length=200,required=False)