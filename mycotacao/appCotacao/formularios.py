from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Projeto

class TesteForm(forms.Form):
    template_name = "cotacao/form_snippet.html"
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    btn = forms

    def clean(self):
        cleaned_data = super().clean()
        # self.add_error("cc_myself", "oi meu amigo")

class ProjetoForm(forms.Form):
    cod = forms.IntegerField(initial=-1)
    titulo = forms.CharField(max_length=100, 
                             widget=forms.TextInput(
                                 attrs={'class':'form-control'}))
    inicio = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={'type':'datetime-local', 'class':'form-control'}))
    fim = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={'type':'datetime-local', 'class':'form-control'}), 
            required=False)
    fornecedor = forms.CharField()
    produto = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        cod = self.cleaned_data['cod']
        if Projeto.objects.filter(nome=self.cleaned_data['titulo'], pk__lt=cod).exists():
            self.add_error('titulo', 'Titulo já existe')
