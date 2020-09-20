import pygame
pygame.init()
screen = pygame.display.set_mode([500,500])

bullets = []
y = screen.get_height()
wait = 0

while 1:
    x = pygame.mouse.get_pos()[0]

    screen.fill((0,0,0))

    pygame.event.get()
    keys = pygame.mouse.get_pressed()
    if wait == 40:
        if keys[0] == 1:
            bullets.append([x,y])

    if len(bullets) != 0:
        for bullet in bullets:
            bullet[1] -= 1
            if bullet[1] <= 0:
                bullets.remove(bullet)
            pygame.draw.rect(screen, (255,0,0), (bullet[0], bullet[1], 5,20))
    wait += 1
    if wait > 40:
        wait = 0
    pygame.display.update()
    pygame.time.wait(5)
