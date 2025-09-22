import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # Necesitas instalar tkcalendar: pip install tkcalendar

class EventApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Eventos")
        self.root.geometry("700x400")

        # Frames
        self.frame_list = ttk.Frame(root)
        self.frame_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.frame_inputs = ttk.Frame(root)
        self.frame_inputs.pack(fill=tk.X, padx=10, pady=5)

        self.frame_buttons = ttk.Frame(root)
        self.frame_buttons.pack(fill=tk.X, padx=10, pady=5)

        # TreeView para eventos
        columns = ("fecha", "hora", "descripcion")
        self.tree = ttk.Treeview(self.frame_list, columns=columns, show="headings")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.column("fecha", width=100)
        self.tree.column("hora", width=80)
        self.tree.column("descripcion", width=400)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Scrollbar para TreeView
        scrollbar = ttk.Scrollbar(self.frame_list, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Campos de entrada con etiquetas
        ttk.Label(self.frame_inputs, text="Fecha:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_fecha = DateEntry(self.frame_inputs, date_pattern='yyyy-mm-dd')
        self.entry_fecha.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame_inputs, text="Hora (HH:MM):").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.entry_hora = ttk.Entry(self.frame_inputs, width=10)
        self.entry_hora.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(self.frame_inputs, text="Descripción:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.entry_descripcion = ttk.Entry(self.frame_inputs, width=40)
        self.entry_descripcion.grid(row=0, column=5, padx=5, pady=5)

        # Botones
        self.btn_agregar = ttk.Button(self.frame_buttons, text="Agregar Evento", command=self.agregar_evento)
        self.btn_agregar.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_eliminar = ttk.Button(self.frame_buttons, text="Eliminar Evento Seleccionado", command=self.eliminar_evento)
        self.btn_eliminar.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_salir = ttk.Button(self.frame_buttons, text="Salir", command=root.quit)
        self.btn_salir.pack(side=tk.RIGHT, padx=5, pady=5)

    def agregar_evento(self):
        fecha = self.entry_fecha.get()
        hora = self.entry_hora.get().strip()
        descripcion = self.entry_descripcion.get().strip()

        if not hora or not descripcion:
            messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos.")
            return

        # Validar formato de hora HH:MM
        if not self.validar_hora(hora):
            messagebox.showerror("Formato de hora inválido", "Ingrese la hora en formato HH:MM (24 horas).")
            return

        # Insertar en TreeView
        self.tree.insert("", tk.END, values=(fecha, hora, descripcion))

        # Limpiar campos
        self.entry_hora.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)

    def eliminar_evento(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Seleccionar evento", "Por favor, seleccione un evento para eliminar.")
            return

        respuesta = messagebox.askyesno("Confirmar eliminación", "¿Está seguro de eliminar el evento seleccionado?")
        if respuesta:
            for item in selected:
                self.tree.delete(item)

    def validar_hora(self, hora_str):
        try:
            partes = hora_str.split(":")
            if len(partes) != 2:
                return False
            h, m = int(partes[0]), int(partes[1])
            return 0 <= h < 24 and 0 <= m < 60
        except:
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = EventApp(root)
    root.mainloop()
