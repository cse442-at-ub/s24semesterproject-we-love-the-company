import pygame


class Slider:
    def __init__(self, pos, width, height, min_value, max_value):
        self.rect = pygame.Rect(pos[0] - width // 2, pos[1] - height // 2, width, height)
        self.handle_pos = pos[0] - width // 2, pos[1]
        self.handle_radius = height // 2
        self.min_value = min_value
        self.max_value = max_value
        self.value = min_value

    def update(self, screen):
        #slider track
        track_rect = pygame.Rect(self.rect.left, self.rect.centery - 2, self.rect.width, 4)
        pygame.draw.rect(screen, (200, 200, 200), track_rect)

        #slider handle
        pygame.draw.circle(screen, (0, 0, 0), self.handle_pos, self.handle_radius)

    def move_handle(self, pos):
        #Move the handle based on mouse position
        x = min(max(pos[0], self.rect.left), self.rect.right)
        self.handle_pos = (x, self.handle_pos[1])
        self.value = int((x - self.rect.left) / self.rect.width * (self.max_value - self.min_value) + self.min_value)
