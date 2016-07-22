import requests
import xlrd


def get_file():
    url = 'http://www.who.int/entity/immunization/monitoring_surveillance/data/incidence_series.xls?ua=1'
    r = requests.get(url, stream=True)

    with open('outfile.xls', 'w') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)

        f.flush()


def read_file():

    file_contents = []

    book = xlrd.open_workbook('outfile.xls')

    sheet_names = book.sheet_names()

    for n_sheet in range(book.nsheets):

        if n_sheet not in [0, book.nsheets]:

            sheet_name = sheet_names[n_sheet]
            print sheet_name

            sheet = book.sheet_by_index(n_sheet)
            rows = []
            for i in range(sheet.nrows):
                row_values = sheet.row_values(i)
                rows.append(row_values)
                print row_values

            file_content = {sheet_name: rows}

            file_contents.append(file_content)

    return file_contents
