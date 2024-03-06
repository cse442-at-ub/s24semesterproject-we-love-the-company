from combat import Combat

from grid import Grid

# this should all be static but oh well
strike = Combat()

class Enemy:
    def __init__(self, x = 0, y = 0):
        self.hitDie = strike.upgrade_path[0]
        self.x = x
        self.y = y

    @property
    def position(self):
        return (self.x, self.y)

    # returns False when movement isn't possible
    def move(self, x, y, grid: Grid):
        if (grid.is_inbounds(self.x + x, self.y + y)):
            obj = grid.get_object(self.x + x, self.y + y)

            # SUBJECT TO CHANGE !!!
            if (obj == None or "name" not in obj or obj["name"] != "wall"):
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

    # returns "defeated" or new hitDie
    def getHit(self):
        res = strike.downgrade_die(self.hitDie)

        if (res != "defeated"):
            self.hitDie = res

        return res

    # increases the die
    def increaseDie(self):
        self.hitDie = strike.upgrade_die(self.hitDie)
