from django.forms import ModelForm
from django import forms
from ws_administracion.models import *

class Galeria_EmpresaForm(ModelForm):
    class Meta:
        model = Galeria_Empresa
        fields = '__all__'
        widgets = {}
        
    def __init__(self, *args, **kwargs):
        super(Galeria_EmpresaForm, self).__init__(*args, **kwargs)
        for campo in self.fields:
            if 'imagen' in campo:
                self.fields[campo].widget.attrs['class'] = 'form-control-file'
                self.fields['imagen'].widget.attrs['accept'] = '.jpg, .jpeg, .png'
            elif 'estado' in campo:
                self.fields[campo].widget.attrs['class'] = 'form-control js-switch'
                self.fields[campo].widget.attrs['checked'] = "checked"    
            else:
                self.fields[campo].widget.attrs['class'] = 'form-control'

class Informacion_EmpleoForm(ModelForm):
    class Meta:
        model = Informacion_Empleo
        fields = '__all__'
        widgets = {
            'descripcion': forms.Textarea(attrs = {
				'rows': 3
			}),
        }
        
    def __init__(self, *args, **kwargs):
        super(Informacion_EmpleoForm, self).__init__(*args, **kwargs)
        for campo in self.fields:
            if 'imagen' in campo:
                self.fields[campo].widget.attrs['class'] = 'form-control-file'
                self.fields['imagen'].widget.attrs['accept'] = '.jpg, .jpeg, .png'
            elif 'num_vacantes' in campo:
                self.fields[campo].widget.attrs.update({
                    'onkeypress ':'return numberKeyPress(event)', 'class':'form-control', 'min':'0', 'max':'20'
                })
            elif 'estado' in campo:
                self.fields[campo].widget.attrs['class'] = 'form-control js-switch'
                self.fields[campo].widget.attrs['checked'] = "checked"   
            else:
                self.fields[campo].widget.attrs['class'] = 'form-control'
                
                
class Valores_EmpresaFrom(ModelForm):
    class Meta:
        model = Valores_Empresa
        fields = '__all__'
        
        
class Redes_SocialesForm(ModelForm):
    class Meta:
        model = Redes_Sociales
        fields = '__all__'
        widgets = {
            'estado': forms.TextInput(attrs = {
                'type': 'checkbox',
			}),
            
        }
        
    def __init__(self, *args, **kwargs):
        super(Redes_SocialesForm, self).__init__(*args, **kwargs)
        for campo in self.fields:
            if 'imagen' in campo:
                self.fields[campo].widget.attrs['class'] = 'form-control-file'
                self.fields['imagen'].widget.attrs['accept'] = '.jpg, .jpeg, .png'
            elif 'estado' in campo:
                self.fields[campo].widget.attrs['class'] = 'form-control js-switch'
                self.fields[campo].widget.attrs['checked'] = "checked"    
            else:
                self.fields[campo].widget.attrs['class'] = 'form-control'
                

class Sala_VideosForm(ModelForm):
    class Meta:
        model = Sala_Videos
        fields = '__all__'
        widgets = {
            'estado': forms.TextInput(attrs = {
                'type': 'checkbox',
			}),
            
        }
        
    def __init__(self, *args, **kwargs):
        super(Sala_VideosForm, self).__init__(*args, **kwargs)
        for campo in self.fields:
            if 'imagen' in campo:
                self.fields[campo].widget.attrs['class'] = 'form-control-file'
                self.fields['imagen'].widget.attrs['accept'] = '.jpg, .jpeg, .png'
            elif 'estado' in campo:
                self.fields[campo].widget.attrs['class'] = 'form-control js-switch'
                self.fields[campo].widget.attrs['checked'] = "checked"    
            else:
                self.fields[campo].widget.attrs['class'] = 'form-control'



# Responsabilidad_SocialForm
class R_SocialForm(ModelForm):
    class Meta:
        model = Responsabilidad_Social
        fields = '__all__'
        widgets = {
            'estado': forms.TextInput(attrs = {
                'type': 'checkbox',
			}),
            'fecha_realizacion': forms.TextInput(attrs = {
                'type': 'date',
			}),
            'descripcion': forms.Textarea(attrs = {
				'rows': 2
			}),
            
        }
        
    def __init__(self, *args, **kwargs):
        super(R_SocialForm, self).__init__(*args, **kwargs)
        
        for campo in self.fields:
            if 'imagen' in campo:
                self.fields[campo].widget.attrs['class'] = 'form-control-file'
                self.fields['imagen'].widget.attrs['accept'] = '.jpg, .jpeg, .png'
            elif 'estado' in campo:
                self.fields[campo].widget.attrs['class'] = 'form-control js-switch'
                self.fields[campo].widget.attrs['checked'] = "checked"   
            else:
                self.fields[campo].widget.attrs['class'] = 'form-control'
                
# Productos y Servicios Form
class Prod_ServForm(ModelForm):
    class Meta:
        model = Productos_Servicios
        fields = '__all__'
        widgets = {
            'estado': forms.TextInput(attrs = {
                'type': 'checkbox',
			}),
            'es_producto': forms.TextInput(attrs = {
                'type': 'checkbox',
			}),
            'descripcion': forms.Textarea(attrs = {
				'rows': 3
			}),
        }
        exclude = ('frecuencia_pagos',)
        
    def __init__(self, *args, **kwargs):
        super(Prod_ServForm, self).__init__(*args, **kwargs)
        
        for campo in self.fields:
            if 'imagen' in campo:
                self.fields[campo].widget.attrs['class'] = 'form-control-file'
                self.fields['imagen'].widget.attrs['accept'] = '.jpg, .jpeg, .png'
            elif 'estado' in campo:
                self.fields[campo].widget.attrs['class'] = 'form-control js-switch'
                self.fields[campo].widget.attrs['checked'] = "checked"   
            elif 'es_producto' in campo:
                self.fields[campo].widget.attrs['class'] = 'form-control js-switch'
                self.fields[campo].widget.attrs['checked'] = "checked"   
            else:
                self.fields[campo].widget.attrs['class'] = 'form-control'
                
                
# Productos y Servicios Form
class Detalle_Productos_ServiciosForm(ModelForm):
    class Meta:
        model = Detalle_Productos_Servicios
        fields = '__all__'
    
                
class ContactanosForm(forms.Form):
    nombre_completo = forms.CharField(
        label= 'Nombre Completo', min_length = 1, max_length = 50, required = True,
        widget= forms.TextInput(attrs = {'class': 'form-control text-left'}))
    
    num_identidad = forms.CharField(
        label = 'Número de Identidad', max_length = 15, required = True,
        widget = forms.TextInput(attrs = {'class': 'form-control text-left', 'placeholder': '9999-9999-99999'}))
        
    correo = forms.EmailField(
        label = 'Correo Electónico', required = True,
        widget = forms.TextInput(attrs = {'class': 'form-control text-left'}))
    
    telefono = forms.CharField(
        label = 'Teléfono', max_length = 9, required = False,
        widget = forms.TextInput(attrs = {'class': 'form-control text-left', 'placeholder': '9999-9999'}))
    
    celular = forms.CharField(
        label = 'Celular', max_length = 9, required = False,
        widget = forms.TextInput(attrs = {'class': 'form-control text-left', 'placeholder': '9999-9999'}))
    
    ciudad = forms.CharField(
        label = 'Ciudad', required = True,
        widget = forms.TextInput(attrs = {'class': 'form-control text-left'}))
    
    asunto = forms.CharField(
        label = 'Asunto', required = True, 
        widget = forms.Textarea(attrs = {'class': 'form-control text-left', 'rows': '3'}))
    
    
    
class empleo_contactoForm(forms.Form):
    nombre_completo = forms.CharField(
        label= 'Nombre Completo', min_length = 1, max_length = 50, required = True,
        widget= forms.TextInput(attrs = {'class': 'form-control'}))
    
    num_identidad = forms.CharField(
        label = 'Número de Identidad', max_length = 15, required = True,
        widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': '9999-9999-99999'}))
        
    correo = forms.EmailField(
        label = 'Correo Electónico', required = True,
        widget = forms.TextInput(attrs = {'class': 'form-control'}))
    
    telefono = forms.CharField(
        label = 'Teléfono', max_length = 9, required = False,
        widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': '9999-9999 '}))
    
    celular = forms.CharField(
        label = 'Celular', max_length = 9, required = False,
        widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': '9999-9999 '}))
    
    ciudad = forms.CharField(
        label = 'Ciudad', required = True,
        widget = forms.TextInput(attrs = {'class': 'form-control'}))
    
    asunto = forms.CharField(
        label = 'Asunto', required = True, 
        widget = forms.Textarea(attrs = {'class': 'form-control', 'rows': '3'}))
    
    curriculum = forms.FileField(
        # widget=forms.ClearableFileInput(attrs = {'multiple': True})
        widget=forms.ClearableFileInput(attrs = {'class': 'custom-file-input', 'lang':'es'}) )

    