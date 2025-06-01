# Importació de les llibreries necessàries
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from db_connection import conexio_bd
import pandas as pd
from datetime import datetime
import json

def exportar_informe_reserves():
    """Funció per exportar informe de reserves entre dues dates en format JSON"""
    finestra_export = tk.Toplevel()
    finestra_export.title("Exportar Informe de Reserves")
    finestra_export.geometry("500x400")
    finestra_export.configure(bg="slategray3")

    frame_principal = tk.Frame(finestra_export, bg="slategray3")
    frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    frame_hotel_wrapper = tk.Frame(frame_principal, bg="slategray3")
    frame_hotel_wrapper.pack(fill=tk.X, pady=10)
    frame_hotel = tk.Frame(frame_hotel_wrapper, bg="slategray3")
    frame_hotel.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame_hotel, text="Hotel:", bg="slategray3", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
    combo_hotels = ttk.Combobox(frame_hotel, state="readonly", width=30)

    try:
        conn = conexio_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT nom FROM hotel ORDER BY nom")
        hotels = [row[0] for row in cursor.fetchall()]
        combo_hotels['values'] = hotels
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", "Error al carregar els hotels")
    
    combo_hotels.pack(side=tk.LEFT, padx=5)

    frame_dates_wrapper = tk.Frame(frame_principal, bg="slategray3")
    frame_dates_wrapper.pack(pady=20)
    frame_dates = tk.Frame(frame_dates_wrapper, bg="slategray3")
    frame_dates.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame_dates, text="Data Inici:", bg="slategray3", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
    frame_data_inici_wrapper = tk.Frame(frame_dates, bg="slategray3")
    frame_data_inici_wrapper.grid(row=0, column=1, padx=5, pady=5)
    frame_data_inici = tk.Frame(frame_data_inici_wrapper, bg="slategray3")
    frame_data_inici.pack(fill=tk.BOTH, expand=True)

    combo_dia_inici = ttk.Combobox(frame_data_inici, state="readonly", width=3)
    combo_dia_inici['values'] = [str(i).zfill(2) for i in range(1, 32)]
    combo_dia_inici.pack(side=tk.LEFT, padx=2)

    combo_mes_inici = ttk.Combobox(frame_data_inici, state="readonly", width=3)
    combo_mes_inici['values'] = [str(i).zfill(2) for i in range(1, 13)]
    combo_mes_inici.pack(side=tk.LEFT, padx=2)

    combo_any_inici = ttk.Combobox(frame_data_inici, state="readonly", width=5)
    combo_any_inici['values'] = [str(i) for i in range(2000, datetime.now().year + 5)]
    combo_any_inici.pack(side=tk.LEFT, padx=2)

    tk.Label(frame_dates, text="Data Fi:", bg="slategray3", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5)
    frame_data_fi_wrapper = tk.Frame(frame_dates, bg="slategray3")
    frame_data_fi_wrapper.grid(row=1, column=1, padx=5, pady=5)
    frame_data_fi = tk.Frame(frame_data_fi_wrapper, bg="slategray3")
    frame_data_fi.pack(fill=tk.BOTH, expand=True)

    combo_dia_fi = ttk.Combobox(frame_data_fi, state="readonly", width=3)
    combo_dia_fi['values'] = [str(i).zfill(2) for i in range(1, 32)]
    combo_dia_fi.pack(side=tk.LEFT, padx=2)

    combo_mes_fi = ttk.Combobox(frame_data_fi, state="readonly", width=3)
    combo_mes_fi['values'] = [str(i).zfill(2) for i in range(1, 13)]
    combo_mes_fi.pack(side=tk.LEFT, padx=2)

    combo_any_fi = ttk.Combobox(frame_data_fi, state="readonly", width=5)
    combo_any_fi['values'] = [str(i) for i in range(2000, datetime.now().year + 5)]
    combo_any_fi.pack(side=tk.LEFT, padx=2)

    def generar_informe():
        hotel = combo_hotels.get()
        if not hotel:
            messagebox.showwarning("Avís", "Si us plau, selecciona un hotel")
            return

        try:
            data_inici = f"{combo_any_inici.get()}-{combo_mes_inici.get()}-{combo_dia_inici.get()}"
            data_fi = f"{combo_any_fi.get()}-{combo_mes_fi.get()}-{combo_dia_fi.get()}"
            
            if not all([combo_dia_inici.get(), combo_mes_inici.get(), combo_any_inici.get(),
                       combo_dia_fi.get(), combo_mes_fi.get(), combo_any_fi.get()]):
                messagebox.showwarning("Avís", "Si us plau, selecciona les dates completes")
                return
                
            datetime.strptime(data_inici, '%Y-%m-%d')
            datetime.strptime(data_fi, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Format de data incorrecte")
            return

        try:
            conn = conexio_bd()
            cursor = conn.cursor()
            cursor.execute("SELECT id_hotel FROM hotel WHERE nom = %s", (hotel,))
            id_hotel = cursor.fetchone()[0]

            cursor.execute("""
                SELECT 
                    r.id_reserva,
                    h.nom as hotel,
                    c.dni,
                    c.nom,
                    c.cognoms,
                    c.nacionalitat,
                    r.data_inici,
                    r.data_fi,
                    hab.numero as habitacio
                FROM reserva r
                JOIN hotel h ON r.id_hotel = h.id_hotel
                JOIN client c ON r.dni = c.dni
                JOIN habitacio hab ON r.id_habitacio = hab.id_habitacio
                WHERE r.id_hotel = %s 
                AND r.data_inici BETWEEN %s AND %s
                ORDER BY r.data_inici
            """, (id_hotel, data_inici, data_fi))
            
            reserves = cursor.fetchall()
            
            if not reserves:
                messagebox.showinfo("Informació", "No s'han trobat reserves per aquest període")
                return

            dades_json = []
            for reserva in reserves:
                dades_json.append({
                    "dni": reserva[2],
                    "nombre": reserva[3],
                    "apellidos": reserva[4],
                    "fecha_llegada": reserva[6].strftime('%Y-%m-%d'),
                    "fecha_salida": reserva[7].strftime('%Y-%m-%d'),
                    "habitación": str(reserva[8]),
                    "nacionalidad": reserva[5]
                })

            nom_arxiu_defecte = f"dataclysm_{datetime.now().strftime('%Y%m%d')}.json"
            ruta_arxiu = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("Arxius JSON", "*.json")],
                initialfile=nom_arxiu_defecte,
                title="Guardar informe JSON"
            )
            
            if not ruta_arxiu:
                return

            with open(ruta_arxiu, 'w', encoding='utf-8') as f:
                json.dump(dades_json, f, indent=4, ensure_ascii=False)
            
            messagebox.showinfo("Èxit", f"Informe exportat correctament com: {ruta_arxiu}")

            if messagebox.askyesno("Enviar a Mossos", "Voleu enviar aquest informe als Mossos d'Esquadra?"):
                from mossos_api import enviar_dades_mossos
                exit, missatge = enviar_dades_mossos(ruta_arxiu)
                
                if exit:
                    messagebox.showinfo("Èxit", "Dades enviades correctament als Mossos d'Esquadra")
                else:
                    messagebox.showerror("Error", f"Error en enviar les dades: {missatge}")

            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error en generar l'informe: {str(e)}")

    frame_botons_wrapper = tk.Frame(frame_principal, bg="slategray3")
    frame_botons_wrapper.pack(pady=20)
    frame_botons = tk.Frame(frame_botons_wrapper, bg="slategray3")
    frame_botons.pack(fill=tk.BOTH, expand=True)

    def enviar_mossos_directe():
        ruta_arxiu = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("Arxius JSON", "*.json")],
            title="Seleccionar informe JSON per enviar als Mossos"
        )
        
        if ruta_arxiu:
            from mossos_api import enviar_dades_mossos
            exit, missatge = enviar_dades_mossos(ruta_arxiu)
            
            if exit:
                messagebox.showinfo("Èxit", "Dades enviades correctament als Mossos d'Esquadra")
            else:
                messagebox.showerror("Error", f"Error en enviar les dades: {missatge}")

    tk.Button(
        frame_botons,
        text="Generar Informe",
        command=generar_informe,
        bg="white",
        activebackground="slategray3",
        font=("Arial", 12),
        padx=15, pady=8     
    ).pack(side=tk.LEFT, padx=10)

    tk.Button(
        frame_botons,
        text="Exportació Mossos",
        command=enviar_mossos_directe,
        bg="white",
        activebackground="slategray3",
        font=("Arial", 12),
        padx=15, pady=8 
    ).pack(side=tk.LEFT, padx=10)

    tk.Button(
        frame_botons,
        text="Tancar",
        command=finestra_export.destroy,
        bg="white",
        activebackground="slategray3",
        font=("Arial", 12),
        padx=15, pady=8 
    ).pack(side=tk.LEFT, padx=10)
