class SymbolTable(object):
  """One-to-one mapping of integers to arbitrary hashable objects."""

  def __init__(self, *args, **kwargs):
    self._label_to_index = {}
    self._index_to_label = []

  def __len__(self):
    return len(self._label_to_index)

  def __contains__(self, label):
    return label in self._label_to_index

  def add(self, label):
    if label not in self:
      self._index_to_label.append(label)
      self._label_to_index[label] = len(self._label_to_index)
      return True
    return False

  def get_label(self, index):
    """Gets label corresponding to an index.

    Raises:
      IndexError if index is out of bounds, i.e. if ! (0 <= index < len(self)).
    """
    return self._index_to_label[index]

  def get_index(self, label):
    """Gets index corresponding to a label.

    Raises:
      KeyError if label is not in internal dictionary.
    """
    return self._label_to_index[label]
