from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import secrets


# Create your models here.



class FailedLoginAttempt(models.Model):
    email = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)





class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    dni = models.CharField(max_length=10)
    telefono = models.CharField(max_length=10)
    contraseña = models.CharField(max_length=128, validators=[MinLengthValidator(6)], default='valor_predeterminado')  # Campo para almacenar la contraseña cifrada
    last_login = models.DateTimeField(verbose_name='last login', blank=True, null=True)
    tipo= models.CharField(max_length=30, default="")
    puntuacion = models.DecimalField(max_digits=10, decimal_places=2)

    # Campo filial solo para ayudantes
    filial_nombre = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.tipo != "ayudante":
            self.filial = None  # Resetear el valor de filial si el tipo no es ayudante
        super().save(*args, **kwargs)



class UsuarioBloqueado(models.Model):
    email= models.EmailField(unique=True)


class porDesbloquear(models.Model):
    email= models.EmailField(unique=True)  
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre



class Publicacion(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=400)
    nuevo = models.BooleanField(default=True)
    estado = models.BooleanField(default=True)
    estadoCategoria = models.BooleanField(default=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=True)
    imagen = models.ImageField(upload_to='media/publicaciones/', null=True, blank=True)
    trueque = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

email= models.EmailField(unique=True)


class Filial(models.Model):
    ayudante = models.ForeignKey(Usuario, on_delete=models.CASCADE,null=True)
    nombre = models.CharField(max_length=20)
    latitud = models.FloatField()
    longitud = models.FloatField()

class Turno(models.Model):
    fecha = models.DateField()
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)
    cupo_maximo = models.IntegerField(default=50)
    cupos_disponibles = models.IntegerField()
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.cupos_disponibles = self.cupo_maximo
        super(Turno, self).save(*args, **kwargs)

class Trueque(models.Model):
    solicitante = models.ForeignKey(Usuario, related_name='solicitante', on_delete=models.CASCADE)
    receptor = models.ForeignKey(Usuario, related_name='receptor', on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.SET_NULL, null=True, blank=True)
    filial = models.ForeignKey(Filial, on_delete=models.SET_NULL, null=True, blank=True)
    aceptado = models.BooleanField(default=False)
    fecha_efectivizacion = models.DateTimeField(null=True, blank=True) 
    codigo_confirmacion_solicitante = models.CharField(max_length=10, blank=True, null=True)
    codigo_confirmacion_receptor = models.CharField(max_length=10, blank=True, null=True)
    token = models.CharField(max_length=100, unique=True, default=secrets.token_urlsafe)
    confirmado = models.BooleanField(default=False)
    
    def generar_codigos_confirmacion(self):
        self.codigo_confirmacion_solicitante = secrets.token_hex(5)  # Genera un código aleatorio de 10 caracteres hexadecimales
        self.codigo_confirmacion_receptor = secrets.token_hex(5)  # Genera un segundo código aleatorio
        self.save()
    
    def generar_token(self):
        self.token = secrets.token_hex(16)
        self.save()


class Solicitud(models.Model):
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='solicitudes')
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    estado = models.BooleanField(default=False)
    publicacionOfrecida = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='ofrecimientos')
    rechazado = models.BooleanField(default=False)  # ESTO SE BORRA
    realizado= models.BooleanField(default=False)
  

    def rechazar(self):
        self.realizado = True
        self.save()
    
    def __str__(self):
        return f"{self.solicitante} solicita {self.publicacion}"
    
    def aceptar(self):
        self.estado = True
        self.publicacion.trueque = True
        self.publicacionOfrecida.trueque = True
        self.publicacion.save()
        self.publicacionOfrecida.save()
        self.save()  
    