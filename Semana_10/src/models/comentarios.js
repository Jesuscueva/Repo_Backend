const {Schema} = require("mongoose")

const comentarioSchema = new Schema({
    comentario: {
        type: String,
        maxlength: 100,
        required: true
    },
    usuario: {
        type: Schema.Types.ObjectId,
        required: true,
    },
    curso: {
        type: Schema.Types.ObjectId,
        required: true
    },
})

module.exports = {
    comentarioSchema
}
