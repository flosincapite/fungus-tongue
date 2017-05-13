import logging
import numpy

from projects.language_games.compositional_model import helpers
from projects.language_games.compositional_model import symbol_table


class Model(object):

  def __init__(self, active_matrix, passive_matrix):
    self._active_matrix = active_matrix
    self._passive_matrix = passive_matrix

  @property
  def active_matrix(self):
    return self._active_matrix

  @property
  def passive_matrix(self):
    return self._passive_matrix


class NormalizedModel(Model):

  def __init__(self, active_matrix, passive_matrix, normalize=False):
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

    super(NormalizedModel, self).__init__(active_matrix, passive_matrix)

  @classmethod
  def with_random_matrices(cls, number_signals, number_meanings):
    """Factory function for a Model with randomly initialized P and Q matrices.

    Arguments:
      number_signals: Number of signals in the lexicon.
      number_meanings: Number of objects that can be referenced.

    Returns:
      A Model with randomly-initialized P ("active") and Q ("passive") matrices.
    """
    active_matrix = numpy.random.rand(number_meanings, number_signals)
    passive_matrix = numpy.random.rand(number_signals, number_meanings)
    return cls(active_matrix, passive_matrix, normalize=True)

  @classmethod
  def from_association_matrix(cls, association_matrix):
    """Factory function; derives P and Q from an A ("association") matrix.

    Arguments:
      association_matrix: Observed meaning->signal mapping samples.

    Returns:
      A Model with P and Q derived from A.
    """
    active_matrix = helpers.make_probability_distribution(association_matrix)
    passive_matrix = helpers.make_probability_distribution(association_matrix.T)
    return cls(active_matrix, passive_matrix)

  def get_signal(self, meaning_index):
    """Returns a signal index by sampling from the P ("active") matrix.

    Arguments:
      meaning_index: Index of the meaning for which to produce a signal.

    Returns:
      The index of a signal determined by the weights in the active matrix.

    Raises:
      IndexError if meaning_index >= number of signals.
    """
    return helpers.weighted_index(self._active_matrix[meaning_index], 1)[0]
 
  def get_meaning(self, signal_index):
    """Returns a meaning index by sampling from the Q ("passive") matrix.

    Arguments:
      signal_index: Index of the signal for which to produce a meaning.

    Returns:
      The index of a meaning determined by the weights in the passive matrix.

    Raises:
      IndexError if signal_index >= number of meanings.
    """
    return helpers.weighted_index(self._passive_matrix[signal_index], 1)[0]


class Interlocutor(Model):

  def __init__(self, signal_space, meaning_space):
    self._signal_map = symbol_table.SymbolTable()
    self._meaning_map = symbol_table.SymbolTable()
    # world.SignalSpace(alphabet, max_length)
    self._signal_space = signal_space
    # world.MeaningSpace(alphabet, max_length)
    self._meaning_space = meaning_space

  @classmethod
  def from_zero_matrices(cls, number_signals, number_meanings):
    """Factory function for a Model with randomly initialized P and Q matrices.

    Arguments:
      number_signals: Number of signals in the lexicon.
      number_meanings: Number of objects that can be referenced.

    Returns:
      A Model with randomly-initialized P ("active") and Q ("passive") matrices.
    """
    active_matrix = numpy.array.zeros([number_meanings, number_signals])
    passive_matrix = numpy.array.zeros(number_signals, number_meanings)
    return cls(active_matrix, passive_matrix)

  @classmethod
  def from_association_matrix(cls, association_matrix):
    return NotImplemented

  def get_signal(self, meaning_index):
    return NotImplemented
 
  def get_meaning(self, signal_index):
    return NotImplemented


class LabeledModel(Model):

  def __init__(self, signal_space, meaning_space):
    self._signal_map = symbol_table.SymbolTable()
    self._meaning_map = symbol_table.SymbolTable()
    # world.SignalSpace(alphabet, max_length)
    self._signal_space = signal_space
    # world.MeaningSpace(alphabet, max_length)
    self._meaning_space = meaning_space

  @classmethod
  def from_zero_matrices(cls, number_signals, number_meanings):
    """Factory function for a Model with randomly initialized P and Q matrices.

    Arguments:
      number_signals: Number of signals in the lexicon.
      number_meanings: Number of objects that can be referenced.

    Returns:
      A Model with randomly-initialized P ("active") and Q ("passive") matrices.
    """
    active_matrix = numpy.array.zeros([number_meanings, number_signals])
    passive_matrix = numpy.array.zeros(number_signals, number_meanings)
    return cls(active_matrix, passive_matrix)

  @classmethod
  def from_association_matrix(cls, association_matrix):
    return NotImplemented

  def get_signal(self, meaning_index):
    return NotImplemented
 
  def get_meaning(self, signal_index):
    return NotImplemented
