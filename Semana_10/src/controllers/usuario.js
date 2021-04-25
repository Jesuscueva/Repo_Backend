require("dotenv").config()
const {AES, enc} = require("crypto-js")
const { enviarCorreo } = require("../utils/manejadorCorreo")
const { Usuario, Curso } = require("../config/mongoose")
const {subirArchivo} = require("../utils/manejarFirebaseImagen")

const registro = async (req, res) => {
    const objUsuario = new Usuario(req.body)
    objUsuario.encriptarPassword(req.body.password)
    const usuarioCreado = await objUsuario.save().catch((error) => 
        res.status(500).json({
            success: true,
            content: error,
            message: "Error al crear el usuario"
        })
    )
    return res.status(201).json({
        success: true,
        content: usuarioCreado,
        message: "Usuario Creado exitosamente"
    })
}

const login = async(req, res)=> {
    const { email, password } = req.body
    const usuarioEncontrado = await Usuario.findOne({
        usuario_email: email
    }).catch((error)=> 
        res.status(500).json({
            success: false,
            content: error,
            message: "Error al buscar el usuario"
        })
    )
    if(!usuarioEncontrado){
        return res.status(404).json({
            success: false,
            content: null,
            message: "Correo no se encuentra"
        })
    }

    if(usuarioEncontrado.validarPassword(password)) {
        return res.json({
            success: true,
            content: usuarioEncontrado.generarJWT(),
            message: "Logeado correctamente"
        })
    }else {
        return res.status(404).json({
            success: false,
            content: null,
            message: "Error en la contraseña"
        })
    }
}


const inscribirCurso = async (req, res) => {
    /**
     * 1. usar la token para ver que usuario esta queriendo acceder a que curso 
     * 2. mediante la url indicar el id del curso (query)
     * 2.1 cer si el curso existe
     * 3. ver si el usuario ya esta inscrito en el curso y si lo esta no permitir volver a inscribirlo
     * 4. si no esta inscrito , inscribirlo
     */
    const curso_id =req.query.id
    const { usuario_id } = req.usuario;
    const cursoEncontrado = await Curso.findById(curso_id).catch((error) => 
        res.status(404).json({
            success: false,
            content: error,
            message: "No se encontro el curso"
        })
    )
    if (cursoEncontrado){
        const usuarioEncontrado = await Usuario.findById(usuario_id)
        const resultado = usuarioEncontrado.cursos.includes(curso_id)
        if(resultado && cursoEncontrado.usuarios.includes(usuario_id)){
            return res.json({
                success: false,
                content: null,
                message: "Usuario ya se encuentra en el curso"
                })
        }
        usuarioEncontrado.cursos.push(curso_id)
        usuarioEncontrado.save()

        cursoEncontrado.usuarios.push(usuario_id)
        cursoEncontrado.save()

    return res.status(201).json({
            success: true,
            content: usuarioEncontrado,
            message: "Curso Agregado exitosamente"
    })
    }



    res.send("ok")

}

const mostrarCursosUsuario = async(req, res) => {
    const { usuario_id } = req.usuario 

    const { cursos } = await Usuario.findById(usuario_id)
    console.log(cursos)

    let resultado = [];
    // await Promise.all(
    //     (resultado = cursos.map((curso)=> 
    //     Curso.findById(
    //         curso,
    //         "curso_nombre curso_descripcion curso_link curso_imagenes"
    //     ) ))
    // )

    for(let key in cursos){
        resultado.push(
            await Curso.findById(cursos[key], "curso_nombre curso_descripcion curso_link curso_imagenes")
        )}

    return res.json({
        success: true,
        content: resultado,
        message: null
    })

}

const editarUsuario = async(req, res) => {
    const {usuario_id } = req.usuario
    const link = await subirArchivo(req.file).catch((error) => res.json({
        success: false,
        content: error,
        message: "Error al subir imagen"
    }))
    if(link){
        if(req.body.usuario_password) delete req.body.usuario_password
        console.log(req.body)
        req.body.usuario_imagen = { imagen_url: link[0]}
        const usuarioActualizado = await Usuario.findByIdAndUpdate(usuario_id, req.body, {new:true})
        return res.json({
            success: true,
            content: usuarioActualizado,
            message: null
        })
    }
}

const cambiarPassword = async(req, res)=>{
    const { usuario_id } = req.usuario
    const { newPassword, oldPassword } = req.body;
    const usuarioEncontrado =  await Usuario.findById(usuario_id)
    console.log(usuarioEncontrado.usuario_password)
    const resultado = usuarioEncontrado.validarPassword(oldPassword)
    if(!resultado){
        return res.status(400).json({
            success: false,
            content: null,
            message: "Contraseña invalida"
        })
    } else {
        usuarioEncontrado.encriptarPassword(newPassword)
        await usuarioEncontrado.save()
        return res.status(200).json({
            success: true,
            content: usuarioEncontrado,
            message: "Contraseña Actualizada correctamente"
        })
    }
    
}


const resetPassword = async (req, res) => {
    const fechaVencimiento = new Date().setHours(1).toString();
    const hash = AES.encrypt(fechaVencimiento, process.env.PASSWORD);
    const { email } = req.body;
    try {
        const usuarioEncontrado = await Usuario.findOne({ usuario_email: email });
        if (!usuarioEncontrado) {
        return res.status(404).json({
            success: false,
            content: null,
            message: "Usuario no encontrado",
        });
        }
        usuarioEncontrado.usuario_password_recovery = hash;
        await usuarioEncontrado.save();
        const cuerpo = `Hola ${usuarioEncontrado.usuario_nombre} has solicitado el cambio de tu password, tu hash es ${hash}`;
        const resultado = await enviarCorreo(
        usuarioEncontrado.usuario_email,
        "Resetear password",
        cuerpo
        );
        return res.status(201).json({
        success: true,
        content: resultado,
        message: "Correo enviado exitosamente",
        });
    } catch (error) {
        return res.status(500).json({
        success: false,
        content: error,
        message: "Error",
        });
    }
    };

    
const consultarHash = async(req, res)=>{
    //validar si el hash existe 
    const { hash } = req.query
    const usuarioEncontrado = await Usuario.where({
        usuario_password_recovery : hash
    })
    if(!usuarioEncontrado) {
        return res.status(404).json({
            success: false,
            content: null,
            message: "hash incorrecto"
        })
    }
    const bytes = AES.decrypt(hash, process.env.PASSWORD)
    const horaOriginal = +bytes.toString(enc.Utf8)
    console.log(horaOriginal)
    const horaActual = new Date().setHours(0)
    console.log(horaActual)
    if(horaActual < horaOriginal){
        // console.log("aun hay tiempo")
        return res.json({
            success: true,
            content: true,
            message: "Aun hay Tiempo"
        })
    }else {
        // console.log("ya no hay tiempo")
        return res.json({
            success:false,
            content:false,
            message: "Aun no hay tiempo"
        })
    }

}

const changePassword = async (req, res) => {
    const { hash, newPassword } = req.body
    const usuarioEncontrado = await Usuario.findOne({
            usuario_password_recovery: hash
        })
    // console.log(usuarioEncontrado)
    if(!usuarioEncontrado){
        return res.status(500).json({
            success: false
        })
    }
    // console.log(usuarioEncontrado)
    usuarioEncontrado.encriptarPassword(newPassword)
    usuarioEncontrado.usuario_password_recovery = ""
    usuarioEncontrado.save()
    return res.json({
        success: true
    })


}

module.exports = {
    registro,
    login,
    inscribirCurso,
    mostrarCursosUsuario,
    editarUsuario,
    cambiarPassword,
    resetPassword,
    consultarHash,
    changePassword,
}