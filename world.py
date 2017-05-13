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

  def __init__(self, alphabet, max_length):
    self._alphabet = frozenset(alphabet)
    self._max_length = max_length
    self._min_length = 1

  def get(self):
    return tuple(
        random.choice(self._alphabet)
        for _ in xrange(self._min_length, self._max_length))

  @property
  def alphabet(self):
    return self._alphabet

  @classmethod
  def distance(self, signal_a, signal_b):
    return NotImplemented