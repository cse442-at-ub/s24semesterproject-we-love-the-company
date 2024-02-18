import pygame
import math

pygame.init()

screen = pygame.display.set_mode((1280, 720))
running = True

while running:


    screen.fill("gray")

    pygame.draw.circle(screen, "black", (1280 / 2, 720 / 2), ((math.sin(pygame.time.get_ticks() / 1000) + 1) / 2) * 200)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

pygame.quit()