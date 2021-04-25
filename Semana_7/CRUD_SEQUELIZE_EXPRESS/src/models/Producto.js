const { DataTypes } = require("sequelize");
const { conexion } = require("../config/Sequelize");

module.exports = producto_model = () => {
  return conexion.define(
    "productos",
    {
      productoId: {
        primaryKey: true,
        autoIncrement: true,
        type: DataTypes.INTEGER,
        field: "prod_id",
        unique: true,
        allowNull: false,
      },
      productoNombre: {
        type: DataTypes.STRING(45),
        allowNull: false,
        field: "prod_nombre",
        validate: {
          len: [5, 45],
        },
      },
      productoPrecio: {
        type: DataTypes.FLOAT(5, 2),
        allowNull: false,
        field: "prod_precio",
      },
      productoCantidad: {
        type: DataTypes.INTEGER,
        allowNull: false,
        field: "prod_cantidad",
        validate: {
          min: 0,
        },
      },
      productoFechaVencimiento: {
        // DATEONLY => solamente da YYYY/MM/DD y DATE => YYYY/MM/DD HH:MM:SS
        type: DataTypes.DATEONLY,
        allowNull: false,
        field: "prod_fecvec",
        validate: {
          isAfter: "2022-01-01",
        },
      },
      productoEstado: {
        type: DataTypes.BOOLEAN,
        allowNull: false,
        field: "prod_estado",
        defaultValue: true,
      },
    },
    {
      tableName: "t_producto",
      timestamps: false,
    }
  );
};
