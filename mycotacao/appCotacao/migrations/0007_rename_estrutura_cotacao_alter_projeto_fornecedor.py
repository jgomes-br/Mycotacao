# Generated by Django 4.0 on 2025-03-02 03:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appCotacao', '0006_auto_20250302_0021'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Estrutura',
            new_name='Cotacao',
        ),
        migrations.AlterField(
            model_name='projeto',
            name='fornecedor',
            field=models.ManyToManyField(limit_choices_to={'is_active': True, 'is_staff': False, 'is_superuser': False}, to=settings.AUTH_USER_MODEL),
        ),
    ]
