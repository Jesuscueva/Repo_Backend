const {Router} = require("express")
const usuario_controller = require("../controllers/usuario")
const { usuarioSchema } = require("../models/usuario")
const { wachiman } = require("../utils/validador")
const Multer = require("multer")


const multer = Multer({
    storage: Multer.memoryStorage(),
    limits: {
        //UNIDAD EXPRESADA EN BYTE
        // BYTES * 1024 => KILOBYTES * 1024 => MEGABYTES
        fileSize: 5 * 1024 * 1024,
    }
})

const usuario_router = Router()

usuario_router.post("/registro", usuario_controller.registro)
usuario_router.post('/login', usuario_controller.login)
usuario_router.post('/inscribir',wachiman , usuario_controller.inscribirCurso)
usuario_router.get('/mostrarCursos',wachiman, usuario_controller.mostrarCursosUsuario)
usuario_router.put("/actualizarUsuario", wachiman, multer.single("imagen"),usuario_controller.editarUsuario)

usuario_router.post("/cambiarPassword", wachiman, usuario_controller.cambiarPassword)

usuario_router.post("/resetPassword", usuario_controller.resetPassword)
usuario_router.get("/consultarHash", usuario_controller.consultarHash)
usuario_router.post("/newPasword", usuario_controller.changePassword)

module.exports = usuario_router