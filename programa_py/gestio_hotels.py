# Importació de les llibreries necessàries
import tkinter as tk
from tkinter import messagebox, ttk
from db_connection import conexio_bd
import psycopg2

def afegir_hotel():
    """Funció per afegir un nou hotel a la base de dades"""
    # Configuració de la finestra principal
    finestra_nou = tk.Toplevel()
    finestra_nou.title("Afegir Nou Hotel")
    finestra_nou.geometry("500x550")
    finestra_nou.configure(bg="slategray3")

    # Creació del formulari amb els camps necessaris
    tk.Label(finestra_nou, text="Nom de l'Hotel:", bg="slategray3").pack(pady=5)
    nom_entry = tk.Entry(finestra_nou)
    nom_entry.pack(pady=5)

    tk.Label(finestra_nou, text="Adreça:", bg="slategray3").pack(pady=5)
    adreca_entry = tk.Entry(finestra_nou)
    adreca_entry.pack(pady=5)

    tk.Label(finestra_nou, text="Població:", bg="slategray3").pack(pady=5)
    poblacio_entry = tk.Entry(finestra_nou)
    poblacio_entry.pack(pady=5)

    tk.Label(finestra_nou, text="Web:", bg="slategray3").pack(pady=5)
    web_entry = tk.Entry(finestra_nou)
    web_entry.pack(pady=5)

    tk.Label(finestra_nou, text="Número d'estrelles:", bg="slategray3").pack(pady=5)
    estrelles_entry = tk.Entry(finestra_nou)
    estrelles_entry.pack(pady=5)

    tk.Label(finestra_nou, text="Telèfon:", bg="slategray3").pack(pady=5)
    telefon_entry = tk.Entry(finestra_nou)
    telefon_entry.pack(pady=5)

    tk.Label(finestra_nou, text="ID Director:", bg="slategray3").pack(pady=5)
    director_entry = tk.Entry(finestra_nou)
    director_entry.pack(pady=5)

    tk.Label(finestra_nou, text="ID Gerent:", bg="slategray3").pack(pady=5)
    gerent_entry = tk.Entry(finestra_nou)
    gerent_entry.pack(pady=5)

    def guardar_hotel():
        """Funció per validar i guardar les dades del nou hotel"""
        # Obtenció dels valors dels camps
        nom = nom_entry.get()
        adreca = adreca_entry.get()
        poblacio = poblacio_entry.get()
        web = web_entry.get() or None

        try:
            # Conversió dels camps numèrics
            num_estrelles = int(estrelles_entry.get())
            id_director = int(director_entry.get())
            id_gerent = int(gerent_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Els camps numèrics han de ser números vàlids")
            return

        # Validació dels camps obligatoris
        if not all([nom, adreca, poblacio, num_estrelles, id_director, id_gerent]):
            messagebox.showwarning("Advertència", "Si us plau, ompliu tots els camps obligatoris")
            return

        # Confirmació abans de guardar
        confirmacio = messagebox.askyesno(
            "Confirmar",
            f"Esteu segur que voleu afegir l'hotel?\n\n" +
            f"Nom: {nom}\n" +
            f"Adreça: {adreca}\n" +
            f"Població: {poblacio}\n" +
            f"Web: {web or 'No especificada'}\n" +
            f"Estrelles: {num_estrelles}\n" +
            f"Telèfon: {telefon or 'No especificat'}\n" +
            f"ID Director: {id_director}\n" +
            f"ID Gerent: {id_gerent}"
        )

        if not confirmacio:
            return

        try:
            # Connexió a la base de dades i verificació de dades
            conn = conexio_bd()
            if conn:
                with conn.cursor() as cur:
                    # Verificació de l'existència del director
                    cur.execute("SELECT 1 FROM treballador WHERE id_treballador = %s", (id_director,))
                    if not cur.fetchone():
                        messagebox.showerror("Error", "L'ID del director no existeix a la taula treballador")
                        return

                    # Verificació de l'existència del gerent
                    cur.execute("SELECT 1 FROM treballador WHERE id_treballador = %s", (id_gerent,))
                    if not cur.fetchone():
                        messagebox.showerror("Error", "L'ID del gerent no existeix a la taula treballador")
                        return

                    # Inserció del nou hotel a la base de dades
                    cur.execute(
                        """INSERT INTO hotel (nom, adreca, poblacio, web, num_estrelles, 
                        telefon, id_director, id_gerent) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (nom, adreca, poblacio, web, num_estrelles, telefon, 
                         id_director, id_gerent)
                    )
                    conn.commit()
                    messagebox.showinfo("Èxit", "Hotel afegit correctament")
                    finestra_nou.destroy()

        except psycopg2.Error as e:
            # Gestió d'errors de la base de dades
            mensaje_error = str(e).split("CONTEXT:")[0].strip()
            if mensaje_error.startswith("ERROR:"):
                mensaje_error = mensaje_error[6:].strip()
            messagebox.showerror("Error", f"Error en guardar l'hotel: {mensaje_error}")
        except Exception as e:
            messagebox.showerror("Error", f"Error en guardar l'hotel: {str(e)}")

    frame_botons = tk.Frame(finestra_nou, bg="slategray3")
    frame_botons.pack(pady=20)

    def cancelar():
        if messagebox.askyesno("Confirmar", "Esteu segur que voleu cancel·lar? Es perdran totes les dades introduïdes."):
            finestra_nou.destroy()

    tk.Button(
        frame_botons,
        text="Guardar",
        command=guardar_hotel,
        font=("Arial", 12),
        width=10
    ).pack(side="left", padx=10)

    tk.Button(
        frame_botons,
        text="Cancel·lar",
        command=cancelar,
        font=("Arial", 12),
        width=10
    ).pack(side="left", padx=10)

def modificar_hotel():
    """Funció per modificar les dades d'un hotel existent"""
    finestra_mod = tk.Toplevel()
    finestra_mod.title("Modificar Hotel")
    finestra_mod.geometry("500x550")
    finestra_mod.configure(bg="slategray3")

    tk.Label(finestra_mod, text="Seleccionar Hotel:", bg="slategray3").pack(pady=5)
    hotel_combo = ttk.Combobox(finestra_mod)
    hotel_combo.pack(pady=5)

    # Camps per modificar
    tk.Label(finestra_mod, text="Nom:", bg="slategray3").pack(pady=5)
    nom_entry = tk.Entry(finestra_mod)
    nom_entry.pack(pady=5)

    tk.Label(finestra_mod, text="Adreça:", bg="slategray3").pack(pady=5)
    adreca_entry = tk.Entry(finestra_mod)
    adreca_entry.pack(pady=5)

    tk.Label(finestra_mod, text="Població:", bg="slategray3").pack(pady=5)
    poblacio_entry = tk.Entry(finestra_mod)
    poblacio_entry.pack(pady=5)

    tk.Label(finestra_mod, text="Web:", bg="slategray3").pack(pady=5)
    web_entry = tk.Entry(finestra_mod)
    web_entry.pack(pady=5)

    tk.Label(finestra_mod, text="Número d'estrelles:", bg="slategray3").pack(pady=5)
    estrelles_entry = tk.Entry(finestra_mod)
    estrelles_entry.pack(pady=5)

    tk.Label(finestra_mod, text="Telèfon:", bg="slategray3").pack(pady=5)
    telefon_entry = tk.Entry(finestra_mod)
    telefon_entry.pack(pady=5)

    tk.Label(finestra_mod, text="ID Director:", bg="slategray3").pack(pady=5)
    director_entry = tk.Entry(finestra_mod)
    director_entry.pack(pady=5)

    tk.Label(finestra_mod, text="ID Gerent:", bg="slategray3").pack(pady=5)
    gerent_entry = tk.Entry(finestra_mod)
    gerent_entry.pack(pady=5)

    def carregar_hotels():
        try:
            conn = conexio_bd()
            if conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id_hotel, nom FROM hotel")
                    hotels = cur.fetchall()
                    hotel_combo['values'] = [f"{h[0]} - {h[1]}" for h in hotels]
        except Exception as e:
            messagebox.showerror("Error", f"Error en carregar hotels: {str(e)}")

    def carregar_dades_hotel(event):
        seleccio = hotel_combo.get()
        if seleccio:
            id_hotel = seleccio.split(' - ')[0]
            try:
                conn = conexio_bd()
                if conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            SELECT nom, adreca, poblacio, web, num_estrelles, 
                            telefon, id_director, id_gerent 
                            FROM hotel WHERE id_hotel = %s
                        """, (id_hotel,))
                        hotel = cur.fetchone()
                        if hotel:
                            nom_entry.delete(0, tk.END)
                            nom_entry.insert(0, hotel[0])
                            adreca_entry.delete(0, tk.END)
                            adreca_entry.insert(0, hotel[1])
                            poblacio_entry.delete(0, tk.END)
                            poblacio_entry.insert(0, hotel[2])
                            web_entry.delete(0, tk.END)
                            if hotel[3]:
                                web_entry.insert(0, hotel[3])
                            estrelles_entry.delete(0, tk.END)
                            estrelles_entry.insert(0, str(hotel[4]))
                            telefon_entry.delete(0, tk.END)
                            if hotel[5]:
                                telefon_entry.insert(0, hotel[5])
                            director_entry.delete(0, tk.END)
                            director_entry.insert(0, str(hotel[6]))
                            gerent_entry.delete(0, tk.END)
                            gerent_entry.insert(0, str(hotel[7]))
            except Exception as e:
                messagebox.showerror("Error", f"Error en carregar dades: {str(e)}")

    def guardar_modificacions():
        seleccio = hotel_combo.get()
        if not seleccio:
            messagebox.showwarning("Advertència", "Si us plau, seleccioneu un hotel")
            return

        id_hotel = seleccio.split(' - ')[0]
        try:
            nom = nom_entry.get()
            adreca = adreca_entry.get()
            poblacio = poblacio_entry.get()
            web = web_entry.get() or None
            num_estrelles = int(estrelles_entry.get())
            telefon = telefon_entry.get()
            id_director = int(director_entry.get())
            id_gerent = int(gerent_entry.get())

            if not all([nom, adreca, poblacio, num_estrelles, id_director, id_gerent]):
                messagebox.showwarning("Advertència", "Si us plau, ompliu tots els camps obligatoris")
                return

            conn = conexio_bd()
            if conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE hotel 
                        SET nom = %s, adreca = %s, poblacio = %s, web = %s, 
                        num_estrelles = %s, telefon = %s, id_director = %s, id_gerent = %s
                        WHERE id_hotel = %s
                    """, (nom, adreca, poblacio, web, num_estrelles, telefon, 
                          id_director, id_gerent, id_hotel))
                conn.commit()
                messagebox.showinfo("Èxit", "Hotel modificat correctament")
                finestra_mod.destroy()
        except ValueError:
            messagebox.showerror("Error", "Els camps numèrics han de ser números vàlids")
        except psycopg2.Error as e:
            # Extreure nomès el missatge principal sense el CONTEXT
            mensaje_error = str(e).split("CONTEXT:")[0].strip()
            
            # Si el missate té format específic de PostgreSQL (ERROR: missatge)
            if mensaje_error.startswith("ERROR:"):
                mensaje_error = mensaje_error[6:].strip()
                
            messagebox.showerror("Error", f"Error en modificar l'hotel: {mensaje_error}")
        except Exception as e:
            messagebox.showerror("Error", f"Error en modificar l'hotel: {str(e)}")

    hotel_combo.bind('<<ComboboxSelected>>', carregar_dades_hotel)
    carregar_hotels()

    frame_botons = tk.Frame(finestra_mod, bg="slategray3")
    frame_botons.pack(pady=20)

    def cancelar():
        if messagebox.askyesno("Confirmar", "Esteu segur que voleu cancel·lar? Es perdran totes les modificacions."):
            finestra_mod.destroy()

    tk.Button(
        frame_botons,
        text="Guardar",
        command=guardar_modificacions,
        font=("Arial", 12),
        width=10
    ).pack(side="left", padx=10)

    tk.Button(
        frame_botons,
        text="Cancel·lar",
        command=cancelar,
        font=("Arial", 12),
        width=10
    ).pack(side="left", padx=10)
