import pygame


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
        self.scene = initScene
        self.timer = 0
        
        self.clock = pygame.time.Clock()
        self.running = True
    
    def update(self, deltaT):
        self.timer += deltaT
        self.handlers[self.scene.id].onUpdate(self, deltaT)

    def render(self):
        self.handlers[self.scene.id].onRender(self)

    def moveMouse(self, pos, rel, buttons, touch):
        self.handlers[self.scene.id].onMouseMove(self, pos, rel, buttons, touch)

    def pressMouse(self, pos, buttons, touch):
        self.handlers[self.scene.id].onMouseMove(self, pos, buttons, touch)

    def pressKey(self, key, mod, unicode, scancode):
        self.handlers[self.scene.id].onKeyPress(self, key, mod, unicode, scancode)