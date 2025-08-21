from django.db import models
from django.contrib.auth.models import User
from catalogos.models import *
from configuraciones.models import *
import sys
from importlib import reload
reload(sys)

#Modelo de Estado_Civil
class Estado_Civil(models.Model):
	estado = models.CharField(max_length = 50, verbose_name = 'Estado Civil')
	class Meta:
		verbose_name_plural = 'Estados Civiles'
	def __str__(self):
		return self.estado


#Modelo de Funcion_Cargo
class Funcion_Cargo(models.Model):
	funcion = UpperCaseCharField(max_length = 2000, verbose_name = 'Función del Cargo')
	class Meta:
		verbose_name_plural = 'Funciones de los Cargos'
	def __str__(self):
		return self.funcion

#Modelo de Cargo
class Cargo(models.Model):
    cargo = UpperCaseCharField(max_length = 50)
    funcion_cargo = models.ManyToManyField(Funcion_Cargo, blank = True)

    def __str__(self):
      return self.cargo


#Modelo de Jefe_Inmediato
class Jefe_Inmediato(models.Model):
    jefe = UpperCaseCharField(max_length = 50)
    class Meta:
      verbose_name_plural = 'Jefes Inmediatos'
    def __str__(self):
      return self.jefe


#Modelo de Zona
class Zona(models.Model):
    pais = models.ForeignKey(Pais, on_delete = models.CASCADE)
    departamento = models.ForeignKey(Departamentos, on_delete = models.CASCADE)
    municipio = models.ForeignKey(Municipios, on_delete = models.CASCADE)
    zona = models.CharField(max_length = 100)
    sucursal = models.ForeignKey(Sucursal, on_delete = models.CASCADE)
    estado = models.BooleanField(default = True)

    def __str__(self):
      return "{} -- {} -- {}" .format(self.zona, self.municipio, self.departamento)


#Modelo de Centro_Costo
class Centro_Costo(models.Model):
    codigo = models.CharField(max_length = 10)
    centro = UpperCaseCharField(max_length = 60)
    es_recurso_humano = models.BooleanField(default = False)
    es_financiero = models.BooleanField(default = False)
    sucursal = models.ForeignKey(Sucursal, on_delete = models.CASCADE)
    class Meta:
      verbose_name_plural = 'Centros de Costos'
    def __str__(self):
      return "{} -- {}" .format(self.codigo, self.centro)

#Modelo de SubCentro_Costo
class SubCentro_Costo(models.Model):
    codigo = models.CharField(max_length = 20)
    subcentro = UpperCaseCharField(max_length = 60)
    es_recurso_humano = models.BooleanField(default = False)
    es_financiero = models.BooleanField(default = False)
    centro = models.ForeignKey(Centro_Costo, on_delete = models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete = models.CASCADE)
    class Meta:
      verbose_name_plural = 'Sub Centros de Costos'
    def __str__(self):
      return "{} -- {} -> {}" .format(self.codigo, self.subcentro, self.centro.centro)


#Modelo de Tipo_Contrato
class Tipo_Contrato(models.Model):
    tipo_contrato = UpperCaseCharField(max_length = 50, verbose_name = 'Tipo de Contrato')
    class Meta:
      verbose_name_plural = 'Tipos de Contrato'
    def __str__(self):
      return self.tipo_contrato


#Modelo de Profesion
class Profesion(models.Model):
    abreviatura = models.CharField(max_length = 30, null = True, blank = True)
    profesion = models.CharField(max_length = 50)
    class Meta:
      verbose_name_plural = 'Profesiones'
    def __str__(self):
      return self.profesion

#Modelo de Tipo_Sucursal_Empleado
class Tipo_Sucursal_Empleado(models.Model):
    tipo_sucursal_empleado = models.CharField(max_length = 50)
    class Meta:
      verbose_name_plural = 'Tipos Sucursal Empleado'
    def __str__(self):
      return self.tipo_sucursal_empleado


#Modelo de Empleado
class Empleado(models.Model):
    codigo = models.IntegerField(default = 0, verbose_name = 'Código Correlativo Cliente')
    rtn = models.CharField(max_length = 16, null = True, blank = True)
    num_identidad = models.CharField(max_length = 15, verbose_name = 'Numero de Identidad')
    cod_banco = models.IntegerField(verbose_name = 'Código del Banco para el Empleado')
    num_cuenta = models.CharField(max_length = 15, verbose_name = 'Número de Cuenta del Empleado')
    primer_nombre = UpperCaseCharField(max_length = 30)
    segundo_nombre = UpperCaseCharField(max_length = 30, null = True, blank = True)
    primer_apellido = UpperCaseCharField(max_length = 30)
    segundo_apellido = UpperCaseCharField(max_length = 30, null = True, blank = True)
    fecha_nac = models.DateField(verbose_name = 'Fecha de Nacimiento')
    fecha_registro = models.DateTimeField(auto_now_add = True)
    fecha_entrada_empresa = models.DateField(verbose_name = 'Fecha de Ingreso a la Empresa')
    fecha_ingreso = models.DateField(verbose_name = 'Fecha de Inicio de Contrato')
    fecha_finalizacion = models.DateField(verbose_name = 'Fecha de Finalizacion Contrato')
    telefono_casa = models.CharField(max_length = 25, null = True, blank = True, verbose_name = 'Teléfono de la Casa')
    telefono_trabajo = models.CharField(max_length = 25, null = True, blank = True, verbose_name = 'Teléfono del Trabajo')
    es_cobrador = models.BooleanField(default = False)
    es_desembolsador = models.BooleanField(default = False)
    es_promotor = models.BooleanField(default = False)
    celular = models.CharField(max_length = 25, null = True, blank = True)
    direccion = models.TextField()
    direccion_referencia = models.TextField(verbose_name = 'Dirección de Referencia')
    mac_adress = models.CharField(max_length = 30, null = True, blank = True)
    correo = models.EmailField()
    imagen = models.ImageField(upload_to = 'imagen_empleado_perfil', max_length = 250, null = True, blank = True)
    doc_legales = models.FileField(upload_to = 'documentos_legales_empleados', max_length = 250, null = True, blank = True, verbose_name = 'Documentos Legales')
    doc_cargo = models.FileField(upload_to = 'documentos_cargo_empleados', max_length = 250, null = True, blank = True, verbose_name = 'Documentos del Cargo')
    dias_vacacion = models.IntegerField(default = 10, verbose_name = 'Cantidad de Días de Vacaciones')
    sueldo = models.FloatField(default = 0.00, verbose_name = 'Sueldo Base Mensual')
    depreciacion = models.FloatField(default = 0.00, verbose_name = 'Depreciación Motocicleta Mensual')
    combustible = models.FloatField(default = 0.00, verbose_name = 'Depreciación de Combustible Mensual')
    ihss = models.FloatField(default = 0.00)
    rap = models.FloatField(default = 0.00)
    plan_celular = models.FloatField(default = 0.00)
    isr = models.FloatField(default = 0.00)
    rol = models.ForeignKey(Rol, on_delete = models.CASCADE)
    estado_civil = models.ForeignKey(Estado_Civil, on_delete = models.CASCADE)
    nivel_educativo = models.ForeignKey(Nivel_Educativo, on_delete = models.CASCADE)
    conyuge = models.ForeignKey(Conyuge, null = True, blank = True, on_delete = models.CASCADE)
    socializacion = models.ManyToManyField(Tipo_Socializacion)
    profesion = models.ForeignKey(Profesion, on_delete = models.CASCADE)
    pais = models.ForeignKey(Pais, on_delete = models.CASCADE)
    departamento = models.ForeignKey(Departamentos, on_delete = models.CASCADE)
    municipio = models.ForeignKey(Municipios, on_delete = models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete = models.CASCADE)
    genero = models.ForeignKey(Genero, on_delete = models.CASCADE)
    jefe_inmediato = models.ManyToManyField(Jefe_Inmediato)
    tipo_contrato = models.ForeignKey(Tipo_Contrato, on_delete = models.CASCADE, verbose_name = 'Tipo de Contrato')
    subcentro_costo = models.ForeignKey(SubCentro_Costo, on_delete = models.CASCADE, verbose_name = 'Sub Centro de Costos')
    usuario = models.IntegerField(null = True, blank = True)
    usuario_registro = models.IntegerField()
    sucursal = models.ForeignKey(Sucursal, on_delete = models.CASCADE)
    firma_empleado = models.ImageField(upload_to = 'firma_empleado', max_length = 250, null = True, blank = True)
    tipo_zona = models.ForeignKey(to = 'clientes.Tipo_Zona', null = True, blank = True, on_delete = models.CASCADE, verbose_name = 'Tipo de Zona')
    estado_empleado = models.ForeignKey(Estado_Sujeto, null = True, blank = True, on_delete = models.CASCADE, verbose_name = 'Estado del Empleado')
    tipo_sucursal_empleado = models.ForeignKey(Tipo_Sucursal_Empleado, on_delete = models.CASCADE)
    es_aval = models.BooleanField(default = False, verbose_name = 'Es Aval')
    num_ciclos = models.IntegerField(default = 0, verbose_name = 'Número de Ciclos')

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s%s%s%s' % (self.primer_nombre + ' ', self.segundo_nombre +' ' if self.segundo_nombre is not None else '', self.primer_apellido +' ', self.segundo_apellido if self.segundo_apellido is not None else '')
    @property
    def nombre_id_guiones(self):
        "Return, el Primer Nombre, Primer Apellido, Código separado con guiones"
        return '%s_%s_%s' % (self.primer_nombre, self.primer_apellido, self.codigo)
    def __str__(self):
        return "{} -- {} {}" .format(self.num_identidad, self.primer_nombre, self.primer_apellido)

#Modelo de Asignacion_Gasto_Empleado_Sucursal
class Asignacion_Gasto_Empleado_Sucursal(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete = models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete = models.CASCADE)
    porcentaje_gastos_empleado = models.FloatField(default = 0.00, verbose_name = 'Porcentaje de Gastos Empleado')

    def __str__(self):
        return '{} -- {}' .format(self.empleado, self.sucursal)
    class Meta:
        unique_together = ("empleado", "sucursal",)
        verbose_name_plural = 'Asignacion Gasto Empleado por Sucursal'


#Modelo de Cambio_Estado_Empleado
class Cambio_Estado_Empleado(models.Model):
	estado_empleado = models.ForeignKey(Estado_Sujeto, on_delete = models.CASCADE, verbose_name = 'Estado del Empleado')
	descripcion = models.TextField()
	fecha_registro = models.DateTimeField()
	empleado = models.ForeignKey(Empleado, on_delete = models.CASCADE)
	usuario_registro = models.IntegerField()
	class Meta:
		verbose_name_plural = 'Cambios de Estado del Empleado'
	def __str__(self):
		return "{}" .format(self.empleado)

#Modelo de Asignacion_Tipo_Zona_Empleado
class Asignacion_Tipo_Zona_Empleado(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete = models.CASCADE)
    tipo_zona = models.ForeignKey(to = 'clientes.Tipo_Zona', on_delete = models.CASCADE)
    usuario_empleado = models.IntegerField()
    
    def __str__(self):
        return '{} -- {}' .format(self.empleado, self.tipo_zona)
    class Meta:
        unique_together = ("empleado", "tipo_zona",)
        verbose_name_plural = 'Asignacion Tipo Zona a Empleado'





