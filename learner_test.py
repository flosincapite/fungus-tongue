#!/usr/bin/python

import contextlib
import mock
import unittest

import learner


class LearningStateTest(unittest.TestCase):

  def testInit(self):
    state = learner.LearningState(generation=5, individuals=['ubiety'])
    self.assertEquals(5, state._generation)
    self.assertEquals(['ubiety'], state._individuals)

  def testGetGeneration(self):
    state = learner.LearningState()

    # Forcibly set the private member to keep the test hermetic.
    state._generation = 30
    self.assertEquals(30, state.generation)

  def testGetIndividuals(self):
    state = learner.LearningState()

    # Forcibly set the private member to keep the test hermetic.
    state._individuals = ['nihility']
    self.assertEquals(['nihility'], state.individuals)

  def testSetGeneration(self):
    state = learner.LearningState()
    state.generation = 30

    # Check the private member to keep the test hermetic.
    self.assertEquals(30, state._generation)

  def testSetIndividuals(self):
    state = learner.LearningState()
    state.individuals = ['nihility']

    # Check the private member to keep the test hermetic.
    self.assertEquals(['nihility'], state._individuals)


class _FakeState(object):
  """Simple fake implementation of LearningState."""

  def __init__(self, *unused_args, **unused_kwargs):
    self.generation = 0

  def __eq__(self, other):
    if isinstance(other, type(self)):
      return True
    return NotImplemented


@mock.patch.object(learner, 'LearningState', new=_FakeState)
class LearnerTest(unittest.TestCase):

  def setUp(self):

    def _wilt_function(iterations):
      wilt_state = {'iterations': iterations}
      def _wilt(*unused_args, **unused_kwargs):
        wilt_state['iterations'] -= 1
        return wilt_state['iterations'] < 0
      return _wilt

    @contextlib.contextmanager
    def _mock_context(unused_state):
      yield

    self._seed_mock = mock.create_autospec(lambda: None)
    self._wilt = _wilt_function(5)
    self._reproduce_mock = mock.create_autospec(lambda unused_state: None)
      
    self._learner = learner.Learner(
        seed=self._seed_mock,
        wilt=self._wilt,
        reproduce=self._reproduce_mock)

  def testEpoch(self):
    self._learner.epoch(3)

    # TODO: This test can be more precise, checking that the _FakeState's
    # generation member was correct at the time it was called. Hard to do that
    # since mock_calls just gets a shallow copy.
    self.assertItemsEqual(
        [
          mock.call(_FakeState()),
          mock.call(_FakeState()),
          mock.call(_FakeState())],
        self._reproduce_mock.mock_calls)

  def testChatter(self):
    self._learner.chatter()

    # Five calls because self._wilt terminates after five iterations.
    #
    # TODO: This test can be more precise, checking that the _FakeState's
    # generation member was correct at the time it was called. Hard to do that
    # since mock_calls just gets a shallow copy.
    self.assertItemsEqual(
        [
          mock.call(_FakeState()),
          mock.call(_FakeState()),
          mock.call(_FakeState()),
          mock.call(_FakeState()),
          mock.call(_FakeState())],
        self._reproduce_mock.mock_calls)


if __name__ == '__main__':
  unittest.main()
