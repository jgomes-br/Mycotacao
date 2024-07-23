# Generated by Django 4.0 on 2024-07-23 03:27

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
                ('cnpj', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, unique=True)),
                ('start', models.DateTimeField()),
                ('fim', models.DateTimeField(null=True)),
                ('lance_atual', models.SmallIntegerField(default=1)),
                ('produtos', models.CharField(default='', max_length=200)),
                ('fornecedores', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Estrutura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('1', 'Aguardando fornecedor'), ('2', 'Aguardando Adm'), ('3', 'Finalizado')], max_length=1, null=True)),
                ('lance_vencedor', models.SmallIntegerField(null=True)),
                ('volume', models.IntegerField(null=True)),
                ('fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCotacao.fornecedor')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCotacao.produto')),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCotacao.projeto')),
            ],
            options={
                'unique_together': {('projeto', 'produto', 'fornecedor')},
            },
        ),
        migrations.CreateModel(
            name='Lance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lance', models.SmallIntegerField()),
                ('preco', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=5)),
                ('status', models.CharField(choices=[('P', 'Pendente'), ('A', 'Aceito'), ('R', 'Recusado'), ('S', 'Avançou sem resposta')], max_length=1, null=True)),
                ('obs', models.CharField(max_length=100, null=True)),
                ('dono', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='User')),
                ('estrutura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCotacao.estrutura')),
            ],
            options={
                'unique_together': {('lance', 'estrutura')},
            },
        ),
    ]