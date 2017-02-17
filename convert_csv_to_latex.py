# converts csv table to latex and bolds the 'best' value per row
import os
import re
import sys
import pandas as pd
import numpy as np


from output_tables.latex_output_table import LatexOutputTable

DELIMETER = '\s+'

# Arguments:
# 1: input csv file
# could add delimeter optional as well as definition of what constitutes 'best' value per row
# ASSUMPTIONS:
#   values are numbers




def convert_csv_to_latex(csv_ordered_files, delimeter, column_headers_to_keep=None, aggregate_tables=False):
  '''
  csv_ordered_files: csv files to convert to another table format
  delimeter: delimeter used within the csv files
  column_headers_to_keep: columns to keep if some are wished to be discarded
    TODO: this parameter is kind of hackish..it involves alot of manual intervention.
      maybe try to eventually make it 'representative_sets' where the algorithm determines
      the best column within each representative_set and only outputs that to the other
      table format
  aggregate_tables: boolean whether to place all tables into one
  '''

  assert(len([x for x in csv_ordered_files if os.path.splitext(x)[1] == '.csv']) > 0)
  output_table = LatexOutputTable()
  # strip non-digits
  #match = re.search('\d', value)
  #idx_first_digit = match.start()
  #match = re.match('.+([0-9])[^0-9]*$', value)
  #idx_last_digit = match.start(1)+1
  #value = value[idx_first_digit:idx_last_digit]
  #tex_row += 'p%s' % (value)

  output = LatexOutputTable()
  for csv_filepath in csv_ordered_files:
    with open(csv_filepath, 'r') as csv_file:
      # Read the first word which should be the metric the values represent
      line = csv_file.readline()
      table_name = line.split(None, 1)[0]

      csv_file.seek(0)  # Reset to Start of file
      # Read file as csv and add to output
      data_frame = pd.read_csv(csv_file, sep=delimeter, index_col=0)
      output.add_data(table_name, data_frame)

    #with open(csv_filepath, 'r') as csv_file:
    #  print(csv_file)
    #  data_frame = pd.read_csv(csv_file, sep=delimeter, index_col=0)
    #  row_headers = list(data_frame.index)
    #  if column_headers_to_keep is None:
    #    column_headers = list(data_frame)
    #  else:
    #    column_headers = column_headers_to_keep

    #  print("row headers=")
    #  print(row_headers)
    #  print("col headers=")
    #  print(column_headers)

    #  column_header = list(data_frame)

    #  output.add_new_table(table_name, row_headers, column_headers)
    #  row_num = 0
    #  for row in data_frame.itertuples():
    #    # row is a Series object mapping column header to value
    #    for column_index in output_table.column_headers:
    #      # Store data if it is part of column we are 'keep'ing
    #      print("adding data at %d %d = %d" %(row_num, column_index, row[column_index]))
    #      output.add_data(row_num, column_index, row[column_index])

  directory = os.path.dirname(csv_filepath) + os.sep
  output.save(directory, aggregate_tables=aggregate_tables)



# TODO: want to automate this eventually with representative sets
# This is the part that requires too much human intervention
columns_to_keep = {
    'blocks': ['BFS', 'BFS_DD', 'LUBY', 'EXP', 'PROB0.2'],
    'grid': ['BFS', 'BFS_DD', 'LUBY', 'EXP', 'PROB0.2'],
    'gripper': ['BFS', 'BFS_DD', 'LUBY', 'EXP', 'PROB0.05'],
    'rovers': ['BFS', 'BFS_DD', 'LUBY', 'EXP', 'PROB0.2']
}

if __name__ == '__main__':
  if len(sys.argv) < 2:
    sys.exit()

  directory_or_file = sys.argv[1]
  if os.path.isdir(directory_or_file):
    for root,_,files in os.walk(directory_or_file):
      print(root)
      csv_files = [x for x in files if os.path.splitext(x)[1] == '.csv']
      if len(csv_files) > 0:
        # TODO: make this more automatic, hackish
        for domain_key in columns_to_keep.keys():
          if domain_key in csv_files[0]:
            domain = domain_key
            break

        print("  " + ','.join(csv_files))
        convert_csv_to_latex([ os.path.join(root, x) for x in csv_files], DELIMETER, column_headers_to_keep=columns_to_keep[domain], aggregate_tables=False)

