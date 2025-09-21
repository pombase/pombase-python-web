from django import forms

class IdForm(forms.Form):
    ids = forms.CharField(label=False, widget=forms.Textarea(attrs={'class': 'ids-field'}))
    dag = forms.BooleanField(label="Use top-down layout", required=False)
