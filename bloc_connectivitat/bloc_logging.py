import tkinter as tk
from tkinter import messagebox
import hashlib
import os
from db_connection import conexio_bd
import admin_menu  

# Fitxer per guardar les dades d'usuari
LOGIN_FILE = "logins.txt"

def hash_password(password):
    """Funció per encriptar la contrasenya."""
    return hashlib.sha256(password.encode()).hexdigest()

# Eliminar la funció conexio_bd() ja que ara la importem de db_connection

def inici_sesio():
    """Funció que crea la finestra d'inici de sessio i la seva funcionalitat"""
    def ok():
        """Funció que comprova les credencials d'inici de sessió"""
        usuari = entrada_usuari.get()
        password = entrada_contrasenya.get()
        
        # Primer verificar si és admin
        if admin_menu.ok_modificat(usuari, password):  # Canviat a la versió catalana
            finestra_inici_sesio.destroy()
            return
            
        # Si no és admin, continuar la verificació normal
        hashed_password = hash_password(password)

        if not os.path.exists(LOGIN_FILE):
            messagebox.showerror("Error", "No hi ha usuaris registrats.")
            return

        with open(LOGIN_FILE, "r") as file:
            for line in file:
                stored_usuari, stored_password = line.strip().split(",")
                if usuari == stored_usuari and hashed_password == stored_password:
                    messagebox.showinfo("Èxit", "Inici de sessió correcte!")
                    finestra_inici_sesio.destroy()
                    return
        messagebox.showerror("Error", "Nom d'usuari o contrasenya incorrectes.")

    def cancelar():
        """Funció que es crida quan es prem el botó cancelar"""
        finestra_inici_sesio.destroy() #tanca la finestra d'inici de sessio
        messagebox.showinfo("Avís", "S'ha cancelat l'operació") #missatge de cancel·lar l'operació

    finestra_inici_sesio = tk.Tk() #creació de la finestra d'inici de sessio
    finestra_inici_sesio.title("login") #titol de la finestra
    finestra_inici_sesio.geometry("300x200") #mida de la finestra
    etiqueta_usuari = tk.Label(finestra_inici_sesio, text="Usuari:") #label d'usuari
    etiqueta_contrasenya = tk.Label(finestra_inici_sesio, text="Contrasenya:") #label de contrasenya
    entrada_usuari = tk.Entry(finestra_inici_sesio) #entrada d'usuari
    entrada_contrasenya = tk.Entry(finestra_inici_sesio, show="*") #entrada de contrasenya i que no es vegi el que s'escriu

    # col·locació de las etiquetes, entrades i botons
    etiqueta_usuari.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entrada_usuari.grid(row=0, column=1, padx=10, pady=5)

    etiqueta_contrasenya.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entrada_contrasenya.grid(row=1, column=1, padx=10, pady=5)

    # Caixa perque els botons quedin junts
    frame_botons = tk.Frame(finestra_inici_sesio)
    frame_botons.grid(row=2, column=0, columnspan=2, pady=10)

    btn_ok = tk.Button(frame_botons, text="OK", command=ok, width=12, height=2)
    btn_cancelar = tk.Button(frame_botons, text="Cancel·lar", command=cancelar, width=12, height=2)

    # col·locació dels botons
    btn_ok.pack(side="left", padx=5)
    btn_cancelar.pack(side="left", padx=5)

    finestra_inici_sesio.mainloop() #perque no es tanqui la finestra

def registre():
    """Funció que crea la finestra de registre i la seva funcionalitat"""
    def ok():
        """Funció que registra un nou usuari"""
        usuari = entrada_usuari.get()
        password = entrada_contrasenya.get()
        hashed_password = hash_password(password)

        # Guardar les dades al fitxer
        with open(LOGIN_FILE, "a") as file: #obrir el fitxer d'usuaris
            file.write(f"{usuari},{hashed_password}\n")
        messagebox.showinfo("Èxit", "Usuari registrat correctament!")
        finestra_registre.destroy()

    def cancelar():
        finestra_registre.destroy() #tanca la finestra de registre
        messagebox.showinfo("Avís", "S'ha cancelat l'operació") #missatge de cancel·lat l'operació

    finestra_registre = tk.Tk() #creació de la finestra de registre
    finestra_registre.title("registre") #titol de la finestra
    finestra_registre.geometry("300x200") #mida de la finestra
    etiqueta_usuari = tk.Label(finestra_registre, text="Usuari:") #label d'usuari
    etiqueta_contrasenya = tk.Label(finestra_registre, text="Contrasenya:") #label de contrasenya
    entrada_usuari = tk.Entry(finestra_registre) #entrada d'usuari
    entrada_contrasenya = tk.Entry(finestra_registre, show="*") #entrada de contrasenya

    # col·locació de las etiquetes, entrades i botons
    etiqueta_usuari.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entrada_usuari.grid(row=0, column=1, padx=10, pady=5)

    etiqueta_contrasenya.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entrada_contrasenya.grid(row=1, column=1, padx=10, pady=5)

    # Caixa perque els botons quedin junts
    frame_botons = tk.Frame(finestra_registre)
    frame_botons.grid(row=2, column=0, columnspan=2, pady=10)

    btn_ok = tk.Button(frame_botons, text="OK", command=ok, width=12, height=2)
    btn_cancelar = tk.Button(frame_botons, text="Cancel·lar", command=cancelar, width=12, height=2)

    # col·locació dels botons
    btn_ok.pack(side="left", padx=5)
    btn_cancelar.pack(side="left", padx=5)

    finestra_registre.mainloop() #inici de la finestra de registre

def logger():
    """Funció que crea la finestra de logging i la seva funcionalitat"""
    finestra = tk.Tk() #creació de la finestra de logging
    finestra.title("Gestor d'hotels") #titol de la finestra
    finestra.geometry("400x450") #mida de la finestra
    finestra.configure(bg="lightblue") #color de fons de la finestra
    etiqueta_benvinguda = tk.Label(
        finestra,  #label de benvinguda al hotel
        text="Benvingut al gestor d'hotels", 
        bg="lightblue",
        font=("Arial", 20, "bold"), # tipus de lletra
        width=50) 

    btn_inici_sesio = tk.Button( #botó d'inici de sessio
        finestra, 
        text="Iniciar Sessió", 
        command=inici_sesio, 
        font=("Arial", 12, "bold"), # tipus de lletra
        bg="#4A90E2",  # Blau 
        fg="white", #fons de lletra
        width=15, 
        height=2, 
        bd=3,  # Cantonades en 3d
        cursor="hand2"
    )

    btn_registre = tk.Button( #botó de registre
        finestra, 
        text="Registrar-se", 
        command=registre, 
        font=("Arial", 12, "bold"), # tipus de lletra
        bg="#50C878",  # Verd 
        fg="white", #fons de lletra
        width=15, 
        height=2, 
        bd=3, # Cantonades en 3d
        cursor="hand2"
    )
    conexio_bd()
    #colocació dels botons/etiquetes
    etiqueta_benvinguda.pack(pady=10, fill="x") 
    btn_inici_sesio.pack(pady=10) 
    btn_registre.pack(pady=10) 
    finestra.mainloop() #perque no es tanqui la finestra
