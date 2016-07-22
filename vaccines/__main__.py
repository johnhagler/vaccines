
import download_xls
from db import SQLite3


def main():
    url = 'http://www.who.int/entity/immunization/monitoring_surveillance/data/incidence_series.xls?ua=1'
    output_file = 'incidences.xls'
    download_xls.get_file(url, output_file)
    contents = download_xls.read_file(output_file)

    db = SQLite3('data.db', 'schema.sql')
    c = db.cursor()

    print 'Inserting data to db'

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


if __name__ == '__main__':
    main()
