import pygame
import os
from Buttons import Button

# taken from: https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame
def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

class Instructions:
    def __init__(self, window, clock, path, textFont, paragraphFont):
        self.window = window
        self.clock = clock
        self.path = path
        self.textFont = textFont
        self.paragraphFont = paragraphFont

    #For this i followed what we had in menu.py 
    #using the button class complete and following the whole layout like the menu.py
    #for now the audio and video buttons dont do anything
    #and the back(exit button takes back to the menu page)
    def display_instructions_menu(self):
        pygame.display.set_caption("We love the Company | How to Play")
        run = True
        instructions_window = pygame.display.set_mode((1024, 720))
        instructions_file = open("how-to-play-text.txt")
        instructions_text = instructions_file.read()
        instructions_file.close()
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

            blit_text(instructions_window,instructions_text,(0,0),self.paragraphFont)

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
                        print("back button pressed")


            pygame.display.flip()  # Update the display