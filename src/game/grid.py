EMPTY_SPACE = dict()

class Grid:
    def __init__(self, width: int, height: int):

        if width < 1 or height < 1:
            raise ValueError("Grids cannot be constructed width non-positive dimensions.")
        
        self.width = width
        self.height = height
        self.matrix = []

        for y in range(height):
            self.matrix.append([EMPTY_SPACE] * width)
    
    def is_inbounds(self, x: int, y: int):
        """Checks if the given pair of coordinates are inside the bounds of the grid."""
        return x >= 0 and y >= 0 and x < self.width and y < self.height
    
    def insert(self, item: dict, x: int, y: int):
        """Places an object at the given coordinates."""
        """Returns True if the placement was successful, and False if something is already in that space."""
        if item == EMPTY_SPACE:
            raise ValueError(f"Attempting to insert item '{EMPTY_SPACE}' which normally denotes empty space. Use removal functions to place empty space.")
        elif not self.is_inbounds(x,y):
            raise ValueError(f"Attempting to insert item '{item}' at out of bounds grid position ({x},{y}).")
        
        if self.matrix[x][y] == EMPTY_SPACE:
            self.matrix[x][y] = item
            return True
        else:
            return False
    
    def remove_at_location(self, x: int, y: int):
        """Removes an object at the given coordinates, and returns the object."""
        """If the space was already empty, returns None instead."""
        if not self.is_inbounds(x,y):
            raise ValueError(f"Attempting to remove item at out of bounds grid position ({x},{y}).")
        
        removed_item = self.matrix[x][y]
        if removed_item == EMPTY_SPACE:
            return None
        else:
            self.matrix[x][y] = EMPTY_SPACE
            return removed_item
    
    def find_object_with_properties(self, key_value_pairs: dict, loose_match: bool=False):
        """Searches the grid for objects that have all of the given key/value pairs in their data."""
        """Returns a list of coordinates for all objects that match."""
        """If loose_match is enabled, objects that match any one of the key value pairs will be included."""
        locations = []

        if loose_match:
            for y in range(len(self.matrix)):
                for x in range(len(self.matrix[y])):
                    object = self.matrix[x][y]
                    for key in key_value_pairs:
                        if key in object and key_value_pairs[key] == object[key]:
                            locations.append((x,y))
                            break
        else:
            matches_required = len(key_value_pairs)
            for y in range(len(self.matrix)):
                for x in range(len(self.matrix[y])):
                    object = self.matrix[x][y]
                    matches = 0
                    for key in key_value_pairs:
                        if key in object and key_value_pairs[key] == object[key]:
                            matches += 1
                    if matches == matches_required:
                        locations.append((x,y))
        
        return locations

    def remove_all_with_properties(self, key_value_pairs: dict, loose_match: bool=False):
        """Removes all objects that have the given properties, searching and selecting the same way as find_object_with_properties."""
        """Returns a list of all objects removed."""
        targets = self.find_object_with_properties(key_value_pairs,loose_match)
        removed = []
        for target in targets:
            removed.append(self.remove_at_location(target[0],target[1]))
        
        return removed

if __name__ == "__main__":
    print("Tests go here!")