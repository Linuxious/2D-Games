#! /usr/bin/python
import pygame, random
pygame.init()

screen = pygame.display.set_mode([1200,800])
speedx = 1
speedy = 1
player1_location = 0
player2_location = 0
player1_score = 0
player2_score = 0
speed = 1
slow = 0
ball = [round(screen.get_width() / 2), round(screen.get_height() / 2)]
game = True

while game:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game = False
    screen.fill((0,0,0))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player1_location -= speed
    if keys[pygame.K_s]:
        player1_location += speed
    if keys[pygame.K_UP]:
        player2_location -= speed
    if keys[pygame.K_DOWN]:
        player2_location += speed

    if player1_location < 0:
        player1_location += speed
    if player1_location + 30 > screen.get_height():
        player1_location -= speed
    if player2_location < 0:
        player2_location += speed
    if player2_location + 30 > screen.get_height():
        player2_location -= speed

    score_text = pygame.sysfont.SysFont("Helvetica", 50).render(str(player1_score), True, (255,255,255))
    screen.blit(score_text, (round(screen.get_width()/2) - 40 - score_text.get_rect().width,10))
    score_text = pygame.sysfont.SysFont("Helvetica", 50).render(str(player2_score), True, (255,255,255))
    screen.blit(score_text, (round(screen.get_width()/2) + 40,10))

    for y in range(0,screen.get_height(), 20):
        pygame.draw.rect(screen, (255,255,255), (round(screen.get_width() / 2),y, 1,10))
    if slow == 2:
        ball[0] += speedx
        ball[1] += speedy
    player1 = pygame.draw.rect(screen, (255,255,255), (20, player1_location, 5,30))
    player2 = pygame.draw.rect(screen, (255,255,255), (screen.get_width() - 30, player2_location, 5,30))

    if ball[0] <= 0:
        ball = [round(screen.get_width() / 2), random.randint(0,screen.get_height() - 10)]
        #speedx = -speedx
        if ball[1] >= round(screen.get_height() / 2):
            if speedy > 0:
                speedy = -speedy
        player2_score += 1
        if speedx < 0:
            speedx = -1
        else:
            speedx = 1
    if ball[0] + 10 >= screen.get_width():
        #speedx = -speedx
        ball = [round(screen.get_width()/ 2), random.randint(0,screen.get_height() - 10)]
        if ball[1] >= round(screen.get_height() / 2):
            if speedy > 0:
                speedy = -speedy
        player1_score += 1
        if speedx < 0:
            speedx = -1
        else:
            speedx = 1

    if ball[1] <= 0 or ball[1] + 10 >= screen.get_height():
        speedy = -speedy
    if player1.collidepoint(ball[0], ball[1]):
        ball[0] += 5
        speedx = -speedx
        if speedx < 0:
            speedx -= 1
        else:
            speedx += 1
    elif player1.collidepoint(ball[0], ball[1] + 10):
        ball[0] += 5
        speedx = -speedx
        if speedx < 0:
            speedx -= 1
        else:
            speedx += 1
    if player2.collidepoint(ball[0] + 10, ball[1]):
        ball[0] -= 5
        speedx = -speedx
        if speedx < 0:
            speedx -= 1
        else:
            speedx += 1
    elif player2.collidepoint(ball[0] + 10, ball[1] + 10):
        ball[0] -= 5
        speedx = -speedx
        if speedx < 0:
            speedx -= 1
        else:
            speedx += 1
    pygame.draw.rect(screen, (255,255,255), (ball[0], ball[1], 10,10))

    slow += 1
    if slow > 2:
        slow = 0

    pygame.display.update()
    pygame.time.wait(1)

pygame.quit()
