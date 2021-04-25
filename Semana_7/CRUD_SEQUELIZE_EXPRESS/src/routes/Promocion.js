const { Router } = require("express");
const promocion_controller = require("../controllers/Promocion");

const promocion_router = Router();
promocion_router.post("/promocion", promocion_controller.crearPromocion);
promocion_router.get("/promocion", promocion_controller.devolverPromociones);

module.exports = promocion_router;
