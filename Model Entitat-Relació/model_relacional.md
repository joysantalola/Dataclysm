# Model Relacional

## HOTEL
**HOTEL**(id_hotel, id_director, id_gerent, nom, adreça, poblacio, web, num_estrelles, telefon)  
- **Claus Foranes:**  
  - `id_director` REFERÈNCIA a TREBALLADOR(id_treballador)
  - `id_gerent` REFERÈNCIA a TREBALLADOR(id_treballador)

---

## TREBALLADOR
**TREBALLADOR**(id_treballador, id_hotel, DNI, nom, cognoms, data_naixement, telefon, tipus_empleat, id_director, id_gerent)  
- **Claus Foranes:**  
  - `id_hotel` REFERÈNCIA a HOTEL(id_hotel)
  - `id_director` REFERÈNCIA a HOTEL(id_director)
  - `id_gerent` REFERÈNCIA a HOTEL(id_gerent)

---

## PERSONAL RECEPCIÓ
**PERSONAL_RECEPCIO**(id_treballador, anys_experiencia)  
- **Claus Foranes:**  
  - `id_treballador` REFERÈNCIA a TREBALLADOR(id_treballador)

---

## IDIOMA
**IDIOMA**(id_treballador, id_idioma, nivell_parla, nivell_enten, nivell_escriu)  
- **Claus Foranes:**  
  - `id_treballador` REFERÈNCIA a PERSONAL_RECEPCIO(id_treballador)

---

## PERSONAL CUINA
**PERSONAL_CUINA**(id_treballador, id_supervisor, categoria, ultim_treball)  
- **Claus Foranes:**  
  - `id_treballador` REFERÈNCIA a TREBALLADOR(id_treballador)
  - `id_supervisor` REFERÈNCIA a PERSONAL_CUINA(id_treballador)

---

## HABITACIO
**HABITACIO**(id_hotel, numero, id_habitacio, tv, nevera, num_llits, m_quadrats, estat, preu_temp_alta, preu_temp_baixa, tipus_habitacio)  
- **Claus Foranes:**  
  - `id_hotel` REFERÈNCIA a HOTEL(id_hotel)

---

## CLIENT
**CLIENT**(DNI, nom, cognoms, data_naixement, telefon, nacionalitat)

---

## RESERVA
**RESERVA**(id_reserva, DNI, id_hotel, data_inici, data_fi)  
- **Claus Foranes:**  
  - `DNI` REFERÈNCIA a CLIENT(DNI)
  - `id_hotel` REFERÈNCIA a HOTEL(id_hotel)

---

## DETALL_RESERVA
**DETALL_RESERVA**(id_reserva, id_hotel, num_habitacio)  
- **Claus Foranes:**  
  - `id_reserva` REFERÈNCIA a RESERVA(id_reserva)
  - `id_hotel` REFERÈNCIA a HABITACIO(id_hotel)
  - `num_habitacio` REFERÈNCIA a HABITACIO(numero)

---

## TIPUS SERVEI
**TIPUS_SERVEI**(id_tipu_servei, nom, descripcio, categoria)

---

## SERVEI
**SERVEI**(id_hotel, id_tipu_servei, nom, preu)  
- **Claus Foranes:**  
  - `id_hotel` REFERÈNCIA a HOTEL(id_hotel)
  - `id_tipu_servei` REFERÈNCIA a TIPUS_SERVEI(id_tipu_servei)

---

## SOL·LICITUD SERVEI
**SOLLICITUD_SERVEI**(id_solicitud, id_hotel, id_tipu_servei, DNI, id_reserva, data, hora, pagat)  
- **Claus Foranes:**  
  - `id_hotel` REFERÈNCIA a HOTEL(id_hotel)
  - `id_tipu_servei` REFERÈNCIA a TIPUS_SERVEI(id_tipu_servei)
  - `DNI` REFERÈNCIA a CLIENT(DNI)
  - `id_reserva` REFERÈNCIA a RESERVA(id_reserva)

---

## CHECK IN
**CHECK_IN**(id_check_in, DNI, id_reserva, data_hora)  
- **Claus Foranes:**  
  - `DNI` REFERÈNCIA a CLIENT(DNI)
  - `id_reserva` REFERÈNCIA a RESERVA(id_reserva)

---

## CHECK OUT
**CHECK_OUT**(id_check_out, DNI, id_reserva, id_treballador, data, hora, observacions)  
- **Claus Foranes:**  
  - `DNI` REFERÈNCIA a CLIENT(DNI)
  - `id_reserva` REFERÈNCIA a RESERVA(id_reserva)
  - `id_treballador` REFERÈNCIA a TREBALLADOR(id_treballador)

---

## FACTURA
**FACTURA**(id_factura, id_check_out, DNI, data)  
- **Claus Foranes:**  
  - `DNI` REFERÈNCIA a CLIENT(DNI)
  - `id_check_out` REFERÈNCIA a CHECK_OUT(id_check_out)

---

## DETALL FACTURA
**DETALL_FACTURA**(id_factura, id_linia, id_reserva, id_solicitud, descripcio, subtotal, total)  
- **Claus Foranes:**  
  - `id_factura` REFERÈNCIA a FACTURA(id_factura)
  - `id_reserva` REFERÈNCIA a RESERVA(id_reserva)
  - `id_solicitud` REFERÈNCIA a SOLLICITUD_SERVEI(id_solicitud)

---

## PAGAMENT
**PAGAMENT**(id_pagament, id_factura, data, import)  
- **Claus Foranes:**  
  - `id_factura` REFERÈNCIA a FACTURA(id_factura)

---

## METODE
**METODE**(id_pagament, id_metode, efectiu, transferencia, numero, cvv, data_caducitat, nom)  
- **Claus Foranes:**  
  - `id_pagament` REFERÈNCIA a PAGAMENT(id_pagament)

---

## CREDENCIALS_USUARI
**CREDENCIALS_USUARI**(id_usuari, usuari, contrasenya)  
- **Claus Foranes:**  
  - `usuari` REFERÈNCIA a CLIENT(DNI)
  - `id_usuari` REFERÈNCIA a TREBALLADOR(id_treballador)

---
