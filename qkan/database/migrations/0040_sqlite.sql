-- Neue Tabelle refdata
CREATE TABLE IF NOT EXISTS refdata (
    pk INTEGER PRIMARY KEY,
    bezext TEXT,                        /* externe Bezeichnung, z. B. gem. DWA-M 150 */
    bezqkan TEXT,                       /* Standardbezeichnung in QKan */
    kuerzel TEXT,                       /* Kürzel in QKan */
    subject TEXT,                       /* Bezeichnung der QKan-Tabelle oder interner Mapping-Tabelle */
    modul TEXT,                         /* QKan-Modul (= Modulverzeichnis) */
    kommentar TEXT,
    createdat TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Neue Tabelle Anschlussschächte
CREATE TABLE IF NOT EXISTS anschlussschaechte (
    pk INTEGER PRIMARY KEY,
    schnam TEXT,
    sohlhoehe REAL,
    deckelhoehe REAL,
    durchm REAL,                                    /* Schachtdurchmesser (m) */
    druckdicht INTEGER, 
    entwart TEXT DEFAULT 'Regenwasser',             /* join entwaesserungsarten.bezeichnung */
    strasse TEXT,
    baujahr INTEGER,
    haltnam TEXT,                                   /* Anschluss an Haltung */
    urstation REAL,                                 /* Anschlussposition gegen Fließrichtung */
    ursprung TEXT,                                  /* Adresse oder Objektbezeichnung */
    anschlusstyp TEXT,
    eigentum TEXT,                                  /* join eigentum.name */
    teilgebiet TEXT,                                /* join teilgebiet.tgnam */
    simstatus TEXT DEFAULT 'vorhanden',             /* join simulationsstatus.bezeichnung */
    material TEXT,                                  /* join material.bezeichnung */
    xsch REAL, 
    ysch REAL,
    kommentar TEXT,
    createdat TEXT DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS videos (
    pk INTEGER PRIMARY KEY,
    name TEXT,
    untersuchtag TEXT,
    untersuchrichtung TEXT,
    objekt TEXT,
    datei TEXT,
    createdat TEXT DEFAULT CURRENT_TIMESTAMP);

-- Ergänzen eines Triggers für die Referenztabelle abflussparameter
CREATE TRIGGER IF NOT EXISTS trig_ref_abflussparameter AFTER UPDATE OF apnam ON abflussparameter
    BEGIN
        UPDATE flaechen
        SET abflussparameter = new.apnam
        WHERE abflussparameter = old.apnam AND abflussparameter IS NOT NULL;
        UPDATE tezg
        SET abflussparameter = new.apnam
        WHERE abflussparameter = old.apnam AND abflussparameter IS NOT NULL;
    END;
