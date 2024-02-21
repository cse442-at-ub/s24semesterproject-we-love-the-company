import unittest

import os
import sys

# python is such a well designed language
sys.path.append(os.getcwd() + "/src/game")

import gamestate

import splash

class SplashTests(unittest.TestCase):
    def setUp(self):
        self.state = gamestate.Gamestate((1, 1), splash.SplashScene())

    def getId(self):
        return self.state.scene.id
    
    def test_splash_init(self):
        self.assertEqual(self.getId(), splash.ID)
        self.assertEqual(self.state.scene.timer, 0)
        self.assertIn(self.getId(), self.state.handlers)

    def test_splash_render(self):
        # the test here is to ensure no errors are raised
        # since compile errors are not real
        self.state.render()

    def test_splash_update(self):
        self.state.update(0.1)
        self.assertEqual(self.state.scene.timer, 0.1)

        self.state.update(0.1)
        self.assertEqual(self.state.scene.timer, 0.2)

    def test_splash_nonHandlers(self):
        self.assertEqual(self.state.handlers[self.getId()].onKeyPress, gamestate.doNothing)
        self.assertEqual(self.state.handlers[self.getId()].onMouseMove, gamestate.doNothing)
        self.assertEqual(self.state.handlers[self.getId()].onMousePress, gamestate.doNothing)