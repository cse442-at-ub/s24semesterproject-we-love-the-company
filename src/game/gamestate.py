import pygame

from item import *
from highscore import Highscores

# function for nothing
def doNothing(*args):
    pass

class Handler:
    # takes in a bunch of functions that handle events
    def __init__(self, onRender, onUpdate, onKeyPress = doNothing, onMouseMove = doNothing, onMousePress = doNothing):
        self.onRender = onRender
        self.onUpdate = onUpdate
        self.onKeyPress = onKeyPress
        self.onMouseMove = onMouseMove
        self.onMousePress = onMousePress


class Gamestate:
    # all the scene's handlers
    handlers: dict[str, Handler] = {}

    def __init__(self, screenSize, initScene):
        self.screenSize = screenSize
        self.screen = pygame.display.set_mode(screenSize)
        self._scenes = [initScene]
        initScene.initHandlers(self)
        
        self.clock = pygame.time.Clock()
        self.running = True

        self.items = Items()
        self.player_name = "BOB"
        self.scores = Highscores()
    
    @property
    def scene(self):
        return self._scenes[-1]

    def pushScene(self, scene):
        self._scenes.append(scene)
        scene.initHandlers(self)

    def popScene(self):
        self._scenes.pop()

    def switch_to_game(self):
        from grid_game import GameScene  # Assuming GameScene is defined in game_scene.py
        self.pushScene(GameScene(self.screen,"level1.json", self))

    def switch_to_menu(self):
        from menu import MenuScene  # Assuming MenuScene is defined in menu_scene.py
        self.popScene()
        self.pushScene(MenuScene(self.screen))
    ### Dispatch to handlers ###

    def update(self, deltaT):
        self.handlers[self.scene.id].onUpdate(self, deltaT)

    def render(self):
        self.handlers[self.scene.id].onRender(self)

    def pressKey(self, key, mod, unicode, scancode):
        self.handlers[self.scene.id].onKeyPress(self, key, mod, unicode, scancode)

    def moveMouse(self, pos, rel, buttons, touch):
        self.handlers[self.scene.id].onMouseMove(self, pos, rel, buttons, touch)

    def pressMouse(self, pos, button, touch):
        self.handlers[self.scene.id].onMousePress(self, pos, button, touch)
          