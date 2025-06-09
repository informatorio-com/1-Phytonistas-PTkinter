import tkinter as tk
from tkinter import messagebox
#Otros import necesarios para funcionalidades básicas, borrar si no se usan
import csv 
import os 
import datetime  #Necesario para cumpleaños y alarma

#Constantes Globales
ARCHIVO_CONTACTOS = {
    "Juan": {"telefono": "123456789", "email": "juan@example.com", "cumpleanos": "15/05"},
    "Ana": {"telefono": "987654321", "email": "ana@example.com", "cumpleanos": "20/08"},
} #Archivo para guardar/cargar contactos
NOMBRES_CAMPOS = ['nombre', 'telefono', 'mail', 'cumpleanos'] #Encabezados/datos de los contactos
MENSAJE_CUMPLEANOS_PREDEFINIDO = "¡Feliz cumpleaños! Te deseo un día lleno de alegría y sorpresas." #Mensaje de cumpleaños por defecto, editar si quieren

class GestorContactosApp:
    def __init__(self, maestro):
        self.maestro = maestro #Ventana principal de Tkinter
        maestro.title("Gestor de Contactos") #Título de la ventana
        maestro.geometry("550x700") #Tamaño de la ventana
        maestro.resizable(False, False) #No deja redimensionar la ventana
        
        #Lista de contactos en la memoria,lista central que gestiona la aplicación.
        self.contactos = []

        #Variables de control para los campos de entrada, agregar más si es necesario
        self.var_cumpleanos = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_telefono = tk.StringVar()
        self.var_mail = tk.StringVar()
        self.var_cumpleanos = tk.StringVar()
        self.var_busqueda = tk.StringVar() #Para el campo de búsqueda de contactos

        #Wiodgets
        self.crear_widgets()

        #Estas funciones se llaman al inicio
        self.cargar_contactos() #Carga los contactos desde el archivo
        self.verificar_cumpleanos() #Verifica si hay cumpleaños hoy
        self.actualizar_mostrar_contactos() #Muestra los datos cargados (o nada si no hay)

    def crear_widgets(self):
        """
        Configura los elementos visuales de la interfaz:
        campos de entrada, botones de acción y la lista de contactos.
        """
        #Frame para campos de entrada
        frame_entrada = tk.Frame(self.maestro, padx=10, pady=10)
        frame_entrada.pack(fill=tk.X)

        tk.Label(frame_entrada, text="Nombre:").grid(row=0, column=0, sticky="w", pady=2)
        self.entrada_nombre = tk.Entry(frame_entrada, textvariable=self.var_nombre, width=40)
        self.entrada_nombre.grid(row=0, column=1, pady=2)

        tk.Label(frame_entrada, text="Teléfono:").grid(row=1, column=0, sticky="w", pady=2)
        self.entrada_telefono = tk.Entry(frame_entrada, textvariable=self.var_telefono, width=40)
        self.entrada_telefono.grid(row=1, column=1, pady=2)

        tk.Label(frame_entrada, text="Mail:").grid(row=2, column=0, sticky="w", pady=2)
        self.entrada_mail = tk.Entry(frame_entrada, textvariable=self.var_mail, width=40)
        self.entrada_mail.grid(row=2, column=1, pady=2)

        tk.Label(frame_entrada, text="Cumpleaños (DD/MM):").grid(row=3, column=0, sticky="w", pady=2)
        self.entrada_cumpleanos = tk.Entry(frame_entrada, textvariable=self.var_cumpleanos, width=40)
        self.entrada_cumpleanos.grid(row=3, column=1, pady=2)

        #Frame para botones: Crear, Editar, Eliminar contactos
        frame_botones_crud = tk.Frame(self.maestro, padx=10, pady=5)
        frame_botones_crud.pack(fill=tk.X)
        
        #Botones con comandos a funciones que hay que implementar
        self.btn_crear = tk.Button(frame_botones_crud, text="Crear Contacto", command=self.al_crear_contacto)
        self.btn_crear.pack(side=tk.LEFT, padx=5, pady=5) #Botón para crear un contacto

        self.btn_editar = tk.Button(frame_botones_crud, text="Editar Contacto", command=self.al_editar_contacto)
        self.btn_editar.pack(side=tk.LEFT, padx=5, pady=5) #Botón para editar un contacto

        self.btn_eliminar = tk.Button(frame_botones_crud, text="Eliminar Contacto", command=self.al_eliminar_contacto)
        self.btn_eliminar.pack(side=tk.LEFT, padx=5, pady=5) #Botón para eliminar un contacto

        self.btn_limpiar_campos = tk.Button(frame_botones_crud, text="Limpiar Campos", command=self.limpiar_campos)
        self.btn_limpiar_campos.pack(side=tk.RIGHT, padx=5, pady=5)#Botón para limpiar los campos de entrada

        #Frame para el buscador de contactos, ya está funcional
        frame_busqueda = tk.Frame(self.maestro, padx=10, pady=5)
        frame_busqueda.pack(fill=tk.X)

        tk.Label(frame_busqueda, text="Buscar:").pack(side=tk.LEFT, padx=5)
        self.entrada_busqueda = tk.Entry(frame_busqueda, textvariable=self.var_busqueda, width=30)
        self.entrada_busqueda.pack(side=tk.LEFT, padx=5)
        
        self.btn_buscar = tk.Button(frame_busqueda, text="Buscar", command=self.al_buscar_contacto)
        self.btn_buscar.pack(side=tk.LEFT, padx=5)
        
        #Botón para mostrar todos los contactos de nuevo, después de una búsqueda
        self.btn_mostrar_todos = tk.Button(frame_busqueda, text="Mostrar Todos", command=lambda: self.actualizar_mostrar_contactos(self.contactos))
        self.btn_mostrar_todos.pack(side=tk.LEFT, padx=5)

        #Área de visualización de contactos (Listbox)
        tk.Label(self.maestro, text="Lista de Contactos:", font=("Arial", 12, "bold")).pack(pady=10)
        
        frame_listbox = tk.Frame(self.maestro)
        frame_listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.listbox_contactos = tk.Listbox(frame_listbox, height=15, width=80, font=("Arial", 10))
        self.listbox_contactos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        barra_desplazamiento = tk.Scrollbar(frame_listbox, orient="vertical", command=self.listbox_contactos.yview)
        barra_desplazamiento.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_contactos.config(yscrollcommand=barra_desplazamiento.set)
        
        #Vincula la selección en la Listbox a una función no implementada aún
        self.listbox_contactos.bind('<<ListboxSelect>>', self.al_seleccionar_listbox)

        #Etiqueta para la alarma de cumpleaños, no implementada aún
        self.etiqueta_alarma_cumpleanos = tk.Label(self.maestro, text="[Alarma de Cumpleaños Pendiente]", fg="blue", font=("Arial", 12, "bold"))
        self.etiqueta_alarma_cumpleanos.pack(pady=5)


    #Manejo de Archivos (Carga y Guardado de Contactos), agregar el código para manejar archivos CSV
    def cargar_contactos(self):
       
        self.contactos = []  # Vacía la lista actual

        for nombre, datos in ARCHIVO_CONTACTOS.items():
            contacto = {
            "nombre": nombre,
            "telefono": datos.get("telefono", ""),
            "mail": datos.get("email", ""),  # Ten en cuenta que en self.contactos se llama "mail"
            "cumpleanos": datos.get("cumpleanos", "")
            }
            self.contactos.append(contacto)

    print("Contactos cargados desde ARCHIVO_CONTACTOS.")
     

    #Acá va la lógica para guardar los contactos en el archivo ARCHIVO_CONTACTOS
    def guardar_contactos(self):
        pass



    #Funciones de Interfaz Gráfica (Mostrar y Limpiar)
    def actualizar_mostrar_contactos(self, contactos_a_mostrar=None):
        """
        Actualiza la Listbox con los contactos.
        Si 'contactos_a_mostrar' es None, muestra self.contactos (todos).
        Si se le pasa una lista, muestra solo esos resultados de búsqueda.
        """
        self.listbox_contactos.delete(0, tk.END) #Limpiar elementos actuales
        
        lista_a_mostrar = contactos_a_mostrar if contactos_a_mostrar is not None else self.contactos
        
        for i, contacto in enumerate(lista_a_mostrar):
            texto_mostrar = (f"{i+1}. Nombre: {contacto['nombre']}, Teléfono: {contacto['telefono']}, "
                             f"Mail: {contacto['mail']}, Cumpleaños: {contacto['cumpleanos']}")
            self.listbox_contactos.insert(tk.END, texto_mostrar)
        print("Función 'actualizar_mostrar_contactos' ejecutada.")

    def limpiar_campos(self):
        """
        Limpia el texto de todos los campos de entrada.
        """
        self.var_nombre.set("")
        self.var_telefono.set("")
        self.var_mail.set("")
        self.var_cumpleanos.set("")
        self.var_busqueda.set("") # Limpiar también el campo de búsqueda
        self.listbox_contactos.selection_clear(0, tk.END) #Deseleccionar la Listbox
        print("Función 'limpiar_campos' ejecutada.")

    #Lógica de Validación de Contactos, no implementada aún
    def validar_datos_contacto(self, datos_contacto):
        """
        Esqueleto: Valida los datos de un contacto.
        Hay que implementar la lógica de validación.
        Por ahora, siempre devuelve True.
        """
        print("Función 'validar_datos_contacto' ejecutada. (Implementar la lógica de validación)")
        return True #Por defecto, asumimos que es válido hasta que se implemente la validación


    #Lógica de Interacción con Listbox, no implementada aún
   
    def al_seleccionar_listbox(self, evento):
        """
        Esqueleto: Se activa al seleccionar un elemento en la Listbox.
        No implementada aún.
        Se debe implementar la lógica para cargar los datos del contacto seleccionado en los campos de entrada.
        """
        print("Función 'al_seleccionar_listbox' ejecutada. (Implementar para cargar datos en campos)")
        # Aquí se debe implementar la lógica para cargar los datos del contacto seleccionado en los campos de entrada
        # Por ahora, solo muestra un mensaje de acción pendiente
        pass


    #Lógica de Crear, Editar y Eliminar Contactos, no implementada aún
    def al_crear_contacto(self):
        nombre = self.var_nombre.get()
        telefono = self.var_telefono.get()
        email = self.var_mail.get()
        cumpleanos = self.var_cumpleanos.get()
    
        if not nombre or not telefono or not email:
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
            return

    # Guardar en el diccionario
        ARCHIVO_CONTACTOS[nombre] = {
            "telefono": telefono,
            "email": email,
            "cumpleanos": cumpleanos
            }

        messagebox.showinfo("Éxito", f"Contacto '{nombre}' guardado correctamente.")
        print(f"Contacto '{nombre}' creado con éxito.")
        self.limpiar_campos() #Limpia los campos después de crear el contacto
        print(ARCHIVO_CONTACTOS) #Imprime el diccionario de contactos para verificar)
        self.cargar_contactos() #Recarga los contactos para actualizar la Listbox
        self.actualizar_mostrar_contactos() #Actualiza la Listbox con los nuevos contactos

    #Función para editar un contacto, no implementada aún
    def al_editar_contacto(self):
        """
        Esqueleto: Manejador para el botón 'Editar Contacto'.
       Hay que implementar la lógica de edición de un contacto.
       Por ahora, muestra un mensaje de acción pendiente.
        """
        messagebox.showinfo("Acción Pendiente", "Función 'Editar Contacto' debe ser implementada.")
        print("Función 'al_editar_contacto' ejecutada. (Implementar la lógica de edición)")
        pass

    #Función para eliminar un contacto
    def al_eliminar_contacto(self):
        """
        Manejador para el botón 'Eliminar Contacto'.
        Elimina el contacto seleccionado de la Listbox y de la lista en memoria,
        y guarda los cambios.
        """
        selected_indices = self.listbox_contactos.curselection()

        if not selected_indices:
            messagebox.showwarning("Advertencia", "Debe seleccionar un contacto para eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar eliminación", "¿Está seguro de que desea eliminar el contacto seleccionado?")
        if not confirm:
            return
        index_a_eliminar = selected_indices[0]
        nombre_contacto = self.contactos[index_a_eliminar]['nombre']
        del self.contactos[index_a_eliminar] # Elimina el contacto de la lista en memoria
        
        self.guardar_contactos() # Guarda los cambios en el archivo CSV
        self.actualizar_mostrar_contactos() # Actualiza la Listbox para que refleje la lista actualizada
        self.limpiar_campos() # Opcional: limpiar los campos después de eliminar

        messagebox.showinfo("Contacto eliminado", f"El contacto '{nombre_contacto}' fue eliminado exitosamente.")
#Elimina el contacto seleccionado de la Listbox y de la lista en memoria, y guarda los cambios.
       

        

    #Lógica de Búsqueda de Contactos IMPLEMENTADA
    def al_buscar_contacto(self):
        """
        Implementa la lógica de búsqueda de contactos.
        Filtra self.contactos y muestra los resultados en la Listbox.
        """
        termino_busqueda = self.var_busqueda.get().strip().lower() #Obtiene el texto del campo de búsqueda
        
        if not termino_busqueda: #Si el campo de búsqueda está vacío, muestra todos los contactos
            self.actualizar_mostrar_contactos(self.contactos)
            return

        contactos_encontrados = []
        for contacto in self.contactos:
            #Comprueba si el término de búsqueda está en nombre, teléfono o mail (no diferencia mayúsculas/minúsculas)
            if (termino_busqueda in contacto['nombre'].lower() or
                termino_busqueda in contacto['telefono'].lower() or
                termino_busqueda in contacto['mail'].lower()):
                contactos_encontrados.append(contacto)
        
        self.actualizar_mostrar_contactos(contactos_encontrados) #Actualiza la Listbox con los resultados
        
        if not contactos_encontrados:
            messagebox.showinfo("Búsqueda", "No se encontraron contactos que coincidan con la búsqueda.")
        print("Función 'al_buscar_contacto' ejecutada.")


    #Lógica de Alarma de Cumpleaños, no implementada aún
    # --- PARTE DEL GRUPO: Alarma de Cumpleaños ---
    def verificar_cumpleanos(self):
        """
        Esqueleto: Verifica si hay cumpleaños hoy y muestra una alarma.
        Hay que implementar la lógica de verificación de cumpleaños.
        Por ahora, muestra un mensaje de acción pendiente.
        """
        print("Función 'verificar_cumpleanos' ejecutada. (Implementar la lógica de alarma)")
        pass


#Punto de Entrada de la Aplicación
if __name__ == "__main__":
    ventana_principal = tk.Tk() #Crea la ventana principal de Tkinter
    app = GestorContactosApp(ventana_principal) #Instancia nuestra aplicación
    ventana_principal.mainloop() #Inicia el bucle principal de eventos de Tkinter
