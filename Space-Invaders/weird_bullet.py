import pygame, math
pygame.init()
screen = pygame.display.set_mode([500,500])
bullet_fired2 = pygame.Surface((5,20))
bullet_fired2.set_colorkey((0,0,0))
bullet_fired2.fill((255,255,255))
bullet_fired3 = bullet_fired2.copy()
bullet_fired3.set_colorkey((0,0,0))
angle = 0

bullets = []
y = screen.get_height()
x = screen.get_width() // 2
mousedown = False
count = 0
bullet_fired_rotated = bullet_fired3
rect = bullet_fired3.get_rect()

while 1:

    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousedown = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mousedown = False


    if len(bullets) != 0:
        for bullet in bullets:
            bullet[1] += math.atan(pygame.mouse.get_pos()[1] - rect.y)
            bullet[0] += math.atan(pygame.mouse.get_pos()[0] - rect.x)
    for bullet in bullets:
        if bullet[1] <= 1:
            bullets.remove(bullet)


    if mousedown:
        if count == 30:
            for bullet in bullets:
                bullet_fired_rotated = pygame.transform.rotate(bullet_fired3, math.degrees(math.atan2(pygame.mouse.get_pos()[0] - rect.x, pygame.mouse.get_pos()[1] - rect.y)))
            bullets.append([x,y])

    if len(bullets) != 0:
        for bullet in bullets:
            rect = bullet_fired3.get_rect()
            rect.center = (bullet[0], bullet[1])
            rect = bullet_fired_rotated.get_rect()
            rect.center = (bullet[0],bullet[1])
            screen.blit(bullet_fired_rotated, rect)

    count += 1
    if count > 30:
        count = 0
    angle += 1
    pygame.display.update()
    pygame.time.wait(5)




