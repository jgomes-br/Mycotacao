# Generated by Django 4.0 on 2024-10-29 03:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appCotacao', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='nomeempresa',
            new_name='nome_fornecedor',
        ),
    ]
