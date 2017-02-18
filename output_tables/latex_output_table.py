import numpy as np
import re

from .helpers import determine_best_function

class LatexOutputTable:
  #HIGHLIGHTS_MONO   = [Highlights.Bold, Highlights.Italicize]
  HIGHLIGHTS_MONO   = ['\\textbf', '\\textit']
  HIGHLIGHTS_COLOR  = ['blue', 'red']
  '''
  Converts table data to latex table
  '''
  def __init__(self):
   self._table_names = list()
   self._data_frames = list()


  @property
  def table_names(self):
    return self._table_names

  @property
  def column_headers(self):
    return self._data_frames

  def highlight(self, text, table_num):
    '''
    Highlights the text as important.
    Same highlight is applied to throughout the same table, but
    the highlights applied inter-tables should be different
    '''
    def highlight_color(text, table_num):
      return '{\color{%s} %s}' % (self.HIGHLIGHTS_COLOR[table_num], text)

    def highlight_mono(text, table_num):
      return '%s{%s}' % (self.HIGHLIGHTS_MONO[table_num], text)

    if table_num > len(self.HIGHLIGHTS_MONO):
      print("Not enough highlighters...reusing")
      table_num = table_num % len(self.HIGHLIGHTS_MONO)

    return highlight_mono(highlight_color(text, table_num), table_num)



  #def add_data(self, row_num, col_num, value):
  def add_data(self, table_name, data_frame):
    '''
    Adds the value at the specified row and column header
    '''
    self._table_names.append(table_name)
    self._data_frames.append(data_frame)

  def save(self, directory, aggregate_tables=False):
    if aggregate_tables:
      self.save_aggregate(directory)
    else:
      self.save_separate(directory)

  def save_aggregate(self, directory):
    '''
    Saves collected data into one table.
    The output will be:
          |   col1    |   col2    | ... |
      row1|df1|df2|...|df1|df2|...| ... |
      row2|(a1,b1,...)|(a2,b2,...)| ... |
      row3| ...       |           |     |
    '''
    df = self._data_frames[0]
    base_columns = list(df)
    num_cols = len(base_columns)

    base_rows = list(df.index)
    num_rows = len(base_rows)

    equal_columns = True
    equal_rows = True
    for df in self._data_frames[1:]:
      assert(num_cols == len(set(df)), 'All CSV tables should be the same width')
      assert(num_rows == len(set(df.index)), 'All CSV tables should be the same height')
      if set(base_columns) != set(df):
        equal_columns = False
      if set(base_rows) != set(df.index):
        equal_rows = False

    if not equal_columns:
      print('Not all CSV tables are using the same columns: %s' % (', '.join(base_columns)))
    if not equal_rows:
      print('Not all CSV tables are using the same rows: %s' % (', '.join(base_rows)))

    num_tables = len(self._data_frames)
    # Begin creating latex table
    with open(directory + 'aggregate.representative.textable', 'w') as tex_table:
      tex_table.write('\\begin{tabular}[H]{%s}\n\\hline\n' % (('|c' * (num_tables*(num_cols)+1)) + '|'))

      tex_separator = ' & '
      tex_row = ''
      for header in base_columns:
        tex_row += tex_separator
        tex_row += '\multicolumn{%d}{|c|}{%s}' % (num_tables, re.sub(r'\_', '\\_', header))
      tex_table.write(tex_row + '\\\\ \n')

      # display each table name under each column, (the first cell in the row should be empty)
      tex_separator = ' & '
      tex_row = ''
      print(self._table_names)
      for table_name in self._table_names * num_cols:
        tex_row += tex_separator
        tex_row += re.sub(r'\_', '\\_', table_name)
      tex_table.write(tex_row + '\\\\ \n \\hline\n')

      for row_idx in base_rows:
        tex_table.write(row_idx)
        tex_separator = ' & '
        tex_row = ''
        for col_idx in base_columns:
          table_num = 0
          for data_frame in self._data_frames:
            (best_fn, display_fn) = determine_best_function(data_frame.loc[row_idx])
            value = data_frame.loc[row_idx, col_idx]
            value_of_interest = best_fn(data_frame.loc[row_idx])

            tex_row += tex_separator
            if value == value_of_interest:
              tex_row += self.highlight(display_fn(value), table_num)
            else:
              tex_row += '%s' % (display_fn(value))

            table_num += 1

        # end of row values
        tex_table.write(tex_row)
        tex_table.write('\\\\ \n\\hline\n')

      # finish all table rows
      tex_table.write('\\end{tabular}')

  def save_separate(self, directory):
    '''
    Saves collected data into separate files.
    TODO: could just save file when data is added so we do not have to
      keep in memory.
    TODO: add ability to auto-sum rows/cols
    '''
    for idx in range(0, len(self._table_names)):
      table_name = self._table_names[idx]
      data_frame = self._data_frames[idx]

      num_cols = len(data_frame.values[0])
      with open(directory + table_name + '.representative.textable', 'w') as tex_table:
        tex_table.write('\\begin{tabular}[H]{%s}\n\\hline\n' % (('|c' * (num_cols+1)) + '|'))
        (best_fn, display_fn) = determine_best_function(data_frame.values[0])

        tex_separator = ' & '
        tex_row = table_name
        for header in list(data_frame):
          tex_row += tex_separator
          tex_row += re.sub(r'\_', '\\_', header)
        tex_table.write(tex_row + '\\\\ \n')

        horizontal_line = '\\hline\n'
        for row in data_frame.itertuples():
          value_of_interest = best_fn(row)

          tex_table.write(horizontal_line)
          tex_separator = ' & '
          tex_row = row[0]  # Row Header
          for value in row[1:]: # Only numbers
            tex_row += tex_separator
            if value == value_of_interest:
              tex_row += '\\textbf{%s}' % (display_fn(value))
            else:
              tex_row += '%s' % (display_fn(value))

          # end of row values
          tex_table.write(tex_row)
          tex_table.write('\\\\ \n')

        tex_table.write('\\hline\n')
        # finish all table rows
        tex_table.write('\\end{tabular}')
