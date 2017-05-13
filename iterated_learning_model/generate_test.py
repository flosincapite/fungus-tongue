#!/usr/bin/python

import mock
import numpy
import unittest

from projects.language_games.basic_model import model
from projects.language_games.basic_model import generate


class GenerateTest(unittest.TestCase):

  def setUp(self):
    self._active_1 = numpy.array([
      [0.9, 0.1],
      [0.5, 0.5],
      [0.3, 0.7],
    ])
    self._passive_1 = numpy.array([
      [0.3, 0.1, 0.6],
      [0.33, 0.33, 0.34],
    ])
    self._model_1 = model.Model(self._active_1, self._passive_1)
    self._active_2 = numpy.array([
      [0.7, 0.3],
      [0.5, 0.5],
      [0.3, 0.7],
    ])
    self._passive_2 = numpy.array([
      [0.6, 0, 0.4],
      [0, 0.5, 0.5],
    ])
    self._model_2 = model.Model(self._active_2, self._passive_2)

  def testActiveMatrix(self):
    pass

  @mock.patch(
      'model.numpy.random.rand', spec=True,
      return_value=numpy.array([[0.9, 0.8], [0.5, 0]]))
  def testWithRandomMatrices(self, mock_rand):
    pass

  def testF(self):
    self.assertEquals(1.101, generate.F(self._model_1, self._model_2))

  def testFBadDimensions(self):
    bad_dimensions_model = model.Model(
        numpy.ones([3, 3]), numpy.ones([2, 2]), normalize=True)
    with self.assertRaises(ValueError):
      _ = generate.F(self._model_1, bad_dimensions_model)

  def testRevealForKEqualTo1(self):
    """Tests the behavior of reveal when k = 1."""
    model.numpy.random.seed(0)
    association_matrix = generate.reveal(self._model_1, 1)
    expected_association = numpy.array([
      [1, 0],
      [0, 1],
      [0, 1],
    ])
    numpy.testing.assert_equal(expected_association, association_matrix)

  def testRevealForKGreaterThan1(self):
    """Tests the behavior of reveal for k > 1."""
    model.numpy.random.seed(0)
    association_4 = generate.reveal(self._model_1, 4)
    expected_4 = numpy.array([
      [4, 0],
      [2, 2],
      [0, 4],
    ])
    numpy.testing.assert_equal(expected_4, association_4)
    association_10 = generate.reveal(self._model_1, 10)
    expected_10 = numpy.array([
      [8, 2],
      [5, 5],
      [1, 9],
    ])
    numpy.testing.assert_equal(expected_10, association_10)

  def testTotalPayoff(self):
    model_3 = model.Model(
        numpy.array([
          [0.1, 0.9],
          [0.2, 0.8],
          [0.3, 0.7],
        ]),
        numpy.array([
          [0.1, 0.3, 0.6],
          [0.5, 0.3, 0.2],
        ]))
    individuals = [self._model_1, self._model_2, model_3]
    numpy.testing.assert_almost_equal(
        1.9955, generate.total_payoff(self._model_1, individuals))
    numpy.testing.assert_almost_equal(
        1.986, generate.total_payoff(self._model_2, individuals))
    numpy.testing.assert_almost_equal(
        1.7795, generate.total_payoff(model_3, individuals))


if __name__ == '__main__':
  unittest.main()
