import numpy as np
import re

from .helpers import determine_best_function

class LatexOutputTable:
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
    print("saving aggregate")

  def save_separate(self, directory):
    '''
    Saves collected data into separate files.
    TODO: could just save file when data is added so we do not have to
      keep in memory.
    TODO: add ability to auto-sum rows/cols
    '''
    print("saving separate")
    for idx in range(0, len(self._table_names)):
      table_name = self._table_names[idx]
      data_frame = self._data_frames[idx]

      num_cols = len(data_frame.values[0])
      with open(directory + table_name + '.representative.textable', 'w') as tex_table:
        tex_table.write('\\begin{tabular}[H]{%s}\n\\hline\n' % (('|c' * (num_cols+1)) + '|'))
        (best_fn, display_fn) = determine_best_function(data_frame.values[0])

        tex_separator = ' & '
        tex_row = table_name
        print("col_heaers=")
        print(','.join(list(data_frame)))
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
