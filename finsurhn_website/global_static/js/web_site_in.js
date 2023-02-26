DevExpress.localization.locale("es-HN");

function mensajeError(mensaje, titulo) {
    toastr.error(mensaje, titulo, {
        "progressBar": true,
        "closeButton": true,
        "newestOnTop": true, // Que los nuevos mensajes, siempre salgan arriba de los demás
        "positionClass": "toast-top-right",
        "preventDuplicates": true,
        "showDuration": "300"
    });
}

function mensajeSuccess(mensaje, titulo) {
    toastr.success(mensaje, titulo, {
        "progressBar": true,
        "closeButton": true,
        "newestOnTop": true, // Que los nuevos mensajes, siempre salgan arriba de los demás
        "positionClass": "toast-top-right",
        "preventDuplicates": true,
        "showDuration": "300"
    });
}

function mensajeInfo(mensaje, titulo) {
    toastr.info(mensaje, titulo, {
        "progressBar": true,
        "closeButton": true,
        "newestOnTop": true, // Que los nuevos mensajes, siempre salgan arriba de los demás
        "positionClass": "toast-top-right",
        "preventDuplicates": true,
        "showDuration": "300"
    });
}

function mensajeWarning(mensaje, titulo) {
    toastr.warning(mensaje, titulo, {
        "progressBar": true,
        "closeButton": true,
        "newestOnTop": true, // Que los nuevos mensajes, siempre salgan arriba de los demás
        "positionClass": "toast-top-right",
        "preventDuplicates": true,
        "showDuration": "300"
    });
}

function obtenerImagenNube(direccionImagen, opc) {
	let objetoImagen = "";
	let suministroImagen = "";
	switch(parseInt(opc)) {
		case 1:
			objetoImagen = ".imagenNubeGC";
	        suministroImagen = "src";
			break;
		case 2:
			objetoImagen = ".aNubeGC";
	        suministroImagen = "href";
			break;
		default:
			objetoImagen = ".imagenNubeGC";
	        suministroImagen = "src";
	}

	if (direccionImagen == null || direccionImagen == '' || direccionImagen == '/static/icon/no_image.png/'){
		$(objetoImagen).attr(suministroImagen, '/static/media_finsur/no_image.png/');
	} else {
		$.get("/obtener/imagen/google/cloud/ajax/", { direccionImagen }, function (data) {
            	
			if (data.resultado == "true") {
				$(objetoImagen).attr(suministroImagen, data.imagenNube);
			} else if (data.resultado == "imagenNoEncontrada") {
				$(objetoImagen).attr(suministroImagen, '/static/media_finsur/no_image.png/');
			} else {
				mensajeError("¡Error!, al obtener la Imagen Contacte al Encargado de IT.");

				$(objetoImagen).attr(suministroImagen, '/static/media_finsur/no_image.png/');
			}
	
		}, 'json')
	}
}

$(document).on("click", ".a_obligatorio", function(){
    mensajeWarning("El Llenado o Selección de este Campo es de carácter Obligatorio.", '¡Información');
});

document.oncontextmenu = function () {
    return false;
}

$(function(){   
    if ($(".js-switch")[0]) {
        var elems = Array.prototype.slice.call(document.querySelectorAll('.js-switch'));

        elems.forEach(function(html) {
            var switchery = new Switchery(html, { color:'#1F618D' });
        });
    }
      
    $('#PopupLoginForm').dxPopup({
        contentTemplate: "contenidoPopupLoginForm",
        height: "auto",
        width: 380,
        showTitle: true,
        titleTemplate: "tituloPopupLoginForm",
        visible: false,
        dragEnabled: true,
        closeOnOutsideClick: true,
        shading: true,
        //resizeEnabled : true
    })

    $('#BtnLoginForm').on('click', function(){
        var popup = $("#PopupLoginForm").dxPopup("instance");
        popup.show();
        var content = popup.content();
    
        content.css({
            "padding": 4
        })
    
        popup.option("position", {
            my: "center",
            at: "center"
        })
    
        $('#TxtUsuario').dxTextBox({
			value: "",
			showClearButton: true,
			placeholder: "¡Ingrese el Usuario!",
			maxLength: 150,
			buttons: ['clear', {
				name: 'username',
				location: 'before',
				options: {
					icon: 'fa fa-user',
					stylingMode: 'text'
				},
			}]
		}).dxValidator({
			validationGroup: "validationGroup_FormularioIngresar",
			validationRules: [{
				type: 'required',
				message: '¡Ingrese el Usuario!'
			}]
		});

		$('#TxtContrasena').dxTextBox({
			value: "",
			mode: 'password',
			showClearButton: true,
			placeholder: "¡Ingrese la Contraseña!",
			maxLength: 100,
			buttons: ['clear', {
				name: 'key',
				location: 'before',
				options: {
					icon: 'fa fa-key',
					stylingMode: 'text'
				},
			}, {
				name: 'password',
				location: 'after',
				options: {
					icon: 'fa fa-eye',
					stylingMode: 'text',
					onClick() {
						$('#TxtContrasena').dxTextBox("instance").option('mode', $('#TxtContrasena').dxTextBox("instance").option('mode') === 'text' ? 'password' : 'text');
					},
				},
			}]
		}).dxValidator({
			validationGroup: "validationGroup_FormularioIngresar",
			validationRules: [{
				type: 'required',
				message: '¡Ingrese la Contraseña!'
			}]
		});
    
        $('#BtnIngresar').on('click', function(){
            var resultadoFormulario = DevExpress.validationEngine.validateGroup("validationGroup_FormularioIngresar")
            if (resultadoFormulario.isValid) {
        
                let txtUsuario = $('#TxtUsuario').dxTextBox("instance").option("value");
                let txtContrasena = $('#TxtContrasena').dxTextBox("instance").option("value");
            
                $.post("/ajax/iniciar/sesion/", { txtUsuario, txtContrasena }, function (data) {
    
                    if (data.resultado == "true") {
                        $(location).attr('href', data.url);
                    } else if (data.resultado == "false"){
                        mensajeError(`Error, ${data.error}`);
                    } else if (data.resultado == "error"){
                        mensajeError("¡Error al Ingresar al Sitio Web!");
                    } 
    
                }, 'json')
                
            } else {
                var control = resultadoFormulario.brokenRules[0].validator.option("adapter").editor;  
                control.focus();  
        
                mensajeError('El Llenado de este Campo es de carácter Obligatorio.');
            }
        });

        popup.repaint();
    });

    $('#PopupImagen').dxPopup({
        contentTemplate: "contenidoPopupImagen",
        height: "auto",
        showTitle: true,
        titleTemplate: "tituloPopupImagen",
        visible: false,
        dragEnabled: true,
        closeOnOutsideClick: true,
        shading: true,
        //resizeEnabled : true 
        wrapperAttr: {
            class: "dxPopupWidthUno"
        }
    })

    $('#PopupCambioContrasena').dxPopup({
		contentTemplate: "contenidoPopupCambioContrasena",
		height: "auto",
		width: 380,
		showTitle: true,
		titleTemplate: "tituloPopupCambioContrasena",
		visible: false,
		dragEnabled: true,
		closeOnOutsideClick: false,
		shading: true,
		//resizeEnabled : true
	})

	$('.btn_cambio_contrasena').on('click', function(){
		var popup = $("#PopupCambioContrasena").dxPopup("instance");
		popup.show();
		var content = popup.content();
	
		content.css({
			"padding": 4
		})
	
		popup.option("position", {
			my: "center",
			at: "center"
		})
	
		$('#TxtContrasenaNueva').dxTextBox({
			value: "",
			mode: 'password',
			showClearButton: true,
			placeholder: "¡Ingrese la Contraseña!",
			maxLength: 100,
			buttons: ['clear', {
				name: 'password',
				location: 'after',
				options: {
					icon: 'fa fa-eye',
					stylingMode: 'text',
					onClick() {
						$('#TxtContrasenaNueva').dxTextBox("instance").option('mode', $('#TxtContrasenaNueva').dxTextBox("instance").option('mode') === 'text' ? 'password' : 'text');
					},
				},
			}]
		}).dxValidator({
			validationGroup: "validationGroup_FormularioCambioContrasena",
			validationRules: [{
				type: 'required',
				message: '¡Ingrese la Contraseña!'
			}]
		});
	
		$('#TxtContrasenaConfirmar').dxTextBox({
			value: "",
			mode: 'password',
			showClearButton: true,
			placeholder: "¡Confirme la Contraseña!",
			maxLength: 100,
			buttons: ['clear', {
				name: 'password',
				location: 'after',
				options: {
					icon: 'fa fa-eye',
					stylingMode: 'text',
					onClick() {
						$('#TxtContrasenaConfirmar').dxTextBox("instance").option('mode', $('#TxtContrasenaConfirmar').dxTextBox("instance").option('mode') === 'text' ? 'password' : 'text');
					},
				},
			}]
		}).dxValidator({
			validationGroup: "validationGroup_FormularioCambioContrasena",
			validationRules: [{
				type: 'required',
				message: '¡Confirme la Contraseña!'
			}]
		});
	
		$('#BtnCancelarCambioContrasena').dxButton({
			icon: 'close',
			type: 'danger',
			text: 'Cancelar',
			stylingMode: 'contained',
			width: "100%",
			onClick() {
	
				DevExpress.ui.dialog.confirm("¿Seguro(a) de descartar los cambios realizados?", "Confirmación").done(function (r) {
					if (r) {
						$("#dataCambioContrasena").attr('data_opc', 1);
						$("#PopupCambioContrasena").dxPopup("instance").hide();
					}
				});
	
			}
		});
	
		$('#BtnGuardarCambioContrasena').dxButton({
			icon: 'check',
			type: 'success',
			text: 'Ok',
			stylingMode: 'contained',
			width: "100%",
			onClick: onClick_BtnGuardarCambioContrasena
		});
	
		popup.repaint();
	});

	function onClick_BtnGuardarCambioContrasena() {
		var resultadoFormulario = DevExpress.validationEngine.validateGroup("validationGroup_FormularioCambioContrasena")
		if (resultadoFormulario.isValid) {
	
			DevExpress.ui.dialog.confirm("¿Seguro(a) de Actualizar la Contraseña?", "Confirmación").done(function (r) {
				if (r) {
					
					let txtContrasenaNueva = $('#TxtContrasenaNueva').dxTextBox("instance").option("value");
					let txtContrasenaConfirmar = $('#TxtContrasenaConfirmar').dxTextBox("instance").option("value");
				
					$.post("/editar/contrasena/actual/ajax/", { txtContrasenaNueva, txtContrasenaConfirmar }, function (data) {
		
						if (data.resultado == "true") {
							
							$("#PopupCambioContrasena").dxPopup("instance").hide();
							mensajeSuccess("Contraseña Actualizada exitosamente!", "Exito");
							
						} else if (data.resultado == "false"){
							mensajeError("¡Las Contraseñas no son Iguales!");
						} else {
							mensajeError(`${data.resultado}`);
						}
		
					}, 'json')
	
				}
			
			});
	
		} else {
			var control = resultadoFormulario.brokenRules[0].validator.option("adapter").editor;  
			control.focus();  
	
			mensajeError('El Llenado de este Campo es de carácter Obligatorio.');
		}
	}
});