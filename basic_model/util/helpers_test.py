#!/usr/bin/python

import numpy
import unittest

from basic_model.util import helpers


class HelpersTest(unittest.TestCase):
  """Tests evaluating various utility functions."""

  def testWeightedIndex(self):
    distribution = numpy.array([0.0, 1.0, 0.0, 0.0])

    # 1 until the end of time.
    expected = numpy.array([1, 1, 1, 1, 1, 1])
    numpy.testing.assert_equal(
        expected, helpers.weighted_index(distribution, len(expected)))

  def testWeightedIndexDefaultNumberResults(self):
    distribution = numpy.array([0.0, 1.0, 0.0, 0.0])

    # 1 until the end of time.
    expected = numpy.array([1, 1, 1, 1])
    numpy.testing.assert_equal(expected, helpers.weighted_index(distribution))

  def testWeightedIndexRespectsDistribution(self):
    # TODO: This is a change detector; find a better strategy than RNG seeding.
    numpy.random.seed(0)
    distribution = numpy.array([0.3, 0.0, 0.3, 0.3, 0.1])
    expected = [2, 2, 2, 2, 2, 3, 3, 3, 3, 4]
    self.assertItemsEqual(
        expected, helpers.weighted_index(distribution, len(expected)))

  def testIsProbabilityDistributionTrue(self):
    distribution = numpy.array([
      [0.4, 0.4, 0.2],  # Sums to 1.
      [0.0, 0.0, 0.0],  # All entries are 0.
    ])
    self.assertTrue(helpers.is_probability_distribution(distribution))

  def testIsProbabilityDistributionFalse(self):
    distribution = numpy.array([
      [0.4, 0.4, 0.1],  # Does not sum to 1.
    ])
    self.assertFalse(helpers.is_probability_distribution(distribution))

  def testSafeDivideArrayByArray(self):
    numerator = numpy.array([1.0, 1.0, 1.0, 1.0])
    denominator_array = numpy.array([0, 2, 1, 0])
    numpy.testing.assert_equal(
        numpy.array([0, 0.5, 1.0, 0]),
        helpers.safe_divide(numerator, denominator_array))

  def testSafeDivideArrayByScalar(self):
    numerator = numpy.array([2.0, 1.0, 0.5, 0.0])
    numpy.testing.assert_equal(
        numpy.array([1.0, 0.5, 0.25, 0.0]),
        helpers.safe_divide(numerator, 2))
    numpy.testing.assert_equal(
        numpy.array([0, 0, 0, 0]),
        helpers.safe_divide(numerator, 0))
   
  def testMakeProbabilityDistribution(self):
    matrix = numpy.array([
      [1, 2, 3, 4],
      [50, 30, 0, 0],
      [0, 0, 0, 0],
    ])
    expected = numpy.array([
      [0.1, 0.2, 0.3, 0.4],
      [0.625, 0.375, 0.0, 0.0],
      [0.0, 0.0, 0.0, 0.0],
    ])
    numpy.testing.assert_equal(
        expected, helpers.make_probability_distribution(matrix))
   
  def testMakeProbabilityDistributionWeirdShape(self):
    matrix = numpy.array([
      [1, 2, 3, 4],
      [50, 30],
      [0, 0, 0, 0],
    ])
    with self.assertRaises(ValueError):
      _ = helpers.make_probability_distribution(matrix)


if __name__ == '__main__':
  unittest.main()
