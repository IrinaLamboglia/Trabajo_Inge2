# views.py
from django.shortcuts import render, get_object_or_404, redirect

from core.models import Categoria
from .CategoriaForm import CategoriaForm

def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    nombre_original = categoria.nombre  # Guarda el nombre original de la categoría
    
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('mostarCategoria')  # Redirigir a la página de categorías
   
    else:
        form = CategoriaForm(instance=categoria)
        
    return render(request, 'editarCategoria/editar_categoria.html', {'form': form, 'categoria': categoria, 'nombre_original': nombre_original})