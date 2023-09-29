from django.shortcuts import render, HttpResponse


# Create your views here.

def home(request):
        return render (request, "NominaApp/home.html")


#cargar todos los productos ingresados en el panel de administracion 
 