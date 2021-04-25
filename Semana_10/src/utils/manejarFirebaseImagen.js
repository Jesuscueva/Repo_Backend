const { Storage } = require("@google-cloud/storage")
// Inicializamos el onjeto de firabase para poder conectarme al bucket (almacenamiento)

const storage = new Storage({
    projectId: "prueba-firebase-jesus",
    keyFilename: "./credenciales_firebase.json",
});

// se crea la variable bucket que se usa como referencia  al link del storage

const bucket = storage.bucket("prueba-firebase-jesus.appspot.com")

const subirArchivo = (archivo) => {
    return new Promise((resolve, reject) => {
        // validamos que tengamos un archivo si es que no hay hacemos un rechazo(reject)
        if(!archivo) reject("No se encontro el archivo");
        // comenzamos a cargar el archivo mediante su nombre
        const fileUpload = bucket.file(archivo.originalname)
        // agregamos configuracion adicional de nuestro archivo a subir como x ejemplo su metadata
        const blobStream = fileUpload.createWriteStream({
            metadata: {
                contentType: archivo.mimetype
            }
        })
        // si hay un error al momento de subir el archivo ingresamos a su estado "error"
        blobStream.on("error", (error)=> {
            reject(`Hubo un error al subir el archivo: ${error}`)
        })
        blobStream.on("finish", async () => {
            fileUpload.getSignedUrl({
                action: "read",
                expires: "04-10-2021"
            }).then((link)=> resolve(link)).catch((error)=> reject(error))
        })
        // aca es donde se culmina el proceso de subida de imagenes
        // se le manda el buffer del archivo (los bytes del archivo)
        blobStream.end(archivo.buffer)
    })
}


const eliminarArchivo = async(nombre) => {
    try{
        const rpta = await bucket.file(nombre).delete()
        console.log(rpta)
        return true
    }catch(error){
        console.log(error)
        return false
    }
}

module.exports = { subirArchivo, eliminarArchivo }
