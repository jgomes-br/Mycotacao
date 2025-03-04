# Generated by Django 4.0 on 2025-03-02 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appCotacao', '0009_alter_lance_options_rename_lance_lance_sequencia_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotacao',
            name='status',
            field=models.SmallIntegerField(choices=[('1', 'Cotando'), ('2', 'Aceitar ou Recusar'), ('3', 'Finalizado com acordo'), ('5', 'Finalizado sem acordo')], max_length=1, null=True),
        ),
    ]
