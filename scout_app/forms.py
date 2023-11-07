from django import forms

class NewSearchForm(forms.Form):
    class Meta:
        fields = ('street_address', 'city', 'state')
