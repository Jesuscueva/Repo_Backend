const { Usuario } = require("../config/Relaciones");
// Registro
const registro = async (req, res) => {
  // vamos a utilizar la creacion en dos pasos
  // 1. contruimos el objeto usuario
  const { password } = req.body;
  const nuevoUsuario = Usuario.build(req.body);
  nuevoUsuario.setearPassword(password);
  // 2. una vez realizadas las modificaciones a nuestro objeto, procedemos a guardarlo en la bd
  await nuevoUsuario.save();
  return res.status(201).json({
    success: true,
    content: nuevoUsuario,
    message: "Usuario creado exitosamente",
  });
};
// Login
const login = async (req, res) => {
  const { email, password } = req.body;
  // 1. validar si el correo existe
  const usuario = await Usuario.findOne({ where: { usuarioEmail: email } });
  if (usuario) {
    // 2. validar si la contraseña existe
    const resultado = usuario.validarPassword(password);
    console.log(resultado);
    if (resultado) {
      // devolvemos la token
      const token = usuario.generarJWT();
      return res.json({
        success: true,
        content: token,
        message: "Bievenido!!",
      });
    } else {
      return res.status(404).json({
        success: false,
        content: null,
        message: "Usuario o contraseña incorrectos",
      });
    }
  } else {
    return res.status(404).json({
      success: false,
      content: null,
      message: "Usuario o contraseña incorrectos",
    });
  }
};

module.exports = {
  registro,
  login,
};
