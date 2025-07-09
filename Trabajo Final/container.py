from tkinter import *
import tkinter as tk
from ventas import Ventas
from clientes import Clientes
from inventario import Inventario
import sys
import os

bg_color = "#5891A8"

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self. pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.widgets()
        self.frames ={}
        self.buttons =[]
        for i in (Ventas, Inventario, Clientes):
            frame = i(self, controlador)
            self.frames[i] = frame
            frame.pack()
            frame.config(bg=bg_color, highlightbackground= "gray", highlightthickness=1)
            frame.place(x=0, y=40, width=  1100, height=610)
        self.show_frame(Ventas)
        
    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()
        
    def ventas(self):
        self.show_frame(Ventas)
        
    def inventario(self):
        self.show_frame(Inventario)
        
    def clientes(self):
        self.show_frame(Clientes)
        
        
    def widgets(self):
        frame2= tk.Frame(self)
        frame2.place(x=0, y=0, width=1100, height=40)
        
        self.btn_ventas =Button(frame2, fg= "Black", text= "Ventas", font="sans 16 bold", command= self.ventas )
        self.btn_ventas.place(x=0, y=0, width= 200, height= 40)
        
        self.btn_inventario =Button(frame2, fg= "Black", text= "Inventario", font="sans 16 bold", command= self.inventario )
        self.btn_inventario.place(x=200, y=0, width= 200, height= 40)
        
        self.btn_clientes =Button(frame2, fg= "Black", text= "Clientes", font="sans 16 bold", command= self.clientes )
        self.btn_clientes.place(x=400, y=0, width= 200, height= 40)
        
        self.buttons ={self.btn_ventas, self.btn_inventario, self.btn_clientes}