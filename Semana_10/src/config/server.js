
const express = require("express");
const {json} = require("body-parser")
const mongoose = require("mongoose")
const curso_router = require("../routes/curso");
const usuario_router = require("../routes/usuario")
const imagen_router = require("../routes/imagen")

module.exports = class Server {
    constructor() {
        this.app = express();
        this.puerto = process.env.PORT || 5000
        this.CORS()
        this.bodyParser()
        this.rutas()
        this.conectarMongoDb()
    }
    CORS(){
        this.app.use((req, res, next)=> {
            res.header('Access-Control-Allow-Origin', '*')
            res.header('Access-Control-Allow-Header', 'Content-Type, Authorization' );
            res.header('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE")
            next()
        })
    }
    /**
     * 
     */
    bodyParser(){
        this.app.use(json())
    }
    rutas(){
        this.app.get('/', (req, res)=> {
            return res.json({
                success: True,
                content: null,
                message: "Bienvenido a mi API"
            }).end()
        })
        this.app.use(curso_router);
        this.app.use(usuario_router)
        this.app.use(imagen_router)
    }
    async conectarMongoDb(){
        await mongoose.connect("mongodb://localhost:27017/plataforma_educativa", {
            useNewUrlParser: true, // para indicar que estamos usando formato de coneccion url
            useUnifiedTopology: true,
             // para indicar que vamos a usar un nuevo motor de administracion en conneciones, solamente indicar false cuando la conexion sea poco estable
            useCreateIndex: true,
            // para ver documentacion https://mongoosejs.com/docs/connections.html#options
            useFindAndModify: false,// sirve para indicar que los metodos findOneAndUpdate y findOneAndDelete no se usaran porque ya son deprecados (obsoletos)
        }).catch((e) => console.log(e), console.log("Base de datos conectada"))
    }
    start(){
        this.app.listen(this.puerto, ()=>{
            console.log(`Servidor corriendo en http://127.0.0.1:${this.puerto}`)
        })
    }
}