-- SQLite
INSERT INTO personen (nachname, vorname, stammnummer) VALUES ('kelber', 'yannick', 382208);
INSERT INTO personen (nachname, vorname, stammnummer) VALUES ('john', 'timo', 381234);
INSERT INTO personen (nachname, vorname, stammnummer) VALUES ('klimmer', 'daniel', 381111);
 SELECT * FROM PERSONEN

 INSERT INTO laptop (laptopnummer, beschreibung) VALUES (123456, 10);
 INSERT INTO laptop (laptopnummer, beschreibung) VALUES (654321, 11);
  SELECT * FROM laptop

INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (1,1);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (2,2);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (3,3);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (4,4);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (5,5);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (6,6);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (7,7);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (8,8);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (9,9);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (10,10);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (11,11);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (12,12);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (13,13);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (14,14);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (15,15);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (16,16);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (17,17);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (18,18);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (19,19);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (20,20);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (21,21);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (22,22);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (23,23);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (24,24);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (25,25);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (26,26);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (27,27);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (28,28);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (29,29);
INSERT INTO laptop_lagerplatz (lagerplatzId, laptopId) VALUES (30,30);

UPDATE laptop SET beschreibung = 'laptop 1' WHERE laptopnummer  = 0001;

   SELECT * FROM laptop;

   DELETE FROM laptop WHERE lagerplatz = 3


   SELECT p.nachname
   , o.postleitzahl
   , o.ortsname
   , o.bundesland
   FROM person p
   LEFT JOIN ortschaft o ON p.postleitzahl = o.postleitzahl AND p.staat = o.staat

SELECT * FROM ausleihen WHERE laptopId = 3 AND datum_zurueck IS NULL AND uhrzeit_zurueck IS NULL

UPDATE ausleihen SET datum_zurueck = NULL, uhrzeit_zurueck = NULL WHERE laptopId = 3 AND datum_zurueck IS NULL AND uhrzeit_zurueck IS NULL
UPDATE laptop_lagerplatz SET laptopId = 10 WHERE laptopId = 1

 COMMIT;

 ALTER TABLE lagerplatz ADD UNIQUE (lagerplatz)

 DROP TABLE laptop