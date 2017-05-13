import numpy

from projects.language_games.compositional_model import model


class CapriciousDemiurge(object):

  def __init__(
      self, number_individuals, number_signals, number_meanings,
      creator=model.NormalizedModel.with_random_matrices):
    self._number_individuals = number_individuals
    self._number_meanings = number_meanings
    self._number_signals = number_signals
    self._creator = creator

  def __call__(self):
    return numpy.array([
      self._creator(self._number_signals, self._number_meanings)
      for _ in numpy.arange(self._number_individuals)])
