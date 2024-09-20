from django import forms


class ContactUsForm(forms.Form):
    message = forms.CharField()
