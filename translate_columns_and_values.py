import csv


def get_column_and_translation(row):
  split_row = row.split(':')
  column = split_row[0]
  column_translated = split_row[1].strip()

  return column, column_translated

def get_value_and_translation(row):
  split_row = row.split('\t')
  value = split_row[0].strip()
  value_translated = split_row[1].strip()

  return value, value_translated

def prepare_translation(translations_file):
  column = ''
  translations = {}

  for row in translations_file:
    if row[0].isalnum():
      column, column_translated = get_column_and_translation(row)
      translations[column] = {
        'column_translated': column_translated,
        'values_translated': {},
      }
    elif row.strip() == '':
      pass
    else:
      value, value_translated = get_value_and_translation(row)
      translations[column]['values_translated'][value] = value_translated

  return translations

def translate_column(column, translations):
  return translations.get(column, {'column_translated': column})['column_translated']

def translate_columns(columns, translations):
  return [translate_column(column, translations) for column in columns]

def translate_values(row, columns, translations):
  row_translated = {}
  for i in range(len(columns)):
    column = columns[i]
    column_translated = translate_column(column, translations)
    row_translated[column_translated] = translations \
      .get(column, {'values_translated': {row[i]: row[i]}}) \
      .get('values_translated', {row[i]: row[i]}) \
      .get(row[i], row[i])

  return row_translated

def translate(source_csv, target_csv, translations):
  csv_reader = csv.reader(source_csv, delimiter=',')

  columns = next(csv_reader)
  columns_translated = translate_columns(columns, translations)
  writer = csv.DictWriter(target_csv, columns_translated)
  writer.writeheader()

  while row := next(csv_reader, None):
    row_translated = translate_values(row, columns, translations)
    writer.writerow(row_translated)


if __name__ == '__main__':
  with open('data_description.txt', 'r') as translations_file:
    translations = prepare_translation(translations_file)

  with open('raw_data.csv') as source_csv:
    with open('house-prices.csv', mode='w') as target_csv:
      translate(source_csv, target_csv, translations)
