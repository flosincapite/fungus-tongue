class SymbolTable(dict):

  def __init__(self, *args, **kwargs):
    self._index_to_label = []
    super(SymbolTable, self).__init__(*args, **kwargs)

  def add(self, label):
    if label in self:
      return
    self[label] = len(self)
    self._index_to_label.append(label)

  def get_label(self, index):
    """Gets label corresponding to an index.

    Raises:
      IndexError if index is out of bounds, i.e. if ! (0 <= index < len(self)).
    """
    return self._index_to_label[index]
