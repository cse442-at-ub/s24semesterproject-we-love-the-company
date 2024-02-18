import pygame

import gamestate
import util

ID = "splash"

SPLASH_TIME = 2

# scene's state
class SplashScene:
    def __init__(self):
        self.id = ID
        self.timer = 0

    def initHandlers(self, state: gamestate.Gamestate):
        state.handlers[ID] = gamestate.Handler(render, update)

def render(state: gamestate.Gamestate):
    # grow a rect (sprite) over some time period
    scale = util.lerp(0.33, 1.0, (state.scene.timer / SPLASH_TIME))

    # center it
    wh = (state.screenSize[0] * scale, state.screenSize[1] * scale)
    xy = ((state.screenSize[0] - wh[0]) / 2, (state.screenSize[1] - wh[1]) / 2)

    # draw it
    pygame.draw.rect(state.screen, (200, 10, 10), pygame.Rect(xy[0], xy[1], wh[0], wh[1]))

import menu

def update(state: gamestate.Gamestate, deltaT):
    state.scene.timer += deltaT

    if (state.scene.timer > SPLASH_TIME):
        # mainMenu has an infinite loop yay!
        menu.mainMenu()
        # we have to exit early or we crash instead
        # quitting is more graceful than crashing
        pygame.quit()
        quit() 
        # @TODO uncomment once main menu exists
        #state.setScene(mainMenuScene())
        state.scene.timer = 0

