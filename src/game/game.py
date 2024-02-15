import pygame
import menu 

from gamestate import Gamestate

from splash import SplashScene

def gameloop(gamestate: Gamestate):
    
    gamestate.screen.fill((10, 13, 15))

    gamestate.render()

    pygame.display.flip()

    dt = min(gamestate.clock.tick(60) / 1000, 0.1)
    gamestate.update(dt)

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            gamestate.running = False
            return
        elif (event.type == pygame.KEYDOWN):
            gamestate.pressKey(event.key, event.mod, event.unicode, event.scancode)
        elif (event.type == pygame.MOUSEMOTION):
            gamestate.moveMouse(event.pos, event.rel, event.buttons, event.touch)
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            gamestate.pressMouse(event.pos, event.button, event.touch)

def main():
    state = Gamestate((1280, 720), SplashScene())
    pygame.display.set_caption("We Love The Company.")

    while state.running:
        gameloop(state)

if __name__ == "__main__":
    pygame.init()
    
    main()

    pygame.quit()