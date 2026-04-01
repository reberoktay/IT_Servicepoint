-- SQLite
CREATE TABLE personen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nachname TEXT,
    vorname TEXT,
    stammnummer INT UNIQUE NOT NULL);

CREATE TABLE laptop (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     laptopnummer INT UNIQUE NOT NULL,
                     beschreibung TEXT
                 );

CREATE TABLE lagerplatz (
id INTEGER PRIMARY KEY AUTOINCREMENT, 
lagerplatz INT UNIQUE  --kann nicht einer existierenden Tabelle hinzugefügt werden. Alle Tabellen droppen und neu erstellen!!
);


CREATE TABLE laptop_lagerplatz (
id INTEGER PRIMARY KEY AUTOINCREMENT, 
lagerplatzId INT UNIQUE,
laptopId INT UNIQUE,
FOREIGN KEY(laptopId) REFERENCES laptop(id),
FOREIGN KEY(lagerplatzId) REFERENCES lagerplatz(id)
);

CREATE TABLE ausleihen (
id INTEGER PRIMARY KEY AUTOINCREMENT,
                     personenId INT,
                     laptopId INT,
                     datum_ausleih TEXT,
                     uhrzeit_ausleih TEXT,
                     datum_zurueck TEXT,
                     uhrzeit_zurueck TEXT,
FOREIGN KEY(personenId) REFERENCES personen(id),
FOREIGN KEY(laptopId) REFERENCES laptop(id)
);

CREATE VIEW laptop_status
AS 
   SELECT lap.id as laptopId
   , lap.laptopnummer
   , lap.beschreibung
   , laplag.lagerplatzId
   , lag.lagerplatz
   FROM laptop lap
   LEFT JOIN laptop_lagerplatz laplag ON lap.id = laplag.laptopId
   LEFT JOIN lagerplatz lag ON laplag.lagerplatzId = lag.id
;

SELECT name, sql FROM sqlite_master WHERE type='table' OR type='view';

2