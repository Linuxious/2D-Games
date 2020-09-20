
import pygame
pygame.init()
screen = pygame.display.set_mode([800,600])
pygame.display.set_caption("Smiley Pong")
keepgoing = True
pic = pygame.image.load("Blob.bmp")
colorkey = pic.get_at((0,0))
pic.set_colorkey(colorkey)
picx = 0
picy = 0
black = (0,0,0)
white = (255,255,255)
timer = pygame.time.Clock()
speedx = 0
speedy = 0
paddlew = 200
paddleh = 25
paddlex = 300
paddley = 550
picw = 100
pich = 100
points = 0
lives = 5
font = pygame.font.SysFont("Times", 24)

while keepgoing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepgoing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                points = 0
                lives = 5
                picx = 0
                picy = 0
                speedx = 5
                speedy = 5
        picx += speedx
        picy += speedy

        if picx <= 0 or picx >= 700:
            speedx = round(-speedx * 1.1)
        if picy <= 0:
            speedy = round(-speedy * 1.1)
        if picy >= 500:
            lives -= 1
            speedy = -5
            speedx = 5
            picy = 499

        screen.fill(black)
        screen.blit(pic, (picx, picy))

        paddlex = pygame.mouse.get_pos()[0]
        paddlex -= round(paddlew/2)
        pygame.draw.rect(screen, white, (paddlex, paddley, paddlew, paddleh))

        if picy + pich >= paddley and picy + pich <= paddley + paddleh and speedy > 0:
            if picx + picw/2 >= paddlex and picx + picw/2 <= paddlex + paddlew:
                speedy = -speedy
                points += 1
        draw_string = "Lives: " + str(lives) + "Points: " + str(points)
        if lives < 1:
            speedx = speedy = 0
            draw_string = "Game Over. Your Score was: " + str(points)
            draw_string += ". Press F1 to play again. "

        text = font.render(draw_string, True, white)
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.y = 10
        screen.blit(text, text_rect)
        pygame.display.update()
        #timer.tick(60)
pygame.quit()
