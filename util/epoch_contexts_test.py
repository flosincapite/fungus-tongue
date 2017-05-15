import mock
import unittest

from util import epoch_contexts


class _FakeRawInput(object):

  def __init__(self, inputs):
    self._i = 0
    self._inputs = inputs

  def __call__(self, *args, **kwargs):
    index = self._i % len(self._inputs)
    result = self._inputs[index]
    self._i += 1
    return result


class _FakeState(object):

  def __init__(self, generation, thing):
    self.generation = generation
    self.thing = thing


class EpochContextsTest(unittest.TestCase):

  def testGetQueryContext(self):
    mock_log = mock.Mock()
    fake_input = _FakeRawInput(['generation', 'thing', 'nothing', ''])
    manager = epoch_contexts.get_query_context(
        5, log=mock_log, get_input=fake_input)
    state = _FakeState(5, 'florid')
    with manager(state):
      pass

    # TODO: This could be better. Find a way to assert that mocks are called
    # with a string matching a regex.
    self.assertEquals(
        [mock.call('\n5'), mock.call('\n\'florid\''), mock.call(mock.ANY)],
        mock_log.call_args_list)

  def testGetQueryContextWrongGeneration(self):
    """Nothing should happen here."""
    # This context manager will only trigger on four-divisible generations.
    mock_log = mock.Mock()
    manager = epoch_contexts.get_query_context(4, log=mock_log)
    state = _FakeState(5, 'abstemious')
    with manager(state):
      pass
    mock_log.assert_not_called()

  def testGetVoidContext(self):
    """Nothing should happen here."""
    void = epoch_contexts.get_void_context()
    with void('no state here'):
      pass


if __name__ == '__main__':
  unittest.main()
