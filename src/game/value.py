
from item import *
from backpack import *

# this code doesn't work LOL!!!!!

def value(backpack: Backpack, items: Items):
    value = 0.0

    for item in backpack.items.items():
        id = item[0]
        count = item[1]

        value += items.get(id).value * count

    return value

if __name__ == "__main__":
    # Test 1
    backpack = Backpack(6)
    object1 = Common()
    list = Items()

    print(value(backpack,list))

    # Test 2
    backpack.add(object1)
    print(value(backpack,list))

    # Test 3
    object2 = Common()
    backpack.add(object2)
    object3 = Common()
    backpack.add(object3)
    object4 = Common()
    backpack.add(object4)
    print(value(backpack,list))

    # Test 4
    backpack2 = Backpack(5)
    backpack2.add(object1)
    backpack2.add(object2)

    backpack2.add(Uncommon())
    print(value(backpack2,list))
