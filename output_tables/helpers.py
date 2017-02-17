
def determine_best_function(row):
  '''
  Automatically determines what quantity is 'best' based on the values in the row.
  row: list of values (or at least iterable)
  Currently supports:
    maximum if values resemble probabilities [0,1]
    minimum-non-zero otherwise
  '''
  def min_non_zero(X):
    minimum = float('inf')
    for x in X:
      if x > 0.0 and x < minimum:
        minimum = x
    return minimum

  def scientific(x):
    if x == 0.0:
      return '0.0'
    return '%.2e' % x

  def percent(x):
    if x == 0.0:
      return '0.0'
    if x == 1.0:
      return '1.0'
    return '%.2f' % x

  probabilities = True
  for x in row:
    probabilities = probabilities and x <= 1.0

  if probabilities:
    return (max, percent) # use percent notation, 2 significant dig
  else:
    return (min_non_zero, scientific) # use scientific notation
