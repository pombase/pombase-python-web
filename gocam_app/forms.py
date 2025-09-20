from django import forms

class IdForm(forms.Form):
    ids = forms.CharField(label=False, widget=forms.Textarea)
