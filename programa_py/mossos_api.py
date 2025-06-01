# Importació de les llibreries necessàries per l'enviament de dades als Mossos
import json  # Per manipular dades en format JSON
import requests  # Per fer peticions HTTP a l'API
from datetime import datetime  # Per gestionar dates i temps
from db_connection import conexio_bd  # Per connectar amb la base de dades
from tkinter import messagebox  # Per mostrar missatges a l'usuari

def enviar_dades_mossos(ruta_arxiu):
    """
    Funció per enviar les dades dels check-ins als Mossos d'Esquadra.
    
    Aquesta funció:
    1. Llegeix un fitxer JSON amb les dades dels check-ins
    2. Envia aquestes dades a l'API dels Mossos
    3. Registra el resultat de l'enviament a la base de dades    
    """
    # Configuració de l'API dels Mossos
    API_URL = "http://apihotels.codeworks.es:7777/subir-json"
    USER = "usuario1"
    PASSWORD = "contrasenya1"

    try:
        # Primer llegim el fitxer per verificar que el JSON és vàlid
        with open(ruta_arxiu, 'r', encoding='utf-8') as f:
            dades = json.load(f)
            print(f"Contingut del JSON a enviar: {json.dumps(dades, indent=2)}")

        # Obrim el fitxer en mode binari per l'enviament
        with open(ruta_arxiu, 'rb') as f:
            # Configurem el fitxer per enviar-lo com a multipart/form-data
            files = {
                'file': (ruta_arxiu.split('/')[-1], f, 'application/json')
            }
            
            # Configurem les credencials d'autenticació
            auth = (USER, PASSWORD)

            print("Enviant fitxer a l'API...")
            # Fem la petició POST a l'API dels Mossos
            response = requests.post(
                API_URL,
                auth=auth,
                files=files,
                verify=False,  # Desactivem la verificació SSL per desenvolupament
                timeout=30  # Timeout de 30 segons per la petició
            )
        
        # Registrem la informació de l'enviament
        print(f"URL utilitzada: {API_URL}")
        print(f"Resposta API: {response.status_code} - {response.text}")

        # Guardem el resultat a la base de dades per tenir un registre
        conn = conexio_bd()
        if conn:
            with conn.cursor() as cur:
                # Inserim el registre de l'enviament
                cur.execute("""
                    INSERT INTO enviament_mossos 
                    (data_enviament, estat, fitxer_json, resposta_api)
                    VALUES (%s, %s, %s, %s)
                """, (
                    datetime.now(),  # Data i hora actual
                    'OK' if response.status_code == 200 else 'ERROR',  # Estat segons la resposta
                    json.dumps(dades),  # Contingut del JSON enviat
                    response.text  # Resposta rebuda de l'API
                ))
                conn.commit()
            conn.close()

        # Retornem el resultat de l'operació
        if response.status_code == 200:
            return True, "Enviament realitzat amb èxit"
        else:
            return False, f"Error en l'enviament: {response.text}"
            
    except Exception as e:
        # Capturem i registrem qualsevol error que pugui ocórrer
        print(f"Error detallat: {str(e)}")
        messagebox.showerror("Error", f"Error en enviar les dades: {str(e)}")
        return False, str(e)
