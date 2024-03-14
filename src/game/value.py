
from item import *
from backpack import *

# this code doesn't work LOL!!!!!

def value(backpack, list):
    value = 0.0
    com = Common()
    itm = Items()
    for obj in backpack.dict:
        if (type(obj) == type(com)):
            value = value + obj.value
        if(type(obj) == type(itm)):
            for it in obj.dict:
                value = value + obj.get(it).value
    print(value)
    return value

# Test 1
backpack = Backpack(6)
object1 = Common()
list = Items()
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
backpack2 = Backpack(5)
backpack2.add(object1)
backpack2.add(object2)
item2 = Items()
object5 = Common()
object5.value = 13.37
item2.add(object5)
backpack2.add(item2)
value(backpack2,list)
