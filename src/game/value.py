class BackPack:

    def __init__(self, capacity):
        self.capacity = capacity;
        self.dict = {}
        self.number = 0

    def add(self, id):
        self.number = 0
        count = sum(self.dict.values())
        if len(self.dict) > 0:
            if type(self.dict.get(id)) == type(self.number):
                self.number = self.dict.get(id)
        if count < self.capacity:
            self.number = self.number + 1
            self.dict.update({id: self.number})

    def remove(self,id):
        self.number = 0
        if len(self.dict) > 0:
            if type(self.dict.get(id))==type(self.number) :
                self.number = self.dict.get(id)
            self.number = self.number - 1
        self.dict.update({id: self.number})
        if self.number <= 0:
            self.dict.pop(id)

    def printiterm(self):
        print(self.dict)

class Common:

    def __init__(self):
        self.value = 10.0
        self.identifier = "common"
        self.name = "common object"
        self.description ="a common object"

class Item:
    def __init__(self):
            self.dict = {}

    def add(self, object):
        if self.dict.get(object.identifier) != None:
            raise Exception('duplicate identifier')
        self.dict.update({object.identifier: object})

    def get(self, id):
        if self.dict.get(id) == None :
            raise Exception('bad identifier!')
        return self.dict.get(id)


def value(backpack, list):
    value = 0.0
    com = Common()
    itm = Item()
    for obj in backpack.dict:
        if (type(obj) == type(com)):
            value = value + obj.value
        if(type(obj) == type(itm)):
            for it in obj.dict:
                value = value + obj.get(it).value
    print(value)
    return value

# Test 1
backpack = BackPack(6)
object1 = Common()
list = Item()
list.add(object1)

value(backpack,list)

# Test 2
backpack.add(object1)
value(backpack,list)

# Test 3
object2 = Common()
backpack.add(object2)
object3 = Common()
backpack.add(object3)
object4 = Common()
backpack.add(object4)
value(backpack,list)

# Test 4
backpack2 = BackPack(5)
backpack2.add(object1)
backpack2.add(object2)
item2 = Item()
object5 = Common()
object5.value = 13.37
item2.add(object5)
backpack2.add(item2)
value(backpack2,list)
