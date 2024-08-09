from django.db import models
import sys
from importlib import reload
reload(sys)

"""
Modelo Rol
id		rol					es_admin	es_cliente		es_empleado		es_rrhh
1		ADMINISTRADOR		1			0				0				0
2		EMPLEADO			0			0				1				0
3		CLIENTE				0			1				0				0
4		RECURSOS HUMANOS	0			0				0				1
"""
class Rol(models.Model):
	rol = models.CharField(max_length = 60, verbose_name = 'Nombre del Rol')
	es_admin = models.BooleanField(default = False)
	es_cliente = models.BooleanField(default = False)
	es_empleado = models.BooleanField(default = False)
	es_rrhh = models.BooleanField(default = False)
	class Meta:
		verbose_name_plural = 'Roles'
	def __str__(self):
		return self.rol

#Modelo Empresa
class Empresa(models.Model):
	abreviatura = models.CharField(max_length = 50)
	empresa = models.CharField(max_length = 150)
	tipo_empresa = models.CharField(max_length = 100, verbose_name = 'Tipo de Empresa')
	historia = models.TextField()
	objetivo_general = models.TextField()
	vision = models.TextField()
	mision = models.TextField()
	telefono = models.CharField(max_length = 25, null = True, blank = True)
	celular = models.CharField(max_length = 25, null = True, blank = True)
	direccion = models.TextField()
	def __str__(self):
		return self.empresa

#Modelo Sucursal
class Sucursal(models.Model):
	rtn = models.CharField(max_length = 16, null = True, blank = True)
	sucursal = models.CharField(max_length = 60, verbose_name = 'Nombre de la Sucursal')
	celular = models.CharField(max_length = 25, null = True, blank = True)
	telefono = models.CharField(max_length = 25)
	correo = models.EmailField(null = True, blank = True)
	direccion = models.TextField(null = True, blank = True)
	estado = models.BooleanField(default = True)
	logo = models.ImageField(upload_to = 'logo_sucursal', max_length = 250, verbose_name = 'Imagen del Logo')
	altura_logo = models.IntegerField(default = 1, verbose_name = 'Altura del Logo')
	ancho_logo = models.IntegerField(default = 1, verbose_name = 'Ancho del Logo')
	logo_p = models.ImageField(upload_to = 'logo_sucursal_pequeno', max_length = 250, verbose_name = 'Imagen del Logo Pequeño')
	altura_logo_p = models.IntegerField(default = 1, verbose_name = 'Altura del Logo Pequeño')
	ancho_logo_p = models.IntegerField(default = 1, verbose_name = 'Ancho del Logo Pequeño')
	encabezado_reporte = models.ImageField(upload_to = 'encabezado_reporte', max_length = 250, verbose_name = 'Encabezado de los Reportes')
	altura_encabezado = models.IntegerField(default = 1, verbose_name = 'Altura del Encabezado')
	ancho_encabezado = models.IntegerField(default = 1, verbose_name = 'Ancho del Encabezado')
	pie_pagina_reporte = models.ImageField(upload_to = 'pie_pagina_reporte', max_length = 250, verbose_name = 'Pie de Página de los Reportes')
	altura_pie_pagina = models.IntegerField(default = 1, verbose_name = 'Altura del Pie de Página')
	ancho_pie_pagina = models.IntegerField(default = 1, verbose_name = 'Ancho del Pie de Página')
	color = models.CharField(max_length = 10, verbose_name = 'Color de la Sucursal')
	empresa = models.ForeignKey(Empresa, on_delete = models.CASCADE)
	class Meta:
		verbose_name_plural = 'Sucursales'
	def __str__(self):
		return self.sucursal

# altura_logo 			= 40	
# ancho_logo 			= 210	
# altura_logo_p 		= 40	
# ancho_logo_p 			= 40	
# altura_encabezado 	= 62	
# ancho_encabezado 		= 735	
# altura_pie_pagina 	= 55	
# ancho_pie_pagina 		= 735	
# color 				= #E5E7E9


#Modelo Sar
class Sar(models.Model):
	cai = models.CharField(max_length = 100, verbose_name = 'Código del Caí')
	inicial = models.CharField(max_length = 19, verbose_name = 'Inicio')
	final = models.CharField(max_length = 19)
	correlativo = models.IntegerField()
	estado = models.BooleanField(default = True)
	fecha_limite = models.DateField(verbose_name = 'Fecha Limite de Emisión')
	sucursal = models.ForeignKey(Sucursal, on_delete = models.CASCADE)
	class Meta:
		verbose_name_plural = 'Sar'
	def __str__(self):
		return "{} - Fecha Limite => {}" .format(self.cai, self.fecha_limite)

# Notario
class Notario(models.Model):
	num_identidad = models.CharField(max_length = 15, verbose_name = 'Numero de Identidad')
	nombre = models.CharField(max_length = 50)
	apellidos = models.CharField(max_length = 50)
	telefono = models.CharField(max_length = 25, null = True, blank = True)
	celular = models.CharField(max_length = 25)
	correo = models.EmailField(null = True, blank = True)
	direccion = models.TextField()

	@property
	def full_name(self):
		"Returns the person's full name."
		return '%s %s' % (self.nombre, self.apellidos)

	def __str__(self):
		return '{}' .format(self.full_name)

class Notario_Sucursal(models.Model):
	sucursal = models.ForeignKey(Sucursal, on_delete = models.CASCADE)
	notario = models.ForeignKey(Notario, on_delete = models.CASCADE)
	firma_notario = models.BooleanField(default = False)

	def __str__(self):
		return '{} -- {}' .format(self.sucursal, self.notario)
	class Meta:
		unique_together = ("sucursal", "notario",)
		verbose_name_plural = 'Notarios de Sucursales'


#Modelo Tipo_Dispositivo
class Tipo_Dispositivo(models.Model):
	dispositivo = models.CharField(max_length = 60, verbose_name = 'Nombre del Dispositivo')
	class Meta:
		verbose_name_plural = 'Tipos de Dispositivos'
	def __str__(self):
		return self.dispositivo
	
#Tipos de Dispositivos
#1 -- Computadora
#2 -- Dispositivo Móvil

#Modelo Admon_Empresa
class Admon_Empresa(models.Model):
    gerente = models.ForeignKey(to = 'empleados.Empleado', related_name = 'gerente_general_empresa', on_delete = models.CASCADE, verbose_name = 'Gerente de la Sucursal')
    recursos_humanos = models.ForeignKey(to = 'empleados.Empleado', related_name = 'rrhh_general_empresa', on_delete = models.CASCADE, verbose_name = 'Encargado de Recursos Humanos')
    contador = models.ForeignKey(to = 'empleados.Empleado', related_name = 'contador_general_empresa', on_delete = models.CASCADE, verbose_name = 'Contador General')
    it = models.ForeignKey(to = 'empleados.Empleado', related_name = 'it_general_empresa', on_delete = models.CASCADE, verbose_name = 'Jefe Informatica General')
    empresa = models.ForeignKey(Empresa, on_delete = models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'Administracion Empresa'
    def __str__(self):
        return "{} - {} {}" .format(self.empresa, self.gerente.primer_nombre, self.gerente.primer_apellido)

"""
id	tipo_notificacion
1	CREACIÓN SOLICITUD DE PRÉSTAMO
2	SUPERVISIÓN SOLICITUD DE PRÉSTAMO
3	SUPERVISIÓN DEL PRÉSTAMO POR CÓMITE
4	REALIZACIÓN DEL DESEMBOLSO DEL PRÉSTAMO
"""

#Modelo de Tipo_Notificacion_Correo
class Tipo_Notificacion_Correo(models.Model):
	tipo_notificacion = models.CharField(max_length = 100, verbose_name = 'Tipo de Notificacion')
	class Meta:
		verbose_name_plural = 'Tipos de Notificaciones por Correo'
	def __str__(self):
		return self.tipo_notificacion

#Modelo de Notificacion_Correo
class Notificacion_Correo(models.Model):
	tipo_notificacion = models.ForeignKey(Tipo_Notificacion_Correo, on_delete = models.CASCADE, verbose_name = 'Tipo de Notificacion por Correo')
	descripcion = models.TextField(verbose_name = 'Descripcion de la Notificacion', null = True, blank = True)
	sucursal = models.ForeignKey(Sucursal, on_delete = models.CASCADE)
	class Meta:
		verbose_name_plural = 'Notificaciones por Correo'
	def __str__(self):
		return self.tipo_notificacion.tipo_notificacion

#Modelo de Asignacion_Notificacion_Correo_Empleado
class Asignacion_Notificacion_Correo_Empleado(models.Model):
	empleado = models.ForeignKey(to = 'empleados.Empleado', on_delete = models.CASCADE)
	notificacion = models.ForeignKey(Notificacion_Correo, on_delete = models.CASCADE)
	usuario_empleado = models.IntegerField()

	def __str__(self):
		return '{} -- {}' .format(self.empleado, self.notificacion)
	class Meta:
		unique_together = ("empleado", "notificacion",)
		verbose_name_plural = 'Asignacion Notificacion por Correo a Empleado'

#Modelo de Asignacion_Gestores_Promotor
class Asignacion_Gestores_Promotor(models.Model):
	promotor = models.ForeignKey(to = 'empleados.Empleado', related_name = 'empleado_promotor', on_delete = models.CASCADE)
	gestor = models.ForeignKey(to = 'empleados.Empleado', related_name = 'empleado_gestor', on_delete = models.CASCADE)
	fecha_registro = models.DateTimeField(auto_now_add = True)
	usuario_promotor = models.IntegerField()
	usuario_registro = models.IntegerField()
	class Meta:
		verbose_name_plural = 'Asignaciones de Gestores a Promotor'
	def __str__(self):
		return "{} -- {}" .format(self.promotor.full_name, self.gestor.full_name)

#Modelo de Asignacion_Gestores_Desembolsador
class Asignacion_Gestores_Desembolsador(models.Model):
	desembolsador = models.ForeignKey(to = 'empleados.Empleado', related_name = 'empleado_d', on_delete = models.CASCADE)
	gestor = models.ForeignKey(to = 'empleados.Empleado', related_name = 'empleado_g', on_delete = models.CASCADE)
	fecha_registro = models.DateTimeField(auto_now_add = True)
	usuario_desembolsador = models.IntegerField()
	usuario_registro = models.IntegerField()
	class Meta:
		verbose_name_plural = 'Asignaciones de Gestores a Desembolsador'
	def __str__(self):
		return "{} -- {}" .format(self.desembolsador.full_name, self.gestor.full_name)

#Modelo de Asignacion_Ruta_Apoyo
class Asignacion_Ruta_Apoyo(models.Model):
	gestor_apoyo = models.ForeignKey(to = 'empleados.Empleado', related_name = 'empleado_gestor_apoyo', on_delete = models.CASCADE)
	gestor_ausente = models.ForeignKey(to = 'empleados.Empleado', related_name = 'empleado_gestor_ausente', on_delete = models.CASCADE)
	fecha_registro = models.DateTimeField(auto_now_add = True)
	usuario_gestor_apoyo = models.IntegerField()
	usuario_registro = models.IntegerField()
	class Meta:
		verbose_name_plural = 'Asignaciones de Rutas de Apoyo a Gestor'
	def __str__(self):
		return "{} -- {}" .format(self.gestor_apoyo.full_name, self.gestor_ausente.full_name)

#Modelo de Error_Excepcion
class Error_Excepcion(models.Model):
	descripcion_error = models.TextField()
	fecha_registro = models.DateTimeField(auto_now_add = True)
	sistema_id = models.IntegerField()
	aplicacion_id = models.IntegerField()
	nombre_area = models.CharField(max_length = 50)
	usuario_registro = models.IntegerField()

	solucion_error = models.TextField(null = True, blank = True)
	usuario_solucion = models.IntegerField(null = True, blank = True)
	class Meta:
		verbose_name_plural = 'Errores y Excepciones'
	def __str__(self):
		return "{} -- {}" .format(self.fecha_registro, self.usuario_registro)
