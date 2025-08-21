from django.core.mail import send_mail, EmailMessage
from django.conf import settings

def es_transicion_valida(estado_anterior, nuevo_estado):
    """Valida si la transición entre estados es permitida"""
    transiciones_permitidas = {
        1: [2],  
        2: [1, 3], 
        3: []  
    }
    return nuevo_estado in transiciones_permitidas.get(estado_anterior, [])

def acciones_solicitud(solicitud, nuevo_estado, estado_anterior):
    """Acciones a realizar en la solicitud"""
    if nuevo_estado == 2: # EN REVISIÓN
        enviar_notificacion_revision(solicitud)
        
    elif nuevo_estado == 3: # FINALIZADA
        enviar_notificacion_finalizada(solicitud)
        
    elif nuevo_estado == 1 and estado_anterior == 2: # DEVUELTO A PENDIENTE
        enviar_notificacion_pendiente(solicitud)

def enviar_notificacion_revision(solicitud):
    """Notifica que la solicitud está en revisión"""
    mensaje =f'''
    <!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #f8f9fa; padding: 15px; text-align: center; }}
        .content {{ padding: 20px; background-color: #fff; }}
        .footer {{ margin-top: 20px; font-size: 12px; color: #777; }}
        .btn {{
            display: inline-block; padding: 10px 20px; 
            background-color: #007bff; color: white !important; 
            text-decoration: none; border-radius: 5px; 
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>¡Estamos revisando tu solicitud!</h2>
        </div>
        <div class="content">
            <p>Hola <strong>{ solicitud.primerNombre + " " + solicitud.primerApellido }</strong>,</p>
            <p>Tu pre-solicitud de crédito con número de identificación <strong>#{ solicitud.id }</strong> está siendo procesada.</p>
            <p>Te notificaremos cuando hayamos completado la revisión.</p>Inversiones Financieras del Sur © 2025
        </div>
        <div class="footer">
            <p>Fecha de solicitud: { solicitud.fecha_envio }</p>
            <p>Inversiones Financieras del Sur © 2025</p>
        </div>
    </div>
</body>
</html>
    '''
    try:
        email = EmailMessage(
            subject="Tu pre-solicitud está en revisión",
            body=mensaje,
            from_email=settings.EMAIL_HOST_USER,
            to=[solicitud.correo]
        )
        email.content_subtype = "html"  
        email.send()
        
    except Exception as e:
        print(f"Error enviando email: {str(e)}")

def enviar_notificacion_finalizada(solicitud):
    """Notifica que la pre-solicitud ha sido procesada"""
    mensaje =f'''
    <!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #f8f9fa; padding: 15px; text-align: center; }}
        .content {{ padding: 20px; background-color: #fff; }}
        .footer {{ margin-top: 20px; font-size: 12px; color: #777; }}
        .btn {{
            display: inline-block; padding: 10px 20px; 
            background-color: #007bff; color: white !important; 
            text-decoration: none; border-radius: 5px; 
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>¡Revisión Completa!</h2>
        </div>
            <div class="content">
                <p>Hola <strong>{ solicitud.primerNombre + " " + solicitud.primerApellido }</strong>,</p>
                <p>Tu pre-solicitud con número de identificación <strong>#{ solicitud.id }</strong> ha sido procesada.</p>
                <p>Un asesor se comunicará contigo pronto para continuar con el proceso.</p>
            </div>
        <div class="footer">
            <p>Fecha de solicitud: { solicitud.fecha_envio }</p>
            <p>Inversiones Financieras del Sur © 2025</p>
        </div>
    </div>
</body>
</html>
    '''
    try:
        email = EmailMessage(
            subject="Resolución de tu pre-solicitud",
            body=mensaje,
            from_email=settings.EMAIL_HOST_USER,
            to=[solicitud.correo]
        )
        email.content_subtype = "html"  
        email.send()
    except Exception as e:
        print(f"Error enviando email: {str(e)}")
    
def enviar_notificacion_pendiente(solicitud):
    """Solicita información adicional"""
    try:
        send_mail(
            subject="Información requerida para tu pre-solicitud",
            message="Necesitamos información adicional para procesar tu pre-solicitud.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[solicitud.correo],
            fail_silently=False
        )
    except Exception as e:
        print(f"Error enviando email: {str(e)}")