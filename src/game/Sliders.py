import pygame

audio_pack = pygame.mixer.music.load("src/game/Assets/Background_music_menu.wav")
audio_control = pygame.mixer.music.play(-1)
button_sound_que = pygame.mixer.Sound("src/game/Assets/button_click.mp3")

class Slider:
    def __init__(self, xpos, ypos, width, height, min_val: int, max_val: int):
        self.x_pos = xpos
        self.y_pos = ypos
        self.width = width
        self.height = height

        self.is_dragging = False #flag to see if it is being dragged

        self.min = min_val
        self.max = max_val

        self.value = min_val + max_val // 2  #initial val

        self.container_rect = pygame.Rect(self.x_pos, (self.y_pos - height // 2), width, height)  #makes the track

        self.handle_radius = 10  # Width of the slider handle
        self.handle_rec = pygame.Rect(self.container_rect.left, self.container_rect.centery - 2, self.container_rect.width, 4)
        self.handle_center = self.container_rect.left + self.width // 2


    def draw(self,screen):
        pygame.draw.rect(screen, (255,255,255), self.container_rect)
        pygame.draw.circle(screen, (255, 0, 0), (self.handle_rec.centerx, self.handle_rec.centery), self.handle_radius)

    def move(self, pos):
        self.handle_center = max(self.container_rect.left, min(pos[0], self.container_rect.right))

    def update_value(self):
        #hopefully this calculation is right
        relative_position = self.handle_center - self.container_rect.left
        total_width = self.container_rect.width - 2 * self.handle_radius

        # Calculate the volume based on the relative position of the handle
        volume = (relative_position / total_width) * 100  # Scale to a 0-100 range

        # Update the volume of the background music
        pygame.mixer.music.set_volume(volume / 100)  # Set volume between 0 and 1

    def move_handle(self, event):
        if event == pygame.MOUSEBUTTONDOWN:
            if self.handle_rec.collidepoint(event.pos):
                self.is_dragging = True
        elif event == pygame.MOUSEBUTTONUP:
            self.is_dragging = False
        elif event == pygame.MOUSEMOTION:
            if self.is_dragging:      
                self.move(event.pos)
                self.update_value()