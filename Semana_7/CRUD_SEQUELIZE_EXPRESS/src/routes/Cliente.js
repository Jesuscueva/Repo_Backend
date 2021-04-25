const { Router } = require("express");
const cliente_controller = require("../controllers/Cliente");
const { wachiman } = require("../utils/Validadores");

const cliente_router = Router();
cliente_router.post("/cliente", wachiman, cliente_controller.crearCliente);

module.exports = cliente_router;
