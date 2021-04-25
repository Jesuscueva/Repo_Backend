const { verificar, verify } = require("jsonwebtoken")

const verificarToken = (token) => {
    try {
        const payload = verify(token, process.env.JWT_SECRET, {
            algorithm: "RS256"
        })
        return payload
    } catch (error) {
        return error.message
    }
}

const wachiman = (req, res, next) => {
    if(!req.headers.authorization){
        return res.status(401).json({
            success: false,
            content: null,
            message: "Necesitas estar autenticado para realizar esta peticion"
        })
    }

    const token = req.headers.authorization.split(' ')[1]
    const respuesta = verificarToken(token) // ["Bearer", "2414321423232.23123123.123123123"]
    if( typeof respuesta === "object"){
        req.usuario = respuesta
        next()
    }else{
        return res.status(401).json({
            success: false,
            content: respuesta,
            message: "No estas autorizado para realizar esta solicitud"
        })
    }
}

module.exports = {
    wachiman,
}
