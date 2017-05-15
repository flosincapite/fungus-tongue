from util import epoch_contexts


# TODO: Maybe just use a namedtuple (ugly idea: metaclass that automatically
# creates properties and _corresponding_private_members).
class LearningState(object):

  def __init__(self, generation=0, individuals=None):
    if individuals is None:
      individuals = []
    self._generation = generation
    self._individuals = individuals

  @property
  def generation(self):
    return self._generation

  @generation.setter
  def generation(self, value):
    self._generation = value

  @property
  def individuals(self):
    return self._individuals

  @individuals.setter
  def individuals(self, value):
    self._individuals = value


class Learner(object):
  
  def __init__(
      self, seed=None, wilt=None, reproduce=None,
      epoch_context=epoch_contexts.get_void_context()):
    self._seed = seed
    self._wilt = wilt
    self._reproduce = reproduce
    self._state = None
    self._epoch_context = epoch_context

  @property
  def state(self):
    if self._state is None:
      self._state = LearningState(generation=0, individuals=self._seed())
    return self._state

  def chatter(self):
    while not self._wilt(self.state):
      self.epoch()

  def epoch(self, n=1):
    assert 0 <= n
    for _ in xrange(n):
      self._epoch()

  def _epoch(self):
    with self._epoch_context(self.state):
      self._state.individuals = self._reproduce(self.state)
      self._state.generation += 1
