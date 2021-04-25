const { verify } = require("jsonwebtoken");
const password = process.env.JWT_SECRET || "password";
const { Usuario } = require("../config/Relaciones");

const verificarToken = (token) => {
  try {
    // sirve para verificar la autenticidad, validez y que este correctamente formateada la token, si lo esta devolvera el payload caso contrario saltará el catch
    const payload = verify(token, password, { algorithm: "RS256" });
    return payload;
  } catch (error) {
    // si la token no es valida, la password no concuerda o si ya expiro saltará el catch y nos devolvera un json con la llave message en la cual se mostrara el mensaje que sucitó el error
    // name => nombre del error
    // expiredAt => fecha en la que expiro la token
    return error.message;
  }
};

const wachiman = (req, res, next) => {
  // primero validamos si me esta dando una token
  if (req.headers.authorization) {
    // dentro de mis headers voy a buscar la llave authorization
    // ahora tengo que utilizar la token que me este dando
    // Bearer 123kalsjd.as9d8v8s9.9sd8f0s9d8f0
    const token = req.headers.authorization.split(" ")[1]; //<- ["Bearer", "123kalsjd.as9d8v8s9.9sd8f0s9d8f0"]
    const respuesta = verificarToken(token);
    // si el tipo de dato de respuesta es un objeto significa que es el payload y por ende la token fue verificada correctamente
    if (typeof respuesta === "object") {
      next();
    } else {
      return res.status(401).json({
        succes: false,
        content: respuesta,
        message: "No estas autorizado para realizar esta solicitud",
      });
    }
  } else {
    return res.status(401).json({
      succes: false,
      content: null,
      message: "Necesitas estar autorizado para realizar esta peticion",
    });
  }
};

module.exports = {
  wachiman,
};
