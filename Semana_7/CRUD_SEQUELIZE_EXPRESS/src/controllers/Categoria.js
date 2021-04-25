const { Categoria } = require("../config/Relaciones");
const { Op } = require("sequelize");
// CREATE
const crearCategoria = async (req, res) => {
  // Si queremos registrar los datos tal y como nos llega del front usamos el metodo create, si queremos modificar o validar primero usamos dos pasos que es .build() y luego el .save()
  // INSERT INTO T_CATEGORIA VALUES ('','','')
  const nuevaCategoria = await Categoria.create(req.body).catch((error) => {
    return res.status(500).json({
      success: false,
      content: error,
      message: "Error al crear la categoria",
    });
  });
  console.log(nuevaCategoria);
  return res.status(201).json({
    success: true,
    content: nuevaCategoria,
    message: "Categoria creada exitosamente",
  });
};

// READ ALL
const devolverCategorias = async (req, res) => {
  // SELECT * FROM T_CATEGORIA
  // https://sequelize.org/master/manual/model-querying-finders.html
  const categorias = await Categoria.findAll().catch((error) =>
    res.status(500).json({
      success: false,
      content: error,
      message: "Hubo un error al devolver las categorias",
    })
  );
  return res.json({
    success: true,
    content: categorias,
    message: null,
  });
};

// READ BY ID
const devolverCategoriaPorId = async (req, res) => {
  console.log(req.params);
  const { id } = req.params;
  const categoria = await Categoria.findByPk(id).catch((error) =>
    res.status(500).json({
      success: false,
      content: error,
      message: "Hubo un error",
    })
  );

  return res.json({
    success: true,
    content: categoria,
    // OPERADOR TERNARIO => CONDICION ? VERDADERA : FALSA
    message: categoria ? null : "Categoria no existe",
  });
};

// UPDATE
const editarCategoriaPorId = async (req, res) => {
  const { id } = req.params;
  // UPDATE T_CATEGORIA SET (...) WHERE CATEGORIAID = ID
  const resultado = await Categoria.update(req.body, {
    where: {
      categoriaId: id,
    },
  }).catch((error) =>
    res.status(500).json({
      success: false,
      content: error,
      message: "Hubo un error al actualizar la categoria",
    })
  );
  // el resultado sera la cantidad de registros actualizados me lo devolvera en un array con una sola posicion
  return res.status(201).json({
    success: true,
    content: null,
    // mediante el uso del operador ternario indicar si se actualizo o no!
    message:
      resultado[0] === 0
        ? "No se actualizo nada"
        : "Categoria actualizada exitosamente",
  });
};

// DELETE
const eliminarCategoriaPorId = async (req, res) => {
  const { id } = req.params;
  const resultado = await Categoria.destroy({
    where: {
      categoriaId: id,
    },
  }).catch((error) =>
    res.status(500).json({
      success: false,
      content: error,
      message: "Hubo un error al actualizar la categoria",
    })
  );
  return res.json({
    success: true,
    content: null,
    message:
      resultado !== 0
        ? "Categoria eliminada exitosamente"
        : "No se encontro la categoria a eliminar",
  });
};

// Listar las categorias segun una coincidencia por el nombre
const listarCategoriasLikeName = async (req, res) => {
  // para usar parametros dinamicos (no lo indicamos en la ruta) usamos el query el cual va a capturar todos los parametros y lo mostrara en un JSON
  const { nombre } = req.query;
  // SELECT CAT_NOMBRE FROM T_CATEGORIA WHERE CAT_NOMBRE LIKE  %NOMBRE%
  const resultado = await Categoria.findAll({
    where: {
      categoriaNombre: {
        [Op.like]: "%" + nombre + "%",
      },
    },
    /*
        attributes: ['categoriaNombre'], // para definir que columnas queremos mostrar
        attributes: { // para excluir que columnas no queremos devolver

            exclude : ['categoriaId']
        }
        */
  });
  console.log(resultado);
  return res.json({
    success: true,
    content: resultado,
  });
};

module.exports = {
  crearCategoria,
  devolverCategorias,
  devolverCategoriaPorId,
  editarCategoriaPorId,
  eliminarCategoriaPorId,
  listarCategoriasLikeName,
};
