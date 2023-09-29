# Generated by Django 4.2.5 on 2023-09-26 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0002_nomina_nomina_aumento_total_nomina_nomina_piezas_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aporte',
            fields=[
                ('aporte_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Liquidacion',
            fields=[
                ('liquidacion_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('prestamo_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='nomina',
            name='nomina_dobles_calculada',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10, verbose_name='Total horas dobles'),
        ),
        migrations.AddField(
            model_name='nomina',
            name='nomina_extras_calculada',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10, verbose_name='Total horas extras'),
        ),
        migrations.AddField(
            model_name='nomina',
            name='nomina_igss',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='IGSS'),
        ),
        migrations.AddField(
            model_name='nomina',
            name='nomina_prestamo',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Prestamo'),
        ),
        migrations.AddField(
            model_name='nomina',
            name='nomina_tienda',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Compras en tienda'),
        ),
        migrations.AlterField(
            model_name='nomina',
            name='nomina_piezas',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Piezas hechas (Depto. Produccion)'),
        ),
        migrations.AlterField(
            model_name='nomina',
            name='nomina_ventas',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Venta realizada (Depto. Ventas)'),
        ),
    ]