"""Contexts within which Learners advance one epoch forward."""

import contextlib
import logging


def get_query_context(log_after):

  @contextlib.contextmanager
  def query_context(state):
    yield
    
    if not state.generation % log_after:
      while True:
        query = raw_input('Enter query: ').lower().strip()
        if query in {'go on', 'get', 'quit', 'q', ''}:
          break
        elif hasattr(state, query):
          log_message = '\n' + repr(getattr(state, query))
        else:
          log_message = 'state does not have an attribute <%s>' % query
        logging.info(log_message)

  return query_context


@contextlib.contextmanager
def void_context(unused_state):
  yield
