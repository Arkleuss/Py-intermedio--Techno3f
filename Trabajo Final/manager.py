from tkinter import *
from tkinter import ttk
from ventas import Ventas
from clientes import Clientes
from inventario import Inventario
from container import Container
import sys
import os


bg_color = "#5891A8"

class Manager(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("CRUD v1.0")
        self.geometry("1100x650+120+20")
        self.resizable(False, False)
        
        container=Frame(self)
        container.pack(side= TOP, fill=BOTH, expand=True)
        container.config(bg=bg_color)
        
        self.frames = {}
        frame = Container(container, self)
        self.frames[Container] = frame
            
        self.show_frame(Container)
        
        self.Style = ttk.Style()
        self.Style.theme_use("clam")
        
    def show_frame(self, container):
        frame =self.frames[container]
        frame.tkraise()
        
def main():
    app =Manager()
    app.mainloop()
            
if __name__ == "__main__":
    main()
            