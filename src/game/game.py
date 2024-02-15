import pygame
import menu 


def handleMouseMove(pos, rel, buttons, touch):
    pass

def handleMousePress(pos, button, touch):
    pass

def gameloop(screen):
    
    screen.fill((10, 13, 15))

    # Put rendering code here

    pygame.display.flip()

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            return False
        elif (event.type == pygame.MOUSEMOTION):
            handleMouseMove(event.pos, event.rel, event.buttons, event.touch)
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            handleMousePress(event.pos, event.button, event.touch)

    return True

def main():
    
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("We Love The Company.")

    while gameloop(screen):
        menu.mainMenu()
        pass


if __name__ == "__main__":
    pygame.init()
    
    main()
    
    



    pygame.quit()

