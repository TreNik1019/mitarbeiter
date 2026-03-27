-- =========================
-- Indizes löschen
-- =========================
DROP INDEX IF EXISTS
    werksausweis_mitarbeiter_id_idx,
    mitarbeiter_abteilung_id_idx,
    mitarbeiter_nachname_idx;

-- =========================
-- Tabellen löschen
-- =========================
DROP TABLE IF EXISTS
    werksausweis,
    mitarbeiter,
    abteilung;

-- =========================
-- ENUMs löschen
-- =========================
DROP TYPE IF EXISTS
    ausweisstatus,
    position,
    geschlecht;
