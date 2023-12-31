# Generated by Django 4.2.5 on 2023-09-23 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Empleados', '0006_remove_producto_producto_seccion_delete_compra_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nomina',
            name='nomina_empleado_id',
        ),
        migrations.AddField(
            model_name='empleado',
            name='empleado_departamento',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Empleados.departamento'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='empleado_puesto',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='empleados_puesto', to='Empleados.puesto'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='empleado_salario',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='empleados_salario', to='Empleados.puesto'),
        ),
        migrations.DeleteModel(
            name='Aumento',
        ),
        migrations.DeleteModel(
            name='Nomina',
        ),
    ]
