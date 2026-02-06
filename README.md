# Dataclysm

<img src="https://github.com/joysantalola/Dataclysm/blob/main/logo.jpeg" alt="Dataclysm Logo" width="200"/>

# Dataclysm

**Dataclysm** es un gestor de hoteles desarrollado como un proyecto intermodular, diseñado para facilitar la gestión de establecimientos hoteleros de manera eficiente y segura.

## Características principales

- **Backend con SQL (PostgreSQL):** Todos los datos se gestionan mediante una base de datos PostgreSQL, garantizando confiabilidad y escalabilidad.
- **Interfaz gráfica con Python (Tkinter):** La aplicación ofrece una interfaz de usuario intuitiva y sencilla gracias a la librería Tkinter de Python.
- **Infraestructura segura:** La base de datos se aloja en una máquina virtual Debian, con sistema de copias de seguridad automatizado y una segunda máquina virtual en modo activo-pasivo para garantizar alta disponibilidad.
- **Gestión de hoteles:** El sistema permite gestionar hoteles, habitaciones, reservas, clientes, trabajadores y servicios asociados.
- **Copias de seguridad y restauración:** El sistema realiza copias de seguridad periódicas de la base de datos y permite restaurarlas fácilmente.

## Estructura del proyecto (resumen)

Árbol de archivos y carpetas principales:

```
Dataclysm
├── /Images
│   └── logo_data.png
├── /Modelo Entidad-Relación
│   └── creacion_tablas.sql
│   └── esquema.jpg
│   └── modelo_relacional.md
├── /esquema_alta_seguridad
│   └── SSL.md 
│   └── crear_roles.sql
│   └── datamasking.md
│   └── trigger_borrar_datos.sql
├── /esquema_gran_seguridad             
│   └── Backups.md
│   └── nodos_activo_pasivo.md
│   └── infraestructura_deseada.md
├── /programa_py
│   └── admin_menu.py
│   └── block_login.py
│   └── check_in.py
│   └── check_out.py
│   └── consultas_informes.py
│   └── credenciales.py
│   └── db_connection.py
│   └── exportacion.py
│   └── gestion_hoteles.py
│   └── gestion_personal.py
│   └── gestion_reservas.py
│   └── login.txt
│   └── main.py
│   └── main.spec
│   └── mossos_apu.py
```

## Arquitectura del sistema

```
+---------------------------+
| Interfaz de usuario (GUI) |
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
| PostgreSQL Database VM    |
|  (Debian Activo-Pasivo)   |
+---------------------------+
```

- **Usuario:** Interactúa con la interfaz gráfica desarrollada en Python.
- **Gestor:** Python actúa como puente entre la GUI y la base de datos SQL, gestionando las consultas y la lógica de la aplicación.
- **Base de datos:** PostgreSQL, alojado en una máquina virtual Debian, con copias de seguridad y un sistema de réplica Activo-Pasivo mediante una segunda máquina virtual.

## Funcionalidades principales

- **Gestión de clientes, reservas, habitaciones, trabajadores y servicios.**
- **Alta, baja y modificación de elementos del sistema (CRUD completo).**
- **Visualización del estado de las reservas y disponibilidad de habitaciones.**
- **Asignación de servicios extras a las reservas.**
- **Sistema de autenticación de usuarios y permisos diferenciados (por ejemplo, administrador y trabajadores).**
- **Exportación de informes o datos relevantes.**
- **Sistema de copias de seguridad y restauración, con réplica Activo-Pasivo.**

## Requisitos técnicos

- **Python 3.13.3**
- **Tkinter**
- **psycopg2** (conector Python para PostgreSQL)
- **PostgreSQL**
- **Debian (para las máquinas virtuales)**

## Instalación y puesta en marcha

1. **Despliegue de la base de datos:**
    - Crear dos máquinas virtuales Debian (Activa y Pasiva).
    - Instalar PostgreSQL y configurar el sistema de backups y la réplica Activo-Pasivo.

2. **Configuración de la aplicación:**
    - Clonar este repositorio.
    - Instalar las dependencias de Python:
      ```bash
      pip install -r requirements.txt
      ```
    - Configurar los parámetros de conexión a la base de datos en el archivo de configuración correspondiente.

3. **Ejecución:**
    - Lanzar la aplicación Python para comenzar a gestionar el hotel.

## Copias de seguridad y recuperación

El sistema realiza copias de seguridad periódicas de la base de datos y, en caso de fallo de la máquina Activa, la Pasiva puede tomar el relevo, minimizando el tiempo de inactividad y la pérdida de datos.

## Contribución

¡Cualquier contribución es bienvenida! Puedes enviar issues o pull requests con mejoras, correcciones o sugerencias.

## Licencia

Este proyecto se distribuye bajo la licencia MIT.

---

## Miembros del proyecto

- [Oleguer Esteo](https://olegueresteo.es)
- [David Gutierrez](https://davidgutierrez.es)
- **Sergi Gallart**
- **Eder Aira**

## Enlaces rápidos al repositorio

- [Modelo Entidad-Relación](https://github.com/joysantalola/Dataclysm/tree/main/Modelo%20Entidad-Relaci%C3%B3n)
- [Esquema Alta Seguridad](https://github.com/joysantalola/Dataclysm/tree/main/esquema_alta_seguridad)
- [Esquema Gran Seguridad](https://github.com/joysantalola/Dataclysm/tree/main/esquema_gran_seguridad)
- [Programa Python](https://github.com/joysantalola/Dataclysm/tree/main/programa_py)
- [README.md (este archivo)](https://github.com/joysantalola/Dataclysm/blob/main/README.md)