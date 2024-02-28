from backpack import Backpack

from combat import Combat

from grid import Grid

# this should all be static but oh well
strike = Combat()

class Player:
    def __init__(self):
        self.heldItem = None
        self.inventory = Backpack(5)
        self.hitDie = strike.upgrade_path[0]
        self.x = 0
        self.y = 0

    @property
    def position(self):
        return (self.x, self.y)

    def move(self, x, y, grid: Grid):
        if (grid.is_inbounds(self.x + x, self.y + y)):
            obj = grid.get_object(self.x + x, self.y + y)
            if ("name" not in obj or obj["name"] != "wall"):
                self.x += x
                self.y += y
                return True

        return False

    def moveLeft(self, grid: Grid):
        return self.move(-1, 0, grid)
    
    def moveDown(self, grid: Grid):
        return self.move(0, 1, grid)
    
    def moveUp(self, grid: Grid):
        return self.move(0, -1, grid)
    
    def moveRight(self, grid: Grid):
        return self.move(1, 0, grid)