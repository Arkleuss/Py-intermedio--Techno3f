Integrantes:
Leandro Figliolia (arkleuss@gmail.com)


ejecutar desde el archivo main.py
el programa tiene 3 modulos principales:

1.Modulo inventario
Muestra todos los productos de la base de datos y permite buscar desde el desplegable ya sea abriendo o tipeando para filtrar por nombre.
Una vez seleccionado en el desplegable el producto se visualizan los datos del mismo 
Dentro del modulo inventario se puede agrega, editar o eliminar productos.
    -Agregar: pide datos para crear nuevo producto, en caso de tener una imagen del producto se puede cargar desde cualquier carpeta de la pc, 
    en caso de no tener imagen se guarda con una imagen default.
    -Editar y Eliminar: el producto a modificar es el que esta seleccionado en el desplegable.

2.Modulo Clientes
Muestra todos los clientes de la base de datos.
    -Crear: Requiere que esten llenos todos los campos de la izquierda
    -Editar: El cliente a modificar es el que esta seleccionado desde la lista completa.

3.Modulo Ventas.
Para realizar una venta el procedimiento es el siguiente:
    -Seleccionar el cliente, esto va a completar los datos del Nivel y el Descuento.
    -Seleccionar el producto, se puede filtrar tipeando, una vez seleccionado muestra los datos de stock, 
    -Tipear la cantidad del producto seleccionado y presionar el boton Agregar, en la vista inferior muestra todos los datos del producto.
    -El boton Eliminar Producto quita el producto seleccionado en la lista inferior
    -El boton Editar Producto modifica la cantidad del producto seleccionado en la lista inferior
    -El boton Limpiar lista, vacia todos los productos 
    En la parte inferior se actualiza el Subtotal de la venta, el descuento segun el nivel del cliente, y el total a pagar.
    -El boton Finalizar permite finalizar la venta y se guarda la factura en la base de datos.
    