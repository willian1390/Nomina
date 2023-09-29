# Generated by Django 4.2.5 on 2023-09-21 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0002_compra_compra_empleado_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='compra_preciou',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio unitario'),
        ),
        migrations.AlterField(
            model_name='compra',
            name='compra_total',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='producto_precio',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='producto_precio_descuento',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10, verbose_name='Precio con descuento'),
        ),
    ]
