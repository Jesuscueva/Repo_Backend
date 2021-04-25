const { Producto, Categoria } = require("../config/Relaciones");
const { Op } = require("sequelize");
const crearProducto = async (req, res) => {
  const nuevoProducto = await Producto.create(req.body).catch((error) =>
    res.status(500).json({
      success: false,
      content: error,
      message: "Error al crear el producto",
    })
  );
  return res.status(201).json({
    success: true,
    content: nuevoProducto,
    message: "Producto creado exitosamente",
  });
};

// hacer el devolver producto por busqueda por nombre
const devolverProductosPorNombre = async (req, res) => {
  const { nombre } = req.query;
  const productos = await Producto.findAll({
    where: {
      productoNombre: {
        [Op.like]: "%" + nombre + "%",
      },
      productoEstado: true, // solamente mostrara los productos activos
    },
    include: {
      model: Categoria,
    },
  });
  return res.json({
    success: true,
    content: productos,
  });
};

const editarProducto = async (req, res) => {
  const { id } = req.params;
  await Producto.update(req.body, {
    where: {
      productoId: id,
    },
  }).catch((error) =>
    res.json({
      succes: false,
      content: error,
      message: "Error al actualizar el producto",
    })
  );
  return res.status(201).json({
    success: true,
    content: null,
    message: "Se actualizo el producto exitosamene",
  });
};

module.exports = {
  crearProducto,
  devolverProductosPorNombre,
  editarProducto,
};
