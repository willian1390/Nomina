from django.db import models
from Empleados.models import Empleado

# Create your models here.
class Seccion(models.Model):
    seccion_id = models.AutoField(primary_key=True)
    seccion_nombre =  models.CharField(max_length=50, verbose_name="Nombre de seccion")        

    def __str__(self):
        return self.seccion_nombre    

class Producto(models.Model):
    producto_id = models.AutoField(primary_key=True)
    producto_imagen = models.ImageField(upload_to='producto', null=True, blank=True)
    producto_nombre = models.CharField(max_length=50, verbose_name="Nombre de producto")
    producto_descripcion = models.CharField(max_length=500, verbose_name="Descripcion")
    producto_seccion = models.ForeignKey(Seccion, null=False, default=None, blank=False, on_delete=models.CASCADE)
    producto_precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    producto_descuento = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Descuento", blank=True, null=True)
    producto_precio_descuento = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio con descuento", editable=False, default=0)
    def __str__(self):
        return self.producto_nombre
"""     def save(self, *args, **kwargs):
        if self.producto_descuento:
            descuento = self.producto_precio * (self.producto_descuento / 100)
            self.producto_precio_descuento = self.producto_precio - descuento
        else:
            self.producto_precio_descuento = 0
        super().save(*args, **kwargs) """
    




class Compra(models.Model):
    compra_id = models.AutoField(primary_key=True)
    compra_fecha = models.DateTimeField(auto_now_add=True)
    compra_empleado_id = models.ForeignKey(Empleado, null=False, default=None, blank=False, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='CompraProducto' ,blank=True)

"""     def calcular_total(self):
        total = 0
        for compra_producto in self.compraproducto_set.all():
            total += compra_producto.producto.producto_precio * compra_producto.compra_cantidad
        return total  """   

class CompraProducto(models.Model):
    compra= models.ForeignKey(Compra, on_delete=models.CASCADE, blank=True, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=True, null=True)
    compra_cantidad = models.IntegerField(verbose_name="Cantidad", default=0)
    compra_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total", default=0)

"""     def save(self, *args, **kwargs):
        if self.producto and self.compra_cantidad:
            self.compra_total = self.producto.producto_precio * self.compra_cantidad
        else:
            self.compra_total = 0
        super().save(*args, **kwargs) """