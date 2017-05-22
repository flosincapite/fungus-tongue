#!/usr/bin/python

import mock
import numpy
import unittest

from projects.language_games.basic_model import model


class ModelTest(unittest.TestCase):

  def setUp(self):
    self._active_1 = numpy.array([
      [0.9, 0.1],
      [0.5, 0.5],
      [0.3, 0.7],
    ])
    self._passive_1 = numpy.array([
      [0.6, 0, 0.4],
      [0, 0.5, 0.5],
    ])
    self._model_1 = model.Model(self._active_1, self._passive_1)

  def testActiveMatrix(self):
    numpy.testing.assert_equal(self._active_1, self._model_1.active_matrix)
    numpy.testing.assert_equal(self._passive_1, self._model_1.passive_matrix)

  @mock.patch(
      'model.numpy.random.rand', spec=True,
      return_value=numpy.array([[0.9, 0.8], [0.5, 0]]))
  def testWithRandomMatrices(self, mock_rand):
    new_model = model.Model.with_random_matrices(2, 2)
    mock_rand.assert_has_calls(
        [mock.call(2, 2), mock.call(2, 2)], any_order=True)

  def testFromAssociationMatrix(self):
    association_matrix = numpy.array([
      [5, 2, 0, 3],
      [2, 1, 0, 7],
    ])
    new_model = model.Model.from_association_matrix(association_matrix)
    expected_active = numpy.array([
      [0.5, 0.2, 0, 0.3],
      [0.2, 0.1, 0, 0.7],
    ])
    expected_passive = numpy.array([
      [0.714285, 0.285714],
      [0.666667, 0.333333],
      [0, 0],
      [0.3, 0.7],
    ])
    numpy.testing.assert_almost_equal(
        expected_active, new_model.active_matrix, decimal=5)
    numpy.testing.assert_almost_equal(
        expected_passive, new_model.passive_matrix, decimal=5)

  def testGetSignal(self):
    model.numpy.random.seed(0)
    signals = [
        self._model_1.get_signal(0), self._model_1.get_signal(0),
        self._model_1.get_signal(0), self._model_1.get_signal(0),
        self._model_1.get_signal(1), self._model_1.get_signal(1),
        self._model_1.get_signal(2), self._model_1.get_signal(2),
    ]
    self.assertEquals([0, 0, 0, 0, 0, 1, 1, 1], signals)

  def testGetSignalBadIndex(self):
    with self.assertRaises(IndexError):
      _ = self._model_1.get_signal(3)

  def testGetMeaning(self):
    model.numpy.random.seed(0)
    meanings = [
        self._model_1.get_meaning(0), self._model_1.get_meaning(0),
        self._model_1.get_meaning(0), self._model_1.get_meaning(0),
        self._model_1.get_meaning(1), self._model_1.get_meaning(1),
        self._model_1.get_meaning(1), self._model_1.get_meaning(1),
    ]
    self.assertEquals([0, 2, 2, 0, 1, 2, 1, 2], meanings)

  def testGetMeaningBadIndex(self):
    with self.assertRaises(IndexError):
      _ = self._model_1.get_meaning(2)


if __name__ == '__main__':
  unittest.main()
