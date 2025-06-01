# Infraestructura Desitjada per al Sistema de Gestió d'Hotels

Aquest document descriu la infraestructura recomanada i la configuració real utilitzada per gestionar la nostra base de dades, amb una atenció especial al creixement previst de la taula de clients.

---

## Càlcul de creixement

S'espera que la taula **clients** sigui la que més creixi amb el temps, ja que cada nova reserva implica l’alta d’un client. Per aquest motiu, la infraestructura ha d’estar pensada per suportar increments constants de volum de dades i garantir un alt rendiment en l’accés i consulta.

---

## Infraestructura Recomanada

### Processador

- **Recomanat:** AMD EPYC, especialment orientat a entorns de servidor per la seva alta capacitat de processos paral·lels i escalabilitat.
- **Alternativa:** Processadors de gamma alta Intel Xeon.

### Discos Durs

- **SSD NVMe** per a la base de dades activa, amb l’objectiu de garantir una latència molt baixa i altes velocitats d’accés.
- **HDD** per a còpies de seguretat i arxiu de dades antigues, optimitzant el cost sense sacrificar la capacitat d’emmagatzematge.

### Memòria RAM

- **Recomanat:** 64GB o més, per permetre la càrrega de grans volums de dades en memòria i millorar la velocitat de consulta.
- **Escalable:** Afegir més RAM segons el creixement de la base de dades.

### Xarxa

- **Dues o més interfícies Ethernet**, per separar el trànsit de base de dades del trànsit administratiu i oferir redundància davant fallades de connexió.
- **Connexió de 10GbE** opcional per a entorns d’alta concurrència.

### Sistema Operatiu

- **Linux** (preferiblement Debian o Ubuntu Server), per la seva estabilitat, seguretat i gran comunitat de suport.

---

## Maquinari Actual

Tot i les recomanacions, la infraestructura disponible actualment és la següent:

| Component         | Descripció                      |
|-------------------|---------------------------------|
| Processador       | AMD Ryzen 7 7730U (8 nuclis, 16 fils, fins a 4.5GHz, gràfics Radeon) |
| Memòria RAM       | 16GB DDR4                       |
| Disc dur          | Micron 500GB SSD (NVMe)         |
| Xarxa             | 1x Ethernet (connexió principal a PostgreSQL) + 1x Ethernet secundària (navegació) |
| Sistema Operatiu  | Debian Linux                    |

### Observacions

- **Processador:** El Ryzen 7 7730U ofereix un bon rendiment per a entorns petits o mitjans, encara que no té la capacitat d’escala d’EPYC o Xeon.
- **RAM:** Els 16GB són adequats per a un entorn de desenvolupament o inicial, però es recomana ampliar a mesura que el nombre de clients creixi.
- **SSD:** El disc Micron NVMe garanteix velocitats d’accés òptimes per a la base de dades.
- **Xarxa:** Tot i tenir una única connexió principal, seria ideal afegir una segona interfície per a redundància i separació de trànsit.

---

## Consideracions de futur

- **Escalabilitat:** Si el nombre de clients i reserves creix substancialment, es recomana migrar a una infraestructura amb processadors de gamma servidor, més RAM i sistemes d’emmagatzematge en RAID.
- **Disponibilitat:** Implementar rèplica Actiu-Passiu i còpies de seguretat regulars per garantir la continuïtat del servei.
- **Monitorització:** Utilitzar eines com Prometheus o Zabbix per monitorar recursos i anticipar colls d’ampolla.

---

## Resum

L’objectiu és garantir un equilibri entre cost, rendiment i escalabilitat, començant per una infraestructura sòlida i evolucionant segons les necessitats reals del sistema i el creixement de la base de dades de clients.
