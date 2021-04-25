const { Cliente } = require("../config/Relaciones");

const crearCliente = async (req, res) => {
  // solamente un usuario logeado puede crear clientes
  const nuevoCliente = await Cliente.create(req.body).catch((error) =>
    res.status(500).json({
      success: false,
      content: error,
      message: "Error al crear el cliente",
    })
  );
  return res.status(201).json({
    success: true,
    content: nuevoCliente,
    message: "Cliente creado exitosamente",
  });
};
// mandar foto o screenshot del postman o objeto
// mandar screenshot o codigo del controlador
// mandar screenshot o codigo del enrutador

module.exports = {
  crearCliente,
};
