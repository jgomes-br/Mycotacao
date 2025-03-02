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
    fornecedor = models.ManyToManyField(CustomUser, 
                                        limit_choices_to={'is_active': True, 
                                                          'is_superuser': False, 
                                                          "is_staff": False})
    produto = models.ManyToManyField(Produto)
    
    def __str__(self) -> str:
        return self.nome

class Lance(models.Model):

    class Meta:
        ordering = ['lance']
    OPCOES_STATUS =(
        ('P', 'Pendente'),
        ('A', 'Aceito'),
        ('R', 'Recusado'),
        ('D', 'Desistiu'),
    )   
    data = models.DateTimeField(auto_now_add=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(CustomUser,verbose_name = 'User', on_delete=models.CASCADE)
    dono = models.ForeignKey(CustomUser, related_name='dono', on_delete=models.CASCADE)
    numero = models.SmallIntegerField()
    preco = models.DecimalField(default=Decimal("0.0"), max_digits=5 ,decimal_places=2)
    status = models.CharField(max_length=1, null=True, choices=OPCOES_STATUS)