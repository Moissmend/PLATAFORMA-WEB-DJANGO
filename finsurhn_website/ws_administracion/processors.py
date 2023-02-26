from ws_administracion.models import *
from configuraciones.models import *

def ctx_empresa(request):
    ctx_empresa, empresa = {}, Empresa.objects.all().first()
    sucursal = Sucursal.objects.filter(empresa = empresa).first()
    
    ctx_empresa.update({
        'abreviatura': empresa.abreviatura,
        'empresa': empresa.empresa,
        'tipo_empresa': empresa.tipo_empresa,
        'historia': empresa.historia,
        'objetivo_general': empresa.objetivo_general,
        'vision': empresa.vision,
        'mision': empresa.mision,
        'telefono': empresa.telefono,
        'celular': empresa.celular,
        'direccion': empresa.direccion,
        'logo': sucursal.logo_p if sucursal.logo_p else None
    })
    
    return {'ctx_empresa':ctx_empresa}

def ctx_redes_sociales(request):
    redes_sociales = Redes_Sociales.objects.filter(estado = True).order_by('nombre')
    
    i = 0
    correlativo_redes = []
    for j in redes_sociales:
        correlativo_redes.append(i)
        i += 1
    return {'ctx_redes_sociales': redes_sociales, 'ctx_redes_sociales_orden': correlativo_redes}