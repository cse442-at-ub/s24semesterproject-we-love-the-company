import pygame

from gamestate import Gamestate

from splash import SplashScene

pygame.mixer.init() 
audio_pack = pygame.mixer.music.load("src/game/Assets/Background_music_menu.wav")
audio_control = pygame.mixer.music.play(-1)
button_sound_que = pygame.mixer.Sound("src/game/Assets/button_click.mp3")
pygame.mixer.music.set_volume(0.2)

def gameloop(gamestate: Gamestate):
    
    # clear
    gamestate.screen.fill((10, 13, 15))

    # render scene
    gamestate.render()

    # show to screen
    pygame.display.flip()

    # get delta time (in seconds)
    dt = min(gamestate.clock.tick(60) / 1000, 0.1)

    # update scene state
    gamestate.update(dt)

    # handle events
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
        #allows to make the window resizable
        elif (event.type == pygame.VIDEORESIZE):
            gamestate.handle_resize(event.w, event.h)

def main():
    # initialize the game to the splash screen
    state = Gamestate((1280, 720), SplashScene())

    # set the window title
    pygame.display.set_caption("We Love The Company.")

    # main loop
    while state.running:
        gameloop(state)

# entry
if __name__ == "__main__":
    pygame.init()
    
    # entry function
    main()

    pygame.quit()