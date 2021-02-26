import unittest

from translate_columns_and_values import *


class TestTranslateColumnsAndValues(unittest.TestCase):

  # get_column_and_translation

  def test_get_column_and_translation(self):
    data = 'a:1'

    column, column_translated = get_column_and_translation(data)

    self.assertEqual(column, 'a')
    self.assertEqual(column_translated, '1')


  def test_get_column_and_translation_with_whitespace(self):
    data = 'a: 1 '

    column, column_translated = get_column_and_translation(data)

    self.assertEqual(column, 'a')
    self.assertEqual(column_translated, '1')

  def test_get_column_and_translation_with_additional_colon(self):
    data = 'a:1:x'

    column, column_translated = get_column_and_translation(data)

    self.assertEqual(column, 'a')
    self.assertEqual(column_translated, '1')


  # get_value_and_translation

  def test_get_value_and_translation(self):
    data = 'a\t1'

    value, value_translated = get_value_and_translation(data)

    self.assertEqual(value, 'a')
    self.assertEqual(value_translated, '1')

  def test_get_value_and_translation_with_whitespace(self):
    data = ' a \t 1 '

    value, value_translated = get_value_and_translation(data)

    self.assertEqual(value, 'a')
    self.assertEqual(value_translated, '1')

  def test_get_value_and_translation_with_additional_tab(self):
    data = 'a\t1\tx'

    value, value_translated = get_value_and_translation(data)

    self.assertEqual(value, 'a')
    self.assertEqual(value_translated, '1')


  # prepare_translation

  def test_prepare_translation(self):
    data = [
      "G:Grades",
      " ",
      " E\tExcellent",
    ]

    translations = prepare_translation(data)

    self.assertEqual(len(translations.keys()), 1)
    self.assertEqual(list(translations.keys())[0], 'G')
    self.assertEqual(translations['G']['column_translated'], 'Grades')
    self.assertEqual(translations['G']['values_translated']['E'], 'Excellent')


  # translate_column

  def test_translate_column(self):
    column = 'A'
    translations = {
      'A': {
        'column_translated': 'Apple'
      },
    }

    column_translated = translate_column(column, translations)

    self.assertEqual(column_translated, 'Apple')

  def test_translate_column_without_translation(self):
    column = 'A'
    translations = {}

    column_translated = translate_column(column, translations)

    self.assertEqual(column_translated, 'A')


  # translate_columns

  def test_translate_columns(self):
    columns = ['A', 'B']
    translations = {
      'A': {
        'column_translated': 'Apple'
      },
    }

    columns_translated = translate_columns(columns, translations)

    self.assertEqual(columns_translated, ['Apple', 'B'])


  # translate_values

  def test_translate_values(self):
    row = ['R', '1', 'x']
    columns = ['A', 'B', 'C']
    translations = {
      'A': {
        'column_translated': 'Apple',
        'values_translated': {
          'R': 'Red',
        },
      },
      'B': {
        'column_translated': 'Banana',
        'values_translated': {},
      },
    }

    row_translated = translate_values(row, columns, translations)

    self.assertEqual(row_translated, {'Apple': 'Red', 'Banana': '1', 'C': 'x'})


if __name__ == '__main__':
  unittest.main()
