const { Schema } = require("mongoose")
const {imagenSchema} = require("./imagen")
const {hashSync, compareSync} = require("bcrypt")
const { sign } = require("jsonwebtoken")
require("dotenv").config()

const telefonoSchema = new Schema({
    fono_codigo: {
        type:Number,
        min: 1,
        max: 99
    },
    fono_numero: {
        type: String,
        minlength: 6,
        maxlength: 10
    }
},
{
    _id: false
})

const usuarioSchema = new Schema({
    usuario_nombre: {
        type: String,
        require: true,
        alias: "usu_nomb"
    },
    usuario_apellido: {
        type: String,
        maxlength: 25,
        require: true
    },
    usuario_email: {
        type: String,
        maxlength: 50,
        minlenght: 10,
        unique: true
    },
    usuario_password: String,
    usuario_categoria: {
        type: Number,
        mon: 1,
        max: 4
    },
    usuario_password_recovery: {
        type: String,
        require: false
    },
    usuario_telefono: [
        telefonoSchema
    ],
    usuario_imagen: imagenSchema,
    cursos: [Schema.Types.ObjectId],
    comentarios: [Schema.Types.ObjectId]
}, 
{
    timestamps: {
        createdAt: "fecha_creacion",
        updatedAt: "fecha_actualizacion"
    },
})


usuarioSchema.methods.encriptarPassword = function (password){
    this.usuario_password =  hashSync(password, 10)
}

usuarioSchema.methods.validarPassword = function(password){
    return compareSync(password, this.usuario_password)
}

usuarioSchema.methods.generarJWT = function(){
    const payload = {
        usuario_id : this._id
    }

    const password = process.env.JWT_SECRET
    return sign(payload, password, {expiresIn: "1h"}, { algorithm: "RS256"})
}

module.exports = {
    usuarioSchema,
}