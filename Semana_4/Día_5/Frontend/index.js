const listarProductos = document.getElementById("getProductos");
const addProducto = document.getElementById("addProductos");
const productos = document.getElementById("productos");
listarProductos.onclick = (e) => {
  devolverProductos()
    .then((responseGet) => {
      const [dataGet, statusGet] = responseGet;
      if (statusGet === 200) {
        productos.innerHTML = `
                            <tr>
                                <th>Id</th>
                                <th>Nombre</th>
                                <th>Precio</th>
                                <th>Cantidad</th>
                                <th>Accion</th>
                            </tr>
    `;

        const { content } = dataGet;
        content.forEach((row, index) => {
          console.log(row);
          const fila = document.createElement("tr");
          const colId = document.createElement("td");
          const colNombre = document.createElement("td");
          const colPrecio = document.createElement("td");
          const colCantidad = document.createElement("td");
          const colAccion = document.createElement("td");
          const editar = document.createElement("button");
          const eliminar = document.createElement("button");
          colId.textContent = index;
          colNombre.textContent = row.producto_nombre;
          colPrecio.textContent = row.producto_precio;
          colCantidad.textContent = row.producto_cantidad;
          editar.innerText = "Editar";
          editar.className = "warning btn-tabla";
          editar.id = index;
          eliminar.innerText = "Eliminar";
          eliminar.id = index;
          eliminar.className = "danger btn-tabla"
          editar.onclick = (e) => {
            const { id } = e.currentTarget;
            Swal.mixin({
              input: "text",
              showCancelButton: true,
              confirmButtonText: "Next &rarr;",
              progressSteps: ["1", "2", "3"],
            })
              .queue([
                {
                  title: "Ingrese nombre del producto",
                  text: "Solo texto",
                },
                {
                  title: "Ingrese el precio del producto",
                  input: "number",
                },
                {
                  title: "Ingrese la cantidad del producto",
                  input: "number",
                },
              ])
              .then((result) => {
                console.log(result);
                if (result.value) {
                  editarProducto(id, {
                    producto_nombre: result.value[0],
                    producto_precio: result.value[1],
                    producto_cantidad: result.value[2],
                  })
                    .then((responseUpdate) => {
                      const [dataUpdate, statusUpdate] = responseUpdate;
                      colNombre.textContent =
                        dataUpdate.content.producto_nombre;
                      colPrecio.textContent =
                        dataUpdate.content.producto_precio;
                      colCantidad.textContent =
                        dataUpdate.content.producto_cantidad;
                    })
                    .catch((errorUpdate) => {
                      console.error(errorUpdate);
                    });
                }
              });
          };
          eliminar.onclick = (e) => {
            const { id } = e.currentTarget;
            eliminarProducto(id)
              .then((responseDelete) => {
                const [dataDelete, statusDelete] = responseDelete;
                console.log(dataDelete);
                Swal.fire({
                  icon: "info",
                  title: dataDelete.message,
                  timer: 2000,
                  timerProgressBar: true,
                  showConfirmButton: false,
                });
                // alert(dataDelete.message);
              })
              .catch((errorUpdate) => {
                console.error(errorUpdate);
              });
            fila.remove();
          };
          colAccion.appendChild(editar);
          colAccion.appendChild(eliminar);

          fila.appendChild(colId);
          fila.appendChild(colNombre);
          fila.appendChild(colPrecio);
          fila.appendChild(colCantidad);
          fila.appendChild(colAccion);
          productos.appendChild(fila);
        });
      } else {
        alert("Algo ocurrio y no se pudo devolver la info");
      }
    })
    .catch((error) => {
      console.error(error);
    });
};

addProducto.onclick = () => {
  Swal.mixin({
    input: "text",
    showCancelButton: true,
    confirmButtonText: "Next &rarr;",
    progressSteps: ["1", "2", "3"],
  })
    .queue([
      {
        title: "Ingrese nombre del producto",
        text: "Solo texto",
      },
      {
        title: "Ingrese el precio del producto",
        input: "text",
      },
      {
        title: "Ingrese la cantidad del producto",
        input: "number",
      },
    ])
    .then((result) => {
      console.log(result);
      if (result.value) {
        ingresarProducto({
          producto_nombre: result.value[0],
          producto_precio: result.value[1],
          producto_cantidad: result.value[2],
        }).then((responseCreate) => {
          const [dataPost, statusPost] = responseCreate;
          console.log(responseCreate);
          Swal.fire({
            title: dataPost.message,
            timer: 2000,
            timerProgressBar: true,
            showConfirmButton: false,
            icon: "success",
          });
          listarProductos.click();
        });
      }
    });
};
