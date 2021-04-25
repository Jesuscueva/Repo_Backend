const { Router } = require("express")

const Multer = require("multer")
const imagen_controller = require("../controllers/imagen")

const imagen_router = Router()

// se le da atributos que guarden en la memory storage (En la RAM)

const multer = Multer({
    storage: Multer.memoryStorage(),
    limits: {
        //UNIDAD EXPRESADA EN BYTE
        // BYTES * 1024 => KILOBYTES * 1024 => MEGABYTES
        fileSize: 5 * 1024 * 1024,
    }
})

imagen_router.post("/subirImagen", multer.single('imagen'),imagen_controller.subirImagen)

imagen_router.delete("/eliminarImagen", imagen_controller.eliminarImagen)
module.exports = imagen_router;