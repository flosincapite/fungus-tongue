import fire
import logging
import numpy

from projects.language_games.compositional_model import helpers
from projects.language_games.compositional_model import learner
from projects.language_games.compositional_model import model
from projects.language_games.compositional_model import pullulate
from projects.language_games.compositional_model import seeds
from projects.language_games.compositional_model import wilts


class GenerateFire(object):

  def run_generations(
      self, individuals, signals, meanings, k, terminal, pause=False):
    exec('terminal_condition = wilts.terminate_%s' % terminal)
    keyword_args = {
        'seed': seeds.CapriciousDemiurge(individuals, signals, meanings),
        'wilt': terminal_condition,
        'reproduce': pullulate.ParentalStrategy(
          pullulate.asexual_reproduction(
            k, model.NormalizedModel.from_association_matrix),
          pullulate.total_payoff),
        'log_after': 50,
    }
    if pause:
      keyword_args['log_context'] = learner.pause_context
    good_learner = learner.LogIndividualsByGeneration(**keyword_args)
    good_learner.chatter()
    final_individuals = good_learner.state.individuals
    for individual in final_individuals:
      logging.info(individual.active_matrix)
      logging.info(individual.passive_matrix)
      logging.info('')


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  fire.Fire(GenerateFire)
