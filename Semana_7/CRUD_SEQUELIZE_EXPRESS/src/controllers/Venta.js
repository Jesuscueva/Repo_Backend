const { conexion } = require("../config/Sequelize");
const {
  Producto,
  Promocion,
  Detalle,
  CabeceraNota,
} = require("../config/Relaciones");

const crearVenta = async (req, res) => {
  const { productos, usuario, cliente, serie } = req.body;
  // primero defino la transaccion
  const transaccion = await conexion.transaction();
  // creamos nuestra cabecera de la venta
  try {
    const cabeceraVenta = await CabeceraNota.create(
      {
        cabeceraSerie: serie,
        cabeceraTotal: 0.0,
        cabeceraDescuento: 0.0,
        cabeceraSubTotal: 0.0,
        usu_id: usuario,
        cli_dni: cliente,
      },
      { transaction: transaccion }
    );
    let descuentoTotal = 0;
    let subTotal = 0;

    // 1. ver si el producto tiene promocion vigente

    for (const key in productos) {
      const { id, cantidad } = productos[key];
      const productoEncontrado = await Producto.findByPk(id, {
        include: {
          // dentro del modelo promocion solamente quiero la primera coincidencia de la promocion mediante el ordenamiento de la columna promocionFechaHasta de manera descendente
          model: Promocion,
          order: [["promocionFechaHasta", "DESC"]],
          limit: 1,
        },
      });
      // ahora iteramos todas las posibles promociones del producto (las vigentes y no vigentes)
      const { promociones } = productoEncontrado;
      const fechaActual = new Date();
      let promocionActiva;
      for (const key1 in promociones) {
        if (fechaActual < promociones[key1].promocionFechaHasta) {
          promocionActiva = promociones[key1];
          // aca lo haria
          const descuentoTemporal =
            promociones[key1].promocionDescuento * cantidad;
          const precioNormal = productoEncontrado.productoPrecio * cantidad;
          descuentoTotal += precioNormal - descuentoTemporal;
          // descuentoTotal = descuentoTotal + (precioNormal - descuentoTemporal)
        }
      }
      // aqui creamos el detalle de la venta
      const detalleVenta = await Detalle.create(
        {
          detalleCantidad: cantidad,
          detallePrecioUnitario: promocionActiva
            ? promocionActiva.promocionDescuento
            : productoEncontrado.productoPrecio,
          prod_id: id,
          cab_id: cabeceraVenta.cabeceraId,
        },
        { transaction: transaccion }
      );
      // ahora actualizo las cantidades de mi producto
      await Producto.update(
        {
          productoCantidad: productoEncontrado.productoCantidad - cantidad,
        },
        {
          where: {
            productoId: id,
          },
          transaction: transaccion,
        }
      );
      subTotal += detalleVenta.detallePrecioUnitario * cantidad;
    }
    // actualizamos la cabecera de la venta con los campos de total, subtotal y descuento
    await CabeceraNota.update(
      {
        cabeceraTotal: subTotal,
        cabeceraSubTotal: subTotal + descuentoTotal,
        cabeceraDescuento: descuentoTotal,
      },
      {
        where: {
          cabeceraId: cabeceraVenta.cabeceraId,
        },
        transaction: transaccion,
      }
    );
    // si todo esta correctamente y no hubo ningun error, se procedera a guardar los cambios en la bd
    await transaccion.commit();
    return res.status(201).json({
      success: true,
      content: CabeceraNota,
      message: "Se genero la venta exitosamente",
    });
  } catch (error) {
    // si hubo algun error en cualquiera de las escrituras en la bd, saltará al catch y por ende ningun cambio se guardara en la bd gracias al rollback
    await transaccion.rollback();
    return res.status(500).json({
      success: false,
      content: error,
      message: "Error al generar la venta",
    });
  }

  // 2. crear el detalle de la venta
  // 3. restar la cantidad del producto del inventario
  // 4. Agregar el total a la cabecera de la venta
  // 5. Generar la cabecera
  // NOTA: se recomienda solamente usar la transaccion en sentencias que modifique nuestra bd (insert, delete, update)
};

module.exports = {
  crearVenta,
};
