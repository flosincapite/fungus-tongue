import numpy


def weighted_index(array, number_of_results=None):
  count_matrix = [number_of_results or len(array)]
  return numpy.random.choice(len(array), count_matrix, p=array)


def sum_rows(array):
  row_sums = numpy.sum(array, axis=1)
  return row_sums.reshape([numpy.size(array, axis=0), 1])


def is_probability_distribution(array):
  for row in array:
    if not numpy.allclose(numpy.sum(row), 1) and not numpy.all(row == numpy.zeros_like(row)):
      return False
  return True


def safe_divide(numerator, denominator):
  with numpy.errstate(divide='ignore', invalid='ignore'):
    result = numpy.true_divide(numerator, denominator)
    result[ ~ numpy.isfinite(result)] = 0
  return result


def make_probability_distribution(array):
  denominator = numpy.sum(
      array, axis=1).reshape([numpy.size(array, axis=0), 1])
  # return numpy.divide(
  #     array, denominator, out=numpy.zeros_like(array), where=denominator!=0)
  return safe_divide(array, denominator)
