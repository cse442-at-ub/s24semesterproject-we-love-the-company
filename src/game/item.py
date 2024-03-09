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
# Test 1
common = Common()

print(common.value)
print(common.identifier)
print(common.name)
print(common.description)

# Test 2
item = Item()
item.add(common)
print(item.dict)
print(item.get("common"))
print(item.get("common").value)
print(item.get("common").identifier)
print(item.get("common").name)
print(item.get("common").description)
# Test 3
print(item.get(""))
# Test 4
common2 = Common()
common2.identifier = "obj"
item.add(common2)

print(item.get("common"))
print(item.get("common").value)
print(item.get("common").identifier)
print(item.get("common").name)
print(item.get("common").description)
print(item.get("obj"))
print(item.get("obj").value)
print(item.get("obj").identifier)
print(item.get("obj").name)
print(item.get("obj").description)

# Test 5
item2 = Item()
item2.add(common)
item2.add(common)
print(item2.dict)
