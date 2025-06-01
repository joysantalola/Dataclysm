# Importació de les llibreries necessàries
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Per utilitzar el Combobox
import bloc_logging
import psycopg2
from db_connection import conexio_bd

def get_hotels():
    """Funció per obtenir la llista d'hotels de la base de dades"""
    hotels = []
    conn = conexio_bd()
    try:
        if conn:
            with conn.cursor() as cur:
                # Consulta per obtenir els hotels ordenats per ID
                cur.execute("SELECT id_hotel, nom FROM hotel ORDER BY id_hotel")
                hotels = cur.fetchall()
            conn.close()
    except psycopg2.Error as e:
        print(f"Error de base de dades: {e}")
    return hotels

def get_tipus_empleat():
    """Funció per obtenir els tipus d'empleats disponibles"""
    tipus = [
        "Director",
        "Gerent",
        "Personal Servei Habitacions",
        "Personal Recepció",
        "Personal Cuina",
        "Personal Servei Restaurant",
        "Personal Activitats"
    ]
    return tipus

def mostrar_formulari_personal():
    """Funció principal per mostrar el formulari d'afegir personal"""
    # Configuració de la finestra principal
    finestra_formulari = tk.Toplevel()
    finestra_formulari.title("Afegir Nou Personal")
    finestra_formulari.geometry("400x650")
    finestra_formulari.configure(bg="slategray3")

    # Obtenció de la llista d'hotels pel desplegable
    hotels = get_hotels()
    hotel_options = {f"{hotel[0]} - {hotel[1]}": hotel[0] for hotel in hotels}

    # Creació dels camps del formulari
    tk.Label(finestra_formulari, text="ID Treballador:", bg="slategray3").pack(pady=5)
    entrada_id = tk.Entry(finestra_formulari)
    entrada_id.pack(pady=5)

    # Desplegable per seleccionar l'hotel
    tk.Label(finestra_formulari, text="ID Hotel:", bg="slategray3").pack(pady=5)
    entrada_hotel = ttk.Combobox(finestra_formulari, values=list(hotel_options.keys()))
    entrada_hotel.pack(pady=5)

    # Obtenció i creació del desplegable per tipus d'empleat
    tipus_empleat_options = get_tipus_empleat()
    tk.Label(finestra_formulari, text="Tipus Empleat:", bg="slategray3").pack(pady=5)
    entrada_tipus = ttk.Combobox(finestra_formulari, values=tipus_empleat_options, state="readonly")
    entrada_tipus.pack(pady=5)

    # Resta de camps del formulari
    tk.Label(finestra_formulari, text="DNI:", bg="slategray3").pack(pady=5)
    entrada_dni = tk.Entry(finestra_formulari)
    entrada_dni.pack(pady=5)

    tk.Label(finestra_formulari, text="Cognoms:", bg="slategray3").pack(pady=5)
    entrada_cognoms = tk.Entry(finestra_formulari)
    entrada_cognoms.pack(pady=5)

    tk.Label(finestra_formulari, text="Nom:", bg="slategray3").pack(pady=5)
    entrada_nom = tk.Entry(finestra_formulari)
    entrada_nom.pack(pady=5)

    tk.Label(finestra_formulari, text="Data Naixement (YYYY-MM-DD):", bg="slategray3").pack(pady=5)
    entrada_data = tk.Entry(finestra_formulari)
    entrada_data.pack(pady=5)

    tk.Label(finestra_formulari, text="Telèfon:", bg="slategray3").pack(pady=5)
    entrada_telefon = tk.Entry(finestra_formulari)
    entrada_telefon.pack(pady=5)

    def guardar():
        """Funció per gestionar el procés de guardar les dades"""
        # Recollida de dades del formulari
        id_treballador = entrada_id.get()
        hotel_selected = entrada_hotel.get()
        id_hotel = hotel_options.get(hotel_selected)
        tipus_empleat = entrada_tipus.get()
        dni = entrada_dni.get()
        cognoms = entrada_cognoms.get()
        nom = entrada_nom.get()
        data_naixement = entrada_data.get()
        telefon = entrada_telefon.get()

        # Diàleg de confirmació
        confirmacio = messagebox.askyesno(
            "Confirmació",
            f"Estàs segur que vols afegir aquest empleat?\n\n"
            f"ID: {id_treballador}\n"
            f"ID Hotel: {id_hotel}\n"
            f"Tipus: {tipus_empleat}\n"
            f"DNI: {dni}\n"
            f"Cognoms: {cognoms}\n"
            f"Nom: {nom}\n"
            f"Data Naixement: {data_naixement}\n"
            f"Telèfon: {telefon}"
        )
        if confirmacio:
            guardar_personal(id_treballador, id_hotel, tipus_empleat, dni, cognoms, nom, data_naixement, telefon)

    # Botó per guardar les dades
    boto_guardar = tk.Button(
        finestra_formulari,
        text="Guardar",
        command=guardar,
        bg="white"
    )
    boto_guardar.pack(pady=20)

def guardar_personal(id_treballador, id_hotel, tipus_empleat, dni, cognoms, nom, data_naixement, telefon):
    """Funció per guardar les dades del personal a la base de dades"""
    conn = conexio_bd()
    try:
        if conn:
            with conn.cursor() as cur:
                # Conversió de tipus de dades
                id_treballador = int(id_treballador)
                id_hotel = int(id_hotel) if id_hotel else None
                
                # Inserció del nou treballador a la base de dades
                cur.execute("""
                    INSERT INTO treballador (
                        id_treballador,
                        id_hotel, 
                        tipus_empleat, 
                        dni, 
                        cognoms, 
                        nom, 
                        data_naixement, 
                        telefon
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (id_treballador, id_hotel, tipus_empleat, dni, cognoms, nom, data_naixement, telefon))
                conn.commit()
                messagebox.showinfo("Èxit", "Treballador afegit correctament")
                conn.close()
    except psycopg2.Error as e:
        print(f"Error de base de dades: {e}")
        messagebox.showerror("Error", f"No s'ha pogut afegir el treballador: {e}")
        if conn:
            conn.close()
