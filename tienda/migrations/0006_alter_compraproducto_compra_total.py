# Generated by Django 4.2.5 on 2023-09-22 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0005_remove_compra_compra_cantidad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compraproducto',
            name='compra_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total'),
        ),
    ]
