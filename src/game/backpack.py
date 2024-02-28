class BackPack:

    def __init__(self, capacity):
        self.capacity = capacity
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

    def printItems(self):
        print(self.dict)

if __name__ == "__main__":
    ## Test 1
    backpack1 = BackPack(5)
    backpack1.add("common")
    backpack1.printItems()

    ## Test 2
    backpack2 = BackPack(5)
    backpack2.remove("")
    backpack2.printItems()

    ## Test 3
    backpack3 = BackPack(5)
    backpack3.add("common")
    backpack3.remove("")
    backpack3.printItems()

    ## Test 4
    backpack4 = BackPack(5)
    backpack4.add("common")
    backpack4.add("common")
    backpack4.remove("common")
    backpack4.printItems()

    ## Test 5
    backpack5 = BackPack(6)
    backpack5.add("common")
    backpack5.add("common")
    backpack5.remove("common")
    backpack5.remove("common")
    backpack5.printItems()

    ## Test 6
    backpack6 = BackPack(5)
    backpack6.add("common")
    backpack6.add("common")
    backpack6.add("common")
    backpack6.add("common")
    backpack6.add("common")
    backpack6.add("common")
    backpack6.printItems()

    ## Test 7
    backpack7 = BackPack(5)
    backpack7.add("common")
    backpack7.add("common")
    backpack7.add("uncommon")
    backpack7.printItems()

    ## Test 8
    backpack8 = BackPack(2)
    backpack8.add("common")
    backpack8.add("common")
    backpack8.add("uncommon")
    backpack8.printItems()
