from decimal import DefaultContext
from django.db import models
from django.contrib.auth.models import User
from catalogos.models import *
from configuraciones.models import *
from empleados.models import *
import sys
from importlib import reload
reload(sys)


#Modelo de Tipo_Zona
class Tipo_Zona(models.Model):
	tipo_zona = UpperCaseCharField(max_length = 50, verbose_name = 'Tipo de Zona')
	sucursal = models.ForeignKey(Sucursal, on_delete = models.CASCADE)
	class Meta:
		verbose_name_plural = 'Tipos Zonas'
	def __str__(self):
		return self.tipo_zona


#Modelo de Tipo_Empleo
class Tipo_Empleo(models.Model):
	tipo_empleo = models.CharField(max_length = 50, verbose_name = 'Tipo de Empleo')
	class Meta:
		verbose_name_plural = 'Tipos de Empleo'
	def __str__(self):
		return self.tipo_empleo

#Modelo de Tipo_Cliente
class Tipo_Cliente(models.Model):
	abreviatura = models.CharField(max_length = 20)
	tipo_cliente = models.CharField(max_length = 50, verbose_name = 'Tipo de Cliente')
	class Meta:
		verbose_name_plural = 'Tipos de Clientes'
	def __str__(self):
		return self.tipo_cliente

#Modelo de Cliente
class Cliente(models.Model):
	codigo = models.IntegerField(default = 0, verbose_name = 'Código Correlativo Cliente')
	rtn = models.CharField(max_length = 16, null = True, blank = True)
	num_identidad = models.CharField(max_length = 15, verbose_name = 'Numero de Identidad')
	primer_nombre = UpperCaseCharField(max_length = 30) 
	segundo_nombre = UpperCaseCharField(max_length = 30, null = True, blank = True)
	primer_apellido = UpperCaseCharField(max_length = 30)
	segundo_apellido = UpperCaseCharField(max_length = 30, null = True, blank = True)
	fecha_nac = models.DateField(verbose_name = 'Fecha de Nacimiento')
	fecha_registro = models.DateTimeField(auto_now_add = True)
	direccion = models.TextField()
	direccion_referencia = models.TextField(verbose_name = 'Dirección de Referencia', null = True, blank = True)
	telefono = models.CharField(max_length = 25, null = True, blank = True)
	celular = models.CharField(max_length = 25)
	correo = models.EmailField(null = True, blank = True)
	datos_adicionales = models.TextField(null = True, blank = True)
	num_pasaporte = models.CharField(max_length = 30, null = True, blank = True, verbose_name = 'Número del Pasaporte')
	carnet_residencia = models.CharField(max_length = 40, null = True, blank = True, verbose_name = 'Carnet de Residencia')
	fecha_expiracion_pasaporte = models.DateField(null = True, blank = True)
	sabe_leer = models.BooleanField(default = False)
	sabe_escribir = models.BooleanField(default = False)
	sabe_firmar = models.BooleanField(default = False)
	estado_civil = models.ForeignKey(Estado_Civil, on_delete = models.CASCADE)
	rol = models.ForeignKey(Rol, on_delete = models.CASCADE)
	sucursal = models.ForeignKey(Sucursal, on_delete = models.CASCADE)
	actividad_economica = models.ForeignKey(ActividadesEconomicas, on_delete = models.CASCADE)
	sector = models.ForeignKey(Sectores, on_delete = models.CASCADE)
	tipo_vivienda = models.ForeignKey(Tipo_Vivienda, on_delete = models.CASCADE, verbose_name = 'Tipo de Vivienda')
	propietario_vivienda = models.CharField(max_length = 50, null = True, blank = True, verbose_name = 'Propietario de la Vivienda')
	nivel_educativo = models.ForeignKey(Nivel_Educativo, on_delete = models.CASCADE)
	num_dependientes = models.IntegerField(default = 0, verbose_name = 'Número de Dependientes')
	num_hijos = models.IntegerField(default = 0, verbose_name = 'Número de Hijos')
	edades_dependientes = models.CharField(max_length = 30, null = True, blank = True)
	antiguedad_domiciliaria = models.CharField(max_length = 30)
	identidad_beneficiario_seguro = models.CharField(max_length = 15, null = True, blank = True)
	nombre_beneficiario_seguro = UpperCaseCharField(max_length = 30, null = True, blank = True)
	parentesco_beneficiario_seguro = models.CharField(max_length = 30, null = True, blank = True)
	latitude = models.FloatField(default = 0.00, blank = True, null = True)
	longitude = models.FloatField(default = 0.00, blank = True, null = True)
	genero = models.ForeignKey(Genero, on_delete = models.CASCADE)
	tipo_empleo = models.ForeignKey(Tipo_Empleo, on_delete = models.CASCADE, verbose_name = 'Tipo de Empleo')
	conyuge = models.ForeignKey(Conyuge, null = True, blank = True, on_delete = models.CASCADE)
	negocio = models.ForeignKey(Negocio, null = True, blank = True, on_delete = models.CASCADE)
	empresa_cliente = models.ForeignKey(Empresa_Cliente, null = True, blank = True, on_delete = models.CASCADE, verbose_name = 'Empresa del Cliente')
	remesa = models.ForeignKey(Datos_Remesa, null = True, blank = True, on_delete = models.CASCADE, verbose_name = 'Remesa del Cliente')
	socializacion = models.ManyToManyField(Tipo_Socializacion)
	tipo_persona = models.ForeignKey(Tipo_Persona, on_delete = models.CASCADE, verbose_name = 'Tipo de Persona')
	tipo_cliente = models.ForeignKey(Tipo_Cliente, on_delete = models.CASCADE, verbose_name = 'Tipo de Cliente')
	pais_origen = models.ForeignKey(Pais, related_name = 'pais_origen', on_delete = models.CASCADE, verbose_name = 'País de Origen')
	pais_residencia = models.ForeignKey(Pais, on_delete = models.CASCADE, verbose_name = 'País de Residencia')
	departamento = models.ForeignKey(Departamentos, on_delete = models.CASCADE)
	municipio = models.ForeignKey(Municipios, on_delete = models.CASCADE)
	caserio = models.ForeignKey(MunicipioCaserios, null = True, blank = True, on_delete = models.CASCADE)
	barrio_colonia = models.ForeignKey(MunicipioBarrioColonia, null = True, blank = True, on_delete = models.CASCADE, verbose_name = 'Barrio o Colonia')
	aldea = models.ForeignKey(MunicipioAldeas, null = True, blank = True, on_delete = models.CASCADE)
	caserio_aldea = models.ForeignKey(AldeaCaserio, null = True, blank = True, on_delete = models.CASCADE, verbose_name = 'Caserío de una Aldea')
	barrio_colonia_aldea = models.ForeignKey(AldeaBarriosColonia, null = True, blank = True, on_delete = models.CASCADE, verbose_name = 'Barrio o Colonia de una Aldea')
	caserio_barrio = models.ForeignKey(CaserioBarrio, null = True, blank = True, on_delete = models.CASCADE, verbose_name = 'Barrio o Colonia de un Caserío')
	tipo_zona = models.ForeignKey(Tipo_Zona, on_delete = models.CASCADE, verbose_name = 'Tipo de Zona')
	imagen = models.ImageField(upload_to = 'imagen_cliente_perfil', max_length = 250, null = True, blank = True)
	firma_cliente = models.ImageField(upload_to = 'firma_cliente', max_length = 250, null = True, blank = True)
	usuario = models.IntegerField(null = True, blank = True, verbose_name = 'Usuario del Cliente')
	usuario_registro = models.IntegerField()
	estado_cliente = models.ForeignKey(Estado_Sujeto, null = True, blank = True, on_delete = models.CASCADE, verbose_name = 'Estado del Cliente')
	es_recurrente = models.BooleanField(default = False, verbose_name = 'Cliente Recurrente')
	es_aval = models.BooleanField(default = False, verbose_name = 'Es Aval')
	num_ciclos = models.IntegerField(default = 0, verbose_name = 'Número de Ciclos')

	@property
	def full_name(self):
		"Return, el Nombre Completo del Sujeto"
		return '%s%s%s%s' % (self.primer_nombre + ' ', self.segundo_nombre + ' ' if self.segundo_nombre is not None else '', self.primer_apellido + ' ', self.segundo_apellido if self.segundo_apellido is not None else '')
	@property
	def nombre_id_guiones(self):
		"Return, el Primer Nombre, Primer Apellido, Código separado con guiones"
		return '%s_%s_%s' % (self.primer_nombre, self.primer_apellido, self.codigo)
	def __str__(self):
		return "{} -- {}, {}" .format(self.num_identidad, self.full_name, self.sucursal)


#Modelo de Cambio_Estado_Cliente
class Cambio_Estado_Cliente(models.Model):
	estado_cliente = models.ForeignKey(Estado_Sujeto, on_delete = models.CASCADE, verbose_name = 'Estado del Cliente')
	descripcion = models.TextField()
	fecha_registro = models.DateTimeField()
	cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)
	usuario_registro = models.IntegerField()
	class Meta:
		verbose_name_plural = 'Cambios de Estado del Cliente'
	def __str__(self):
		return "{}" .format(self.estado_cliente.estado)


"""
id	tipo_imagen						cantidad_imagen		altura_imagen	anchura_imagen
1	# IDENTIDAD						2					400				550
2	ANTECEDENTES PENALES			1					900				450
3	ANTECEDENTES POLICIALES			1					900				450
4	CASA							5					650				700
5	CONSTANCIA DE TRABAJO			1					900				450
6	CROQUIS DE LA CASA				1					650				700
7	CROQUIS DEL NEGOCIO				1					650				700
8	CROQUIS LUGAR DE TRABAJO		1					650				700
9	NEGOCIO							5					650				700
10	PERMISO DE OPERACIÓN 			1					650				700
11	PRESTAMOS DE LA COMPETENCIA		5					650				700
12	RECIBO SERVICIO PÚBLICO			3					900				450
13	RTN								2					400				550
"""
#Modelo de Tipo_Imagen_Cliente
class Tipo_Imagen_Cliente(models.Model):
	tipo_imagen = models.CharField(max_length = 50, verbose_name = 'Tipo de Imagen')
	cantidad_imagen = models.IntegerField(default = 0, verbose_name = 'Cantidad de Imagenes')
	altura_imagen = models.IntegerField(default = 0, verbose_name = 'Altura de la Imagen')
	anchura_imagen = models.IntegerField(default = 0, verbose_name = 'Anchura de la Imagen')
	class Meta:
		verbose_name_plural = 'Tipos de Imagenes del Cliente'
	def __str__(self):
		return self.tipo_imagen


#Modelo de Imagen_Cliente
class Imagen_Cliente(models.Model):
	imagen = models.ImageField(upload_to = 'imagenes_cliente_empleado', max_length = 250)
	cliente = models.ForeignKey(Cliente, null = True, blank = True, on_delete = models.CASCADE)
	empleado = models.ForeignKey(Empleado, null = True, blank = True, on_delete = models.CASCADE)
	tipo_imagen = models.ForeignKey(Tipo_Imagen_Cliente, on_delete = models.CASCADE, verbose_name = 'Tipo de Imagen')
	class Meta:
		verbose_name_plural = 'Imagenes del Cliente'
	def __str__(self):
		return "{}" .format(self.tipo_imagen)


#Modelo de Asignacion_Clientes_Empleado
class Asignacion_Clientes_Empleado(models.Model):
	cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)
	empleado = models.ForeignKey(Empleado, on_delete = models.CASCADE)
	fecha_registro = models.DateTimeField(auto_now_add = True)
	usuario_empleado = models.IntegerField()
	usuario_registro = models.IntegerField()
	class Meta:
		verbose_name_plural = 'Asignaciones de Clientes a Empleado'
	def __str__(self):
		return "{} -- {}" .format(self.cliente.full_name, self.empleado.full_name)


#Modelo de Garantia_Hipotecaria
class Garantia_Hipotecaria(models.Model):
	duenio_propiedad = UpperCaseCharField(max_length = 100)
	co_duenio_propiedad = UpperCaseCharField(max_length = 100, null = True, blank = True)
	valor_avaluo = models.FloatField(default = 0)
	valor_comercial = models.FloatField(default = 0)
	tipo_inmueble = models.ForeignKey(Tipo_Inmueble, on_delete = models.CASCADE)
	condicion_inmueble = models.ForeignKey(Condicion_Inmueble, on_delete = models.CASCADE)
	direccion = models.TextField()
	direccion_referencia = models.TextField()
	otros_datos = models.TextField(null = True, blank = True)
	cliente = models.ForeignKey(Cliente, null = True, blank = True, on_delete = models.CASCADE)
	empleado = models.ForeignKey(Empleado, null = True, blank = True, on_delete = models.CASCADE)
	estado = models.BooleanField(default = True)
	fecha_registro = models.DateTimeField(auto_now_add = True)
	usuario_registro = models.IntegerField()
	class Meta:
		verbose_name_plural = 'Garantias Hipotecarias'
	def __str__(self):
		return "{}" .format(self.tipo_inmueble)

#Modelo de Garantia_Menaje_Casa
class Garantia_Menaje_Casa(models.Model):
	duenio_propiedad = UpperCaseCharField(max_length = 100)
	valor_avaluo = models.FloatField(default = 0)
	valor_comercial = models.FloatField(default = 0)
	num_serie = models.CharField(max_length = 50, null = True, blank = True)
	tipo_menaje_casa = models.ForeignKey(Tipo_Menaje_Casa, on_delete = models.CASCADE)
	color = models.ForeignKey(Color, on_delete = models.CASCADE)
	marca = models.ForeignKey(Marca, on_delete = models.CASCADE)
	modelo = models.ForeignKey(Modelo, on_delete = models.CASCADE)
	otros_datos = models.TextField(null = True, blank = True)
	cliente = models.ForeignKey(Cliente, null = True, blank = True, on_delete = models.CASCADE)
	empleado = models.ForeignKey(Empleado, null = True, blank = True, on_delete = models.CASCADE)
	estado = models.BooleanField(default = True)
	fecha_registro = models.DateTimeField(auto_now_add = True)
	usuario_registro = models.IntegerField()
	class Meta:
		verbose_name_plural = 'Garantias Menaje de Casa'
	def __str__(self):
		return "{}" .format(self.tipo_menaje_casa)

#Modelo de Garantia_Vehiculo
class Garantia_Vehiculo(models.Model):
	duenio_propiedad = UpperCaseCharField(max_length = 100)
	valor_avaluo = models.FloatField(default = 0)
	valor_comercial = models.FloatField(default = 0)
	anio = models.IntegerField(default = 0)
	numero_asientos = models.IntegerField(default = 0)
	num_placa = models.CharField(max_length = 50)
	num_matricula = models.CharField(max_length = 50)
	num_chasis = models.CharField(max_length = 50)
	motor = models.CharField(max_length = 50)
	tipo_vehiculo = models.ForeignKey(Tipo_Vehiculo, on_delete = models.CASCADE)
	tipo_transmision = models.ForeignKey(Tipo_Transmision_Vehiculo, on_delete = models.CASCADE)
	tipo_combustible = models.ForeignKey(Tipo_Combustible_Vehiculo, on_delete = models.CASCADE)
	color = models.ForeignKey(Color, on_delete = models.CASCADE)
	marca = models.ForeignKey(Marca, on_delete = models.CASCADE)
	modelo = models.ForeignKey(Modelo, on_delete = models.CASCADE)
	otros_datos = models.TextField(null = True, blank = True)
	cliente = models.ForeignKey(Cliente, null = True, blank = True, on_delete = models.CASCADE)
	empleado = models.ForeignKey(Empleado, null = True, blank = True, on_delete = models.CASCADE)
	estado = models.BooleanField(default = True)
	fecha_registro = models.DateTimeField(auto_now_add = True)
	usuario_registro = models.IntegerField()
	class Meta:
		verbose_name_plural = 'Garantias Vehículos'
	def __str__(self):
		return "{}" .format(self.tipo_vehiculo)

#Modelo de Imagen_Garantia
class Imagen_Garantia(models.Model):
	garantia_hipotecaria = models.ForeignKey(Garantia_Hipotecaria, on_delete = models.CASCADE, null = True, blank = True)
	garantia_menaje_casa = models.ForeignKey(Garantia_Menaje_Casa, on_delete = models.CASCADE, null = True, blank = True)
	garantia_vehiculo = models.ForeignKey(Garantia_Vehiculo, on_delete = models.CASCADE, null = True, blank = True)
	imagen = models.ImageField(upload_to = 'imagenes_garantias', max_length = 250)
	fecha_registro = models.DateTimeField(auto_now_add = True)
	usuario_registro = models.IntegerField()
	
	class Meta:
		verbose_name_plural = 'Imágenes Garantias'
	def __str__(self):
		return "{} -- {}" .format(self.fecha_registro, self.usuario_registro)

