# Generated by Django 4.2.5 on 2023-09-29 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0004_nomina_nomina_descuento_total_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nomina',
            name='nomina_dobles_calculada',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total horas dobles'),
        ),
        migrations.AlterField(
            model_name='nomina',
            name='nomina_extras_calculada',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total horas extras'),
        ),
        migrations.AlterField(
            model_name='nomina',
            name='nomina_interes',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Interes mensual'),
        ),
    ]
