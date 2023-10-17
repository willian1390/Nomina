from django.contrib import admin, messages
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from .models import Producto, Seccion, Compra, CompraProducto
from django.core.exceptions import ValidationError
from django.utils.html import format_html

# Register your models here.
class CompraProductoInline(admin.TabularInline):
    model = CompraProducto
    extra = 1
    autocomplete_fields = ['producto']
    readonly_fields = ['compra_total']
    list_display=("compra_id", "compra_empleado_id",)

class ProductoAdmin(admin.ModelAdmin):
    #inlines = [CompraProductoInline,]
    search_fields = ('producto_nombre'),
    ordering = ['producto_nombre']
    list_display=("producto_nombre", "producto_precio", "producto_seccion",'foto',)
    list_per_page = 20
    #mostrar la foto del producto
    def foto(self, object):
        return format_html ('<img src={} width="70" height="70" />', object.producto_imagen.url)

class CompraAdmin(admin.ModelAdmin):
    inlines = [CompraProductoInline,]
    actions = ["generar_pdf_compra"]
    search_fields = ('compra_empleado_id'),
    autocomplete_fields=['compra_empleado_id']
    list_display = (
        'compra_id',
        'compra_empleado_id', 'compra_total',)
    filter_horizontal = ['productos',]
    list_display_links = ["compra_empleado_id"]
    #mostrar el total de la compra
    def compra_total(self, obj):
        total = sum(item.compra_total for item in obj.compraproducto_set.all())
        return total

    compra_total.short_description = "Total de la Compra"
 
    def generar_pdf_compra(self, request, queryset):
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=detalle_compra.pdf"

        # Crear un objeto PDF con reportlab
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        logo = Image('pagos/img_logo/logo.png', width=50, height=50)
        elements.append(logo)
        elements.append(Spacer(1, 35))

        title = "TIENDA EMPRESARIAL"
        title_paragraph = Paragraph(title, getSampleStyleSheet()['Title'])
        elements.append(title_paragraph)
        elements.append(Spacer(1, 10))

        for compra in queryset:
            data = []

            data.append(["ID de Compra:", compra.compra_id])
            data.append(["Fecha de Compra:", compra.compra_fecha.strftime('%d/%m/%Y %H:%M:%S')])
            data.append(["ID de Empleado:", compra.compra_empleado_id.empleado_id])
            nombre_apellido = f"{compra.compra_empleado_id.empleado_nombre} {compra.compra_empleado_id.empleado_apellido}"
            data.append(["Empleado:", nombre_apellido])
            data.append(["", "", ""])
            data.append(["Productos", "Cantidad", "Total"])

            for compra_producto in compra.compraproducto_set.all():
                data.append([compra_producto.producto.producto_nombre,
                            compra_producto.compra_cantidad,
                            f"Q{compra_producto.compra_total}"])

            total_compra = sum(item.compra_total for item in compra.compraproducto_set.all())
            data.append(["", "Total de la Compra:", f"Q{total_compra}"])

            # Crear una tabla con los datos
            table = Table(data, colWidths=[110, 170, 100])
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
            elements.append(Spacer(1, 12))

        doc.build(elements)
        return response

    generar_pdf_compra.short_description = "Detalle de compra"

    def validar_compra(self):
        total_compra = sum(item.compra_total for item in self.compraproducto_set.all())
        if total_compra > self.compra_empleado_id.empleado_salario:
            raise ValidationError("La compra no puede ser realizada, el salario es insuficiente para cubrir el costo.")

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Seccion)
admin.site.register(Compra, CompraAdmin)
