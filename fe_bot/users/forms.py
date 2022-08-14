from django import forms

class NameForm(forms.Form):
    us_is = forms.CharField(label='us_is', max_length=100)