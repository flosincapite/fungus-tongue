"""Functions related to evolutionary fitness (see README.md, [1]). """


import numpy


def F(L1, L2):
  """Calculates the payoff between two languages.
  
  Payoff is defined here as total informational exchange between interlocutors,
  i.e. the amount of successful communication expected over a series of
  interlocutions. See Nowak et al., 149 [1].

  Arguments:
    L1: A Interlocutor.
    L2: A Interlocutor.

  Returns:
    The payoff between the two interlocutors.

  Raises:
    ValueError if L1 and L2 do not have compatible dimensions.
  """
  return 0.5 * (numpy.sum(
    L1.active_matrix * L2.passive_matrix.T +
    L2.active_matrix * L1.passive_matrix.T))


def total_payoff(individual, population):
  """Calculates an individual's total payoff given its population.
  
  Individual is assumed to be a member of population. The total payoff of the
  individual (its evolutionary fitness) is simply the sum of the payoff holding
  between it and each other member of the population.

  Returns:
    The sum of F(individual, other) for every other individual in population.

  Raises:
    ValueError whenever two individuals have incompatible dimensions.
  """
  payoff_vector = numpy.vectorize(lambda revelator: F(individual, revelator))
  return numpy.sum(payoff_vector(population)) - F(individual, individual)
