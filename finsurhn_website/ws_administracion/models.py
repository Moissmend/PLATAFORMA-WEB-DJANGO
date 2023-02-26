from email.policy import default
from django.db import models


#Modelo Valores de la Empresa
class Valores_Empresa(models.Model):
    valor = models.CharField(max_length = 50)
    descripcion = models.TextField()
    
    class Meta:
        verbose_name_plural = 'Valores de la Empresa'
    def __str__(self):
        return self.valor

class Redes_Sociales(models.Model):
    nombre = models.CharField(max_length = 15)
    imagen = models.ImageField(verbose_name = "Imagen", upload_to="finsurhn_ws/redes_sociales", max_length = 250, null = True, blank = True)
    link = models.CharField(max_length = 100)
    orden = models.IntegerField(default = 1, verbose_name = 'Orden de las redes sociales')
    estado = models.BooleanField(default = True, verbose_name = 'Estado de la Red Social')
    
    class Meta:
        ordering = ['orden']
        verbose_name_plural = 'Redes Sociales de la Empresa'
        
    def __str__(self):
        return '{}' .format(self.link)

class Galeria_Empresa(models.Model):
    contenido = models.TextField(verbose_name = 'Contenido de la Imagen')
    orden = models.IntegerField(default = 1, verbose_name = 'Orden de la Imagen')
    imagen = models.ImageField(verbose_name ="Imagen_Galeria", upload_to = "finsurhn_ws/galeria", max_length = 250, null = True, blank = True)
    estado = models.BooleanField(default = True, verbose_name = 'Estado de la Imagen')
    
    class Meta:
        ordering = ['orden']
        verbose_name_plural = 'Galería de la Empresa'
        
        
    def __str__(self):
        return '{}' .format(self.contenido)
    

        
class Responsabilidad_Social(models.Model):
    nombre = models.CharField(max_length = 60 )
    descripcion = models.TextField(verbose_name = 'Descripción', max_length = 400)
    estado = models.BooleanField(default = True, verbose_name = 'Estado de la Imagen')
    imagen = models.ImageField(upload_to = "finsurhn_ws/responsabilidad_social", max_length = 250)
    fecha_realizacion = models.DateField()
    fecha_creacion = models.DateField(auto_now_add=True, verbose_name='Fecha de creación')
    
    class Meta:
        ordering = ['fecha_creacion']
        verbose_name_plural = 'Responsabilidad Social'
        
    def __str__(self):
        return '{} - {}' .format(self.nombre, self.fecha_realizacion)
    
    
class Informacion_Empleo(models.Model):
    idcargo = models.IntegerField()
    descripcion = models.TextField(max_length = 300)
    num_vacantes = models.IntegerField()
    ciudad = models.CharField(max_length = 50)
    orden = models.IntegerField(default = 1, verbose_name = 'Orden de Empleo')
    imagen = models.ImageField(upload_to = "finsurhn_ws/informacion_empleo", max_length = 250, null = True, blank = True)
    estado = models.BooleanField(default = True, verbose_name = 'Estado de la Imagen')
    
    class Meta:
        ordering = ['orden']
        verbose_name_plural = 'Información de Empleo'
        
    def __str__(self):
        return '{}' .format(self.descripcion)
    

class Sala_Videos(models.Model):
    nombre = models.CharField(max_length = 60 )
    link = models.TextField()
    estado = models.BooleanField(default = True, verbose_name = 'Estado de la Imagen')
    imagen = models.ImageField(upload_to = "finsurhn_ws/sala_videos", max_length = 250)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    
    class Meta:
        ordering = ['fecha_creacion']
        verbose_name_plural = 'Sala de Videos'
        
    def __str__(self):
        return '{} - {}' .format(self.nombre, self.link)
    
    
class Productos_Servicios(models.Model):
    nombre  = models.CharField(max_length = 50, blank = False, null = False, verbose_name = 'Nombre del producto o servicio')
    descripcion = models.TextField(max_length = 350)
    imagen = models.ImageField(upload_to = "finsurhn_ws/productos_servicios", max_length = 250)
    estado = models.BooleanField( default = True, choices = ((True, 'Activo'),(False, 'Inactivo')) )
    es_producto = models.BooleanField( default = True, choices = ((True, 'Producto'),(False, 'Servicio')), verbose_name = 'Es un producto')
    
    class Meta:
        verbose_name_plural = 'Productos y Servicios Financieros'
    
    def __str__(self):
        return '{}'.format(self.nombre)

    
class Detalle_Productos_Servicios(models.Model):
    requisitos = models.TextField()
    producto_servicio = models.ForeignKey(Productos_Servicios, on_delete = models.CASCADE, related_name="getDetalleProductosServicios") 
    frecuencia_pago = models.IntegerField()

    class Meta:
        unique_together = ("producto_servicio", "frecuencia_pago",)
        verbose_name_plural = 'Detalle de los productos y servicios'
        
    def __str__(self):
        return 'Detalle: {} | Producto: {} -> {}' .format(self.id, self.producto_servicio.id , self.producto_servicio.nombre)
    
    
# Empresa y Sectores van a ir a la DB Principal # Las imagenes irán en Base 64    
# Empresa -> Movido
# Cargo -> Movido
# Mora -> Movido
# Sectores -> Movido
# FrecuenciaPagos -- Movido