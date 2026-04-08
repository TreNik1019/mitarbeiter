-- =========================
-- Indizes löschen
-- =========================
DROP INDEX IF EXISTS
    werksausweis_mitarbeiter_id_idx,
    mitarbeiter_auftrag_id_idx,
    mitarbeiter_nachname_idx;

-- =========================
-- Tabellen löschen
-- =========================
DROP TABLE IF EXISTS
    werksausweis,
    mitarbeiter,
    auftrag;

-- =========================
-- ENUMs löschen
-- =========================
DROP TYPE IF EXISTS
    ausweisstatus,
    position,
    geschlecht;
