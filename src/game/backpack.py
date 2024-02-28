class Backpack:

    def __init__(self, capacity):
        self.capacity = capacity
        self.dict = {}
        self.number = 0

    def add(self, id):
        self.number = 0
        if not self.isEmpty():
            if type(self.dict.get(id)) == type(self.number):
                self.number = self.dict.get(id)

        if not self.isFull():
            self.number = self.number + 1
            self.dict.update({id: self.number})

    def remove(self,id):
        self.number = 0
        if not self.isEmpty():
            if type(self.dict.get(id))==type(self.number) :
                self.number = self.dict.get(id)
            self.number = self.number - 1

        self.dict.update({id: self.number})
        if self.number <= 0:
            self.dict.pop(id)

    def isFull(self):
        return sum(self.dict.values()) >= self.capacity
    
    def isEmpty(self):
        return len(self.dict) <= 0

    def printItems(self):
        print(self.dict)

if __name__ == "__main__":
    ## Test 1
    backpack1 = Backpack(5)
    backpack1.add("common")
    backpack1.printItems()

    ## Test 2
    backpack2 = Backpack(5)
    backpack2.remove("")
    backpack2.printItems()

    ## Test 3
    backpack3 = Backpack(5)
    backpack3.add("common")
    backpack3.remove("")
    backpack3.printItems()

    ## Test 4
    backpack4 = Backpack(5)
    backpack4.add("common")
    backpack4.add("common")
    backpack4.remove("common")
    backpack4.printItems()

    ## Test 5
    backpack5 = Backpack(6)
    backpack5.add("common")
    backpack5.add("common")
    backpack5.remove("common")
    backpack5.remove("common")
    backpack5.printItems()

    ## Test 6
    backpack6 = Backpack(5)
    backpack6.add("common")
    backpack6.add("common")
    backpack6.add("common")
    backpack6.add("common")
    backpack6.add("common")
    backpack6.add("common")
    backpack6.printItems()

    ## Test 7
    backpack7 = Backpack(5)
    backpack7.add("common")
    backpack7.add("common")
    backpack7.add("uncommon")
    backpack7.printItems()

    ## Test 8
    backpack8 = Backpack(2)
    backpack8.add("common")
    backpack8.add("common")
    backpack8.add("uncommon")
    backpack8.printItems()
