const { Schema } = require("mongoose")

const imagenSchema = new Schema({
    imagen_url: String
})
module.exports = {
    imagenSchema
}
