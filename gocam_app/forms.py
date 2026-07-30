from django import forms

class IdForm(forms.Form):
    model_ids = forms.CharField(label=False, widget=forms.Textarea(attrs={'class': 'ids-field'}))
    highlight_gene_ids = forms.CharField(label=False, widget=forms.Textarea(attrs={'class': 'ids-field'}), required=False, strip=True)
    dag = forms.BooleanField(label="Use top-down layout", required=False)
    targets = forms.BooleanField(label="Include targets", required=False)
