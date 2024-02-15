import pygame

import gamestate
import util

ID = "splash"

SPLASH_TIME = 2

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

def update(state: gamestate.Gamestate, deltaT):
    state.scene.timer += deltaT

    if (state.scene.timer > SPLASH_TIME):
        # @TODO uncomment once main menu exists
        #state.scene = "main_menu"
        state.timer = 0

