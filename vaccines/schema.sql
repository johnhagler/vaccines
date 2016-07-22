PRAGMA encoding="UTF-8";

drop table if exists incidents;

create table incidents (
    region text,
    country_iso text,
    country_name text,
    disease text,
    year integer,
    incident_count real
);

drop table if exists coverage;

create table coverage (
    region text,
    country_iso text,
    country_name text,
    vaccine text,
    year integer,
    incident_count real
);

drop table if exists countries;

create table countries (
    who_country_name text,
    population_country_name text
);

drop table if exists populations;

create table populations (
    country_name text,
    year integer,
    population real
);