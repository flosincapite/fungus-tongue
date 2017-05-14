import fire
import logging

from basic_model.learning import revelations
import learner
from util import epoch_contexts


class GenerateFire(object):

  def basic_model(
      self, individuals, signals, meanings, k, terminal, monitor=None):
    exec('terminal_condition = revelations.terminate_%s' % terminal)

    keyword_args = {
        'seed': revelations.initialize(individuals, signals, meanings),
        'reproduce': revelations.parental_learning(k),
        'wilt': terminal_condition,
    }
    if monitor is not None:
      exec('monitor = epoch_contexts.get_%s' % monitor)
      keyword_args['epoch_context'] = monitor

    self._run(learner.Learner(**keyword_args))

  def _run(self, the_learner):
    the_learner.chatter()
    final_individuals = the_learner.state.individuals
    for individual in final_individuals:
      logging.info('\n' + repr(individual.active_matrix))
      logging.info('\n' + repr(individual.passive_matrix))
      logging.info('')


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  fire.Fire(GenerateFire)
