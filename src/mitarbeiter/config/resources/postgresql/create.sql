SET default_tablespace = mitarbeiterspace;

-- =========================
-- ENUMs
-- =========================
CREATE TYPE geschlecht AS ENUM ('MAENNLICH', 'WEIBLICH', 'DIVERS');

CREATE TYPE position AS ENUM ('MANAGER', 'ENTWICKLER', 'DESIGNER', 'TESTER');

CREATE TYPE ausweisstatus AS ENUM ('AKTIV', 'GESPERRT', 'ABGELAUFEN');


-- =========================
-- Mitarbeiter
-- =========================
CREATE TABLE IF NOT EXISTS mitarbeiter (
    id              INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    version         INTEGER NOT NULL DEFAULT 0,
    nachname        TEXT NOT NULL,
    email           TEXT NOT NULL UNIQUE,
    "position"        "position" NOT NULL,
    gehalt          NUMERIC(10,2) NOT NULL CHECK (gehalt >= 0),
    eintrittsdatum  DATE NOT NULL CHECK (eintrittsdatum <= current_date),
    homepage        TEXT,
    geschlecht      geschlecht,
    username        TEXT NOT NULL,
    erzeugt         TIMESTAMP NOT NULL,
    aktualisiert    TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS mitarbeiter_nachname_idx
    ON mitarbeiter(nachname);


    -- =========================
-- Auftrag
-- =========================
CREATE TABLE IF NOT EXISTS auftrag (
    id                INTEGER PRIMARY KEY,
    bezeichnung       TEXT NOT NULL,
    auftragserteilung DATE NOT NULL,
    dauer             DATE NOT NULL,
    mitarbeiter_id    INTEGER NOT NULL REFERENCES mitarbeiter ON DELETE CASCADE
    );

CREATE INDEX IF NOT EXISTS auftrag_mitarbeiter_id_idx
    ON auftrag(mitarbeiter_id);
-- =========================
-- Werksausweis
-- =========================
CREATE TABLE IF NOT EXISTS werksausweis (
    id                  INTEGER PRIMARY KEY,
    status              ausweisstatus NOT NULL,
    ausstellungsdatum   DATE NOT NULL,
    guthaben            NUMERIC(10,2) NOT NULL CHECK (guthaben >= 0),
    mitarbeiter_id      INTEGER NOT NULL REFERENCES mitarbeiter ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS werksausweis_mitarbeiter_id_idx
    ON werksausweis(mitarbeiter_id);
