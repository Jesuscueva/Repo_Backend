const { model } = require("mongoose")
const { usuarioSchema } = require("../models/usuario")
const { cursoSchema } = require("../models/curso")
const { comentarioSchema } = require("../models/comentarios")

const Usuario = model("usuario", usuarioSchema)
const Curso = model("curso", cursoSchema)
const Comentario = model("comentario", comentarioSchema)

module.exports = {
    Usuario,
    Curso,
    Comentario,
};
