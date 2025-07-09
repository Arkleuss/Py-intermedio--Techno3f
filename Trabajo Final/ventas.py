from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import datetime
import sys
import os
import threading

bg_color = "#5891A8"
bg_btn = "#CED4E0" 


class Ventas(tk.Frame):
    
    DB_NAME=os.path.join(os.path.dirname(__file__),"database.db")
    
    
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.numero_factura = self.obtener_numero_factura()
        self.productos_seleccionados = []
        self.cliente_seleccionado =[]
        self.controlador = controlador
        self.widgets()
        self.cargar_clientes_v()
        self.cargar_productos_v()
        self.timer_producto = None
        self.timer_clientes = None
        
    def obtener_numero_factura(self):
        try:
            conn = sqlite3.connect(self.DB_NAME)
            cur =conn.cursor()
            cur.execute("SELECT MAX(factura) FROM ventas")
            last_invoice_number = cur.fetchone()[0]
            conn.close()
            return last_invoice_number +1 if last_invoice_number is not None else 1 
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener numero de factura: {e}")
            return 1
        
        ###################################################################################
        
    def cargar_clientes_v(self):
        try:
            self.conn =sqlite3.connect(self.DB_NAME)
            self.cur = self.conn.cursor()
            self.cur.execute("""SELECT * FROM clientes  as c 
                            INNER JOIN niveles as n 
                            ON c.nivel = n.nivel;
                            """)
            self.clientes= [row[1] for row in self.cur.fetchall()]
            self.entry_cliente["values"] = self.clientes
            self.conn.close()
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error cargando clientes {e}")
            
    
    
    
    def actualizar_nivel(self, event =None):
        cliente_seleccionado = self.entry_cliente.get()
        
        try:
            self.conn = sqlite3.connect(self.DB_NAME)
            self.cur = self.conn.cursor()
            
            
            self.cur.execute("""SELECT * FROM clientes  as c 
                            INNER JOIN niveles as n 
                            ON c.nivel = n.nivel 
                            WHERE c.cliente = ? 
                            """, (cliente_seleccionado, ))
            datos_cliente =self.cur.fetchone()
            self.nivel =datos_cliente[4]
            self.descuento =datos_cliente[5]
            self.conn.close
            
            self.label_nivel.config(text=f"Nivel: {self.nivel} ")
            self.label_descuento.config(text= f"Descuento: {self.descuento} %")
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener nivel del cliente {e}")
            
    def filtrar_clientes(self, event):
        if self.timer_clientes:
            self.timer_clientes.cancel()
        self.timer_clientes = threading.Timer(0.5, self._filter_clientes)
        self.timer_clientes.start()
        
    def _filter_clientes(self):
        typed = self.entry_cliente.get()
        
        if typed == "":
            data = self.clientes
        else:
            data= [item for item in self.clientes if typed.lower() in item.lower()]
            
        if data:
            self.entry_cliente["values"] = data
            self.entry_cliente.event_generate("<Down>")
        else:
            self.entry_cliente["values"] = ["No se encontro cliente"]
            self.entry_cliente.event_generate("<Down>")
            self.entry_cliente.delete(0, tk.END)
        
        
    ##################################################################################
        
        
    def cargar_productos_v(self):
        try:
            self.conn =sqlite3.connect(self.DB_NAME)
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT producto FROM productos")
            self.productos= [row[0] for row in self.cur.fetchall()]
            self.entry_producto["values"] = self.productos
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error cargando productos {e}")
            
    def filtrar_productos(self, event):
        if self.timer_producto:
            self.timer_producto.cancel()
        self.timer_producto = threading.Timer(0.5, self._filter_products)
        self.timer_producto.start()
        
    def _filter_products(self):
        typed = self.entry_producto.get()
        
        if typed == "":
            data = self.productos
        else:
            data= [item for item in self.productos if typed.lower() in item.lower()]
            
        if data:
            self.entry_producto["values"] = data
            self.entry_producto.event_generate("<Down>" )
        else:
            self.entry_producto["values"] = ["No se encontraron resultados"]
            self.entry_producto.event_generate("<Down>")
            self.entry_producto.delete(0, tk.END)
        
    #########################################
        
    def agregar_producto_v(self):
        cliente = self.entry_cliente.get()
        producto= self.entry_producto.get()
        cantidad = self.entry_cantidad.get()
        
        
        if not cliente:
            messagebox.showerror("Error", "Seleccionar cliente")
            
        if not producto:
            messagebox.showerror("Error", "Seleccionar producto")
            
        if not cantidad.isdigit() or int(cantidad) <=0:
            messagebox.showerror("Error", "Seleccione cantidad valida")
            return
        cantidad= int(cantidad)
        cliente= self.entry_cliente.get()
        
        try:
            self.conn = sqlite3.connect(self.DB_NAME)
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT precio, stock FROM productos WHERE producto=?", (producto,))
            resultado =self.cur.fetchone()
            
            if resultado is None:
                messagebox.showerror("Error", "Producto no encontrado")
                return
            precio, stock = resultado
            
            if cantidad>stock:
                messagebox.showerror("Error", f"Stock insuficiente: {stock} unidades disponibles")
                
            total = precio * cantidad
            total_cop ="{:,.0f}".format(total)
            
            
            self.tre.insert("", "end", values=(self.numero_factura, cliente, producto, "{:,.0f}".format(precio), cantidad, total_cop))
            self.productos_seleccionados.append((self.numero_factura, cliente, producto, "{:,.0f}".format(precio), cantidad, total_cop))
            
            self.conn.close()
            
            self.entry_producto.set("")
            self.entry_cantidad.delete(0, "end")
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al agregar producto {e}")
            
        self.calcular_precio_total()
        
    def calcular_precio_total(self):
        total_pagar = sum(float(str(self.tre.item(item)["values"][-1]).replace(" ","").replace(",","")) for item in self.tre.get_children())
        total_pagar_cop = "{:,.0f}".format(total_pagar)
        self.monto_descuento = (total_pagar * self.descuento) /100
        self.monto_final = total_pagar - self.monto_descuento
        self.label_subtotal.config(text=f"Subtotal: $ {total_pagar}")
        self.label_monto_descuento.config(text=f"Descuento: $ {self.monto_descuento}")
        self.label_precio_total.config(text=f"Precio a pagar: $ {self.monto_final}")
    
    def actualizar_stock(self, event =None):
        producto_seleccionado = self.entry_producto.get()
        
        
        try:
            self.conn = sqlite3.connect(self.DB_NAME)
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT * FROM productos WHERE producto=?", (producto_seleccionado,))
            datos =self.cur.fetchone()
            
            precio = datos[2]
            stock = datos[3]
            self.conn.close
            
            self.label_stock.config(text=f"Stock: {stock:.0f}")
            self.label_precio.config(text=f"Precio: {precio:.2f}")
        except sqlite3.Error as e:
            messagebox.showerror("Error", "Error al obtener stock del producto ", e)
            
    def finalizar_venta(self):
        if not self.tre.get_children():
            messagebox.showerror("Error", "No se seleccionaron productos")
            
        #total_venta= sum(float(item[5].replace(" ","").replace(",","")) for item in self.productos_seleccionados)
        total_venta = self.monto_final
        #total_cop = "{:,.0f}".format(total_venta)
        
        ventana_pago =tk.Toplevel(self)
        ventana_pago.title("Finalizar venta")
        ventana_pago.geometry("400x400+450+80")
        ventana_pago.config(bg=bg_color)
        ventana_pago.resizable(False, False)
        ventana_pago.transient(self.master)
        ventana_pago.grab_set()
        ventana_pago.focus_set()
        ventana_pago.lift()
            
        label_titulo =tk.Label(ventana_pago, text="Realizar venta", font="arial 30 bold", bg=bg_color)
        label_titulo.place(x=70, y=10)
        
        label_total =tk.Label(ventana_pago, text=f"Total: {self.monto_final}", font="arial 14 bold", bg=bg_color)
        label_total.place(x=80, y=100)
        
        btn_confirmar = tk.Button(ventana_pago, text="Confirmar", font="arial 14 bold", command=lambda: self.procesar_venta(ventana_pago, total_venta))
        btn_confirmar.place(x=80, y=270, width=240, height=40)
        
    def procesar_venta(self, ventana_pago, total_venta):
        total_venta=float(total_venta)
        cliente= self.entry_cliente.get()
        
        try:
            self.conn =sqlite3.connect(self.DB_NAME)
            self.cur = self.conn.cursor()
            
            fecha = datetime.datetime.now().strftime("%Y-%m-%d")
            
            for item in self.productos_seleccionados:
                factura, cliente, producto, precio, cantidad, total = item
                self.cur.execute("INSERT INTO ventas (factura, cliente, total, fecha) VALUES (?,?,?,?)",
                                (factura, cliente,  total_venta, fecha))
                """.replace(" ", "").replace(",","")"""
                self.cur.execute("UPDATE productos SET stock = stock - ? WHERE producto = ?", (cantidad, producto))
                                
                messagebox.showinfo("", "Venta realizada con exito")
            self.conn.commit()
            self.conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al registrar venta: {e}")
            
        self.numero_factura +=1
        self.label_nro_factura.config(text=str(self.numero_factura))
        self.productos_seleccionados =[]
        self.limpiar_campos()
        
        ventana_pago.destroy()
        
    def limpiar_campos(self):
        for item in self.tre.get_children():
            self.tre.delete(item)
        self.label_precio_total.config(text="Monto final: $ 0")
        self.label_subtotal.config(text="Subtotal: $ 0 ")
        self.label_monto_descuento.config(text="Descuento: $ 0 ") 
        
        self.entry_cliente.set("")
        self.entry_producto.set("")
        self.entry_cantidad.delete(0, "end")
        
    def limpiar_lista(self):
        self.tre.delete(*self.tre.get_children())
        self.productos_seleccionados.clear()
        self.calcular_precio_total
        self.label_precio_total.config(text="Monto final: $ 0")
        self.label_subtotal.config(text="Subtotal: $ 0 ")
        self.label_monto_descuento.config(text="Descuento: $ 0 ") 
        
    def eliminar_producto_lista(self):
        item_seleccionado = self.tre.selection()
        if not item_seleccionado:
            messagebox.showerror("Error", "No hay ningun articulo seleccionado")
            return
        
        item_id = item_seleccionado[0]
        valores_item = self.tre.item(item_id)["values"]
        
        factura, cliente, producto, precio, cantidad, total = valores_item
        
        self.tre.delete(item_id)
        
        self.productos_seleccionados = [producto for productos in self.productos_seleccionados if productos[2] != producto]
        
        self.calcular_precio_total()
        
    def editar_producto_lista(self):
        selected_item = self.tre.selection()
        if not selected_item:
            messagebox.showerror("Error", "No hay ningun articulo seleccionado ")
            return
        item_values = self.tre.item(selected_item[0], "values")
        if not item_values:
            return
        
        current_product =item_values[2]
        current_cantidad = item_values[4]
        
        new_cantidad= simpledialog.askinteger("Editar articulo", "ingresar nueva cantidad", initialvalue =current_cantidad)
        
        if new_cantidad is not None:
            try:
                self.conn = sqlite3.connect(self.DB_NAME)
                self.cur= self.conn.cursor()
                self.cur.execute("SELECT precio, stock FROM productos WHERE producto =?", (current_product,))
                resultado= self.cur.fetchone()
                
                if resultado is None:
                    messagebox.showerror("Error", "Producto no encontrado")
                    
                precio, stock = resultado
                
                if new_cantidad > stock:
                    messagebox.showerror("Error", f"Stock insuficiente. Solo hay {stock} unidades disponibles")
                    return
                
                total = precio* new_cantidad
                
                self.tre.item(selected_item[0], values=(self.numero_factura, self.entry_cliente.get(), current_product, precio, new_cantidad, total))
                
                for idx, producto in enumerate(self.productos_seleccionados):
                    if producto[2]==current_product:
                        self.productos_seleccionados[idx] =(self.numero_factura, self.entry_cliente.get(),current_product, precio, new_cantidad, total)
                        break
                self.conn.close()
                
                self.calcular_precio_total()
                
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al editar el articulo {e}")
                    
        
    def widgets(self):
        
        labelframe = tk.LabelFrame(self, font="arial 12 bold", bg=bg_color)
        labelframe.place(x=25, y=30, width=1045, height=180)
        
        label_cliente = tk.Label(labelframe, text="Cliente: ", font="arial 14 bold", bg=bg_color)
        label_cliente.place(x=10, y=11)
        self.entry_cliente= ttk.Combobox(labelframe, font="arial 14 bold")
        self.entry_cliente.place(x=120, y=8, width=260, height=40)
        self.entry_cliente.bind("<KeyRelease>", self.filtrar_clientes)
        self.entry_cliente.bind("<<ComboboxSelected>>", self.actualizar_nivel)
        
        
        label_producto = tk.Label(labelframe, text="Producto: ", font="arial 14 bold", bg=bg_color)
        label_producto.place(x=10, y=70)
        self.entry_producto= ttk.Combobox(labelframe, font="arial 14 bold",)
        self.entry_producto.place(x=120, y=60, width=260, height=40)
        self.entry_producto.bind("<KeyRelease>", self.filtrar_productos)
        self.entry_producto.bind("<<ComboboxSelected>>", self.actualizar_stock)
        
        label_cantidad = tk.Label(labelframe, text="Cantidad: ", font="arial 14 bold", bg=bg_color)
        label_cantidad.place(x=400, y=11)
        self.entry_cantidad= ttk.Entry(labelframe, font="arial 14 bold")
        self.entry_cantidad.place(x=510, y=8, width=100, height=40)
        
        self.label_stock = tk.Label(labelframe, text="Stock: ", font="arial 14 bold", bg=bg_color)
        self.label_stock.place(x=400, y=70)
        
        self.label_precio =tk.Label(labelframe, text="Precio: ", font="arial 14 bold", bg=bg_color)
        self.label_precio.place(x=550, y=70)
        
        self.label_factura =tk.Label(labelframe, text="Factura Nro: ", font="arial 14 bold", bg=bg_color)
        self.label_factura.place(x=750, y=11)
        self.label_nro_factura =tk.Label(labelframe, text=f"{self.numero_factura}", font="arial 14 bold", bg=bg_color)
        self.label_nro_factura.place(x=870, y=11)

        self.label_nivel =tk.Label(labelframe, text="Nivel: ", font="arial 14 bold", bg=bg_color)
        self.label_nivel.place(x=750, y=70)
        
        self.label_descuento =tk.Label(labelframe, text="Descuento: ", font="arial 14 bold", bg=bg_color)
        self.label_descuento.place(x=850, y=70)
        
        
        
        btn_agregar = tk.Button(labelframe, text="Agregar producto", font=" arial 14 bold", bg=bg_btn, command=self.agregar_producto_v)
        btn_agregar.place(x=90, y=120, width=200, height=40)
        
        btn_eliminar = tk.Button(labelframe, text="Eliminar producto", font=" arial 14 bold", bg=bg_btn, command=self.eliminar_producto_lista)
        btn_eliminar.place(x=300, y=120, width=200, height=40)
        
        btn_editar = tk.Button(labelframe, text="Editar producto", font=" arial 14 bold", bg=bg_btn, command=self.editar_producto_lista)
        btn_editar.place(x=510, y=120, width=200, height=40)
        
        btn_limpiar = tk.Button(labelframe, text="Limpiar lista", font=" arial 14 bold", bg=bg_btn, command=self.limpiar_lista)
        btn_limpiar.place(x=720, y=120, width=200, height=40)
        
        #######################################################
        
        treFrame = tk.Frame(self, bg="white")
        treFrame.place(x=70, y=220, width=980, height=300)
        
        scroll_y = ttk.Scrollbar(treFrame)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        scroll_x = ttk.Scrollbar(treFrame, orient= HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        
        self.tre = ttk.Treeview(treFrame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, height=40, columns=("Factura", "Cliente", "Producto", "Precio", "Cantidad", "Total"), show="headings")
        self.tre.pack(expand=True, fill=BOTH)
        
        scroll_y.config(command=self.tre.yview)
        scroll_x.config(command=self.tre.xview)
        
        self.tre.heading("Factura", text="Factura") 
        self.tre.heading("Cliente", text="Cliente") 
        self.tre.heading("Producto", text="Producto") 
        self.tre.heading("Precio", text="Precio") 
        self.tre.heading("Cantidad", text="Cantidad") 
        self.tre.heading("Total", text="Total") 
        
        self.tre.column("Factura", width=70, anchor="center")
        self.tre.column("Cliente", width=250, anchor="center")
        self.tre.column("Producto", width=250, anchor="center")
        self.tre.column("Precio", width=120, anchor="center")
        self.tre.column("Cantidad", width=120, anchor="center")
        self.tre.column("Total", width=150, anchor="center")
        
        
        btn_finalizar= tk.Button(self, text="Finalizar", font="arial 14 bold", bg=bg_btn, command=self.finalizar_venta)
        btn_finalizar.place(x=70, y=550, width=180, height=40)
        
        self.label_subtotal =tk.Label(self, text="Subtotal: $ 0 ", font="arial 14 ", bg=bg_color)
        self.label_subtotal.place(x=400, y=555)
        
        self.label_monto_descuento =tk.Label(self, text="Descuento: $ 0 ", font="arial 14 ", bg=bg_color)
        self.label_monto_descuento.place(x=610, y=555)
        
        self.label_precio_total =tk.Label(self, text="Monto final: $ 0 ", font="arial 14 bold", bg=bg_color)
        self.label_precio_total.place(x=820, y=555)
        
        
        