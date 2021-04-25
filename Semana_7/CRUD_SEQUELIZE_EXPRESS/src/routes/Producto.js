const { Router } = require("express");
const producto_controller = require("../controllers/Producto");

const producto_router = Router();
producto_router.post("/producto", producto_controller.crearProducto);
producto_router.get(
  "/buscarProducto",
  producto_controller.devolverProductosPorNombre
);
producto_router.put("/producto/:id", producto_controller.editarProducto);
module.exports = producto_router;
