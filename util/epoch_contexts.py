"""Contexts within which Learners advance one epoch forward."""

import contextlib
import logging


def get_query_context(log_after, log=logging.info, get_input=raw_input):
  """Creates a context manager that allows LearningState to be queried.
  
  If the input matches the name of a member of the LearningState, that member
  will be logged. A closed set of queries will allow execution to continue.

  TODO: Why am I dependency-injecting log but not raw_input? The tests are
  really weird. Maybe just use classes instead of function factories.
  """

  @contextlib.contextmanager
  def query_context(state):
    yield
    
    if not state.generation % log_after:
      while True:
        query = get_input('Enter query: ').strip()
        if query.lower() in {'go on', 'get', 'quit', 'q', ''}:
          break
        elif hasattr(state, query):
          log_message = '\n' + repr(getattr(state, query))
        else:
          log_message = 'state does not have an attribute <%s>' % query
        log(log_message)

  return query_context


def get_void_context():
  """Creates a do-nothing, lazy context manager."""

  @contextlib.contextmanager
  def void_context(unused_state):
    yield

  return void_context
