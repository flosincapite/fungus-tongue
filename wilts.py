# Functions related to the cull.


def C(individual, signal_distance, meaning_distance):
  pass


def terminate_iterations(iterations):
  def result_function(learning_state):
    return learning_state.generation > iterations
  return result_function


def terminate_saturated():
  last_result = {}
  def result_function(learning_state):
    payoff_vector = numpy.vectorize(
        lambda individual: total_payoff(individual, learning_state.individuals))
    payoffs = payoff_vector(learning_state.individuals)
    total = numpy.sum(payoffs)
    previous = last_result.get('result')
    last_result['result'] = total
    return previous is not None and previous >= total
  return result_function
