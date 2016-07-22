import requests
from db import SQLite3
import pandas as pd
import pyprind


def population_country_list():
    print 'Retreiving list of country names from population.io'
    r = requests.get('http://api.population.io:80/1.0/countries')
    r.raise_for_status()
    json = r.json()
    return json['countries']


def who_country_list():
    print 'Retreiving list of country names from WHO dataset'
    db = SQLite3('data.db')
    sql = """
    SELECT DISTINCT country_name
      FROM (
               SELECT country_name
                 FROM coverage
               UNION ALL
               SELECT country_name
                 FROM incidents
           )
    WHERE country_name <> ''
    ORDER BY country_name;
    """
    c = db.cursor().execute(sql)
    results = map(lambda x: x[0], c.fetchall())
    return results


def generate_country_map(p_countries, w_countries):
    print 'Generating csv map for country names'
    map_who = []
    map_p = []
    for w_country in w_countries:
        if w_country in p_countries:
            map_who.append(w_country)
            map_p.append(w_country)
        else:
            w_country_stripped = w_country.strip('(the)').strip()
            if w_country_stripped in p_countries:
                map_who.append(w_country)
                map_p.append(w_country_stripped)
            else:
                map_who.append(w_country)
                map_p.append('')

    df = pd.DataFrame({'who_country': map_who, 'p_country': map_p})
    df.to_csv('country_map.csv', encoding='utf-8')


def save_complete_map():
    db = SQLite3('data.db')
    c = db.cursor()
    df = pd.read_csv('country_map_complete.csv')

    for i in df.index:
        who_country = df.ix[i]['who_country']
        p_country = df.ix[i]['p_country']

        SQLite3.insert(c, 'countries', [who_country, p_country])

    db.commit()


def get_populations():

    populations = []

    db = SQLite3('data.db')
    c = db.cursor().execute("""
    SELECT DISTINCT year,
                    population_country_name as country
      FROM (
               SELECT year,
                      country_name
                 FROM coverage
               UNION ALL
               SELECT year,
                      country_name
                 FROM incidents
           )
           LEFT OUTER JOIN
           countries ON who_country_name = country_name
     WHERE population_country_name IS NOT NULL
     ORDER BY population_country_name,
              year;
    """)

    rows = c.fetchall()

    bar = pyprind.ProgBar(len(rows), title='Downloading population data')
    i = 0
    for row in rows:

        country = row['country']
        year = row['year']

        url = 'http://api.population.io:80/1.0/population/%s/%s/' % (year, country)
        r = requests.get(url)
        r.raise_for_status()
        entries = r.json()
        total = 0
        for entry in entries:
            total += entry['total']

        data = (country, year, total)
        populations.append(data)
        bar.update()

    print 'Inserting population data into db'
    SQLite3.insertmany(c, 'populations', populations)
    db.commit()


if __name__ == '__main__':

    # p_countries = population_country_list()
    # w_countries = who_country_list()
    # generate_country_map(p_countries, w_countries)

    save_complete_map()
    get_populations()
