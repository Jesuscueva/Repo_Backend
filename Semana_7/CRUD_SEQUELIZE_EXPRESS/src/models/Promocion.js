const { DataTypes } = require("sequelize");
const { conexion } = require("../config/Sequelize");

module.exports = promocion_model = () => {
  return conexion.define(
    "promociones",
    {
      promocionId: {
        type: DataTypes.INTEGER,
        field: "prom_id",
        primaryKey: true,
        autoIncrement: true,
        allowNull: false,
      },
      promocionFechaDesde: {
        type: DataTypes.DATE,
        field: "prom_fecdesde",
        allowNull: false,
      },
      promocionFechaHasta: {
        type: DataTypes.DATE,
        field: "prom_fechasta",
        allowNull: false,
      },
      promocionDescuento: {
        type: DataTypes.FLOAT(5, 2),
        field: "prom_descuento",
        allowNull: false,
      },
      promocionEstado: {
        type: DataTypes.BOOLEAN,
        field: "prom_estado",
        allowNull: false,
      },
    },
    {
      tableName: "t_promocion",
      timestamps: false,
    }
  );
};
