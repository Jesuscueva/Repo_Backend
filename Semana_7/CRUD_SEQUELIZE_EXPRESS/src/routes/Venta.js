const { Router } = require("express");
const venta_controller = require("../controllers/Venta");

const venta_router = Router();

venta_router.post("/venta", venta_controller.crearVenta);

module.exports = venta_router;
