import pygame

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


    def draw(self,screen):
        pygame.draw.rect(screen, (255,255,255), self.container_rect)
        pygame.draw.circle(screen, (0, 0, 0), (self.handle_rec.centerx, self.handle_rec.centery), self.handle_radius)

    def move(self, pos):
        self.container_rect.x = max(self.x_pos, min(pos[0], self.x_pos + self.width))

    def update_value(self):
        self.value = (self.container_rect.x - self.x_pos) / self.width * (self.max - self.min) + self.min

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