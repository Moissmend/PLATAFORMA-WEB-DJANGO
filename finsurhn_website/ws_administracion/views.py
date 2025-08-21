#IMPORTACIONES
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.urls import reverse
from htmlmin.decorators import minified_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from google.cloud import storage
from django.utils import timezone
from django.core.files.storage import default_storage
import datetime
from django_ratelimit.decorators import ratelimit
from django.conf import settings
# Para poder mandar el correo con archivos
from django.core.mail import send_mail, EmailMessage
from django.db import transaction

from clientes.utils import *
from .services import *
from importlib import reload
reload(sys)
import os, json

#MODELOS
from catalogos.models import *
from clientes.models import *
from configuraciones.models import *
from empleados.models import *

from .models import *
from .forms import *

# @minified_response
# def inicio(request):
#     # if request.user.is_authenticated:
#     #     return redirect(reverse('ws_administracion:inicio_administracion'))

#     # else:
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
#     listaSectores = []
#     for s in Sectores.objects.filter(estado = True):
#         if s.imagen == None or s.imagen == '':
#             imagenNube = ''
#         else:
            
#             direccionImagenNube = str(s.imagen)
#             if default_storage.exists(direccionImagenNube) == True:
#                 blob = bucket.blob(direccionImagenNube)

#                 imagenNube = blob.generate_signed_url(
#                     version = "v4",
#                     expiration = datetime.timedelta(hours = 1),
#                     method = "GET"
#                 )
#             else:
#                 imagenNube = ''

#         listaSectores.append({
#             'descripcion_sector': s.descripcion_sector,
#             'imagen': imagenNube,
#             'imagendos': s.imagen
#         })
    
#     lista_empleo = []
#     for ie in Informacion_Empleo.objects.filter(estado = True).order_by('orden').exclude(num_vacantes = 0):
#         info_empleo = {}
#         info_empleo.update({
#             'id': ie.id,
#             'idcargo': ie.idcargo,
#             'cargo': Cargo.objects.get(id = int(ie.idcargo)).cargo,
#             'descripcion': ie.descripcion,
#             'num_vacantes': ie.num_vacantes,
#             'ciudad': ie.ciudad,
#             'orden': ie.orden,
#             'imagen': ie.imagen,
#             'estado': ie.estado
#         })
#         lista_empleo.append(info_empleo)
    
#     return render(request, 'inicio.html', {
#         'form': ContactanosForm(),
#         'sectores': listaSectores,
#         'valores': Valores_Empresa.objects.all().order_by('valor'),
#         'info_empleo': lista_empleo,
#         'galeria_empresa': Galeria_Empresa.objects.filter(estado = True).order_by('orden')
#     })

@minified_response
def index(request):
    # if request.user.is_authenticated:
    #     return redirect(reverse('ws_administracion:inicio_administracion'))
    # else:  
    
    lista_empleo = []
    for ie in Informacion_Empleo.objects.filter(estado = True).order_by('orden').exclude(num_vacantes = 0):
        info_empleo = {}
        info_empleo.update({
            'id': ie.id,
            'idcargo': ie.idcargo,
            'cargo': Cargo.objects.get(id = int(ie.idcargo)).cargo,
            'descripcion': ie.descripcion,
            'num_vacantes': ie.num_vacantes,
            'ciudad': ie.ciudad,
            'orden': ie.orden,
            'imagen': ie.imagen,
            'estado': ie.estado
        })
        lista_empleo.append(info_empleo)
        
    return render(request, "web/index.html", {
        'form': ContactForm(),
        'galeria_empresa': Galeria_Empresa.objects.filter(estado = True).order_by('orden'),
        'info_empleo': lista_empleo,
    })

@minified_response
def acercade(request):
    # if request.user.is_authenticated:
    #     return redirect(reverse('ws_administracion:inicio_administracion'))
    # else:
    valores_db = Valores_Empresa.objects.all().order_by('valor')
    
    valores_svg = [
        { "src": "img/confianza.svg", "alt": "Confianza"},
        { "src": "img/integridad.svg", "alt": "Integridad"},
        { "src": "img/pasion.svg", "alt": "Pasión"},
        { "src": "img/respeto.svg", "alt": "Respeto"},
        { "src": "img/servicio.svg", "alt": "Servicio"},
    ]
    
    valores = list(zip(valores_db, valores_svg))
    
    return render(request, 'web/acercade.html', {
        'valores': valores,
    })

@minified_response
def solicitud(request):
    return render(request, 'web/solicitud_credito.html')

@minified_response
def aplicar(request):
    return render(request, 'web/aplicar_solicitud.html', {"form": SolicitudForm()})

@minified_response
def contacto(request):
    # if request.user.is_authenticated:
    #     return redirect(reverse('ws_administracion:inicio_administracion'))
    # else:
    return render(request, "web/contacto.html", {"form": ContactForm()})

@minified_response
def servicios(request):
    # if request.user.is_authenticated:
    #     return redirect(reverse('ws_administracion:inicio_administracion'))
    # else:
    storage_client = storage.Client()
    bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
    listaSectores = []
    for s in Sectores.objects.filter(estado = True):
        if s.imagen == None or s.imagen == '':
            imagenNube = ''
        else:
            direccionImagenNube = str(s.imagen)
            if default_storage.exists(direccionImagenNube) == True:
                blob = bucket.blob(direccionImagenNube)

                imagenNube = blob.generate_signed_url(
                    version = "v4",
                    expiration = datetime.timedelta(hours = 1),
                    method = "GET"
                )
            else:
                imagenNube = ''

        listaSectores.append({
            'descripcion_sector': s.descripcion_sector,
            'imagen': imagenNube,
            'imagendos': s.imagen
        })
    return render(request, "web/servicios.html", { 'sectores': listaSectores })

@minified_response
def social(request):
    # if request.user.is_authenticated:
    #     return redirect(reverse('ws_administracion:inicio_administracion'))
    # else:
    storage_client = storage.Client()
    bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
    listaRes = []
    
    responsabilidad = Responsabilidad_Social.objects.filter(estado = True)

    for r in responsabilidad:
        direccionImagenNube = str(r.imagen)
        if default_storage.exists(direccionImagenNube) == True:
            blob = bucket.blob(direccionImagenNube)

            imagenNube = blob.generate_signed_url(
                version = "v4",
                expiration = datetime.timedelta(hours = 1),
                method = "GET"
            )
        else:
            imagenNube = ''

        listaRes.append({
            'id': r.id, 
            'nombre': r.nombre, 
            'descripcion': r.descripcion, 
            'estado': r.estado, 
            'nombreImagen': str(r.imagen),
            'imagen': imagenNube,
            'fecha_realizacion': r.fecha_realizacion
        })
    
    return render(request, "web/social.html", { 'imagenes': listaRes})

def inicio_sesion(request):
    return render(request, 'login.html')

def ratelimited_view(request, exception):
    return JsonResponse({
        'resultado': 'false', 
        'error': 'Demasiados intentos de inicio de sesión. Por favor espere 5 minutos.'
    }, status=429)

@ratelimit(key = 'ip', rate='2/m')
def ajax_inicio_session(request):
    # was_limited = getattr(request, 'limited', False)
    # if was_limited:
    #     return JsonResponse({
    #         'resultado': 'false',
    #         'error': 'Demasiados intentos. Intente de nuevo en unos minutos.'
    #     })
    
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest': 
        try:
            usuario = authenticate(
                username = request.POST.get('txtUsuario'),
                password = request.POST.get('txtContrasena')
                )
                        
            if usuario is not None:
                if usuario.is_active:
                    # if Empleado.objects.filter(usuario = int( usuario.pk )):k
                    login(request, usuario) 
                    
                    if usuario.is_staff or usuario.is_superuser:
                        return JsonResponse({'resultado': 'true', 'url': reverse('ws_administracion:inicio_administracion')})
                    else:
                        return JsonResponse({'resultado': 'false', 'error': 'No tienes permisos para acceder a esta sección.'})

                    # elif Cliente.objects.filter(usuario = int( usuario.pk )):
                    #     return JsonResponse({'resultado': 'false', 'error': 'Los Usuarios de Clientes no tienen Acceso a este Sistema.'})

                    # else:
                    #     return JsonResponse({'resultado': 'false', 'error': 'Usuario Sin Asignar'})

                else:
                    return JsonResponse({'resultado': 'false', 'error': 'Usuario Inactivo'})

            else:
                return JsonResponse({'resultado': 'false', 'error': 'Usuario o Contraseña Incorrectos'})
            
        except BaseException as e:
            almacenarErroresExcepciones(
                descripcion_error = str(e), 
                aplicacion_id = 11,
                nombre_area = str( request.resolver_match.func.__name__ ), 
                usuario_registro = request.user.id
            )
            
            print(f"Error: {e}")

            return JsonResponse({'resultado': f'error {str(e)}'})

    else:
        return render(request, '404.html')
        
def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect(reverse('inicio'))

@login_required()
@csrf_exempt
def ajax_editar_contrasena_actual(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest': 
        if str( request.POST.get('txtContrasenaNueva') ) == str( request.POST.get('txtContrasenaConfirmar') ):
            try:
                User.objects.filter(pk = request.user.id).update(password = make_password( request.POST.get('txtContrasenaNueva') ))

                update_session_auth_hash(request, User.objects.get(pk = request.user.id))
                
            except BaseException as e:
                return JsonResponse({'resultado': str(e)})
            else:
                return JsonResponse({'resultado': 'true'})
        else:
            return JsonResponse({'resultado': 'false'})
    else:
        return render(request, '404.html')

@login_required
@minified_response
def inicio_administracion(request):
    return render(request, 'inicio_administracion.html')


@login_required
@csrf_exempt
def ajax_obtener_imagen_google_cloud(request):
	if request.method == "GET" and request.headers.get('x-requested-with') == 'XMLHttpRequest': 
		try:
			direccionImagen = str(request.GET.get('direccionImagen'))

			if default_storage.exists(direccionImagen) == True:
				storage_client = storage.Client()
				bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
				blob = bucket.blob(direccionImagen)

				imagenNube = blob.generate_signed_url(
					version = "v4",
					expiration = datetime.timedelta(minutes = 15),
					method = "GET"
				)
			else:
				return JsonResponse({'resultado': 'imagenNoEncontrada'})

		except BaseException as e:
			almacenarErroresExcepciones(
				descripcion_error = str(e), 
				aplicacion_id = 11,
				nombre_area = str( request.resolver_match.func.__name__ ), 
				usuario_registro = request.user.id
			)

			return JsonResponse({'resultado': 'false'})

		else:
			return JsonResponse({'resultado': 'true', 'imagenNube': imagenNube})

	else:
		return render(request, '404.html')

################################################################################################
################################################################################################
                            #CRUD: GALERÍA DE LA EMPRESA
################################################################################################
################################################################################################
@login_required
@minified_response
def gestion_galeria_empresa(request):
    if verificarPermiso(request, request.resolver_match.func.__name__):
        return render(request, 'sin_permiso.html', {'vista': request.resolver_match.func.__name__, 'url_anterior': request.META.get('HTTP_REFERER', None) or '/'})
    
    form = Galeria_EmpresaForm()
    return render(request, 'gestion_galeria_empresa.html', {'form':form})


@login_required
def ajax_gestion_galeria_empresa_listar(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            return JsonResponse(list(Galeria_Empresa.objects.all().order_by('orden').values('id', 'contenido', 'orden', 'imagen', 'estado')), safe = False)
        
        except BaseException as e:
            return JsonResponse(({'error': 'No se han cargado los datos en la tabla'}), safe = False)
    else:
        return redirect(reverse('inicio'))


@login_required
def ajax_gestion_galeria_empresa_agregar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest' and not request.POST.get('dato_pk'):
        data_form, data_json = request.POST.copy(), {}
        data_form['estado'] = True
        
        try:
            with transaction.atomic(using = 'finsurhn_ws_db'):
                galeria = Galeria_Empresa.objects.all()
                if galeria:
                    data_form['orden'] = int(galeria.count()) + 1
                else:
                    data_form['orden'] = 1

                # Pasando los datos a un modelForm para válidar si es un formulario válido
                form = Galeria_EmpresaForm(data = data_form, files = request.FILES)
                
                if form.is_valid():
                    form.save()
                    data_json.update({'exito': 'Se han Agregado Nuevos Datos'})
                    return JsonResponse((data_json), safe = False)
                else:
                    data_json.update({'error': 'No se han Agregado Nuevos Datos'})
                    return JsonResponse((data_json), safe = False)
        
        except DatabaseError as errorInterno:
            raise errorInterno #LOS ERRORES VAN A DAR A BaseException

        except BaseException as e:
            almacenarErroresExcepciones(
                descripcion_error = str(e), 
                aplicacion_id = 11,
                nombre_area = str( request.resolver_match.func.__name__ ), 
                usuario_registro = request.user.id
            )
            data_json.update({'error': 'No se han Agregado Nuevos Datos'})
            return JsonResponse((data_json), safe = False)
    else:
        return redirect(reverse('inicio'))

@login_required
def ajax_gestion_galeria_empresa_editar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json, form, data_form = {}, {}, request.POST
                
        try:
            if 'dato_pk' in data_form and data_form['dato_pk'].isnumeric() == True:
                galeria = Galeria_Empresa.objects.get( id = int(data_form['dato_pk']) )
                
                # IMPORTANTE!!!
                # NO colocar la instancia galeria en el form ejemplo: form( instance = galeria )
                # Si se coloca la instancia ocasiona problemas, NO podrá borrar la imagen con os.remove()
                # Al parecer en algunas ocasiones es mejor NO poner una instancia que se almecene en una variable dentro del form
                form = Galeria_EmpresaForm( data = data_form, files = request.FILES, instance = Galeria_Empresa.objects.get(id = int(data_form['dato_pk'])) )
                del form.fields['estado'] # Eliminando la fila de estado para que no se valide
                
                # Eliminando 'filas' del formulario
                del form.fields['orden']
                #del form.fields['estado'] 
                
                if not request.FILES.get('imagen'):
                    del form.fields['imagen']
                
                if form.is_valid():
                    if request.FILES.get('imagen') != None:
                        if default_storage.exists( str(galeria.imagen) ) == True:
                            default_storage.delete( str(galeria.imagen) )
                    
                    form.save()
                    data_json.update({'exito': 'Se han Actualizado los Datos'})
                    return JsonResponse((data_json), safe = False)
                else:
                    data_json.update({'error': 'No se han Actualizado los Datos'})
                    return JsonResponse((data_json), safe = False)
            else:
                data_json.update({'error': 'Key no Válida'})
                return JsonResponse((data_json), safe = False)
                
        except ValueError as e:
            data_json.update({'error': 'Hubo una Excepción, no se ha Actualizado'})
            return JsonResponse((data_json), safe = False)
    else:
       return redirect(reverse('inicio'))
    

@login_required
@csrf_exempt
def ajax_gestion_galeria_empresa_editar_datagrid(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json = {}
        try:
            if 'key' in request.POST and request.POST['key'].isnumeric() == True:
                
                # Si viene la lista de datos en el POST
                if request.POST.getlist('data')[0]:
                    datos_list = json.loads(request.POST.getlist('data')[0])

                    # Creando instancia de objeto a guardar
                    galeria_empresa = Galeria_Empresa.objects.get( id = int(request.POST['key']) )
                    
                    # Si viene orden y si es numerico
                    if 'orden' in datos_list:
                        galeria_empresa.orden = int(datos_list['orden'])
                    
                    if 'estado' in datos_list:
                        galeria_empresa.estado = int(datos_list['estado'])
                        
                    # GUARDANDO
                    try:
                        galeria_empresa.save()
                        data_json.update({'exito': 'Se han Actualizado los Datos'})
                        return JsonResponse((data_json), safe = False)
                    except ValueError as e:
                        data_json.update({'error': 'No se han Actualizado los Datos'})
                        return JsonResponse((data_json), safe = False)
                else:
                    data_json.update({'error': 'Datos no Válidos'})
                    return JsonResponse((data_json), safe = False)

            else:
                data_json.update({'error': 'Key no Válida'})
                return JsonResponse((data_json), safe = False)
                
        except Exception as e:
            data_json.update({'error': 'Hubo una Excepción, no se ha Actualizado'})
            return JsonResponse((data_json), safe = False)
    else:
        return redirect(reverse('inicio'))
    
    
@login_required
@csrf_exempt
def ajax_gestion_galeria_empresa_editar_orden(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json = {}
        try:
            if 'key' in request.POST and request.POST['key'].isnumeric() == True:

                # Creando instancia de objeto a guardar
                info_empleo = Informacion_Empleo.objects.get( id = int(request.POST['key']) )

                # Si viene la lista de datos en el POST
                if request.POST.getlist('data')[0]:
                    datos_list = json.loads(request.POST.getlist('data')[0])

                    # Si viene orden y si es numerico
                    if 'orden' in datos_list:
                        info_empleo.orden = int(datos_list['orden'])

                    if 'estado' in datos_list:
                        info_empleo.estado = int(datos_list['estado'])

                    # GUARDANDO
                    try:
                        info_empleo.save()
                        data_json.update({'exito': 'Se han Actualizado los Datos'})
                        return JsonResponse((data_json), safe = False)
                    except ValueError as e:
                        data_json.update({'error': 'No se han Actualizado los Datos'})
                        return JsonResponse((data_json), safe = False)

                else:
                    data_json.update({'error': 'Datos no Válidos'})
                    return JsonResponse((data_json), safe = False)

            else:
                data_json.update({'error': 'Key no Válida'})
                return JsonResponse((data_json), safe = False)

        except Exception as e:
            data_json.update({'error': 'Hubo una Excepción, no se ha Actualizado'})
            return JsonResponse((data_json), safe = False)
    else:
        return redirect(reverse('inicio'))
    
@login_required
@csrf_exempt
def ajax_gestion_galeria_empresa_eliminar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json, data_form = {}, request.POST.copy()
        try:
            if 'dato_pk' in data_form and data_form['dato_pk'].isnumeric() == True:
                galeria = Galeria_Empresa.objects.get(id=int(data_form['dato_pk']))
                # Eliminar la imagen si existe
                if galeria.imagen and default_storage.exists(str(galeria.imagen)):
                    default_storage.delete(str(galeria.imagen))
                galeria.delete()
                data_json.update({'exito': 'Se ha eliminado el registro correctamente'})
                return JsonResponse(data_json, safe=False)
            else:
                data_json.update({'error': 'Key no Válida'})
                return JsonResponse(data_json, safe=False)
        except Exception as e:
            data_json.update({'error': 'Hubo una Excepción, no se ha eliminado'})
            print(f"Error: {e}")
            return JsonResponse(data_json, safe=False)
    else:
        return redirect(reverse('inicio'))


################################################################################################
################################################################################################
                            # CRUD: VALORES DE LA EMPRESA
################################################################################################
################################################################################################
@login_required
@minified_response
def valores_empresa(request):
    if verificarPermiso(request, request.resolver_match.func.__name__):
        return render(request, 'sin_permiso.html', {'vista': request.resolver_match.func.__name__, 'url_anterior': request.META.get('HTTP_REFERER', None) or '/'})
    
    return render(request, 'valores_empresa.html')
    
@login_required   
@csrf_exempt 
def ajax_valores_empresa_listar(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            return JsonResponse(list(Valores_Empresa.objects.all().values('id', 'valor', 'descripcion').order_by('valor')), safe = False)

        except BaseException as e:
            return JsonResponse(({'error': 'No se han cargado los datos en la tabla'}), safe = False)
    else:
        return redirect(reverse('inicio'))
    
@login_required
@csrf_exempt 
def ajax_valores_empresa_agregar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json = {}
        try:            
            if request.POST.getlist('data')[0]:
                with transaction.atomic(using = 'finsurhn_ws_db'):
                    datos_list = json.loads(request.POST.getlist('data')[0])
                    
                    # Pasando los datos a un modelForm para válidar si es un formulario válido
                    form = Valores_EmpresaFrom(data = datos_list)
                    
                    if form.is_valid():
                        form.save()
                        data_json.update({'exito': 'Se han Agregado Nuevos Datos'});
                        return JsonResponse((data_json), safe = False)
                    
                    else:
                        data_json.update({'error': 'No se han Agregado Nuevos Datos'})
                        return JsonResponse((data_json), safe = False)
                    
            else:
                data_json.update({'error': 'Datos no válidos'})
                return JsonResponse((data_json), safe = False)
            
        except DatabaseError as errorInterno:
            raise errorInterno #LOS ERRORES VAN A DAR A BaseException

        except BaseException as e:
            almacenarErroresExcepciones(
                descripcion_error = str(e), 
                aplicacion_id = 11,
                nombre_area = str( request.resolver_match.func.__name__ ), 
                usuario_registro = request.user.id
            )
            data_json.update({'error': 'Hubo una excepción, no se han agregado nuevos datos'})
            return JsonResponse((data_json), safe = False)
    else:
        return redirect(reverse('inicio'))


@login_required
@csrf_exempt 
def ajax_valores_empresa_editar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json = {}
    
        try:
            if 'key' in request.POST and request.POST['key'].isnumeric() == True:
                
                if request.POST.getlist('data')[0]:
                    with transaction.atomic(using = 'finsurhn_ws_db'):
                        datos_list, data_json = json.loads(request.POST.getlist('data')[0]), {}
                        
                        valor = Valores_Empresa.objects.get(id=int(request.POST['key']))
                        
                        # Pasando los datos a un modelForm para válidar si es un formulario válido
                        form = Valores_EmpresaFrom(data = datos_list, instance=valor)
                        
                        if not 'valor' in datos_list:
                            del form.fields['valor']
                        if not 'descripcion' in datos_list:
                            del form.fields['descripcion']
                        
                        if form.is_valid():
                            form.save()
                            data_json.update({'exito': 'Se han Actualizado los Datos'});
                            return JsonResponse((data_json), safe = False)
                        else:
                            data_json.update({'error': 'No se han Actualizado los Datos'})
                            return JsonResponse((data_json), safe = False)
                else:
                    data_json.update({'error': 'Datos no válidos'})
                    return JsonResponse((data_json), safe = False)
            else:
                data_json.update({'error': 'Key no Válida'})
                return JsonResponse((data_json), safe = False)
                
        except DatabaseError as errorInterno:
            raise errorInterno #LOS ERRORES VAN A DAR A BaseException

        except BaseException as e:
            almacenarErroresExcepciones(
                descripcion_error = str(e), 
                aplicacion_id = 11,
                nombre_area = str( request.resolver_match.func.__name__ ), 
                usuario_registro = request.user.id
            )
            data_json.update({'error': 'Hubo una Excepción, no se ha Actualizado'})
            return JsonResponse((data_json), safe = False)
    else:
        return redirect(reverse('inicio'))
    
@login_required
@csrf_exempt 
def ajax_valores_empresa_eliminar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json = {}

        try:
            with transaction.atomic(using = 'finsurhn_ws_db'):
                if 'key' in request.POST and request.POST['key'].isnumeric() == True:
                    valores = Valores_Empresa.objects.get(id = int(request.POST['key']))
                    valores.delete()
                else:
                    data_json.update({'error': 'Key no Válida'})
                    
        except DatabaseError as errorInterno:
            raise errorInterno #LOS ERRORES VAN A DAR A BaseException

        except BaseException as e:
            almacenarErroresExcepciones(
                descripcion_error = str(e), 
                aplicacion_id = 11,
                nombre_area = str( request.resolver_match.func.__name__ ), 
                usuario_registro = request.user.id
            )

            data_json.update({'error': 'Hubo una excepción, no se han elimninado los datos'});
            return JsonResponse((data_json), safe = False)
        
        else:
            data_json.update({'exito': 'Se han eliminado los datos'});
            return JsonResponse((data_json), safe = False)

    else:
        return redirect(reverse('inicio'))
    

################################################################################################
################################################################################################
                            # CRUD: REDES SOCIALES DE LA EMPRESA 
################################################################################################
################################################################################################
@login_required
@minified_response
def redes_sociales_empresa(request):
    if verificarPermiso(request, request.resolver_match.func.__name__):
        return render(request, 'sin_permiso.html', {'vista': request.resolver_match.func.__name__, 'url_anterior': request.META.get('HTTP_REFERER', None) or '/'})
    
    return render(request, 'redes_sociales_empresa.html', {'form': Redes_SocialesForm()})    

@login_required
def ajax_redes_sociales_empresa_listar(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            redes_sociales = list(Redes_Sociales.objects.all().values('id', 'nombre', 'imagen', 'link', 'orden', 'estado'))
            return JsonResponse((redes_sociales), safe = False)
        
        except BaseException as e:
            return JsonResponse(({'error': 'No se han cargado los datos en la tabla'}), safe = False)
    else:
        return redirect(reverse('inicio'))
    

@login_required
def ajax_redes_sociales_empresa_agregar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest' and not request.POST.get('dato_pk'):
        data_form, data_json = request.POST.copy(), {}
        data_form['estado'] = True
        
        try:
            with transaction.atomic(using = 'finsurhn_ws_db'):
                redes_sociales = Redes_Sociales.objects.all()

                # Se validan que datos vienen en el POST, para posteriormente poder guardar los cambios
                if redes_sociales:
                    data_form['orden'] = int(redes_sociales.count()) + 1
                else:
                    data_form['orden'] = 1

                # Pasando los datos a un modelForm para válidar si es un formulario válido
                form = Redes_SocialesForm(data = data_form, files = request.FILES)
                
                if form.is_valid():
                    form.save()
                    data_json.update({'exito': 'Se han Agregado Nuevos Datos'})
                    return JsonResponse((data_json), safe = False)
                else:
                    data_json.update({'error': 'No se han Agregado Nuevos Datos'})
                    return JsonResponse((data_json), safe = False)
                
        except DatabaseError as errorInterno:
            raise errorInterno #LOS ERRORES VAN A DAR A BaseException

        except BaseException as e:
            almacenarErroresExcepciones(
                descripcion_error = str(e), 
                aplicacion_id = 11,
                nombre_area = str( request.resolver_match.func.__name__ ), 
                usuario_registro = request.user.id
            )
            data_json.update({'error': 'Hubo una Excepción, no se ha Actualizado'})
            return JsonResponse((data_json), safe = False)
    else:
        return redirect(reverse('inicio'))
    
    
@login_required
def ajax_redes_sociales_empresa_editar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json, form, data_form = {}, {}, request.POST.copy()  
        
        try:
            if 'dato_pk' in data_form and data_form['dato_pk'].isnumeric() == True:
                redes_sociales = Redes_Sociales.objects.get( id = int(data_form['dato_pk']) )
                
                # IMPORTANTE!
                # NO colocar la instancia prod_serv en el form ejemplo: form( instance = prod_serv ) NO podrá borrar la imagen con os.remove()
                form = Redes_SocialesForm( data = data_form, files = request.FILES, instance = Redes_Sociales.objects.get(id = int(data_form['dato_pk'])) )
                
                #Borrando 'filas' del formulario
                del form.fields['orden']
                del form.fields['estado']
                
                if form.is_valid():
                    if request.FILES.get('imagen') != None:
                        if default_storage.exists( str(redes_sociales.imagen) ) == True:
                            default_storage.delete( str(redes_sociales.imagen) )
                    
                    form.save()
                    data_json.update({'exito': 'Se han Actualizado los Datos'})
                    return JsonResponse((data_json), safe = False)
                
                else:
                    data_json.update({'error': 'No se han Actualizado los Datos'})
                    return JsonResponse((data_json), safe = False)
            
            else:
                data_json.update({'error': 'Key no Válida'})
                return JsonResponse((data_json), safe = False)
                
        except Exception as e:
            data_json.update({'error': 'Hubo una Excepción, no se ha Actualizado'})
            return JsonResponse((data_json), safe = False)
    else:
        return redirect(reverse('inicio'))

@login_required
@csrf_exempt
def ajax_redes_sociales_empresa_editar_datagrid(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json = {}
        try:
            if 'key' in request.POST and request.POST['key'].isnumeric() == True:
                
                 # Si viene la lista de datos en el POST
                if request.POST.getlist('data')[0]:
                    datos_list = json.loads(request.POST.getlist('data')[0])
                
                    # Creando instancia de objeto a guardar
                    redes_sociales = Redes_Sociales.objects.get( id = int(request.POST['key']) )
                    
                    # Si viene orden y si es numerico
                    if 'orden' in datos_list:
                        redes_sociales.orden = int(datos_list['orden'])
                    
                    if 'estado' in datos_list:
                        redes_sociales.estado = int(datos_list['estado'])
                        
                    # GUARDANDO
                    try:
                        redes_sociales.save()
                        data_json.update({'exito': 'Se han Actualizado los Datos'})
                        return JsonResponse((data_json), safe = False)
                    except ValueError as e:
                        data_json.update({'error': 'No se han Actualizado los Datos'})
                        return JsonResponse((data_json), safe = False)
                        
                else:
                    data_json.update({'error': 'Datos no válidos'})
                    return JsonResponse((data_json), safe = False)

            else:
                data_json.update({'error': 'Key no Válida'})
                return JsonResponse((data_json), safe = False)
                
        except BaseException as e:
            data_json.update({'error': 'Hubo una Excepción, no se ha Actualizado'})
            return JsonResponse((data_json), safe = False)
    else:
        return redirect(reverse('inicio'))
    
@login_required
@csrf_exempt
def ajax_redes_sociales_empresa_eliminar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json, data_form = {}, request.POST.copy()
        try:
            if 'dato_pk' in data_form and data_form['dato_pk'].isnumeric() == True:
                red_social = Redes_Sociales.objects.get(id=int(data_form['dato_pk']))
                # Eliminar la imagen si existe
                if red_social.imagen and default_storage.exists(str(red_social.imagen)):
                    default_storage.delete(str(red_social.imagen))
                red_social.delete()
                data_json.update({'exito': 'Se ha eliminado el registro correctamente'})
                return JsonResponse(data_json, safe=False)
            else:
                data_json.update({'error': 'Key no Válida'})
                return JsonResponse(data_json, safe=False)
        except Exception as e:
            data_json.update({'error': 'Hubo una Excepción, no se ha eliminado'})
            print(f"Error: {e}")
            return JsonResponse(data_json, safe=False)
    else:
        return redirect(reverse('inicio')) 
    
    

################################################################################################
################################################################################################
                    # FORMULARIO CONTACTANOS -- INICIO -- SESIÓN NO INICIADA #
################################################################################################
################################################################################################

@csrf_exempt
def ajax_contactanos(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data, form = {}, {} 
        try:
            form = ContactForm(data=request.POST)
            
            if form.is_valid():
                
                titulo = 'Comentario - Finsurhn_Website'
                correo_remitente = settings.EMAIL_HOST_USER
                correo_destinatario = 'esli.mendoza@uph.edu.hn'

                mensaje_correo = f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ 
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }}
            .container {{ 
                max-width: 600px;
                background-color: #fff;
                margin: auto;
                border-radius: 10px;
                border: #333333 solid 1px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .header {{
                text-align: center;
                background-color: #F0910C;
                color: #ffffff;
                padding: 15px;
                border-radius: 8px 8px 0 0;
            }}
            .header h2 {{
                margin: 0;
            }}
            .content {{
                padding: 10px 10px;
                color: #333333;
            }}
            .content p {{
                margin: 10px 0;
            }}
            .footer {{
                text-align: center;
                font-size: 12px;
                color: #888888;
                margin-top: 30px;
                border-top: 1px solid #eeeeee;
                padding-top: 10px;
                padding-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Información de Contacto</h2>
            </div>
            <div class="content">
                <p><strong>Nombre:</strong> {form.cleaned_data['nombre']}</p>
                <p><strong>Apellido:</strong> {form.cleaned_data['apellido']}</p>
                <p><strong>Correo Electrónico:</strong> {form.cleaned_data['email']}</p>
                <hr>
                <h2 style="text-align: center;"><strong>Mensaje:</strong></h2>
                <p>
                    {form.cleaned_data['mensaje']}
                </p>
            </div>
            <div class="footer">
            Inversiones Financieras del Sur © 2025
            </div>
        </div>
    </body>
    </html>
    '''
                try:  
                    nueva_consulta = Consulta(
                        nombre=form.cleaned_data['nombre'],
                        apellido=form.cleaned_data['apellido'],
                        correo=form.cleaned_data['email'],
                        mensaje=form.cleaned_data['mensaje'],
                    )
                    nueva_consulta.save()
                    email = EmailMessage(
                        titulo,
                        mensaje_correo,
                        correo_remitente,
                        [correo_destinatario],
                    )
                    email.content_subtype = "html"
                    email.send()
                    
                    return JsonResponse({'exito': 'Su solicitud de contacto ha sido enviada'}, safe = False)
                
                except Exception as e:
                    if str(type(e)) == "<class 'smtplib.SMTPAuthenticationError'>":
                        # Autorización de aplicaciones poco seguras
                        # https://myaccount.google.com/lesssecureapps

                        data.update({'error': 'Correo del sistema desactivado'})
                        return JsonResponse((data), safe = False)
                    else:
                        data.update({'error': 'Correo Electrónico inválido'})
                        print(f"error: {e}")
                        return JsonResponse((data), safe = False)
            else: 
                data.update({'exito': 'Su solicitud de contacto ha sido enviada'})
                return JsonResponse((data), safe = False)
            
        except BaseException as e:
            data.update({'error': 'Hubo una excepción, no se ha actualizado'})
            return JsonResponse((data), safe = False)
    else:
        return redirect(reverse("inicio"))

@csrf_exempt
def ajax_solicitud_credito(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data_json, info_solicitud, form  = {}, {}, SolicitudForm(request.POST)
        try:
            sucursal_choices = dict(SolicitudForm.SUCURSALES[1:])
            forma_pago_choices = dict(SolicitudForm.FORMAS_PAGO[1:])
            
            info_solicitud = {
                'identificacion' : request.POST.get('identificacion', ''),
                'primerNombre' : request.POST.get('primerNombre', ''),
                'segundoNombre' : request.POST.get('segundoNombre', ''),
                'primerApellido' : request.POST.get('primerApellido', ''),
                'segundoApellido' : request.POST.get('segundoApellido', ''),
                'correo' : request.POST.get('correo', ''),
                'sucursal' : {
                    'id' : request.POST.get('sucursal', ''),
                    'nombre': sucursal_choices.get(request.POST.get('sucursal'), '')}, 
                'celular' : request.POST.get('celular', ''),
                'direccion' : request.POST.get('direccion', ''),
                'formaPago' : {
                    'id' : request.POST.get('formaDePago', ''),
                    'nombre' : forma_pago_choices.get(request.POST.get('formaDePago'), '')},
                'montoSolicitado' : request.POST.get('montoSolicitado', ''),
                'descripcionTipoIngreso' : request.POST.get('descripcionTipoIngreso', '')
            }
            
            if form.is_valid():
                
                identificacion = request.POST.get('identificacion')
                
                if Solicitud.objects.filter(identificacion=identificacion).exists():
                    return JsonResponse({
                        'error': 'El número de identificación ya está registrado.'
                    }, status=400, safe=False)
                
                try:
                    sucursal = Sucursal.objects.get(id=request.POST.get('sucursal'))    
                    forma_pago = FormaPago.objects.get(id=request.POST.get('formaDePago'))    
                    nueva_solicitud = Solicitud(
                        identificacion=identificacion,
                        primerNombre=request.POST.get('primerNombre'),
                        segundoNombre=request.POST.get('segundoNombre'),
                        primerApellido=request.POST.get('primerApellido'),
                        segundoApellido=request.POST.get('segundoApellido'),
                        correo=request.POST.get('correo'),
                        sucursal=sucursal,
                        celular=request.POST.get('celular'),
                        direccion=request.POST.get('direccion'),
                        formaPago=forma_pago,
                        montoSolicitado=request.POST.get('montoSolicitado'),
                        descripcionTipoIngreso=request.POST.get('descripcionTipoIngreso')
                    )
                    nueva_solicitud.save()
                    #ENVIAR CORREO ELECTRÓNICO
                    titulo = 'Solicitud de Crédito - Finsurhn_Website'
                    correo_remitente = settings.EMAIL_HOST_USER
                    correo_destinatario = 'esli.mendoza@uph.edu.hn'
                    mensaje_correo = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style type="text/css">
            body {{
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                text-align: center;
                margin-bottom: 25px;
                border-bottom: 2px solid #FFB412;
                padding-bottom: 10px;
            }}
            .card {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 15px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }}
            h2 {{
                color: #2C2C2C;
                margin: 0;
            }}
            h3 {{
                color: #8d8282;
                margin-top: 0;
                border-bottom: 1px dashed #2C2C2C;
                font-size: 1.3rem;
                padding-bottom: 5px;
                display: inline-block;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                color: #7f8c8d;
                font-size: 0.9em;
            }}
            .logo {{
                max-width: 150px;
                margin-bottom: 15px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <img src="https://i.postimg.cc/jShL9tFg/LOGO-COMPLETO.png" alt="Logo Finsur" class="logo">
            <h2>INFORMACIÓN DE SOLICITUD DE CRÉDITO</h2>
        </div>
        
        <div class="card">
            <h3>📌 Datos Personales</h3>
            <p><strong>No. Identidad:</strong> {info_solicitud['identificacion']}</p>
            <p><strong>Nombre Completo:</strong> {info_solicitud['primerNombre']} {info_solicitud['segundoNombre']} {info_solicitud['primerApellido']} {info_solicitud['segundoApellido']}</p>
            <p><strong>Celular:</strong> {info_solicitud['celular']}</p>
        </div>
        
        <div class="card">
            <h3>🏦 Datos del Crédito</h3>
            <p><strong>Sucursal:</strong> {info_solicitud['sucursal']['nombre']}</p>
            <p><strong>Forma de Pago:</strong> {info_solicitud['formaPago']['nombre']}</p>
            <p><strong>Monto Solicitado:</strong> L. {float(info_solicitud['montoSolicitado']):,.2f}</p>
        </div>
        
        <div class="card" style="background: #fff; border: 1px solid #eee;">
            <h3>📝 Descripción del Tipo de Ingreso</h3>
            <p style="white-space: pre-line; background: #fff; padding: 10px; border-radius: 4px;">{info_solicitud['descripcionTipoIngreso']}</p>
        </div>
        
        <div class="footer">
            <p>Solicitud recibida el: {timezone.now().strftime('%d/%m/%Y a las %H:%M')}</p>
            <p style="font-size: 0.8em; margin-top: 5px;">© {timezone.now().year} Inversiones Financieras del Sur © 2025</p>
        </div>
    </body>
    </html>
    '''
                    email = EmailMessage(
                        titulo,
                        mensaje_correo,
                        correo_remitente,
                        [correo_destinatario],
                    )
                    email.content_subtype = "html"
                    email.send()
                    return JsonResponse({'exito': 'Su solicitud de contacto ha sido enviada'}, safe=False)
                except Exception as e:
                    # print(f"Error al guardar o enviar correo: {e}")
                    if str(type(e)) == "<class 'smtplib.SMTPAuthenticationError'>":
                        return JsonResponse({'error': 'Correo del sistema desactivado'}, safe=False)
                    else:
                        return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500, safe=False)
            else:
                return JsonResponse({'error': 'Datos del formulario inválidos', 'detalles': form.errors}, status=400, safe=False)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': str(e)}, status=500, safe=False)
    else:
        return redirect(reverse("aplicar-solicitud"))


################################################################################################
################################################################################################
                            # CRUD: INFORMACIÓN Y EMPLEO
################################################################################################
################################################################################################

#####################################  NO LOGUEADO  ############################################
@minified_response
def informacion_empleo_vacantes(request):
    lista_empleo = []
    for ie in Informacion_Empleo.objects.filter(estado = True).order_by('orden').exclude(num_vacantes = 0):
        info_empleo = {}
        info_empleo.update({
            'id': ie.id,
            'idcargo': ie.idcargo,
            'cargo': Cargo.objects.get(id = int(ie.idcargo)).cargo,
            'descripcion': ie.descripcion,
            'num_vacantes': ie.num_vacantes,
            'ciudad': ie.ciudad,
            'orden': ie.orden,
            'imagen': ie.imagen,
            'estado': ie.estado
        })
        lista_empleo.append(info_empleo)
    
    return render(request, 'informacion_empleo_vacantes.html', {'info_empleo': lista_empleo} )


@minified_response
def informacion_empleo_vacante_info(request, dato_pk):
    info_empleo = {}
    
    for ie in Informacion_Empleo.objects.filter(id = int(dato_pk), estado = True):
        info_empleo.update({
            'id': ie.id,
            'idcargo': ie.idcargo,
            'cargo': Cargo.objects.get(id = int(ie.idcargo)).cargo,
            'descripcion': ie.descripcion,
            'num_vacantes': ie.num_vacantes,
            'ciudad': ie.ciudad,
            'orden': ie.orden,
            'imagen': ie.imagen,
            'estado': ie.estado
        })

    cant_empleos = len(Informacion_Empleo.objects.filter(estado = True).order_by('orden').exclude(num_vacantes = 0))
    form = empleo_contactoForm()
    return render(request, 'informacion_empleo_vacante_info.html', {'info_empleo':info_empleo, 'cant_empleos':cant_empleos, 'form':form})

@csrf_exempt 
def ajax_informacion_empleo_vacante_correo(request, dato_pk):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json, form, info_empleo = {}, {}, {}
        try:
            for ie in Informacion_Empleo.objects.filter(id = int(dato_pk), estado = True):
                info_empleo = {
                    'id': ie.id,
                    'idcargo': ie.idcargo,
                    'cargo': str(Cargo.objects.get(id = int(ie.idcargo)).cargo),
                    'descripcion': ie.descripcion,
                    'num_vacantes': ie.num_vacantes,
                    'ciudad': ie.ciudad,
                    'orden': ie.orden,
                    'imagen': ie.imagen,
                    'estado': ie.estado
                }       
            form = empleo_contactoForm(data=request.POST, files=request.FILES)
            
            if form.is_valid():                  
                
                name = 'Sistema: Finsurhn_Website'
                correo_remitente = settings.EMAIL_HOST_USER
                correo_destinatario = 'esli.mendoza@uph.edu.hn'
                mensaje_correo = '''
                    
 INFORMACIÓN DE EMPLEO
Finsurhn Website System

Cargo: '''+ info_empleo['cargo'] + '''
Ciudad: '''+ info_empleo['ciudad'] + '''
Vacantes: '''+ str(info_empleo['num_vacantes']) + '''

Nombre Completo: '''+ form.cleaned_data['nombre_completo'] + '''
Número de Identidad: '''+ form.cleaned_data['num_identidad'] + '''
Ciudad: '''+ form.cleaned_data['ciudad'] + '''
Correo Electrónico: '''+ form.cleaned_data['correo'] + '''
Número de Teléfono: '''+ form.cleaned_data['telefono'] + '''
Número de Celular: ''' + form.cleaned_data['celular'] + '''

CONSULTA DE REMITENTE: 
''' + form.cleaned_data['asunto'] + '''
'''
                
                try:
                    archivo = request.FILES['curriculum']
                    mail = EmailMessage(name, mensaje_correo, correo_remitente, [correo_destinatario])
                    mail.attach(archivo.name, archivo.read(), archivo.content_type)
                    mail.send()
                    
                    print(f"El correo con titulo: {name} ha sido enviado correctamente")
                except Exception as e:
                    if str(type(e)) == "<class 'smtplib.SMTPAuthenticationError'>":
                        # Autorización de aplicaciones poco seguras
                        # https://myaccount.google.com/lesssecureapps
                        
                        data_json.update({'error': 'Correo del sistema desactivado'})
                        return JsonResponse((data_json), safe = False)
                    
                    else:
                        data_json.update({'error': 'Correo Electrónico inválido'})
                        print(f"error: {e}")
                        return JsonResponse((data_json), safe = False)
                
                else:
                    data_json.update({'exito': 'Su solicitud de contacto ha sido enviada'})
                    return JsonResponse((data_json), safe = False)

            else:
                data_json.update({'error': 'Datos inválido, su solicitud no ha sido enviada, lo sentimos'})
                return JsonResponse((data_json), safe = False)
        
        except ValueError as e:
            data_json.update({'error': 'Hubo una excepción, correo no enviado'})
            return JsonResponse((data_json), safe = False)
        
    else:
        return redirect(reverse('inicio'))
    

#########################################  LOGUEADO  ###############################################
@login_required
@minified_response
def informacion_empleo(request):
    if verificarPermiso(request, request.resolver_match.func.__name__):
        return render(request, 'sin_permiso.html', {'vista': request.resolver_match.func.__name__, 'url_anterior': request.META.get('HTTP_REFERER', None) or '/'})
    
    return render(request, 'informacion_empleo.html', {'form': Informacion_EmpleoForm()})

@login_required
@csrf_exempt
def ajax_informacion_empleo_listar(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            info_empleo = list(Informacion_Empleo.objects.all().order_by('orden').values('id', 'idcargo', 'descripcion', 'ciudad', 'num_vacantes', 'orden', 'estado', 'imagen'))
            return JsonResponse((info_empleo), safe = False)
        
        except BaseException as e:
            return JsonResponse(({'error': 'No se han cargado los datos en la tabla'}), safe = False)
    else:
        return redirect(reverse('inicio'))
    
@login_required
@csrf_exempt
def ajax_informacion_empleo_agregar(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_form, data_json = request.POST.copy(), {}
        data_form['estado'] = True
        try:
            with transaction.atomic(using = 'finsurhn_ws_db'):
                info = Informacion_Empleo.objects.all()
                if info:
                    data_form['orden'] = int(info.count()) + 1
                else:
                    data_form['orden'] = 1
                    
                # Pasando los datos a un modelForm para válidar si es un formulario válido
                form = Informacion_EmpleoForm(data = data_form, files = request.FILES)
                
                if form.is_valid():
                    form.save()
                    data_json.update({'exito': 'Se han Agregado Nuevos Datos'})
                    return JsonResponse((data_json), safe = False)
                else:
                    data_json.update({'error': 'No se han Agregado Nuevos Datos'})
                    return JsonResponse((data_json), safe = False)
                
        except DatabaseError as errorInterno:
            raise errorInterno #LOS ERRORES VAN A DAR A BaseException

        except BaseException as e:
            almacenarErroresExcepciones(
                descripcion_error = str(e), 
                aplicacion_id = 11,
                nombre_area = str( request.resolver_match.func.__name__ ), 
                usuario_registro = request.user.id
            )
            data_json.update({'error': 'Hubo una Excepción, no se ha Actualizado'})
            return JsonResponse((data_json), safe = False)
    else:
        return redirect(reverse('inicio'))
    
@login_required
@csrf_exempt
def ajax_informacion_empleo_editar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json, form, data_form = {}, {}, request.POST.copy()
        
        try:
            if 'dato_pk' in data_form and data_form['dato_pk'].isnumeric() == True:
                
                # Instancia galeria
                info_emplo = Informacion_Empleo.objects.get( id = int(data_form['dato_pk']) )
                
                # IMPORTANTE!
                # NO colocar la instancia prod_serv en el form ejemplo: form( instance = prod_serv ) NO podrá borrar la imagen con os.remove()
                form = Informacion_EmpleoForm( data = data_form, files = request.FILES, instance = Informacion_Empleo.objects.get(id = int(data_form['dato_pk'])) )
                
                #Borrando 'filas' del formulario
                del form.fields['orden']
                del form.fields['estado']
                
                if form.is_valid():
                    if request.FILES.get('imagen') != None:
                        if default_storage.exists( str(info_emplo.imagen) ) == True:
                            default_storage.delete( str(info_emplo.imagen) )
              
                    form.save()
                    data_json.update({'exito': 'Se han Actualizado los Datos'})
                    return JsonResponse((data_json), safe = False)
                
                else:
                    data_json.update({'error': 'No se han Actualizado los Datos'})
                    return JsonResponse((data_json), safe = False)

            else:
                data_json.update({'error': 'Key no Válida'})
                return JsonResponse((data_json), safe = False)
                
        except Exception as e:
            data_json.update({'error': 'Hubo una Excepción, no se ha Actualizado'})
            return JsonResponse((data_json), safe = False)

    else:
        return redirect(reverse('inicio'))
    

@login_required
@csrf_exempt
def ajax_informacion_empleo_editar_datagrid(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json = {}
        try:
            if 'key' in request.POST and request.POST['key'].isnumeric() == True:
                
                # Si viene la lista de datos en el POST
                if request.POST.getlist('data')[0]:
                    datos_list = json.loads(request.POST.getlist('data')[0])

                    # Creando instancia de objeto a guardar
                    info_empleo = Informacion_Empleo.objects.get( id = int(request.POST['key']) )
                    
                    # Si viene orden y si es numerico
                    if 'orden' in datos_list:
                        info_empleo.orden = int(datos_list['orden'])
                    
                    if 'estado' in datos_list:
                        info_empleo.estado = int(datos_list['estado'])
                        
                    # GUARDANDO
                    try:
                        info_empleo.save()
                        data_json.update({'exito': 'Se han Actualizado los Datos'})
                        return JsonResponse((data_json), safe = False)
                    except ValueError as e:
                        data_json.update({'error': 'No se han Actualizado los Datos'})
                        return JsonResponse((data_json), safe = False)
                else:
                    data_json.update({'error': 'Datos no Válidos'})
                    return JsonResponse((data_json), safe = False)

            else:
                data_json.update({'error': 'Key no Válida'})
                return JsonResponse((data_json), safe = False)
                
        except Exception as e:
            data_json.update({'error': 'Hubo una Excepción, no se ha Actualizado'})
            return JsonResponse((data_json), safe = False)
    else:
        return redirect(reverse('inicio'))
    
@login_required
@csrf_exempt
def ajax_informacion_empleo_eliminar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json, data_form = {}, request.POST.copy()
        try:
            if 'dato_pk' in data_form and data_form['dato_pk'].isnumeric() == True:
                info_emplo = Informacion_Empleo.objects.get(id=int(data_form['dato_pk']))
                # Eliminar la imagen si existe
                if info_emplo.imagen and default_storage.exists(str(info_emplo.imagen)):
                    default_storage.delete(str(info_emplo.imagen))
                info_emplo.delete()
                data_json.update({'exito': 'Se ha eliminado el registro correctamente'})
                return JsonResponse(data_json, safe=False)
            else:
                data_json.update({'error': 'Key no Válida'})
                return JsonResponse(data_json, safe=False)
        except Exception as e:
            data_json.update({'error': 'Hubo una Excepción, no se ha eliminado'})
            print(f"Error: {e}")
            return JsonResponse(data_json, safe=False)
    else:
        return redirect(reverse('inicio'))
    

################################################################################################
################################################################################################
                            # CRUD: SALA DE VIDEOS
################################################################################################
################################################################################################

@login_required
@minified_response
def sala_videos(request):
    # Verificar permiso
    if verificarPermiso(request, request.resolver_match.func.__name__):
        return render(request, 'sin_permiso.html', {'vista': request.resolver_match.func.__name__, 'url_anterior': request.META.get('HTTP_REFERER', None) or '/'})
    
    form = Sala_VideosForm()
    return render(request, 'sala_videos.html', {'form':form})

# La sala de video se muestra en la plantilla de inicio
def ajax_sala_videos_listar(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
            lista = []

            if 'dxTileVideo' in request.GET and int(request.GET.get('dxTileVideo')) == 1:
                sala_videos = Sala_Videos.objects.filter(estado = True).order_by('-fecha_creacion')
            
            elif 'dxTileVideo' in request.GET and int(request.GET.get('dxTileVideo')) == 2:
                sala_videos = Sala_Videos.objects.all().order_by('-fecha_creacion')

            for s in sala_videos:
                direccionImagenNube = str(s.imagen)
                if default_storage.exists(direccionImagenNube) == True:
                    blob = bucket.blob(direccionImagenNube)

                    imagenNube = blob.generate_signed_url(
                        version = "v4",
                        expiration = datetime.timedelta(hours = 1),
                        method = "GET"
                    )
                else:
                    imagenNube = ''

                lista.append({
                    'id': s.id, 
                    'nombre': s.nombre, 
                    'nombreImagen': str(s.imagen),
                    'imagen': imagenNube,
                    'link': s.link, 
                    'estado': s.estado
                })

            return JsonResponse(lista, safe = False)
        
        except BaseException as e:
            return JsonResponse(({'error': 'No se han cargado los datos en la tabla'}), safe = False)
            
    else:
        return redirect(reverse('inicio'))
    
    

@login_required
def ajax_sala_videos_agregar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest' and not request.POST.get('dato_pk'):
        data_form, data_json = request.POST.copy(), {}
        data_form['estado'] = request.POST.get('estado', False)
                
        try:
            with transaction.atomic(using = 'finsurhn_ws_db'):
                form = Sala_VideosForm(data = data_form, files = request.FILES)
                
                if form.is_valid():
                    form.save()
                    data_json.update({'exito': 'Se han Agregado Nuevos Datos'})
                    return JsonResponse((data_json), safe = False)
                else:
                    data_json.update({'error': 'No se han Agregado Nuevos Datos'})
                    return JsonResponse((data_json), safe = False)
                
        except DatabaseError as errorInterno:
            raise errorInterno #LOS ERRORES VAN A DAR A BaseException

        except BaseException as e:
            almacenarErroresExcepciones(
                descripcion_error = str(e), 
                aplicacion_id = 11,
                nombre_area = str( request.resolver_match.func.__name__ ), 
                usuario_registro = request.user.id
            )
            data_json.update({'error': 'Hubo una Excepción, no se ha Actualizado'})
            return JsonResponse((data_json), safe = False)
    else:
        return redirect(reverse('inicio'))
    
    

@login_required
def ajax_sala_videos_editar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json, form, data_form = {}, {}, request.POST.copy()
        data_form['estado'] = request.POST.get('estado', False)  
        
        try:
            if 'dato_pk' in data_form and data_form['dato_pk'].isnumeric() == True:
                sala_videos = Sala_Videos.objects.get( id = int(data_form['dato_pk']) )
                
                # IMPORTANTE!!!
                # NO colocar la instancia sala_videos en el form ejemplo: form( instance = sala_videos )
                # Si se coloca la instancia ocasiona problemas, NO podrá borrar la imagen con os.remove()
                # Al parecer en algunas ocasiones es mejor NO poner una instancia que se almecene en una variable dentro del form
                form = Sala_VideosForm( data = data_form, files = request.FILES, instance = Sala_Videos.objects.get(id = int(data_form['dato_pk'])) )
                
                if form.is_valid():
                    if request.FILES.get('imagen') != None:
                        if default_storage.exists( str(sala_videos.imagen) ) == True:
                            default_storage.delete( str(sala_videos.imagen) )
                    
                    form.save()
                    data_json.update({'exito': 'Se han Actualizado los Datos'})
                    return JsonResponse((data_json), safe = False)
                
                else:
                    data_json.update({'error': 'No se han Actualizado los Datos'})
                    return JsonResponse((data_json), safe = False)
            
            else:
                data_json.update({'error': 'Key no Válida'})
                return JsonResponse((data_json), safe = False)
                
        except BaseException as e:
            data_json.update({'error': 'Hubo una Excepción, no se ha Actualizado'})
            return JsonResponse((data_json), safe = False)
    else:
        return redirect(reverse('inicio'))
    
@login_required
@csrf_exempt
def ajax_sala_videos_eliminar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json, data_form = {}, request.POST.copy()
        try:
            if 'dato_pk' in data_form and data_form['dato_pk'].isnumeric() == True:
                sala_videos = Sala_Videos.objects.get(id=int(data_form['dato_pk']))
                
                if sala_videos.imagen and default_storage.exists(str(sala_videos.imagen)):
                    default_storage.delete(str(sala_videos.imagen))
                sala_videos.delete()
                data_json.update({'exito': 'Se ha eliminado correctamente'})
                return JsonResponse(data_json, safe=False)
            else:
                data_json.update({'error': 'Key no válida'})
        except Exception as e:
            data_json.update({'error': 'Hubo una Excepción, no se ha eliminado'})
            return JsonResponse(data_json, safe=False)
    else:
        return redirect(reverse('inicio'))
    
################################################################################################
################################################################################################
                            # CRUD: Responsabilidad Social
################################################################################################
################################################################################################

@login_required
@minified_response
def responsabilidad_social(request):
    # Verificar permiso
    if verificarPermiso(request, request.resolver_match.func.__name__):
        return render(request, 'sin_permiso.html', {'vista': request.resolver_match.func.__name__, 'url_anterior': request.META.get('HTTP_REFERER', None) or '/'})
    
    form = R_SocialForm()
    return render(request, 'responsabilidad_social.html', {'form':form})

@login_required
@csrf_exempt
def ajax_responsabilidad_social_listar(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
            lista = []

            if 'dxTileVideo' in request.GET and int(request.GET.get('dxTileVideo')) == 1:
                responsabilidad = Responsabilidad_Social.objects.filter(estado = True)
            
            elif 'dxTileVideo' in request.GET and int(request.GET.get('dxTileVideo')) == 2:
                responsabilidad = Responsabilidad_Social.objects.all()

            for r in responsabilidad:
                direccionImagenNube = str(r.imagen)
                if default_storage.exists(direccionImagenNube) == True:
                    blob = bucket.blob(direccionImagenNube)

                    imagenNube = blob.generate_signed_url(
                        version = "v4",
                        expiration = datetime.timedelta(hours = 1),
                        method = "GET"
                    )
                else:
                    imagenNube = ''

                lista.append({
                    'id': r.id, 
                    'nombre': r.nombre, 
                    'descripcion': r.descripcion, 
                    'estado': r.estado, 
                    'nombreImagen': str(r.imagen),
                    'imagen': imagenNube,
                    'fecha_realizacion': r.fecha_realizacion
                })

            return JsonResponse((lista), safe = False)
            
        except BaseException as e:
            return JsonResponse(({'error': 'No se han cargado los datos en la tabla'}), safe = False)

    else:
        return redirect(reverse('inicio'))
    

@login_required
@csrf_exempt
def ajax_responsabilidad_social_agregar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest' and not request.POST.get('dato_pk'):
        data_form, data_json = request.POST.copy(), {}
        data_form['estado'] = request.POST.get('estado', False)
                
        try:
            with transaction.atomic(using = 'finsurhn_ws_db'):
                form = R_SocialForm(data = data_form, files = request.FILES)
                
                if form.is_valid():
                    form.save()
                    data_json.update({'exito': 'Se han Agregado Nuevos Datos'})
                    return JsonResponse((data_json), safe = False)
                else:
                    data_json.update({'error': 'No se han Agregado Nuevos Datos'})
                    return JsonResponse((data_json), safe = False)
                
        except DatabaseError as errorInterno:
            raise errorInterno #LOS ERRORES VAN A DAR A BaseException

        except BaseException as e:
            almacenarErroresExcepciones(
                descripcion_error = str(e), 
                aplicacion_id = 11,
                nombre_area = str( request.resolver_match.func.__name__ ), 
                usuario_registro = request.user.id
            )
            data_json.update({'error': 'Hubo una Excepción, no se ha Actualizado'})
            return JsonResponse((data_json), safe = False)
    else:
        return redirect(reverse('inicio'))
    
    
@login_required
@csrf_exempt
def ajax_responsabilidad_social_editar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json, form, data_form = {}, {}, request.POST.copy()
        data_form['estado'] = request.POST.get('estado', False)  
        
        try:
            if 'dato_pk' in data_form and data_form['dato_pk'].isnumeric() == True:
                r_social = Responsabilidad_Social.objects.get( id = int(data_form['dato_pk']) )
                
                # IMPORTANTE!
                # NO colocar la instancia prod_serv en el form ejemplo: form( instance = prod_serv ) NO podrá borrar la imagen con os.remove()
                form = R_SocialForm( data = data_form, files = request.FILES, instance = Responsabilidad_Social.objects.get(id = int(data_form['dato_pk'])) )
                   
                if form.is_valid():
                    if request.FILES.get('imagen') != None:
                        if default_storage.exists( str(r_social.imagen) ) == True:
                            default_storage.delete( str(r_social.imagen) )
                    
                    form.save()
                    data_json.update({'exito': 'Se han Actualizado los Datos'})
                    return JsonResponse((data_json), safe = False)
                
                else:
                    data_json.update({'error': 'No se han Actualizado los Datos'})
                    return JsonResponse((data_json), safe = False)
            
            else:
                data_json.update({'error': 'Key no Válida'})
                return JsonResponse((data_json), safe = False)
                
        except BaseException as e:
            data_json.update({'error': 'Hubo una Excepción, no se ha Actualizado'})
            return JsonResponse((data_json), safe = False)
    else:
        return redirect(reverse('inicio'))

@login_required
@csrf_exempt
def ajax_responsabilidad_social_eliminar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json, data_form = {}, request.POST.copy()
        
        try:
            if 'dato_pk' in data_form and data_form['dato_pk'].isnumeric() == True:
                r_social = Responsabilidad_Social.objects.get(id=int(data_form['dato_pk']))
                
                #Eliminar la imagen si existe
                if r_social.imagen and default_storage.exists(str(r_social.imagen)):
                    default_storage.delete(str(r_social.imagen))                
                
                #Eliminar el registro
                r_social.delete()
                
                data_json.update({'exito': 'Se ha eliminado el registro correctamente'})
                return JsonResponse((data_json), safe = False)
            else:
                data_json.update({'error': 'Key no Válida'})
                return JsonResponse((data_json), safe = False)
                
        except BaseException as e:
            data_json.update({'error': 'Hubo una Excepción, no se ha Actualizado'})
            print(f"Error: {e}")
            return JsonResponse((data_json), safe = False)
    else:
        return redirect(reverse('inicio'))
    
################################################################################################
################################################################################################
                            # CRUD: Productos y Servicios Financieros
################################################################################################
################################################################################################
                                        
################################################################################################
                                    # VIEWS PÁGINA
################################################################################################
def ajax_productos_servicios_listar_activos(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
            lista = []

            for p in Productos_Servicios.objects.filter(estado = True):
                direccionImagenNube = str(p.imagen)
                if default_storage.exists(direccionImagenNube) == True:
                    blob = bucket.blob(direccionImagenNube)

                    imagenNube = blob.generate_signed_url(
                        version = "v4",
                        expiration = datetime.timedelta(hours = 1),
                        method = "GET"
                    )
                else:
                    imagenNube = ''

                lista.append({
                    'id': p.id, 
                    'nombre': p.nombre, 
                    'descripcion': p.descripcion, 
                    'es_producto': p.es_producto, 
                    'estado': p.estado, 
                    'imagen': imagenNube
                })
            return JsonResponse(lista, safe = False)

        except BaseException as e:
            return JsonResponse(({'error': 'No se han cargado los datos en la tabla'}), safe = False)
    else:
        return redirect(reverse('inicio'))

    



################################################################################################
                                    # VIEWS LOGGIN_REQUIRED
################################################################################################
@login_required
@minified_response
def productos_servicios(request):
    # Verificar permiso
    if verificarPermiso(request, request.resolver_match.func.__name__):
        return render(request, 'sin_permiso.html', {'vista': request.resolver_match.func.__name__, 'url_anterior': request.META.get('HTTP_REFERER', None) or '/'})
    
    form = Prod_ServForm()
    return render(request, 'productos_servicios.html', {'form':form})


def ajax_productos_servicios_listar(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            return JsonResponse(list(Productos_Servicios.objects.all().values('id', 'nombre', 'descripcion', 'estado', 'es_producto', 'imagen')), safe = False)
        
        except BaseException as e:
            return JsonResponse(({'error': 'No se han cargado los datos en la tabla'}), safe = False)
    else:
        return redirect(reverse('inicio'))
    

@login_required
def ajax_productos_servicios_agregar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_form, data_json = request.POST.copy(), {}
        
        if not 'dato_pk' in data_form:
            data_form['estado'] = True
            data_form['es_producto'] = request.POST.get('es_producto', False)
                    
            # Pasando los datos a un modelForm para válidar si es un formulario válido
            form = Prod_ServForm(data = data_form, files = request.FILES)
            
            try:
                with transaction.atomic(using = 'finsurhn_ws_db'):
                    if form.is_valid():
                        form.save()
                        
                        # Si el producto_servicio, es_producto entonces puede guardar detalles del producto
                        if bool(form.data['es_producto']) == True:                                                                                            
                            if 'dataNuevoDetalle' in request.POST: # Primero verificamos si existe el objeto
                                for ls in request.POST.getlist('dataNuevoDetalle'):
                                    if int(json.loads(ls)[0]['id']) == 0:
                                        Detalle_Productos_Servicios.objects.create(
                                            producto_servicio = form.instance,
                                            frecuencia_pago = int(json.loads(ls)[0]['frecuencia_pago']),
                                            requisitos = json.loads(ls)[0]['requisitos']
                                        )                                                
                        
                        data_json.update({'exito': 'Se han Actualizado los Datos'})
                        return JsonResponse((data_json), safe = False)
                    
                    else:
                        data_json.update({'error': 'No se han Agregado Nuevos Datos'})
                        return JsonResponse((data_json), safe = False)
                    
            except DatabaseError as errorInterno:
                raise errorInterno #LOS ERRORES VAN A DAR A BaseException

            except BaseException as e:
                almacenarErroresExcepciones(
                    descripcion_error = str(e), 
                    aplicacion_id = 11,
                    nombre_area = str( request.resolver_match.func.__name__ ), 
                    usuario_registro = request.user.id
                )
                data_json.update({'error': 'Hubo una Excepción, no se ha Actualizado'})
                return JsonResponse((data_json), safe = False)
        
        else:
            data_json.update({'error': 'Intenta agregar y mandar un ID e producto'})
            return JsonResponse((data_json), safe = False)
    else:
        return redirect(reverse('inicio'))
    
    

@login_required
@csrf_exempt
def ajax_productos_servicios_editar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json, form, data_form = {}, {}, request.POST.copy()
        data_form['es_producto'] = request.POST.get('es_producto', False)

        try:
            with transaction.atomic(using = 'finsurhn_ws_db'):
                if 'dato_pk' in data_form and data_form['dato_pk'].isnumeric() == True:
                    prod_serv = Productos_Servicios.objects.get(id = int(data_form['dato_pk']))
                    
                    # IMPORTANTE!
                    # NO colocar la instancia prod_serv en el form ejemplo: form( instance = prod_serv ) NO podrá borrar la imagen con os.remove()
                    instancia_producto = Productos_Servicios.objects.get(id = int(data_form['dato_pk']))
                    form = Prod_ServForm( data = data_form, files = request.FILES, instance = instancia_producto )
                    
                    # Elimando 'filas' del formulario
                    del form.fields['estado']
                        
                    if form.is_valid():
                        if request.FILES.get('imagen') != None:
                            if default_storage.exists( str(prod_serv.imagen) ) == True:
                                default_storage.delete( str(prod_serv.imagen) )
                        
                        form.save()
                        
                        # Si el usuario conviertió un producto a un servicio se eliminarán todos los detalles del producto.
                        if prod_serv.es_producto == True and form.data['es_producto'] == False:
                            Detalle_Productos_Servicios.objects.filter(producto_servicio = prod_serv).delete()
                        
                        if bool(form.data['es_producto']) == True:
                            # Primero se guardan los datos a editar por el unique_together que hay en modelo
                            # Al cambiar la frecuencia de un dato existente (Diaria), y agregaba un dato nuevo con la frecuencia (Diaria)...
                            # Daba error porque la frecuencia ya existía.
                            if 'dataEditarDetalle' in request.POST: # Primero verificamos si existe el objeto
                                for ls in request.POST.getlist('dataEditarDetalle'): # > json.loads(request.POST.getlist('dataEditarDetalle')[0]): Antes se hacía así pero dejo de funcionarme
                                    if int(json.loads(ls)[0]['id']) > 0: 
                                        detalle = Detalle_Productos_Servicios.objects.filter(id = int(json.loads(ls)[0]['id']) )
                                        detalle.update(
                                            frecuencia_pago = int(json.loads(ls)[0]['frecuencia_pago']),
                                            requisitos = json.loads(ls)[0]['requisitos']
                                        )
                                                                        
                            if 'dataNuevoDetalle' in request.POST: # Primero verificamos si existe el objeto
                                for ls in request.POST.getlist('dataNuevoDetalle'):
                                    if int(json.loads(ls)[0]['id']) == 0:
                                        Detalle_Productos_Servicios.objects.create(
                                            producto_servicio = form.instance,
                                            frecuencia_pago = int(json.loads(ls)[0]['frecuencia_pago']),
                                            requisitos = json.loads(ls)[0]['requisitos']
                                        )
                        
                        data_json.update({'exito': 'Se han Actualizado los Datos'})
                        return JsonResponse((data_json), safe = False)
                    
                    else:
                        data_json.update({'error': 'No se han Actualizado los Datos'})
                        return JsonResponse((data_json), safe = False)
                
                else:
                    data_json.update({'error': 'Key no Válida'})
                    return JsonResponse((data_json), safe = False)
                
        except DatabaseError as errorInterno:
            raise errorInterno #LOS ERRORES VAN A DAR A BaseException

        except BaseException as e:
            almacenarErroresExcepciones(
                descripcion_error = str(e), 
                aplicacion_id = 11,
                nombre_area = str( request.resolver_match.func.__name__ ), 
                usuario_registro = request.user.id
            )
            data_json.update({'error': 'Hubo una Excepción, no se ha Actualizado'})
            return JsonResponse((data_json), safe = False)
    else:
        return redirect(reverse('inicio'))
    
    
    
@login_required
@csrf_exempt
def ajax_producto_servicio_editar_datagrid(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json = {}
        try:
            if 'key' in request.POST and request.POST['key'].isnumeric() == True:
                
                # Si viene la lista de datos en el POST
                if request.POST.getlist('data')[0]:
                    
                    datos_list = json.loads(request.POST.getlist('data')[0])
                    
                    # Creando instancia de objeto a guardar
                    producto_servicio = Productos_Servicios.objects.get( id = int(request.POST['key']) )
                    
                    if 'estado' in datos_list:
                        producto_servicio.estado = int(datos_list['estado'])
                        
                    # GUARDANDO
                    try:
                        producto_servicio.save()
                        data_json.update({'exito': 'Se han Actualizado los Datos'})
                        return JsonResponse((data_json), safe = False)
                    except ValueError as e:
                        data_json.update({'error': 'No se han Actualizado los Datos'})
                        return JsonResponse((data_json), safe = False)
                        
                else:
                    data_json.update({'error': 'Datos no válidos'})
                    return JsonResponse((data_json), safe = False)

            else:
                data_json.update({'error': 'Key no Válida'})
                return JsonResponse((data_json), safe = False)
                
        except BaseException as e:
            data_json.update({'error': 'Hubo una Excepción, no se ha Actualizado'})
            return JsonResponse((data_json), safe = False)
    else:
        return redirect(reverse('inicio'))
    
    
################################################################################################
################################################################################################
                            # CRUD: DETALLE DE PRODUCTOS
################################################################################################
################################################################################################

def ajax_detalle_producto_obtener(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            if 'id_producto' in request.GET and request.GET.get('id_producto').isnumeric():

                return JsonResponse(ejecutarSPList('finsurhn_ws_db', 'OBTENER_LISTADO_DETALLE_PRODUCTO', [int(request.GET.get('id_producto'))]), safe = False)
            else:
                return JsonResponse(({'error': 'No se han Cargado los Datos, ID de Producto Inválido'}), safe = False)
        except BaseException as e:
            return JsonResponse(({'error': 'No se han cargado los datos en la tabla'}), safe = False)
    else:
        return redirect(reverse('inicio'))
    
    
@login_required
@csrf_exempt 
def ajax_detalle_producto_eliminar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json, datakeys = {}, json.loads(request.POST.getlist('key')[0])
        try:
            with transaction.atomic(using = 'finsurhn_ws_db'):
                if 'key' in request.POST and str(request.POST['key']).isnumeric() == True:
                    detalle = Detalle_Productos_Servicios.objects.get(id = int(request.POST['key']))
                    detalle.delete()
                else:
                    data_json.update({'error': 'Key no Válida'})
            
        except DatabaseError as errorInterno:
            raise errorInterno #LOS ERRORES VAN A DAR A BaseException

        except BaseException as e:
            almacenarErroresExcepciones(
                descripcion_error = str(e), 
                aplicacion_id = 11,
                nombre_area = str( request.resolver_match.func.__name__ ), 
                usuario_registro = request.user.id
            )
            data_json.update({'error': 'Hubo una excepción, no se han elimninado los datos'});
            return JsonResponse((data_json), safe = False)
        
        else:
            data_json.update({'exito': 'Se han eliminado los datos'});
            return JsonResponse((data_json), safe = False)
    
    else:
        return redirect(reverse('inicio'))


@login_required
def ajax_frecuencia_pagos_listar(request): # Se muestra en productos/servicios 
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            return JsonResponse(list(FrecuenciaPagos.objects.all().values('id', 'descripcion_frecuencia')), safe = False)
        
        except BaseException as e:
            return JsonResponse(({'error': 'No se han cargado los datos del Cargo'}), safe = False)
    else:
        return redirect(reverse('inicio'))

@login_required
def ajax_cargo_listar(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            return JsonResponse(list(Cargo.objects.all().order_by('cargo').values('id', 'cargo')), safe = False)
        
        except BaseException as e:
            return JsonResponse(({'error': 'No se han cargado los datos del Cargo'}), safe = False)
    else:
        return redirect(reverse('inicio'))

################################################################################################
################################################################################################
                            # LISTAR Y EDITAR: MISIÓN, VISIÓN Y HISTORIA
################################################################################################
################################################################################################

@login_required    
@minified_response
def mision_vision_historia(request):
    if verificarPermiso(request, request.resolver_match.func.__name__):
        return render(request, 'sin_permiso.html', {'vista': request.resolver_match.func.__name__, 'url_anterior': request.META.get('HTTP_REFERER', None) or '/'})
    return render(request, 'mvh_empresa.html')
    
    
@login_required
def ajax_mvh_listar(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            empresa = Empresa.objects.all().first() #Todo se obtiene desde la unica fila de la tabla Empresa
            if not empresa:
                return JsonResponse(({'error': 'No hay datos de la empresa'}))

            data = ( 
                {"id": 1, "tipo_informacion": "MISIÓN", "descripcion": empresa.mision},
                {"id": 2, "tipo_informacion": "VISIÓN", "descripcion": empresa.vision},
                {"id": 3, "tipo_informacion": "HISTORIA", "descripcion": empresa.historia},
            )
        
            return JsonResponse(data, safe = False)
        
        except BaseException as e:
            return JsonResponse(({'error': 'Ocurrió un error al cargar los datos'}), safe = False)
    else:
        return redirect(reverse('inicio'))
    
@login_required
@csrf_exempt 
def ajax_mvh_editar(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json = {}
    
        try:
            if 'key' in request.POST and request.POST['key'].isnumeric() == True:
                key = int(request.POST['key'])
                if request.POST.getlist('data')[0]:
                    with transaction.atomic(using = 'finsurhn_sp_db'):
                        dato_list = json.loads(request.POST.getlist('data')[0])
                        
                        empresa = Empresa.objects.using('finsurhn_sp_db').all().first()
                        
                        if not empresa:
                            data_json.update({'error': 'No se encontró la empresa'})
                            return JsonResponse((data_json), safe = False)
                        if key == 1 and 'descripcion' in dato_list:
                            empresa.mision = dato_list['descripcion']
                        elif key == 2 and 'descripcion' in dato_list:
                            empresa.vision = dato_list['descripcion']      
                        elif key == 3 and 'descripcion' in dato_list:   
                            empresa.historia = dato_list['descripcion'] 
                        else:
                            data_json.update({'error': 'Key no Válida o datos incompletos'})
                            return JsonResponse((data_json), safe = False)  
                        
                        empresa.save(using = 'finsurhn_sp_db')
                        data_json.update({'exito': 'Se han Actualizado los Datos'})
                        return JsonResponse((data_json), safe = False)
                    
                else:
                    data_json.update({'error': 'Datos no válidos'})
                    return JsonResponse((data_json), safe = False)
            else:
                data_json.update({'error': 'Key no Válida'})
                return JsonResponse((data_json), safe = False)  
            
        except BaseException as e:
            almacenarErroresExcepciones(
                descripcion_error = str(e), 
                aplicacion_id = 11,
                nombre_area = str( request.resolver_match.func.__name__ ), 
                usuario_registro = request.user.id
            )
            print(f"error lanzado en except : {e} ")
            data_json.update({'error': 'Hubo una Excepción, no se ha Actualizado'})
            return JsonResponse((data_json), safe = False)
    else:
        return redirect(reverse('inicio'))
    
@login_required    
@minified_response
def solicitudes_credito(request):
    if verificarPermiso(request, request.resolver_match.func.__name__):
        return render(request, 'sin_permiso.html', {'vista': request.resolver_match.func.__name__, 'url_anterior': request.META.get('HTTP_REFERER', None) or '/'})
    return render(request, 'solicitudes_credito.html')

def ajax_solicitudes_credito_listar(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            solicitudes = []
            for solicitud in Solicitud.objects.select_related('formaPago', 'sucursal').all():
                solicitudes.append({
                    'id': solicitud.id,
                    'identificacion': solicitud.identificacion,
                    'primerNombre': solicitud.primerNombre,
                    'segundoNombre': solicitud.segundoNombre,
                    'primerApellido': solicitud.primerApellido,
                    'segundoApellido': solicitud.segundoApellido,
                    'celular': solicitud.celular,
                    'direccion': solicitud.direccion,
                    'montoSolicitado': solicitud.montoSolicitado,
                    'estado_id': solicitud.estado_id,
                    'correo': solicitud.correo,
                    'fechaEnvio': solicitud.fecha_envio,
                    'descripcionTipoIngreso': solicitud.descripcionTipoIngreso,
                    'formaPago': solicitud.formaPago.nombre if solicitud.formaPago else None,
                    'sucursal': solicitud.sucursal.nombre if solicitud.sucursal else None,
                })
            return JsonResponse(solicitudes, safe=False)
        except BaseException as e:
            print(f"Error: {str(e)}")
            return JsonResponse(({'error': 'Ocurrió un error al cargar los datos'}), safe=False)
    else:
        return redirect(reverse('inicio'))

@csrf_exempt
def ajax_solicitud_credito_actualizar_estado(request):
    try:
        key = request.POST.get('key')
        data = json.loads(request.POST.get('data', '{}'))
        
        if not key or not data:
            return JsonResponse({'error': 'Datos incompletos'}, safe=False)
        
        solicitud = Solicitud.objects.get(id=key)
        estado_anterior = solicitud.estado_id
        
        if 'estado_id' in data:
            nuevo_estado = int(data['estado_id'])
            if not es_transicion_valida(estado_anterior, nuevo_estado):
                return JsonResponse({'error': 'Transición de estado no permitida'}, safe=False)
            
            solicitud.estado_id = nuevo_estado
            solicitud.save()

            acciones_solicitud(solicitud, nuevo_estado, estado_anterior)

            return JsonResponse({'exito': 'Estado actualizado correctamente'})
        else:
            return JsonResponse({'error': 'No se especificó el estado a actualizar'}, safe=False)
            
    except Solicitud.DoesNotExist:
        return JsonResponse({'error': 'Solicitud no encontrada'}, safe=False)
    except ValueError:
        return JsonResponse({'error': 'Valor de estado inválido'}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False)
    
@login_required    
@minified_response
def consultas(request):
    if verificarPermiso(request, request.resolver_match.func.__name__):
        return render(request, 'sin_permiso.html', {'vista': request.resolver_match.func.__name__, 'url_anterior': request.META.get('HTTP_REFERER', None) or '/'})
    return render(request, 'consultas.html', {'form': RespuestaConsultaForm()})

def ajax_consultas_listar(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            consultas = Consulta.objects.all().values()
            return JsonResponse(list(consultas), safe=False)
        except:
            return JsonResponse(({'error': 'Ocurrió un error al cargar los datos'}), safe=False)
    else:
        return redirect(reverse('inicio'))

@csrf_exempt 
def ajax_consultas_eliminar(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json = {}
        try:
            if 'key' in request.POST and request.POST['key'].isnumeric() == True:
                consulta = Consulta.objects.get(id=int(request.POST['key']))
                consulta.delete()
                data_json.update({'exito': 'Se ha eliminado la consulta correctamente'})
                return JsonResponse((data_json), safe = False)
            else:
                data_json.update({'error': 'Key no Válida'})
                return JsonResponse((data_json), safe = False)
        except BaseException as e:
            data_json.update({'error': 'Hubo una Excepción, no se ha Actualizado'})
            return JsonResponse((data_json), safe = False)
    else:
        return redirect(reverse('inicio'))

@login_required
@csrf_exempt
def ajax_consultas_responder(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json = {}
        data_form = request.POST.copy()
        print(f"Datos recibidos: {data_form}")

        try:
            if 'key' in data_form and data_form['key'].isnumeric() == True:
                consulta_id = int(data_form['key'])
                print(consulta_id)
                consulta = Consulta.objects.get(id=consulta_id)
                
                respuesta = data_form.get('respuesta', '').strip()
                if not respuesta:
                    raise ValueError("La respuesta no puede estar vacía")

                # Envío de correo
                send_mail(
                    subject="Respuesta a su consulta",
                    message=respuesta,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[data_form.get('email')],
                    fail_silently=False
                )

                consulta.respondido = True
                consulta.fecha_respuesta = timezone.now()
                consulta.save()

                data_json['exito'] = 'Respuesta enviada correctamente'
                return JsonResponse(data_json)

            else:
                data_json['error'] = 'ID de consulta inválido'
                return JsonResponse(data_json, status=400)

        except Consulta.DoesNotExist:
            data_json['error'] = 'La consulta no existe'
            return JsonResponse(data_json, status=404)
            
        except Exception as e:
            data_json['error'] = str(e)
            return JsonResponse(data_json, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)