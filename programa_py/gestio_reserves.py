# Importació de les llibreries necessàries per la gestió de reserves
import tkinter as tk
from tkinter import messagebox, ttk
from db_connection import conexio_bd
import bloc_logging
import psycopg2


# Afegir reserva
def afegir_reserva():
    """Funció per afegir una nova reserva"""
    # Configuració de la finestra principal per afegir reserves
    finestra_nou = tk.Toplevel()
    finestra_nou.title("Afegir Nova Reserva")
    finestra_nou.geometry("500x550")
    finestra_nou.configure(bg="slategray3")

    # Crear formulari
    tk.Label(finestra_nou, text="Hotel:", bg="slategray3").pack(pady=5)
    hotel_combo = ttk.Combobox(finestra_nou)
    hotel_combo.pack(pady=5)

    tk.Label(finestra_nou, text="Client:", bg="slategray3").pack(pady=5)
    client_combo = ttk.Combobox(finestra_nou)
    client_combo.pack(pady=5)

    tk.Label(finestra_nou, text="Habitació:", bg="slategray3").pack(pady=5)
    habitacio_combo = ttk.Combobox(finestra_nou)
    habitacio_combo.pack(pady=5)

    tk.Label(finestra_nou, text="Data d'entrada (YYYY-MM-DD):", bg="slategray3").pack(pady=5)
    data_entrada_entry = tk.Entry(finestra_nou)
    data_entrada_entry.pack(pady=5)

    tk.Label(finestra_nou, text="Data de sortida (YYYY-MM-DD):", bg="slategray3").pack(pady=5)
    data_sortida_entry = tk.Entry(finestra_nou)
    data_sortida_entry.pack(pady=5)

    tk.Label(finestra_nou, text="Número de persones:", bg="slategray3").pack(pady=5)
    persones_entry = tk.Entry(finestra_nou)
    persones_entry.pack(pady=5)

    def carregar_hotels():
        """Funció per obtenir i mostrar la llista d'hotels disponibles"""
        try:
            conn = conexio_bd()
            if conn:
                with conn.cursor() as cur:
                    # Consulta per obtenir tots els hotels
                    cur.execute("SELECT id_hotel, nom FROM hotel")
                    hotels = cur.fetchall()
                    hotel_combo['values'] = [f"{h[0]} - {h[1]}" for h in hotels]
        except Exception as e:
            messagebox.showerror("Error", f"Error en carregar hotels: {str(e)}")

    def carregar_clients():
        """Funció per obtenir i mostrar la llista de clients registrats"""
        try:
            conn = conexio_bd()
            if conn:
                with conn.cursor() as cur:
                    # Consulta per obtenir tots els clients
                    cur.execute("SELECT dni, nom, cognoms FROM client")
                    clients = cur.fetchall()
                    client_combo['values'] = [f"{c[0]} - {c[1]} {c[2]}" for c in clients]
        except Exception as e:
            messagebox.showerror("Error", f"Error en carregar clients: {str(e)}")

    def carregar_habitacions(event=None):
        """Funció per carregar les habitacions disponibles segons l'hotel seleccionat"""
        try:
            hotel_seleccionat = hotel_combo.get()
            if not hotel_seleccionat:
                habitacio_combo['values'] = []
                return

            # Obtenir l'ID de l'hotel i carregar les seves habitacions
            id_hotel = hotel_seleccionat.split(' - ')[0]
            conn = conexio_bd()
            if conn:
                with conn.cursor() as cur:
                    # Consulta per obtenir les habitacions de l'hotel seleccionat
                    cur.execute("""
                        SELECT id_habitacio, numero, tipus_habitacio 
                        FROM habitacio 
                        WHERE id_hotel = %s
                    """, (id_hotel,))
                    habitacions = cur.fetchall()
                    habitacio_combo['values'] = [
                        f"{h[0]} - Hab. {h[1]} ({h[2]})" for h in habitacions
                    ]
        except Exception as e:
            messagebox.showerror("Error", f"Error en carregar habitacions: {str(e)}")

    def guardar_reserva():
        # Obtenir valors
        try:
            hotel_seleccionat = hotel_combo.get()
            client_seleccionat = client_combo.get()
            habitacio_seleccionada = habitacio_combo.get()
            
            if not hotel_seleccionat or not client_seleccionat or not habitacio_seleccionada:
                messagebox.showwarning("Advertència", "Si us plau, seleccioneu un hotel, un client i una habitació")
                return
                
            id_hotel = hotel_seleccionat.split(' - ')[0]
            dni = client_seleccionat.split(' - ')[0]
            id_habitacio = habitacio_seleccionada.split(' - ')[0]
            data_inici = data_entrada_entry.get()
            data_fi = data_sortida_entry.get()
            num_persones = int(persones_entry.get())

            if not all([data_inici, data_fi, num_persones]):
                messagebox.showwarning("Advertència", "Si us plau, ompliu tots els camps obligatoris")
                return

            confirmacio = messagebox.askyesno(
                "Confirmar",
                f"Esteu segur que voleu afegir la reserva?\n\n" +
                f"Hotel: {hotel_seleccionat}\n" +
                f"Client: {client_seleccionat}\n" +
                f"Habitació: {habitacio_seleccionada}\n" +
                f"Data d'entrada: {data_inici}\n" +
                f"Data de sortida: {data_fi}\n" +
                f"Persones: {num_persones}\n"
            )

            if not confirmacio:
                return

            conn = conexio_bd()
            if conn:
                with conn.cursor() as cur:
                    # Insert into reserva table and get the new id_reserva
                    cur.execute(
                        """INSERT INTO reserva (id_hotel, dni, data_inici, data_fi, 
                        num_persones) 
                        VALUES (%s, %s, %s, %s, %s) RETURNING id_reserva""",
                        (id_hotel, dni, data_inici, data_fi, num_persones)
                    )
                    id_reserva = cur.fetchone()[0]
                    
                    # Insert into detall_reserva table
                    cur.execute(
                        """INSERT INTO detall_reserva (id_reserva, id_habitacio) 
                        VALUES (%s, %s)""",
                        (id_reserva, id_habitacio)
                    )
                    
                conn.commit()
                messagebox.showinfo("Èxit", "Reserva afegida correctament")
                finestra_nou.destroy()
        except ValueError:
            messagebox.showerror("Error", "Els camps numèrics han de ser números vàlids")
        except psycopg2.Error as e:
            # Extract only the main message without the CONTEXT
            mensaje_error = str(e).split("CONTEXT:")[0].strip()
            
            # If the message has PostgreSQL specific format (ERROR: message)
            if mensaje_error.startswith("ERROR:"):
                mensaje_error = mensaje_error[6:].strip()
                
            messagebox.showerror("Error", f"Error en guardar la reserva: {mensaje_error}")
        except Exception as e:
            messagebox.showerror("Error", f"Error en guardar la reserva: {str(e)}")

    # Bind hotel selection to load available rooms
    hotel_combo.bind('<<ComboboxSelected>>', carregar_habitacions)
    
    # Carregar dades per als combobox
    carregar_hotels()
    carregar_clients()

    frame_botons = tk.Frame(finestra_nou, bg="slategray3")
    frame_botons.pack(pady=20)

    def cancelar():
        if messagebox.askyesno("Confirmar", "Esteu segur que voleu cancel·lar? Es perdran totes les dades introduïdes."):
            finestra_nou.destroy()

    tk.Button(
        frame_botons,
        text="Guardar",
        command=guardar_reserva,
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

# Elininar reserva
def eliminar_reserva():
    """Funció per eliminar una reserva existent"""
    finestra_elim = tk.Toplevel()
    finestra_elim.title("Eliminar Reserva")
    finestra_elim.geometry("500x400")
    finestra_elim.configure(bg="slategray3")

    tk.Label(finestra_elim, text="Seleccionar Reserva:", bg="slategray3").pack(pady=10)
    reserva_combo = ttk.Combobox(finestra_elim, width=50)
    reserva_combo.pack(pady=10)

    # Frame per mostrar detalls
    frame_detalls = tk.Frame(finestra_elim, bg="slategray3")
    frame_detalls.pack(pady=10, fill="both", expand=True)

    # Labels per mostrar detalls
    detall_labels = {}
    for camp in ["Hotel", "Client", "Habitació", "Data entrada", "Data sortida", "Persones", "Preu"]:
        frame = tk.Frame(frame_detalls, bg="slategray3")
        frame.pack(fill="x", pady=2)
        tk.Label(frame, text=f"{camp}:", width=15, anchor="w", bg="slategray3").pack(side="left")
        lbl = tk.Label(frame, text="", bg="slategray3")
        lbl.pack(side="left", fill="x", expand=True)
        detall_labels[camp] = lbl

    def carregar_reserves():
        try:
            conn = conexio_bd()
            if conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT r.id_reserva, h.nom, CONCAT(c.nom, ' ', c.cognoms), 
                        r.data_inici, r.data_fi
                        FROM reserva r
                        JOIN hotel h ON r.id_hotel = h.id_hotel
                        JOIN client c ON r.dni = c.dni
                        ORDER BY r.data_inici DESC
                    """)
                    reserves = cur.fetchall()
                    reserva_combo['values'] = [
                        f"{r[0]} - {r[1]} - {r[2]} ({r[3]} a {r[4]})" for r in reserves
                    ]
        except Exception as e:
            messagebox.showerror("Error", f"Error en carregar reserves: {str(e)}")

    def mostrar_detalls_reserva(event):
        seleccio = reserva_combo.get()
        if seleccio:
            id_reserva = seleccio.split(' - ')[0]
            try:
                conn = conexio_bd()
                if conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            SELECT h.nom, CONCAT(c.nom, ' ', c.cognoms), 
                            hab.numero, r.data_inici, r.data_fi, 
                            r.num_persones
                            FROM reserva r
                            JOIN hotel h ON r.id_hotel = h.id_hotel
                            JOIN client c ON r.dni = c.dni
                            JOIN detall_reserva dr ON r.id_reserva = dr.id_reserva
                            JOIN habitacio hab ON dr.id_habitacio = hab.id_habitacio
                            WHERE r.id_reserva = %s
                        """, (id_reserva,))
                        reserva = cur.fetchone()
                        if reserva:
                            detall_labels["Hotel"].config(text=reserva[0])
                            detall_labels["Client"].config(text=reserva[1])
                            detall_labels["Habitació"].config(text=f"Hab. {reserva[2]}")
                            detall_labels["Data entrada"].config(text=reserva[3])
                            detall_labels["Data sortida"].config(text=reserva[4])
                            detall_labels["Persones"].config(text=str(reserva[5]))
                            # Remove reference to reserva[6] since it doesn't exist
                            detall_labels["Preu"].config(text="N/A")
            except Exception as e:
                messagebox.showerror("Error", f"Error en carregar detalls: {str(e)}")

    def confirmar_eliminacio():
        seleccio = reserva_combo.get()
        if not seleccio:
            messagebox.showwarning("Advertència", "Si us plau, seleccioneu una reserva")
            return

        id_reserva = seleccio.split(' - ')[0]
        confirmacio = messagebox.askyesno(
            "Confirmar Eliminació",
            f"Esteu segur que voleu eliminar la reserva seleccionada?\n\n{seleccio}"
        )

        if not confirmacio:
            return

        try:
            conn = conexio_bd()
            if conn:
                with conn.cursor() as cur:
                    # First delete from detall_reserva
                    cur.execute("DELETE FROM detall_reserva WHERE id_reserva = %s", (id_reserva,))
                    # Then delete from reserva
                    cur.execute("DELETE FROM reserva WHERE id_reserva = %s", (id_reserva,))
                conn.commit()
                messagebox.showinfo("Èxit", "Reserva eliminada correctament")
                carregar_reserves()
                # Netejar detalls
                for lbl in detall_labels.values():
                    lbl.config(text="")
                reserva_combo.set("")
        except psycopg2.Error as e:
            # Extract only the main message without the CONTEXT
            mensaje_error = str(e).split("CONTEXT:")[0].strip()
            
            # If the message has PostgreSQL specific format (ERROR: message)
            if mensaje_error.startswith("ERROR:"):
                mensaje_error = mensaje_error[6:].strip()
                
            messagebox.showerror("Error", f"Error en eliminar la reserva: {mensaje_error}")
        except Exception as e:
            messagebox.showerror("Error", f"Error en eliminar la reserva: {str(e)}")

    reserva_combo.bind('<<ComboboxSelected>>', mostrar_detalls_reserva)
    carregar_reserves()

    frame_botons = tk.Frame(finestra_elim, bg="slategray3")
    frame_botons.pack(pady=20)

    tk.Button(
        frame_botons,
        text="Eliminar",
        command=confirmar_eliminacio,
        font=("Arial", 12),
        width=10,
        bg="red",
        fg="white"
    ).pack(side="left", padx=10)

    tk.Button(
        frame_botons,
        text="Cancel·lar",
        command=finestra_elim.destroy,
        font=("Arial", 12),
        width=10
    ).pack(side="left", padx=10)


# Modificar reserva
def modificar_reserva():
    """Funció per modificar una reserva existent"""
    finestra_mod = tk.Toplevel()
    finestra_mod.title("Modificar Reserva")
    finestra_mod.geometry("500x600")
    finestra_mod.configure(bg="slategray3")

    tk.Label(finestra_mod, text="Seleccionar Reserva:", bg="slategray3").pack(pady=5)
    reserva_combo = ttk.Combobox(finestra_mod, width=50)
    reserva_combo.pack(pady=5)

    # Camps per modificar
    tk.Label(finestra_mod, text="Hotel:", bg="slategray3").pack(pady=5)
    hotel_combo = ttk.Combobox(finestra_mod)
    hotel_combo.pack(pady=5)

    tk.Label(finestra_mod, text="Client:", bg="slategray3").pack(pady=5)
    client_combo = ttk.Combobox(finestra_mod)
    client_combo.pack(pady=5)
    
    tk.Label(finestra_mod, text="Habitació:", bg="slategray3").pack(pady=5)
    habitacio_combo = ttk.Combobox(finestra_mod)
    habitacio_combo.pack(pady=5)

    tk.Label(finestra_mod, text="Data d'entrada (YYYY-MM-DD):", bg="slategray3").pack(pady=5)
    data_entrada_entry = tk.Entry(finestra_mod)
    data_entrada_entry.pack(pady=5)

    tk.Label(finestra_mod, text="Data de sortida (YYYY-MM-DD):", bg="slategray3").pack(pady=5)
    data_sortida_entry = tk.Entry(finestra_mod)
    data_sortida_entry.pack(pady=5)

    tk.Label(finestra_mod, text="Número de persones:", bg="slategray3").pack(pady=5)
    persones_entry = tk.Entry(finestra_mod)
    persones_entry.pack(pady=5)

    def carregar_reserves():
        try:
            conn = conexio_bd()
            if conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT r.id_reserva, h.nom, CONCAT(c.nom, ' ', c.cognoms), 
                        r.data_inici, r.data_fi
                        FROM reserva r
                        JOIN hotel h ON r.id_hotel = h.id_hotel
                        JOIN client c ON r.dni = c.dni
                        ORDER BY r.data_inici DESC
                    """)
                    reserves = cur.fetchall()
                    reserva_combo['values'] = [
                        f"{r[0]} - {r[1]} - {r[2]} ({r[3]} a {r[4]})" for r in reserves
                    ]
        except Exception as e:
            messagebox.showerror("Error", f"Error en carregar reserves: {str(e)}")

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

    def carregar_clients():
        try:
            conn = conexio_bd()
            if conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT dni, nom, cognoms FROM client")
                    clients = cur.fetchall()
                    client_combo['values'] = [f"{c[0]} - {c[1]} {c[2]}" for c in clients]
        except Exception as e:
            messagebox.showerror("Error", f"Error en carregar clients: {str(e)}")
            
    def carregar_habitacions(event=None):
        try:
            hotel_seleccionat = hotel_combo.get()
            if not hotel_seleccionat:
                habitacio_combo['values'] = []
                return
                
            id_hotel = hotel_seleccionat.split(' - ')[0]
            conn = conexio_bd()
            if conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT id_habitacio, numero, tipus_habitacio 
                        FROM habitacio 
                        WHERE id_hotel = %s
                    """, (id_hotel,))
                    habitacions = cur.fetchall()
                    habitacio_combo['values'] = [
                        f"{h[0]} - Hab. {h[1]} ({h[2]})" for h in habitacions
                    ]
        except Exception as e:
            messagebox.showerror("Error", f"Error en carregar habitacions: {str(e)}")

    def carregar_dades_reserva(event):
        seleccio = reserva_combo.get()
        if seleccio:
            id_reserva = seleccio.split(' - ')[0]
            try:
                conn = conexio_bd()
                if conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            SELECT r.id_hotel, r.dni, r.data_inici, r.data_fi, 
                            r.num_persones,
                            h.nom, CONCAT(c.nom, ' ', c.cognoms),
                            dr.id_habitacio, hab.numero, hab.tipus_habitacio
                            FROM reserva r
                            JOIN hotel h ON r.id_hotel = h.id_hotel
                            JOIN client c ON r.dni = c.dni
                            JOIN detall_reserva dr ON r.id_reserva = dr.id_reserva
                            JOIN habitacio hab ON dr.id_habitacio = hab.id_habitacio
                            WHERE r.id_reserva = %s
                        """, (id_reserva,))
                        reserva = cur.fetchone()
                        if reserva:
                            # Seleccionar hotel i client als combobox
                            hotel_combo.set(f"{reserva[0]} - {reserva[5]}")
                            client_combo.set(f"{reserva[1]} - {reserva[6]}")
                            
                            # Carregar habitacions del hotel seleccionat
                            carregar_habitacions()
                            
                            # Seleccionar habitació
                            habitacio_combo.set(f"{reserva[7]} - Hab. {reserva[8]} ({reserva[9]})")
                            
                            # Omplir camps
                            data_entrada_entry.delete(0, tk.END)
                            data_entrada_entry.insert(0, reserva[2])
                            data_sortida_entry.delete(0, tk.END)
                            data_sortida_entry.insert(0, reserva[3])
                            persones_entry.delete(0, tk.END)
                            persones_entry.insert(0, str(reserva[4]))
                            # Remove reference to preu_entry since it doesn't exist
            except Exception as e:
                messagebox.showerror("Error", f"Error en carregar dades: {str(e)}")

    def guardar_modificacions():
        seleccio = reserva_combo.get()
        if not seleccio:
            messagebox.showwarning("Advertència", "Si us plau, seleccioneu una reserva")
            return

        id_reserva = seleccio.split(' - ')[0]
        try:
            hotel_seleccionat = hotel_combo.get()
            client_seleccionat = client_combo.get()
            habitacio_seleccionada = habitacio_combo.get()
            
            if not hotel_seleccionat or not client_seleccionat or not habitacio_seleccionada:
                messagebox.showwarning("Advertència", "Si us plau, seleccioneu un hotel, un client i una habitació")
                return
                
            id_hotel = hotel_seleccionat.split(' - ')[0]
            dni = client_seleccionat.split(' - ')[0]
            id_habitacio = habitacio_seleccionada.split(' - ')[0]
            data_inici = data_entrada_entry.get()
            data_fi = data_sortida_entry.get()
            num_persones = int(persones_entry.get())

            if not all([data_inici, data_fi, num_persones]):
                messagebox.showwarning("Advertència", "Si us plau, ompliu tots els camps obligatoris")
                return

            confirmacio = messagebox.askyesno(
                "Confirmar",
                f"Esteu segur que voleu modificar la reserva?\n\n" +
                f"Hotel: {hotel_seleccionat}\n" +
                f"Client: {client_seleccionat}\n" +
                f"Habitació: {habitacio_seleccionada}\n" +
                f"Data d'entrada: {data_inici}\n" +
                f"Data de sortida: {data_fi}\n" +
                f"Persones: {num_persones}\n" 
            )

            if not confirmacio:
                return

            conn = conexio_bd()
            if conn:
                with conn.cursor() as cur:
                    # Update reserva table
                    cur.execute("""
                        UPDATE reserva 
                        SET id_hotel = %s, dni = %s, data_inici = %s, data_fi = %s,
                        num_persones = %s
                        WHERE id_reserva = %s
                    """, (id_hotel, dni, data_inici, data_fi, 
                          num_persones, id_reserva))
                    
                    # Update detall_reserva table - Fixed missing parameter
                    cur.execute("""
                        UPDATE detall_reserva 
                        SET id_habitacio = %s
                        WHERE id_reserva = %s
                    """, (id_habitacio, id_reserva))
                    
                conn.commit()
                messagebox.showinfo("Èxit", "Reserva modificada correctament")
                finestra_mod.destroy()
        except ValueError:
            messagebox.showerror("Error", "Els camps numèrics han de ser números vàlids")
        except psycopg2.Error as e:
            # Extract only the main message without the CONTEXT
            mensaje_error = str(e).split("CONTEXT:")[0].strip()
            
            # If the message has PostgreSQL specific format (ERROR: message)
            if mensaje_error.startswith("ERROR:"):
                mensaje_error = mensaje_error[6:].strip()
                
            messagebox.showerror("Error", f"Error en modificar la reserva: {mensaje_error}")
        except Exception as e:
            messagebox.showerror("Error", f"Error en modificar la reserva: {str(e)}")

    # Bind hotel selection to load available rooms
    hotel_combo.bind('<<ComboboxSelected>>', carregar_habitacions)
    
    # Carregar dades
    reserva_combo.bind('<<ComboboxSelected>>', carregar_dades_reserva)
    carregar_reserves()
    carregar_hotels()
    carregar_clients()

    frame_botons = tk.Frame(finestra_mod, bg="slategray3")
    frame_botons.pack(pady=20)

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
        command=finestra_mod.destroy,
        font=("Arial", 12),
        width=10
    ).pack(side="left", padx=10)

def mostrar_menu_reserves():
    """Funció per mostrar el menú de gestió de reserves"""
    finestra_reserves = tk.Toplevel()
    finestra_reserves.title("Gestió de Reserves")
    finestra_reserves.geometry("400x300")
    finestra_reserves.configure(bg="slategray3")
    
    # Crear botons per a les diferents opcions
    tk.Button(
        finestra_reserves,
        text="Afegir Reserva",
        command=afegir_reserva,
        font=("Arial", 12),
        width=20,
        height=2
    ).pack(pady=15)
    
    tk.Button(
        finestra_reserves,
        text="Modificar Reserva",
        command=modificar_reserva,
        font=("Arial", 12),
        width=20,
        height=2
    ).pack(pady=15)
    
    tk.Button(
        finestra_reserves,
        text="Eliminar Reserva",
        command=eliminar_reserva,
        font=("Arial", 12),
        width=20,
        height=2
    ).pack(pady=15)
