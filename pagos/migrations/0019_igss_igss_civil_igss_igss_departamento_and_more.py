# Generated by Django 4.2.5 on 2023-10-09 23:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0018_bono14_aguinaldo'),
    ]

    operations = [
        migrations.AddField(
            model_name='igss',
            name='igss_civil',
            field=models.CharField(default='Soltero', max_length=50, verbose_name='Estado civil'),
        ),
        migrations.AddField(
            model_name='igss',
            name='igss_departamento',
            field=models.CharField(default='', max_length=50, verbose_name='Departamento'),
        ),
        migrations.AddField(
            model_name='igss',
            name='igss_municipio',
            field=models.CharField(default='', max_length=50, verbose_name='Municipio'),
        ),
        migrations.AddField(
            model_name='igss',
            name='igss_nac',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de nacimiento'),
        ),
        migrations.AddField(
            model_name='igss',
            name='igss_nacion',
            field=models.CharField(default='Guatemalteca', max_length=50, verbose_name='Nacionalidad'),
        ),
        migrations.AddField(
            model_name='igss',
            name='igss_ncm',
            field=models.CharField(default='', max_length=50, verbose_name='Nombre completo de Madre'),
        ),
        migrations.AddField(
            model_name='igss',
            name='igss_ncp',
            field=models.CharField(default='', max_length=50, verbose_name='Nombre completo de Padre'),
        ),
        migrations.AddField(
            model_name='igss',
            name='igss_sexo',
            field=models.CharField(default='', max_length=50, verbose_name='Sexo'),
        ),
    ]
