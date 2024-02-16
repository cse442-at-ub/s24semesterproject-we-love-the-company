import pygame
import os
from Buttons import Button

class Instructions:
    def __init__(self, window, clock, path, textFont):
        self.window = window
        self.clock = clock
        self.path = path
        self.textFont = textFont

    #For this i followed what we had in menu.py 
    #using the button class complete and following the whole layout like the menu.py
    #for now the audio and video buttons dont do anything
    #and the back(exit button takes back to the menu page)
    def display_instructions_menu(self):
        pygame.display.set_caption("We love the Company | How to Play")
        run = True
        instructions_window = pygame.display.set_mode((1024, 720))
        while run: 
            #this is kinda copied from the menu.py (i assume it just makes the screen)
            window_size = instructions_window.get_size()
            self.clock.tick(27)  # Control framerates
            instructions_window.fill((0, 0, 0))
            background_image = pygame.image.load(os.path.join(self.path + 'background.jpg'))
            background_image = pygame.transform.scale(background_image, window_size)
            instructions_window.blit(background_image, (0, 0))

            menuMousePOS = pygame.mouse.get_pos()

            screen_center_x = instructions_window.get_width() // 2
            back_button_y = instructions_window.get_height() - 50

            BackButton = Button(image=pygame.image.load(self.path + "Assets/button.png"), pos=(screen_center_x, back_button_y),
                            text_input="Back", font=self.textFont, base_color="white", hovering_color="blue")

            for button in [BackButton]:
                button.changeColor(menuMousePOS)
                button.update(instructions_window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if BackButton.checkForInput(menuMousePOS):
                        run = False
                        print("exit button pressed")


            pygame.display.flip()  # Update the display