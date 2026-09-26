import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk


class MainView(tk.Frame):
    def __init__(
        self,
        master,
        restaurante_servicio,
        usuario_actual,
        al_cerrar_sesion,
    ):
        super().__init__(master, bg="#f7fafc")

        self.restaurante_servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.al_cerrar_sesion = al_cerrar_sesion

        self.contenido = None
        self.etiqueta_estado = None

        self.botones_menu = {}
        self.iconos = {}

        # Productos
        self.producto_codigo_entry = None
        self.producto_nombre_entry = None
        self.producto_categoria_entry = None
        self.producto_precio_entry = None
        self.producto_stock_entry = None
        self.tabla_productos = None

        # Usuarios
        self.tabla_usuarios = None

        # Ventas
        self.usuario_venta_combo = None
        self.producto_venta_combo = None
        self.tabla_ventas = None

        self.opciones_usuarios_venta = {}
        self.opciones_productos_venta = {}

        self.definir_estilos()
        self.construir_interfaz()

    # ---------------------------------------------------------
    # Configuracion general
    # ---------------------------------------------------------

    def definir_estilos(self):
        self.color_fondo = "#f7fafc"
        self.color_panel = "#ffffff"
        self.color_encabezado = "#1f2a44"
        self.color_texto = "#243447"
        self.color_secundario = "#dbeafe"
        self.color_resaltado = "#2563eb"

        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "MenuApp.TButton",
            background="#334155",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(10, 8),
            borderwidth=0,
            anchor="w",
        )

        estilo.map(
            "MenuApp.TButton",
            background=[("active", "#475569")],
        )

        estilo.configure(
            "MenuActivo.TButton",
            background=self.color_resaltado,
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(10, 8),
            borderwidth=0,
            anchor="w",
        )

        estilo.map(
            "MenuActivo.TButton",
            background=[("active", "#1d4ed8")],
        )

        estilo.configure(
            "Secundario.TButton",
            background="#1f2a44",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0,
        )

        estilo.map(
            "Secundario.TButton",
            background=[("active", "#334155")],
        )

        estilo.configure(
            "Accion.TButton",
            background=self.color_resaltado,
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0,
        )

        estilo.map(
            "Accion.TButton",
            background=[("active", "#1d4ed8")],
        )

        estilo.configure(
            "Eliminar.TButton",
            background="#e11d48",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0,
        )

        estilo.map(
            "Eliminar.TButton",
            background=[("active", "#be123c")],
        )

        estilo.configure(
            "Treeview.Heading",
            background=self.color_secundario,
            foreground=self.color_encabezado,
            font=("Arial", 10, "bold"),
        )

    # ---------------------------------------------------------
    # Carga de iconos
    # ---------------------------------------------------------

    def cargar_icono(self, nombre_archivo):
        ruta_base = Path(__file__).resolve().parent.parent

        ruta_icono = (
            ruta_base
            / "assets"
            / "icons"
            / nombre_archivo
        )

        if not ruta_icono.exists():
            return None

        try:
            icono_original = tk.PhotoImage(
                file=str(ruta_icono)
            )

            ancho = icono_original.width()
            alto = icono_original.height()

            dimension_mayor = max(
                ancho,
                alto,
            )

            # Reduce automaticamente los iconos grandes.
            if dimension_mayor > 32:
                factor = (
                    dimension_mayor + 31
                ) // 32

                icono = icono_original.subsample(
                    factor,
                    factor,
                )
            else:
                icono = icono_original

            # Se conserva la referencia para evitar
            # que Tkinter elimine la imagen.
            self.iconos[nombre_archivo] = icono

            return icono

        except tk.TclError:
            return None

    def crear_boton(
        self,
        contenedor,
        texto,
        comando,
        estilo,
        icono=None,
    ):
        imagen = (
            self.cargar_icono(icono)
            if icono
            else None
        )

        if imagen is not None:
            boton = ttk.Button(
                contenedor,
                text=texto,
                command=comando,
                style=estilo,
                image=imagen,
                compound="left",
            )
        else:
            boton = ttk.Button(
                contenedor,
                text=texto,
                command=comando,
                style=estilo,
            )

        return boton

    # ---------------------------------------------------------
    # Menu principal
    # ---------------------------------------------------------

    def construir_interfaz(self):
        frame_sidebar = tk.Frame(
            self,
            bg=self.color_encabezado,
            width=220,
            padx=16,
            pady=18,
        )

        frame_sidebar.pack(
            side="left",
            fill="y",
        )

        frame_sidebar.pack_propagate(False)

        tk.Label(
            frame_sidebar,
            text="RESTAURANTE",
            bg=self.color_encabezado,
            fg="#ffffff",
            font=("Arial", 17, "bold"),
        ).pack(
            anchor="w",
            pady=(0, 8),
        )

        tk.Label(
            frame_sidebar,
            text=self.usuario_actual.nombre,
            bg=self.color_encabezado,
            fg="#dbeafe",
            font=("Arial", 10),
            wraplength=180,
            justify="left",
        ).pack(
            anchor="w",
            pady=(0, 24),
        )

        self.crear_boton_menu(
            frame_sidebar,
            "Inicio",
            self.mostrar_inicio,
            "home.png",
        )

        self.crear_boton_menu(
            frame_sidebar,
            "Usuarios",
            self.mostrar_usuarios,
            "users.png",
        )

        self.crear_boton_menu(
            frame_sidebar,
            "Productos",
            self.mostrar_productos,
            "productos.png",
        )

        self.crear_boton_menu(
            frame_sidebar,
            "Ventas",
            self.mostrar_ventas,
            "sales.png",
        )

        tk.Frame(
            frame_sidebar,
            bg=self.color_encabezado,
        ).pack(
            fill="both",
            expand=True,
        )

        self.crear_boton(
            frame_sidebar,
            "Cerrar sesion",
            self.cerrar_sesion,
            "Eliminar.TButton",
            "logout.png",
        ).pack(
            fill="x",
            pady=(16, 0),
        )

        frame_principal = tk.Frame(
            self,
            bg=self.color_fondo,
        )

        frame_principal.pack(
            side="left",
            fill="both",
            expand=True,
        )

        self.contenido = tk.Frame(
            frame_principal,
            bg=self.color_fondo,
            padx=28,
            pady=24,
        )

        self.contenido.pack(
            fill="both",
            expand=True,
        )

        barra_estado = tk.Frame(
            frame_principal,
            bg=self.color_secundario,
            padx=18,
            pady=8,
        )

        barra_estado.pack(
            fill="x",
            side="bottom",
        )

        self.etiqueta_estado = tk.Label(
            barra_estado,
            bg=self.color_secundario,
            fg=self.color_texto,
            font=("Arial", 10),
        )

        self.etiqueta_estado.pack(
            side="left"
        )

        self.mostrar_inicio()

    def crear_boton_menu(
        self,
        contenedor,
        texto,
        comando,
        icono,
    ):
        boton = self.crear_boton(
            contenedor,
            texto,
            comando,
            "MenuApp.TButton",
            icono,
        )

        boton.pack(
            fill="x",
            pady=(0, 8),
        )

        self.botones_menu[texto] = boton

    def marcar_seccion(self, seccion):
        for texto, boton in self.botones_menu.items():
            if texto == seccion:
                estilo = "MenuActivo.TButton"
            else:
                estilo = "MenuApp.TButton"

            boton.configure(
                style=estilo
            )

    def limpiar_contenido(self):
        assert self.contenido is not None

        for widget in self.contenido.winfo_children():
            widget.destroy()

    def actualizar_barra_estado(self):
        assert self.etiqueta_estado is not None

        self.etiqueta_estado.config(
            text=(
                f"Productos: "
                f"{self.restaurante_servicio.cantidad_productos()} | "
                f"Usuarios: "
                f"{self.restaurante_servicio.cantidad_usuarios()} | "
                f"Ventas: "
                f"{self.restaurante_servicio.cantidad_ventas()} | "
                "Datos JSON locales"
            )
        )

    # ---------------------------------------------------------
    # Inicio
    # ---------------------------------------------------------

    def mostrar_inicio(self):
        self.marcar_seccion("Inicio")
        self.limpiar_contenido()
        self.actualizar_barra_estado()

        assert self.contenido is not None

        tk.Label(
            self.contenido,
            text="Panel principal",
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 20, "bold"),
        ).pack(
            anchor="w",
            pady=(0, 8),
        )

        tk.Label(
            self.contenido,
            text=(
                "Consulte usuarios, gestione productos "
                "y registre ventas desde el menu lateral."
            ),
            bg=self.color_fondo,
            fg=self.color_texto,
            font=("Arial", 12),
        ).pack(
            anchor="w",
            pady=(0, 22),
        )

        resumen = tk.Frame(
            self.contenido,
            bg=self.color_fondo,
        )

        resumen.pack(
            fill="x"
        )

        self.crear_tarjeta_resumen(
            resumen,
            "Usuarios registrados",
            self.restaurante_servicio.cantidad_usuarios(),
        )

        self.crear_tarjeta_resumen(
            resumen,
            "Productos registrados",
            self.restaurante_servicio.cantidad_productos(),
        )

        self.crear_tarjeta_resumen(
            resumen,
            "Ventas registradas",
            self.restaurante_servicio.cantidad_ventas(),
        )

    def crear_tarjeta_resumen(
        self,
        contenedor,
        titulo,
        valor,
    ):
        tarjeta = tk.Frame(
            contenedor,
            bg=self.color_panel,
            padx=18,
            pady=16,
        )

        tarjeta.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 14),
        )

        tk.Label(
            tarjeta,
            text=titulo,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).pack(
            anchor="w"
        )

        tk.Label(
            tarjeta,
            text=str(valor),
            bg=self.color_panel,
            fg=self.color_resaltado,
            font=("Arial", 24, "bold"),
        ).pack(
            anchor="w",
            pady=(8, 0),
        )

    # ---------------------------------------------------------
    # Usuarios
    # ---------------------------------------------------------

    def mostrar_usuarios(self):
        self.marcar_seccion("Usuarios")
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion(
            "Usuarios registrados"
        )

        listado = self.crear_listado(
            self.contenido,
            "Consulta de usuarios",
        )

        self.tabla_usuarios = self.crear_tabla(
            listado,
            (
                "identificador",
                "nombre",
                "usuario",
            ),
            (
                "Identificador",
                "Nombre",
                "Usuario",
            ),
        )

        self.refrescar_usuarios()

    def refrescar_usuarios(self):
        assert self.tabla_usuarios is not None

        self.limpiar_tabla(
            self.tabla_usuarios
        )

        for usuario in (
            self.restaurante_servicio
            .listar_usuarios()
        ):
            self.tabla_usuarios.insert(
                "",
                tk.END,
                values=(
                    usuario.identificador,
                    usuario.nombre,
                    usuario.usuario,
                ),
            )

        self.actualizar_barra_estado()

    # ---------------------------------------------------------
    # Productos
    # ---------------------------------------------------------

    def mostrar_productos(self):
        self.marcar_seccion("Productos")
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion(
            "Gestion de productos"
        )

        cuerpo = tk.Frame(
            self.contenido,
            bg=self.color_fondo,
        )

        cuerpo.pack(
            fill="both",
            expand=True,
        )

        cuerpo.grid_columnconfigure(
            1,
            weight=1,
        )

        cuerpo.grid_rowconfigure(
            0,
            weight=1,
        )

        formulario = tk.LabelFrame(
            cuerpo,
            text="Datos del producto",
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=14,
            pady=14,
        )

        formulario.grid(
            row=0,
            column=0,
            sticky="n",
            padx=(0, 18),
        )

        self.producto_codigo_entry = self.crear_campo(
            formulario,
            "Codigo",
            0,
        )

        self.producto_nombre_entry = self.crear_campo(
            formulario,
            "Nombre",
            1,
        )

        self.producto_categoria_entry = self.crear_campo(
            formulario,
            "Categoria",
            2,
        )

        self.producto_precio_entry = self.crear_campo(
            formulario,
            "Precio",
            3,
        )

        self.producto_stock_entry = self.crear_campo(
            formulario,
            "Stock",
            4,
        )

        acciones = tk.Frame(
            formulario,
            bg=self.color_panel,
        )

        acciones.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(12, 0),
        )

        botones = (
            (
                "Registrar",
                self.registrar_producto,
                "Accion.TButton",
                "add.png",
            ),
            (
                "Cargar por codigo",
                self.cargar_producto_en_formulario,
                "Secundario.TButton",
                "search.png",
            ),
            (
                "Actualizar",
                self.actualizar_producto,
                "Accion.TButton",
                "edit.png",
            ),
            (
                "Eliminar",
                self.eliminar_producto,
                "Eliminar.TButton",
                "delete.png",
            ),
            (
                "Limpiar",
                self.limpiar_formulario_producto,
                "Secundario.TButton",
                "clean.png",
            ),
        )

        for texto, comando, estilo, icono in botones:
            self.crear_boton(
                acciones,
                texto,
                comando,
                estilo,
                icono,
            ).pack(
                fill="x",
                pady=(0, 7),
            )

        listado = self.crear_listado(
            cuerpo,
            "Productos registrados",
            usar_grid=True,
        )

        self.tabla_productos = self.crear_tabla(
            listado,
            (
                "codigo",
                "nombre",
                "categoria",
                "precio",
                "stock",
            ),
            (
                "Codigo",
                "Nombre",
                "Categoria",
                "Precio",
                "Stock",
            ),
        )

        self.refrescar_productos()

    def obtener_datos_producto(self):
        assert self.producto_codigo_entry is not None
        assert self.producto_nombre_entry is not None
        assert self.producto_categoria_entry is not None
        assert self.producto_precio_entry is not None
        assert self.producto_stock_entry is not None

        return (
            self.producto_codigo_entry.get(),
            self.producto_nombre_entry.get(),
            self.producto_categoria_entry.get(),
            self.producto_precio_entry.get(),
            self.producto_stock_entry.get(),
        )

    def registrar_producto(self):
        try:
            self.restaurante_servicio.registrar_producto(
                *self.obtener_datos_producto()
            )

            self.limpiar_formulario_producto()
            self.refrescar_productos()

            messagebox.showinfo(
                "Productos",
                "Producto registrado correctamente.",
            )

        except ValueError as error:
            messagebox.showerror(
                "Productos",
                str(error),
            )

    def cargar_producto_en_formulario(self):
        assert self.producto_codigo_entry is not None
        assert self.producto_nombre_entry is not None
        assert self.producto_categoria_entry is not None
        assert self.producto_precio_entry is not None
        assert self.producto_stock_entry is not None

        producto = (
            self.restaurante_servicio
            .buscar_producto_por_codigo(
                self.producto_codigo_entry.get()
            )
        )

        if producto is None:
            messagebox.showerror(
                "Productos",
                "No existe un producto con ese codigo.",
            )
            return

        self.limpiar_formulario_producto()

        self.producto_codigo_entry.insert(
            0,
            producto.codigo,
        )

        self.producto_nombre_entry.insert(
            0,
            producto.nombre,
        )

        self.producto_categoria_entry.insert(
            0,
            producto.categoria,
        )

        self.producto_precio_entry.insert(
            0,
            producto.precio,
        )

        self.producto_stock_entry.insert(
            0,
            producto.stock,
        )

    def actualizar_producto(self):
        try:
            self.restaurante_servicio.actualizar_producto(
                *self.obtener_datos_producto()
            )

            self.refrescar_productos()

            messagebox.showinfo(
                "Productos",
                "Producto actualizado correctamente.",
            )

        except ValueError as error:
            messagebox.showerror(
                "Productos",
                str(error),
            )

    def eliminar_producto(self):
        assert self.producto_codigo_entry is not None

        try:
            self.restaurante_servicio.eliminar_producto(
                self.producto_codigo_entry.get()
            )

            self.limpiar_formulario_producto()
            self.refrescar_productos()

            messagebox.showinfo(
                "Productos",
                "Producto eliminado correctamente.",
            )

        except ValueError as error:
            messagebox.showerror(
                "Productos",
                str(error),
            )

    def limpiar_formulario_producto(self):
        entradas = (
            self.producto_codigo_entry,
            self.producto_nombre_entry,
            self.producto_categoria_entry,
            self.producto_precio_entry,
            self.producto_stock_entry,
        )

        for entrada in entradas:
            assert entrada is not None

            entrada.delete(
                0,
                tk.END,
            )

    def refrescar_productos(self):
        assert self.tabla_productos is not None

        self.limpiar_tabla(
            self.tabla_productos
        )

        for producto in (
            self.restaurante_servicio
            .listar_productos()
        ):
            self.tabla_productos.insert(
                "",
                tk.END,
                values=(
                    producto.codigo,
                    producto.nombre,
                    producto.categoria,
                    producto.precio,
                    producto.stock,
                ),
            )

        self.actualizar_barra_estado()

    # ---------------------------------------------------------
    # Ventas - Semana 15
    # ---------------------------------------------------------

    def mostrar_ventas(self):
        self.marcar_seccion("Ventas")
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion(
            "Ventas"
        )

        cuerpo = tk.Frame(
            self.contenido,
            bg=self.color_fondo,
        )

        cuerpo.pack(
            fill="both",
            expand=True,
        )

        cuerpo.grid_columnconfigure(
            1,
            weight=1,
        )

        cuerpo.grid_rowconfigure(
            0,
            weight=1,
        )

        formulario = tk.LabelFrame(
            cuerpo,
            text="Registrar venta",
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=14,
            pady=14,
        )

        formulario.grid(
            row=0,
            column=0,
            sticky="n",
            padx=(0, 18),
        )

        self.usuario_venta_combo = (
            self.crear_selector_venta(
                formulario,
                "Usuario",
                0,
                self.obtener_opciones_usuarios_venta(),
            )
        )

        self.producto_venta_combo = (
            self.crear_selector_venta(
                formulario,
                "Producto",
                1,
                self.obtener_opciones_productos_venta(),
            )
        )

        acciones = tk.Frame(
            formulario,
            bg=self.color_panel,
        )

        acciones.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(12, 0),
        )

        # Evento principal de la Semana 15:
        # command= conecta el boton con el callback.
        self.crear_boton(
            acciones,
            "Registrar venta",
            self.registrar_venta,
            "Accion.TButton",
            "add.png",
        ).pack(
            fill="x"
        )

        listado = self.crear_listado(
            cuerpo,
            "Ventas registradas",
            usar_grid=True,
        )

        self.tabla_ventas = self.crear_tabla(
            listado,
            (
                "identificador",
                "usuario",
                "producto",
                "fecha",
            ),
            (
                "Venta",
                "Usuario",
                "Producto",
                "Fecha",
            ),
        )

        self.refrescar_ventas()

    def crear_selector_venta(
        self,
        contenedor,
        etiqueta,
        fila,
        opciones,
    ):
        tk.Label(
            contenedor,
            text=etiqueta,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(
            row=fila,
            column=0,
            sticky="w",
            pady=(0, 8),
            padx=(0, 10),
        )

        selector = ttk.Combobox(
            contenedor,
            values=list(opciones.keys()),
            state="readonly",
            width=34,
        )

        selector.grid(
            row=fila,
            column=1,
            sticky="ew",
            pady=(0, 8),
        )

        return selector

    def obtener_opciones_usuarios_venta(self):
        self.opciones_usuarios_venta = {
            (
                f"{usuario.identificador} - "
                f"{usuario.nombre}"
            ): usuario.identificador
            for usuario in (
                self.restaurante_servicio
                .listar_usuarios()
            )
        }

        return self.opciones_usuarios_venta

    def obtener_opciones_productos_venta(self):
        self.opciones_productos_venta = {
            (
                f"{producto.codigo} - "
                f"{producto.nombre}"
            ): producto.codigo
            for producto in (
                self.restaurante_servicio
                .listar_productos()
            )
        }

        return self.opciones_productos_venta

    def registrar_venta(self):
        assert self.usuario_venta_combo is not None
        assert self.producto_venta_combo is not None

        usuario_id = (
            self.opciones_usuarios_venta.get(
                self.usuario_venta_combo.get(),
                "",
            )
        )

        producto_codigo = (
            self.opciones_productos_venta.get(
                self.producto_venta_combo.get(),
                "",
            )
        )

        try:
            self.restaurante_servicio.registrar_venta(
                usuario_id,
                producto_codigo,
            )

            self.limpiar_formulario_venta()
            self.refrescar_ventas()

            messagebox.showinfo(
                "Ventas",
                "Venta registrada correctamente.",
            )

        except ValueError as error:
            messagebox.showerror(
                "Ventas",
                str(error),
            )

    def limpiar_formulario_venta(self):
        assert self.usuario_venta_combo is not None
        assert self.producto_venta_combo is not None

        self.usuario_venta_combo.set("")
        self.producto_venta_combo.set("")

    def refrescar_ventas(self):
        assert self.tabla_ventas is not None

        self.limpiar_tabla(
            self.tabla_ventas
        )

        for venta in (
            self.restaurante_servicio
            .listar_ventas()
        ):
            usuario = (
                self.restaurante_servicio
                .buscar_usuario_por_identificador(
                    venta.usuario_id
                )
            )

            producto = (
                self.restaurante_servicio
                .buscar_producto_por_codigo(
                    venta.producto_codigo
                )
            )

            if usuario is None:
                texto_usuario = venta.usuario_id
            else:
                texto_usuario = (
                    f"{usuario.identificador} - "
                    f"{usuario.nombre}"
                )

            if producto is None:
                texto_producto = venta.producto_codigo
            else:
                texto_producto = (
                    f"{producto.codigo} - "
                    f"{producto.nombre}"
                )

            self.tabla_ventas.insert(
                "",
                tk.END,
                values=(
                    venta.identificador,
                    texto_usuario,
                    texto_producto,
                    venta.fecha,
                ),
            )

        self.actualizar_barra_estado()

    # ---------------------------------------------------------
    # Utilidades compartidas
    # ---------------------------------------------------------

    def crear_titulo_seccion(
        self,
        texto,
    ):
        assert self.contenido is not None

        tk.Label(
            self.contenido,
            text=texto,
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 20, "bold"),
        ).pack(
            anchor="w",
            pady=(0, 16),
        )

    def crear_campo(
        self,
        contenedor,
        etiqueta,
        fila,
    ):
        tk.Label(
            contenedor,
            text=etiqueta,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(
            row=fila,
            column=0,
            sticky="w",
            pady=(0, 8),
            padx=(0, 10),
        )

        entrada = tk.Entry(
            contenedor,
            width=28,
            font=("Arial", 10),
        )

        entrada.grid(
            row=fila,
            column=1,
            sticky="ew",
            pady=(0, 8),
        )

        return entrada

    def crear_listado(
        self,
        contenedor,
        titulo,
        usar_grid=False,
    ):
        listado = tk.LabelFrame(
            contenedor,
            text=titulo,
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=12,
            pady=12,
        )

        if usar_grid:
            listado.grid(
                row=0,
                column=1,
                sticky="nsew",
            )
        else:
            listado.pack(
                fill="both",
                expand=True,
            )

        return listado

    def crear_tabla(
        self,
        contenedor,
        columnas,
        encabezados,
    ):
        frame_tabla = tk.Frame(
            contenedor,
            bg=self.color_panel,
        )

        frame_tabla.pack(
            fill="both",
            expand=True,
        )

        tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=12,
        )

        barra = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=tabla.yview,
        )

        tabla.configure(
            yscrollcommand=barra.set
        )

        for columna, encabezado in zip(
            columnas,
            encabezados,
        ):
            tabla.heading(
                columna,
                text=encabezado,
            )

            tabla.column(
                columna,
                width=150,
                anchor="w",
            )

        tabla.pack(
            side="left",
            fill="both",
            expand=True,
        )

        barra.pack(
            side="right",
            fill="y",
        )

        return tabla

    def limpiar_tabla(
        self,
        tabla,
    ):
        for item in tabla.get_children():
            tabla.delete(item)

    def cerrar_sesion(self):
        self.al_cerrar_sesion()