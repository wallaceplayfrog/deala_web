from django import forms
from myapp.models import Company_Info

class SelectForm(forms.Form):
    company = forms.ModelChoiceField(
        queryset=Company_Info.objects.all(), 
        widget=forms.Select(
            attrs={'class':'form-control'}
        )
    )