class Common:
    def __init__(self):
        self.value = 10.0
        self.identifier = "common"
        self.name = "common object"
        self.description = "a common object"

class Sword(Common):
    def __init__(self):
        super().__init__()
        self.value = 50.0
        self.identifier = "sword"
        self.name = "Sword of Might"
        self.description = "Increases attack power."

class Shield(Common):
    def __init__(self):
        super().__init__()
        self.value = 40.0
        self.identifier = "shield"
        self.name = "Shield of Fortitude"
        self.description = "Increases defense."

class Potion(Common):
    def __init__(self):
        super().__init__()
        self.value = 20.0
        self.identifier = "potion"
        self.name = "Healing Potion"
        self.description = "Restores health."

class Boots(Common):
    def __init__(self):
        super().__init__()
        self.value = 30.0
        self.identifier = "boots"
        self.name = "Boots of Speed"
        self.description = "Increases movement speed."
        
class Arrow(Common):
    def __init__(self):
        super().__init__()
        self.value = 5.0
        self.identifier = "arrow"
        self.name = "Arrow of Swift"
        self.description = "Increases range attack speed."



class Item:
    def __init__(self):
        self.dict = {}

    def add(self, object):
        if object.identifier in self.dict:
            raise Exception('duplicate identifier')
        self.dict[object.identifier] = object


    def get(self, id):
        if id not in self.dict:
            raise Exception('bad identifier!')
        return self.dict[id]


