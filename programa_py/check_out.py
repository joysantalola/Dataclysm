import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import conexio_bd
import psycopg2

def realizar_check_out():
    """Funció principal per gestionar el procés de check-out"""
    finestra_check_out = tk.Toplevel()
    finestra_check_out.title("Check-out")
    finestra_check_out.geometry("600x500")
    finestra_check_out.configure(bg="slategray3")

    # Títol dins la finestra
    tk.Label(
        finestra_check_out,
        text="Check-out",
        font=("Arial", 22, "bold"),
        bg="slategray3",
        fg="black"
    ).pack(pady=(20, 10))

    # Marc per mostrar els detalls del check-in
    details_frame = tk.Frame(finestra_check_out, bg="slategray3")
    details_frame.pack(pady=10, fill="both", expand=True)

    # Font gran per als labels
    font_etiquetes = ("Arial", 16)

    # Creació de les etiquetes per mostrar la informació
    labels = {}
    for field in ["Client", "Hotel", "Habitació", "Data Check-in", "Treballador"]:
        frame = tk.Frame(details_frame, bg="slategray3")
        frame.pack(fill="x", pady=2)
        tk.Label(frame, text=f"{field}:", width=15, anchor="w", bg="slategray3", font= font_etiquetes).pack(side="left")
        lbl = tk.Label(frame, text="", bg="slategray3", font=font_etiquetes)
        lbl.pack(side="left")
        labels[field] = lbl

    # Marc per seleccionar el check-in
    select_frame = tk.Frame(finestra_check_out, bg="slategray3")
    select_frame.pack(pady=10, padx=10, fill="x")

    tk.Label(select_frame, text="Seleccionar Check-in:", bg="slategray3", font= font_etiquetes).pack(side="left", padx=5)
    checkin_combo = ttk.Combobox(select_frame, width=50)
    checkin_combo.pack(side="left", padx=5)

    def mostrar_detalls(event):
        """Funció per mostrar els detalls del check-in seleccionat"""
        selected = checkin_combo.get()
        if selected:
            id_checkin = selected.split('ID: ')[1].split(' -')[0]
            try:
                conn = conexio_bd()
                if conn:
                    with conn.cursor() as cur:
                        # Consulta per obtenir els detalls del check-in
                        cur.execute("""
                            SELECT c.nom, c.cognoms, h.nom as hotel_nom,
                                   string_agg(hab.id_habitacio::text, ', ') as habitacions,
                                   ci.data_hora,
                                   'Treballador Assignat'
                            FROM check_in ci
                            JOIN reserva r ON ci.id_reserva = r.id_reserva
                            JOIN client c ON r.dni = c.dni
                            JOIN hotel h ON r.id_hotel = h.id_hotel
                            JOIN detall_reserva dr ON r.id_reserva = dr.id_reserva
                            JOIN habitacio hab ON dr.id_habitacio = hab.id_habitacio
                            WHERE ci.id_check_in = %s
                            GROUP BY c.nom, c.cognoms, h.nom, ci.data_hora
                        """, (id_checkin,))
                        result = cur.fetchone()
                        if result:
                            # Actualitzar les etiquetes amb la informació
                            labels["Client"].config(text=f"{result[0]} {result[1]}")
                            labels["Hotel"].config(text=result[2])
                            labels["Habitació"].config(text=result[3])
                            labels["Data Check-in"].config(text=result[4])
                            labels["Treballador"].config(text=result[5])
            except Exception as e:
                messagebox.showerror("Error", f"Error en carregar detalls: {str(e)}")

    def carregar_checkins():
        """Funció per carregar tots els check-ins pendents de check-out"""
        try:
            conn = conexio_bd()
            if conn:
                with conn.cursor() as cur:
                    # Consulta per obtenir els check-ins sense check-out
                    cur.execute("""
                        SELECT ci.id_check_in, c.nom, c.cognoms, h.nom as hotel_nom, 
                               ci.data_hora
                        FROM check_in ci
                        JOIN reserva r ON ci.id_reserva = r.id_reserva
                        JOIN client c ON r.dni = c.dni
                        JOIN hotel h ON r.id_hotel = h.id_hotel
                        LEFT JOIN check_out co ON ci.id_reserva = co.id_reserva
                        WHERE co.id_check_out IS NULL
                        ORDER BY ci.data_hora DESC
                    """)
                    checkins = cur.fetchall()
                    if checkins:
                        # Omplir el combobox amb els check-ins disponibles
                        checkin_combo['values'] = [
                            f"ID: {ci[0]} - {ci[1]} {ci[2]} - Hotel: {ci[3]} ({ci[4]})"
                            for ci in checkins
                        ]
                    else:
                        checkin_combo['values'] = ["No hi ha check-ins pendents"]
        except Exception as e:
            messagebox.showerror("Error", f"Error en carregar check-ins: {str(e)}")

    def realizar_checkout():
        """Funció per processar el check-out"""
        selected = checkin_combo.get()
        if not selected:
            messagebox.showwarning("Avís", "Si us plau, selecciona un check-in")
            return
    
        id_checkin = selected.split('ID: ')[1].split(' -')[0]
        try:
            conn = conexio_bd()
            if conn:
                with conn.cursor() as cur:
                    # Inserir el nou check-out
                    cur.execute("""
                        INSERT INTO check_out (dni, id_reserva, data_hora)
                        SELECT ci.dni, ci.id_reserva, CURRENT_TIMESTAMP
                        FROM check_in ci
                        WHERE ci.id_check_in = %s
                    """, (id_checkin,))
                    conn.commit()
                    messagebox.showinfo("Èxit", "Check-out realitzat correctament")
                    # Actualitzar la interfície
                    carregar_checkins()
                    for label in labels.values():
                        label.config(text="")
                    checkin_combo.set("")
        except psycopg2.Error as db_error:
            messagebox.showerror("Error", f"Error de base de dades: {db_error.pgcode} - {db_error.pgerror}")
        except Exception as e:
            messagebox.showerror("Error", f"Error en realitzar check-out: {str(e)}")

    # Marc pels botons
    button_frame = tk.Frame(finestra_check_out, bg="slategray3")
    button_frame.pack(pady=20)

    # Botó per realitzar el check-out
    tk.Button(
        button_frame,
        text="Realitzar Check-out",
        command=realizar_checkout,
        bg="mediumseagreen",
        fg="white",
        font=("Arial", 12)
    ).pack(side="left", padx=10)

    # Botó per cancel·lar l'operació
    tk.Button(
        button_frame,
        text="Cancel·lar",
        command=finestra_check_out.destroy,
        font=("Arial", 12)
    ).pack(side="left", padx=10)

    # Carregar els check-ins inicials i vincular els esdeveniments
    carregar_checkins()
    checkin_combo.bind('<<ComboboxSelected>>', mostrar_detalls)
