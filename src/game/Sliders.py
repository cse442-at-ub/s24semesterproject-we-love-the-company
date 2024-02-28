import pygame

class Slider:
    def __init__(self, pos: tuple, width, height, min_val: int, max_val: int):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.width = width
        self.height = height

        self.grabbed = False #flag to see if it is being dragged

        self.min = min_val
        self.max = max_val

        self.value = min_val + max_val // 2  #initial val

        self.slider_color = (255,255,255)

        self.container_rect = pygame.Rect(self.x_pos, (self.y_pos - height // 2), width, height)  #makes the track


    def draw(self,screen):
        pygame.draw.rect(screen, self.slider_color, self.container_rect)

    def move(self, pos):
        self.container_rect.x = max(self.x_pos, min(pos[0], self.x_pos + self.width))

    def update_value(self):
        self.value = (self.container_rect.x - self.x_pos) / self.width * (self.max - self.min) + self.min

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.move(event.pos)
                self.update_value()