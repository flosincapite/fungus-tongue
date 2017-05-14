import numpy

from basic_model.models import model
from basic_model.util import fitness
from basic_model.util import helpers


def reveal(revelator, k):
  """Gets an association matrix by sampling revelator's active matrix.
 
  Revelator will respond k times to each object.
  
  Arguments:
    revelator: The Interlocutor whose active matrix will be sampled.
    k: The number of times revelator will numinously utter.

  Returns:
    An A ("association") matrix recording revelator's pronouncements.
  """
  association_matrix = numpy.zeros_like(revelator.active_matrix)
  for sacred_item in numpy.arange(numpy.size(revelator.active_matrix, axis=0)):
    for _ in xrange(k):
      association_matrix[sacred_item, revelator.get_signal(sacred_item)] += 1
  return association_matrix


def parental_learning(k):
  def reproduce(state):
    payoff_vector = numpy.vectorize(
        lambda individual: fitness.total_payoff(individual, state.individuals))
    payoffs = payoff_vector(state.individuals)
    normalized = helpers.safe_divide(payoffs, numpy.sum(payoffs))
    new_indices = helpers.weighted_index(normalized)

    # TODO: Create a vfunc to create a freq dict from new_indices, then another
    #   to cache association matrices, obviating duplicate calculation. Then
    #   again, maybe each child SHOULD get a separate A matrix?
    parents = state.individuals[new_indices]
    return numpy.array([
      model.Interlocutor.from_association_matrix(reveal(revelator, k))
      for revelator in parents])
  return reproduce


def terminate_iterations(iterations):
  def result_function(state):
    return state.generation > iterations
  return result_function


def terminate_saturated():
  last_result = {}
  def result_function(state):
    payoff_vector = numpy.vectorize(
        lambda individual: fitness.total_payoff(individual, state.individuals))
    payoffs = payoff_vector(state.individuals)
    total = numpy.sum(payoffs)
    previous = last_result.get('result')
    last_result['result'] = total
    return previous is not None and previous >= total
  return result_function


def initialize(number_of_individuals, number_of_signals, number_of_meanings):
  def seed():
    return numpy.array([
      model.Interlocutor.with_random_matrices(
        number_of_signals, number_of_meanings)
      for _ in numpy.arange(number_of_individuals)])
  return seed
