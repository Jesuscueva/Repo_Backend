import express from "express"
import { Server } from "http"
import socketIo from "socket.io"

export default class ServidorSocket{
    constructor(){
        this.app = express()
        this.puerto = process.env.PORT || 3000
        this.httpServer = new Server(this.app)
        this.io = socketIo(this.httpServer, {
            cors: {
                origin: "*",
                methods: "*"
            }
        })
        this.escucharSocket()
        this.rutas()
    }
    escucharSocket(){
        let usuarios = []
        const mensajes = []
        this.io.on("connect", (cliente) => {
            this.io.emit("lista-usuarios", usuarios)
            // console.log(cliente)
            console.log(`Se conecto el cliente ${cliente.id}`)
            cliente.on("disconnect", (motivo) => {
                console.log(`Se desconecto el cliente ${cliente.id}`)
                console.log(motivo)
                usuarios = usuarios.filter((usuario) => usuario.id !== cliente.id);
                this.io.emit("lista-usuarios", usuarios)
                // pransport close => cuando el cliente cierra sesion o cierra pestaña
                // ping timeout => cuando el tiempo de espera es demasiado prolongado
            })
            cliente.on("configurar-cliente", (nombre) => {
                console.log(nombre)
                usuarios.push({
                    id: cliente.id,
                    nombre,
                });
                this.io.emit("lista-usuarios", usuarios)
            })
            cliente.on("mensaje", (mensajeUsu)=>{
                const usuario = usuarios.filter(usuario => usuario.id === cliente.id)[0]
                console.log(usuario)
                mensajes.push({
                    cliente: usuario.nombre,
                    mensaje: mensajeUsu
                })
                this.io.emit("lista-mensajes", mensajes)
            })
        })  
    }
    rutas(){
        this.app.get('/', (req, res) => {
            res.json({
                success: true,
                content: null,
                message: "Bienvenido a mi app de sockets 🔌🔌"
            })
        } )
    }
    start(){
        this.httpServer.listen(this.puerto, ()=>{
            console.log(`
            Servidor corriendo exitosamente en http://127.0.0.1:${this.puerto}`)
        })
    }
}