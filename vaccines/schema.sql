drop table if exists incidents;

create table incidents (
    region text,
    country_iso text,
    country_name text,
    disease text,
    year integer,
    incident_count real
);
