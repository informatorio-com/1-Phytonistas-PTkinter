import tkinter as tk
from tkinter import messagebox
# Importar el nuevo módulo de persistencia
import persistencia_datos 
import os # Necesario para algunas verificaciones en cargar_contactos
import datetime # Necesario para la función de cumpleaños

# --- Constantes Globales ---
# Ya no necesitamos el diccionario ARCHIVO_CONTACTOS_INICIAL_EJEMPLO aquí
# Los contactos se cargarán/guardarán desde el archivo CSV directamente
NOMBRE_ARCHIVO_CSV = "contactos.csv" # Nombre del archivo CSV real para guardar/cargar
NOMBRES_CAMPOS = ['nombre', 'telefono', 'mail', 'cumpleanos'] # Encabezados de los contactos
MENSAJE_CUMPLEANOS_PREDEFINIDO = "¡Feliz cumpleaños! Te deseo un día lleno de alegría y sorpresas."

class GestorContactosApp:
    def __init__(self, maestro):
        self.maestro = maestro
        maestro.title("Gestor de Contactos - Mínimo")
        maestro.geometry("650x550")
        maestro.resizable(False, False)

        self.contactos = []

        self.var_nombre = tk.StringVar()
        self.var_telefono = tk.StringVar()
        self.var_mail = tk.StringVar()
        self.var_cumpleanos = tk.StringVar()
        self.var_busqueda = tk.StringVar()

        self.crear_widgets()
        
        # Cargar contactos al inicio usando el nuevo módulo
        self.cargar_contactos()
        self.actualizar_mostrar_contactos()


    def crear_widgets(self):
        frame_entrada = tk.Frame(self.maestro, padx=10, pady=10)
        frame_entrada.pack(fill=tk.X)

        tk.Label(frame_entrada, text="Nombre:").grid(row=0, column=0, sticky="w", pady=2)
        tk.Entry(frame_entrada, textvariable=self.var_nombre, width=40).grid(row=0, column=1, pady=2)

        tk.Label(frame_entrada, text="Teléfono:").grid(row=1, column=0, sticky="w", pady=2)
        tk.Entry(frame_entrada, textvariable=self.var_telefono, width=40).grid(row=1, column=1, pady=2)

        tk.Label(frame_entrada, text="Mail:").grid(row=2, column=0, sticky="w", pady=2)
        tk.Entry(frame_entrada, textvariable=self.var_mail, width=40).grid(row=2, column=1, pady=2)

        tk.Label(frame_entrada, text="Cumpleaños (DD/MM):").grid(row=3, column=0, sticky="w", pady=2)
        tk.Entry(frame_entrada, textvariable=self.var_cumpleanos, width=40).grid(row=3, column=1, pady=2)

        frame_botones = tk.Frame(self.maestro, padx=10, pady=5)
        frame_botones.pack(fill=tk.X)
        
        tk.Button(frame_botones, text="Crear Contacto", command=self.al_crear_contacto).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(frame_botones, text="Editar Contacto", command=self.al_editar_contacto).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(frame_botones, text="Eliminar Contacto", command=self.al_eliminar_contacto).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(frame_botones, text="Limpiar Campos", command=self.limpiar_campos).pack(side=tk.RIGHT, padx=5, pady=5)

        frame_busqueda = tk.Frame(self.maestro, padx=10, pady=5)
        frame_busqueda.pack(fill=tk.X)

        tk.Label(frame_busqueda, text="Buscar:").pack(side=tk.LEFT, padx=5)
        tk.Entry(frame_busqueda, textvariable=self.var_busqueda, width=30).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_busqueda, text="Buscar", command=self.al_buscar_contacto).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_busqueda, text="Mostrar Todos", command=lambda: self.actualizar_mostrar_contactos(self.contactos)).pack(side=tk.LEFT, padx=5)

        tk.Label(self.maestro, text="Lista de Contactos:", font=("Arial", 12, "bold")).pack(pady=5)
        
        frame_listbox = tk.Frame(self.maestro)
        frame_listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.listbox_contactos = tk.Listbox(frame_listbox, height=10, width=80, font=("Arial", 10))
        self.listbox_contactos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        barra_desplazamiento = tk.Scrollbar(frame_listbox, orient="vertical", command=self.listbox_contactos.yview)
        barra_desplazamiento.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_contactos.config(yscrollcommand=barra_desplazamiento.set)
        
        self.listbox_contactos.bind('<<ListboxSelect>>', self.al_seleccionar_listbox)

        self.etiqueta_alarma_cumpleanos = tk.Label(self.maestro, text="[Alarma de Cumpleaños]", fg="gray", font=("Arial", 10)).pack(pady=5)


    # --- Funciones de Manejo de Archivos (AHORA USAN EL MÓDULO EXTERNO) ---
    def cargar_contactos(self):
        """
        Carga los contactos usando la función del módulo 'persistencia_datos'.
        """
        # Intentamos cargar contactos desde el archivo CSV
        self.contactos = persistencia_datos.cargar_contactos_desde_csv(NOMBRE_ARCHIVO_CSV, NOMBRES_CAMPOS)
        
        # Si la lista de contactos está vacía y el archivo CSV no existe,
        # significa que es la primera vez que se ejecuta la app o el archivo se borró.
        # En este caso, podemos inicializar con una lista vacía o unos datos de ejemplo
        # y guardarlos para que el archivo CSV se cree.
        if not self.contactos and not os.path.exists(NOMBRE_ARCHIVO_CSV):
            print("Archivo CSV no encontrado o vacío. Inicializando con lista de contactos vacía.")
            # Puedes opcionalmente agregar aquí algunos contactos de ejemplo si lo prefieres:
            # self.contactos.append({'nombre': 'Ejemplo', 'telefono': '123', 'mail': 'ejemplo@mail.com', 'cumpleanos': '01/01'})
            # self.guardar_contactos() # Guardar estos contactos de ejemplo para que el archivo se cree
            pass # Si no hay datos de ejemplo, la lista quedará vacía.


    def guardar_contactos(self):
        """
        Guarda el contenido de self.contactos en el archivo CSV usando el módulo externo.
        """
        persistencia_datos.guardar_contactos_en_csv(self.contactos, NOMBRE_ARCHIVO_CSV, NOMBRES_CAMPOS)


    # --- Funciones de Interfaz Gráfica (Mostrar y Limpiar) ---
    def actualizar_mostrar_contactos(self, contactos_a_mostrar=None):
        self.listbox_contactos.delete(0, tk.END)
        
        lista_a_mostrar = contactos_a_mostrar if contactos_a_mostrar is not None else self.contactos
        
        for i, contacto in enumerate(lista_a_mostrar):
            texto_mostrar = (f"{i+1}. Nombre: {contacto.get('nombre', 'N/A')}, Teléfono: {contacto.get('telefono', 'N/A')}, "
                             f"Mail: {contacto.get('mail', 'N/A')}, Cumpleaños: {contacto.get('cumpleanos', 'N/A')}")
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

    # --- Lógica de Validación de Contactos (Esqueleto) ---
    def validar_datos_contacto(self, datos_contacto):
        print("Función 'validar_datos_contacto' ejecutada. (Implementar la lógica de validación)")
        return True 

    # --- Lógica de Interacción con Listbox (Esqueleto) ---
    def al_seleccionar_listbox(self, evento):
        print("Función 'al_seleccionar_listbox' ejecutada. (Implementar para cargar datos en campos)")
        pass


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
        messagebox.showinfo("Acción Pendiente", "Función 'Editar Contacto' debe ser implementada.")
        print("Función 'al_editar_contacto' ejecutada. (Implementar la lógica de edición)")
        pass

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
        

    # --- Lógica de Búsqueda de Contactos (IMPLEMENTADA) ---
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


    # --- Lógica de Alarma de Cumpleaños (Esqueleto) ---
    def verificar_cumpleanos(self):
        print("Función 'verificar_cumpleanos' ejecutada. (Implementar la lógica de alarma)")
        self.etiqueta_alarma_cumpleanos.config(text="[Función de Alarma de Cumpleaños PENDIENTE]")
        pass


# --- Punto de Entrada de la Aplicación ---
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = GestorContactosApp(ventana_principal)
    ventana_principal.mainloop()