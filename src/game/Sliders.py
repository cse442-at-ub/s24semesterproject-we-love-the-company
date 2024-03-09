
import pygame
from gamestate import *
class Slider:
    def __init__(self, pos: tuple, size: tuple, min_value: int, max_value: int, initial_val: None, game_state: Gamestate) -> None:
        self.pos = pos
        self.size = size
        self.hovered = False
        self.grabbed = False
<<<<<<< HEAD

=======
>>>>>>> Video_settings
        self.game_state = game_state

        if initial_val is not None:
            self.current_val = initial_val
        else:
            self.current_val = (self.min_value + self.max_value) / 2
<<<<<<< HEAD
        self.min_value = min_value
        self.max_value = max_value

        if initial_val is not None:
            self.current_val = initial_val
        else:
            self.current_val = (self.min_value + self.max_value) / 2

        # Calculate slider coordinates accurately
        self.slider_left = self.pos[0] - self.size[0] // 2
        self.slider_right = self.slider_left + self.size[0]
        self.slider_top = self.pos[1] - self.size[1] // 2

        # Calculate slider coordinates accurately
        self.slider_left = self.pos[0] - self.size[0] // 2
        self.slider_right = self.slider_left + self.size[0]
        self.slider_top = self.pos[1] - self.size[1] // 2

=======

        self.min_value = min_value
        self.max_value = max_value

        # Calculate slider coordinates accurately
        self.slider_left = self.pos[0] - self.size[0] // 2
        self.slider_right = self.slider_left + self.size[0]
        self.slider_top = self.pos[1] - self.size[1] // 2

>>>>>>> Video_settings
        # Calculate initial handle position based on value
        self.handle_pos = self.slider_left + (self.current_val / (self.max_value - self.min_value)) * (self.slider_right - self.slider_left)
        self.handle_rect = pygame.Rect(self.handle_pos, self.slider_top, 10, self.size[1])

        self.container_rect = pygame.Rect(self.slider_left, self.slider_top, self.size[0], self.size[1])

    def move_handle(self, pos):
        # Clamp mouse position to slider bounds
        new_handle_pos = max(self.slider_left, min(pos[0], self.slider_right - self.handle_rect.width))
        self.handle_pos = new_handle_pos
        self.handle_rect.x = self.handle_pos
        self.current_val = float(self.get_value())
    
    def set_lable(self,lable):
        self.lable = lable

    def hover(self):
        self.hovered = True

    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.container_rect)
        pygame.draw.rect(screen, (255, 0, 0), self.handle_rect)

    def get_value(self):
        # Calculate value based on handle position
        value_range = self.slider_right - self.slider_left - 1
        handle_val = self.handle_pos - self.slider_left
<<<<<<< HEAD

        val = (handle_val / value_range) * (self.max_value - self.min_value) + self.min_value
        #print(val)
        return val

=======
        return (handle_val / value_range) * (self.max_value - self.min_value) + self.min_value
>>>>>>> Video_settings

    def display_value(self, screen):
        value_font = pygame.font.Font(None, 30)
        value_text = value_font.render(str(int(self.get_value())), True, (0,0,100))
        value_text_rect = value_text.get_rect(center=(self.pos[0], self.slider_top - 15))
        screen.blit(value_text, value_text_rect)

        lable_font = pygame.font.Font(None, 40)
        lable_text = lable_font.render(self.lable, True, (0, 0, 0))
        label_text_rect = lable_text.get_rect(centery=self.pos[1])
        label_text_rect.right = self.container_rect.left - 5
<<<<<<< HEAD
        screen.blit(lable_text, label_text_rect)
=======
        screen.blit(lable_text, label_text_rect)


>>>>>>> Video_settings
