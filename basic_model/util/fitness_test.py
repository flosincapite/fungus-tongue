#!/usr/bin/python

import numpy
import unittest

from basic_model.models import model
from basic_model.util import fitness


class FitnessTest(unittest.TestCase):
  """Tests for payoff functions."""

  def setUp(self):
    self._interlocutors = [
        model.Interlocutor(
            numpy.array([
              [0.9, 0.1],
              [0.5, 0.5],
              [0.3, 0.7],
            ]),
            numpy.array([
              [0.3, 0.1, 0.6],
              [0.33, 0.33, 0.34],
            ])),
        model.Interlocutor(
            numpy.array([
              [0.7, 0.3],
              [0.5, 0.5],
              [0.3, 0.7],
            ]),
            numpy.array([
              [0.6, 0, 0.4],
              [0, 0.5, 0.5],
            ])),
        model.Interlocutor(
            numpy.array([
              [0.1, 0.9],
              [0.2, 0.8],
              [0.3, 0.7],
            ]),
            numpy.array([
              [0.1, 0.3, 0.6],
              [0.5, 0.3, 0.2],
            ])),
    ]

  def testF(self):
    self.assertEquals(
        1.101, fitness.F(self._interlocutors[0], self._interlocutors[1]))

  def testFBadDimensions(self):
    bad_dimensions_interlocutor = model.Interlocutor(
        numpy.ones([3, 3]), numpy.ones([2, 2]), normalize=True)
    with self.assertRaises(ValueError):
      _ = fitness.F(self._interlocutors[0], bad_dimensions_interlocutor)
    with self.assertRaises(ValueError):
      _ = fitness.F(bad_dimensions_interlocutor, self._interlocutors[0])

  def testTotalPayoff(self):
    numpy.testing.assert_almost_equal(
        1.9955,
        fitness.total_payoff(self._interlocutors[0], self._interlocutors))
    numpy.testing.assert_almost_equal(
        1.986,
        fitness.total_payoff(self._interlocutors[1], self._interlocutors))
    numpy.testing.assert_almost_equal(
        1.7795,
        fitness.total_payoff(self._interlocutors[2], self._interlocutors))


if __name__ == '__main__':
  unittest.main()
