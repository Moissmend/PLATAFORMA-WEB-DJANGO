#IMPORTACIONES
from django.db import connection, connections, transaction, DatabaseError
import datetime
from django.conf import settings 
from django.core.mail import send_mail

#IMPORTACIONES NECESARIAS PARA LOS REPORTES PDF 
import os
from django.http import HttpResponse
from xhtml2pdf import pisa
from html import escape
from django.template.loader import get_template

#MODELOS
from django.contrib.auth.models import User
from catalogos.models import *
from configuraciones.models import *
from empleados.models import *

def verificarPermiso(request, vista):
	permiso = 'admin.' + str(vista)
	if request.user.has_perm(permiso):
		return False
	else: 
		return True

def link_callback(uri, rel):
    #CONVIERTA URI HTML A RUTAS DE SISTEMA ABSOLUTAS PARA QUE XHTML2PDF PUEDA ACCEDER A ESOS RECURSOS
    sUrl = settings.STATIC_URL    
    sRoot = settings.STATIC_ROOT      
    
    #CONVIERTE LA URL A RUTAS DEL SISTEMA ABSOLUTAS
    if uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  

    # Asegúrese de que ese archivo existe
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s' % (sUrl)
        )
    return path

def generar_pdf(template_src, context_dict = {}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type = 'application/pdf')
    pisa_status = pisa.CreatePDF(html, dest = response, link_callback = link_callback)
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def getEmpleado( idUsuario ):
    return Empleado.objects.get(usuario = int( idUsuario ))

def getUsuario( idUsuario ):
    return User.objects.get(pk = int( idUsuario ))

def ejecutarSPList(conexion_bd, nombreProcedure, parametrosBD):
	try:
		with connections[conexion_bd].cursor() as cursorResultadoBD:
			cursorResultadoBD.callproc(nombreProcedure, parametrosBD)

			columnas = [columna[0] for columna in cursorResultadoBD.description]
			return [
				dict(zip(columnas, fila))for fila in cursorResultadoBD.fetchall()
			]
	except BaseException as e:
		return str(e)

def ejecutarSPScalar(conexion_bd, nombreProcedure, parametrosBD):
	try:
		with connections[conexion_bd].cursor() as cursorResultadoBD:
			cursorResultadoBD.callproc(nombreProcedure, parametrosBD)

			return cursorResultadoBD.fetchone()

	except BaseException as e:
		return str(e)

def ejecutarSPComando(conexion_bd, nombreProcedure, parametrosBD):
	try:
		with connections[conexion_bd].cursor() as cursorResultadoBD:
			return cursorResultadoBD.callproc(nombreProcedure, parametrosBD)

	except BaseException as e:
		return str(e)

#APLICACIONES DEL SISTEMA
# 1 -- catalogos
# 2 -- clientes
# 3 -- configuraciones
# 4 -- contabilidad
# 5 -- empleados
# 6 -- prestamos
# 7 -- recursos_humanos
# 8 -- reportes
# 9 -- rh_reportes
# 10 -- seguridad
# 11 -- ws_administracion
def almacenarErroresExcepciones(descripcion_error, aplicacion_id, nombre_area, usuario_registro):
	try:
		with transaction.atomic(using = 'finsurhn_sp_db'):
			error = Error_Excepcion(
				descripcion_error = descripcion_error,
				sistema_id = settings.SISTEMA_ID,
				aplicacion_id = aplicacion_id,
				nombre_area = nombre_area,
				usuario_registro = usuario_registro,
				solucion_error = None,
				usuario_solucion = None)

			error.save()
	except BaseException as e:
		pass