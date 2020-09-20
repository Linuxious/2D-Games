#! /usr/bin/python3

import pygame, time, random


class Wormy:

    def __init__(self, screen):
        self.outside = (0,100,0)
        self.inside = (0,255,0)
        self.red = (255,0,0)
        self.screen = screen

    def worm2(self, worm, width, height):
        for segment in worm:
            index = worm.index(segment)
            if index == 0:
                pygame.draw.rect(self.screen, (0,0,255), (segment[0], segment[1], width, height))
                pygame.draw.rect(self.screen, (0,100,255), (segment[0] + 3, segment[1] + 3, width - 6, height - 6))
            else:
                pygame.draw.rect(self.screen, self.outside, (segment[0], segment[1], width, height))
                pygame.draw.rect(self.screen, self.inside, (segment[0] + 3, segment[1] + 3, width - 6, height - 6))

    def apple(self, x, y, width, height):
        apple = pygame.draw.rect(self.screen, self.red, (x,y,width, height))
        return apple

    def grid(self, screen_height, screen_width, speed):
        for x in range(0,screen_width, speed):
            pygame.draw.line(self.screen, (93,93,93), (x,0), (x,screen_height))
        for y in range(0,screen_height, speed):
            pygame.draw.line(self.screen, (93,93,93), (0,y), (screen_width, y))

    def score(self, size):
        score = len(size) - 3
        score = pygame.sysfont.SysFont("Helvetica", 20, bold=True).render("Score: " + str(score), True, (255,255,255))
        self.screen.blit(score, (self.screen.get_width()- 150, 10))

    def presskeytext(self):
        text = pygame.sysfont.SysFont("Helvetica", 18).render("Press a key to play.", True, (93,93,93))
        textrect = text.get_rect()
        textrect.topleft = (self.screen.get_width() - 200, self.screen.get_height() - 30)
        self.screen.blit(text, textrect)


continue_game = True
start = True

while continue_game:
    # Colors
    background = (0,0,0)
    white = (255,255,255)
    green = (0,255,0)
    dark_green = (0,100,0)

    # Initiate Game
    pygame.init()
    screen = pygame.display.set_mode([500, 500])

    # Speed
    fps = 0.1

    # Worm
    Direction = "Right"
    tail = []
    x = 100
    y = 100
    speedx = 20
    speedy = 20
    length = 0

    # Apple
    apple_posx = random.randrange(0, screen.get_width() - speedx, speedx)
    apple_posy = random.randrange(0,screen.get_height() - speedy, speedy)
    wait = 0
    size = [[x,y],[x + 1,y],[x + 2,y]]
    run_game = True
    game_over = True
    degrees_slow = 0
    degrees_fast = 0


    while start:
        screen.fill(background)
        Wormy(screen).presskeytext()
        worm_slow = pygame.sysfont.SysFont("Helvetica", 100,bold=True).render("Wormy!", True, white, dark_green)
        worm_fast = pygame.sysfont.SysFont("Helvetica", 100, bold=True).render("Wormy!", True, green)
        rotate_slow = pygame.transform.rotate(worm_slow, degrees_slow)
        rotate_fast = pygame.transform.rotate(worm_fast, degrees_fast)
        rotate_slow_rect = rotate_slow.get_rect()
        rotate_fast_rect = rotate_fast.get_rect()
        rotate_slow_rect.center = (round(screen.get_width() / 2), round(screen.get_height() / 2))
        rotate_fast_rect.center = (round(screen.get_width() / 2), round(screen.get_height() / 2))
        screen.blit(rotate_slow, rotate_slow_rect)
        screen.blit(rotate_fast, rotate_fast_rect)
        pygame.display.update()
        pygame.time.Clock().tick(20)
        degrees_slow += 3
        degrees_fast += 7
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                run_game = False
                game_over = False
                continue_game = False
            if event.type == pygame.KEYDOWN:
                start = False
    screen = pygame.display.set_mode([700,700])
    while run_game:
        screen.fill(background)
        Wormy(screen).grid(screen.get_height(), screen.get_width(), speedx)
        apple = Wormy(screen).apple(apple_posx, apple_posy, speedx, speedy)
        worm = Wormy(screen).worm2(size, speedx, speedy)
        Wormy(screen).worm2(size, speedx, speedy)
        Wormy(screen).score(size)
        check_collide = apple.collidepoint(size[0][0], size[0][1])
        if check_collide:
            length += speedx
            apple_posx = random.randrange(0, screen.get_width() - speedx, speedx)
            apple_posy = random.randrange(0, screen. get_height() - speedy, speedy)
        else:
            del size[-1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
                continue_game = False
                game_over = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if Direction != "Down":
                        Direction = "UP"
                elif event.key == pygame.K_s:
                    if Direction != "UP":
                        Direction = "Down"
                elif event.key == pygame.K_a:
                    if Direction != "Right":
                        Direction = "Left"
                elif event.key == pygame.K_d:
                    if Direction != "Left":
                        Direction = "Right"

        if x < 0 or y < 0 or x > screen.get_width() or y > screen.get_height():
            run_game = False

        if Direction == "UP":
            y -= speedy
            size.insert(0,[x,y])
        elif Direction == "Down":
            y += speedy
            size.insert(0,[x,y])
        elif Direction == "Left":
            x -= speedx
            size.insert(0,[x,y])
        elif Direction == "Right":
            x += speedy
            size.insert(0,[x,y])

        pygame.display.update()
        wait += 1
        if wait == 4:
            wait = 0
        time.sleep(fps)
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continue_game = False
                game_over = False

            if event.type == pygame.KEYDOWN:
                game_over = False

        gametext = pygame.sysfont.SysFont("Helvetica", 150, bold=True).render("Game", True, white)
        overtext = pygame.sysfont.SysFont("Helvetica", 150, bold=True).render("Over", True, white)
        game_rect = gametext.get_rect()
        over_rect = overtext.get_rect()
        game_rect.midtop = (round(screen.get_width() / 2), round(screen.get_height() / 2) - game_rect.height)
        over_rect.midtop = (round(screen.get_width() / 2), game_rect.height + 150)
        screen.blit(gametext, game_rect)
        screen.blit(overtext, over_rect)
        Wormy(screen).presskeytext()
        pygame.display.update()
        pygame.time.wait(1)
