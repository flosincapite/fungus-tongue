"""Helper functions for common mathematical operations."""

import numpy


def weighted_index(distribution, number_of_results=None):
  """Gets an array of integers in [0, len(DISTRIBUTION)) by random sampling.
 
  Args:
    distribution: The probability distribution from which to sample; for each
      index i in [0, len(distribution)), the probability that i will be in the
      output array is equal to `distribution[i]`.
    number_of_results: How many integers to output (equal to `len(distribution)`
      if this is a nullary value).

  Returns:
    A one-dimensional array of integers.

  Raises:
    ValueError if distribution is not a probability distribution.
  """
  shape_matrix = [
      len(distribution) if number_of_results is None else number_of_results]
  return numpy.random.choice(
      a=len(distribution), size=shape_matrix, p=distribution)


def sum_rows(array):
  """Gets a row matrix consisting of the sum of the rows in array."""
  row_sums = numpy.sum(array, axis=1)
  return row_sums.reshape([numpy.size(array, axis=0), 1])


def is_probability_distribution(array):
  """Checks that every row in array either sums-ish to 1 or is but zeros."""
  for row in array:
    if not (
        numpy.isclose(numpy.sum(row), 1)
        or numpy.all(row == numpy.zeros_like(row))):
      return False
  return True


def safe_divide(numerator, denominator):
  """Divides two arrays, replacing n/0 results with 0."""
  with numpy.errstate(divide='ignore', invalid='ignore'):
    result = numpy.true_divide(numerator, denominator)
    result[ ~ numpy.isfinite(result)] = 0
  return result


def make_probability_distribution(matrix):
  """Normalizes matrix so that all rows sum to 1 (or contain only zeros).
  
  Args:
    matrix: A two-dimensional array.

  Returns:
    matrix with all rows normalized to sum to 1 (zero rows unchanged).

  Raises:
    ValueError if the matrix is degenerate (rows of different lengths, etc.).
  """
  denominator = numpy.sum(
      matrix, axis=1).reshape([numpy.size(matrix, axis=0), 1])
  return safe_divide(matrix, denominator)
