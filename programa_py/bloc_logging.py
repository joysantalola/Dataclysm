import tkinter as tk
from tkinter import messagebox, ttk
import hashlib
from db_connection import conexio_bd
import os
import admin_menu

# Fitxer per guardar les dades d'usuari
LOGIN_FILE = "logins.txt"

def hash_password(password):
    """Funció per encriptar la contrasenya."""
    return hashlib.sha256(password.encode()).hexdigest()

def inici_sesio(finestra_principal):
    """Funció que crea la finestra d'inici de sessio i la seva funcionalitat"""

    finestra_inici_sesio = tk.Toplevel(finestra_principal)
    finestra_inici_sesio.title("login")
    finestra_inici_sesio.geometry("300x200")

    # Mostrar-la al davant de la finestra principal
    finestra_inici_sesio.transient(finestra_principal)
    finestra_inici_sesio.grab_set()
    finestra_inici_sesio.focus_set()
    
    def on_closing():
        finestra_inici_sesio.destroy()
    
    finestra_inici_sesio.protocol("WM_DELETE_WINDOW", on_closing)

    
    def ok():
        """Funció que comprova les credencials d'inici de sessió"""
        usuari = entrada_usuari.get()
        password = entrada_contrasenya.get()
        
        # Primer verificar si és admin
        if admin_menu.ok_modificat(usuari, password):
            finestra_inici_sesio.destroy()
            finestra_principal.destroy()  # Tancar definitivament la principal
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
                    finestra_principal.destroy()  # Tancar definitivament la principal
                    # Aquí podries obrir la següent finestra
                    return
        messagebox.showerror("Error", "Nom d'usuari o contrasenya incorrectes.")

    finestra_inici_sesio.deiconify()


    def cancelar():
        """Funció que es crida quan es prem el botó cancelar"""
        finestra_inici_sesio.destroy()
        finestra_principal.deiconify()  # Mostrar de nou la principal
        messagebox.showinfo("Avís", "S'ha cancelat l'operació")


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

def registre(finestra_principal):
    """Funció que crea la finestra de registre i la seva funcionalitat"""
    # Ocultar la finestra principal temporalment
    finestra_principal.withdraw()
    
    finestra_registre = tk.Toplevel(finestra_principal)
    finestra_registre.title("registre")
    finestra_registre.geometry("300x200")
    
    # Si es tanca la finestra amb la X, mostrar de nou la principal
    def on_closing():
        finestra_principal.deiconify()
        finestra_registre.destroy()
    
    finestra_registre.protocol("WM_DELETE_WINDOW", on_closing)
    
    def ok():
        """Funció que registra un nou usuari"""
        usuari = entrada_usuari.get()
        password = entrada_contrasenya.get()
        hashed_password = hash_password(password)

        # Guardar les dades al fitxer
        with open(LOGIN_FILE, "a") as file:
            file.write(f"{usuari},{hashed_password}\n")
        messagebox.showinfo("Èxit", "Usuari registrat correctament!")
        finestra_registre.destroy()
        # Després del registre, redirigir a l'inici de sessió
        inici_sesio(finestra_principal)

    def cancelar():
        finestra_registre.destroy()
        finestra_principal.deiconify()  # Mostrar de nou la principal
        messagebox.showinfo("Avís", "S'ha cancelat l'operació")

    etiqueta_usuari = tk.Label(finestra_registre, text="Usuari:")
    etiqueta_contrasenya = tk.Label(finestra_registre, text="Contrasenya:")
    entrada_usuari = tk.Entry(finestra_registre)
    entrada_contrasenya = tk.Entry(finestra_registre, show="*")

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


def logger():
    """Funció que crea la finestra de logging i la seva funcionalitat"""
    finestra = tk.Tk()
    finestra.title("Gestor d'hotels")
    finestra.geometry("400x200")
    finestra.configure(bg="lightblue")
    
    # Etiqueta de benvinguda
    etiqueta_benvinguda = tk.Label(
        finestra,
        text="Benvingut al gestor d'hotels", 
        bg="lightblue",
        font=("Arial", 20, "bold"),
        width=50
    )
    etiqueta_benvinguda.pack(pady=10, fill="x")

    # Frame per cada parell de botons
    frame1 = tk.Frame(finestra, bg="lightblue")
    frame1.pack(pady=10)
    
    # Primer parell: Inici sessió i Registre
    btn_inici_sesio = tk.Button(
        frame1, 
        text="Iniciar Sessió", 
        command=lambda: inici_sesio(finestra),
        font=("Arial", 12, "bold"),
        bg="#4A90E2",
        fg="white",
        width=15, 
        height=2, 
        bd=3,
        cursor="hand2"
    )
    btn_inici_sesio.pack(side=tk.LEFT, padx=5)

    btn_registre = tk.Button(
        frame1, 
        text="Registrar-se", 
        command=lambda: registre(finestra),
        font=("Arial", 12, "bold"),
        bg="#50C878",
        fg="white",
        width=15, 
        height=2, 
        bd=3,
        cursor="hand2"
    )
    btn_registre.pack(side=tk.LEFT, padx=5)

    finestra.mainloop()
