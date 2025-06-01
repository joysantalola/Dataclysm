-- HOTEL
CREATE TABLE HOTEL (
    id_hotel SERIAL PRIMARY KEY,
    id_director INT NOT NULL,
    id_gerent INT NOT NULL,
    nom VARCHAR(100) NOT NULL,
    adreca VARCHAR(200) NOT NULL,
    poblacio VARCHAR(100) NOT NULL,
    web VARCHAR(100),
    num_estrelles INT NOT NULL,
    telefon VARCHAR(20)
);

-- TREBALLADOR
CREATE TABLE TREBALLADOR (
    id_treballador SERIAL PRIMARY KEY,
    id_hotel INT NOT NULL,
    DNI VARCHAR(20) UNIQUE NOT NULL,
    nom VARCHAR(100) NOT NULL,
    cognoms VARCHAR(100) NOT NULL,
    data_naixement DATE NOT NULL,
    telefon VARCHAR(20),
    tipus_empleat VARCHAR(50) NOT NULL,
	FOREIGN KEY (id_hotel) REFERENCES HOTEL(id_hotel)
);

-- PERSONAL RECEPCIÓ
CREATE TABLE PERSONAL_RECEPCIO (
    id_treballador INT PRIMARY KEY,
    anys_experiencia INT NOT NULL,
    FOREIGN KEY (id_treballador) REFERENCES TREBALLADOR(id_treballador)
);

-- IDIOMA
CREATE TABLE IDIOMA (
    id_treballador INT NOT NULL,
    id_idioma INT NOT NULL,
    nivell_parla VARCHAR(10) NOT NULL CHECK (nivell_parla IN ('Basic', 'Mitja', 'Avancat')),
    nivell_enten VARCHAR(10) NOT NULL CHECK (nivell_enten IN ('Basic', 'Mitja', 'Avancat')),
    nivell_escriu VARCHAR(10) NOT NULL CHECK (nivell_escriu IN ('Basic', 'Mitja', 'Avancat')),
    PRIMARY KEY (id_treballador, id_idioma),
    FOREIGN KEY (id_treballador) REFERENCES PERSONAL_RECEPCIO(id_treballador)
);

-- PEROSNAL CUINA
CREATE TABLE PERSONAL_CUINA (
    id_treballador INT PRIMARY KEY,
    id_supervisor INT,
    categoria VARCHAR(50) NOT NULL,
    ultim_treball VARCHAR(100),
    FOREIGN KEY (id_treballador) REFERENCES TREBALLADOR(id_treballador),
    FOREIGN KEY (id_supervisor) REFERENCES PERSONAL_CUINA(id_treballador)
);

-- HABITACIÓ
CREATE TABLE HABITACIO (
	id_habitacio SERIAL PRIMARY KEY,
    id_hotel INT NOT NULL,
    numero INT NOT NULL,
    tv VARCHAR(2) NOT NULL CHECK (tv IN ('Si', 'No')),
    nevera VARCHAR(2) NOT NULL CHECK (nevera IN ('Si', 'No')),
    num_llits INT NOT NULL,
    m_quadrats NUMERIC(5,2) NOT NULL,
    estat VARCHAR(20) NOT NULL DEFAULT 'Disponible' CHECK (estat IN ('Disponible', 'Ocupada', 'Manteniment')),
    preu_temp_alta NUMERIC(10,2) NOT NULL,
    preu_temp_baixa NUMERIC(10,2) NOT NULL,
    tipus_habitacio VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_hotel) REFERENCES HOTEL(id_hotel)
);

-- CLIENT
CREATE TABLE CLIENT (
    DNI VARCHAR(20) PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    cognoms VARCHAR(100) NOT NULL,
    data_naixement DATE NOT NULL,
    telefon VARCHAR(20),
    nacionalitat VARCHAR(50) NOT NULL
);

-- RESERVA
CREATE TABLE RESERVA (
    id_reserva SERIAL PRIMARY KEY,
    DNI VARCHAR(20) NOT NULL,
    id_hotel INT NOT NULL,
    data_inici DATE NOT NULL,
    data_fi DATE NOT NULL,
    FOREIGN KEY (DNI) REFERENCES CLIENT(DNI),
    FOREIGN KEY (id_hotel) REFERENCES HOTEL(id_hotel)
);

-- DETALL RESERVA
CREATE TABLE DETALL_RESERVA (
    id_reserva INT NOT NULL,
    id_habitacio INT NOT NULL,
    PRIMARY KEY (id_reserva, id_habitacio),
    FOREIGN KEY (id_reserva) REFERENCES RESERVA(id_reserva),
    FOREIGN KEY (id_habitacio) REFERENCES HABITACIO(id_habitacio)
);

-- TIPUS SERVEI
CREATE TABLE TIPUS_SERVEI (
    id_tipu_servei SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    descripcio TEXT,
    categoria VARCHAR(50) NOT NULL
);

-- SERVEI
CREATE TABLE SERVEI (
    id_hotel INT NOT NULL,
    id_tipu_servei INT NOT NULL,
    nom VARCHAR(100) NOT NULL,
    preu NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (id_hotel, id_tipu_servei),
    FOREIGN KEY (id_hotel) REFERENCES HOTEL(id_hotel),
    FOREIGN KEY (id_tipu_servei) REFERENCES TIPUS_SERVEI(id_tipu_servei)
);

-- SOL·LICITUD SERVEI
CREATE TABLE SOLICITUD_SERVEI (
    id_solicitud SERIAL PRIMARY KEY,
    id_hotel INT NOT NULL,
    id_tipu_servei INT NOT NULL,
    DNI VARCHAR(20) NOT NULL,
    id_reserva INT NOT NULL,
    data DATE NOT NULL,
    hora TIME NOT NULL,
    pagat VARCHAR(2) NOT NULL CHECK (pagat IN ('Si', 'No')),
    FOREIGN KEY (id_hotel) REFERENCES HOTEL(id_hotel),
    FOREIGN KEY (id_tipu_servei) REFERENCES TIPUS_SERVEI(id_tipu_servei),
    FOREIGN KEY (DNI) REFERENCES CLIENT(DNI),
    FOREIGN KEY (id_reserva) REFERENCES RESERVA(id_reserva)
);

-- CHECK-IN
CREATE TABLE CHECK_IN (
    id_check_in SERIAL PRIMARY KEY,
    DNI VARCHAR(20) NOT NULL,
    id_reserva INT NOT NULL,
    data_hora TIMESTAMP NOT NULL,
    FOREIGN KEY (DNI) REFERENCES CLIENT(DNI),
    FOREIGN KEY (id_reserva) REFERENCES RESERVA(id_reserva)
);

-- CHECK-OUT
CREATE TABLE CHECK_OUT (
    id_check_out SERIAL PRIMARY KEY,
    DNI VARCHAR(20) NOT NULL,
    id_reserva INT NOT NULL,
    id_treballador INT NOT NULL,
    data DATE NOT NULL,
    hora TIME NOT NULL,
    observacions TEXT,
    FOREIGN KEY (DNI) REFERENCES CLIENT(DNI),
    FOREIGN KEY (id_reserva) REFERENCES RESERVA(id_reserva),
    FOREIGN KEY (id_treballador) REFERENCES TREBALLADOR(id_treballador)
);

-- FACTURA
CREATE TABLE FACTURA (
    id_factura SERIAL PRIMARY KEY,
    id_check_out INT NOT NULL,
    DNI VARCHAR(20) NOT NULL,
    data DATE NOT NULL,
    FOREIGN KEY (id_check_out) REFERENCES CHECK_OUT(id_check_out),
    FOREIGN KEY (DNI) REFERENCES CLIENT(DNI)
);

-- DETALL FACTURA
CREATE TABLE DETALL_FACTURA (
    id_factura INT NOT NULL,
    id_linia SERIAL NOT NULL,
    id_reserva INT,
    id_solicitud INT,
    descripcio TEXT NOT NULL,
    subtotal NUMERIC(10,2) NOT NULL,
    total NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (id_factura, id_linia),
    FOREIGN KEY (id_factura) REFERENCES FACTURA(id_factura),
    FOREIGN KEY (id_reserva) REFERENCES RESERVA(id_reserva),
    FOREIGN KEY (id_solicitud) REFERENCES SOLICITUD_SERVEI(id_solicitud)
);

-- PAGAMENT
CREATE TABLE PAGAMENT (
    id_pagament SERIAL PRIMARY KEY,
    id_factura INT NOT NULL,
    data DATE NOT NULL,
    import NUMERIC(10,2) NOT NULL,
    FOREIGN KEY (id_factura) REFERENCES FACTURA(id_factura)
);

-- METODE
CREATE TABLE metode ( 
    id_metode SERIAL PRIMARY KEY,
	id_pagament INTEGER,
    efectiu BOOLEAN DEFAULT FALSE,
    transferencia BOOLEAN DEFAULT FALSE,
    tarjeta_credit BOOLEAN DEFAULT FALSE,
    cvv VARCHAR(3),
    numero VARCHAR(16),
    data_caducitat DATE,
    nom VARCHAR(100),
	FOREIGN KEY (id_pagament) REFERENCES PAGAMENT(id_pagament)
);

-- ALTER PER AFEGIR LES FOREIGN KEY A HOTEL
ALTER TABLE HOTEL
ADD CONSTRAINT id_director FOREIGN KEY (id_director) REFERENCES TREBALLADOR(id_treballador);

ALTER TABLE HOTEL
ADD CONSTRAINT id_gerent FOREIGN KEY (id_gerent) REFERENCES TREBALLADOR(id_treballador);


ALTER TABLE TREBALLADOR
ADD COLUMN id_gerent INT;

ALTER TABLE TREBALLADOR
ADD COLUMN id_director INT;

ALTER TABLE HOTEL
ADD CONSTRAINT fk_gerent FOREIGN KEY (id_gerent) REFERENCES TREBALLADOR(id_treballador);

ALTER TABLE HOTEL
ADD CONSTRAINT fk_director FOREIGN KEY (id_director) REFERENCES TREBALLADOR(id_treballador);
