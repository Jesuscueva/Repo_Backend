const { Router } = require("express");
const usuario_controller = require("../controllers/Usuario");

const usuario_router = Router();

usuario_router.post("/registro", usuario_controller.registro);
usuario_router.post("/login", usuario_controller.login);

module.exports = usuario_router;
