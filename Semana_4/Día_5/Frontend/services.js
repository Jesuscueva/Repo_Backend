const URL_BACKEND = "http://127.0.0.1:5001/producto";

const devolverProductos = async () => {
  const result = await fetch(URL_BACKEND, {
    method: "GET",
  });
  const data = await result.json();
  const status = result.status;
  return [data, status];
};

const ingresarProducto = async (objProducto) => {
  const result = await fetch(URL_BACKEND, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(objProducto),
  });
  const data = await result.json();
  const status = result.status;
  return [data, status];
};

const editarProducto = async (id, objProducto) => {
  const result = await fetch(`${URL_BACKEND}/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(objProducto),
  });
  const data = await result.json();
  const status = result.status;
  return [data, status];
};

const eliminarProducto = async (id) => {
  const result = await fetch(`${URL_BACKEND}/${id}`, {
    method: "DELETE",
  });
  const data = await result.json();
  const status = result.status;
  return [data, status];
};
