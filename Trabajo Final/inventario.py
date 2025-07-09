from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import sys
import os
from PIL import Image, ImageTk
import threading

bg_btn = "#CED4E0" 

DB_NAME=os.path.join(os.path.dirname(__file__),"database.db")
bg_color = "#5891A8"


class Inventario(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador= controlador
        self.widgets()
        self.productos_combobox()
        self.cargar_productos()
        self.timer_productos =None
        
        self.image_folder = "img"
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)
        
        
    def widgets(self):
        #========================================================================================
        canvas_productos = tk.LabelFrame(self, text="Productos", font="Arial 14 bold", bg= bg_color ) #contenedor de canvas y scrollbar
        canvas_productos.place(x=300, y=10, width=780, height= 580)
        
        self.canvas = tk.Canvas(canvas_productos, bg="white" )
        self.scrollbar = tk.Scrollbar(canvas_productos, orient="vertical", command=self.canvas.yview ) #scrollbar vertical
        self.scrollable_frame = tk.Frame(self, bg="white")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        #========================================================================================
        
        lblframe_buscar= LabelFrame(self, text="Buscar", font="arial 14 bold", bg=bg_color)
        lblframe_buscar.place(x=10, y=10, width=280, height=80)
        
        self.comboboxbuscar = ttk.Combobox(lblframe_buscar, font="arial 12")
        self.comboboxbuscar.place(x=5, y=5, width=260, height=40)
        self.comboboxbuscar.bind("<<ComboboxSelected>>", self.on_combobox_event)
        self.comboboxbuscar.bind("<KeyRelease>", self.filtrar_productos)
        
        #========================================================================================
        lblframe_seleccion =LabelFrame(self, text="Seleccion", font="arial 14 bold", bg=bg_color )
        lblframe_seleccion.place(x=10, y=95, width=280, height=190)
        
        self.label1= tk.Label(lblframe_seleccion, text="ID", font="arial 12", bg=bg_color,)
        self.label1.place(x=5, y=5)
        
        self.label2= tk.Label(lblframe_seleccion, text="Producto", font="arial 12", bg=bg_color, wraplength=300)
        self.label2.place(x=5, y=35)
        
        self.label3= tk.Label(lblframe_seleccion, text="Precio", font="arial 12", bg=bg_color,)
        self.label3.place(x=5, y=70)
        
        self.label4= tk.Label(lblframe_seleccion, text="Stock", font="arial 12", bg=bg_color,)
        self.label4.place(x=5, y=100)
        
        self.label5= tk.Label(lblframe_seleccion, text="Categoria", font="arial 12", bg=bg_color,)
        self.label5.place(x=5, y=130)
        #========================================================================================
        
        lblframe_opciones= LabelFrame(self, bg=bg_color, text="Opciones", font="arial 14 bold")
        lblframe_opciones.place(x=10, y=290, width=280, height=300)
        
        btn1= tk.Button(lblframe_opciones, text="Agregar", font="arial 14 bold", bg=bg_btn, command=self.agregar_producto)
        btn1.place(x=20, y=20, width=180, height=40)
        
        btn2= tk.Button(lblframe_opciones, text="Editar", font="arial 14 bold", bg=bg_btn, command=self.editar_producto)
        btn2.place(x=20, y=80, width=180, height=40)
        
        btn3= tk.Button(lblframe_opciones, text="Eliminar", font="arial 14 bold", bg=bg_btn, command=self.eliminar_producto)
        btn3.place(x=20, y=140, width=180, height=40)
        
        
    def load_image(self):
        file_path =filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
            image = image.resize((200,200), Image.LANCZOS)
            image_name =os.path.basename(file_path)
            image_save_path = os.path.join(self.image_folder, image_name)
            image.save(image_save_path)
            
            self.image_tk = ImageTk.PhotoImage(image)
            
            self.product_image = self.image_tk
            self.image_path = image_save_path
            
            img_label =tk.Label(self.frameimg, image= self.image_tk)
            img_label.place(x=0, y=0, width= 200, height=200)
        
    def productos_combobox(self):
        self.conn =sqlite3.connect(DB_NAME)
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT producto FROM productos")
        self.productos = [row[0] for row in self.cur.fetchall()]
        self.comboboxbuscar["values"]= self.productos
        
    
    
    def agregar_producto(self):
        top =tk.Toplevel(self)
        top.title("Agregar Producto")
        top.geometry("700x400+200+50")
        top.config(bg=bg_color)
        top.resizable(False, False)
        
        #posiciona la ventana emergente encima de la principal y bloquea la principal hasta que no se cierre la emergente 
        top.transient(self.master) 
        top.grab_set()
        top.focus_set()
        top.lift()
        
        tk.Label(top, text="Producto:", font="arial 12 bold", bg=bg_color).place(x=20, y=20,width=80, height=25)
        entry_producto = ttk.Entry(top, font="arial 12 bold")
        entry_producto.place(x=120, y=20, width=250, height=30)
        
        tk.Label(top, text="Precio:", font="arial 12 bold", bg=bg_color).place(x=20, y=60,width=80, height=25)
        entry_precio = ttk.Entry(top, font="arial 12 bold")
        entry_precio.place(x=120, y=60, width=250, height=30)
        
        tk.Label(top, text="Stock:", font="arial 12 bold", bg=bg_color).place(x=20, y=100,width=80, height=25)
        entry_stock = ttk.Entry(top, font="arial 12 bold")
        entry_stock.place(x=120, y=100, width=250, height=30)
        
        query_cat= "SELECT * FROM categorias"
        params =[]
        self.cur.execute(query_cat)
        datos_categorias =self.cur.fetchall()
        
        for i in datos_categorias:
            params.append(i[1])
        
        
        tk.Label(top, text="Categoria:", font="arial 12 bold",bg=bg_color).place(x=20, y=140,width=80, height=25)
        
        #entry_categoria.bind("<<ComboboxSelected>>", obtener_categoria)
        self.categorias =["Seleccione Categoria"] + params
        self.entry_categoria =ttk.Combobox(top, font="arial 12 bold", state="readonly", )
        self.entry_categoria.place(x=120, y=140, width=250, height=30)
        self.entry_categoria["values"]=self.categorias
        self.entry_categoria.current(0)
        self.entry_categoria.bind("<<ComboboxSelected>>")
        
        self.frameimg = tk.Frame(top,bg="white", highlightbackground="gray", highlightthickness=1)
        self.frameimg.place(x=440, y=30, width=200, height=200)
        
        btnimage= tk.Button(top, text="Cargar Imagen", font="arial 12 bold", bg=bg_btn, command=self.load_image)
        btnimage.place(x=470, y=260, width=150, height=40)
        
        
            
        def guardar_producto():
            producto = entry_producto.get()
            precio = entry_precio.get()
            stock = entry_stock.get()
            categoria = self.entry_categoria.current()
            
            
            if not producto or not precio or not stock or not categoria:
                messagebox.showerror("Error", "Completar TODOS los campos")
                return
            try:
                precio =float(precio)
                stock =int(stock)
                categoria =int(categoria)
            except ValueError:
                messagebox.showerror("Error", f"Precio y Stock deben ser numeros {categoria}")
                return
            
            if hasattr(self, "image_path"):
                image_path =self.image_path
            else:
                image_path =(r"Trabajo Final/img/default.png")
                
            try:
                self.cur.execute("INSERT INTO  productos (producto, precio, stock, categoria, imagen_path) VALUES (?, ?, ?, ?, ?)",
                                (producto, precio, stock, categoria, image_path))
                self.conn.commit()
                messagebox.showinfo("Exito", "Producto agregado correctamente")
                top.destroy()
                self.cargar_productos()
                self.productos_combobox()
            except sqlite3.Error as e:
                print("Error al cargar el producto:", e)
                messagebox.showerror("Error", "Error al cargar producto")
                
        tk.Button(top, text="Guardar", font="arial 12 bold",bg=bg_btn,  command=guardar_producto).place(x=50, y=260, width=150, height=40)
        tk.Button(top, text="Cancelar", font="arial 12 bold", bg=bg_btn, command=top.destroy).place(x=260, y=260, width=150, height=40)
        
    def cargar_productos(self, filtro=None, cat=None):
        self.after(0, self._cargar_productos, filtro, cat)
        
    def _cargar_productos(self, filtro= None, cat= None):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        query="SELECT producto, precio, imagen_path FROM productos "
        params =[]
        
        if filtro:
            query += " WHERE producto LIKE ?"
            params.append(f"%{filtro}%")
            
        self.cur.execute(query, params)
        productos = self.cur.fetchall()
        
        self.row =0
        self.column=0
        
        for producto, precio, image_path in productos:
            self.mostrar_productos(producto, precio, image_path)
        
    def mostrar_productos(self, producto, precio, image_path):
        producto_frame = tk.Frame(self.scrollable_frame, bg="white", relief="solid")
        producto_frame.grid(row= self.row, column=self.column, padx=10, pady=10)
        
        dir =os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(dir, image_path)
        if image_path and os.path.exists(image_path):
            image = Image.open(image_path)
            image= image.resize((150,150), Image.LANCZOS)
            imagen = ImageTk.PhotoImage(image)
            image_label= tk.Label(producto_frame, image=imagen)
            image_label.image = imagen
            image_label.pack(expand=True, fill="both")
            
        name_label =tk.Label(producto_frame, text=producto, bg="white", anchor="w", wraplength=150, font="arial 10 bold")
        name_label.pack(side="top", fill="x")
        
        precio_label =tk.Label(producto_frame, text= f"Precio: {precio:.2f}", bg="white", anchor="w", wraplength=150, font="arial 8")
        precio_label.pack(side="bottom", fill="x")
            
        self.column += 1
        if self.column > 3:
            self.column = 0
            self.row += 1
            
    def on_combobox_event(self, event):
        self.actualizar_label()
        
    def actualizar_label(self, event=None):
        producto_seleccionado =self.comboboxbuscar.get()
        
        try:
            self.cur.execute("""SELECT * FROM productos as p 
                            INNER JOIN categorias as c
                            ON p.categoria = c.id
                            WHERE producto=?""", (producto_seleccionado,))
            resultado= self.cur.fetchone()
            
            if resultado is not None:
                
                id = resultado[0]
                producto =resultado[1]
                precio = resultado[2] 
                stock = resultado[3] 
                categoria = resultado[7]
                
                
                
                self.label1.config(text=f"ID: {id}")
                self.label2.config(text=f"Producto: {producto}")
                self.label3.config(text=f"Precio: {precio}")
                self.label4.config( text=f"Stock: {stock:.0f}")
                self.label5.config(text=f"Categoria: {categoria}")
                
            else:
                self.label1.config(text=f"ID: No encontrado")
                self.label2.config(text=f"Producto: No encontrado")
                self.label3.config(text=f"Precio: No encontrado")
                self.label4.config( text=f"Stock: No encontrado")
                self.label5.config(text=f"Categoria: No encontrado")
                
                
        except sqlite3.Error as e:
            print("Error al obtener producto:", e)
            messagebox.showerror("Error", "Error al obtener datos del producto")
            
            
    """
    def filtrar_articulos(self,event):
        if self.timerarticulos:
            self.after_cancel(self.timerarticulos)
        self.timerarticulos = self.after(500, self._filterarticulos)
    """
    def filtrar_productos(self, event):
        if self.timer_productos:
            self.timer_productos.cancel()
        self.timer_productos = threading.Timer(0.5, self._filter_productos)
        self.timer_productos.start()
            
    def _filter_productos(self):
        typed= self.comboboxbuscar.get()
        
        if typed =="":
            data = self.productos
        else:
            data = [item for item in self.productos if typed.lower() in item.lower()]
            
        if data:
            self.comboboxbuscar["values"] = data
            self.comboboxbuscar.event_generate("<Down>")
        else:
            self.comboboxbuscar["values"] = ["No se encontraron resultados "]
            self.comboboxbuscar.event_generate("<Down>")
            
        self.cargar_productos(filtro=typed)
        
        
    def editar_producto(self):
        selected_item = self.comboboxbuscar.get()
        
        if not selected_item:
            messagebox.showerror("Error", "Seleccionar un producto a editar")
            return
        
        self.cur.execute("""SELECT * FROM productos as p
                        INNER JOIN categorias as c
                        ON p.categoria = c.id
                        WHERE producto = ? """, (selected_item, ))
        resultado = self.cur.fetchone()
        
        if not resultado:
            messagebox.showerror("Error", "Articulo no encontrado")
            return
        
        top = tk.Toplevel(self)
        top.title("Editar producto")
        top.geometry("700x400+200+50")
        top.config(bg=bg_color)
        top.resizable(False,False)
        
        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()
        
        #(producto, precio, stock, categoria, image_path) = resultado
        
        
        producto =resultado[1]
        precio = resultado[2] 
        stock = resultado[3] 
        categoria = resultado[7]
        image_path =resultado[5]
        
        tk.Label(top, text="Producto:", font= "arial 12 bold", bg=bg_color).place(x=20, y=20, width=80, height=25)
        entry_producto= ttk.Entry(top, font="arial 12 bold")
        entry_producto.place(x=120, y=20, width=250, height=30)
        entry_producto.insert(0, producto)

        tk.Label(top, text="Precio:", font= "arial 12 bold", bg=bg_color).place(x=20, y=60, width=80, height=25)
        entry_precio= ttk.Entry(top, font="arial 12 bold")
        entry_precio.place(x=120, y=60, width=250, height=30)
        entry_precio.insert(0, precio)
        
        tk.Label(top, text="Stock:", font= "arial 12 bold", bg=bg_color).place(x=20, y=100, width=80, height=25)
        entry_stock= ttk.Entry(top, font="arial 12 bold")
        entry_stock.place(x=120, y=100, width=250, height=30)
        entry_stock.insert(0, f"{stock:.0f}")
        
        
        query_cat= "SELECT * FROM categorias"
        params =[]
        self.cur.execute(query_cat)
        datos_categorias =self.cur.fetchall()
        
        for i in datos_categorias:
            params.append(i[1])
        
        tk.Label(top, text="Categoria:", font= "arial 12 bold", bg=bg_color).place(x=20, y=140, width=80, height=25)
        """
        entry_categoria= ttk.Combobox( top, font="arial 12 bold", values= params, state="readonly")
        entry_categoria.place(x=120, y=140, width=250, height=30)
        entry_categoria.insert(0, categoria)
        """
        self.categorias =["Seleccione Categoria"] + params
        self.entry_categoria =ttk.Combobox(top, font="arial 12 bold", state="readonly", )
        self.entry_categoria.place(x=120, y=140, width=250, height=30)
        self.entry_categoria["values"]=self.categorias
        self.entry_categoria.current(0)
        self.entry_categoria.bind("<<ComboboxSelected>>")
        
        
        self.frameimg = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1)
        self.frameimg.place(x=440, y=30, width=200, height=200)
        
        dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(dir, image_path)
        if image_path and os.path.exists(image_path):
            image= Image.open(image_path)
            image = image.resize((200,200), Image.LANCZOS)
            self.product_image= ImageTk.PhotoImage(image)
            self.image_path= image_path
            image_label =tk.Label(self.frameimg, image=self.product_image)
            image_label.pack(expand=True, fill ="both")
            
        btnimagen = tk.Button(top, text="Cargar imagen", font="arial 12 bold", command=self.load_image)
        btnimagen.place(x=470, y=260, width=150, height=40)
        
        def guardar_edicion():
            nuevo_producto = entry_producto.get()
            nuevo_precio = entry_precio.get()
            nuevo_stock = entry_stock.get()
            nueva_categoria =self.entry_categoria.current()
            
            for i in datos_categorias:
                if i[1] == nueva_categoria:
                    nueva_categoria= i[0]
                    
            
            #nueva_categoria = nueva_categoria[0]
            
            if not nuevo_producto or not nuevo_precio or not nuevo_stock or not nueva_categoria:
                messagebox.showerror("Error", "Todos los campos deben ser completados")
                return
            
            try:
                nuevo_precio = float(nuevo_precio)
                nuevo_stock = int(nuevo_stock)
            except ValueError:
                messagebox.showerror("Error", "Precio, y stock deben ser numeros validos")
                
            if hasattr(self, "image_path"):
                image_path =self.image_path
            else:
                image_path =(r"/Trabajo Final/img/default.png")
                
            self.cur.execute("UPDATE productos SET producto =?, precio=?, stock=?, categoria=?, imagen_path=? WHERE producto=? ",
                            (nuevo_producto, nuevo_precio, nuevo_stock, nueva_categoria, image_path, selected_item, ))
            self.conn.commit()
            
            self.productos_combobox()
            
            self.after(0,lambda: self.cargar_productos(filtro=nuevo_producto))
            
            top.destroy()
            messagebox.showinfo("Exito", "Producto editado correctamente")
            
        btn_guardar = tk.Button(top, text="Guardar", font="arial 12 bold", command=guardar_edicion)
        btn_guardar.place(x=260, y=260, width=150, height=40)
                
    def eliminar_producto(self):
        selected_item = self.comboboxbuscar.get()
        
        if not selected_item:
            messagebox.showerror("Error", "Seleccionar un producto a eliminar")
            return
        
        self.cur.execute("""SELECT * FROM productos as p
                        INNER JOIN categorias as c
                        ON p.categoria = c.id
                        WHERE producto = ? """, (selected_item, ))
        resultado = self.cur.fetchone()
        
        if not resultado:
            messagebox.showerror("Error", "Articulo no encontrado")
            return
        
        self.top = tk.Toplevel(self)
        self.top.title("Eliminar producto")
        self.top.geometry("700x400+200+50")
        self.top.config(bg=bg_color)
        self.top.resizable(False,False)
        
        self.top.transient(self.master)
        self.top.grab_set()
        self.top.focus_set()
        self.top.lift()
        
        producto =resultado[1]
        precio = resultado[2] 
        stock = resultado[3] 
        categoria = resultado[7]
        image_path =resultado[5]
        
        tk.Label(self.top, text="Producto:", font= "arial 12 bold", bg=bg_color).place(x=20, y=20, width=80, height=25)
        entry_producto= tk.Label(self.top, font="arial 12 bold", text=producto, bg="white", highlightthickness=1)
        entry_producto.place(x=120, y=20, width=250, height=30)
        

        tk.Label(self.top, text="Precio:", font= "arial 12 bold", bg=bg_color).place(x=20, y=60, width=80, height=25)
        entry_precio= tk.Label(self.top, font="arial 12 bold", text=precio, bg="white", highlightthickness=1)
        entry_precio.place(x=120, y=60, width=250, height=30)
        
        
        tk.Label(self.top, text="Stock:", font= "arial 12 bold", bg=bg_color).place(x=20, y=100, width=80, height=25)
        entry_stock= tk.Label(self.top, font="arial 12 bold", text=stock, bg="white", highlightthickness=1)
        entry_stock.place(x=120, y=100, width=250, height=30)
        
        tk.Label(self.top, text="Categoria:", font= "arial 12 bold", bg=bg_color).place(x=20, y=140, width=80, height=25)
        self.entry_categoria =tk.Label(self.top, font="arial 12 bold", text=categoria, bg="white", highlightthickness=1)
        self.entry_categoria.place(x=120, y=140, width=250, height=30)
        
        self.frameimg = tk.Frame(self.top, bg="white", highlightbackground="gray", highlightthickness=1)
        self.frameimg.place(x=440, y=30, width=200, height=200)
        
        if image_path and os.path.exists(image_path):
            image= Image.open(image_path)
            image = image.resize((200,200), Image.LANCZOS)
            self.product_image= ImageTk.PhotoImage(image)
            self.image_path= image_path
            image_label =tk.Label(self.frameimg, image=self.product_image)
            image_label.pack(expand=True, fill ="both")
            
        
        
        def _eliminar_producto():
            
            respuesta = messagebox.askyesno("Eliminar", "¿Quiere eliminar el producto?")
            if respuesta:
                conn =sqlite3.connect(DB_NAME)
                cur = conn.cursor()
                cur.execute("DELETE FROM productos WHERE producto = ?", (selected_item, ))
                conn.commit()
                self.productos_combobox()
                self.after(0,lambda: self.cargar_productos())
                self.top.destroy()
                messagebox.showinfo("Exito", "Producto eliminado correctamente")
            else:
                messagebox.showinfo("Cancelado", "El producto NO ha sido eliminado")
                self.top.destroy()
        btn_eliminar = tk.Button(self.top, text="Eliminar producto", font="arial 12 bold", command=_eliminar_producto)
        btn_eliminar.place(x=260, y=260, width=150, height=40)