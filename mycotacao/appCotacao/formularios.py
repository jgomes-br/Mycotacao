from django import forms
from .core.db.create_projeto import criar_cotacoes
from .models import Cotacao

class ProjectoAdminForm(forms.ModelForm):
    def save(self, commit=True):
        project = super(ProjectoAdminForm, self).save(commit=False)  
        project.save()
        self.save_m2m()
        criar_cotacoes(project)
        return project

class FormRespostaCotacao(forms.Form):
    cotacao_id = forms.IntegerField(widget=forms.HiddenInput)
    
    novo_custo = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        label="Nova contraproposta",
        widget=forms.NumberInput(attrs={
            'step': '0.01',          # Permite 2 casas decimais
            'class': 'form-control', # Exemplo: usando Bootstrap
            'placeholder': '0,00',
            'style': 'width: 100px; display: inline-block;text-align: center;',
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cotacao = kwargs.pop("cotacao", None)  # Pega o modelo se for passado
         # Se inicializar com dados (do initial), armazena o modelo na instância
        if "initial" in kwargs and kwargs["initial"]:
            self.cotacao = kwargs["initial"].get("cotacao")
        
        # se for passado pelo post
        if self.cotacao is None:
            chave = f"{kwargs.get('prefix', {})}-cotacao_id"
            numero_cotacao = kwargs.get('data', {}).get(chave, {})
            self.cotacao = Cotacao.objects.get(id=numero_cotacao)  # Se não for passado, pega do banco

    def get_model(self):
        return self.cotacao  # Método para acessar o modelo facilmente
    