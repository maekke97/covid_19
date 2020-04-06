import pdftotext
import datetime as dt

COLUMNS = [
    'date',
    'ncases_per_day',
    'ncumul_cases',
    'n_hospital_non_icu',
    'n_hospital_icu',
    'n_hospital_icu_non_tube',
    'n_hospital_icu_tube',
    'n_hospital_total',
    'n_icu_covid',
    'n_icu_non_tube',
    'n_icu_tube',
    'n_icu_non_covid',
    'n_icu_total',
    'n_deceased',
    'ncumul_deceased'
]


def parse_table_line(single_line: str) -> str:
    """parse line of entries separated by : and additional spaces.
    handle date
    return csv line, separated by ,
    """
    fields = [dat.strip() for dat in single_line.split(':')]
    if len(fields) < 2:
        return ''
    out_fields = []
    for i, _ in enumerate(COLUMNS):
        if i == 0:
            out_fields.append(dt.datetime.strptime(fields[0].strip().replace('mars', '03').replace('avril', '04'),
                                                   '%d%m%Y').strftime('%d-%m-%Y'))
        elif i < len(fields):
            out_fields.append(fields[i].strip())
        else:
            out_fields.append('')
    return ','.join(out_fields)+'\n'


def pdf_ne_to_csv(input_filename: str, output_filename: str):
    with open(input_filename, 'rb') as ifh:
        pdf_content = pdftotext.PDF(ifh)
    pdf_content_string = '\n'.join(pdf_content)
    # magic column fix (don't know if this is stable)
    pdf_content_string = pdf_content_string.replace('avr\n   il', 'avril')
    # pdf_content_string = pdf_content_string.replace('avr\n il', 'avril')
    # find the start of the table on page 5
    start = pdf_content_string.find('1mars2020')
    data_str = pdf_content_string[start:]
    # handle the overlong indent after the date
    data_str = data_str.replace('2020                      ', '2020:')
    data_str = data_str.replace('                    ', ':')
    data_str = data_str.replace('              ', ':')
    data = [parse_table_line(line) for line in data_str.split('\n')]
    with open(output_filename, 'w', encoding='utf-8') as ofh:
        ofh.write(','.join(COLUMNS) + '\n')
        ofh.writelines(data)


if __name__ == '__main__':
    pdf_ne_to_csv('/home/nem/Downloads/COVID19_PublicationInternet.pdf',
                  '/home/nem/Downloads/COVID19_PublicationInternet.txt')
