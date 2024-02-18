import pygame
import os
from Buttons import Button


class Settings:
    def __init__(self, window, clock, path, textFont):
        self.window = window
        self.clock = clock
        self.path = path
        self.textFont = textFont

    #For this i followed what we had in menu.py 
    #using the button class complete and following the whole layout like the menu.py
    #for now the audio and video buttons dont do anything
    #and the back(exit button takes back to the menu page)
    def display_settings_menu(self):
        pygame.display.set_caption("We love the Company | Options Menu")
        run = True
        settings_window = pygame.display.set_mode((1024, 720))
        while run: 
            #this is kinda copied from the menu.py (i assume it just makes the screen)
            window_size = settings_window.get_size()
            self.clock.tick(27)  # Control framerates
            settings_window.fill((0, 0, 0))
            background_image = pygame.image.load(os.path.join(self.path + 'background.jpg'))
            background_image = pygame.transform.scale(background_image, window_size)
            settings_window.blit(background_image, (0, 0))

            menuMousePOS = pygame.mouse.get_pos()

            screen_center_x = settings_window.get_width() // 2
            audio_button_y = settings_window.get_height() // 2 - 50
            video_button_y = settings_window.get_height() // 2 + 50
            back_button_y = settings_window.get_height() // 2 + 150

            BackButton = Button(image=pygame.image.load(self.path + "Assets/button.png"), pos=(screen_center_x, back_button_y),
                            text_input="Back", font=self.textFont, base_color="white", hovering_color="blue")
        
            AudioButton = Button(image=pygame.image.load(self.path + "Assets/button.png"), pos=(screen_center_x, audio_button_y),
                            text_input="Audio", font=self.textFont, base_color="white", hovering_color="blue")
            
            VideoButton = Button(image=pygame.image.load(self.path + "Assets/button.png"), pos=(screen_center_x, video_button_y),
                            text_input="Display", font=self.textFont, base_color="white", hovering_color="blue")

            for button in [AudioButton, BackButton, VideoButton]:
                button.changeColor(menuMousePOS)
                button.update(settings_window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if AudioButton.checkForInput(menuMousePOS):
                        print("Audio settings pressed")  # Placeholder for starting the game
                    elif BackButton.checkForInput(menuMousePOS):
                        run = False
                        print("exit button pressed")
                    elif VideoButton.checkForInput(menuMousePOS):
                        print("Video settings pressed")


            pygame.display.flip()  # Update the display
    
    pygame.quit()