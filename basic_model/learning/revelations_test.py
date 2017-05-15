#!/usr/bin/python

import numpy
import unittest

from basic_model.models import model
from basic_model.learning import revelations


class GenerateTest(unittest.TestCase):

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

  def testRevealForKEqualTo1(self):
    """Tests the behavior of reveal when k = 1."""
    model.numpy.random.seed(0)
    association_matrix = revelations.reveal(self._interlocutors[0], 1)
    expected_association = numpy.array([
      [1, 0],
      [0, 1],
      [0, 1],
    ])
    numpy.testing.assert_equal(expected_association, association_matrix)

  def testRevealForKGreaterThan1(self):
    """Tests the behavior of reveal for k > 1."""
    model.numpy.random.seed(0)
    association_4 = revelations.reveal(self._interlocutors[0], 4)
    expected_4 = numpy.array([
      [4, 0],
      [2, 2],
      [0, 4],
    ])
    numpy.testing.assert_equal(expected_4, association_4)
    association_10 = revelations.reveal(self._interlocutors[0], 10)
    expected_10 = numpy.array([
      [8, 2],
      [5, 5],
      [1, 9],
    ])
    numpy.testing.assert_equal(expected_10, association_10)


if __name__ == '__main__':
  unittest.main()
