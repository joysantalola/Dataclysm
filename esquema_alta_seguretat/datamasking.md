# Data Masking a PostgreSQL amb l'extensió Anonymizer

Aquest document explica com protegir dades sensibles dins d'una base de dades PostgreSQL utilitzant l'extensió `anon` per aplicar data masking.

---

## 1. Actualització dels paquets del sistema

És important tenir el sistema operatiu actualitzat abans d'instal·lar noves eines:

```bash
sudo apt update
sudo apt upgrade
```

---

## 2. Instal·lació de PGXN Client i llibreries de PostgreSQL

Instal·la l'eina `pgxnclient` i les llibreries de desenvolupament necessàries per compilar extensions de PostgreSQL:

```bash
sudo apt install pgxnclient postgresql-server-dev-15
```

---

## 3. Instal·lació de l’extensió Anonymizer

Un cop instal·lades les eines, pots instal·lar l’extensió `anon` per fer data masking dins de la base de dades.

Dins de `psql`, crea l’extensió:

```sql
CREATE EXTENSION anon CASCADE;
```

Aquesta comanda instal·la l’extensió i totes les seves dependències.

---

## 4. Aplicació de data masking

Per protegir dades sensibles, pots aplicar una sentència SQL que amaga part d’una columna. Per exemple, per mostrar només els 4 últims dígits dels números de targeta de la columna `metode.numero`:

```sql
SECURITY LABEL FOR anon ON COLUMN metode.numero IS 'MASKED WITH FUNCTION anon.partial(null, null, null, 4)';
```

Aquesta configuració fa que només siguin visibles els 4 últims dígits; la resta quedarà oculta.

---

## 5. Verificació

Després d’aplicar la sentència, quan es consultin les dades de la columna, només seran visibles els 4 últims dígits. Això garanteix la privacitat dels usuaris i evita exposar completament la informació sensible.

---

## 6. Recurs utilitzat

S’ha utilitzat el vídeo següent com a referència per implementar el procés:

[Com aplicar Data Masking a PostgreSQL amb Anonymizer – YouTube](https://www.youtube.com/watch?v=niIIFL4s-L8&t=45s)

---

## Resum

Amb aquests passos es protegeixen dades sensibles a PostgreSQL utilitzant l’extensió `anon` per aplicar data masking. S’inclouen tant la instal·lació com la configuració i l’aplicació a una columna concreta.
