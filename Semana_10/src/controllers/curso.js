const { Curso } = require("../config/mongoose");

const crearCurso = async (req, res) => {
    try {
        // Forma 1 : en dos pasos
        const nuevoCurso = new Curso(req.body);
        // aqui ira la logica de subida de imagenes
        const cursoCreado = await nuevoCurso.save();
        // Forma 2 : en un solo paso
        // const cursoCreado2 = await Curso.create(req.body);
        // Forma 3: insertar varios registros
        // Curso.insertMany(req.body) // req.body => deberia ser un array de objetos de cursos
        return res.status(201).json({
        success: true,
        content: cursoCreado,
        message: "Curso creado exitosamente",
        });
    } catch (error) {
        return res.status(500).json({
        success: false,
        content: error,
        message: "Error al crear el curso",
        });
    }
};

const listarCursos = async(req, res) => {
    const cursos = await Curso.find().catch((error) => 
    res.status(500).json({
        success: false,
        content: error,
        message: "error al devolver los cursos"
    })
    )
    return res.json({
        success: true,
        content: cursos,
        message: null
    })
}

const listarCursosPorNombre = async(req, res)=> {
    const {nombre} = req.query
    // Primera Forma
    // const resultado = await Curso.find({
    //     curso_nombre: { $regex: '.*' + nombre + "*."}
    // })
    //Segunda Forma
    const resultado = await Curso.where({
        curso_nombre: { $regex: ".*" + nombre + "*."}
    })
    // Tercera Forma
    // const resultado = await Curso.where('curso_nombre').equals({$regex: ".*" + nombre + "*."})
    // .where("curso_publicado").equals(false)


    return res.json({
        success:true,
        content: resultado,
        message: null
    })
}

const actualizarCurso = async (req, res) => {
    const { id } = req.params
    //el new sirve para indicar si queremos que nos retorne el registro ya actualizado o el registro previo a la actualizacion
    const resultado = await Curso.findOneAndUpdate({_id: id}, req.body).catch(
        (error) => 
        res.status(500).json({
                success: false,
                content: error,
                message: "Error al actualizar el curso"
            })
    )
    return res.status(201).json({
        success: true,
        content: resultado,
        message: "Curso actualizado exitosamente"
    })
}

const eliminarCurso = async (req, res) => {
    const { id } = req.params
    const resultado = await Curso.findOneAndDelete({_id: id})
    .catch((error)=> res.status(500).json({
        success: false,
        content: error,
        message: "Error al eliminar curso"
    })
    )

    return res.status(201).json({
        success: true,
        content: resultado,
        message: "Curso eliminado BN"
    })
}

module.exports = {
    crearCurso,
    listarCursos,
    listarCursosPorNombre,
    actualizarCurso,
    eliminarCurso,
};
