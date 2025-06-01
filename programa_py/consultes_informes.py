import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import conexio_bd

def obrir_resum_hotel():
    finestra_resum = tk.Toplevel()
    finestra_resum.title("Resum Hotel")
    finestra_resum.geometry("1200x300")
    finestra_resum.configure(bg="slategray3")

    frame_principal = tk.Frame(finestra_resum, bg="slategray3")
    frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    frame_seleccio = tk.Frame(frame_principal, bg="slategray3")
    frame_seleccio.pack(fill=tk.X, pady=(0, 10))

    tk.Label(
        frame_seleccio,
        text="Seleccionar Hotel:",
        font=("Arial", 10),
        bg="slategray3"
    ).pack(side=tk.LEFT, padx=5)

    combo_hotels = ttk.Combobox(
        frame_seleccio,
        state="readonly",
        width=50
    )

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

    # Treeview per mostrar el resum
    columns = [
        "Hotel", "Habitacions", "Recepcionista", "Director", "Cuiner", 
        "Gerent", "Seguretat", "Manteniment", "Netejador", "Total Personal"
    ]
    tree = ttk.Treeview(frame_principal, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=110, anchor="center")

    tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def mostrar_resum():
        hotel_seleccionat = combo_hotels.get()
        if not hotel_seleccionat:
            messagebox.showwarning("Avís", "Si us plau, selecciona un hotel")
            return

        for item in tree.get_children():
            tree.delete(item)

        try:
            conn = conexio_bd()
            cursor = conn.cursor()

            cursor.execute("SELECT id_hotel FROM hotel WHERE nom = %s", (hotel_seleccionat,))
            id_hotel = cursor.fetchone()[0]

            # Total habitacions
            cursor.execute("SELECT COUNT(*) FROM habitacio WHERE id_hotel = %s", (id_hotel,))
            total_habitacions = cursor.fetchone()[0]

            # Personal per tipus
            cursor.execute("""
                SELECT tipus_empleat, COUNT(*) 
                FROM treballador 
                WHERE id_hotel = %s 
                GROUP BY tipus_empleat
            """, (id_hotel,))
            personal = dict(cursor.fetchall())

            # Definir tipus fixes
            tipus_fixos = [
                "Recepcionista", "Director", "Cuiner",
                "Gerent", "Seguretat", "Manteniment", "Netejador"
            ]

            totals = {tipus: personal.get(tipus, 0) for tipus in tipus_fixos}
            total_personal = sum(totals.values())

            tree.insert("", "end", values=(
                hotel_seleccionat,
                total_habitacions,
                totals["Recepcionista"],
                totals["Director"],
                totals["Cuiner"],
                totals["Gerent"],
                totals["Seguretat"],
                totals["Manteniment"],
                totals["Netejador"],
                total_personal
            ))

            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtenir les dades: {str(e)}")

    combo_hotels.bind('<<ComboboxSelected>>', lambda e: mostrar_resum())

    ttk.Button(
        finestra_resum,
        text="Tancar",
        command=finestra_resum.destroy
    ).pack(pady=10)



def obrir_informe_personal():
    finestra_personal = tk.Toplevel()
    finestra_personal.title("Empleats dels Hotels")
    finestra_personal.geometry("1400x600")
    finestra_personal.configure(bg="slategray3")

    # Frame principal (tk en lloc de ttk)
    frame_principal = tk.Frame(finestra_personal, bg="slategray3")
    frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Frame per la selecció d'hotel (tk en lloc de ttk)
    frame_seleccio = tk.Frame(frame_principal, bg="slategray3")
    frame_seleccio.pack(fill=tk.X, pady=(0, 10))

    tk.Label(
        frame_seleccio,
        text="Seleccionar Hotel:",
        font=("Arial", 10),
        bg="slategray3"
    ).pack(side=tk.LEFT, padx=5)

    combo_hotels_personal = ttk.Combobox(
        frame_seleccio,
        state="readonly",
        width=50
    )
    
    try:
        conn = conexio_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT nom FROM hotel ORDER BY nom")
        hotels = [row[0] for row in cursor.fetchall()]
        combo_hotels_personal['values'] = hotels
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", "Error al carregar els hotels")
    
    combo_hotels_personal.pack(side=tk.LEFT, padx=5)

    # Crear Treeview per mostrar les dades
    columns = ("DNI", "Nom Complet", "Tipus Personal", "Data Naixement", "Telèfon", "Anys Experiència", "Idiomes", "Categoria", "Últim Treball")
    tree = ttk.Treeview(frame_principal, columns=columns, show="headings")

    # Configurar les columnes
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def actualitzar_dades():
        hotel_seleccionat = combo_hotels_personal.get()
        if not hotel_seleccionat:
            return

        # Netejar dades anteriors
        for item in tree.get_children():
            tree.delete(item)

        try:
            conn = conexio_bd()
            cursor = conn.cursor()
            
            # Obtenir id_hotel
            cursor.execute("SELECT id_hotel FROM hotel WHERE nom = %s", (hotel_seleccionat,))
            id_hotel = cursor.fetchone()[0]

            # Consulta millorada per obtenir totes les dades dels empleats
            cursor.execute("""
                SELECT 
                    t.dni,
                    t.nom || ' ' || t.cognoms as nom_complet,
                    t.tipus_empleat,
                    TO_CHAR(t.data_naixement, 'DD/MM/YYYY') as data_naixement,
                    COALESCE(t.telefon, '-') as telefon,
                    COALESCE(pr.anys_experiencia::text, '-') as experiencia,
                    COALESCE(
                        (SELECT STRING_AGG(
                            'Parla: ' || i.nivell_parla || 
                            ', Entén: ' || i.nivell_enten || 
                            ', Escriu: ' || i.nivell_escriu,
                            '; '
                        )
                        FROM idioma i 
                        WHERE i.id_treballador = pr.id_treballador
                        ), '-') as idiomes,
                    COALESCE(pc.categoria, '-') as categoria,
                    COALESCE(pc.ultim_treball, '-') as ultim_treball
                FROM treballador t
                LEFT JOIN personal_recepcio pr ON t.id_treballador = pr.id_treballador
                LEFT JOIN personal_cuina pc ON t.id_treballador = pc.id_treballador
                WHERE t.id_hotel = %s
                ORDER BY t.cognoms, t.nom
            """, (id_hotel,))

            # Inserir dades a la taula
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)

            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtenir les dades: {str(e)}")

    # Vincular l'actualització a la selecció del combobox
    combo_hotels_personal.bind('<<ComboboxSelected>>', lambda e: actualitzar_dades())

    # Botó per tancar
    ttk.Button(
        finestra_personal,
        text="Tancar",
        command=finestra_personal.destroy
    ).pack(pady=10)

    
def obrir_informe_reserves():
    """Funció que mostra l'informe de reserves filtrat per hotel"""
    finestra_reserves = tk.Toplevel()
    finestra_reserves.title("Informe Reserves")
    finestra_reserves.geometry("900x600")
    finestra_reserves.configure(bg="slategray3")

    # Frame principal (tk en lloc de ttk)
    frame_principal = tk.Frame(finestra_reserves, bg="slategray3")
    frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Frame per la selecció d'hotel (tk en lloc de ttk)
    frame_seleccio = tk.Frame(frame_principal, bg="slategray3")
    frame_seleccio.pack(fill=tk.X, pady=(0, 10))

    tk.Label(
        frame_seleccio,
        text="Seleccionar Hotel:",
        font=("Arial", 10),
        bg="slategray3"
    ).pack(side=tk.LEFT, padx=5)

    combo_hotels = ttk.Combobox(
        frame_seleccio,
        state="readonly",
        width=50
    )
    combo_hotels.pack(side=tk.LEFT, padx=5)

    # Crear Treeview
    columns = ("Hotel", "Habitació", "Client", "Data Entrada", "Data Sortida", "Persones")
    tree = ttk.Treeview(frame_principal, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def carregar_hotels():
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

    def mostrar_reserves_per_hotel(event=None):
        hotel_seleccionat = combo_hotels.get()
        if not hotel_seleccionat:
            return

        # Netejar dades anteriors
        for item in tree.get_children():
            tree.delete(item)

        try:
            conn = conexio_bd()
            cursor = conn.cursor()
            # Obtenir id_hotel
            cursor.execute("SELECT id_hotel FROM hotel WHERE nom = %s", (hotel_seleccionat,))
            id_hotel = cursor.fetchone()[0]

            cursor.execute("""
                SELECT 
                    h.nom as hotel,
                    STRING_AGG(CONCAT('Hab. ', hab.numero, ' (', hab.tipus_habitacio, ')'), ', ') as habitacions,
                    CONCAT(c.nom, ' ', c.cognoms) as client,
                    r.data_inici,
                    r.data_fi,
                    r.num_persones
                FROM reserva r
                JOIN hotel h ON r.id_hotel = h.id_hotel
                JOIN client c ON r.dni = c.dni
                JOIN detall_reserva dr ON r.id_reserva = dr.id_reserva
                JOIN habitacio hab ON dr.id_habitacio = hab.id_habitacio
                WHERE h.id_hotel = %s
                GROUP BY h.nom, c.nom, c.cognoms, r.data_inici, r.data_fi, r.num_persones
                ORDER BY r.data_inici
            """, (id_hotel,))
            reserves = cursor.fetchall()

            for reserva in reserves:
                tree.insert("", "end", values=reserva)

            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtenir les dades: {str(e)}")

    combo_hotels.bind('<<ComboboxSelected>>', mostrar_reserves_per_hotel)
    carregar_hotels()

    # Botó per tancar
    ttk.Button(
        finestra_reserves,
        text="Tancar",
        command=finestra_reserves.destroy
    ).pack(pady=10)


    
def obrir_consultes_informes():
    """Funció que crea la finestra principal de consultes i informes"""
    finestra_consultes = tk.Toplevel()
    finestra_consultes.title("Consultes i Informes")
    finestra_consultes.geometry("400x400")
    finestra_consultes.configure(bg="slategray3")

    # Títol
    ttk.Label(
        finestra_consultes,
        text="Consultes i Informes",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    # Frame pels botons
    frame_botons = ttk.Frame(finestra_consultes)
    frame_botons.pack(pady=20)

    # Botó 1: Resum Hotel
    ttk.Button(
        frame_botons,
        text="Resum Hotel",
        command=obrir_resum_hotel,
        width=30
    ).pack(pady=10)

    # Botó 2: Informe Personal
    ttk.Button(
        frame_botons,
        text="Informe Personal",
        command=obrir_informe_personal,
        width=30
    ).pack(pady=10)

    # Botó 3: Informe Reserves
    ttk.Button(
        frame_botons,
        text="Informe Check-ins/Check-outs",
        command=obrir_informe_moviments,
        width=30
    ).pack(pady=10)

    # Botó per tancar
    ttk.Button(
        frame_botons,
        text="Tancar",
        command=finestra_consultes.destroy,
        width=15
    ).pack(pady=20)

def consultar_serveis_hotels():
    """Mostra els serveis disponibles per cada hotel amb selecció automàtica"""
    finestra_serveis = tk.Toplevel()
    finestra_serveis.title("Serveis dels Hotels")
    finestra_serveis.geometry("800x500")
    finestra_serveis.configure(bg="slategray3")

    # Frame principal
    frame_principal = tk.Frame(finestra_serveis, bg="slategray3")
    frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Frame per la selecció d'hotel
    frame_seleccio = tk.Frame(frame_principal, bg="slategray3")
    frame_seleccio.pack(fill=tk.X, pady=(0, 10))

    tk.Label(
        frame_seleccio,
        text="Seleccionar Hotel:",
        font=("Arial", 10),
        bg="slategray3"
    ).pack(side=tk.LEFT, padx=5)

    combo_hotels = ttk.Combobox(
        frame_seleccio,
        state="readonly",
        width=50
    )
    combo_hotels.pack(side=tk.LEFT, padx=5)

    hotels_dict = {}

    # Frame per resultats
    frame_resultats = tk.Frame(frame_principal, bg="slategray3")
    frame_resultats.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(
        frame_resultats,
        columns=("Hotel", "Servei", "Categoria", "Descripció", "Preu"),
        show="headings"
    )
    tree.heading("Hotel", text="Hotel")
    tree.heading("Servei", text="Servei")
    tree.heading("Categoria", text="Categoria")
    tree.heading("Descripció", text="Descripció")
    tree.heading("Preu", text="Preu (€)")

    tree.column("Hotel", width=150)
    tree.column("Servei", width=150)
    tree.column("Categoria", width=100)
    tree.column("Descripció", width=250)
    tree.column("Preu", width=100)

    scrollbar = ttk.Scrollbar(frame_resultats, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    # Funció per carregar serveis segons hotel seleccionat
    def carregar_serveis(event=None):
        hotel_nom = combo_hotels.get()
        id_hotel = hotels_dict.get(hotel_nom)

        if not id_hotel:
            return

        for item in tree.get_children():
            tree.delete(item)

        try:
            conn = conexio_bd()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT h.nom, ts.nom, ts.categoria, ts.descripcio, s.preu
                FROM HOTEL h
                JOIN SERVEI s ON h.id_hotel = s.id_hotel
                JOIN TIPUS_SERVEI ts ON s.id_tipu_servei = ts.id_tipu_servei
                WHERE h.id_hotel = %s
                ORDER BY ts.categoria
            """, (id_hotel,))
            serveis = cursor.fetchall()
            for servei in serveis:
                tree.insert("", "end", values=servei)
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error en consultar els serveis: {str(e)}")

    combo_hotels.bind("<<ComboboxSelected>>", carregar_serveis)

    # Carregar noms dels hotels al combobox i diccionari
    try:
        conn = conexio_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT id_hotel, nom FROM hotel ORDER BY nom")
        hotels = cursor.fetchall()
        hotels_dict.update({nom: id_hotel for id_hotel, nom in hotels})
        combo_hotels['values'] = list(hotels_dict.keys())
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", "Error al carregar els hotels")

    # Botó per tancar
    tk.Button(
        finestra_serveis,
        text="Tancar",
        command=finestra_serveis.destroy,
        font=("Arial", 12),
        width=10,
        bg="white"
    ).pack(pady=10)


def obrir_informe_moviments():
    """Funció que mostra els check-ins i check-outs d'un hotel"""
    finestra_moviments = tk.Toplevel()
    finestra_moviments.title("Informe de Check-ins i Check-outs")
    finestra_moviments.geometry("1400x600")
    finestra_moviments.configure(bg="slategray3")

    # Frame principal
    frame_principal = tk.Frame(finestra_moviments, bg="slategray3")
    frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Frame per la selecció
    frame_seleccio = tk.Frame(frame_principal, bg="slategray3")
    frame_seleccio.pack(fill=tk.X, pady=(0, 10))

    # Selecció d'hotel
    tk.Label(frame_seleccio, text="Hotel:", font=("Arial", 10), bg="slategray3").pack(side=tk.LEFT, padx=5)
    combo_hotels = ttk.Combobox(frame_seleccio, state="readonly", width=30)
    combo_hotels.pack(side=tk.LEFT, padx=5)


    # Selecció de data
    tk.Label(frame_seleccio, text="Data:", font=("Arial", 10), bg="slategray3").pack(side=tk.LEFT, padx=5)

    # Crear desplegables per dia, mes i any
    frame_data = tk.Frame(frame_seleccio, bg="slategray3")
    frame_data.pack(side=tk.LEFT, padx=5)

    combo_dia = ttk.Combobox(frame_data, state="readonly", width=3)
    combo_dia['values'] = [str(i).zfill(2) for i in range(1, 32)]
    combo_dia.pack(side=tk.LEFT, padx=2)

    combo_mes = ttk.Combobox(frame_data, state="readonly", width=3)
    combo_mes['values'] = [str(i).zfill(2) for i in range(1, 13)]
    combo_mes.pack(side=tk.LEFT, padx=2)

    from datetime import datetime
    combo_any = ttk.Combobox(frame_data, state="readonly", width=5)
    any_actual = datetime.now().year
    combo_any['values'] = [str(i) for i in range(2000, any_actual + 5)]
    combo_any.pack(side=tk.LEFT, padx=2)

    # Crear Treeview
    columns = ("Tipus", "Hora", "Habitació", "Client", "DNI")
    tree = ttk.Treeview(frame_principal, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack(fill=tk.BOTH, expand=True, pady=10)

    # Carregar hotels
    try:
        conn = conexio_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT nom FROM hotel ORDER BY nom")
        hotels = [row[0] for row in cursor.fetchall()]
        combo_hotels['values'] = hotels
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al carregar els hotels: {str(e)}")

    combo_hotels.pack(side=tk.LEFT, padx=5)

    def actualitzar_dades():
        hotel_seleccionat = combo_hotels.get()
        dia = combo_dia.get()
        mes = combo_mes.get()
        any = combo_any.get()

        if not hotel_seleccionat or not dia or not mes or not any:
            messagebox.showwarning("Avís", "Si us plau, selecciona un hotel i una data completa")
            return

        data_seleccionada = f"{any}-{mes}-{dia}"

        for item in tree.get_children():
            tree.delete(item)

        try:
            conn = conexio_bd()
            cursor = conn.cursor()

            cursor.execute("SELECT id_hotel FROM hotel WHERE nom = %s", (hotel_seleccionat,))
            id_hotel = cursor.fetchone()[0]

            cursor.execute("""
                SELECT 
                    'Check-in' as tipus,
                    TO_CHAR(ci.data_hora, 'HH24:MI') as hora,
                    CONCAT('Hab. ', hab.numero) as habitacio,
                    CONCAT(c.nom, ' ', c.cognoms) as client,
                    c.dni
                FROM check_in ci
                JOIN client c ON ci.dni = c.dni
                JOIN reserva r ON ci.id_reserva = r.id_reserva
                JOIN detall_reserva dr ON r.id_reserva = dr.id_reserva
                JOIN habitacio hab ON dr.id_habitacio = hab.id_habitacio
                WHERE r.id_hotel = %s 
                AND DATE(ci.data_hora) = %s
            """, (id_hotel, data_seleccionada))

            for row in cursor.fetchall():
                tree.insert("", "end", values=row, tags=('checkin',))

            cursor.execute("""
                SELECT 
                    CONCAT('Hab. ', hab.numero),
                    CONCAT(c.nom, ' ', c.cognoms),
                    c.dni,
                    TO_CHAR(co.data_hora, 'HH24:MI') as hora
                FROM check_out co
                JOIN client c ON co.dni = c.dni
                JOIN reserva r ON co.id_reserva = r.id_reserva
                JOIN detall_reserva dr ON r.id_reserva = dr.id_reserva
                JOIN habitacio hab ON dr.id_habitacio = hab.id_habitacio
                WHERE r.id_hotel = %s 
                AND DATE(co.data_hora) = %s
                ORDER BY co.data_hora
            """, (id_hotel, data_seleccionada))

            for row in cursor.fetchall():
                tree.insert("", "end", values=row, tags=('checkout',))

            tree.tag_configure('checkin', background='#E8F5E9')
            tree.tag_configure('checkout', background='#FFEBEE')

            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtenir les dades: {str(e)}")

    # Botó per actualitzar
    tk.Button(
        frame_seleccio,
        text="Consultar",
        command=actualitzar_dades,
        bg="white"
    ).pack(side=tk.LEFT, padx=20)

    # Botó per tancar
    tk.Button(
        finestra_moviments,
        text="Tancar",
        command=finestra_moviments.destroy,
        bg="white"
    ).pack(pady=10)
