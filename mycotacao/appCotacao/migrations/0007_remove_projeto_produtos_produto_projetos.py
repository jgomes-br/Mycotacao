# Generated by Django 4.0 on 2024-07-23 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appCotacao', '0006_projeto_produtos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projeto',
            name='produtos',
        ),
        migrations.AddField(
            model_name='produto',
            name='projetos',
            field=models.ManyToManyField(blank=True, to='appCotacao.Projeto'),
        ),
    ]
