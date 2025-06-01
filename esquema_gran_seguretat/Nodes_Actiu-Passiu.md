# Configuració de Nodes PostgreSQL (Actiu - Passiu)

Aquest document explica com configurar un sistema de rèplica Actiu-Passiu entre dos servidors PostgreSQL.

---

## Server Actiu (192.168.56.106)

### 1. Editar `/etc/postgresql/15/main/postgresql.conf`

Modifica o afegeix aquestes línies:

```conf
listen_addresses = '*'
wal_level = replica
max_wal_senders = 3
wal_keep_size = 64MB
```

---

### 2. Editar `/etc/postgresql/15/main/pg_hba.conf`

Afegir la següent línia per permetre la connexió del node secundari:

```
host    replication     replicador      192.168.56.107/24       md5
```

---

### 3. Crear l’usuari replicador

Des de `psql`, executa:

```sql
CREATE ROLE replicador WITH REPLICATION LOGIN ENCRYPTED PASSWORD 'contrasenya';
```

---

### 4. Reiniciar PostgreSQL per aplicar els canvis

```bash
sudo systemctl restart postgresql
```

---

## Server Passiu (192.168.56.107)

### 1. Aturar PostgreSQL

```bash
sudo systemctl stop postgresql
```

---

### 2. Buidar el directori de dades (per iniciar la rèplica des de zero)

```bash
sudo rm -rf /var/lib/postgresql/15/main/*
```

---

### 3. Copiar dades des del servidor actiu

Exemple amb `pg_basebackup`:

```bash
pg_basebackup -h 192.168.56.106 -D /var/lib/postgresql/15/main -U replicador -Fp -Xs -P
```

> **Nota:** Pot ser necessari configurar el fitxer `.pgpass` per evitar que es demani la contrasenya.

---

### 4. Reiniciar PostgreSQL

```bash
sudo systemctl start postgresql
```

---

## Comprovació de la replicació

### 1. Crear una taula en el node principal

Des del node actiu:

```sql
CREATE TABLE prova (id serial PRIMARY KEY, nom text);
```

### 2. Comprovar la rèplica al node passiu

Des del node passiu:

```sql
\dt
SELECT * FROM prova;
```

---

### 3. Promoure el node passiu en cas de fallada del principal

Per convertir el node passiu en nou node actiu:

```bash
sudo -u postgres /usr/lib/postgresql/15/bin/pg_ctl promote -D /var/lib/postgresql/15/main/
```

---

## Resum de passos

- Configura el servidor actiu per permetre rèplica.
- Dona accés al node passiu.
- Crea l’usuari de rèplica.
- Copia el directori de dades al passiu.
- Comprova la sincronització.
- Promou el node passiu si cal.

Aquesta configuració assegura alta disponibilitat i tolerància a errors a PostgreSQL mitjançant rèplica Actiu-Passiu.
