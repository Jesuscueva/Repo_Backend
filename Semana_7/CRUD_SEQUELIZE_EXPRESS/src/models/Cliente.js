const { DataTypes } = require("sequelize");
const { conexion } = require("../config/Sequelize");

module.exports = cliente_model = () => {
  return conexion.define(
    "clientes",
    {
      clienteDni: {
        type: DataTypes.STRING(9),
        primaryKey: true,
        allowNull: false,
        unique: true,
        field: "cli_dni",
      },
      clienteNombre: {
        type: DataTypes.STRING(45),
        allowNull: true,
        field: "cli_nombre",
      },
      clienteDireccion: {
        type: DataTypes.STRING(45),
        allowNull: true,
        field: "cli_direccion",
      },
      clienteFono: {
        type: DataTypes.STRING(10),
        allowNull: true,
        field: "cli_fono",
      },
    },
    {
      tableName: "t_cliente",
    }
  );
};
