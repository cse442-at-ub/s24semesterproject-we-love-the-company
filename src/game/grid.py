EMPTY_SPACE = '.'

class Grid:
    def __init__(self, width: int, height: int):

        if width < 1 or height < 1:
            raise ValueError("Grids cannot be constructed width non-positive dimensions.")
        
        self.width = width
        self.height = height
        self.matrix = []

        for y in range(height):
            self.matrix.append([EMPTY_SPACE] * width)
    
    def __str__(self):
        row_strings = []
        for row in self.matrix:
            row_strings.append(''.join(row))
        return '\n'.join(row_strings)
    
    def is_inbounds(self, x: int, y: int):
        return x >= 0 and y >= 0 and x < self.width and y < self.height
    
    def insert(self, item: str, x: int, y: int):
        if len(item) != 1:
            raise ValueError(f"Attempting to insert item '{item}' with invalid length ({len(item)}). Expected length of exactly 1.")
        elif item == EMPTY_SPACE:
            raise ValueError(f"Attempting to insert item '{EMPTY_SPACE}' which normally denotes empty space. Use removal functions to place empty space.")
        elif not self.is_inbounds(x,y):
            raise ValueError(f"Attempting to insert item '{item}' at out of bounds grid position ({x},{y}).")
        
        replaced_item = self.matrix[x][y]
        if replaced_item == item:
            return None
        else:
            self.matrix[x][y] = item
            return True
    
    def remove_at_location(self, x: int, y: int):
        if not self.is_inbounds(x,y):
            raise ValueError(f"Attempting to remove item at out of bounds grid position ({x},{y}).")
        
        removed_item = self.matrix[x][y]
        if removed_item == EMPTY_SPACE:
            return None
        else:
            self.matrix[x][y] = EMPTY_SPACE
            return removed_item

    def remove_all_of_type(self, item: str):
        if len(item) != 1:
            raise ValueError(f"Attempting to remove item '{item}' with invalid length ({len(item)}). Expected length of exactly 1.")
        elif item == EMPTY_SPACE:
            raise ValueError(f"Attempting to remove item '{EMPTY_SPACE}' which normally denotes empty space.")
        
        removed_locations = []
        for y in range(len(self.matrix)):
            row = self.matrix[y]
            for x in range(len(row)):
                if self.matrix[x][y] == item:
                    self.matrix[x][y] = EMPTY_SPACE
                    removed_locations.append((x,y))
        
        return removed_locations