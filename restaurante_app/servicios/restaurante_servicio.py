from datetime import date

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
    def __init__(self, archivo_servicio):
        self.archivo_servicio = archivo_servicio
        self.usuarios = []
        self.productos = []
        self.ventas = []
        self.cargar_datos()

    def cargar_datos(self):
        # Carga los datos persistidos y los convierte en objetos.
        usuarios_json = self.archivo_servicio.leer_json(
            "usuarios.json"
        )
        productos_json = self.archivo_servicio.leer_json(
            "productos.json"
        )
        ventas_json = self.archivo_servicio.leer_json(
            "ventas.json"
        )

        self.usuarios = [
            Usuario(
                datos.get("identificador", ""),
                datos.get("nombre", ""),
                datos.get("usuario", ""),
                datos.get("contrasena", ""),
            )
            for datos in usuarios_json
        ]

        self.productos = [
            Producto(
                datos.get("codigo", ""),
                datos.get("nombre", ""),
                datos.get("categoria", ""),
                datos.get("precio", 0),
                datos.get("stock", 0),
            )
            for datos in productos_json
        ]

        # Semana 15: carga las ventas almacenadas.
        self.ventas = [
            Venta(
                datos.get("identificador", ""),
                datos.get("usuario_id", ""),
                datos.get("producto_codigo", ""),
                datos.get("fecha", ""),
            )
            for datos in ventas_json
        ]

    def validar_acceso(self, usuario, contrasena):
        # Verifica las credenciales con los usuarios cargados.
        for usuario_registrado in self.usuarios:
            if (
                usuario_registrado.usuario == usuario
                and usuario_registrado.contrasena == contrasena
            ):
                return usuario_registrado

        return None

    def cantidad_usuarios(self):
        return len(self.usuarios)

    def cantidad_productos(self):
        return len(self.productos)

    def cantidad_ventas(self):
        return len(self.ventas)

    def listar_usuarios(self):
        return self.usuarios

    def listar_productos(self):
        return self.productos

    def listar_ventas(self):
        return self.ventas

    def guardar_productos(self):
        # Convierte los productos en datos y los guarda en JSON.
        datos = [
            {
                "codigo": producto.codigo,
                "nombre": producto.nombre,
                "categoria": producto.categoria,
                "precio": producto.precio,
                "stock": producto.stock,
            }
            for producto in self.productos
        ]

        self.archivo_servicio.escribir_json(
            "productos.json",
            datos,
        )

    def buscar_producto_por_codigo(self, codigo):
        codigo = codigo.strip()

        for producto in self.productos:
            if producto.codigo == codigo:
                return producto

        return None

    def buscar_usuario_por_identificador(self, identificador):
        identificador = identificador.strip()

        for usuario in self.usuarios:
            if usuario.identificador == identificador:
                return usuario

        return None

    def generar_identificador_venta(self):
        siguiente = len(self.ventas) + 1

        return f"V{siguiente:03d}"

    def registrar_producto(
        self,
        codigo,
        nombre,
        categoria,
        precio,
        stock,
    ):
        nuevo_producto = Producto(
            codigo,
            nombre,
            categoria,
            precio,
            stock,
        )

        if (
            self.buscar_producto_por_codigo(
                nuevo_producto.codigo
            )
            is not None
        ):
            raise ValueError(
                "Ya existe un producto con ese codigo."
            )

        self.productos.append(nuevo_producto)
        self.guardar_productos()

        return nuevo_producto

    def actualizar_producto(
        self,
        codigo,
        nombre,
        categoria,
        precio,
        stock,
    ):
        producto_actual = self.buscar_producto_por_codigo(
            codigo
        )

        if producto_actual is None:
            raise ValueError(
                "No existe un producto con ese codigo."
            )

        # Se crea un producto temporal para validar los nuevos datos.
        datos_validados = Producto(
            codigo,
            nombre,
            categoria,
            precio,
            stock,
        )

        producto_actual.nombre = datos_validados.nombre
        producto_actual.categoria = datos_validados.categoria
        producto_actual.precio = datos_validados.precio
        producto_actual.stock = datos_validados.stock

        self.guardar_productos()

        return producto_actual

    def eliminar_producto(self, codigo):
        producto_actual = self.buscar_producto_por_codigo(
            codigo
        )

        if producto_actual is None:
            raise ValueError(
                "No existe un producto con ese codigo."
            )

        self.productos.remove(producto_actual)
        self.guardar_productos()

        return producto_actual

    # ---------------------------------------------------------
    # Ventas - Semana 15
    # ---------------------------------------------------------

    def guardar_ventas(self):
        # Convierte las ventas en datos y las guarda en JSON.
        datos = [
            {
                "identificador": venta.identificador,
                "usuario_id": venta.usuario_id,
                "producto_codigo": venta.producto_codigo,
                "fecha": venta.fecha,
            }
            for venta in self.ventas
        ]

        self.archivo_servicio.escribir_json(
            "ventas.json",
            datos,
        )

    def registrar_venta(
        self,
        usuario_id,
        producto_codigo,
    ):
        usuario_id = usuario_id.strip()
        producto_codigo = producto_codigo.strip()

        if not usuario_id:
            raise ValueError(
                "Debe seleccionar un usuario."
            )

        if not producto_codigo:
            raise ValueError(
                "Debe seleccionar un producto."
            )

        if (
            self.buscar_usuario_por_identificador(
                usuario_id
            )
            is None
        ):
            raise ValueError(
                "El usuario seleccionado no existe."
            )

        if (
            self.buscar_producto_por_codigo(
                producto_codigo
            )
            is None
        ):
            raise ValueError(
                "El producto seleccionado no existe."
            )

        nueva_venta = Venta(
            self.generar_identificador_venta(),
            usuario_id,
            producto_codigo,
            date.today().isoformat(),
        )

        self.ventas.append(nueva_venta)
        self.guardar_ventas()

        return nueva_venta