import requests
import xlrd


def get_file(url, output_file):
    print 'Downloading %s' % url
    r = requests.get(url, stream=True)

    with open(output_file, 'w') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)

        f.flush()


def read_file(output_file):

    print 'Reading file %s' % output_file

    book = xlrd.open_workbook(output_file)

    sheet_names = book.sheet_names()

    file_contents = {}

    for n_sheet in range(book.nsheets):

        sheet_name = sheet_names[n_sheet]


        sheet = book.sheet_by_index(n_sheet)
        rows = []
        for i in range(sheet.nrows):
            row_values = sheet.row_values(i)
            rows.append(row_values)


        file_contents[sheet_name] = rows

    return file_contents
