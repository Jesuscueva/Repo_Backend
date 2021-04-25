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
        this.escucharScoket()
    }
    escucharScoket(){
        this.io.on("connect", (dibujo) => {
            console.log(dibujo.id)
            dibujo.on("emit", (dicujo)=> {
                console.log(dicujo)
                dibujo.broadcast.emit("coordenadas", {
                    x : dicujo[0],
                    y: dicujo[1]
                })
            })
        })
        
    }

    start(){
        this.httpServer.listen(this.puerto, ()=>{
            console.log(`
            Servidor corriendo exitosamente en http://127.0.0.1:${this.puerto}`)
        })
    }
}