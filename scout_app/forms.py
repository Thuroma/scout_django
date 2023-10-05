from django import forms
from .models import Search

class NewSearchForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ('street_address', 'city', 'state', 'zip_code')
