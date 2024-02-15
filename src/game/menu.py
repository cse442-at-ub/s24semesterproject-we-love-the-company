import pygame
import os

# Initialize Pygame
pygame.init()

# Set up the path for assets
path = os.path.dirname(__file__) + "/"
print(path)

# Initialize global variables
current_connection = {}
currently_connected = 0
friends = []

# Set up the window
window = pygame.display.set_mode((1024, 720))
pygame.display.set_caption("ShadeShare")

# Set up game variables
newVolume = 0.5
clock = pygame.time.Clock()
textFont = pygame.font.SysFont("Arial", 40)
game_won = 0

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

def draw_text(text, font, color, x, y):
    textImg = font.render(text, True, color)
    window.blit(textImg, (x, y))

def mainMenu():
    pygame.display.set_caption("background")
    run = True
    window_size = window.get_size()  # Get the current window size


    while run:
        clock.tick(27)  # Control framerates
        window.fill((0, 0, 0))
        background_image = pygame.image.load(path + 'background.jpg')
        background_image = pygame.transform.scale(background_image, window_size)
        window.blit(background_image, (0, 0))



        menuMousePOS = pygame.mouse.get_pos()

        screen_center_x = window.get_width() // 2
        play_button_y = window.get_height() // 2 - 50
        exit_button_y = window.get_height() // 2 + 150

        PlayButton = Button(image=pygame.image.load(path + "Assets/button.png"), pos=(screen_center_x, play_button_y),
                            text_input="Play", font=textFont, base_color="white", hovering_color="blue")

        ExitButton = Button(image=pygame.image.load(path + "Assets/button.png"), pos=(screen_center_x, exit_button_y),
                            text_input="Exit", font=textFont, base_color="white", hovering_color="blue")

        for button in [PlayButton, ExitButton]:
            button.changeColor(menuMousePOS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if PlayButton.checkForInput(menuMousePOS):
                    print("Play button clicked")  # Placeholder for starting the game
                if ExitButton.checkForInput(menuMousePOS):
                    run = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    mainMenu()
