# Importació de les llibreries necessàries
import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import conexio_bd
import datetime

def realizar_check_in():
    """Funció principal per gestionar el procés de check-in"""
    # Configuració de la finestra principal
    finestra_check_in = tk.Toplevel()
    finestra_check_in.title("Check-in")
    finestra_check_in.geometry("500x400")
    finestra_check_in.configure(bg="slategray3")

    # Marc per mostrar els detalls de la reserva
    details_frame = tk.Frame(finestra_check_in, bg="slategray3")
    details_frame.pack(pady=10, fill="both", expand=True)

    # Font gran per als labels
    font_etiquetes = ("Arial", 16)

    # Creació de les etiquetes per mostrar la informació
    labels = {}
    for field in ["Client", "Hotel", "Habitació", "Data Entrada", "Data Sortida", "Persones"]:
        frame = tk.Frame(details_frame, bg="slategray3")
        frame.pack(fill="x", pady=2)
        tk.Label(frame, text=f"{field}:", width=15, anchor="w", bg="slategray3", font= font_etiquetes).pack(side="left")
        lbl = tk.Label(frame, text="", bg="slategray3")
        lbl.pack(side="left")
        labels[field] = lbl

    # Marc per seleccionar la reserva
    select_frame = tk.Frame(finestra_check_in, bg="slategray3")
    select_frame.pack(pady=10, padx=10, fill="x")

    tk.Label(select_frame, text="Seleccionar Reserva:", bg="slategray3", font= font_etiquetes).pack(side="left", padx=5)
    reserva_combo = ttk.Combobox(select_frame, width=50)
    reserva_combo.pack(side="left", padx=5)

    def mostrar_detalls(event):
        """Funció per mostrar els detalls de la reserva seleccionada"""
        selected = reserva_combo.get()
        if selected:
            id_reserva = selected.split('ID: ')[1].split(' -')[0]
            try:
                conn = conexio_bd()
                if conn:
                    with conn.cursor() as cur:
                        # Consulta per obtenir els detalls de la reserva
                        cur.execute("""
                            SELECT c.nom, c.cognoms, h.nom as hotel_nom,
                                   string_agg(hab.id_habitacio::text, ', ') as habitacions,
                                   r.data_inici, r.data_fi, r.num_persones
                            FROM reserva r
                            JOIN client c ON r.dni = c.dni
                            JOIN hotel h ON r.id_hotel = h.id_hotel
                            JOIN detall_reserva dr ON r.id_reserva = dr.id_reserva
                            JOIN habitacio hab ON dr.id_habitacio = hab.id_habitacio
                            WHERE r.id_reserva = %s
                            GROUP BY c.nom, c.cognoms, h.nom, r.data_inici, r.data_fi, r.num_persones
                        """, (id_reserva,))
                        result = cur.fetchone()
                        if result:
                            # Actualitzar les etiquetes amb la informació
                            labels["Client"].config(text=f"{result[0]} {result[1]}")
                            labels["Hotel"].config(text=result[2])
                            labels["Habitació"].config(text=result[3])
                            labels["Data Entrada"].config(text=result[4])
                            labels["Data Sortida"].config(text=result[5])
                            labels["Persones"].config(text=str(result[6]))
            except Exception as e:
                messagebox.showerror("Error", f"Error en carregar detalls: {str(e)}")

    def carregar_reserves():
        """Funció per carregar les reserves disponibles per fer check-in"""
        try:
            conn = conexio_bd()
            if conn:
                with conn.cursor() as cur:
                    # Consulta per obtenir les reserves pendents de check-in
                    cur.execute("""
                        SELECT DISTINCT r.id_reserva, c.nom, c.cognoms, h.nom as hotel_nom, 
                               r.data_inici, r.data_fi
                        FROM reserva r
                        JOIN client c ON r.dni = c.dni
                        JOIN hotel h ON r.id_hotel = h.id_hotel
                        WHERE r.data_inici >= CURRENT_DATE
                        AND NOT EXISTS (
                            SELECT 1 
                            FROM check_in ci 
                            WHERE ci.id_reserva = r.id_reserva
                        )
                        ORDER BY r.data_inici ASC
                    """)
                    reserves = cur.fetchall()
                    if reserves:
                        # Omplir el combobox amb les reserves disponibles
                        reserva_combo['values'] = [
                            f"ID: {r[0]} - {r[1]} {r[2]} - Hotel: {r[3]} ({r[4].strftime('%d/%m/%Y')} a {r[5].strftime('%d/%m/%Y')})"
                            for r in reserves
                        ]
                    else:
                        reserva_combo['values'] = ["No hi ha reserves pendents"]
        except Exception as e:
            messagebox.showerror("Error", f"Error en carregar reserves: {str(e)}")

    def process_check_in():
        """Funció per processar el check-in de la reserva seleccionada"""
        selected = reserva_combo.get()
        if not selected:
            messagebox.showwarning("Advertència", "Si us plau, seleccioneu una reserva")
            return

        id_reserva = selected.split('ID: ')[1].split(' -')[0]
        try:
            conn = conexio_bd()
            if conn:
                with conn.cursor() as cur:
                    # Obtenir el DNI del client
                    cur.execute("""
                        SELECT dni FROM reserva WHERE id_reserva = %s
                    """, (id_reserva,))
                    dni = cur.fetchone()[0]

                    # Registrar el check-in
                    cur.execute("""
                        INSERT INTO check_in (dni, id_reserva, data_hora)
                        VALUES (%s, %s, CURRENT_TIMESTAMP)
                    """, (dni, id_reserva))

                conn.commit()
                messagebox.showinfo("Èxit", "Check-in realitzat correctament")
                # Actualitzar la interfície
                carregar_reserves()
                for label in labels.values():
                    label.config(text="")
                reserva_combo.set("")
        except Exception as e:
            messagebox.showerror("Error", f"Error en processar check-in: {str(e)}")

    # Marc pels botons
    button_frame = tk.Frame(finestra_check_in, bg="slategray3")
    button_frame.pack(pady=10)

    # Botó per realitzar el check-in
    tk.Button(
        button_frame,
        text="Realitzar Check-in",
        command=process_check_in,
        bg="mediumseagreen",
        fg="white",
        font=("Arial", 12)
    ).pack(side="left", padx=10)

    # Botó per cancel·lar l'operació
    tk.Button(
        button_frame,
        text="Cancel·lar",
        command=finestra_check_in.destroy,
        font=("Arial", 12)
    ).pack(side="left", padx=10)

    # Carregar les reserves inicials i vincular els esdeveniments
    carregar_reserves()
    reserva_combo.bind('<<ComboboxSelected>>', mostrar_detalls)
