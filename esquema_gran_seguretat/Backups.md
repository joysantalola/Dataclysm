# Còpies de seguretat (Backups) a PostgreSQL

Aquest document descriu el procés per configurar còpies de seguretat automàtiques de la base de dades PostgreSQL.

---

## 1. Configuració del checkpoint

Dóna permís d’execució a l’script `pg_checkpoint.sh` perquè pugui ser executat:

```bash
chmod +x pg_checkpoint.sh
```

---

## 2. Configuració del backup

Dóna permís d’execució a l’script de còpia de seguretat `pg_backup`:

```bash
chmod +x pg_backup
```

---

## 3. Prova d’execució del backup

Executa l’script manualment per comprovar que funciona correctament:

```bash
./pg_backup
```

---

## 4. Programació automàtica amb crontab

Per fer una còpia de seguretat automàtica cada dia a les 3:00 AM, edita el crontab amb:

```bash
crontab -e
```

Afegeix la línia següent al final del fitxer (substitueix `/ruta/al/script/pg_backup` per la ruta correcta):

```bash
0 3 * * * /ruta/al/script/pg_backup
```

Aquesta programació assegura que el backup s’executa diàriament a les 3:00 del matí de manera automàtica.

---

## Resum

- Dona permisos d’execució als scripts de checkpoint i backup.
- Prova manualment la còpia de seguretat.
- Configura l’execució automàtica diària amb crontab.

Aquesta configuració ajudarà a garantir la seguretat i disponibilitat de les dades de la base de dades.
