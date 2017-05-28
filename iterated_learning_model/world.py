import random


class Wildcard(object):
  
  def __init__(self, symbol):
    self.symbol = symbol

  @property
  def symbol(cls):
    return self._symbol

  @symbol.setter
  def symbol(cls, new_symbol):
    self._symbol = new_symbol

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.symbol == other.symbol
    return NotImplemented


def characteristic_function(cls, iterable, null_value=Wildcard('<?>')):
  mask = (1 << len(iterable))
  result = []
  while mask > 1:  # Must have at least one non-wildcard component.
    mask -= 1
    bits = bit_array(mask, length(iterable))
    result.append(tuple(
      [null_value, element][bits[i]]
      for i, element in enumerate(iterable)))
  return result


class MeaningSpace(object):
  """Representation of meaning space, the set of all possible observations.

  A meaning space is defined as a set of feature vectors. Let F be the dimension
  of the feature. Let [0, V) be the range from which values may be drawn.

  TODO: Allow continuous values.
  TODO: Consider the user of "distance" as a function property. Why this 
    "has-a" relationship instead of using inheritance? Pythonic? Just bizarre
    OOP?
  """

  def __init__(self, F, V, distance):
    """Sets member variables.
    
    Arguments:
      F: vectors in the space are of dimension 1 x F.
      V: the values of each vector component are in [0, V)
      distance: 
        The distance function between two meanings.
        distance(meaning_a, meaning_b) must return zero when
        meaning_a == meaning_b; i.e., the nearest possible distance is 0.

    Returns:
    """
    self._F = F
    self._V = V
    self._values = range(self._V)
    self._distance = distance

  def get(self):
    return tuple(random.choice(self._values) for _ in xrange(self.F))

  @property
  def F(self):
    return self._F

  @property
  def V(self):
    return self._V

  @property
  def distance(self, meaning_a, meaning_b):
    """Re-raise the exception if document(meaning_a, meaning_b) is not possible.
    
    This docstring is invisible because it's for a property!

    Arguments:
      meaning_a: The first meaning to be compared.
      meaning_b: The second meaning to be compared.

    Raises:
      TypeError if the distance function cannot be called appropriately.
    """
    return self._distance(meaning_a, meaning_b)


class SignalSpace(object):
  """Representation of signal space, the set of all possible signals.

  A signal space is defined as a set of sequences of minimal units (e.g. words
  or phonemes in the case the signal is an acoustic utterance). The alphabet is
  the set of values these units can take one. The length is the length of each
  utterance in units.
  """

  def __init__(self, alphabet, length, distance):
    self._alphabet = frozenset(alphabet)

    # Length of signals.
    #
    # TODO: Decide on an elegant way to modify g() so as to account for signals
    # of varying lengths.
    self._length = length
    self._size = (len(self.alphabet) + 1) ** self.length - 1

  @property
  def length(self):
    return self._length

  @property
  def size(self):
    return self._size

  def get(self):
    return tuple(
        random.choice(self._alphabet)
        for _ in xrange(self._min_length, self._max_length))

  @property
  def alphabet(self):
    return self._alphabet

  @property
  def distance(self, signal_a, signal_b):
    """Re-raise the exception if document(signal_a, signal_b) is not possible.
    
    This docstring is invisible because it's for a property!

    Arguments:
      signal_a: The first signal to be compared.
      signal_b: The second signal to be compared.

    Raises:
      TypeError if the distance function cannot be called appropriately.
    """
    return self._distance(signal_a, signal_b)


class Environment(object):
  """Contains the objects in the meaning space.

  Encapsulates the "environment" in which learning is modeled to occur. This
  includes objects manifest in the world--the meanings whose feature vectors are
  available to be observed/mentioned by Interlocutors--but also, somehow, the
  signal and meaning spaces with their symbol tables. A mapping between words
  and the learning faculties of sentient beings inheres the world.

  Arguments:
    signal_space: a SignalSpace
    meaning_space:
      a MeaningSpace (parameters constraining what objects can exist)
    manifest_reality: objects which do, in fact, exist
  """

  def __init__(self, signal_space, meaning_space, manifest_reality):
    if not meaning_space.can_engender(manifest_reality):
      raise ValueError(
          'manifest_reality is incompatible with meaning_space (check '
          'MeaningSpace.(F|V)).')
    self._signal_space = signal_space
    self._meaning_space = meaning_space
    self._reality = manifest_reality

  @property
  def signal_space(self):
    return self._signal_space

  @property
  def meaning_space(self):
    return self._meaning_space

  @property
  def reality(self):
    return self._reality
