from backpack import Backpack

from combat import Combat

from grid import Grid

# this should all be static but oh well
strike = Combat()

class Player:
    def __init__(self, x = 0, y = 0):
        self.heldItem = None
        self.inventory = Backpack(5)
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

    def useHeld(self):
        pass

    # picks up an item from the ground
    def pickUp(self, x, y, grid: Grid, range = 1):
        # check if out of range
        if (abs(self.x - x) + abs(self.y - y) > range):
            return False

        if (self.heldItem == None):
            if (grid.is_inbounds(x, y)):
                obj = grid.get_object(x, y)
                if (obj != None and "item" in obj):
                    grid.remove_at_location(x, y)
                    self.heldItem = obj["item"]
                    return True

        return False

    # puts item in hands into inventory
    def stash(self):
        if (self.heldItem != None and not self.inventory.isFull()):
            self.inventory.add(self.heldItem)
            self.heldItem = None
            return True

        return False

    # drops currently held item to feet
    def drop(self, grid: Grid):
        if (self.heldItem != None):
            obj = {"item": self.heldItem}
            if (grid.insert(obj, self.x, self.y)):
                self.heldItem = None
                return True

        return False

    # drops from the backpack
    def dropFromBackpack(self, id, grid: Grid):
        if (not self.inventory.isEmpty() and id in self.inventory.dict):
            obj = {"item": id}
            if (grid.insert(obj, self.x, self.y)):
                self.inventory.remove(id)
                return True

        return False

    # takes item from inventory and puts into hands
    def retrieve(self, id):
        if (self.heldItem == None and not self.inventory.isEmpty()):
            if (id in self.inventory.dict):
                self.heldItem = id
                self.inventory.remove(id)
                return True

        return False

    # returns "defeated" or new hitDie
    def getHit(self):
        res = strike.downgrade_die(self.hitDie)

        if (res != "defeated"):
            self.hitDie = res

        return res

    # increases the die
    def increaseDie(self):
        self.hitDie = strike.upgrade_die(self.hitDie)
