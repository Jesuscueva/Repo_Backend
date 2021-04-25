const { DataTypes } = require("sequelize");
const { conexion } = require("../config/Sequelize");
const bcrypt = require("bcrypt");
const { sign } = require("jsonwebtoken");
module.exports = usuario_model = () => {
  let usuario = conexion.define(
    "usuarios",
    {
      usuarioId: {
        type: DataTypes.INTEGER,
        autoIncrement: true,
        field: "usu_id",
        allowNull: false,
        primaryKey: true,
        unique: true,
      },
      usuarioEmail: {
        type: DataTypes.STRING(45),
        field: "usu_email",
        unique: true,
        // https://sequelize.org/master/manual/validations-and-constraints.html
        validate: {
          isEmail: true,
          len: [5, 45],
        },
      },
      usuarioSuperuser: {
        type: DataTypes.BOOLEAN,
        field: "usu_superuser",
        defaultValue: false,
      },
      usuarioPassword: {
        type: DataTypes.TEXT,
        field: "usu_password",
        allowNull: false,
      },
    },
    {
      timestamps: false,
      tableName: "t_usuario",
    }
  );
  /** Aqui ira la encriptacion de la contraseña */
  // al momento de usar el prototype estamos agregando nuevas funcionalidades a nuestro objecto usuario para que puedan ser usadas como el findAll(), build(), etc. estas podran ser accedidas desde cualquier lado de la app
  usuario.prototype.setearPassword = function (password) {
    // Por si se desea guardar el salt en la bd
    // bcrypt.genSaltSync(10)
    const hash = bcrypt.hashSync(password, 10);
    this.usuarioPassword = hash;
  };
  usuario.prototype.validarPassword = function (password) {
    // comparar la contraseña que se le provee con el hash almacenado y si son iguales retornara Verdadero, caso contrario retornara Falso
    return bcrypt.compareSync(password, this.usuarioPassword);
  };
  usuario.prototype.generarJWT = function () {
    // primero creo el payload (que es la parte que el front puede visualizar con normalidad en la token)
    const payload = {
      usuarioId: this.usuarioId,
      usuarioEmail: this.usuarioEmail,
    };
    // luego declaro la firma para encriptar la token
    const password = process.env.JWT_SECRET || "password";
    // una vez que ya tenemos definido el payload y la contraseña, procedemos a la creacion de la token
    return sign(payload, password, { expiresIn: "1h" }, { algorithm: "RS256" });
  };
  return usuario;
};
