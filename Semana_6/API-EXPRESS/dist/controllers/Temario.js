// let funcionar en el scope actual y no es reconocido fuera de el
// var funciona de manera global en el documento
// const funciona como una constante en la cual no se puede cambiar su valor despues de definirlo
let temarios = [];
const crearTemario = (req, res)=>{
    // el request sirve para recibir todo lo que el usuario nos este mandando
    console.log(req.body);
    temarios.push(req.body);
    return res.json({
        success: true
    })
}
const devolverTemarios = (req, res)=>{
    // devolver todos los temarios
    return res.json({
        success: true,
        content: temarios,
        message: null
    })
}

const actualizarTemario = (req, res)=>{
    // console.log(req.params); // devuelve todos los valores dados por el parametro
    let {id} = req.params;
    if (temarios[id]){
        temarios[id] = req.body;
        return res.json({
            success: true,
            content: temarios[id],
            message: 'Temario actualizado exitosamente'
        })
    }else{
        return res.status(404).json({
            success: false,
            content: null,
            message: 'Temario no existe'
        })
    }
}

module.exports={
    crearTemario,
    devolverTemarios,
    actualizarTemario
}