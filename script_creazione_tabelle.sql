CREATE TABLE Paziente (
    id_paziente SERIAL PRIMARY KEY , 
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    data_nascita DATE NOT NULL,
    sesso CHAR(1) CHECK (sesso IN ('M', 'F')), 
    codice_fiscale VARCHAR(16) UNIQUE NOT NULL,
    indirizzo VARCHAR(100),
    citta VARCHAR(50),
    cap VARCHAR(10),
    telefono VARCHAR(20),
    email VARCHAR(100) UNIQUE,
	username VARCHAR(100) UNIQUE,
	pw VARCHAR(200)
);

CREATE TABLE Diabetologo (
    id_diabetologo SERIAL PRIMARY KEY ,
	paziente_associato INT,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    data_nascita DATE NOT NULL,
    sesso CHAR(1) CHECK (sesso IN ('M', 'F')),  
    codice_fiscale VARCHAR(16) UNIQUE NOT NULL,
    indirizzo VARCHAR(100),
    citta VARCHAR(50),
    cap VARCHAR(10),
    telefono VARCHAR(20),
    email VARCHAR(100) UNIQUE,
	username VARCHAR(100) UNIQUE,
	pw VARCHAR(200)
);

CREATE TABLE Terapia (
    id_terapia SERIAL PRIMARY KEY ,
	paziente INT,
	diabetologo INT,
    farmaco VARCHAR(50) NOT NULL,
	dosaggio FLOAT,
	assunzioni_gg INT NOT NULL,
    data_inizio DATE NOT NULL,
	data_fine DATE NOT NULL  
);

CREATE TABLE Glicemia (
    id_glicemia SERIAL PRIMARY KEY ,
	paziente INT NOT NULL,
    farmaco VARCHAR(50),
	dosaggio FLOAT,
	sintomo VARCHAR(50),
    data_inserimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

alter table Glicemia ADD column valore INT;

CREATE TABLE InfoPaziente (
    id_info SERIAL PRIMARY KEY ,
	paziente INT NOT NULL,
	diabetologo INT NOT NULL,
    patologie_pregresse VARCHAR(50) ,
	fattori_rischio VARCHAR(50) ,
    comorbidita VARCHAR(50) ,
	
	terapia_conc INT,
    data_inizio DATE,
	data_fine DATE 
    
);

CREATE TABLE Operazione (
    id_operazione SERIAL PRIMARY KEY ,
	paziente INT,
	diabetologo INT,
    data_inserimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE RichiesteAccount (
    id_richiesta SERIAL PRIMARY KEY ,
	nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    data_nascita DATE NOT NULL,
    sesso CHAR(1) CHECK (sesso IN ('M', 'F')), 
    codice_fiscale VARCHAR(16) UNIQUE NOT NULL,
    indirizzo VARCHAR(100),
    citta VARCHAR(50),
    cap VARCHAR(10),
    telefono VARCHAR(20),
	email VARCHAR(100) UNIQUE,
	paziente BOOLEAN NOT NULL,
    data_richiesta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	stato VARCHAR(20) default 'noletta',
	password VARCHAR(200) NOT NULL
	
);

ALTER TABLE Paziente ADD COLUMN diabetologo_associato INT REFERENCES Diabetologo(id_diabetologo);
ALTER TABLE Diabetologo DROP COLUMN paziente_associato;




