
import download_xls
from db import SQLite3


def load_incidence_data(db):
    url = 'http://www.who.int/entity/immunization/monitoring_surveillance/data/incidence_series.xls?ua=1'
    output_file = 'incidences.xls'
    download_xls.get_file(url, output_file)
    contents = download_xls.read_file(output_file)

    print 'Inserting incidence data to db'

    c = db.cursor()

    for sheet in contents:

        if sheet in ['Readme Incidence', 'Reg_&_Global_Incidence']:
            continue

        rows = contents.get(sheet)

        headers = []
        for i in range(len(rows)):
            if i == 0:
                headers = rows[i]
            else:
                data = rows[i]
                region = data[0]
                iso_code = data[1]
                country = data[2]
                disease = data[3]

                for j in range(4, len(data)):
                    year = headers[j]
                    value = data[j]
                    if value:
                        SQLite3.insert(c, 'incidents', (region, iso_code, country, disease, year, value))
        db.commit()


def load_coverage_data(db):
    url = 'http://www.who.int/entity/immunization/monitoring_surveillance/data/coverage_series.xls?ua=1'
    output_file = 'coverage.xls'
    download_xls.get_file(url, output_file)
    contents = download_xls.read_file(output_file)

    print 'Inserting coverage data to db'

    c = db.cursor()

    for sheet in contents:

        if sheet in ['Readme Coverage']:
            continue

        rows = contents.get(sheet)

        headers = []
        for i in range(len(rows)):
            if i == 0:
                headers = rows[i]
            else:
                data = rows[i]
                region = data[0]
                iso_code = data[1]
                country = data[2]
                vaccine = data[3]

                for j in range(4, len(data)):
                    year = headers[j]
                    value = data[j]
                    if value:
                        SQLite3.insert(c, 'coverage', (region, iso_code, country, vaccine, year, value))
        db.commit()


def main():
    db = SQLite3('data.db', 'schema.sql')
    load_incidence_data(db)
    load_coverage_data(db)

if __name__ == '__main__':
    main()
