const { DataTypes } = require("sequelize");
const { conexion } = require("../config/Sequelize");

module.exports = detalle_model = () => {
  return conexion.define(
    "detalles",
    {
      detalleId: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true,
        field: "det_id",
        allowNull: false,
      },
      detalleCantidad: {
        type: DataTypes.STRING(45),
        field: "det_cantidad",
        allowNull: false,
      },
      detallePrecioUnitario: {
        type: DataTypes.FLOAT(5, 2),
        field: "det_precunit",
        allowNull: false,
      },
    },
    {
      timestamps: false,
      tableName: "t_det_nota",
    }
  );
};
