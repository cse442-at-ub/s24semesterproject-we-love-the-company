import pygame
from gamestate import Handler
from grid import Grid, EMPTY_SPACE  # Adjust this path as needed

class GameScene:
    def __init__(self, screen):
        self.screen = screen
        self.id = "game_scene"
        self.grid = Grid(width=10, height=10)  # Initialize the grid with desired dimensions
        
        # Populate the grid with initial objects
        self.populate_grid()

    def initHandlers(self, gamestate):
        gamestate.handlers[self.id] = Handler(
            onRender=self.render,
            onUpdate=self.update,
            onMousePress=self.onMousePress,)

    def populate_grid(self):
        # Define the objects to populate the grid, simplified without sprite paths
        objects = [
            {"type": "player", "x": 5, "y": 5},
            {"type": "enemy", "x": 2, "y": 3},
            # Add more objects as needed
        ]

        # Insert each object into the grid
        for obj in objects:
            self.grid.insert(item=obj, x=obj["x"], y=obj["y"])

    def render(self, gamestate):
        self.screen.fill((0, 0, 0))

        cell_size = 64  # Define the size of each cell in the grid
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                obj = self.grid.get_object(x, y)
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                if obj is not None:
                    if obj["type"] == "player":
                        color = (0, 255, 0)  # Green for player
                    elif obj["type"] == "enemy":
                        color = (255, 0, 0)  # Red for enemy
                    pygame.draw.rect(self.screen, color, rect)
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)  # Draw empty cell borders

        pygame.display.flip()

    def update(self, gamestate, dt):
        # Add logic to update objects in the grid as needed
        pass

    def onMousePress(self, gamestate, pos, button, touch):
        # Implement interactions based on mouse press
        pass