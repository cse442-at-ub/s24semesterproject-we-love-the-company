import unittest

import os
import sys

# python is such a well designed language
sys.path.append(os.getcwd() + "/src/game")

import grid

import player

COMMON = "common"
UNCOMMON = "uncommon"

class PlayerTests(unittest.TestCase):
    def setUp(self):
        self.grid = grid.Grid(5, 5)
        self.player = player.Player(self.grid,0,0,None)
        self.grid.insert({"item": COMMON}, 1, 0)
        self.grid.insert({"item": UNCOMMON}, 0, 2)

    def test_init(self):
        self.assertIsNone(self.player.heldItem)
        self.assertTrue(self.player.inventory.isEmpty())
        self.assertEqual(self.player.hitDie, "d4")
        self.assertEqual(self.player.position, (0, 0))

    def test_pickup(self):
        self.assertTrue(self.player.pickUp(1, 0))
        self.assertEqual(COMMON, self.player.heldItem)
        self.assertTrue(self.player.stash())
        self.assertIsNone(self.player.heldItem)
        self.assertFalse(self.player.inventory.isEmpty())
        self.assertIn(COMMON, self.player.inventory.dict)

    def test_retrieve(self):
        self.assertTrue(self.player.pickUp(1, 0))
        self.assertEqual(COMMON, self.player.heldItem)
        self.assertTrue(self.player.stash())
        self.assertIsNone(self.player.heldItem)
        self.assertTrue(self.player.retrieve(COMMON))
        self.assertEqual(COMMON, self.player.heldItem)
        self.assertFalse(self.player.retrieve(COMMON))
        self.assertFalse(self.player.retrieve(UNCOMMON))
        self.assertEqual(COMMON, self.player.heldItem)

    def test_out_of_range(self):
        self.assertFalse(self.player.pickUp(0, 2))
        self.assertIsNone(self.player.heldItem)

    def test_drop(self):
        self.assertTrue(self.player.pickUp(1, 0))
        self.assertEqual(COMMON, self.player.heldItem)
        self.assertTrue(self.player.drop())
        self.assertEqual({"item": COMMON}, self.grid.get_object(0, 1))

    def test_backpack_drop(self):
        self.assertTrue(self.player.pickUp(1, 0))
        self.assertEqual(COMMON, self.player.heldItem)
        self.assertTrue(self.player.stash())
        self.assertTrue(self.player.dropFromBackpack(COMMON))
        self.assertEqual({"item": COMMON}, self.grid.get_object(0, 1))

    def test_multiple_pickup(self):
        self.assertTrue(self.player.pickUp(1, 0))
        self.assertEqual(COMMON, self.player.heldItem)
        self.assertTrue(self.player.moveDown())
        self.assertEqual(self.player.position, (0, 1))
        self.assertFalse(self.player.pickUp(0, 2))
        self.assertTrue(self.player.stash())
        self.assertFalse(self.player.stash())
        self.assertTrue(self.player.pickUp(0, 2))
        self.assertTrue(self.player.stash())
        self.assertIsNone(self.player.heldItem)
        self.assertIn(COMMON, self.player.inventory.dict)
        self.assertIn(UNCOMMON, self.player.inventory.dict)

    def test_movement(self):
        self.assertFalse(self.player.moveLeft())
        self.assertEqual(self.player.position, (0, 0))
        self.assertTrue(self.player.moveRight())
        self.assertEqual(self.player.position, (1, 0))
        self.assertTrue(self.player.moveDown())
        self.assertEqual(self.player.position, (1, 1))
        self.assertTrue(self.player.moveUp())
        self.assertEqual(self.player.position, (1, 0))
        self.assertTrue(self.player.moveLeft())
        self.assertEqual(self.player.position, (0, 0))

    def test_loss(self):
        self.assertEqual("defeated", self.player.getHit())
        self.assertEqual("d4", self.player.hitDie)

    def test_win(self):
        for _ in range(10):
            self.player.increaseDie()

        self.assertEqual("d20", self.player.hitDie)
        self.assertEqual("d12", self.player.getHit())
        self.assertEqual("d12", self.player.hitDie)
