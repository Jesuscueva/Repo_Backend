const socket = io("http://127.0.0.1:3000")

socket.on("connect", () =>{
    console.log("conectado")
})


function setup(){
    createCanvas(300, 300);
    background(0);
    socket.on("coordenadas", (data)=> {
        fill(0,0,255)
        noStroke()
        ellipse(data.x, data.y, 10, 10)
    })
}
function mouseDragged(){
    fill(112, 239, 65)
    noStroke()
    ellipse(mouseX, mouseY, 10, 10)
    enviarPunto(mouseX, mouseY)
    socket.emit("emit", [mouseX, mouseY]
    )
}

const enviarPunto = (posX, posY) =>{
    console.log(`Posicion x: ${posX}`)
    console.log(`Posicion y:${posY}`)
}