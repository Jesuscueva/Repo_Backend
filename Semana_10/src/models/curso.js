const { schema, Schema } = require("mongoose")
const moment = require("moment-timezone")
const { imagenSchema } = require("./imagen")

const fechaPeruana = moment.tz(Date.now(), "America/Lima")

const contenidoSchema = new Schema(
    {
        video_url: {
            type: String,
            required: true,
        },
        video_orden: {
            type: Number,
            required: true,
            min: 0
        },
        video_nombre: {
            type: String,
            maxlength: 80
        }
    },
    {
        _id: false
    }
)

const cursoSchema = new Schema({
    curso_nombre: {
        type: String,
        unique: true,
        required: true,
        uppercase: true,
        maxlength: 50
    },
    curso_descripcion: String,
    curso_link: String,
    curso_fecha_lanzamiento:{
        type: Date,
        min: "2021-01-01",
        max: "2021-04-30 23:59",
        default: fechaPeruana
    },
    curso_imagenes: [imagenSchema],
    curso_videos: [contenidoSchema],
    curso_publicado: {
        type: Boolean,
        default: false
    },
    curso_duracion: String,
    curso_costo: {
        type: Schema.Types.Decimal128,
        min:0
    },
    usuarios: [Schema.Types.ObjectId],
    comentarios : [Schema.Types.ObjectId],
})

module.exports = {
    cursoSchema
}