from django import forms
from .models import *

class signupform(forms.ModelForm):
    class Meta:
        model=signupdata
        # fields='__all__'
        fields=['emailorphone','username','password','image']

class adsressform(forms.ModelForm):
    class Meta:
        model=signupdata
        # fields='__all__'
        fields=['username','address','city','country','phone']
        
class contactform(forms.ModelForm):
    class Meta:
        model=contact
        fields='__all__'

class paymentform(forms.ModelForm):
    class Meta:
        model=Payment
        fields='__all__'

class subform(forms.ModelForm):
    class Meta:
        model=Subscribe
        fields='__all__'

