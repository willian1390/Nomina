# Generated by Django 4.2.5 on 2023-10-09 23:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0019_igss_igss_civil_igss_igss_departamento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='igss',
            name='igss_nac',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Fecha de nacimiento'),
        ),
    ]
