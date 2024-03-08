import pygame

class DropDown:
    def __init__(self, options,pos,font):
        self.options = options
        self.pos = pos
        self.font = font
        self.selected_option = None
        self.rects = []
        self.opened = False

        for key, val in enumerate(options):
            rect = pygame.Rect(pos[0], pos[1] + (font.get_linesize() * key), 200, font.get_linesize())
            self.rects.append(rect)
        
    
    def draw(self, screen):
        selected_text = self.font.render(self.selected_option if self.selected_option else "Select Resolution", True, (255, 255, 255))
        screen.blit(selected_text, self.pos)
    
        if self.opened:
            for idx, option in enumerate(self.options):
                pygame.draw.rect(screen, (50, 50, 50), self.rects[idx])
                option_text = self.font.render(option, True, (255, 255, 255))
                screen.blit(option_text, self.rects[idx].topleft)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Handle dropdown selection logic here
                if self.rects[0].collidepoint(event.pos):  # Assuming first rect is for selection
                    self.opened = not self.opened
                elif self.opened:
                    for idx, rect in enumerate(self.rects):
                        if rect.collidepoint(event.pos):
                            selected_option = self.options[idx]
                            # Extract width and height from the selected option (e.g., "1920x1080")
                            width, height = map(int, selected_option.split('x'))
                            self.selected_option = selected_option
                            self.opened = False
                            self.update_resolution(width, height)  # Update resolution
                            break