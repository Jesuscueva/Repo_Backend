const { DataTypes } = require("sequelize");
const { conexion } = require("../config/Sequelize");

module.exports = cabecera_model = () => {
  return conexion.define(
    "cabeceras",
    {
      cabeceraId: {
        type: DataTypes.INTEGER,
        allowNull: false,
        field: "cab_id",
        primaryKey: true,
        unique: true,
        autoIncrement: true,
      },
      cabeceraFecha: {
        type: DataTypes.DATEONLY,
        allowNull: false,
        field: "cab_fecha",
        defaultValue: DataTypes.NOW, // agarra la fecha actual del servidor y la pone como valor por defecto
      },
      cabeceraSerie: {
        type: DataTypes.STRING(4),
        allowNull: false,
        field: "cab_serie",
      },
      cabeceraTotal: {
        type: DataTypes.FLOAT(5, 2),
        allowNull: false,
        field: "cab_total",
      },
      cabeceraDescuento: {
        type: DataTypes.FLOAT(5, 2),
        allowNull: false,
        field: "cab_dscto",
      },
      cabeceraSubTotal: {
        type: DataTypes.FLOAT(5, 2),
        allowNull: false,
        field: "cab_subtotal",
      },
    },
    {
      timestamps: false,
      tableName: "t_cab_nota",
    }
  );
};
