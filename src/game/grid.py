class grid:
    def __init__(self, width: int, height: int):

        if width < 1 or height < 1:
            raise ValueError("Grids cannot be constructed width non-positive dimensions.")
        
        self.width = width
        self.height = height
        self.matrix = []

        for y in range(height):
            self.matrix.append(['.'] * width)
    
    def __str__(self):
        row_strings = []
        for row in self.matrix:
            row_strings.append(''.join(row))
        return '\n'.join(row_strings)