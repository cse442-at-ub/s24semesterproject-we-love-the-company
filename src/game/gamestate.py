import pygame


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
        #should make the screen resizable
        self.screen = pygame.display.set_mode(screenSize, pygame.RESIZABLE)
        self._scenes = [initScene]
        initScene.initHandlers(self)
        
        self.clock = pygame.time.Clock()
        self.running = True
    
    @property
    def scene(self):
        return self._scenes[-1]

    def pushScene(self, scene):
        self._scenes.append(scene)
        scene.initHandlers(self)

    def popScene(self):
        self._scenes.pop()


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
    
    def update_scene_elements(self, width: int, height: int):
        for scene in self._scenes:
            scene.update_elements(width, height)
    
    def handle_resize(self, width: int, height: int):
        self.screenSize = (width, height)
        self.screen = pygame.display.set_mode(self.screenSize, pygame.RESIZABLE)
        self.update_scene_elements(width, height)