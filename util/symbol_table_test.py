#!/usr/bin/python

import unittest

from util import symbol_table


# TODO: Lots of interdependency here--maybe refactor.
class SymbolTableTest(unittest.TestCase):

  def setUp(self):
    self._table = symbol_table.SymbolTable()

  def testContains(self):
    self.assertNotIn('saprotrophy', self._table)

    # Ensure that the value is added.
    _ = self._table.add('saprotrophy')
    self.assertIn('saprotrophy', self._table)

  def testLength(self):
    self.assertEquals(0, len(self._table))

    # Ensure that the value is added.
    _ = self._table.add('saprotrophy')
    self.assertEquals(1, len(self._table))

  def testAdd(self):
    # Preconditions.
    self.assertNotIn('ganoderma', self._table)

    # Test return values.
    self.assertTrue(self._table.add('ganoderma'))
    self.assertFalse(self._table.add('ganoderma'))

    # Postconditions.
    self.assertIn('ganoderma', self._table)

  def testGetLabel(self):
    self.assertEquals(0, len(self._table))  # Precondition.
    _ = self._table.add('ekphrasis')
    self.assertEquals('ekphrasis', self._table.get_label(0))

  def testGetLabelRaisesIndexError(self):
    self.assertEquals(0, len(self._table))  # Precondition.
    with self.assertRaises(IndexError):
      _ = self._table.get_label(0)

  def testGetIndex(self):
    self.assertEquals(0, len(self._table))  # Precondition.
    _ = self._table.add('ekphrasis')
    self.assertEquals(0, self._table.get_index('ekphrasis'))

  def testGetIndexRaisesIndexError(self):
    self.assertEquals(0, len(self._table))  # Precondition.
    with self.assertRaises(KeyError):
      _ = self._table.get_index('patulous')
