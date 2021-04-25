const { Router } = require("express")
const comentario_controller = require("../controllers/comentarios")

const { wachiman } = require("../utils/validator")

const comentario_router = Router()

module.exports = comentario_router