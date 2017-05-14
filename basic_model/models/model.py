"""Interlocutor for an evolutionary language game.

Definitions:
  active matrix (P matrix): matrix that gives the likelihood of identifying a
    particular meaning given a signal. See [1], 149.
  passive matrix (Q matrix): matrix that gives the likelihood of producing a
    particular signal in response to a given meaning. See [1], 149.
  association matrix (A matrix): matrix derived from observing another
    another interlocutor's responses to various objects; this matrix is a sample
    derived from the probability distribution of the "parent"'s P matrix. See
    [1], 150.
"""


import logging
import numpy

from basic_model.util import helpers


class Interlocutor(object):
  """A communicative agent."""

  def __init__(self, active_matrix, passive_matrix, normalize=False):
    """Initializes the internal P and Q matrices.
    
    Arguments:
      active_matrix: The desired P matrix.
      passive_matrix: The desired Q matrix.
      normalize: Whether to convert the given matrices into probability
        distributions.

    Raises:
      ValueError if P or Q is not a probability distribution.
    """
    if normalize:
      active_matrix = helpers.make_probability_distribution(active_matrix)
      passive_matrix = helpers.make_probability_distribution(passive_matrix)
   
    if not helpers.is_probability_distribution(active_matrix):
      logging.error(active_matrix)
      raise ValueError(
          'P matrix is not a probability distribution. '
          'Supply normalize=True or ensure rows of P matrix sum to 1.')
    if not helpers.is_probability_distribution(passive_matrix):
      logging.error(passive_matrix)
      raise ValueError(
          'Q matrix is not a probability distribution. '
          'Supply normalize=True or ensure rows of Q matrix sum to 1.')

    self._active_matrix = active_matrix
    self._passive_matrix = passive_matrix

  @classmethod
  def with_random_matrices(cls, number_signals, number_meanings):
    """Factory function; randomly initializes P and Q matrices.

    Arguments:
      number_signals: Number of signals in the lexicon.
      number_meanings: Number of objects that can be referenced.

    Returns:
      An Interlocutor with randomly-initialized P and Q matrices.
    """
    active_matrix = numpy.random.rand(number_meanings, number_signals)
    passive_matrix = numpy.random.rand(number_signals, number_meanings)
    return Interlocutor(active_matrix, passive_matrix, normalize=True)

  @classmethod
  def from_association_matrix(cls, association_matrix):
    """Factory function; derives P and Q from an A matrix.

    Arguments:
      association_matrix: Observed meaning->signal mapping samples.

    Returns:
      An Interlocutor with P and Q derived from A.
    """
    active_matrix = helpers.make_probability_distribution(association_matrix)
    passive_matrix = helpers.make_probability_distribution(association_matrix.T)
    return Interlocutor(association_matrix, association_matrix.T, normalize=True)

  def get_signal(self, meaning_index):
    """Returns a signal by sampling from the P matrix.

    Arguments:
      meaning_index: Index of the meaning for which to produce a signal.

    Returns:
      The index of a signal determined by the weights in the active matrix.

    Raises:
      IndexError if meaning_index >= number of signals or meaningy_index < 0.
    """
    return helpers.weighted_index(self._active_matrix[meaning_index], 1)[0]
 
  def get_meaning(self, signal_index):
    """Returns a meaning by sampling from the Q matrix.

    Arguments:
      signal_index: Index of the signal for which to produce a meaning.

    Returns:
      The index of a meaning determined by the weights in the passive matrix.

    Raises:
      IndexError if signal_index >= number of meanings or signal_index < 0.
    """
    return helpers.weighted_index(self._passive_matrix[signal_index], 1)[0]

  @property
  def active_matrix(self):
    return self._active_matrix

  @property
  def passive_matrix(self):
    return self._passive_matrix

  def __repr__(self):
    return '\n'.join(map(repr, [self.active_matrix, self.passive_matrix]))
