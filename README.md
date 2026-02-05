# Dataclysm
<img src="https://github.com/joysantalola/Dataclysm/blob/main/logo.jpeg" alt="Dataclysm Logo" width="200"/>

# Dataclysm

**Dataclysm** és un gestor d'hotels desenvolupat com a projecte intermodular, pensat per facilitar la gestió d'establiments hotelers de manera eficient i segura.

## Característiques principals

- **Backend amb SQL (PostgreSQL):** Totes les dades es gestionen mitjançant una base de dades PostgreSQL, garantint fiabilitat i escalabilitat.
- **Interfície gràfica amb Python (Tkinter):** L'aplicació ofereix una interfície d'usuari intuïtiva i senzilla gràcies a la llibreria Tkinter de Python.
- **Infraestructura segura:** La base de dades s'allotja en una màquina virtual Debian, amb sistema de còpies de seguretat automatitzat i una segona màquina virtual en mode actiu-passiu per garantir alta disponibilitat.
- **Gestió d'hotels:** El sistema permet gestionar hotels, habitacions, reserves, clients, treballadors i serveis associats.
- **Còpies de seguretat i restauració:** El sistema realitza còpies de seguretat periòdiques de la base de dades i permet restaurar-les fàcilment.

## Arquitectura del sistema

```
+---------------------------+
| Interfície d'usuari (GUI) |
|      Python + Tkinter     |
+-------------+-------------+
              |
              v
+---------------------------+
|   Backend / Gestor SQL    |
|      Python + psycopg2    |
+-------------+-------------+
              |
              v
+---------------------------+
|  PostgreSQL Database VM   |
|   (Debian Actiu-Passiu)   |
+---------------------------+
```

- **Usuari:** Interactua amb la interfície gràfica desenvolupada en Python.
- **Gestor:** Python fa de pont entre la GUI i la base de dades SQL, gestionant les consultes i la lògica d'aplicació.
- **Base de dades:** PostgreSQL, allotjat en una màquina virtual Debian, amb còpies de seguretat i un sistema de rèplica Actiu-Passiu mitjançant una segona màquina virtual.

## Funcionalitats principals

- **Gestió de clients, reserves, habitacions, treballadors i serveis.**
- **Alta, baixa i modificació d'elements del sistema (CRUD complet).**
- **Visualització de l'estat de les reserves i disponibilitat d'habitacions.**
- **Assignació de serveis extres a les reserves.**
- **Sistema d'autenticació d'usuaris i permisos diferenciats (per exemple, administrador i treballadors).**
- **Exportació d'informes o dades rellevants.**
- **Sistema de còpies de seguretat i restauració, amb rèplica Actiu-Passiu.**

## Requisits tècnics

- **Python 3.13.3**
- **Tkinter**
- **psycopg2** (connector Python per PostgreSQL)
- **PostgreSQL**
- **Debian (per a les màquines virtuals)**

## Instal·lació i posada en marxa

1. **Desplegament de la base de dades:**
    - Crear dues màquines virtuals Debian (Actiu i Passiu).
    - Instal·lar PostgreSQL i configurar el sistema de backups i la rèplica Actiu-Passiu.

2. **Configuració de l'aplicació:**
    - Clonar aquest repositori.
    - Instal·lar les dependències de Python:
      ```bash
      pip install -r requirements.txt
      ```
    - Configurar els paràmetres de connexió a la base de dades a l'arxiu de configuració corresponent.

3. **Execució:**
    - Llançar l'aplicació Python per començar a gestionar l'hotel.

## Còpies de seguretat i recuperació

El sistema realitza còpies de seguretat periòdiques de la base de dades i, en cas de fallada de la màquina Activa, la Passiva pot prendre el relleu, minimitzant el temps d'inactivitat i la pèrdua de dades.

## Contribució

Qualsevol contribució és benvinguda! Pots enviar issues o pull requests amb millores, correccions o suggeriments.

## Llicència

Aquest projecte es distribueix sota la llicència MIT.

---

## Membres del projecte

- **Oleguer Esteo** (jo)
- **Sergi Gallart**
- **Eder Aira**
- **David Gutierrez**

## Enllaços ràpids al repositori

- [Model Entitat-Relació](https://github.com/joysantalola/Dataclysm/tree/main/Model%20Entitat-Relaci%C3%B3)
- [Esquema Alta Seguretat](https://github.com/joysantalola/Dataclysm/tree/main/esquema_alta_seguretat)
- [Esquema Gran Seguretat](https://github.com/joysantalola/Dataclysm/tree/main/esquema_gran_seguretat)
- [Programa Python](https://github.com/joysantalola/Dataclysm/tree/main/programa_py)
- [README.md (aquest fitxer)](https://github.com/joysantalola/Dataclysm/blob/main/README.md)
