import pygame
import os
from OptionsMenu import Settings
from Buttons import Button
from HowToPlay import Instructions
#This initialization thing I think we did it in the game.py so I think we can use that and not
#use this makes it game.py pointless kinda. tbh im getting used to pygame so idk for sure tho.

# Initialize Pygame
pygame.init()

# Set up the path for assets
path = os.path.dirname(__file__) + "/"
# Initialize global variables
current_connection = {}
currently_connected = 0
friends = []

# Set up the window
window = pygame.display.set_mode((1024, 720))

# Set up game variables
newVolume = 0.5
clock = pygame.time.Clock()
textFont = pygame.font.SysFont("Arial", 40)
paragraphFont = pygame.font.SysFont("Arial", 30)
game_won = 0


def draw_text(text, font, color, x, y):
    textImg = font.render(text, True, color)
    window.blit(textImg, (x, y))

def mainMenu():
    pygame.display.set_caption("We love the Company")
    run = True
    window_size = window.get_size()  # Get the current window size

    #intializing the options object so I can call it later (designated by : here)
    Options = Settings(window, clock, path, textFont)

    #initialize How To Play screen here
    HowToPlay = Instructions(window, clock, path, textFont, paragraphFont)

    while run:
        clock.tick(27)  # Control framerates
        window.fill((0, 0, 0))
        background_image = pygame.image.load(path + 'background.jpg')
        background_image = pygame.transform.scale(background_image, window_size)
        window.blit(background_image, (0, 0))

        logo_image = pygame.image.load(path + 'logo3.png')
        logo_image = pygame.transform.scale(logo_image, window_size)
        window.blit(logo_image, (0, -200))

        menuMousePOS = pygame.mouse.get_pos()

        screen_center_x = window.get_width() // 2
        play_button_y = window.get_height() // 2 - 50
        exit_button_y = window.get_height() // 2 + 150
        #putting the settings button in the middle of the play and exit buttons
        settings_button_y = window.get_height() // 2 + 50
        instruct_button_y = window.get_height() - 50

        PlayButton = Button(image=pygame.image.load(path + "Assets/button.png"), pos=(screen_center_x, play_button_y),
                            text_input="Play", font=textFont, base_color="white", hovering_color="blue")

        ExitButton = Button(image=pygame.image.load(path + "Assets/button.png"), pos=(screen_center_x, exit_button_y),
                            text_input="Exit", font=textFont, base_color="white", hovering_color="blue")
        
        #put a settings button with the button.img. It uses the same fonts and color and hover color
        SettingsButton = Button(image=pygame.image.load(path + "Assets/button.png"), pos=(screen_center_x, settings_button_y),
                                text_input="Settings", font=textFont, base_color="white", hovering_color="blue")

        InstructionsButton = Button(image=pygame.image.load(path + "Assets/button.png"), pos=(screen_center_x, instruct_button_y),
                                text_input="How To Play", font=textFont, base_color="white", hovering_color="blue")

        for button in [PlayButton, ExitButton, SettingsButton, InstructionsButton]:
            button.changeColor(menuMousePOS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if PlayButton.checkForInput(menuMousePOS):
                    print("Play button clicked")  # Placeholder for starting the game
                elif ExitButton.checkForInput(menuMousePOS):
                    run = False
                #if the settings button is clicked then it should say settinsg button clicked in the terminal an take to the options menu
                elif SettingsButton.checkForInput(menuMousePOS):
                    print("Settings button clicked")
                    #calling the settings page func from the settings class (in @OptionsMenu)
                    #here
                    Options.display_settings_menu()
                elif InstructionsButton.checkForInput(menuMousePOS):
                    print("How To Play button clicked")
                    HowToPlay.display_instructions_menu()

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    mainMenu()
