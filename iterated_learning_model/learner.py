import collections
import contextlib
import logging


class InimitableNames(type):
  """TODO: Implement.
  
  Basically, the idea is to solve the "automatically set an underscore-prefixed
  version of an arbitrary kwarg with a default value" problem while also raising
  an exception if two classes in the hierarchy try to use the same variable name
  (variable names can't override each other--partitioning scheme).
  """

  def __something__bizarre_(self, **kwargs):
    for name, default in kwargs.iteritems():
      assert not name.startswith('_')
      new_name = '_' + name
      assert not self.__hasattr__(new_name)
      reserved_variable_names = {'_number_generations'}
      for var_name in reserved_variable_names:
        if hasattr(self, var_name):
          raise ValueError('Subclass has overwriten member "%s"' % var_name)
      # Hmm. Keep thinking. This should become a property.
      # Plus this code doesn't do anything, so TODO: implement.


# TODO: The problem with this pattern is that callers silently ignore some
# fields if this tuple changes. Maybe that's not a big deal? Subclassing
# namedtuple might help.
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
  __metaclass__ = InimitableNames
  
  def __init__(self, seed=None, wilt=None, reproduce=None):
    self._seed = seed
    self._wilt = wilt
    self._reproduce = reproduce
    self._state = None

  @property
  def state(self):
    return self._state

  @state.setter
  def state(self, value):
    self._state = value

  def chatter(self, state=None):
    self._state = LearningState(generation=0, individuals=self._seed())
    while not self._wilt(self._state):
      self.step()

  def step(self, n=1):
    assert 0 <= n
    for _ in xrange(n):
      self._step()

  def _step(self):
    self._state.individuals = self._reproduce(self.state.individuals)
    self._state.generation += 1


def loggable(log_function):
  def decorator(original_function):
    def result_function(*args, **kwargs):
      log_function()
      return original_function(*args, **kwargs)
    return result_function
  return decorator


class LoggingLearner(Learner):

  def _should_log(self):
    return NotImplemented

  def log(self):
    return NotImplemented
  
  def _step(self):
    if self._should_log():
      self.log()
    super(LoggingLearner, self)._step()


@contextlib.contextmanager
def pause_context():
  yield
  _ = raw_input()


@contextlib.contextmanager
def surreal():
  yield


class LogIndividualsByGeneration(LoggingLearner):

  def __init__(self, log_after=5, log_context=surreal, *args, **kwargs):
    super(LogIndividualsByGeneration, self).__init__(*args, **kwargs)
    self._log_after_n_generations = log_after
    self._log_context = pause_context

  def _should_log(self):
    return (self._state.generation % self._log_after_n_generations) == 0

  def log(self):
    with self._log_context():
      for individual in self._state.individuals:
        logging.info(repr(individual.active_matrix))
        logging.info(repr(individual.passive_matrix))
      logging.info(repr(self._state.generation))
