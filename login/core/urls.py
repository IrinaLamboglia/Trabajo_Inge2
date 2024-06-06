"""login URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path 
from .views import home,products
from log_out.views import exit
#importo funcion exit
from . import views
from altaFilial.views import editar_filial,guardar_filial,listar_filiales,eliminar_filial
from editarPerfil.views import editar_ayudante
from agregarCategoria.views import agregar_categoria, mostrar_categorias
from bajaCategoria.views import  desactivar_categoria
from listarprod.views import mostrar_validacion, aceptar_publicacion, rechazar_publicacion, bloquear_usuario
from editarCategoria.views import editar_categoria

from django.urls import path
from aceptarTrueque.views import aceptar_trueque
from elegirTurno.views import elegir_turno
from confirmarTurno.views import confirmar_turno
from visualizarTrueques.views import visualizar_trueques_diarios
from efectivizar_trueques.views import efectivizar_trueques,aceptacion_trueque,penalizar_trueque,rechazar_efectivizacion
from rechazarTrueque.views import rechazar_trueque
from rechazarTurno.views import rechazar_turno
urlpatterns = [
    path('', home, name='home'),
    path('products/', products,name='products'),
    path('logout/',exit, name='exit'),
    path('accounts/login/', views.login_nuevo , name='login'),
    path('registro/', views.formularioreg, name='registro'),  
    path('login_ayudante/', views.procesar_clave, name="login_ayudante"),

   # path('bajaAyudante/',views.bajaAyudante,name='bajaAyudante'), #la tengo q hacer 
    path('sobreNosotros/',views.editar_sobre_nosotros,name='editarSobreNosotros'),
    path('bajaAyudante/',views.mostrarBaja,name='mostrarBaja'),
    #path('confirmar_salida/', confirmar_salida, name='confirmar_salida'),
    
    
    path('eliminarAyudante/<str:email>/', views.eliminarAyudante, name='eliminarAyudante'),
    # URL para la edición de perfil del ayudante
    path('editar_perfil/<int:id>/', editar_ayudante, name='editar_ayudante'),
   
    path('listado/bloqueadosListado/',views.listadoBloqueado, name='listadoBloqueados'),
    
    path('agregar_categoria/', agregar_categoria, name='agregar_categoria'),
    
    path('categoria/', mostrar_categorias, name='mostarCategoria'),

   # path('categoria/<int:categoria_id>/', bajar_categoria, name='bajarCategoria'),
    path('inicio/', home, name='inicio'),
    path('accounts/login/<email>/', views.recuperarCuenta, name='recuperarCuenta'), #no anda y no lo tenia q hacer lpm
    
    path('crearPublicacion/',views.crear_publicacion, name='crear_publicacion'),
    path('ver/<int:publicacion_id>/',views.ver_producto, name='ver_producto'),
    
    path('desbloquear/<str:email>/', views.desbloquearUsuario, name='desbloquear_usuario'),
    path('mis_publicaciones/', views.mis_publicaciones, name='mis_publicaciones'),
    
    #ESTO ES NUEVO
    path('eliminar_publicacion/<int:publicacion_id>/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('mostrarValidacion/', mostrar_validacion, name='mostrar_validacion'),
    path('aceptarPublicacion/<int:id>/', aceptar_publicacion, name='aceptar_publicacion'),
    path('rechazarPublicacion/<int:id>/', rechazar_publicacion, name='rechazar_publicacion'),
    path('bloquearUsuario/<int:id>/', bloquear_usuario, name='bloquear_usuario'),
    path('editar_filial/', editar_filial, name='editar_filial'),
    path('guardar_filial/', guardar_filial, name='guardar_filial'),
    path('listar_filiales/', listar_filiales, name='listar_filiales'),
    path('eliminar_filial/<int:filial_id>/', eliminar_filial, name='eliminar_filial'),
    
    path('mis_publicaciones1/', views.mis_publicaciones1, name='mis_publicaciones1'),

    path('categoria/desactivar/<int:categoria_id>/', desactivar_categoria, name='desactivar_categoria'),
    path('editar_categoria/<int:id>/', editar_categoria, name='editar_categoria'),

    path('check_email/', views.check_email, name='check_email'),
    path('misTrueques/', views.ver_misTrueques, name='misTrueques'),

    path('solicitar-trueque/<int:publicacion_id>/', views.solicitar_trueque, name='solicitar_trueque'),
    path('registrar-solicitud/<int:publicacion_objetivo_id>/', views.registrar_solicitud, name='registrar_solicitud'),
    path('filtro/misTrueques/',views.filtro_trueques,name='filtro_trueques'),

    path('aceptar_trueque/<int:solicitud_id>/', aceptar_trueque, name='aceptar_trueque'),
    path('elegir-turno/<int:trueque_id>/', elegir_turno, name='elegir_turno'),
    
    path('confirmar-turno/<int:trueque_id>/', confirmar_turno, name='confirmar_turno'),
    path('rechazar-turno/<int:trueque_id>/', rechazar_turno, name='rechazar_turno'),

    path('trueques_diarios/', visualizar_trueques_diarios, name='visualizar_trueques_diarios'),
    path('efectivizar_trueques/', efectivizar_trueques, name='efectivizar_trueque'),
    path('aceptacion_trueque/<int:id>', aceptacion_trueque, name='aceptacion_trueque'),
    path('rechazar_efectivizacion/<int:id>', rechazar_efectivizacion, name='rechazar_efectivizacion'),
    path('penalizar_trueque/<int:trueque_id>/', penalizar_trueque, name='penalizar_trueque'),
    path('rechazar_trueque/<int:solicitud_id>/', rechazar_trueque, name='rechazar_trueque'),
    
    
    path('eliminar_publicacion/<int:publicacion_id>/', views.eliminar_publicacion, name='eliminar_publicacion'),
    
    path('truequesAdmin/',views.trueques_realizados,name='trueques_realizados')
   
]
