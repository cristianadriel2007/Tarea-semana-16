# Restaurante App - Semana 15

## Autor

**Cristian Adriel Baño Lanche**

## Descripción del proyecto

Restaurante App es una aplicación gráfica desarrollada en Python utilizando Programación Orientada a Objetos y Tkinter. El sistema permite iniciar sesión, consultar usuarios, gestionar productos y registrar ventas mediante una interfaz organizada y modular.

Durante la Semana 15 se continuó con la evolución del proyecto realizado en semanas anteriores, incorporando los conceptos fundamentales del manejo de eventos. La principal funcionalidad agregada corresponde al registro de ventas, relacionando un usuario existente con un producto registrado.

La aplicación mantiene la separación entre modelos, servicios, interfaz gráfica, archivos de datos y punto de entrada, permitiendo conservar una estructura modular y organizada.

## Objetivo de la Semana 15

El objetivo de esta semana es aplicar los fundamentos básicos del manejo de eventos en una interfaz gráfica.

Para ello, se implementó una nueva sección de ventas en la cual el usuario puede seleccionar un usuario registrado y un producto existente. Al presionar el botón **Registrar venta**, el evento se conecta mediante `command=` con un callback encargado de solicitar el registro de la operación al servicio correspondiente.

El flujo implementado es el siguiente:

```text
Usuario
   ↓
Selecciona usuario y producto
   ↓
Botón "Registrar venta"
   ↓
command=
   ↓
Callback registrar_venta()
   ↓
RestauranteServicio
   ↓
Persistencia en ventas.json
   ↓
Actualización de la tabla
   ↓
Respuesta visual al usuario
```

## Evolución del proyecto

La Semana 15 parte del proyecto desarrollado previamente y conserva las funcionalidades existentes.

### Funcionalidades conservadas

- Inicio de sesión.
- Validación de usuarios.
- Consulta de usuarios registrados.
- Gestión de productos.
- Registro de productos.
- Búsqueda de productos por código.
- Actualización de productos.
- Eliminación de productos.
- Limpieza del formulario.
- Visualización de productos mediante `Treeview`.
- Persistencia de usuarios y productos mediante archivos JSON.

### Funcionalidades incorporadas en la Semana 15

- Modelo `Venta`.
- Archivo `ventas.json`.
- Nueva sección **Ventas**.
- Selección de usuarios mediante `ttk.Combobox`.
- Selección de productos mediante `ttk.Combobox`.
- Botón **Registrar venta**.
- Uso de `command=` para asociar el botón con un callback.
- Validación de la venta mediante `RestauranteServicio`.
- Generación automática de identificadores de venta.
- Registro automático de la fecha.
- Persistencia de ventas en formato JSON.
- Visualización de ventas mediante `Treeview`.
- Actualización inmediata de la interfaz después de registrar una venta.
- Incorporación de íconos y logotipo mediante la carpeta `assets`.

## Estructura del proyecto

```text
restaurante_app/
│
├── assets/
│   ├── icons/
│   │   ├── add.png
│   │   ├── clean.png
│   │   ├── delete.png
│   │   ├── edit.png
│   │   ├── home.png
│   │   ├── logout.png
│   │   ├── productos.png
│   │   ├── sales.png
│   │   ├── search.png
│   │   └── users.png
│   │
│   └── logo/
│       ├── icono.png
│       └── logo.png
│
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
│
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
│
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
│
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
│
└── main.py
```

## Arquitectura del sistema

El proyecto utiliza una estructura modular para separar las responsabilidades de la aplicación.

### `modelos/`

Contiene las clases que representan las entidades principales del sistema:

- `Producto`: representa los productos disponibles en el restaurante.
- `Usuario`: representa los usuarios autorizados para ingresar al sistema.
- `Venta`: representa la relación entre un usuario, un producto y la fecha de la operación.

### `servicios/`

Contiene la lógica del sistema.

- `ArchivoServicio`: permite leer y escribir archivos JSON.
- `RestauranteServicio`: administra usuarios, productos y ventas, además de realizar las validaciones correspondientes.

### `ui/`

Contiene las interfaces desarrolladas con Tkinter.

- `LoginView`: controla la pantalla de inicio de sesión.
- `MainView`: contiene la navegación principal, la consulta de usuarios, la gestión de productos y el registro de ventas.

### `datos/`

Contiene los archivos utilizados para mantener la persistencia de la información:

- `usuarios.json`
- `productos.json`
- `ventas.json`

### `assets/`

Contiene los recursos visuales utilizados por la aplicación, incluyendo el logotipo del restaurante y los íconos de los botones y opciones del menú.

## Gestión de productos

La sección **Productos** conserva las funciones desarrolladas previamente.

Cada producto posee los siguientes atributos:

```text
Código
Nombre
Categoría
Precio
Stock
```

Desde la interfaz es posible:

- Registrar un producto.
- Buscar un producto por código.
- Actualizar sus datos.
- Eliminar un producto.
- Limpiar el formulario.
- Consultar los productos registrados mediante una tabla.

Los cambios realizados se almacenan en `productos.json`.

## Gestión de ventas

La sección **Ventas** permite registrar una operación relacionando un usuario existente con un producto registrado.

Para realizar una venta se utilizan dos componentes `ttk.Combobox`:

```text
Usuario  → usuario registrado
Producto → producto registrado
```

Después de seleccionar ambos elementos, el usuario presiona:

```text
Registrar venta
```

El sistema valida la información, genera automáticamente un identificador para la venta y registra la fecha de la operación.

Por ejemplo:

```text
Venta: V001
Usuario: U001 - Administrador del Restaurante
Producto: P001 - Hamburguesa Clasica
Fecha: 2026-09-23
```

Las ventas registradas se muestran inmediatamente en una tabla `Treeview`.

## Manejo de eventos con command y callbacks

Uno de los principales conceptos aplicados durante la Semana 15 es el manejo de eventos mediante `command=`.

El botón utilizado para registrar una venta se conecta con el método correspondiente de la interfaz:

```python
self.crear_boton(
    acciones,
    "Registrar venta",
    self.registrar_venta,
    "Accion.TButton",
    "add.png",
)
```

En este caso:

```text
self.registrar_venta
```

es el callback que se ejecuta cuando el usuario presiona el botón.

El callback obtiene las opciones seleccionadas en la interfaz y solicita a `RestauranteServicio` que realice el registro.

La lógica de negocio no se realiza directamente en la interfaz, sino que se delega al servicio:

```text
MainView
   ↓
RestauranteServicio
   ↓
ArchivoServicio
   ↓
ventas.json
```

De esta manera se mantiene una adecuada separación de responsabilidades.

## Persistencia de datos

La información del sistema se almacena utilizando archivos JSON.

### Productos

```text
datos/productos.json
```

### Usuarios

```text
datos/usuarios.json
```

### Ventas

```text
datos/ventas.json
```

Una venta almacenada tiene una estructura similar a la siguiente:

```json
{
    "identificador": "V001",
    "usuario_id": "U001",
    "producto_codigo": "P001",
    "fecha": "2026-09-23"
}
```

Cuando se registra una nueva venta, `RestauranteServicio` actualiza la colección de ventas y utiliza `ArchivoServicio` para guardar nuevamente la información en `ventas.json`.

Esto permite que las ventas permanezcan almacenadas incluso después de cerrar y volver a ejecutar la aplicación.

## Interfaz gráfica

La aplicación utiliza Tkinter y `ttk` para construir la interfaz gráfica.

El menú principal dispone de las siguientes secciones:

```text
Inicio
Usuarios
Productos
Ventas
Cerrar sesión
```

La sección de inicio muestra un resumen con la cantidad de:

- Usuarios registrados.
- Productos registrados.
- Ventas registradas.

Además, se incorporó la carpeta `assets` para utilizar recursos visuales propios del restaurante.

Los íconos se utilizan en:

- Inicio.
- Usuarios.
- Productos.
- Ventas.
- Registrar.
- Buscar.
- Actualizar.
- Eliminar.
- Limpiar.
- Cerrar sesión.

También se utiliza un logotipo en la pantalla de inicio de sesión y un icono para la ventana principal.

## Credenciales de prueba

El sistema dispone de los siguientes usuarios registrados:

### Administrador

```text
Usuario: administrador
Contraseña: 1234
```

### Encargado

```text
Usuario: encargado
Contraseña: 5678
```

## Ejecución del proyecto

Para ejecutar la aplicación se debe tener instalado Python.

### 1. Abrir el proyecto

Ubicarse dentro de la carpeta:

```text
restaurante_app
```

### 2. Ejecutar el archivo principal

Desde una terminal ejecutar:

```bash
python main.py
```

También se puede ejecutar `main.py` directamente desde Visual Studio Code.

### 3. Iniciar sesión

Utilizar una de las credenciales registradas.

Después del inicio de sesión se mostrará el panel principal de Restaurante App.

## Pruebas realizadas

Para comprobar el funcionamiento de la aplicación se verificaron las siguientes operaciones:

- Ejecución correcta de `main.py`.
- Inicio de sesión con usuarios registrados.
- Navegación entre las diferentes secciones.
- Consulta de usuarios.
- Visualización de productos registrados.
- Funcionamiento del CRUD de productos.
- Selección de usuario para una venta.
- Selección de producto para una venta.
- Registro de una venta mediante el botón correspondiente.
- Ejecución del callback asociado mediante `command=`.
- Validación de la operación mediante `RestauranteServicio`.
- Almacenamiento de la venta en `ventas.json`.
- Actualización automática de la tabla de ventas.
- Recuperación de las ventas después de cerrar y volver a ejecutar la aplicación.
- Visualización correcta de íconos y logotipo desde la carpeta `assets`.

## Tecnologías utilizadas

- Python
- Programación Orientada a Objetos
- Tkinter
- ttk
- JSON
- pathlib
- Visual Studio Code
- Git
- GitHub

## Conclusión

Durante la Semana 15 se continuó con la evolución de Restaurante App incorporando una nueva gestión de ventas y aplicando los fundamentos básicos del manejo de eventos en interfaces gráficas.

El uso de `command=` permite relacionar las acciones realizadas por el usuario con callbacks específicos. A su vez, la lógica y las validaciones se mantienen dentro de `RestauranteServicio`, mientras que la persistencia se realiza mediante archivos JSON.

La aplicación conserva las funcionalidades desarrolladas previamente e integra usuarios, productos, ventas y recursos visuales dentro de una arquitectura modular orientada a objetos.