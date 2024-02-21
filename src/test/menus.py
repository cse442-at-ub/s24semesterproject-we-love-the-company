import unittest

import os
import sys

# python is such a well designed language
sys.path.append(os.getcwd() + "/src/game")

import gamestate

import splash
import menu
import OptionsMenu
import HowToPlay

class SplashTests(unittest.TestCase):
    def setUp(self):
        self.state = gamestate.Gamestate((1280, 720), splash.SplashScene())

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


class MainMenuTests(unittest.TestCase):
    def setUp(self):
        self.state = gamestate.Gamestate((1280, 720), splash.SplashScene())
        self.state.update(splash.SPLASH_TIME * 2)

    def getId(self):
        return self.state.scene.id

    def test_menu_init(self):
        self.assertEqual(self.getId(), menu.ID)

    def test_menu_mouse_move(self):
        for button in self.state.scene.buttons:
            # tests via proxy, so not that accurate
            old = button.text
            self.state.moveMouse((button.x_pos, button.y_pos), (0, 0), (1, 0, 0), False)
            self.assertNotEqual(button.text, old)

    def test_menu_mouse_press(self):
        self.assertTrue(self.state.running)

        # simulate pressing the ExitButton
        self.state.pressMouse((self.state.scene.ExitButton.x_pos, self.state.scene.ExitButton.y_pos), 1, False)
        self.assertFalse(self.state.running)

        self.state.pressMouse((self.state.scene.SettingsButton.x_pos, self.state.scene.SettingsButton.y_pos), 1, False)
        self.assertNotEqual(self.getId(), menu.ID)
        self.state.popScene()

        self.state.pressMouse((self.state.scene.InstructionsButton.x_pos, self.state.scene.InstructionsButton.y_pos), 1, False)
        self.assertNotEqual(self.getId(), menu.ID)
        self.state.popScene()

    def test_menu_render(self):
        self.state.render()

    def test_menu_nonHandlers(self):
        self.assertEqual(self.state.handlers[self.getId()].onKeyPress, gamestate.doNothing)
        self.assertEqual(self.state.handlers[self.getId()].onUpdate, gamestate.doNothing)

class SettingsTests(unittest.TestCase):
    def setUp(self):
        self.state = gamestate.Gamestate((1280, 720), splash.SplashScene())
        self.state.pushScene(OptionsMenu.SettingsScene(self.state.screen))

    def getId(self):
        return self.state.scene.id

    def test_settings_init(self):
        self.assertEqual(self.getId(), OptionsMenu.ID)

    def test_settings_mouse_move(self):
        for button in self.state.scene.buttons:
            # tests via proxy, so not that accurate
            old = button.text
            self.state.moveMouse((button.x_pos, button.y_pos), (0, 0), (1, 0, 0), False)
            self.assertNotEqual(button.text, old)

    def test_settings_mouse_press(self):
        

        # simulate pressing the BackButton [do this last!]
        self.state.pressMouse((self.state.scene.BackButton.x_pos, self.state.scene.BackButton.y_pos), 1, False)
        self.assertNotEqual(self.getId(), OptionsMenu.ID)

    def test_settings_render(self):
        self.state.render()

    def test_settings_nonHandlers(self):
        self.assertEqual(self.state.handlers[self.getId()].onKeyPress, gamestate.doNothing)
        self.assertEqual(self.state.handlers[self.getId()].onUpdate, gamestate.doNothing)


class HowToPlayTests(unittest.TestCase):
    def setUp(self):
        self.state = gamestate.Gamestate((1280, 720), splash.SplashScene())
        self.state.pushScene(HowToPlay.InstructionsScene(self.state.screen))

    def getId(self):
        return self.state.scene.id

    def test_instructions_init(self):
        self.assertEqual(self.getId(), HowToPlay.ID)

    def test_instructions_mouse_move(self):
        button = self.state.scene.BackButton
        old = button.text
        self.state.moveMouse((button.x_pos, button.y_pos), (0, 0), (1, 0, 0), False)
        self.assertNotEqual(button.text, old)

    def test_instructions_mouse_press(self):
        # simulate pressing the BackButton [do this last!]
        self.state.pressMouse((self.state.scene.BackButton.x_pos, self.state.scene.BackButton.y_pos), 1, False)
        self.assertNotEqual(self.getId(), HowToPlay.ID)

    def test_instructions_render(self):
        self.state.render()

    def test_instructions_nonHandlers(self):
        self.assertEqual(self.state.handlers[self.getId()].onKeyPress, gamestate.doNothing)
        self.assertEqual(self.state.handlers[self.getId()].onUpdate, gamestate.doNothing)
