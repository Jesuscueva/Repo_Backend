import requests
from datetime import datetime
from .models import CabeceraComandaModel, DetalleComandaModel, ComprobanteModel


def emitirComprobante(pedido, cabecera_id):
    # sunat_transaccion => sirve para indicar que tipo de transaccion estas reslizando, generalmente se usara el valor de 1 "VENTA INTERNA"
    cliente_demnominacion = ""
    # 6 => RUC, 1 => DNI, - => VARIOS
    documento = 0 # el numero de documento que toca crear
    cliente_documento = pedido["cliente_documento"]
    cliente_tipo_documento = pedido["cliente_tipo_documento"]
    tipo_comprobante = pedido["tipo_comprobante"]
    # buscamos ese pedido para jalar sus datos
    comanda= CabeceraComandaModel.objects.get(cabeceraId=cabecera_id)
    # sacamos el total del pedido
    total = float(comanda.cabeceraTotal)
    # el valor total sin el IGV
    total_gravada = total / 1.18
    # el valor total del IGV de la compra

    total_igv = total - total_gravada
    print(total_igv)
    # si la compra es mayor a 700 soles se tiene q dar el dni

    if len(pedido['cliente_documento'])> 0:
        base_url_apiperu = "https://apiperu.dev/api/"
        if cliente_tipo_documento == "RUC":
            base_url_apiperu = base_url_apiperu + "ruc/{}".format(cliente_documento)
        elif cliente_tipo_documento == "DNI":
            base_url_apiperu = base_url_apiperu + "dni/{}".format(cliente_documento)
        
        headers = {
            "Authorization": "Bearer 8389c125f5c44cd4791786ff111992abd840f1128ce626db5a67e18af56a18bb ",
            "Content-Type": "application/json"
        }

        respuestaApiPeru = requests.get(url=base_url_apiperu, headers=headers)

        if cliente_tipo_documento == "RUC":
            documento = 6
            cliente_demnominacion = respuestaApiPeru.json()["data"]["nombre_o_razon_social"]
        elif cliente_tipo_documento == "DNI":
            documento = 1
            cliente_demnominacion = respuestaApiPeru.json()["data"]["nombre_completo"]
    else:
        if total > 700:
            return {
                "error": "Para un monto mayor es necesario una identificacion"
            }
        documento = "-"
        cliente_demnominacion = "VARIOS"
        cliente_documento = "VARIOS"
    
    # ahora rellenamos el detalle del comprobante
    # codigo => codigo interno que manejamos nosotros
    # unidad_de_medida => NIU = PRODUCTOS | ZZ = SERVICIOS

    items = []
    # me retorna todo el detalle de un pedido
    for detalle in comanda.cabeceraDetalles.all():
        print(detalle)
        precio_unitario = float(detalle.detalleSubtotal)
        valor_unitario = precio_unitario / 1.18
        cantidad = detalle.detalleCantidad
        print(valor_unitario)
        print(cantidad)
        print(valor_unitario * .18 * cantidad)
        item = {
            "unidad_de_medida" : "NIU",
            "codigo": detalle.plato.platoId,
            "descripcion": detalle.plato.platoDescripcion,
            "cantidad": cantidad,
            "valor_unitario": valor_unitario,
            "precio_unitario": precio_unitario,
            "subtotal": valor_unitario*cantidad,
            "tipo_de_igv": 1,
            "igv": (valor_unitario * cantidad) * 0.18,
            "total": precio_unitario * cantidad,
            "anticipo_regularizacion": False
        }
        items.append(item)

    # indicar la serie y numero de comprobante
    # las facturas y notas asociadas con ellas empiezan con F
    # las boletas y notas asociadas con ellas empiezan con B

    serie = ""
    ultimoComprobante = None
    if tipo_comprobante == "BOLETA":
        tipo_comprobante = 2
        serie = "BBB1"
        # traer el ultimo comprobante que es boleta
        ultimoComprobante = ComprobanteModel.objects.filter(comprobanteTipo=2).order_by("-comprobanteNumero").first()
    elif tipo_comprobante == "FACTURA":
        tipo_comprobante = 1
        serie = "FFF1"
        # traer el ultimo comprobante que es factura
        ultimoComprobante = ComprobanteModel.objects.filter(comprobanteTipo=1).order_by("-comprobanteNumero").first()
    print("el ultimo comprobante")
    print(ultimoComprobante)
    if ultimoComprobante is None:
        numero = 1
    elif ultimoComprobante is not None:
        numero = ultimoComprobante.comprobanteNumero + 1
    
    cliente_email = pedido["cliente_email"]
    observaciones = pedido["observaciones"]
    comprobante_body = {
        "operacion": "generar_comprobante",
        "tipo_de_comprobante": tipo_comprobante,
        "serie": serie,
        "numero": numero,
        "sunat_transaction": 1,
        "cliente_tipo_de_documento": documento,
        "cliente_numero_de_documento": cliente_documento,
        "cliente_denominacion": cliente_demnominacion,
        "cliente_direccion": "",
        "cliente_email": cliente_email,
        "fecha_de_emision": datetime.now().strftime("%d-%m-%Y"),
        "moneda": 1,
        "porcentaje_de_igv": 18.00,
        "total_gravada": total_gravada,
        "total_igv": total_igv,
        "total": total,
        "detraccion": False,
        "observaciones": observaciones,
        "enviar_automaticamente_a_la_sunat": True,
        "enviar_automaticamente_al_cliente": True,
        "medio_de_pago": "EFECTIVO",
        "formato_de_pdf": "A4",
        "items": items
    }

    url_nubefact = "https://api.nubefact.com/api/v1/f9bc2e8e-153a-4585-991a-9fe55352c05a"

    headers_nubefact = {
        "Authorization": "73ac94afba76494dba64702f4061cabad51d5f8e0ab64d5ea414fcd98fec0a2f",
        "Content-Type": "application/json"
    }
    respuestaNubefact = requests.post(url=url_nubefact, json=comprobante_body, headers=headers_nubefact)

    json = respuestaNubefact.json()
    # ahora guardamos ese comprobante en nuestra bd
    nuevoComprobante = ComprobanteModel.objects.create(
        comprobanteSerie = serie ,
        comprobanteNumero= numero,
        comprobantePdf = json['enlace_del_pdf'],
        comprobanteCdr = json['enlace_del_cdr'],
        comprobanteXml = json['enlace_del_xml'],
        comprobanteRuc = cliente_documento,
        comprobanteTipo = tipo_comprobante
        )
    # comanda.comprobante = nuevoComprobante
    # comanda.save()
    return respuestaNubefact.json()


