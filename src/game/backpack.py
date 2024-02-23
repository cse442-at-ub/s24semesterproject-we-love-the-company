class BackPack:

    def __init__(self, capacity):
        self.capacity = capacity;
        self.dict = {}
        self.number = 0

    def add(self, id):
        if self.number < self.capacity:
            self.number = self.number + 1
            self.dict.update({id: self.number})

    def remove(self,id):
        length = len(self.dict)
        self.number = self.number - 1
        self.dict.update({id: self.number})
        if self.number <= 0:
            self.dict.pop(id)

    def printiterm(self):
        print(self.dict)

## Test 1
backpack1 = BackPack(5)
backpack1.add("common")
backpack1.printiterm()

## Test 2
backpack2 = BackPack(5)
backpack2.remove("")
backpack2.printiterm()

## Test 3
backpack3 = BackPack(5)
backpack3.add("common")
backpack3.remove("")
backpack3.printiterm()

## Test 4
backpack4 = BackPack(5)
backpack4.add("common")
backpack4.add("common")
backpack4.remove("common")
backpack4.printiterm()

## Test 5
backpack5 = BackPack(6)
backpack5.add("common")
backpack5.add("common")
backpack5.remove("common")
backpack5.remove("common")
backpack5.printiterm()

## Test 6
backpack6 = BackPack(5)
backpack6.add("common")
backpack6.add("common")
backpack6.add("common")
backpack6.add("common")
backpack6.add("common")
backpack6.add("common")
backpack6.printiterm()


