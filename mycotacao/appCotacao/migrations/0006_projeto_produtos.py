# Generated by Django 4.0 on 2024-07-23 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appCotacao', '0005_remove_projeto_fornecedores_remove_projeto_produto'),
    ]

    operations = [
        migrations.AddField(
            model_name='projeto',
            name='produtos',
            field=models.ManyToManyField(blank=True, to='appCotacao.Produto'),
        ),
    ]
