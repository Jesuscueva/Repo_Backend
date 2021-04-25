const { subirArchivo, eliminarArchivo } = require("../utils/manejarFirebaseImagen")


const subirImagen = async (req, res) => {
    const archivo = req.file;
    const link = await subirArchivo(archivo).catch((error)=> res.json({
        success: false,
        content: null,
        message: error
    }))
    return res.json({
        success: true,
        content: link,
        message: "Imagen subida exitosamente"
    })
}

const eliminarImagen = async (req, res) => {
    const { nombre } = req.query
    if(await eliminarArchivo(nombre)){
        res.json({
            success: true,
            content: null,
            message: "Archivo eliminado exitosamente"
        })
    } else{
        res.status(400).json({
            success: true,
            content: null,
            message: "error al eliminar"
        })
    }
}

module.exports = {
    subirImagen,
    eliminarImagen,
}