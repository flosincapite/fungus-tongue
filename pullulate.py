import numpy

from projects.language_games.compositional_model import helpers
from projects.language_games.compositional_model import model


def F(L1, L2):
  return 0.5 * (numpy.sum(
    L1.active_matrix * L2.passive_matrix.T +
    L2.active_matrix * L1.passive_matrix.T))


def max_F_for_active_matrix(active_matrix):
  return numpy.sum(numpy.max(active_matrix.T))


def total_payoff(individual, individuals):
  # return numpy.sum(
  #     F(individuals[individual_index], revelator)
  #     for revelator_index, revelator in enumerate(individuals)
  #     if individual_index != revelator_index)
  # TODO: This is hella slow. Can just cache the calculation once, then
  #   reaccess each time. 
  payoff_vector = numpy.vectorize(lambda revelator: F(individual, revelator))
  return numpy.sum(payoff_vector(individuals)) - F(individual, individual)


def elitist_strategy(number_culled, fitness_function, reproduction_strategy):
  """Reproductive strategy.

  Generations are permitted to overlap. reproduction_strategy specifies how new
  individuals will be created from the existing population.
  
  Some will be culled;
  the fittest will remain.
  New ones to come
  will come, but after pain.
  """
  def strategy(individuals):
    return [
        reproduction_strategy(individuals) for _ in xrange(number_culled)
    ] + sort(
        individuals,
        cmp=lambda x, y: fitness_function(individuals, x, y))[number_culled:]
  return strategy
  
  
def mingle(individuals, normalized):
  if not individuals:
    return numpy.array([])
  a_revelator = individuals[0]
  association_matrix = numpy.zeros_like(a_revelator.active_matrix)
  for sacred_item in numpy.arange(numpy.size(a_revelator.active_matrix, axis=0)):
    for _ in xrange(k):
      # revelator = individuals[helpers.weighted_index(0, 1)[0]]
      association_matrix[sacred_item, revelator.get_signal(sacred_item)] += 1
  return association_matrix


def clout_strategy():
  """Reproductive strategy.

  New individuals mingle with the current population, sampling their responses
  to objects.
  """
  payoff_vector = numpy.vectorize(
      lambda individual: total_payoff(individual, individuals))
  payoffs = payoff_vector(individuals)
  normalized = helpers.safe_divide(payoffs, numpy.sum(payoffs))
  new_individuals = []

  for _ in individuals:
    new_individuals.append(
        model.Model.from_association_matrix(mingle(individuals, normalized)))
  return numpy.array(new_individuals)


def reveal(revelators, k):
  """Gets association matrix by sampling revelators' active matrices.
 
  Each revelator will respond k times to each object.
  
  Arguments:
    revelators: The individuals whose active matrices will be sampled.
    k: The number of times each revelator will utter sacred syllables.

  Returns:
    An A ("association") matrix recording revelators' pronouncements.
  """
  try:
    item_generator = numpy.arange(numpy.size(
      revelators[0].active_matrix, axis=0))
  except:
    raise
  association_matrix = numpy.zeros_like(revelators[0].active_matrix)
  for sacred_item in item_generator:
    for revelator in revelators:
      for _ in xrange(k):
        association_matrix[sacred_item, revelator.get_signal(sacred_item)] += 1
  return association_matrix


def asexual_reproduction(k, creator):
  def reproduce(revelator): 
    return creator(reveal([revelator], k))
  return reproduce
  


class ParentalStrategy(object):

  def __init__(self, reproduction_function, fitness_function):
    self._reproduce = reproduction_function
    self._fitness = fitness_function

  def __call__(self, individuals):
    fitness_vector = numpy.vectorize(
        lambda individual: self._fitness(individual, individuals))
    fitnesses = fitness_vector(individuals)
    normalized = helpers.safe_divide(fitnesses, numpy.sum(fitnesses))
    new_indices = helpers.weighted_index(normalized)

    # TODO: Create a vfunc to create a freq dict from new_indices, then another
    #   to cache association matrices, obviating duplicate calculation.
    #   Then again, maybe each child SHOULD get a separate A matrix?
    parents = individuals[new_indices]
    return numpy.array([
      self._reproduce(parent) for parent in parents])


def g():
  pass


def iterated_learning(e, environment, creator):
  def reproduce(revelator):
    number_signals = ((1 << len(environment.alphabet)) - 1) * environment.F
    number_meanings = ((1 << environment.V) - 1) * environment.F
    association_matrix = numpy.zeroes([number_signals, number_meanings])
    observations = numpy.random.choice(environment.reified, size=e, replace=False)
    pairs = [
        (observation, revelator.get_signal(observation))
        for obvervation in observations]
    for meaning, signal in pairs:
      signal_indices = set(
          revelator.signal_map.get(label)
          for label in IterableAnonymizer.characteristic_function(signal))
      meaning_indices = set(
          revelator.meaning_map.get(label)
          for label in IterableAnonymizer.characteristic_function(meaning))
      for i in xrange(number_signals):
        for j in xrange(number_meanings):
          delta = [0, -1, 1][i in signal_indices + j in meaning_indices]
          association_matrix[i, j] += delta
    return creator(association_matrix)
  return reproduce
