# views.py
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from core.models import Filial
from django.views.decorators.csrf import csrf_exempt






def editar_filial(request):
    filiales = Filial.objects.all()

    return render(request, 'altaFilial/editar_filial.html',{'filiales':filiales})

@csrf_exempt
def guardar_filial(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nombre = data.get('nombre')
        latitud = data.get('latitud')
        longitud = data.get('longitud')

        if (nombre is not None and latitud is not None and longitud is not None):
            Filial.objects.create(ayudante=None,nombre=nombre,latitud=latitud,longitud=longitud)
            return JsonResponse({'message': 'Filial creada exitosamente!'})
        else:
            return JsonResponse({'error': 'Datos incompletos'}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)



def listar_filiales(request):
    if request.method == 'GET':
        filiales = Filial.objects.all()
        filial_list = []
        for filial in filiales:
            filial_list.append({
                'nombre': filial.nombre,
                'latitud': filial.latitud,
                'longitud': filial.longitud,
                'ayudante': filial.ayudante.nombre if filial.ayudante else None
            })
        return JsonResponse(filial_list, safe=False)
    
@csrf_exempt
def eliminar_filial(request, filial_id):  # Cambiar el nombre del argumento xq no me funciona
    if request.method == 'POST': 
        try:
            print("entra al try")
            filial = Filial.objects.get(pk=filial_id)

            if filial.ayudante:
                mensaje = 'No se puede eliminar la filial porque tiene un ayudante asignado.'
                return JsonResponse({'error': mensaje}, status=400) 
    
            filial.delete()
            mensaje = 'La filial ha sido eliminada correctamente.'
            return JsonResponse({'message': mensaje}, status=200)
        except Exception as e:
            mensaje = f'Se levantó la excepción: {str(e)}'
            return JsonResponse({'error': mensaje}, status=404)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
