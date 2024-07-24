from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Projeto, Produto, Fornecedor

from .opdb import create_strutura

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

class ProjectoAdminForm(forms.ModelForm):
    class Meta:
        model = Projeto
        exclude = ('produto','fornecedor')
        fields = "__all__" # not in original SO post

    produtos = forms.ModelMultipleChoiceField(
        queryset=Produto.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Produtos',
            is_stacked=False
        )
    )

    fornecedores = forms.ModelMultipleChoiceField(
        queryset=Fornecedor.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Fornecedores',
            is_stacked=False
        )
    )

    def __init__(self, *args, **kwargs):
        super(ProjectoAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['fornecedores'].initial = self.instance.fornecedor.all()
            self.fields['produtos'].initial = self.instance.produto.all()

    def save(self, commit=True):
        project = super(ProjectoAdminForm, self).save(commit=False)  
        if commit:
            project.save()

        if project.pk:
            
            project.produto.set(self.cleaned_data['produtos'])
            project.fornecedor.set(self.cleaned_data['fornecedores'])
            # print(project.produto.set)
            self.save_m2m()
            
        create_strutura(project)
        
        return project