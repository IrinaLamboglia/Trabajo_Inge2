# views.py
from django.shortcuts import render, redirect
from core.models import Categoria

def agregar_categoria(request):
    error_message = None
    exito_message = "Alta exitosa"
    if request.method == 'POST':
        nombre_categoria = request.POST.get('nombre_categoria')
        if not Categoria.objects.filter(nombre=nombre_categoria).exists():
            categoria = Categoria.objects.create(nombre=nombre_categoria)
            # Actualizar la lista de productos (a implementar)
            return  render(request, 'agregar_categoria/aceptarCategoria.html', {'exito_message': exito_message})  # Redirigir a la página de inicio o a donde sea necesario
        else:
            error_message = "Alta fallida: Categoría existente"
    return render(request, 'agregar_categoria/aceptarCategoria.html', {'error_message': error_message})

def mostrar_categorias(request):
    # Obtener el valor del filtro de la solicitud GET
    filtro = request.GET.get('filtro')
    
    # Filtrar las categorías según el valor del filtro
    if filtro == 'activas':
        categorias = Categoria.objects.filter(estado=True)
        selected_option = 'activas'
    elif filtro == 'desactivadas':
        categorias = Categoria.objects.filter(estado=False)
        selected_option = 'desactivadas'
    else:
        categorias = Categoria.objects.all()
        selected_option = 'todas'
    
    return render(request, 'agregar_categoria/mostrarCategoria.html', {'categorias': categorias, 'selected_option': selected_option})
