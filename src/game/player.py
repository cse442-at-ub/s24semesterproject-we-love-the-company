from backpack import Backpack

from combat import Combat

from grid import Grid

# this should all be static but oh well
strike = Combat()

class Player:
    def __init__(self, grid: Grid, x: int, y: int, image):
        self.heldItem = None
        self.inventory = Backpack(5)
        self.hitDie = strike.upgrade_path[0]
        self.grid = grid

        player_object = {
            "name":"player",
            "obstruction":True,
            "image":image
        }

        self.grid.insert(player_object,x,y)
    
    @property
    def position(self):
        """Returns the position of the player in the grid."""
        return list(self.grid.find_object_with_properties({"name":"player"}))[0]
    
    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    # returns False when movement isn't possible
    def move(self, x, y):
        current_x,current_y = self.position
        if (self.grid.is_inbounds(current_x + x, current_y + y)):
            obj = self.grid.get_object(current_x + x, current_y + y)

            # SUBJECT TO CHANGE !!!
            if (obj == None or not obj.get("obstruction",False)):
                player_obj = self.grid.get_object(current_x,current_y)
                self.grid.remove_at_location(current_x,current_y)
                self.grid.insert(player_obj,current_x+x,current_y+y)
                return True

        return False

    def moveLeft(self):
        return self.move(-1, 0)

    def moveDown(self):
        return self.move(0, 1)

    def moveUp(self):
        return self.move(0, -1)

    def moveRight(self):
        return self.move(1, 0)

    def useHeld(self):
        pass

    # picks up an item from the ground
    def pickUp(self, x, y, range = 1):
        # check if out of range
        if (abs(self.x - x) + abs(self.y - y) > range):
            return False

        if (self.heldItem == None):
            if (self.grid.is_inbounds(x, y)):
                obj = self.grid.get_object(x, y)
                if (obj != None and "item" in obj):
                    self.grid.remove_at_location(x, y)
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
    def drop(self):
        if (self.heldItem != None):
            obj = {"item": self.heldItem}
            if (self.grid.insert(obj, self.x, self.y)):
                self.heldItem = None
                return True

        return False

    # drops from the backpack
    def dropFromBackpack(self, id):
        if (not self.inventory.isEmpty() and id in self.inventory.dict):
            obj = {"item": id}
            if (self.grid.insert(obj, self.x, self.y)):
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
