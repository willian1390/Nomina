# Generated by Django 4.2.5 on 2023-10-05 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0011_alter_igss_igss_empleado_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestamo',
            name='prestamo_aporte',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Aporte'),
        ),
    ]