class Backpack:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = {}
        self.current_capacity = 0

    def add(self, id: str):
        if self.current_capacity < self.capacity:
            if id in self.items:
                self.items[id] += 1
            else:
                self.items[id] = 1
            self.current_capacity += 1
        else:
            raise Exception('Backpack is full')

    def remove(self, identifier):
        """Remove an item from the backpack by its identifier."""
        if identifier in self.items:
            self.items[identifier] -= 1
            self.current_capacity -= 1
            if self.items[identifier] <= 0:
                del self.items[identifier]
        else:
            raise Exception(f'Item with identifier {identifier} not found in backpack.')

    def isFull(self):
        return self.current_capacity >= self.capacity
    
    def isEmpty(self):
        return self.current_capacity == 0

    def printItems(self):
        print("Backpack items:")
        for id, count in self.items.items():
            print(f"{id}: {count}")
