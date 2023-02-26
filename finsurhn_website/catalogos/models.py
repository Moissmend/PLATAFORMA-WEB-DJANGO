from email.policy import default
from django.db import models
from configuraciones.models import *
from django.contrib.auth.models import *
import sys
from importlib import reload
reload(sys)

class UpperCaseCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(UpperCaseCharField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if value:
            value = value.upper()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(UpperCaseCharField, self).pre_save(model_instance, add)

class Pais(models.Model):
	descripcion = UpperCaseCharField(max_length = 100, verbose_name = 'Nombre del País')
	abreviatura_nacionalidad = UpperCaseCharField(max_length = 10, verbose_name = 'Abreviatura del País')
	nacionalidad = UpperCaseCharField(max_length = 100, verbose_name = 'Nacionalidad del País')
	estado = models.BooleanField(default = True, verbose_name = 'Estado del País')
	class Meta:
		verbose_name_plural = 'Países'

	def __str__(self):
		return self.descripcion

class Departamentos(models.Model):
	codigo = models.CharField(max_length = 20, verbose_name = 'Código del Departamento')
	descripcion_departamento = UpperCaseCharField(max_length = 100, verbose_name = 'Nombre del Departamento')
	pais = models.ForeignKey(Pais, on_delete = models.CASCADE, verbose_name = 'País del Departamento')
	estado = models.BooleanField(default = True, verbose_name = 'Estado del Departamento')
	class Meta:
		verbose_name_plural = 'Departamentos'

	def __str__(self):
		return '{}'.format(self.descripcion_departamento)

class Municipios(models.Model):
	codigo = models.CharField(max_length = 20, verbose_name = 'Código del Municipio')
	descripcion_municipio = UpperCaseCharField(max_length = 100, verbose_name = 'Nombre del Municipio')
	departamento = models.ForeignKey(Departamentos, on_delete = models.CASCADE, verbose_name = 'Departamento del Municipio')
	estado = models.BooleanField(default = True, verbose_name = 'Estado del Municipio')
	class Meta:
		verbose_name_plural = 'Municipios'
	
	def __str__(self):
		return '{}'.format(self.descripcion_municipio)

class MunicipioAldeas(models.Model):
	descripcion_aldea = UpperCaseCharField(max_length = 100, verbose_name = 'Nombre de la Aldea')
	municipio = models.ForeignKey(Municipios, on_delete = models.CASCADE, verbose_name = 'Municipio de la Aldea')
	estado = models.BooleanField(default = True, verbose_name = 'Estado de la Aldea')
	class Meta:
		verbose_name_plural = 'Municipio --> Aldeas'
	
	def __str__(self):
		return '{}'.format(self.descripcion_aldea)

class MunicipioCaserios(models.Model):
	descripcion_caserio = UpperCaseCharField(max_length = 100, verbose_name = 'Nombre del Caserío')
	municipio = models.ForeignKey(Municipios, on_delete = models.CASCADE, verbose_name = 'Municipio del Caserío')
	estado = models.BooleanField(default = True, verbose_name = 'Estado del Caserío')
	class Meta:
		verbose_name_plural = 'Municipio --> Caserios'
	
	def __str__(self):
		return '{}'.format(self.descripcion_caserio)

class MunicipioBarrioColonia(models.Model):
	descripcion_comunidades = UpperCaseCharField(max_length = 100, verbose_name = 'Nombre del Barrio o Colonia')
	municipio = models.ForeignKey(Municipios, on_delete = models.CASCADE, verbose_name = 'Municipio del Barrio o Colonia')
	estado = models.BooleanField(default = True, verbose_name = 'Estado del Barrio o Colonia')
	class Meta:
		verbose_name_plural = 'Municipio --> Barrios o Colonias'
	def __str__(self):
		return '{}'.format(self.descripcion_comunidades)

class AldeaCaserio(models.Model):
	descripcion_aldea = UpperCaseCharField(max_length = 100, verbose_name = 'Nombre del Caserío')
	aldea = models.ForeignKey(MunicipioAldeas, on_delete = models.CASCADE, verbose_name = 'Aldea del Caserío')
	estado = models.BooleanField(default = True, verbose_name = 'Estado del Caserío')
	class Meta:
		verbose_name_plural = 'Aldea --> Caserios'
	def __str__(self):
		return '{} -- {} '.format(self.descripcion_aldea, self.aldea.descripcion_aldea)

class AldeaBarriosColonia(models.Model):
	descripcion_barrios = UpperCaseCharField(max_length = 100, verbose_name = 'Nombre del Barrio o Colonia')
	aldea = models.ForeignKey(MunicipioAldeas, on_delete = models.CASCADE, verbose_name = 'Aldea del Barrio o Colonia')
	estado = models.BooleanField(default = True, verbose_name = 'Estado del Barrio o Colonia')
	class Meta:
		verbose_name_plural = 'Aldea --> Barrios o Colonias'
	def __str__(self):
		return '{} -- {} '.format(self.descripcion_barrios, self.aldea.descripcion_aldea)


class CaserioBarrio(models.Model):
	descripcion_barrio = UpperCaseCharField(max_length = 100, verbose_name = 'Nombre del Barrio o Colonia')
	caserio = models.ForeignKey(MunicipioCaserios, on_delete = models.CASCADE, verbose_name = 'Caserío del Barrio o Colonia')
	estado = models.BooleanField(default = True, verbose_name = 'Estado del Barrio o Colonia')
	class Meta:
		verbose_name_plural = 'Caserio --> Barrios'
	def __str__(self):
		return '{} -- {} '.format(self.descripcion_barrio, self.caserio.descripcion_caserio)


"""
id	descripcion_garantia	estado		es_fiduciaria		es_hipotecaria		es_menaje_casa		es_vehiculo
1	FIDUCIARIAS				1			1					0					0					0
2	HIPOTECARIAS			1			0					1					0					0
3	MENAJE DE CASA			1			0					0					1					0
4	MIXTOS					1			1					1					1					1
5	VEHÍCULOS				1			0					0					0					1
"""
class Garantia(models.Model):
	descripcion_garantia = models.CharField(max_length = 100, blank = False, null = False, verbose_name = 'Nombre de la Garantía')
	estado = models.BooleanField(default = True, verbose_name = 'Estado de la Garantía')
	es_fiduciaria = models.BooleanField(default = False, verbose_name = 'es Fiduciaria')
	es_hipotecaria = models.BooleanField(default = False, verbose_name = 'es Hipotecaria')
	es_menaje_casa = models.BooleanField(default = False, verbose_name = 'es Menaje de Casa')
	es_vehiculo = models.BooleanField(default = False, verbose_name = 'es Vehiculo')
	def __str__(self):
		return self.descripcion_garantia

#Manejos del Cargo
#1 -- Cargo al Efectivo
#2 -- Cargo a la Cuota
#3 -- Cargo al Desembolso
class ManejoCargo(models.Model):
	manejo_cargo = models.CharField(max_length = 100, blank = False, null = False, verbose_name = 'Nombre del Manejo del Cargo')
	estado = models.BooleanField(default = True, verbose_name = 'Estado del Manejo del Cargo')
	pagado_cuota = models.BooleanField(default = False, verbose_name = 'Pagado en la Cuota')
	pagado_desembolso = models.BooleanField(default = False, verbose_name = 'Pagado en el Desembolso')
	pagado_efectivo = models.BooleanField(default = False, verbose_name = 'Pagado en Efectivo')
	class Meta:
		verbose_name_plural = 'Manejo Cargos'
	def __str__(self):
		return self.manejo_cargo

class Mora(models.Model):
	porcentaje_mora = models.FloatField(default = 0.00, verbose_name = 'Porcentaje de la Mora')
	estado = models.BooleanField(default = True, verbose_name = 'Estado de la Mora')
	def __str__(self):
		return '{} %'.format(self.porcentaje_mora)

class Frecuencia(models.Model):
	descripcion_frecuencia = models.CharField(max_length = 50, verbose_name = 'Descripcion')
	sub_descripcion = models.CharField(max_length = 50, verbose_name = 'Sub Descripcion')
	sub_descripcion_singular = models.CharField(max_length = 50, verbose_name = 'Sub Descripcion Singular')
	estado = models.BooleanField(default = True, verbose_name = 'Estado')
	def __str__(self):
		return '{}'.format(self.descripcion_frecuencia)

class Plazo(models.Model):
	plazo = models.FloatField(default = 0, verbose_name = 'Plazo')
	frecuencia = models.ForeignKey(Frecuencia, on_delete = models.CASCADE, verbose_name = 'Frecuencia')
	estado = models.BooleanField(default = True, verbose_name = 'Estado del Plazo')
	def __str__(self):
		return '{} {} / {}'.format(self.plazo, self.frecuencia.sub_descripcion, self.frecuencia.sub_descripcion_singular)


"""
id		descripcion_frecuencia		cantidad		porcentaje_anio		es_superior		estado		mora_id		es_diaria		vence_fecha_finalizacion
1		DIARIA						1				20					0				1			1			1				1
2		CADA DOS DÍAS				2				10					0				1			1			0				1
3		CADA TRES DÍAS				3				7					0				1			1			0				1
4		SEMANAL						7				4					0				1			1			0				1
5		QUINCENAL					15				2					0				1			1			0				0
6		MENSUAL						30				1					0				1			1			0				0
7		BIMESTRAL					60				2					1				1			1			0				0
8		TRIMESTRAL					90				3					1				1			1			0				0
9		CUATRIMESTRAL				120				4					1				1			1			0				0
10		SEMESTRAL					180				6					1				1			1			0				0
11		ANUAL						365				12					1				1			1			0				0
"""
class FrecuenciaPagos(models.Model):
	descripcion_frecuencia = UpperCaseCharField(max_length = 100, verbose_name = 'Frecuencia de Pago')
	cantidad = models.IntegerField(default = 1, verbose_name = 'Cantidad de Días')
	porcentaje_anio = models.IntegerField(default = 0, verbose_name = 'Equivalente en Meses')
	es_superior = models.BooleanField(default = False, verbose_name = 'Superior a un Mes')
	es_diaria = models.BooleanField(default = False, verbose_name = 'Es Diaria')
	vence_fecha_finalizacion = models.BooleanField(default = False, verbose_name = 'Vence Fecha Finalizacion')
	estado = models.BooleanField(default = True, verbose_name = 'Estado')
	class Meta:
		verbose_name_plural = 'Frecuencia de Pagos'
	def __str__(self):
		return '{}'.format(self.descripcion_frecuencia)


class Cantidad_Pagos(models.Model):
	plazo = models.ForeignKey(Plazo, on_delete = models.CASCADE, verbose_name = 'Plazo')
	frecuencia = models.ForeignKey(FrecuenciaPagos, on_delete = models.CASCADE, verbose_name = 'Frecuencia de Pagos')
	pagos = models.IntegerField(default = 1, verbose_name = 'Cantidad de Pagos')
	estado = models.BooleanField(default = True, verbose_name = 'Estado de cantidad de pagos')
	class Meta:
		verbose_name_plural = 'Cantidad de Pagos'
	def __str__(self):
		return '{} -- {}'.format(self.plazo, self.frecuencia)

class TasaInteres(models.Model):
	interes = models.FloatField(default = 0.00, verbose_name = 'Porcentaje de la Tasa de Interés')
	descripcion = UpperCaseCharField(max_length = 100, verbose_name = 'Nombre de la Tasa de Interés')
	mora = models.ForeignKey(Mora, on_delete = models.CASCADE, verbose_name = 'Mora')
	estado = models.BooleanField(default = True, verbose_name = 'Estado de la Tasa de Interés')
	class Meta:
		verbose_name_plural = 'Tasas de Interés'

	def __str__(self):
		return '{} - {}'.format(self.interes, self.descripcion)

class ActividadesEconomicas(models.Model):
	descripcion_actividad = UpperCaseCharField(max_length = 100, verbose_name = 'Nombre de la Actividad')
	estado = models.BooleanField(default = True, verbose_name = 'Estado de la Actividad')
	class Meta:
		verbose_name_plural = 'Actividades Economicas'
	def __str__(self):
		return '{}'.format(self.descripcion_actividad)

class Sectores(models.Model):
	descripcion_sector = UpperCaseCharField(max_length = 100, verbose_name = 'Nombre del Sector')
	imagen = models.ImageField(upload_to = 'imagen_sector', max_length = 250, null = True, blank = True)
	estado = models.BooleanField(default = True, verbose_name = 'Estado del Sector')
	class Meta:
		verbose_name_plural = 'Sectores'
	def __str__(self):
		return '{}'.format(self.descripcion_sector)

class DestinosCreditos(models.Model):
	abreviatura = UpperCaseCharField(max_length = 20, verbose_name = 'Abreviatura')
	descripcion_destino_credito = UpperCaseCharField(max_length = 100, verbose_name = 'Nombre del Destino')
	estado = models.BooleanField(default = True, verbose_name = 'Estado del Destino')
	class Meta:
		verbose_name_plural = 'Destinos Credito'
	def __str__(self):
		return '{}'.format(self.descripcion_destino_credito)

class Mes(models.Model):
	mes = models.CharField(max_length = 100, blank = False, null = False, verbose_name = 'Nombre del Mes')
	class Meta:
		verbose_name_plural = 'Meses'
	def __str__(self):
		return '{}'.format(self.mes)

#Meses
#1 -- Enero
#2 -- Febrero
#3 -- Marzo
#4 -- Abril
#5 -- Mayo
#6 -- Junio
#7 -- Julio
#8 -- Agosto
#9 -- Septiembre
#10 -- Octubre
#11 -- Noviembre
#12 -- Diciembre


class DiasFeriado(models.Model):
	numero_dia = models.IntegerField(default = 1, null = True, blank = True, verbose_name = 'Día del Mes')
	mes = models.ForeignKey(Mes, on_delete = models.CASCADE, verbose_name = 'Mes')
	estado = models.BooleanField(default = True, verbose_name = 'Estado del Día Feriado')
	sucursal = models.ForeignKey(Sucursal, on_delete = models.CASCADE)
	class Meta:
		verbose_name_plural = 'Dias Feriados'
	def __str__(self):
		return '{} de {}'.format(self.numero_dia, self.mes)


class LineasCredito(models.Model):
	linea_credito = UpperCaseCharField(max_length = 100, verbose_name = 'Nombre de la Linea')
	estado = models.BooleanField(default = True, verbose_name = 'Estado de la Linea')
	class Meta:
		verbose_name_plural = 'Lineas de Crédito'
	def __str__(self):
		return '{}'.format(self.linea_credito)



#Modelo de Genero
class Genero(models.Model):
	genero = models.CharField(max_length = 10, verbose_name = 'Nombre del Genero')

	def __str__(self):
		return self.genero

"""
id	color	estado
21	ALMENDRA	1
2	AMARILLO	1
22	AMARILLO / BLANCO	1
23	AMARILLO / NEGRO	1
24	ANARANJADO	1
25	ANARANJADO / GRIS	1
26	ANARANJADO / NEGRO	1
13	AZUL	1
27	AZUL / BEIGE	1
28	AZUL / BLANCO	1
29	AZUL / BLANCO / NEGRO	1
30	AZUL / GRIS	1
31	AZUL / NEGRO	1
32	AZUL / VERDE	1
33	AZUL OSCURO	1
10	BEIGE	1
34	BEIGE / BLANCO	1
35	BEIGE / CAFE	1
36	BEIGE / FLORIADO	1
37	BEIGE / NEGRO	1
38	BEIGE / ROJO	1
39	BEIGE / VERDE	1
4	BLANCO	1
40	BLANCO / ANARANJADO	1
41	BLANCO / CAFE	1
42	BLANCO / CELESTE	1
43	BLANCO / GRIS	1
44	BLANCO / NEGRO	1
45	BLANCO / ROJO	1
46	BLANCO / ROSADA / AMARILLO	1
47	BLANCO HUESO	1
14	CAFE	1
48	CAFE / CELESTE	1
49	CAFE / CON FLORES	1
50	CAFE / DORADO	1
51	CAFE / GRIS	1
52	CAFE / MORADO	1
53	CAFE / NEGRO	1
54	CAFE / VERDE	1
55	CAFE / VERDE OSCURO	1
56	CAFE OSCURO	1
11	CAOBA	1
16	CAQUI	1
7	CELESTE	1
57	CELESTE / GRIS	1
58	CELESTE / NEGRO	1
59	CELESTE / VERDE	1
12	CREMA	1
60	CROMADO	1
15	DORADO	1
61	DORADO / GRIS	1
62	FLOREADO	1
63	GRAFITO	1
64	GRAFITO / GRIS	1
65	GRAFITO / NEGRO	1
9	GRIS	1
66	GRIS / NEGRO	1
67	GRIS / PLATEADO	1
68	GRIS / ROJO	1
69	GRIS / ROSADO	1
70	GRIS / TRANSPARENTE	1
71	GRIS / TURQUEZA	1
72	GRIS / VERDE	1
73	LILA	1
74	MADERA	1
17	MARFIL	1
75	METALICO	1
76	MORADO / BLANCO	1
77	MORADO / FUCSIA	1
78	MORADO / LILA	1
79	MORADO / NEGRO	1
80	MORADO / TURQUEZA	1
81	MORADO / VERDE	1
82	MOSTAZA	1
83	MULTICOLORES	1
84	N/A	1
1	NEGRO	1
85	NEGRO / DORADO	1
86	NEGRO / TRANSPARENTE	1
87	PIEL	1
5	PLATEADO	1
6	PLATEADO / NEGRO	1
20	PURPURA	1
88	ROJO / AZUL / MORADO	1
89	ROJO / CAFE	1
90	ROJO / DORADO	1
91	ROJO / NEGRO	1
92	ROJO FLORAL	1
93	ROSADO	1
94	ROSADO / AZUL	1
95	ROSADO / BEIGE	1
96	ROSADO / BLANCO	1
97	ROSADO / CAFE	1
98	ROSADO / NEGRO	1
99	ROSADO / VERDE	1
100	ROSADO / VERDE / MORADO / ANARANJADO	1
8	TRANSPARENTE	1
101	TURQUESA	1
102	VARIOS	1
3	VERDE	1
103	VERDE / AMARILLO	1
104	VERDE / BLANCO	1
105	VERDE / DORADO	1
106	VERDE / NEGRO	1
18	VERDE CIAN	1
107	VERDE FLORIADO	1
108	VERDE OLIVA	1
109	VERDE OSCURO	1
110	VERDE TIERNO	1
111	VINO	1
19	VIOLETA	1
"""
#Modelo de Color
class Color(models.Model):
	color = UpperCaseCharField(max_length = 50, verbose_name = 'Nombre del Color')
	estado = models.BooleanField(default = True, verbose_name = 'Estado del Color')

	def __str__(self):
		return self.color

#Modelo de Marca
class Marca(models.Model):
	marca = UpperCaseCharField(max_length = 50, verbose_name = 'Nombre de la Marca')
	estado = models.BooleanField(default = True, verbose_name = 'Estado de la Marca')

	def __str__(self):
		return self.marca

#Modelo de Modelo
class Modelo(models.Model):
	modelo = UpperCaseCharField(max_length = 100, verbose_name = 'Modelo')
	marca = models.ForeignKey(Marca, on_delete = models.CASCADE, verbose_name = 'Marca')
	estado = models.BooleanField(default = True, verbose_name = 'Estado')
	def __str__(self):
		return '{} -- {}'.format(self.modelo, self.marca)

#Modelo de Tipo_Vivienda
class Tipo_Vivienda(models.Model):
	tipo_vivienda = models.CharField(max_length = 50, verbose_name = 'Tipo de Vivienda')
	class Meta:
		verbose_name_plural = 'Tipos de Vivienda'
	def __str__(self):
		return self.tipo_vivienda

#Modelo de Nivel_Educativo
class Nivel_Educativo(models.Model):
	nivel_educativo = models.CharField(max_length = 50, verbose_name = 'Nivel Educativo')
	class Meta:
		verbose_name_plural = 'Niveles Educativos'
	def __str__(self):
		return self.nivel_educativo

#Modelo de Conyuge
class Conyuge(models.Model):
	num_identidad = models.CharField(max_length = 15, verbose_name = 'Numero de Identidad', null = True, blank = True)
	nombre_completo = UpperCaseCharField(max_length = 60, verbose_name = 'Nombre Completo del Conyuge')
	fecha_nac = models.DateField(verbose_name = 'Fecha de Nacimiento', null = True, blank = True)
	fecha_registro = models.DateField(auto_now_add = True, verbose_name = 'Fecha de Registro')
	ocupacion = models.CharField(max_length = 40)
	salario = models.FloatField(default = 0, null = True, blank = True)
	celular = models.CharField(max_length = 25, null = True, blank = True)
	direccion = models.TextField()
	nombre_trabajo = models.CharField(max_length = 40, null = True, blank = True, verbose_name = 'Nombre del Trabajo')
	telefono_trabajo = models.CharField(max_length = 25, null = True, blank = True, verbose_name = 'Teléfono del Trabajo')
	direccion_trabajo = models.TextField(null = True, blank = True, verbose_name = 'Dirección del Trabajo')
	genero = models.ForeignKey(Genero, on_delete = models.CASCADE, verbose_name = 'Genero del Conyuge')
	esde_cliente = models.BooleanField(default = True)
	sucursal = models.ForeignKey(Sucursal, on_delete = models.CASCADE)
	def __str__(self):
		return "{} -- {}" .format(self.num_identidad, self.nombre_completo)

#Modelo de Tipo_Socializacion
class Tipo_Socializacion(models.Model):
	tipo_socializacion = UpperCaseCharField(max_length = 50)
	estado = models.BooleanField(default = True)
	class Meta:
		verbose_name_plural = 'Tipos de Socialización'
	def __str__(self):
		return self.tipo_socializacion


class Tipo_Persona(models.Model):
	abreviatura = models.CharField(max_length = 20)
	tipo_persona = models.CharField(max_length = 100, blank = False, null = False, verbose_name = 'Tipo de Persona')
	class Meta:
		verbose_name_plural = 'Tipos de Personas'
	def __str__(self):
		return '{}'.format(self.tipo_persona)


class Producto_Empresa(models.Model):
	producto = UpperCaseCharField(max_length = 50, verbose_name = 'Nombre del Producto')
	estado = models.BooleanField(default = True)
	class Meta:
		verbose_name_plural = 'Productos Empresa'
	def __str__(self):
		return '{}'.format(self.producto)


#Modelo de Negocio
class Negocio(models.Model):
	nombre_negocio = models.CharField(max_length = 100, verbose_name = 'Nombre del Negocio', null = True, blank = True)
	antiguedad_negocio = models.CharField(max_length = 100)
	direccion_negocio = models.TextField()
	sector = models.ForeignKey(Sectores, on_delete = models.CASCADE)
	fecha_inicio = models.DateField(verbose_name = 'Fecha de Inicio', null = True, blank = True)
	numero_empleados = models.IntegerField(default = 1, verbose_name = 'Número de Empleados')
	tipo_actividad = models.TextField(verbose_name = 'Tipo de Actividad', null = True, blank = True)
	sucursal = models.ForeignKey(Sucursal, on_delete = models.CASCADE)
	def __str__(self):
		return "{}" .format(self.nombre_negocio)



#Modelo de Empresa_Cliente
class Empresa_Cliente(models.Model):
	empresa = models.CharField(max_length = 100, verbose_name = 'Nombre de la Empresa')
	celular = models.CharField(max_length = 25, null = True, blank = True)
	telefono = models.CharField(max_length = 25, null = True, blank = True)
	correo = models.EmailField(null = True, blank = True)
	tipo_actividad = models.TextField(verbose_name = 'Tipo de Actividad', null = True, blank = True)
	direccion = models.TextField()
	tiempo_laborando = models.CharField(max_length = 50)
	jefe_inmediato = models.CharField(max_length = 100, null = True, blank = True)
	sector = models.ForeignKey(Sectores, on_delete = models.CASCADE)
	sucursal = models.ForeignKey(Sucursal, on_delete = models.CASCADE)
	class Meta:
		verbose_name_plural = 'Empresas de Clientes'
	def __str__(self):
		return self.empresa

#Modelo de Datos_Remesa
class Datos_Remesa(models.Model):
	nombre_completo = models.CharField(max_length = 100)
	celular = models.CharField(max_length = 25, null = True, blank = True)
	direccion = models.TextField()
	valor_remesa = models.FloatField(default = 0.00)
	pais = models.ForeignKey(Pais, on_delete = models.CASCADE)
	tipo_actividad = models.TextField(verbose_name = 'Tipo de Actividad', null = True, blank = True)
	frecuencia = models.ForeignKey(Frecuencia, on_delete = models.CASCADE)
	sucursal = models.ForeignKey(Sucursal, on_delete = models.CASCADE)
	class Meta:
		verbose_name_plural = 'Datos de Remesas'
	def __str__(self):
		return "{}" .format(self.nombre_completo)


"""
id	estado
1	CREACIÓN
2	ACTUALIZACIÓN
3	VIGENTE
4	PROCESO
5	BLOQUEADO
6	NO DESEADO
7	RETIRADO
8	ACTIVO
9	INACTIVO
"""
class Estado_Sujeto(models.Model):
	estado = models.CharField(max_length = 100, verbose_name = 'Estado del Sujeto')
	class Meta:
		verbose_name_plural = 'Estados del Sujeto'
	
	def __str__(self):
		return '{}'.format(self.estado)

"""
id	tipo_inmueble
1	CASA
2	EDIFICIO
3	TERRENO
"""
#Modelo de Tipo_Inmueble
class Tipo_Inmueble(models.Model):
	tipo_inmueble = models.CharField(max_length = 50)

	def __str__(self):
		return self.tipo_inmueble

"""
id	condicion
1	CON GRAVAMEN
2	LIBRE DE GRAVAMEN
"""
#Modelo de Condicion_Inmueble
class Condicion_Inmueble(models.Model):
	condicion = models.CharField(max_length = 50)

	def __str__(self):
		return self.condicion

"""
id	tipo
1	AUTOBÚS
2	CAMIÓN
3	CAMIONETA
4	CUATRIMOTO
5	MICROBUS
6	MOTOCICLETA
7	PICK UP
8	RASTRA
9	TRACTOR
10	TURISMO
11	VAGONETA (VAN)
"""
#Modelo de Tipo_Vehiculo
class Tipo_Vehiculo(models.Model):
	tipo = models.CharField(max_length = 50)

	def __str__(self):
		return self.tipo

"""
id	tipo_transmision
1	AUTOMÁTICA
2	MANUAL
"""
#Modelo de Tipo_Transmision_Vehiculo
class Tipo_Transmision_Vehiculo(models.Model):
	tipo_transmision = models.CharField(max_length = 50)

	def __str__(self):
		return self.tipo_transmision

"""
id	tipo_combustible
1	DIESEL
2	GAS LPG
3	GASOLINA REGULAR
4	GASOLINA SUPER
"""
#Modelo de Tipo_Combustible_Vehiculo
class Tipo_Combustible_Vehiculo(models.Model):
	tipo_combustible = models.CharField(max_length = 50)

	def __str__(self):
		return self.tipo_combustible

"""
INSERT INTO catalogos_tipo_menaje_casa(tipo_menaje) VALUES
('AIRE ACONDICIONADO'),
('BATIDORA DE REPOSTERIA'),
('CENTRO DE ENTRETENIMIENTO'),
('CHINERO DE METAL'),
('CHINERO MADERA'),
('COLUMNA AMPLIFICADOR'),
('COMODA DE MADERA'),
('COMODA DE METAL'),
('COMODA PLASTICA DE COLORES'),
('COMPRESOR ELECTRICO'),
('COMPUTADORA DE ESCRITORIO'),
('COMPUTADORA PORTATIL'),
('CONSOLA DE VIDEO JUEGO'),
('D V D'),
('DESCREMADORA DE LACTEOS'),
('DESMONTADORA DE LLANTAS AUTOMATICA'),
('DIVISION DE MADERA'),
('DIVISION DE METAL'),
('ECO-FOGON'),
('EQUIPO DE SONIDO'),
('ESCRITORIO DE MADERA'),
('ESCRITORIO DE METAL'),
('ESTANTE DE MADERA'),
('ESTANTE DE METAL'),
('ESTUFA DE GAS'),
('ESTUFA ELECTRICA'),
('ESTUFA INDUSTRIAL DE GAS'),
('FREEZER'),
('FREIDORA INDUSTRIAL'),
('GAVETERO PLASTICO'),
('GENERADOR ELECTRICO'),
('GILLOTINA INDUSTRIAL DE IMPRENTA'),
('GRABADORA'),
('HIDROLAVADORA A PRECION PARA CARROS Y MOTOS'),
('HIELERA PLASTICA'),
('HORNO INDUSTRIAL'),
('IMPRESORA MULTIFUNCIONAL'),
('JUEGO DE COMEDOR'),
('JUEGO DE SALA 3 PIEZAS'),
('LAVADORA'),
('MANTENEDOR DE 1 PUERTA TRANSPARENTE DE VIDRIO'),
('MANTENEDOR DE 2 PUERTAS TRANSPARENTE DE VIDRIO'),
('MAQUINA DE COPIAS DE LLAVES'),
('MAQUINA DE COSTURAR ELECTRICA'),
('MAQUINA DE COSTURAR MECANICA'),
('MAQUINA ESMERILADORA'),
('MAQUINA ESTIRADORA DE MASA INDUSTRIAL'),
('MAQUINA FUNDIDORA'),
('MAQUINA MANUAL PARA HACER TORTILLAS'),
('MAQUINA MEZCLADORA INDUSTRIAL'),
('MAQUINA PARA FABRICAR BLOQUES'),
('MAQUINA PARA HACER PALOMITAS DE MAIZ'),
('MAQUINA PLOTTER PARA IMPRIMIR PEGATINA DE VINILO'),
('MAQUINA PULIDORA DE PRENDAS '),
('MAQUINA SORGETEADORA ELECTRICA'),
('MICROONDAS'),
('MINI COMPONENTE DE SONIDO'),
('MOLINO DE QUEBRAR MAIZ'),
('MOTOR MARINO'),
('MOTOSIERRA MOVIBLE A GASOLINA'),
('MUEBLE PARA COMPUTADORA'),
('OASIS'),
('PIANO DIGITAL O TECLADO ELECTRICO'),
('PISTOLA DE IMPACTO'),
('PRENSA HIDRAULICA MECANICA'),
('RACK PARA TV'),
('REDES DE PESCAR'),
('REFRIGERADORA'),
('ROPERO'),
('SECADORA DE ROPA'),
('SEPARADOR DE PANTALLA LCD PARA CELULAR'),
('SIERRA DE INGLETE PARA CARPINTERO'),
('SILLA DE CORTE PARA PELUQUERIA Y BARBERIA'),
('SILLON'),
('SISTEMA DE AUDIO EN CASA(PARLANTES)'),
('SOLDADORA ELECTRICA'),
('TOCADOR DE MADERA'),
('TRICICLO DE CARGA'),
('TV CONVENCIONAL'),
('TV LCD'),
('TV LED'),
('VITRINA ALUMINIO Y VIDRIO'),
('VITRINA MADERA Y VIDRIO');
"""
#Modelo de Tipo_Menaje_Casa
class Tipo_Menaje_Casa(models.Model):
	tipo_menaje = UpperCaseCharField(max_length = 100)
	estado = models.BooleanField(default = True)

	def __str__(self):
		return self.tipo_menaje




























