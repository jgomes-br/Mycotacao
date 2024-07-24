from django.db import models
from django.contrib.auth.models import  User, Group

from decimal import Decimal

class Produto(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.descricao
    
class Fornecedor(models.Model):
    nomeempresa = models.CharField(max_length=100, unique=True)
    responsavel = models.ForeignKey(User,verbose_name = 'User', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nomeempresa

class Projeto(models.Model):
    nome = models.CharField(max_length=200, unique=True)
    start = models.DateTimeField()
    fim = models.DateTimeField(null=True)
    lance_atual = models.SmallIntegerField(default=1)
    fornecedor = models.ManyToManyField(Fornecedor)
    produto = models.ManyToManyField(Produto)
    
    def __str__(self) -> str:
        return self.nome

class Estrutura(models.Model):
    OPCOES_STATUS =(
        ('1', 'Aguardando fornecedor'),
        ('2', 'Aguardando Adm'),
        ('3', 'Finalizado'),
    )
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, null=True, choices=OPCOES_STATUS)
    lance_vencedor = models.SmallIntegerField(null=True)
    volume = models.IntegerField(null=True)

    class Meta:
        unique_together  = [["produto", "fornecedor", "projeto"]]


class Lance(models.Model):
    OPCOES_STATUS =(
        ('P', 'Pendente'),
        ('A', 'Aceito'),
        ('R', 'Recusado'),
        ('S', 'Avançou sem resposta')
    )
    estrutura = models.ForeignKey(Estrutura, on_delete=models.CASCADE)
    dono = models.ForeignKey(User,verbose_name = 'User', on_delete=models.CASCADE)
    lance = models.SmallIntegerField()
    preco = models.DecimalField(default=Decimal("0.0"), max_digits=5 ,decimal_places=2)
    status = models.CharField(max_length=1, null=True, choices=OPCOES_STATUS)
    obs = models.CharField(max_length=100, null=True)

    class Meta:
        unique_together  = [["lance", "estrutura"]]