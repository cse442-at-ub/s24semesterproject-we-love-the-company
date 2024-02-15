import pygame

# pygame doesn't do this by default
# linear intopolation that clamps the weight
def lerp(a: float, b: float, w: float):
    if (w <= 0.0):
        return a
    
    if (w >= 1.0):
        return b
    
    return pygame.math.lerp(a, b, w)