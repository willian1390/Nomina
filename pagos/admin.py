##Admin de pagos
from django.contrib import admin
from datetime import datetime, date
from django.db import transaction

from .models import *
# Register your models here.
import io
from django.http import HttpResponse, FileResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
styles = getSampleStyleSheet()



def generar_pdf_nomina(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=detalle_nomina.pdf"

    # Crear un objeto PDF con ReportLab
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    elements = []

    logo = Image('pagos/img_logo/logo.png', width=60, height=60)
    elements.append(logo)
    elements.append(Spacer(1, 35))

    for nomina in queryset:
        data = []

        empleado = nomina.nomina_empleado_id

        # Información del empleado
        nombre_completo = f"{empleado.empleado_nombre} {empleado.empleado_apellido}"
        fecha_nomina = nomina.nomina_fecha.strftime('%d/%m/%Y')
        sueldo_base = nomina.nomina_sueldo_base
        aumento = nomina.nomina_aumento_total
        horas_extras = nomina.nomina_extras
        total_horas_extras = nomina.nomina_extras_calculada
        horas_dobles = nomina.nomina_dobles
        total_horas_dobles = nomina.nomina_dobles_calculada
        venta_realizada = nomina.nomina_ventas
        comision = nomina.nomina_comision
        piezas_elaboradas = nomina.nomina_piezas
        bonificacion = nomina.nomina_bonificacion

        # Información de ingresos y descuentos
        ingreso_total = nomina.nomina_ingreso_total
        igss = nomina.nomina_igss
        compras_tienda = nomina.nomina_tienda
        prestamos = nomina.nomina_prestamo
        aporte_solidario = nomina.nomina_aporte
        descuento_total = nomina.nomina_descuento_total
        sueldo_neto = nomina.nomina_neto

        # Agregar los datos a la tabla
        data.append(["Nombre completo:", nombre_completo, "Fecha:", fecha_nomina])
        data.append(["Sueldo base:", sueldo_base, "Aumento:", aumento])
        data.append(["Horas extras:", horas_extras, "Total:", total_horas_extras])
        data.append(["Horas dobles:", horas_dobles, "Total:", total_horas_dobles])
        data.append(["Venta realizada:", venta_realizada, "Comision:", comision])
        data.append(["Piezas elaboradas:", piezas_elaboradas, "Bonificacion:", bonificacion])
        data.append(["", "", "Ingreso total:", ingreso_total])
        data.append(["IGSS:", igss, "", ""])
        data.append(["Compras en tienda:", compras_tienda, "", ""])
        data.append(["Prestamos:", prestamos, "", ""])
        data.append(["Aporte Solidario:", aporte_solidario, "", ""])
        data.append(["", "", "Descuento total:", descuento_total])
        data.append(["", "", "Sueldo neto:", sueldo_neto])

        # Crear una tabla con los datos
        table = Table(data, colWidths=[200, 200, 100, 100])
        table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

    doc.build(elements)
    return response

generar_pdf_nomina.short_description = "Generar PDF de Nomina"

def generar_pdf_igss(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=detalle_igss.pdf"

    # Crear un objeto PDF con reportlab
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    elements = []

    logo = Image('pagos/img_logo/logo.png', width=50, height=50)
    elements.append(logo)
    elements.append(Spacer(1, 35))

    title = "IGSS"
    title_paragraph = Paragraph(title, getSampleStyleSheet()['Title'])
    elements.append(title_paragraph)
    elements.append(Spacer(1, 10))

    for igss in queryset:
        data = []

        empleado = igss.igss_empleado_id
        fecha_nacimiento = igss.igss_nac.strftime('%d/%m/%Y')

        # Agregar información del empleado
        nombre_completo = f"{empleado.empleado_nombre} {empleado.empleado_apellido}"
        data.append(["Fecha:", igss.igss_fecha.strftime('%d/%m/%Y'), "", ""])
        data.append(["Nombre completo:", nombre_completo, "Fecha nacimiento:", fecha_nacimiento])
        data.append(["DPI:", empleado.empleado_dpi, "Teléfono:", empleado.empleado_telefono])
        data.append(["Email:", empleado.empleado_correo, "", ""])
        data.append(["", "", "", ""])
        data.append(["Sexo:", igss.igss_sexo, "Estado civil:", igss.igss_civil])
        data.append(["Nacionalidad:", igss.igss_nacion, "Departamento:", igss.igss_departamento])
        data.append(["Municipio:", igss.igss_municipio, "", ""])
        data.append(["Dirección:", empleado.empleado_direccion, "", ""])
        data.append(["", "", "", ""])
        data.append(["Nombre completo de padre:", igss.igss_ncp, "", ""])
        data.append(["Nombre completo de madre:", igss.igss_ncm, "", ""])
        data.append(["", "", "", ""])
        data.append(["Nombre de empresa:", "Sport", ""])
        data.append(["Ocupación:", empleado.empleado_puesto, "Monto IGSS:", igss.igss_cantidad])

        # Crear una tabla con los datos
        table = Table(data, colWidths=[150, 300, 150, 150])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))
    
    elements.append(Spacer(1, 35))

    styles = getSampleStyleSheet()
    signature_text = "Firma Empleado:___________________________________________"
    signature_paragraph = Paragraph(signature_text, styles['Normal'])
    elements.append(signature_paragraph)

    doc.build(elements)
    return response

generar_pdf_igss.short_description = "Reporte PDF IGSS"

def generar_pdf_bono14(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=detalle_bono14.pdf"

    # Crear un objeto PDF con ReportLab
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Logo de la empresa
    logo = Image('pagos/img_logo/logo.png', width=70, height=70)
    elements.append(logo)
    elements.append(Spacer(1, 35))

    title = "Bono 14"
    title_paragraph = Paragraph(title, getSampleStyleSheet()['Title'])
    elements.append(title_paragraph)
    elements.append(Spacer(1, 10))

    for bono in queryset:
        data = []

        # Información del empleado y la fecha
        empleado = bono.bono_empleado_id
        fecha = bono.bono_fecha.strftime('%d/%m/%Y')

        data.append([f"Empleado: {empleado.empleado_nombre} {empleado.empleado_apellido}"])
        data.append([f"Fecha: {fecha}"])
        data.append([f"Codigo: {empleado.empleado_id}"])
        data.append([f"Monto: {bono.bono_monto}"])

        # Crear una tabla con los datos
        table = Table(data, colWidths=[300])
        table.setStyle(TableStyle([

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(table)
        elements.append(Spacer(1, 12))

    elements.append(Spacer(1, 35))

    styles = getSampleStyleSheet()
    signature_text = "Firma Empleado:___________________________________________"
    signature_paragraph = Paragraph(signature_text, styles['Normal'])
    elements.append(signature_paragraph)

    elements.append(Spacer(1, 35))

    doc.build(elements)
    return response

generar_pdf_bono14.short_description = "Reporte PDF Bono14"

def generar_pdf_aguinaldo(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=detalle_aguinaldo.pdf"

    # Crear un objeto PDF con ReportLab
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Logo de la empresa
    logo = Image('pagos/img_logo/logo.png', width=70, height=70)
    elements.append(logo)
    elements.append(Spacer(1, 35))

    title = "Aguinaldo"
    title_paragraph = Paragraph(title, getSampleStyleSheet()['Title'])
    elements.append(title_paragraph)
    elements.append(Spacer(1, 10))

    for aguinaldo in queryset:
        data = []

        # Información del empleado y la fecha
        empleado = aguinaldo.aguinaldo_empleado_id
        fecha = aguinaldo.aguinaldo_fecha.strftime('%d/%m/%Y')

        data.append([f"Empleado: {empleado.empleado_nombre} {empleado.empleado_apellido}"])
        data.append([f"Fecha: {fecha}"])
        data.append([f"Codigo: {empleado.empleado_id}"])
        data.append([f"Monto: {aguinaldo.aguinaldo_monto}"])

        # Crear una tabla con los datos
        table = Table(data, colWidths=[300])
        table.setStyle(TableStyle([

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(table)
        elements.append(Spacer(1, 12))

    elements.append(Spacer(1, 35))

    styles = getSampleStyleSheet()
    signature_text = "Firma Empleado:___________________________________________"
    signature_paragraph = Paragraph(signature_text, styles['Normal'])
    elements.append(signature_paragraph)

    elements.append(Spacer(1, 35))

    doc.build(elements)
    return response

generar_pdf_aguinaldo.short_description = "Reporte PDF Aguinaldo"

def generar_pdf_prestamo(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=detalle_prestamo.pdf"

    # Crear un objeto PDF con ReportLab
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    

    # Logo de la empresa
    logo = Image('pagos/img_logo/logo.png', width=50, height=50)
    elements.append(logo)
    elements.append(Spacer(1, 35))

    title = "Prestamo"
    title_paragraph = Paragraph(title, getSampleStyleSheet()['Title'])
    elements.append(title_paragraph)
    elements.append(Spacer(1, 10))

    for prestamo in queryset:
        data = []

        # Información del empleado y la fecha
        empleado = prestamo.prestamo_empleado_id
        fecha = prestamo.prestamo_fecha.strftime('%d/%m/%Y')

        data.append([f"Empleado: {empleado.empleado_nombre} {empleado.empleado_apellido}", f"Fecha: {fecha}"])
        data.append([f"Puesto: {empleado.empleado_puesto}", ""])
        data.append(["Interes Anual: 5%", "Interes Mensual: 0.417%"])
        data.append([f"Monto acreditado: {prestamo.prestamo_cantidad}", f"Plazo: {prestamo.prestamo_meses} Meses"])
        total_pagar = prestamo.prestamo_mensualidad * prestamo.prestamo_meses
        data.append([f"Total a pagar: {total_pagar}", ""])
        data.append([f"Cuotas: {prestamo.prestamo_mensualidad}", ""])

        # Crear una tabla con los datos
        table = Table(data, colWidths=[300, 200])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(table)
        elements.append(Spacer(1, 12))
    
    elements.append(Spacer(1, 35))

    styles = getSampleStyleSheet()
    signature_text = "Firma Empleado:___________________________________________"
    signature_paragraph = Paragraph(signature_text, styles['Normal'])
    elements.append(signature_paragraph)
    
    doc.build(elements)
    return response

generar_pdf_prestamo.short_description = "Reporte PDF Prestamo"

def generar_pdf_liquidacion(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=detalle_liquidacion.pdf"

    # Crear un objeto PDF con reportlab
    doc = SimpleDocTemplate(response, pagesize=(letter))
    elements = []

    # Logo de la empresa
    logo = Image('pagos/img_logo/logo.png', width=50, height=50)
    elements.append(logo)
    elements.append(Spacer(1, 35))

    # Título del reporte
    title = "Detalle de Liquidación"
    title_paragraph = Paragraph(title, styles['Title'])
    elements.append(title_paragraph)
    elements.append(Spacer(1, 10))

    for liquidacion in queryset:
        data = []

        # Agregar información de la liquidación
        data.append(["Promedio Mensual:", liquidacion.liquidacion_sm])
        data.append(["Promedio Correspondiente:", liquidacion.liquidacion_sc])
        data.append(["Indemnización:", liquidacion.liquidacion_ind])
        data.append(["Aguinaldo Pendiente:", liquidacion.liquidacion_ag])
        data.append(["Bono 14 Pendiente:", liquidacion.liquidacion_bn])
        data.append(["Vacaciones Pendientes:", liquidacion.liquidacion_vc])
        data.append(["Total:", liquidacion.liquidacion_total])

        # Crear una tabla con los datos
        table = Table(data, colWidths=[150, 150])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER')
        ]))
        elements.append(table)
        elements.append(Spacer(1, 35))

        # Firma y sello (ajusta la posición según tus necesidades)
        firma_text = "Firma: ________________________________________"
        firma_paragraph = Paragraph(firma_text, styles['Normal'])
        elements.append(firma_paragraph)
        elements.append(Spacer(1, 25))
        # Cuadro de sello
        sello_table = Table([["Sello: "]], colWidths=[120], rowHeights=[120], hAlign='RIGHT')
        sello_table.setStyle(TableStyle([
            ('GRID', (0, 0), (0, 0), 1, colors.black)
        ]))
        elements.append(sello_table)

    doc.build(elements)
    return response

generar_pdf_liquidacion.short_description = "Generar PDF Liquidación"


class NominaAdmin(admin.ModelAdmin):
    actions = [generar_pdf_nomina]
    readonly_fields=('nomina_fecha', 'nomina_comision', 'nomina_bonificacion', 
                    'nomina_bono', 'nomina_aguinaldo', 'nomina_igss', 'nomina_tienda', 'nomina_prestamo',
                    'nomina_ausencia','nomina_neto','nomina_sueldo_base','nomina_aumento_total',
                    'nomina_extras_calculada','nomina_dobles_calculada',
                    'nomina_ingreso_total','nomina_descuento_total','nomina_aporte',)

    fields = [('nomina_fecha'),
              ('nomina_empleado_id', 'nomina_sueldo_base', 'nomina_aumento_total'),
              ('nomina_aporte'),
              ('nomina_extras','nomina_extras_calculada'),
              ('nomina_dobles','nomina_dobles_calculada'),
               ('nomina_ventas', 'nomina_comision'),
                ('nomina_piezas','nomina_bonificacion'), 
                ('nomina_igss','nomina_tienda','nomina_prestamo', 'nomina_ausencia'),
                ('nomina_ingreso_total','nomina_descuento_total', 'nomina_neto')
                ]
    list_display = ('nomina_id', 'nomina_empleado_id','nomina_ingreso_total',)
    list_display_links = ["nomina_empleado_id"]

class PrestamoAdmin(admin.ModelAdmin):
    actions = [generar_pdf_prestamo]
    readonly_fields=('prestamo_saldo','prestamo_mensualidad','prestamo_aporte',)
    list_display = ('prestamo_empleado_id', 'prestamo_saldo','prestamo_mensualidad', 'prestamo_aporte',)

class AporteAdmin(admin.ModelAdmin):
    readonly_fields=('aporte_acumulado',)
    list_display = ('aporte_empleado_id', 'aporte_cantidad', 'aporte_acumulado',)

class LiquidacionAdmin(admin.ModelAdmin):
    actions = [generar_pdf_liquidacion]

class IgssAdmin(admin.ModelAdmin):
    actions = [generar_pdf_igss]
    readonly_fields=('igss_cantidad',)
    list_display=('igss_empleado_id', 'igss_cantidad')

class Bono14Admin(admin.ModelAdmin):
     actions = [generar_pdf_bono14]
     readonly_fields=('bono_monto',)
     list_display=('bono_fecha' ,'bono_empleado_id', 'bono_monto')

class AguinaldoAdmin(admin.ModelAdmin):
    actions = [generar_pdf_aguinaldo]
    readonly_fields=('aguinaldo_monto',)
    list_display=('aguinaldo_fecha' ,'aguinaldo_empleado_id', 'aguinaldo_monto')

admin.site.register(Nomina, NominaAdmin)
admin.site.register(Aporte, AporteAdmin)
admin.site.register(Prestamo, PrestamoAdmin)
admin.site.register(Liquidacion, LiquidacionAdmin)
admin.site.register(Igss, IgssAdmin)
admin.site.register(Bono14, Bono14Admin)
admin.site.register(Aguinaldo, AguinaldoAdmin)