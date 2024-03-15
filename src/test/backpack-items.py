import unittest
import os,sys
# python is such a well designed language
sys.path.append(os.getcwd() + "/src/game")

from backpack import Backpack
from item import *

class TestItemBackpackIntegration(unittest.TestCase):
    def setUp(self):
        # Initialize the item library with items
        self.item_library = Items()  # Assuming this class is defined somewhere to hold the items
        self.sword = Sword()
        self.shield = Shield()
        self.potion = Potion()
        self.boots = Boots()

        # Initialize the backpack
        self.backpack = Backpack(10)

    def test_add_items_to_backpack(self):
        # Add item objects to backpack, not their identifiers
        self.backpack.add(self.sword.identifier)
        self.backpack.add(self.shield.identifier)
        self.backpack.add(self.potion.identifier)
        self.backpack.add(self.boots.identifier)
        
        # Adding some items more than once
        self.backpack.add(self.potion.identifier)
        self.backpack.add(self.shield.identifier)

        # Expected result
        expected = {
            self.sword.identifier: 1,
            self.shield.identifier: 2,  # Added twice
            self.potion.identifier: 2,  # Added twice
            self.boots.identifier: 1
        }

        # Verify the backpack contents
        self.assertEqual(self.backpack.items, expected)
    
    def test_backpack_full(self):
        """Test adding items beyond the backpack's capacity."""
        for _ in range(10):
            self.backpack.add(Sword().identifier)
        with self.assertRaises(Exception):
            self.backpack.add(Sword().identifier)  # Adding one more should raise an exception.

    def test_backpack_remove_item(self):
        """Test removing an item from the backpack."""
        self.backpack.add(self.sword.identifier)
        self.backpack.remove(self.sword.identifier)  # Assuming a remove method is implemented.
        self.assertTrue(self.backpack.isEmpty())

    def test_adding_different_items(self):
        """Test adding different types of items to the backpack."""
        self.backpack.add(self.sword.identifier)
        self.backpack.add(Arrow().identifier)  # Adding a different item.
        expected = {
            self.sword.identifier: 1,
            "arrow": 1
        }
        self.assertEqual(self.backpack.items, expected)

    def test_backpack_is_not_full_after_addition(self):
        """Test that backpack reports not full after adding items below its capacity."""
        self.backpack.add(self.sword.identifier)
        self.assertFalse(self.backpack.isFull())
    
    def test_print_items(self):
        """Test the printItems method's behavior (this might need manual verification)."""
        self.backpack.add(self.sword.identifier)
        self.backpack.add(self.shield.identifier)
        self.backpack.printItems()  # Manual verification required to see if items print correctly.


if __name__ == '__main__':
    unittest.main()
