const socket = io("http://127.0.0.1:3000")
const nombre = document.getElementById("nombre")
const ingresar = document.getElementById("ingresar")
const listaUsuarios = document.getElementById("lista-usuarios")
const listaMensajes = document.getElementById("lista-mensajes")
const mensaje = document.getElementById("mensaje")

socket.on("connect", () =>{
    console.log("conectado")
})

ingresar.addEventListener("click", (e) => {
    e.preventDefault()
    const classbtn = ingresar.classList

    if (classbtn.contains("btn-danger")){
        socket.disconnect().connect()
        ingresar.innerText = "Ingresar al Chat"
        ingresar.className = "btn btn-block btn-success"
    } else {
        socket.emit("configurar-cliente", nombre.value)
        nombre.value = ""
        ingresar.innerText = "Desconectar"
        ingresar.className = "btn btn-block btn-danger"
        nombre.disabled = true
    }


})

socket.on("lista-usuarios", (usuarios)=>{
    console.log(usuarios)
    listaUsuarios.innerHTML = ""
    for(const key in usuarios){
        const usuarioLi = document.createElement("li")
        usuarioLi.className = "list-group-item"
        usuarioLi.innerText = usuarios[key].nombre
        listaUsuarios.appendChild(usuarioLi)
    }
})


mensaje.addEventListener("keyup", (e)=> {
    // console.log(e.key)
    if(e.key === "Enter"){
        socket.emit("mensaje", mensaje.value)
    }
    
})
socket.on("lista-mensajes", (mensajes) => {
    console.log(mensajes)
    listaMensajes.innerText = ""

    mensajes.forEach(mensaje => {
        const mensajeLi = document.createElement("li")
        mensajeLi.className = "list-group-item"
        mensajeLi.innerHTML = `<strong>${mensaje.cliente} dice:</strong> ${mensaje.mensaje}`
        listaMensajes.appendChild(mensajeLi)
    })
})