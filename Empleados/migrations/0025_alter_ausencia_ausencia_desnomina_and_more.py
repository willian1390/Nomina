# Generated by Django 4.2.5 on 2023-10-04 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empleados', '0024_alter_puesto_puesto_cantidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ausencia',
            name='ausencia_desNomina',
            field=models.BooleanField(default=False, editable=False, verbose_name='Descuento en nomina?'),
        ),
        migrations.AlterField(
            model_name='ausencia',
            name='ausencia_descuento',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Descuento'),
        ),
    ]
