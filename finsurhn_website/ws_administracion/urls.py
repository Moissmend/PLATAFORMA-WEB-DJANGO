from django.urls import path
from ws_administracion.views import *

app_name = 'ws_administracion'

urlpatterns = [
    path('ajax/iniciar/sesion/', ajax_inicio_session, name = 'ajax_inicio_session'),
    path('cerrar/sesion/', cerrar_sesion, name = 'cerrar_sesion'),
    path('editar/contrasena/actual/ajax/', ajax_editar_contrasena_actual, name = 'ajax_editar_contrasena_actual'),
    path('inicio/administracion/', inicio_administracion, name = 'inicio_administracion'),

    path('obtener/imagen/google/cloud/ajax/', ajax_obtener_imagen_google_cloud, name = 'ajax_obtener_imagen_google_cloud'),
        

    # Valores de la empresa -- Sesión Iniciada
    path('valores/empresa/', valores_empresa, name = 'valores_empresa'),
    path('ajax/valores/empresa/listar/', ajax_valores_empresa_listar, name = 'ajax_valores_empresa_listar'),
    path('ajax/valores/empresa/agregar/', ajax_valores_empresa_agregar, name = 'ajax_valores_empresa_agregar'), 
    path('ajax/valores/empresa/editar/', ajax_valores_empresa_editar, name = 'ajax_valores_empresa_editar'), 
    path('ajax/valores/empresa/eliminar/', ajax_valores_empresa_eliminar, name = 'ajax_valores_empresa_eliminar'),
    
    # Gestion galeria empresa -- Sesion NO Iniciada -- Carousel
    path('gestion/galeria/empresa/', gestion_galeria_empresa, name = 'gestion_galeria_empresa'),
    path('gestion/galeria/empresa/listar/', ajax_gestion_galeria_empresa_listar, name = 'ajax_gestion_galeria_empresa_listar'),
    path('gestion/galeria/empresa/agregar/', ajax_gestion_galeria_empresa_agregar, name = 'ajax_gestion_galeria_empresa_agregar'),
    path('gestion/galeria/empresa/editar/', ajax_gestion_galeria_empresa_editar, name = 'ajax_gestion_galeria_empresa_editar'),
    path('gestion/galeria/empresa/editar/datagrid/', ajax_gestion_galeria_empresa_editar_datagrid, name = 'ajax_gestion_galeria_empresa_editar_datagrid'),
    
    # Redes Sociales -- Pagina de inicio -- Sesion NO Iniciada
    path('redes/sociales/empresa/', redes_sociales_empresa, name = 'redes_sociales_empresa'),
    path('ajax/redes_sociales/empresa/listar/', ajax_redes_sociales_empresa_listar, name = 'ajax_redes_sociales_empresa_listar'),
    path('ajax/redes_sociales/empresa/agregar/', ajax_redes_sociales_empresa_agregar, name = 'ajax_redes_sociales_empresa_agregar'),
    path('ajax/redes_sociales/empresa/editar/', ajax_redes_sociales_empresa_editar, name = 'ajax_redes_sociales_empresa_editar'),
    path('ajax/redes_sociales/empresa/editar/datagrid/', ajax_redes_sociales_empresa_editar_datagrid, name = 'ajax_redes_sociales_empresa_editar_datagrid'),
    path('ajax/redes_sociales/empresa/eliminar/', ajax_redes_sociales_empresa_eliminar, name = 'ajax_redes_sociales_empresa_eliminar'),
    
    # Contactanos -- Pagina de inicio -- Sesion NO Iniciada
    path('ajax/contactanos/', ajax_contactanos, name = 'ajax_contactanos'),
    
    # CRUD Información de Empleo
    path('informacion/empleo/', informacion_empleo, name = 'informacion_empleo'),
    path('ajax/informacion/empleo/listar/', ajax_informacion_empleo_listar, name = 'ajax_informacion_empleo_listar'),
    path('ajax/informacion/empleo/agregar/', ajax_informacion_empleo_agregar, name = 'ajax_informacion_empleo_agregar'),
    path('ajax/informacion/empleo/editar/', ajax_informacion_empleo_editar, name = 'ajax_informacion_empleo_editar'),
    path('ajax/informacion/empleo/editar/datagrid/', ajax_informacion_empleo_editar_datagrid, name = 'ajax_informacion_empleo_editar_datagrid'),
    path('informacion/empleo/vacantes/', informacion_empleo_vacantes, name = 'informacion_empleo_vacantes'),
    path('informacion/empleo/vacante/<int:dato_pk>/info/', informacion_empleo_vacante_info, name = 'informacion_empleo_vacante_info'),
    path('informacion/empleo/vacante/correo/<int:dato_pk>/', ajax_informacion_empleo_vacante_correo, name = 'ajax_informacion_empleo_vacante_correo'),
        
    # CRUD Sala de Videos
    path('sala/videos/', sala_videos, name = 'sala_videos'),
    path('ajax/sala/videos/listar/', ajax_sala_videos_listar, name = 'ajax_sala_videos_listar'),
    path('ajax/sala/videos/agregar/', ajax_sala_videos_agregar, name = 'ajax_sala_videos_agregar'),
    path('ajax/sala/videos/editar/', ajax_sala_videos_editar, name = 'ajax_sala_videos_editar'),
    
    # CRUD Responsabilidad Social
    path('responsabilidad/social/', responsabilidad_social, name = 'responsabilidad_social'),
    path('ajax/responsabilidad/social/listar/', ajax_responsabilidad_social_listar, name = 'ajax_responsabilidad_social_listar'),
    path('ajax/responsabilidad/social/agregar/', ajax_responsabilidad_social_agregar, name = 'ajax_responsabilidad_social_agregar'),
    path('ajax/responsabilidad/social/editar/', ajax_responsabilidad_social_editar, name = 'ajax_responsabilidad_social_editar'),
    
    # CRUD Productos y Servicios
    path('productos/servicios/', productos_servicios, name = 'productos_servicios'),
    path('ajax/productos/servicios/listar/', ajax_productos_servicios_listar, name = 'ajax_productos_servicios_listar'),
    path('ajax/productos/servicios/listar/activos/', ajax_productos_servicios_listar_activos, name = 'ajax_productos_servicios_listar_activos'),
    path('ajax/productos/servicios/agregar/', ajax_productos_servicios_agregar, name = 'ajax_productos_servicios_agregar'),
    path('ajax/productos/servicios/editar/', ajax_productos_servicios_editar, name = 'ajax_productos_servicios_editar'),
    path('ajax/productos/servicios/editar/datagrid/', ajax_producto_servicio_editar_datagrid, name = 'ajax_producto_servicio_editar_datagrid'),
    
    # CRUD Detalle de producto
    path('ajax/detalle/producto/obtener/', ajax_detalle_producto_obtener, name = 'ajax_detalle_producto_obtener'),
    path('ajax/detalle/producto/eliminar/', ajax_detalle_producto_eliminar, name = 'ajax_detalle_producto_eliminar'),

    path('ajax/frecuencia/pagos/listar', ajax_frecuencia_pagos_listar, name = "ajax_frecuencia_pagos_listar"),
    path('ajax/cargo/listar', ajax_cargo_listar, name = "ajax_cargo_listar"),
]