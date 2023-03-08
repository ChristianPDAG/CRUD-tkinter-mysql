from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pymysql

def conexionBBDD():
    conexion = pymysql.connect(user="root",password="",host="localhost",database="base_clientes",port=3306)
    return conexion


def salirAplicacion():
    valor = messagebox.askquestion("Salir","¿Esta seguro que desea salir?")
    if valor == "yes":
        root.destroy()

def limpiarCampos():
    rut_cli.set("")
    nom_cli.set("")
    ape_cli.set("")
    dir_cli.set("")
    ema_cli.set("")

def borrar_registros():
    conexion = conexionBBDD()
    cursor = conexion.cursor() 
    try:
        if messagebox.askyesno("ADVERTENCIA","TODOS LOS REGISTROS CREADOS SERÁN ELIMINADOS DE LA BASE DE DATOS,¿DESEA CONTINUAR?"):
            cursor.execute(f"DELETE FROM cliente")
            conexion.commit()
            messagebox.showinfo("REGISTROS ELIMINADOS","LOS REGISTROS HAN SIDO ELIMINADOS CON ÉXITO")
    except:
        messagebox.showwarning("ADVERTENCIA", "Ocurrio un error al crear el registro. Verifique conexión con BBDD")
        pass

def crear():
    conexion = conexionBBDD()
    cursor = conexion.cursor()   
    try:
        if len(rut_cli.get())>=11 and len(nom_cli.get())>1 and len(ape_cli.get())>1 and len(dir_cli.get())>1 and len(ema_cli.get())>1 :
            cursor.execute(f"INSERT INTO cliente VALUES ('{rut_cli.get()}','{nom_cli.get()}','{ape_cli.get()}','{dir_cli.get()}','{ema_cli.get()}')")
            conexion.commit()
        else:
            messagebox.showwarning("ADVERTENCIA", "TODOS LOS CAMPOS SON NECESARIOS PARA CREAR EL REGISTRO, POR FAVOR COMPLETAR\nEl RUT debe ser ingresado con puntos y guión.")
    except:
        messagebox.showwarning("ADVERTENCIA", "Ocurrio un error al crear el registro. Verifique conexión con BBDD")
        pass
    limpiarCampos()
    mostrar()

def actualizar():
    conexion = conexionBBDD()
    cursor = conexion.cursor()
    try:
        if len(rut_cli.get())>=11 and len(nom_cli.get())>1 and len(ape_cli.get())>1 and len(dir_cli.get())>1 and len(ema_cli.get())>1 :
            cursor.execute(f"UPDATE cliente SET rut_cli='{rut_cli.get()}', nom_cli='{nom_cli.get()}', ape_cli='{ape_cli.get()}',dir_cli='{dir_cli.get()}',ema_cli='{ema_cli.get()}' WHERE rut_cli ='{rut_cli.get()}'")
            conexion.commit()
        else:
            messagebox.showwarning("ADVERTENCIA", "TODOS LOS CAMPOS SON NECESARIOS PARA CREAR EL REGISTRO, POR FAVOR COMPLETAR\nEl RUT debe ser ingresado con puntos y guión.")
    except:
        messagebox.showwarning("ADVERTENCIA", "Ocurrio un error al actualizar el registro.")
        
    limpiarCampos()
    mostrar()

def mostrar():
    conexion = conexionBBDD()
    cursor = conexion.cursor()
    registros = tree.get_children()
    for elemento in registros:
        tree.delete(elemento)
    
    try:
        cursor.execute("SELECT * FROM cliente ")
        for fila in cursor:
            tree.insert("",0,text=fila[0], values=(fila[1],fila[2],fila[3],fila[4]))
    except:
        pass

def borrar():
    conexion = conexionBBDD()
    cursor = conexion.cursor()
    try:             
        if messagebox.askyesno(message="EL REGISTRO " + rut_cli.get() + " SERÁ ELIMINADO DE LA BASE DE DATOS.\n     ¿DESEA CONTINUAR?" , title="ADVERTENCIA"):
            cursor.execute(f"DELETE FROM cliente WHERE rut_cli ='{rut_cli.get()}'")
            conexion.commit()
        else:
            messagebox.showerror("CANCELADO","LA ELIMINACIÓN DEL REGISTRO SE HA CANCELADO")

    except:
        messagebox.showwarning("ADVERTENCIA", "ALGO HA FALLADO AL INTENTAR ELIMINAR EL REGISTRO")
        
    limpiarCampos()
    mostrar()

def MostrarSelecItem(event):
    tree.identify('item',event.x,event.y)
    element = tree.item(tree.focus())
    rut_cli.set(element['text'])
    nom_cli.set(element['values'][0])
    ape_cli.set(element['values'][1])
    dir_cli.set(element['values'][2])
    ema_cli.set(element['values'][3])

#window
root = Tk()
root.resizable(width=0,height=0)
root.title("CLIENTES")
root.geometry("840x300")


#TREEVIEW
tree = ttk.Treeview(height=10, columns=('#0','#1','#2','#3'),selectmode='browse')
tree.place(x=260, y=0)
tree.column('#0', width=100)
tree.column('#1',width=100)
tree.column('#2',width=100)
tree.column('#3',width=130)
tree.column('#4',width=130)
tree.heading('#0', text='RUT', anchor=CENTER)
tree.heading('#1',text='Nombre', anchor=CENTER)
tree.heading('#2', text="Apellido",anchor=CENTER)
tree.heading('#3', text="Dirección",anchor=CENTER)
tree.heading('#4', text="Email",anchor=CENTER)
tree.bind('<<TreeviewSelect>>', MostrarSelecItem)

#SCROLLBAR
tree_scroll = ttk.Scrollbar(root, orient='vertical', command = tree.yview)
tree_scroll.pack(side='right', fill=Y)
tree.configure(yscrollcommand=tree_scroll.set)
tree_scroll.pack(side=RIGHT,fill=Y)

#MENÚ's
menubar = Menu(root)

menubasedatos = Menu(menubar,tearoff=0)
menubasedatos.add_command(label="Salir", command = salirAplicacion)
menubar.add_cascade(label="Inicio", menu = menubasedatos)

edicionMenu = Menu(menubar,tearoff=0)
edicionMenu.add_command(label="Borrar datos ingresados", command = limpiarCampos)
edicionMenu.add_command(label="Borrar todos los registros ", command = borrar_registros)
menubar.add_cascade(label="Edición", menu = edicionMenu)

root.config(menu=menubar)
#VARIABLES
rut_cli = StringVar()
nom_cli = StringVar()
ape_cli = StringVar()
dir_cli = StringVar()
ema_cli = StringVar()
#LABEL's
rutlbl = Label(root,text="RUT").place(x=10,y=10)
namelbl = Label(root,text="Nombre").place(x=10,y=40)
lastnamelbl = Label(root,text="Apellido").place(x=10,y=70)
addresslbl = Label(root,text="Direccion").place(x=10,y=100)
maillbl = Label(root,text="Email").place(x=10,y=130)

#ENTRY's
rut_ent=Entry(root,textvariable= rut_cli,width=30).place(x=70,y=10)
name_ent=Entry(root,textvariable= nom_cli,width=30).place(x=70,y=40)
lastname_ent=Entry(root,textvariable= ape_cli,width=30).place(x=70,y=70)
address_ent=Entry(root,textvariable= dir_cli,width=30).place(x=70,y=100)
mail_ent=Entry(root,textvariable= ema_cli,width=30).place(x=70,y=130)

#BUTTON's
reg_btn = Button(root,text="Registrar", command = crear).place(x=10,y=160)
upd_btn = Button(root, text="Actualizar", command = actualizar).place(x=10, y=200)
view_btn = Button(root, text="Mostrar", command = mostrar).place(x=100, y=160)
del_btn = Button(root, text = "Eliminar", command = borrar).place(x=100, y=200)


root.mainloop()