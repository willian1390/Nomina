# Generated by Django 4.2.5 on 2023-10-06 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0016_alter_nomina_nomina_bonificacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nomina',
            name='nomina_piezas',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Piezas hechas (Depto. Produccion)'),
        ),
        migrations.AlterField(
            model_name='nomina',
            name='nomina_ventas',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Venta realizada (Depto. Ventas)'),
        ),
    ]