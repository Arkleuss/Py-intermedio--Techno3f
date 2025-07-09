from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import sys
import os


bg_color = "#5891A8"
bg_btn = "#CED4E0" 



class Clientes(tk.Frame):
    DB_NAME=os.path.join(os.path.dirname(__file__),"database.db")
    
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador =controlador
        self.widgets()
        self.cargar_clientes()
        
        
    def widgets(self):
        
        
        
        self.labelframe = tk.LabelFrame(self, text="Clientes", font="arial 20 bold", bg=bg_color)
        self.labelframe.place(x=20, y=20, width=250, height=560)
        
        lbl_nombre= tk.Label(self.labelframe, text="Nombre: ", font="arial 14 bold", bg=bg_color)
        lbl_nombre.place(x=10, y=20)
        self.entry_nombre =ttk.Entry(self.labelframe, font="arial 14 bold")
        self.entry_nombre.place(x=10, y=50, width=220, height=40)
        
        lbl_apellido= tk.Label(self.labelframe, text="Apellido: ", font="arial 14 bold", bg=bg_color)
        lbl_apellido.place(x=10, y=100)
        self.entry_apellido =ttk.Entry(self.labelframe, font="arial 14 bold")
        self.entry_apellido.place(x=10, y=130, width=220, height=40)
        
        lbl_mail= tk.Label(self.labelframe, text="Mail: ", font="arial 14 bold", bg=bg_color)
        lbl_mail.place(x=10, y=180)
        self.entry_mail =ttk.Entry(self.labelframe, font="arial 14 bold")
        self.entry_mail.place(x=10, y=210, width=220, height=40)
        
        ############# Combobox niveles
        
        conn = sqlite3.connect(self.DB_NAME)
        cur= conn.cursor()
        query_nivel= "SELECT * FROM niveles"
        params =[]
        cur.execute(query_nivel)
        datos_niveles =cur.fetchall()
        
        for i in datos_niveles:
            params.append(i[0])
        
        
        lbl_nivel= tk.Label(self.labelframe, text="Nivel: ", font="arial 14 bold", bg=bg_color)
        lbl_nivel.place(x=10, y=260)
        self.niveles =["Seleccionar nivel"] + params
        self.entry_nivel =ttk.Combobox(self.labelframe, font="arial 14 bold", state="readonly")
        self.entry_nivel.place(x=10, y=290, width=220, height=40)
        self.entry_nivel["values"]=self.niveles
        self.entry_nivel.bind("<<ComboboxSelected>>")
        
        btn_crear = Button(self.labelframe, fg="black", text="Crear", font="arial 16 bold", bg=bg_btn, command=self.registrar_cliente)
        btn_crear.place(x=10, y=400, width=220, height=40)
        
        btn_editar = Button(self.labelframe, fg="black", text="Editar", font="arial 16 bold", bg=bg_btn, command=self.editar_cliente)
        btn_editar.place(x=10, y=450, width=220, height=40)
        
        #######################################################################
        
        treFrame = Frame(self, bg="white")
        treFrame.place(x=280, y=20, width=800, height=560)
        
        scroll_y = ttk.Scrollbar(treFrame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        scroll_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        
        self.tre = ttk.Treeview(treFrame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, height=40, columns=("ID", "cliente", "nivel", "mail"), show="headings")
        self.tre.pack(expand=True, fill=BOTH)
        
        scroll_y.config(command=self.tre.yview)
        scroll_x.config(command=self.tre.xview)
        
        self.tre.heading("ID", text="ID")
        self.tre.heading("cliente", text="cliente")
        self.tre.heading("nivel", text="nivel")
        self.tre.heading("mail", text="mail")
        
        self.tre.column("ID", width=50, anchor="center")
        self.tre.column("cliente", width=200, anchor="center")
        self.tre.column("nivel", width=50, anchor="center")
        self.tre.column("mail", width=200, anchor="center")

    def validar_campos(self):
        if not self.entry_nombre.get() or not self.entry_apellido.get() or not self.entry_mail.get() or not self.entry_nivel.get():
            messagebox.showerror("Error", "Todos los campos son requeridos.")
            return False
        return True
    
    def registrar_cliente(self):
        if not self.validar_campos():
            return
        
        nombre = self.entry_nombre.get()
        apellido =self.entry_apellido.get()
        mail = self.entry_mail.get()
        nivel= self.entry_nivel.get()
        cliente = nombre + " " + apellido
        
        
        try:
            conn = sqlite3.connect(self.DB_NAME)
            cur= conn.cursor()
            cur.execute("INSERT INTO clientes (cliente, nivel, mail) VALUES (?,?,?)",
                        (cliente, nivel, mail))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Exito", "Cliente registrado correctamente")
            self.limpiar_treeview()
            self.limpiar_campos()
            self.cargar_clientes()
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el cliente: {e}")
            
    def cargar_clientes(self):
        try:
            conn = sqlite3.connect(self.DB_NAME)
            cur= conn.cursor()
            cur.execute("SELECT * FROM clientes")
            rows = cur.fetchall()
            for row in rows:
                self.tre.insert("", "end", values=row)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo cargar los registros: {e}")
            
    def limpiar_treeview(self):
        for item in self.tre.get_children():
            self.tre.delete(item)
        
    def limpiar_campos(self):
        self.entry_nombre.delete(0, END)
        self.entry_apellido.delete(0, END)
        self.entry_mail.delete(0, END)
        self.entry_nivel.current(0)
        
    def editar_cliente(self):
        if not self.tre.selection():
            messagebox.showerror("Error", "No se ha seleccionado cliente a editar")
            return
        cliente_seleccionado = self.tre.selection()[0]
        id_cliente = self.tre.item(cliente_seleccionado, "values")[0]
        
        nombre_actual = self.tre.item(cliente_seleccionado, "values")[1]
        nivel_actual = self.tre.item(cliente_seleccionado, "values")[2]
        mail_actual = self.tre.item(cliente_seleccionado, "values")[3]
        
        top_editar = Toplevel(self)
        top_editar.title("Editar Cliente")
        top_editar.geometry("400x250+500+200")
        top_editar.config(bg=bg_color)
        top_editar.resizable(False, False)
        top_editar.transient(self.master)
        top_editar.grab_set()
        top_editar.focus_set()
        top_editar.lift()
        
        tk.Label(top_editar, text="Cliente: ", font="arial 14 bold", bg=bg_color).place(x=20, y=20, width=80, height=25)
        nombre_nuevo = tk.Entry(top_editar, font="arial 14 bold")
        nombre_nuevo.insert(0, nombre_actual)
        nombre_nuevo.place(x=120, y=20, width=250, height=30)
        
        #################### Combobox niveles
        conn = sqlite3.connect(self.DB_NAME)
        cur= conn.cursor()
        query_nivel= "SELECT * FROM niveles"
        params =[]
        cur.execute(query_nivel)
        datos_niveles =cur.fetchall()
        
        for i in datos_niveles:
            params.append(i[0])
        
        
        
        tk.Label(top_editar, text="Nivel: ", font="arial 14 bold", bg=bg_color).place(x=20, y=60, width=80, height=25)
        self.niveles =["Seleccione Categoria"] + params
        self.nivel_nuevo = ttk.Combobox(top_editar, font="arial 14 bold", state="readonly")
        self.nivel_nuevo.insert(0, nivel_actual)
        self.nivel_nuevo.place(x=120, y=60, width=250, height=30)
        self.nivel_nuevo["values"]=self.niveles
        self.nivel_nuevo.bind("<<ComboboxSelected>>")
        
        
        tk.Label(top_editar, text="Mail: ", font="arial 14 bold", bg=bg_color).place(x=20, y=100, width=80, height=25)
        mail_nuevo = tk.Entry(top_editar, font="arial 14 bold")
        mail_nuevo.insert(0, mail_actual)
        mail_nuevo.place(x=120, y=100, width=250, height=30)
        
        def guardar_edicion():
            nuevo_nombre = nombre_nuevo.get()
            nuevo_nivel = self.nivel_nuevo.get()
            nuevo_mail = mail_nuevo.get()
            
            try:
                conn =sqlite3.connect(self.DB_NAME)
                cur =conn.cursor()
                cur.execute("UPDATE clientes SET cliente = ?, nivel= ?, mail= ? WHERE ID= ?",
                            (nuevo_nombre, nuevo_nivel, nuevo_mail, id_cliente))
                conn.commit()
                conn.close()
                messagebox.showinfo("Exito", "Cliente editado correctamente.")
                self.limpiar_treeview()
                self.cargar_clientes()
                top_editar.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al editar el cliente: {e}")
                
        btn_guardar = tk.Button(top_editar, text="Guardar Cambios", command=guardar_edicion, font="arial 14 bold", bg=bg_btn)
        btn_guardar.place(x=100, y=160, width=200, height=40)
        