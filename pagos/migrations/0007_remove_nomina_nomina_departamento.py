# Generated by Django 4.2.5 on 2023-09-29 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0006_nomina_nomina_departamento_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nomina',
            name='nomina_departamento',
        ),
    ]
