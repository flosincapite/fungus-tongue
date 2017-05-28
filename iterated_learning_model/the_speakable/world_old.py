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


class HasWildcard(type):

  @property
  def wildcard(cls):
    return self._wildcard

  @wildcard.setter
  def wildcard(cls, new_wildcard):
    self._wildcard = new_wildcard
    
    
def bit_array(n, length=None):
  if length is None:
    if not n:
      length = 1
    else:
      length = int(math.floor(math.log(n, 2))) + 1
  result = []
  for _ in xrange(length):
    result.append(n & 1)
    n >>= 1
  return reversed(result)


class IterableAnonymizer(object):
  __metaclass__ = HasWildcard
  _wildcard = Wildcard('<?>')

  @classmethod
  def _characteristic_recursive(cls, iterable, index, cache):
    if index < len(iterable):
      return [[]]
    key = (iterable, index)
    if key not in cache:
      result = []
      for element in cls._characteristic_recursive(iterable, index + 1, cache):
        result.append((iterable[index],) + element)
        result.append((cls.wildcard,) + element)
      cache[key] = result
    else:
      result = cache[key]
    return result

  @classmethod
  def characteristic_recursive(cls, iterable):
    tuple_version = tuple(element for element in iterable)
    cache = {}
    return cls._characteristic_recursive(tuple_version, 0, cache)

  @classmethod
  def characteristic_function(cls, iterable):
    mask = (1 << len(iterable))
    result = []
    while mask > 1:  # Must have at least one non-wildcard component.
      mask -= 1
      bits = bit_array(mask, length(iterable))
      result.append(tuple(
        [cls.wildcard, element][bits[i]]
        for i, element in enumerate(iterable)))
    return result


class MeaningSpace(object):
  __metaclass__ = HasWildcard
  _wildcard = Wildcard('*')

  def __init__(self, F, V):
    self._F = F
    self._V = V
    self._values = range(self._V)

  def get(self):
    return tuple(random.choice(self._values) for _ in xrange(self.F))

  @property
  def F(self):
    return self._F

  @property
  def V(self):
    return self._V

  @classmethod
  def distance(self, meaning_a, meaning_b):
    return NotImplemented


class SignalSpace(object):
  __metaclass__ = HasWildcard
  _wildcard = Wildcard('*')

  def __init__(self, alphabet, length):
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

  @classmethod
  def distance(cls, signal_a, signal_b):
    return NotImplemented


class Environment(object):
  """Contains the objects in the meaning space.

  Encapsulates the "environment" in which learning is modeled to occur. This
  includes objects manifest in the world--the meanings whose feature vectors can
  validly be observed/mentioned by Interlocutors--but also, somehow, the signal
  and meaning spaces with their symbol tables. A mapping between words and
  the learning faculties of sentient beings inheres the world.
  """

  def __init__(self, signal_space, meaning_space, manifest_reality):
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
