from django.db import models
from django.contrib.auth.models import  AbstractUser


from decimal import Decimal

class CustomUser(AbstractUser):
    # user = models.One ToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nome_fornecedor = models.CharField(max_length=100, unique=True)
    contrato = models.DecimalField(default=Decimal("0.0"), max_digits=5, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.nome_fornecedor} "


class Produto(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.descricao
    

class Projeto(models.Model):
    nome = models.CharField(max_length=200, unique=True)
    start = models.DateField()
    fim = models.DateField(null=True)
    fornecedores = models.ManyToManyField(CustomUser, 
                                        limit_choices_to={'is_active': True, 
                                                          'is_superuser': False, 
                                                          "is_staff": False})
    produtos = models.ManyToManyField(Produto)
    
    def __str__(self) -> str:
        return self.nome

class Lance(models.Model):

    class Meta:
        ordering = ['sequencia']
    OPCOES_STATUS =(
        ('P', 'Pendente'),
        ('A', 'Aceito'),
        ('R', 'Recusado'),
    )
    dono = models.ForeignKey(CustomUser,verbose_name = 'User', on_delete=models.CASCADE)
    sequencia = models.SmallIntegerField()
    preco = models.DecimalField(default=Decimal("0.0"), max_digits=5 ,decimal_places=2)
    status = models.CharField(max_length=1, null=True, choices=OPCOES_STATUS)


class Cotacao(models.Model):
    OPCOES_STATUS =(
        (1, 'Cotando'),
        (2, 'Aceitar ou Recusar'),
        (3, 'Finalizado com sucesso'),
        (5, 'Finalizado sem sucesso'),
    )
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.SmallIntegerField(null=True, choices=OPCOES_STATUS)
    qtd_max_lances = models.SmallIntegerField(default=4)
    lances_old = models.ManyToManyField(Lance)
    # lances_inlinha = minha_lista = models.JSONField(default=list)
    
    
    class Meta:
        unique_together  = [["produto", "fornecedor", "projeto"]]

    @property
    def ja_finalizou(self):
        return self.status >= 3

