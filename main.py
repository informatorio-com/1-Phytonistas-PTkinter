import tkinter as tk
from tkinter import messagebox
import persistencia_datos 
import os 
import datetime 

# --- Constantes Globales ---
NOMBRE_ARCHIVO_CSV = "contactos.csv" 
NOMBRES_CAMPOS = ['nombre', 'telefono', 'mail', 'cumpleanos'] 
MENSAJE_CUMPLEANOS_PREDEFINIDO = "¡Feliz cumpleaños! Que tengas un día maravilloso lleno de alegría y sorpresas."

# --- Configuración de Estilos (Colores y Fuentes) ---
COLOR_FONDO_PRINCIPAL = "#282828"  # Negro oscuro
COLOR_FONDO_FRAMES = "#3C3C3C"     # Gris oscuro para los frames
COLOR_TEXTO_PRINCIPAL = "#FFFFFF"  # Blanco para el texto
COLOR_BORDE_ELEMENTOS = "#555555"  # Gris medio para bordes

COLOR_BOTON_FONDO = "#5A5A5A"      # Gris más claro para el fondo de los botones
COLOR_BOTON_TEXTO = "#FFFFFF"      # Blanco para el texto de los botones
COLOR_BOTON_ACTIVO_FONDO = "#707070" # Gris un poco más claro al pasar el ratón

FUENTE_TITULO = ("Arial", 14, "bold")
FUENTE_ETIQUETA = ("Arial", 10)
FUENTE_ENTRADA = ("Arial", 10)
FUENTE_LISTBOX = ("Consolas", 10) 

class GestorContactosApp:
    def __init__(self, maestro):
        self.maestro = maestro
        maestro.title("Gestor de Contactos")
        maestro.geometry("650x580") 
        maestro.resizable(False, False)
        maestro.config(bg=COLOR_FONDO_PRINCIPAL) 

        self.contactos = []

        self.var_nombre = tk.StringVar()
        self.var_telefono = tk.StringVar()
        self.var_mail = tk.StringVar()
        self.var_cumpleanos = tk.StringVar()
        self.var_busqueda = tk.StringVar()

        self.crear_widgets()
        
        self.cargar_contactos()
        self.actualizar_mostrar_contactos()
        
        self.maestro.after(500, self.verificar_cumpleanos) 

    def crear_widgets(self):
        # Frame para campos de entrada
        frame_entrada = tk.Frame(self.maestro, padx=15, pady=15, bg=COLOR_FONDO_FRAMES, bd=2, relief="groove", highlightbackground=COLOR_BORDE_ELEMENTOS, highlightthickness=1)
        frame_entrada.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(frame_entrada, text="Nombre:", font=FUENTE_ETIQUETA, bg=COLOR_FONDO_FRAMES, fg=COLOR_TEXTO_PRINCIPAL).grid(row=0, column=0, sticky="w", pady=2)
        tk.Entry(frame_entrada, textvariable=self.var_nombre, width=40, font=FUENTE_ENTRADA, bd=1, relief="solid", bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_PRINCIPAL, insertbackground=COLOR_TEXTO_PRINCIPAL).grid(row=0, column=1, pady=2, padx=5)

        tk.Label(frame_entrada, text="Teléfono:", font=FUENTE_ETIQUETA, bg=COLOR_FONDO_FRAMES, fg=COLOR_TEXTO_PRINCIPAL).grid(row=1, column=0, sticky="w", pady=2)
        tk.Entry(frame_entrada, textvariable=self.var_telefono, width=40, font=FUENTE_ENTRADA, bd=1, relief="solid", bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_PRINCIPAL, insertbackground=COLOR_TEXTO_PRINCIPAL).grid(row=1, column=1, pady=2, padx=5)

        tk.Label(frame_entrada, text="Mail:", font=FUENTE_ETIQUETA, bg=COLOR_FONDO_FRAMES, fg=COLOR_TEXTO_PRINCIPAL).grid(row=2, column=0, sticky="w", pady=2)
        tk.Entry(frame_entrada, textvariable=self.var_mail, width=40, font=FUENTE_ENTRADA, bd=1, relief="solid", bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_PRINCIPAL, insertbackground=COLOR_TEXTO_PRINCIPAL).grid(row=2, column=1, pady=2, padx=5)

        tk.Label(frame_entrada, text="Cumpleaños (DD/MM):", font=FUENTE_ETIQUETA, bg=COLOR_FONDO_FRAMES, fg=COLOR_TEXTO_PRINCIPAL).grid(row=3, column=0, sticky="w", pady=2)
        tk.Entry(frame_entrada, textvariable=self.var_cumpleanos, width=40, font=FUENTE_ENTRADA, bd=1, relief="solid", bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_PRINCIPAL, insertbackground=COLOR_TEXTO_PRINCIPAL).grid(row=3, column=1, pady=2, padx=5)

        # Frame para botones CRUD
        frame_botones_crud = tk.Frame(self.maestro, padx=15, pady=5, bg=COLOR_FONDO_PRINCIPAL)
        frame_botones_crud.pack(fill=tk.X, padx=10, pady=5)
        
        estilo_boton = {
            "bg": COLOR_BOTON_FONDO,
            "fg": COLOR_BOTON_TEXTO,
            "font": FUENTE_ETIQUETA,
            "relief": "raised",
            "bd": 2,
            "width": 14,
            "activebackground": COLOR_BOTON_ACTIVO_FONDO, # Color al hacer clic
            "activeforeground": COLOR_BOTON_TEXTO # Color de texto al hacer clic
        }

        tk.Button(frame_botones_crud, text="Crear Contacto", command=self.al_crear_contacto, **estilo_boton).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(frame_botones_crud, text="Editar Contacto", command=self.al_editar_contacto, **estilo_boton).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(frame_botones_crud, text="Eliminar Contacto", command=self.al_eliminar_contacto, **estilo_boton).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(frame_botones_crud, text="Limpiar Campos", command=self.limpiar_campos, **estilo_boton).pack(side=tk.RIGHT, padx=5, pady=5)

        # Frame para el buscador de contactos
        frame_busqueda = tk.Frame(self.maestro, padx=15, pady=5, bg=COLOR_FONDO_PRINCIPAL)
        frame_busqueda.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(frame_busqueda, text="Buscar:", font=FUENTE_ETIQUETA, bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_PRINCIPAL).pack(side=tk.LEFT, padx=5)
        tk.Entry(frame_busqueda, textvariable=self.var_busqueda, width=30, font=FUENTE_ENTRADA, bd=1, relief="solid", bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_PRINCIPAL, insertbackground=COLOR_TEXTO_PRINCIPAL).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_busqueda, text="Buscar", command=self.al_buscar_contacto, **estilo_boton).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_busqueda, text="Mostrar Todos", command=lambda: self.actualizar_mostrar_contactos(self.contactos), **estilo_boton).pack(side=tk.LEFT, padx=5)

        # Área de visualización de contactos (Listbox)
        tk.Label(self.maestro, text="Lista de Contactos:", font=FUENTE_TITULO, bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_PRINCIPAL).pack(pady=5)
        
        frame_listbox_container = tk.Frame(self.maestro, bg=COLOR_FONDO_FRAMES, bd=2, relief="sunken", highlightbackground=COLOR_BORDE_ELEMENTOS, highlightthickness=1)
        frame_listbox_container.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # --- Títulos para la Listbox (nuevas etiquetas) ---
        frame_titulos_listbox = tk.Frame(frame_listbox_container, bg=COLOR_FONDO_FRAMES)
        frame_titulos_listbox.pack(fill=tk.X, padx=2, pady=(2, 0)) # Margen superior para separación

        # Label para cada columna
        tk.Label(frame_titulos_listbox, text="Nº", font=("Consolas", 10, "bold"), bg=COLOR_FONDO_FRAMES, fg=COLOR_TEXTO_PRINCIPAL, width=4).pack(side=tk.LEFT)
        tk.Label(frame_titulos_listbox, text="Nombre", font=("Consolas", 10, "bold"), bg=COLOR_FONDO_FRAMES, fg=COLOR_TEXTO_PRINCIPAL, width=20, anchor='w').pack(side=tk.LEFT)
        tk.Label(frame_titulos_listbox, text="Teléfono", font=("Consolas", 10, "bold"), bg=COLOR_FONDO_FRAMES, fg=COLOR_TEXTO_PRINCIPAL, width=15, anchor='w').pack(side=tk.LEFT)
        tk.Label(frame_titulos_listbox, text="Email", font=("Consolas", 10, "bold"), bg=COLOR_FONDO_FRAMES, fg=COLOR_TEXTO_PRINCIPAL, width=30, anchor='w').pack(side=tk.LEFT)
        tk.Label(frame_titulos_listbox, text="Cumpleaños", font=("Consolas", 10, "bold"), bg=COLOR_FONDO_FRAMES, fg=COLOR_TEXTO_PRINCIPAL, width=10, anchor='w').pack(side=tk.LEFT)
        # --- Fin de títulos ---

        # Listbox real
        self.listbox_contactos = tk.Listbox(frame_listbox_container, height=10, font=FUENTE_LISTBOX, 
                                            bd=0, highlightthickness=0, # Eliminar bordes por defecto
                                            bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_PRINCIPAL, 
                                            selectbackground=COLOR_BOTON_FONDO, selectforeground=COLOR_BOTON_TEXTO)
        self.listbox_contactos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2) 
        
        barra_desplazamiento = tk.Scrollbar(frame_listbox_container, orient="vertical", command=self.listbox_contactos.yview, troughcolor=COLOR_FONDO_PRINCIPAL, bg=COLOR_BOTON_FONDO, activebackground=COLOR_BOTON_ACTIVO_FONDO)
        barra_desplazamiento.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_contactos.config(yscrollcommand=barra_desplazamiento.set)
        
        self.listbox_contactos.bind('<<ListboxSelect>>', self.al_seleccionar_listbox)

        # Etiqueta para la alarma de cumpleaños
        self.etiqueta_alarma_cumpleanos = tk.Label(self.maestro, text="[Verificando cumpleaños...]", fg=COLOR_TEXTO_PRINCIPAL, font=FUENTE_ETIQUETA, bg=COLOR_FONDO_PRINCIPAL)
        self.etiqueta_alarma_cumpleanos.pack(pady=5)


    # --- Funciones de Manejo de Archivos (USAN EL MÓDULO EXTERNO) ---
    def cargar_contactos(self):
        """
        Carga los contactos usando la función del módulo 'persistencia_datos'.
        """
        self.contactos = persistencia_datos.cargar_contactos_desde_csv(NOMBRE_ARCHIVO_CSV, NOMBRES_CAMPOS)
        
        if not self.contactos:
            print("No se encontraron contactos, la lista de contactos está vacía.")
        else:
            print("Contactos cargados desde CSV.")


    def guardar_contactos(self):
        """
        Guarda el contenido de self.contactos en el archivo CSV usando el módulo externo.
        """
        persistencia_datos.guardar_contactos_en_csv(self.contactos, NOMBRE_ARCHIVO_CSV, NOMBRES_CAMPOS)


    # --- Funciones de Interfaz Gráfica (Mostrar y Limpiar) ---
    def actualizar_mostrar_contactos(self, contactos_a_mostrar=None):
        self.listbox_contactos.delete(0, tk.END)
        
        lista_a_mostrar = contactos_a_mostrar if contactos_a_mostrar is not None else self.contactos
        
        # Alinear las columnas de la Listbox
        ANCHO_NOMBRE = 20
        ANCHO_TELEFONO = 15
        ANCHO_MAIL = 36
        ANCHO_CUMPLE = 10

        for i, contacto in enumerate(lista_a_mostrar):
            nombre = contacto.get('nombre', 'N/A').ljust(ANCHO_NOMBRE)[:ANCHO_NOMBRE]
            telefono = contacto.get('telefono', 'N/A').ljust(ANCHO_TELEFONO)[:ANCHO_TELEFONO]
            mail = contacto.get('mail', 'N/A').ljust(ANCHO_MAIL)[:ANCHO_MAIL]
            cumpleanos = contacto.get('cumpleanos', 'N/A').ljust(ANCHO_CUMPLE)[:ANCHO_CUMPLE]
            
            # El número se alinea a la derecha 
            texto_mostrar = f"{i+1:2}. {nombre}{telefono}{mail}{cumpleanos}"
            self.listbox_contactos.insert(tk.END, texto_mostrar)
        print("Función 'actualizar_mostrar_contactos' ejecutada.")

    def limpiar_campos(self):
        self.var_nombre.set("")
        self.var_telefono.set("")
        self.var_mail.set("")
        self.var_cumpleanos.set("")
        self.var_busqueda.set("")
        self.listbox_contactos.selection_clear(0, tk.END)
        print("Función 'limpiar_campos' ejecutada.")

    # --- Lógica de Validación de Contactos ---
    def validar_datos_contacto(self, datos_contacto):
        cumple = datos_contacto.get('cumpleanos', '')
        if cumple and not (len(cumple) == 5 and cumple[2] == '/' and cumple[0:2].isdigit() and cumple[3:5].isdigit()):
            messagebox.showwarning("Error de Validación", "El formato del cumpleaños debe ser DD/MM.")
            return False
        
        mail = datos_contacto.get('mail', '')
        if mail and ('@' not in mail or '.' not in mail):
            messagebox.showwarning("Error de Validación", "El formato del correo electrónico no es válido.")
            return False

        return True 

    # --- Lógica de Interacción con Listbox ---
    def al_seleccionar_listbox(self, evento):
        selected_indices = self.listbox_contactos.curselection()
        if selected_indices:
            index_seleccionado = selected_indices[0]
            
            if 0 <= index_seleccionado < len(self.contactos):
                contacto_seleccionado = self.contactos[index_seleccionado]
                self.var_nombre.set(contacto_seleccionado.get('nombre', ''))
                self.var_telefono.set(contacto_seleccionado.get('telefono', ''))
                self.var_mail.set(contacto_seleccionado.get('mail', ''))
                self.var_cumpleanos.set(contacto_seleccionado.get('cumpleanos', ''))
            print("Función 'al_seleccionar_listbox' ejecutada.")


    # --- Lógica de Crear, Editar y Eliminar Contactos ---
    def al_crear_contacto(self):
        nombre = self.var_nombre.get().strip()
        telefono = self.var_telefono.get().strip()
        mail = self.var_mail.get().strip()
        cumpleanos = self.var_cumpleanos.get().strip()
        
        if not nombre or not telefono or not mail:
            messagebox.showwarning("Campos vacíos", "Por favor, completa Nombre, Teléfono y Mail.")
            return

        nuevo_contacto = {
            "nombre": nombre,
            "telefono": telefono,
            "mail": mail,
            "cumpleanos": cumpleanos
        }
        
        if not self.validar_datos_contacto(nuevo_contacto):
            return

        for contacto_existente in self.contactos:
            if contacto_existente['nombre'].lower() == nombre.lower():
                messagebox.showwarning("Advertencia", "Ya existe un contacto con este nombre.")
                return

        self.contactos.append(nuevo_contacto)
        self.guardar_contactos()
        self.actualizar_mostrar_contactos()
        self.limpiar_campos()
        messagebox.showinfo("Éxito", f"Contacto '{nombre}' creado correctamente.")
        print(f"Contacto '{nombre}' creado con éxito.")


    def al_editar_contacto(self):
        selected_indices = self.listbox_contactos.curselection()

        if not selected_indices:
            messagebox.showwarning("Advertencia", "Seleccioná un contacto para editar.")
            return

        index = selected_indices[0] 

        nombre = self.var_nombre.get().strip()
        telefono = self.var_telefono.get().strip()
        mail = self.var_mail.get().strip()
        cumpleanos = self.var_cumpleanos.get().strip()

        if not nombre or not telefono or not mail:
            messagebox.showwarning("Campos vacíos", "Por favor, completá Nombre, Teléfono y Mail.")
            return

        contacto_editado = {
            "nombre": nombre,
            "telefono": telefono,
            "mail": mail,
            "cumpleanos": cumpleanos
        }
        
        if not self.validar_datos_contacto(contacto_editado): 
            return

        for i, c in enumerate(self.contactos):
            if i != index and c['nombre'].lower() == nombre.lower():
                messagebox.showwarning("Advertencia", "Ya existe otro contacto con ese nombre.")
                return

        self.contactos[index] = contacto_editado 
        self.guardar_contactos() 
        self.actualizar_mostrar_contactos() 
        self.limpiar_campos() 

        messagebox.showinfo("Éxito", f"Contacto '{nombre}' editado correctamente.")
        print(f"Contacto '{nombre}' editado exitosamente.")


    def al_eliminar_contacto(self):
        selected_indices = self.listbox_contactos.curselection()

        if not selected_indices:
            messagebox.showwarning("Advertencia", "Debe seleccionar un contacto para eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar eliminación", "¿Está seguro de que desea eliminar el contacto seleccionado?")
        if not confirm:
            return

        index_a_eliminar = selected_indices[0]
        
        nombre_contacto = self.contactos[index_a_eliminar]['nombre']

        del self.contactos[index_a_eliminar]
        
        self.guardar_contactos()
        self.actualizar_mostrar_contactos()
        self.limpiar_campos()

        messagebox.showinfo("Contacto eliminado", f"El contacto '{nombre_contacto}' fue eliminado exitosamente.")
        print(f"Contacto '{nombre_contacto}' eliminado con éxito.")
        

    # --- Lógica de Búsqueda de Contactos ---
    def al_buscar_contacto(self):
        termino_busqueda = self.var_busqueda.get().strip().lower()
        
        if not termino_busqueda:
            self.actualizar_mostrar_contactos(self.contactos)
            return

        contactos_encontrados = []
        for contacto in self.contactos:
            if (termino_busqueda in contacto.get('nombre', '').lower() or
                termino_busqueda in contacto.get('telefono', '').lower() or
                termino_busqueda in contacto.get('mail', '').lower()):
                contactos_encontrados.append(contacto)
        
        self.actualizar_mostrar_contactos(contactos_encontrados)
        
        if not contactos_encontrados:
            messagebox.showinfo("Búsqueda", "No se encontraron contactos que coincidan.")
        print("Función 'al_buscar_contacto' ejecutada.")

    # --- Función para mostrar pop-ups personalizados y centrados ---
    def mostrar_popup_centrado(self, titulo, mensaje_principal, es_confirmacion=False):
        """
        Muestra un pop-up Toplevel personalizado y centrado.
        Si es_confirmacion es True, incluye botones Sí/No y devuelve la elección del usuario.
        De lo contrario, es un pop-up de información simple que se cierra con un botón OK.
        """
        popup = tk.Toplevel(self.maestro)
        popup.title(titulo)
        popup.transient(self.maestro) # Hace que el pop-up esté siempre por encima de la ventana principal
        popup.grab_set() # Bloquea la interacción con la ventana principal mientras el pop-up está abierto

        # Centrar el pop-up
        self.maestro.update_idletasks() # Asegurarse de que el tamaño de la ventana principal esté actualizado
        
        # Obtener dimensiones de la ventana principal
        main_window_width = self.maestro.winfo_width()
        main_window_height = self.maestro.winfo_height()
        main_window_x = self.maestro.winfo_x()
        main_window_y = self.maestro.winfo_y()

        # Dimensiones estimadas del pop-up (pueden requerir ajuste fino)
        popup_width = 400
        popup_height = 180 if es_confirmacion else 150 # Más alto si hay botones de confirmación

        # Calcular posición para centrar
        x = main_window_x + (main_window_width // 2) - (popup_width // 2)
        y = main_window_y + (main_window_height // 2) - (popup_height // 2)

        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        popup.resizable(False, False)
        popup.config(bg=COLOR_FONDO_FRAMES)

        tk.Label(popup, text="🎉", font=("Arial", 24), bg=COLOR_FONDO_FRAMES).pack(pady=(10, 0))
        tk.Label(popup, text=mensaje_principal, font=FUENTE_ETIQUETA, bg=COLOR_FONDO_FRAMES, fg=COLOR_TEXTO_PRINCIPAL, wraplength=popup_width - 40).pack(pady=(5, 10))

        button_frame_popup = tk.Frame(popup, bg=COLOR_FONDO_FRAMES)
        button_frame_popup.pack(pady=5)

        # Configurar estilo de botón para el pop-up
        estilo_boton_popup = {
            "bg": COLOR_BOTON_FONDO,
            "fg": COLOR_BOTON_TEXTO,
            "font": FUENTE_ETIQUETA,
            "relief": "raised",
            "bd": 2,
            "width": 16, # Ancho ligeramente mayor para botones de pop-up
            "activebackground": COLOR_BOTON_ACTIVO_FONDO,
            "activeforeground": COLOR_BOTON_TEXTO
        }

        resultado_confirmacion = tk.BooleanVar(value=False)

        if es_confirmacion:
            def on_yes():
                resultado_confirmacion.set(True)
                popup.destroy()

            def on_no():
                resultado_confirmacion.set(False)
                popup.destroy()

            tk.Button(button_frame_popup, text="Sí, enviar mensaje", command=on_yes, **estilo_boton_popup).pack(side=tk.LEFT, padx=5)
            tk.Button(button_frame_popup, text="No enviar", command=on_no, **estilo_boton_popup).pack(side=tk.LEFT, padx=5)
        else: # Si no es de confirmación, es un botón OK
            def on_ok():
                popup.destroy()
            tk.Button(button_frame_popup, text="OK", command=on_ok, **estilo_boton_popup).pack(padx=5)

        self.maestro.wait_window(popup) # Espera a que el pop-up se cierre antes de continuar

        return resultado_confirmacion.get() if es_confirmacion else None # Devuelve elección para confirmación


    # --- Lógica de Alarma de Cumpleaños ---
    def verificar_cumpleanos(self):
        """
        Verifica si hay cumpleaños hoy y muestra una alarma con pop-up centrado.
        """
        hoy = datetime.datetime.now().strftime("%d/%m")
        cumpleañeros = [c for c in self.contactos if c.get("cumpleanos", "") == hoy]

        if cumpleañeros:
            nombres = ", ".join(c['nombre'] for c in cumpleañeros)
            texto_alarma = f"¡Hoy cumplen años: {nombres}!"
            self.etiqueta_alarma_cumpleanos.config(text=texto_alarma, fg="#FFC107") # Naranja/Amarillo para la alarma
            
            # Usar el pop-up personalizado para la pregunta de envío
            if self.mostrar_popup_centrado("🎉 ¡Feliz Cumpleaños!", 
                                           f"{texto_alarma}\n\n¿Querés enviar un mensaje de cumpleaños?",
                                           es_confirmacion=True): # Indicar que es un pop-up de confirmación
                # Si el usuario elige "Sí"
                for c in cumpleañeros:
                    print(f"Simulando mensaje enviado a {c['nombre']}: {MENSAJE_CUMPLEANOS_PREDEFINIDO}")
                
                # Usar el pop-up personalizado para la confirmación de envío (ahora también centrado)
                self.mostrar_popup_centrado("Mensajes Enviados", f"Se envió '{MENSAJE_CUMPLEANOS_PREDEFINIDO}' a: {nombres}.")
        else:
            self.etiqueta_alarma_cumpleanos.config(text="Nadie cumple años hoy.", fg=COLOR_TEXTO_PRINCIPAL)


# --- Punto de Entrada de la Aplicación ---
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = GestorContactosApp(ventana_principal)
    ventana_principal.mainloop()
# --- Fin del Código ---