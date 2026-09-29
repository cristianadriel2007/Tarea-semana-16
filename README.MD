# Restaurante Cris - Semana 16

## Autor

**Cristian Adriel Baño Lanche**

## Descripción del proyecto

Restaurante Cris es una aplicación de escritorio desarrollada en Python mediante Tkinter y Programación Orientada a Objetos. El sistema permite gestionar productos, usuarios y ventas utilizando una arquitectura modular y archivos JSON para almacenar la información.

Durante la Semana 16 se continuó con la evolución del proyecto desarrollado en semanas anteriores. En esta etapa se amplió principalmente la gestión de usuarios mediante el manejo de eventos en Tkinter, incorporando roles, operaciones CRUD, selección automática desde una tabla y atajos de teclado.

El proyecto conserva las funciones desarrolladas anteriormente, como el inicio de sesión, la gestión de productos, el registro de ventas, la navegación entre secciones y la persistencia de datos.

## Objetivo de la Semana 16

El objetivo principal de esta semana fue aplicar el manejo de eventos dentro de la sección de usuarios.

Se implementaron diferentes mecanismos de interacción utilizando `bind()`, eventos virtuales de Tkinter, callbacks y botones asociados mediante `command=`.

La interfaz permite responder a acciones realizadas por el usuario y mantiene separadas las responsabilidades entre la interfaz gráfica, los modelos, los servicios y la persistencia de datos.

## Evolución del proyecto

La Semana 16 parte directamente de la aplicación desarrollada en la Semana 15.

Se conservaron las siguientes funcionalidades:

- Inicio de sesión.
- Navegación mediante menú lateral.
- Gestión de productos.
- Registro y consulta de ventas.
- Persistencia mediante archivos JSON.
- Uso de una sola ventana principal.
- Uso de recursos gráficos almacenados en `assets/`.
- Arquitectura modular basada en modelos, servicios e interfaz gráfica.

Como nueva funcionalidad se incorporó una gestión completa de usuarios mediante eventos.

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
├── main.py
└── README.md
```

## Arquitectura modular

El proyecto mantiene una separación clara de responsabilidades.

### Modelos

La carpeta `modelos/` contiene las clases que representan las principales entidades utilizadas por el sistema:

- `Producto`
- `Usuario`
- `Venta`

Cada clase contiene sus respectivos atributos, propiedades y validaciones.

### Servicios

La carpeta `servicios/` contiene la lógica de funcionamiento del sistema.

`ArchivoServicio` se encarga de leer y escribir información en los archivos JSON.

`RestauranteServicio` administra las operaciones relacionadas con productos, usuarios y ventas. También contiene las validaciones necesarias y se encarga de solicitar la persistencia de los cambios.

### Interfaz gráfica

La carpeta `ui/` contiene las vistas desarrolladas mediante Tkinter.

`LoginView` permite autenticar al usuario.

`MainView` contiene la navegación principal y las secciones de Inicio, Usuarios, Productos y Ventas.

La interfaz gráfica obtiene los datos ingresados por el usuario y delega las operaciones a `RestauranteServicio`.

## Gestión de usuarios

Durante la Semana 16 se amplió la sección de usuarios para permitir las siguientes operaciones:

- Registrar usuarios.
- Consultar usuarios.
- Actualizar usuarios.
- Eliminar usuarios.
- Mostrar los usuarios almacenados en un `Treeview`.
- Seleccionar usuarios directamente desde la tabla.
- Asignar roles mediante un `Combobox`.
- Guardar los cambios en `usuarios.json`.

La tabla de usuarios muestra únicamente:

- Identificador.
- Nombre.
- Usuario.
- Rol.

La contraseña no se presenta directamente en el `Treeview`.

## Roles de usuario

El modelo `Usuario` incorpora el atributo `rol`.

Los roles utilizados son:

- **Administrador**
- **Empleado**
- **Cliente**

El usuario con rol Administrador puede acceder a la sección administrativa de Usuarios.

Los usuarios con rol Empleado o Cliente no disponen de la misma opción de administración de usuarios.

Desde la pantalla de gestión únicamente se pueden registrar usuarios con roles Empleado o Cliente.

Además, el usuario Administrador que se encuentra actualmente autenticado no puede eliminar accidentalmente su propia cuenta ni cambiar su rol administrativo desde esta pantalla.

## Manejo de eventos

Uno de los principales objetivos de la Semana 16 fue implementar diferentes eventos dentro de la gestión de usuarios.

### Evento `<<TreeviewSelect>>`

Este evento se activa cuando el administrador selecciona un registro dentro de la tabla de usuarios.

```python
self.tabla_usuarios.bind(
    "<<TreeviewSelect>>",
    self.al_seleccionar_usuario,
)
```

El callback obtiene el identificador de la fila seleccionada y utiliza `RestauranteServicio` para consultar el objeto correspondiente.

Después, los datos del usuario se cargan automáticamente en el formulario.

### Evento `<Return>`

La tecla Enter funciona como un atajo para registrar un usuario.

```python
widget.bind(
    "<Return>",
    self.al_presionar_enter,
)
```

El callback reutiliza el método existente:

```python
def al_presionar_enter(self, event):
    self.registrar_usuario()
```

De esta forma no se repite la lógica del registro.

### Evento `<Escape>`

La tecla Escape permite cancelar la operación actual y limpiar el formulario.

```python
widget.bind(
    "<Escape>",
    self.al_presionar_escape,
)
```

El callback reutiliza el método encargado de limpiar el formulario:

```python
def al_presionar_escape(self, event):
    self.limpiar_formulario_usuario()
```

También se elimina cualquier selección activa del `Treeview`.

### Evento `<<ComboboxSelected>>`

El `Combobox` utilizado para seleccionar el rol responde al evento:

```python
self.usuario_rol_combo.bind(
    "<<ComboboxSelected>>",
    self.al_seleccionar_rol,
)
```

Al seleccionar un rol, la interfaz actualiza el texto informativo que muestra el rol actualmente elegido.

## Uso de `bind()`

El método `bind()` se utiliza para asociar un evento específico de un componente con una función callback.

El flujo utilizado en la aplicación es:

```text
Interacción del usuario
        ↓
Evento
        ↓
bind()
        ↓
callback(event)
        ↓
RestauranteServicio
        ↓
Persistencia
        ↓
Actualización de la interfaz
```

Esto permite que la aplicación responda a diferentes acciones del usuario sin concentrar toda la lógica dentro de la interfaz gráfica.

## Uso de `command=`

Los botones principales continúan utilizando `command=`.

Por ejemplo:

```python
command=self.registrar_usuario
```

Los botones disponibles en la sección Usuarios son:

- Registrar.
- Actualizar.
- Eliminar.
- Limpiar.

`command=` se utiliza para acciones directas realizadas mediante botones, mientras que `bind()` permite responder a eventos específicos como teclas, selección de filas o cambios en un `Combobox`.

## Callbacks

Los callbacks son métodos que se ejecutan cuando ocurre una determinada interacción dentro de la aplicación.

Entre los callbacks utilizados durante la Semana 16 se encuentran:

```python
al_seleccionar_usuario()
al_presionar_enter()
al_presionar_escape()
al_seleccionar_rol()
```

Estos métodos coordinan la respuesta de la interfaz y reutilizan las funciones existentes.

Las reglas de negocio y la persistencia continúan siendo responsabilidad de `RestauranteServicio`.

## Persistencia de usuarios

La información se almacena en:

```text
datos/usuarios.json
```

Cada usuario contiene los siguientes datos:

```json
{
    "identificador": "U002",
    "nombre": "Encargado de Atencion",
    "usuario": "encargado",
    "contrasena": "5678",
    "rol": "Empleado"
}
```

Cuando se registra, actualiza o elimina un usuario, `RestauranteServicio` actualiza la colección y posteriormente utiliza `ArchivoServicio` para guardar los cambios.

Al cerrar y volver a ejecutar la aplicación, los usuarios son recuperados desde `usuarios.json`.

## Gestión de productos

La sección Productos conserva las funcionalidades desarrolladas anteriormente.

Permite:

- Registrar productos.
- Buscar productos por código.
- Actualizar productos.
- Eliminar productos.
- Limpiar el formulario.
- Mostrar los productos registrados mediante un `Treeview`.

Los productos se almacenan en:

```text
datos/productos.json
```

## Gestión de ventas

La sección Ventas conserva las funcionalidades desarrolladas durante la Semana 15.

Permite seleccionar un usuario y un producto mediante componentes `Combobox` y registrar una venta.

Las ventas almacenan:

- Identificador de la venta.
- Identificador del usuario.
- Código del producto.
- Fecha.

La información se guarda en:

```text
datos/ventas.json
```

Las ventas registradas se muestran mediante un `Treeview`.

## Recursos visuales

El proyecto utiliza la carpeta:

```text
assets/
```

para almacenar los recursos gráficos utilizados por la aplicación.

Dentro de esta carpeta se encuentran los íconos utilizados en botones y navegación, además del logotipo e icono de Restaurante Cris.

Estos recursos permiten mantener una interfaz visualmente consistente entre las diferentes secciones.

## Credenciales iniciales

### Administrador

```text
Usuario: administrador
Contraseña: 1234
Rol: Administrador
```

### Empleado

```text
Usuario: encargado
Contraseña: 5678
Rol: Empleado
```

## Ejecución del proyecto

Para ejecutar la aplicación se debe tener instalado Python.

Desde una terminal ubicada dentro de la carpeta `restaurante_app`, ejecutar:

```bash
python main.py
```

También puede utilizarse:

```bash
python3 main.py
```

dependiendo de la configuración del sistema operativo.

## Flujo de ejecución

```text
main.py
   ↓
ArchivoServicio
   ↓
RestauranteServicio
   ↓
LoginView
   ↓
Validación de usuario
   ↓
MainView
   ↓
Inicio / Usuarios / Productos / Ventas
```

Cuando el usuario autenticado posee el rol Administrador, puede ingresar a la sección Usuarios y realizar las operaciones administrativas correspondientes.

## Pruebas realizadas

Se verificó el funcionamiento de las siguientes operaciones:

- Inicio correcto de la aplicación.
- Inicio de sesión mediante las credenciales almacenadas.
- Acceso a la gestión de usuarios mediante el rol Administrador.
- Restricción de la gestión administrativa para otros roles.
- Registro de usuarios.
- Actualización de usuarios.
- Eliminación de usuarios con confirmación previa.
- Protección de la cuenta administrativa actualmente autenticada.
- Selección automática de usuarios mediante `<<TreeviewSelect>>`.
- Registro mediante la tecla Enter.
- Limpieza del formulario mediante la tecla Escape.
- Respuesta del selector de roles mediante `<<ComboboxSelected>>`.
- Actualización automática del `Treeview`.
- Persistencia de los usuarios en `usuarios.json`.
- Recuperación de los usuarios después de cerrar y volver a ejecutar la aplicación.
- Funcionamiento de Productos.
- Funcionamiento de Ventas.
- Funcionamiento de los recursos visuales almacenados en `assets/`.

## Tecnologías utilizadas

- Python.
- Tkinter.
- ttk.
- Programación Orientada a Objetos.
- JSON.
- pathlib.
- Git.
- GitHub.

## Conclusión

Durante la Semana 16 se amplió Restaurante Cris incorporando el manejo de eventos dentro de la gestión de usuarios.

El uso de `bind()`, `command=`, callbacks, `Treeview` y `Combobox` permitió crear una interfaz más interactiva sin modificar la arquitectura modular del proyecto.

La aplicación mantiene separadas las responsabilidades entre modelos, servicios, interfaz gráfica y persistencia, al mismo tiempo que conserva las funcionalidades implementadas en semanas anteriores.

Con esta evolución, el sistema permite administrar usuarios mediante roles y diferentes formas de interacción, manteniendo la información almacenada de manera persistente en archivos JSON.