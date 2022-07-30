from django import forms


class AnalyzeForm(forms.Form):
    search = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'id': 'search', 'placeholder': 'Type your instagram account', 'autocomplete' :'off'}))
    
class ContactForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control card-header mb-4', 'placeholder': 'Adresse électronique', 'id': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control card-header mb-4', 'placeholder': 'Mot de passe', 'id': 'password'}))