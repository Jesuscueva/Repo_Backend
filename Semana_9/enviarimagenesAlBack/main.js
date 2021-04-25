const nombre = document.getElementById("nombre")
const cantidad = document.getElementById("cantidad")
const precio = document.getElementById("precio")
const foto = document.getElementById("foto")
const registrar = document.getElementById("btnRegistrar")

const mostrar = document.getElementById("btnMostrar")

const informacion = document.getElementById("informacion")

const URL = "http://127.0.0.1:8000"

const formData  = new FormData

registrar.addEventListener("click", async(e)=> {
    e.preventDefault()
    formData.append("platoDescripcion", nombre.value)
    formData.append("platoCantidad", cantidad.value)
    // el input file siempre guarda los files en forma de un array, aun asi solo se le pasa 1
    formData.append("platoFoto", foto.files[0])
    formData.append("platoPrecio", precio.value)
    const resultado = await fetch(URL + "/plato", {
        method:"POST",
        body: formData,
        headers:{
            Authorization: "Bearer 123123.123123.12312312"
        }
    })
    const json = await resultado.json()
    console.log(json)
})

mostrar.addEventListener("click", async(e)=>{
    e.preventDefault()
    const resultado = await fetch(URL+"/plato", {
        method: "GET"
    })
    const json = await resultado.json()
    informacion.innerText = json    
})