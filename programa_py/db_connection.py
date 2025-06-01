# Importació de les llibreries necessàries
import psycopg2
from tkinter import messagebox
from dotenv import load_dotenv
import os

def conexio_bd():
    """Funció que gestiona la connexió amb la base de dades"""
    # Carregar les variables d'entorn del fitxer de credencials
    load_dotenv('credencials.env')

    # Paràmetres de connexió a la base de dades
    parametres = {
        "host": "192.168.56.106",    # Adreça IP del servidor PostgreSQL
        "port": "5432",              # Port per defecte de PostgreSQL
        "user": "postgres",          # Nom d'usuari de la base de dades
        "password": "P@ssw0rd",      # Contrasenya de la base de dades
        "dbname": "espamus",         # Nom de la base de dades
        "sslmode": "disable"         # Desactivar SSL per a connexions locals
    }

    try:
        # Intent de connexió amb la base de dades
        conexion = psycopg2.connect(**parametres)
        
        # Verificar la connexió amb una consulta simple
        with conexion.cursor() as cursor:
            cursor.execute('SELECT 1')
            
        print("Connexió establerta correctament")
        return conexion
        
    except psycopg2.Error as e:
        # Gestió d'errors de connexió
        print(f"Error de connexió: {e}")
        messagebox.showerror("Error de connexió", f"Error al connectar a la base de dades: {e}")
        return None
