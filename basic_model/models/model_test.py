#!/usr/bin/python

import mock
import numpy
import unittest

from basic_model.models import model


class InterlocutorTest(unittest.TestCase):
  """Tests for the behavior of an instantiated Interlocutor."""

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
    self._interlocutor_1 = model.Interlocutor(self._active_1, self._passive_1)

  def testInitFailsWithUnnormalizedActiveMatrix(self):
    with self.assertRaises(ValueError):
      _ = model.Interlocutor(
          numpy.array([0.4, 0.1], [0.5, 0.5], [0.3, 0.7]),
          self._passive_1)

  def testActiveMatrixProperty(self):
    numpy.testing.assert_equal(
        self._active_1, self._interlocutor_1.active_matrix)

  def testPassiveMatrixProperty(self):
    numpy.testing.assert_equal(
        self._passive_1, self._interlocutor_1.passive_matrix)

  def testGetSignal(self):
    # TODO: This is a change detector; find a better strategy than RNG seeding.
    numpy.random.seed(0)
    signals = [
        self._interlocutor_1.get_signal(0), self._interlocutor_1.get_signal(0),
        self._interlocutor_1.get_signal(0), self._interlocutor_1.get_signal(0),
        self._interlocutor_1.get_signal(1), self._interlocutor_1.get_signal(1),
        self._interlocutor_1.get_signal(2), self._interlocutor_1.get_signal(2),
    ]
    self.assertEquals([0, 0, 0, 0, 0, 1, 1, 1], signals)

  def testGetSignalBadIndex(self):
    with self.assertRaises(IndexError):
      _ = self._interlocutor_1.get_signal(3)

  def testGetMeaning(self):
    # TODO: This is a change detector; find a better strategy than RNG seeding.
    numpy.random.seed(0)
    meanings = [
        self._interlocutor_1.get_meaning(0),
        self._interlocutor_1.get_meaning(0),
        self._interlocutor_1.get_meaning(0),
        self._interlocutor_1.get_meaning(0),
        self._interlocutor_1.get_meaning(1),
        self._interlocutor_1.get_meaning(1),
        self._interlocutor_1.get_meaning(1),
        self._interlocutor_1.get_meaning(1),
    ]
    self.assertEquals([0, 2, 2, 0, 1, 2, 1, 2], meanings)

  def testGetMeaningBadIndex(self):
    with self.assertRaises(IndexError):
      _ = self._interlocutor_1.get_meaning(2)


class InterlocutorFactoryTest(unittest.TestCase):
  """Tests for factory class methods of Interlocutor."""

  @mock.patch.object(
      model.numpy.random, 'rand', spec=True,
      return_value=numpy.array([[0.9, 0.8], [0.5, 0]]))
  def testWithRandomMatrices(self, mock_rand):
    # TODO: Weird thing--nosetests can't find model if I try this with
    #   @mock.patch(...), etc., but bare python can. Investigate; file bug.
    new_interlocutor = model.Interlocutor.with_random_matrices(2, 2)
    mock_rand.assert_has_calls(
        [mock.call(2, 2), mock.call(2, 2)], any_order=True)

  def testFromAssociationMatrix(self):
    association_matrix = numpy.array([
      [5, 2, 0, 3],
      [2, 1, 0, 7],
    ])
    new_interlocutor = model.Interlocutor.from_association_matrix(
        association_matrix)
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
        expected_active, new_interlocutor.active_matrix, decimal=5)
    numpy.testing.assert_almost_equal(
        expected_passive, new_interlocutor.passive_matrix, decimal=5)


if __name__ == '__main__':
  unittest.main()
