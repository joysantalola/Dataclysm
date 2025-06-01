# admin_menu_refactor.py

import tkinter as tk
from tkinter import messagebox, ttk
import hashlib
from gestio_hotels import afegir_hotel, modificar_hotel
import gestio_personal
from gestio_reserves import afegir_reserva, eliminar_reserva, modificar_reserva
import check_in, check_out
from db_connection import conexio_bd
import consultes_informes
from consultes_informes import (
    obrir_resum_hotel,
    obrir_informe_personal,
    obrir_informe_reserves,
    obrir_informe_moviments,
    consultar_serveis_hotels
)
import dummy_data
import exportacio
from PIL import Image, ImageTk
import os

ADMIN_USER = "espamus"
ADMIN_PASSWORD = hashlib.sha256("P@ssw0rd".encode()).hexdigest()


def verificar_admin(usuari, password_hash):
    return usuari == ADMIN_USER and password_hash == ADMIN_PASSWORD


def mostrar_menu_admin():
    finestra_admin = tk.Tk()
    finestra_admin.title("Panell d'Administrador")
    finestra_admin.attributes('-fullscreen', True)  # Pantalla completa real
    finestra_admin.configure(bg="lightblue")

    # Salir de pantalla completa con ESC
    finestra_admin.bind("<Escape>", lambda e: finestra_admin.attributes("-fullscreen", False))

    try:
        # Obtenir el directori del script actual
        dir_actual = os.path.dirname(os.path.abspath(__file__))

        # Construir rutes absolutes
        ruta_letras = os.path.join(dir_actual, "logo", "letras.png")
        ruta_logo = os.path.join(dir_actual, "logo", "logo.png")

        # Carregar les imatges
        imagen_logo = Image.open(ruta_logo).resize((150, 150))
        imagen_letras = Image.open(ruta_letras).resize((300, 150))

        imagen_logo_tk = ImageTk.PhotoImage(imagen_logo)
        imagen_letras_tk = ImageTk.PhotoImage(imagen_letras)

        # Frame principal
        main_frame = tk.Frame(finestra_admin, bg="lightblue")
        main_frame.pack(fill="both", expand=True)

        # Frame superior per les imatges i el títol
        header_frame = tk.Frame(main_frame, bg="lightblue")
        header_frame.pack(fill="x", padx=20, pady=(5, 0))

        etiqueta_logo = tk.Label(header_frame, image=imagen_logo_tk, bg="lightblue")
        etiqueta_logo.image = imagen_logo_tk
        etiqueta_logo.pack(side="left")

        tk.Label(
            header_frame,
            text="Panell d'Administració",
            bg="lightblue",
            font=("Arial", 40, "bold")
        ).pack(side="left", expand=True, padx=0)

        etiqueta_letras = tk.Label(header_frame, image=imagen_letras_tk, bg="lightblue")
        etiqueta_letras.image = imagen_letras_tk
        etiqueta_letras.pack(side="right")

        # Frame dels botons amb layout dinàmic
        button_frame = tk.Frame(main_frame, bg="lightblue")
        button_frame.pack(fill="both", expand=True, padx=40, pady=20)

        print("Imatges carregades correctament")

    except FileNotFoundError as e:
        print(f"Error: Archivo de imagen no encontrado - {e}")
        print("Continuando sin imágenes...")

        main_frame = tk.Frame(finestra_admin, bg="lightblue")
        main_frame.pack(fill="both", expand=True)

        button_frame = tk.Frame(main_frame, bg="lightblue")
        button_frame.pack(fill="both", expand=True, padx=40, pady=20)

        tk.Label(
            main_frame,
            text="Panell d'Administració",
            bg="lightblue",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

    # Configuració dels botons
    boto_config = [
        ("Gestionar Hotels", obrir_gestio_hotels),
        ("Gestionar Personal", gestio_personal.mostrar_formulari_personal),
        ("Gestionar Reserves", obrir_gestio_reserves),
        ("Check-in / Check-out", obrir_check_in_out_ventana),  
        ("Exportar Dades", exportacio.exportar_informe_reserves),
        ("Consultar Personal", obrir_informe_personal),
        ("Consultar Hotel", obrir_resum_hotel),
        ("Consultar Serveis", consultar_serveis_hotels),
        ("Consultar Check-in", obrir_informe_moviments),
        ("Consultar Reserves", obrir_informe_reserves)
        #("Gestió de Dades", obrir_gestio_dades)
    ]

    # Ajusta filas y columnas según ahora son 10 botones (no 11)
    for i in range(5):  # 5 filas
        button_frame.rowconfigure(i, weight=1)
    for j in range(2):  # 2 columnas
        button_frame.columnconfigure(j, weight=1)

    # Crear 10 botones (2 columnas x 5 filas)
    for i, (text, command) in enumerate(boto_config):
        row = i % 5
        col = i // 5
        tk.Button(
            button_frame,
            text=text,
            command=command,
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="black",
            relief=tk.RAISED,
            bd=4
        ).grid(row=row, column=col, padx=20, pady=15, sticky="nsew")


    # Botón "Tancar sessió" pequeño y discreto en la esquina inferior derecha
    boto_tancar_sessio = tk.Button(
        main_frame,
        text="Tancar sessió",
        font=("Arial", 20),   
        bg="#b30303",        
        fg="white",
        relief=tk.FLAT,
        bd=1,
        command=finestra_admin.destroy
    )
    boto_tancar_sessio.pack(side="bottom", anchor="e", padx=20, pady=10)


    finestra_admin.mainloop()

def ok_modificat(usuari, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if verificar_admin(usuari, hashed_password):
        messagebox.showinfo("Èxit", "Benvingut Administrador!")
        # Delay showing the admin menu until after the login window is closed
        tk.Tk().after(100, mostrar_menu_admin)
        return True
    return False

def obrir_check_in_out_ventana():
    finestra = tk.Toplevel()
    finestra.title("Check-in / Check-out")
    finestra.geometry("300x300")
    finestra.configure(bg="slategray3")

    tk.Label(
        finestra,
        text="Selecciona una opció",
        font=("Arial", 16, "bold"),
        bg="slategray3",
        fg="black"
    ).pack(pady=20)

    boto_estil = {
        "font": ("Arial", 14, "bold"),
        "width": 15,
        "height": 2,
        "bg": "#ffffff",
        "fg": "black",
        "relief": tk.RAISED,
        "bd": 4
    }

    tk.Button(
        finestra,
        text="Realitzar Check-in",
        command=check_in.realizar_check_in,
        **boto_estil
    ).pack(pady=10)

    tk.Button(
        finestra,
        text="Realitzar Check-out",
        command=check_out.realizar_check_out,
        **boto_estil
    ).pack(pady=10)


def obrir_gestio_hotels():
    finestra = tk.Toplevel()
    finestra.title("Gestió d'Hotels")
    finestra.geometry("400x300")
    finestra.configure(bg="slategray3")

    # Títol dins la finestra
    tk.Label(
        finestra,
        text="Gestió d'Hotels",
        font=("Arial", 18, "bold"),
        bg="slategray3",
        fg="black"
    ).pack(pady=(20, 10))

    boto_estil = {
        "font": ("Arial", 14, "bold"),
        "width": 25,
        "height": 3,
        "bg": "#ffffff",
        "fg": "black",
        "relief": tk.RAISED,
        "bd": 4
    }

    tk.Button(finestra, text="Afegir Hotel", command=afegir_hotel, **boto_estil).pack(pady=10)
    tk.Button(finestra, text="Modificar Hotel", command=modificar_hotel, **boto_estil).pack(pady=10)


def obrir_gestio_dades():
    finestra_dades = tk.Toplevel()
    finestra_dades.title("Gestió de Dades de Prova")
    finestra_dades.geometry("400x250")
    finestra_dades.configure(bg="slategray3")

    tk.Label(
        finestra_dades,
        text="Dades de Prova",
        font=("Arial", 16, "bold"),
        bg="slategray3"
    ).pack(pady=10)

    # Botó Generar Dades
    tk.Button(
        finestra_dades,
        text="Generar Dades",
        command=generar_dades_handler,
        font=("Arial", 14),
        bg="#FFFFFF",
        fg="black",
        width=20,
        height=2
    ).pack(pady=10)

    # Botó Eliminar Dades
    tk.Button(
        finestra_dades,
        text="Esborrar Dades",
        command=eliminar_dades_handler,
        font=("Arial", 14),
        bg="#ca2115",
        fg="white",
        width=20,
        height=2
    ).pack(pady=10)


def obrir_gestio_reserves():
    finestra = tk.Toplevel()
    finestra.title("Gestió de Reserves")
    finestra.geometry("450x450")
    finestra.configure(bg="slategray3")

    # Títol dins la finestra
    tk.Label(
        finestra,
        text="Gestió de Reserves",
        font=("Arial", 18, "bold"),
        bg="slategray3",
        fg="black"
    ).pack(pady=(20, 10))

    boto_estil = {
        "font": ("Arial", 14, "bold"),
        "width": 25,
        "height": 3,
        "bg": "#ffffff",
        "fg": "black",
        "relief": tk.RAISED,
        "bd": 4
    }

    tk.Button(finestra, text="Afegir Reserva", command=afegir_reserva, **boto_estil).pack(pady=10)
    tk.Button(finestra, text="Eliminar Reserva", command=eliminar_reserva, **boto_estil).pack(pady=10)
    tk.Button(finestra, text="Modificar Reserva", command=modificar_reserva, **boto_estil).pack(pady=10)


def generar_dades_handler():
    try:
        if dummy_data.generar_dades_prova():
            messagebox.showinfo("Èxit", "S'han generat les dades de prova!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def eliminar_dades_handler():
    try:
        if messagebox.askyesno("Confirmar", "Eliminar totes les dades de prova?"):
            if dummy_data.eliminar_dades_prova():
                messagebox.showinfo("Èxit", "Dades eliminades correctament!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Altres funcions com consultar_reserves, consultar_serveis_hotels, etc. haurien de quedar
# definides en mòduls separats i ser importades, per modularitat i mantenibilitat.
# Aquí només es mostra la estructura principal neta i centralitzada.
