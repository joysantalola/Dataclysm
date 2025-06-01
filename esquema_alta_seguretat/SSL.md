
# Configuració del servidor per SSL

Aquest document explica com generar i configurar un certificat SSL per a PostgreSQL, així com la comprovació i renovació automàtica del certificat.

## Índex

1. [Generació del certificat SSL](#generacio-certificat)
2. [Configuració de PostgreSQL](#configuracio-postgresql)
3. [Comprovació](#comprovacio)
4. [Renovació del certificat](#renovacio)

---

## 1. Generació del certificat SSL <a name="generacio-certificat"></a>

Per configurar el servidor per SSL, segueix aquests passos:

### 1.1 Generar la sol·licitud de certificat

```bash
openssl req -new -text -out server.req
```

Aquesta ordre genera una nova sol·licitud de signatura de certificat (CSR) amb OpenSSL. Es demanarà omplir camps com país, ciutat, organització, etc.

### 1.2 Convertir la clau privada RSA

```bash
openssl rsa -in privkey.pem -out server.key
```

Aquesta comanda converteix una clau privada RSA de `privkey.pem` a `server.key`, eliminant la protecció per contrasenya.

### 1.3 Generar el certificat autofirmat

```bash
openssl req -x509 -in server.req -text -key server.key -out server.crt
```

Crea un certificat X.509 a partir de la sol·licitud i la clau privada.

### 1.4 Ajustar permisos dels fitxers

```bash
chmod og-rwx server.key server.crt
```

Elimina permisos per grup i altres usuaris, deixant només el propietari amb accés.

### 1.5 Copiar els arxius al directori de PostgreSQL

```bash
cp -r server.key server.crt /var/lib/postgresql/15/main/
```

### 1.6 Canviar la propietat dels fitxers

```bash
chown -R postgres:postgres /var/lib/postgresql/15/main/server.*
```

---

## 2. Configuració de PostgreSQL <a name="configuracio-postgresql"></a>

1. Edita el fitxer de configuració de PostgreSQL, habitualment a `/etc/postgresql/15/main/postgresql.conf`, amb el teu editor preferit (per exemple, `nano`):

   ```bash
   nano /etc/postgresql/15/main/postgresql.conf
   ```

2. Assegura’t que existeixen i estan actives les següents línies:

   ```
   ssl = on
   ssl_cert_file = '/var/lib/postgresql/15/main/server.crt'
   ssl_key_file = '/var/lib/postgresql/15/main/server.key'
   ```

3. Desa i tanca el fitxer.

4. Reinicia el servei de PostgreSQL:

   ```bash
   systemctl restart postgresql
   ```

---

## 3. Comprovació <a name="comprovacio"></a>

Per comprovar que SSL està actiu, connecta’t a PostgreSQL:

```bash
psql -h localhost -U postgres -W
```

Un cop connectat, pots comprovar l’estat de SSL:

```sql
SHOW ssl;
```

El resultat hauria de ser:

```
ssl
-----
on
```

---

## 4. Renovació del certificat <a name="renovacio"></a>

Per automatitzar la renovació del certificat, afegeix una tasca programada a `crontab`:

```bash
echo "0 3 * * 1 /usr/bin/openssl req -new -text -out /home/sergi/server.req && /usr/bin/openssl rsa -in /home/sergi/privkey.pem -out /home/sergi/server.key && /usr/bin/openssl req -x509 -in /home/sergi/server.req -text -key /home/sergi/server.key -out /home/sergi/server.crt && cp -r /home/sergi/server.key /home/sergi/server.crt /var/lib/postgresql/15/main/ && chown -R postgres:postgres /var/lib/postgresql/15/main/server.* && chmod og-rwx /var/lib/postgresql/15/main/server.* && systemctl restart postgresql" | sudo tee -a /etc/crontab
```

- Aquesta línia afegeix una entrada al fitxer `/etc/crontab` perquè s'executi cada dilluns a les 3:00h.
- Les ordres dins la crontab:
  - Generen una nova sol·licitud de certificat
  - Transformen la clau privada
  - Creen el certificat
  - Copien els fitxers a la carpeta de PostgreSQL
  - Canvien la propietat i ajusten permisos
  - Reinicien PostgreSQL perquè reconegui els nous certificats

---

## Resum

Amb aquests passos tindràs el teu servidor PostgreSQL configurat amb SSL, podràs comprovar la connexió segura i garantir la renovació periòdica i automàtica del certificat.
