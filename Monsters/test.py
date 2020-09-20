

import pygame
screen = pygame.display.set_mode([500,500])
pic = pygame.image.load("Knight.bmp")

while True:
    screen.blit(pic, (100,100))
    pygame.display.update()

