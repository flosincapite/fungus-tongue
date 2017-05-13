import numpy

from projects.language_games.evolutionary_learning import learner
from projects.language_games.evolutionary_learning import pullulate
from projects.language_games.evolutionary_learning import seeds
from projects.language_games.evolutionary_learning import wilts
from projects.language_games.evolutionary_learning import world


class Environment(object):
  pass


# TODO: Start using protobuffers.
LearningState = collections.namedtuple('LearningState', [
  'e', ' F', ' V', 'signal_length', 'meaning_space', 'signal_space',
  'meaning_map', 'signal_map'])


def iterated_learning():
  pass


def reproduce(revelator, learning_state):
  number_signals = len(learning_state.signal_space.size())
  number_meanings = len(learning_state.meaning_space.size())
  association_matrix = numpy.zeroes([number_signals, number_meanings])
  observations = numpy.random.choice(
      learning_state.meaning_space.reified, size=learning_state.e,
      replace=False)
  pairs = [
      (observation, revelator.get_signal(observation))
      for obvervation in observations]
  for meaning, signal in pairs:
    signal_indices = set(
        learning_state.signal_map.get(label)
        for label in IterableAnonymizer.characteristic_function(signal))
    meaning_indices = set(
        learning_state.meaning_map.get(label)
        for label in IterableAnonymizer.characteristic_function(meaning))
    for i in xrange(number_signals):
      for j in xrange(number_meanings):
        delta = [0, -1, 1][i in signal_indices + j in meaning_indices]
        association_matrix[i, j] += delta
  return model.rnterlocutor(association_matrix)
