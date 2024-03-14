import os

path = os.path.dirname(__file__)

class Common:
    def __init__(self):
        self.value = 10.0
        self.identifier = "common"
        self.name = "common object"
        self.description = "a common object"
        self.image = os.path.join(path, "Assets", "apple.png")

class Uncommon:
    def __init__(self):
        self.value = 13.37
        self.identifier = "uncommon"
        self.name = "uncommon object"
        self.description = "an uncommon object"
        self.image = os.path.join(path, "Assets", "tree.png")

class Sword(Common):
    def __init__(self):
        super().__init__()
        self.value = 50.0
        self.identifier = "sword"
        self.name = "Sword of Might"
        self.description = "Increases attack power."
        self.image = os.path.join(path, "Assets", "enemy.png")

class Shield(Common):
    def __init__(self):
        super().__init__()
        self.value = 40.0
        self.identifier = "shield"
        self.name = "Shield of Fortitude"
        self.description = "Increases defense."
        self.image = os.path.join(path, "Assets", "player.png")

class Potion(Common):
    def __init__(self):
        super().__init__()
        self.value = 20.0
        self.identifier = "potion"
        self.name = "Healing Potion"
        self.description = "Restores health."
        self.image = os.path.join(path, "Assets", "player.png")

class Boots(Common):
    def __init__(self):
        super().__init__()
        self.value = 30.0
        self.identifier = "boots"
        self.name = "Boots of Speed"
        self.description = "Increases movement speed."
        self.image = os.path.join(path, "Assets", "player.png")

class Arrow(Common):
    def __init__(self):
        super().__init__()
        self.value = 5.0
        self.identifier = "arrow"
        self.name = "Arrow of Swift"
        self.description = "Increases range attack speed."
        self.image = os.path.join(path, "Assets", "player.png")

class Items:
    def __init__(self):
        self.dict = {}

        self.add(Common())
        self.add(Uncommon())
        self.add(Sword())
        self.add(Shield())
        self.add(Potion())
        self.add(Boots())
        self.add(Arrow())

    def add(self, object):
        if object.identifier in self.dict:
            raise Exception('duplicate identifier')
        self.dict[object.identifier] = object


    def get(self, id):
        if id not in self.dict:
            raise Exception('bad identifier!')
        return self.dict[id]