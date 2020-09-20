#! /usr/bin/python
import pygame, time, os, random, math

pygame.init()

class Maps:

    def __init__(self, screen, map_number, number_monster):
        self.screen = screen
        self.map_number = 6 - map_number
        self.numberofmonsters = number_monster


    def draw_map(self):
        self.maps = list(os.listdir("Pics/Backgrounds/"))
        self.ground = pygame.image.load("Pics/Backgrounds/" + self.maps[self.map_number])
        self.ground = pygame.transform.scale(self.ground, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(self.ground, (0,0))
        return self.numberofmonsters


class Monster(pygame.sprite.Sprite):
    pos = (0,0)
    xvel = 1
    yvel = 1
    scale = 100
    def __init__(self, pos, pic, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pic
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.x = round(pos[0] - self.scale/2)
        self.rect.y = round(pos[1] - self.scale/2)
        self.screen = screen

    def update(self,knight_pos, knight_size, invisable, monsterlist):
        if knight_pos[0] > self.rect.x:
            if invisable == False:
                self.rect.x += 1
                check_collide = 0
                while check_collide != self.rect.width:
                    if self.rect.collidepoint(knight_pos[0], knight_pos[1] + check_collide):
                        self.rect.x -= 1
                        Main.health -= 1
                    check_collide += 1

        if knight_pos[0] < self.rect.x:
            if invisable == False:
                self.rect.x -= 1
                check_collide = 0
                while check_collide != self.rect.height:
                    if self.rect.collidepoint(knight_pos[0] + knight_size[0],knight_pos[1] + check_collide):
                        self.rect.x -= 1
                        Main.health -= 1
                    check_collide += 1

        if knight_pos[1] > self.rect.y:
            if invisable == False:
                self.rect.y += 1
                check_collide = 0
                while check_collide != self.rect.height:
                    if self.rect.collidepoint(knight_pos[0] + check_collide, knight_pos[1]):
                        self.rect.y -= 1
                        Main.health -= 1
                    check_collide += 1

        if knight_pos[1] < self.rect.y:
            if invisable == False:
                self.rect.y -= 1
                check_collide = 0
                while check_collide != self.rect.height:
                    if self.rect.collidepoint(knight_pos[0] + check_collide, knight_pos[1] + knight_size[1]):
                        self.rect.y += 1
                        Main.health -= 1
                    check_collide += 1

class Main:

    colors = {"white": (225,225,225)}
    pics = list(os.listdir("Pics/People"))
    monsters = {}
    strength = 1
    monster_health = 1
    health = 100
    for pic in pics:
        monsters.update({pic: {"strength": strength, "monster_health": monster_health}})
        strength += 1
        monster_health += 1

    def __init__(self):
        self.numberofmap = 1
        self.map_level = 4
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.set_mode([1600,900])
        pygame.display.set_caption("Battle Royale!")
        self.monstersonboard = pygame.sprite.Group()
        self.knight = self.loadify("Pics/People/Knight.png")
        self.enemy = self.loadify("Pics/People/Orc.png")
        self.invisable_knight = self.loadify("Pics/People/Invisable_Knight.png")
        self.knightx = 0 + self.knight.get_rect().x
        self.knighty = 0 + self.knight.get_rect().y
        self.invisable = 500
        self.monsters_left = 0
        texts = ["Health:", "Invisability:", "Monsters:"]
        font = pygame.sysfont.SysFont("Helvetica", 20, bold=True)
        self.font = font
        self.text1 = font.render(texts[0], True, self.colors["white"])
        self.text2 = font.render(texts[1], True, self.colors["white"])
        self.text3 = font.render(texts[2], True, self.colors["white"])
        self.text4 = font.render(str(self.health), True, self.colors["white"])
        self.text5 = font.render(str(self.invisable), True, self.colors["white"])
        self.text6 = font.render(str(self.monsters_left), True, self.colors["white"])

    def main(self):
        run_game = True
        while run_game:
            keep_going = True
            stay_invisable = False
            no_invisable = False
            pause_game = True
            count = 0
            number = Maps(self.screen, self.numberofmap, self.map_level).draw_map()
            stop1 = self.screen.get_width() - self.knight.get_width()
            stop2 = self.screen.get_height() - self.knight.get_height()
            while keep_going:
                self.text4 = self.font.render(str(self.health), True, self.colors["white"])
                self.text5 = self.font.render(str(self.invisable), True, self.colors["white"])
                self.text6 = self.font.render(str(self.monsters_left), True, self.colors["white"])
                keys = pygame.key.get_pressed()

                if keys[pygame.K_SPACE]:
                    self.invisable -= 1
                    no_invisable = False
                    stay_invisable = True
                if keys[pygame.K_LSUPER] and keys[pygame.K_LSHIFT] and keys[pygame.K_q]:
                    keep_going = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        keep_going = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_F5:
                            keep_going = False
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_SPACE:
                            stay_invisable = False
                            no_invisable = True

                if  keys[pygame.K_w]:
                    self.knighty -= 5
                    if stay_invisable == False:
                        check_collide = 0
                        while check_collide != self.knight.get_height():
                            for monster in self.monstersonboard:
                                if monster.rect.collidepoint(self.knightx + check_collide, self.knighty):
                                    self.knighty += 5
                            check_collide += 1
                if keys[pygame.K_s]:
                    self.knighty += 5
                    if stay_invisable == False:
                        check_collide = 0
                        while check_collide != self.knight.get_height():
                            for monster in self.monstersonboard:
                                if monster.rect.collidepoint(self.knightx + check_collide, self.knighty + self.knight.get_height()):
                                    self.knighty -= 5
                            check_collide += 1
                if keys[pygame.K_a]:
                    self.knightx -= 5
                    if stay_invisable == False:
                        check_collide = 0
                        while check_collide != self.knight.get_width():
                            for monster in self.monstersonboard:
                                if monster.rect.collidepoint(self.knightx, self.knighty + check_collide):
                                    self.knightx += 5
                            check_collide += 1
                if keys[pygame.K_d]:
                    self.knightx += 5
                    if stay_invisable == False:
                        check_collide = 0
                        while check_collide != self.knight.get_width():
                            for monster in self.monstersonboard:
                                if monster.rect.collidepoint(self.knightx + self.knight.get_width(), self.knighty + check_collide):
                                    self.knightx -= 5
                            check_collide += 1
                if self.invisable == 0:
                    no_invisable = True
                    stay_invisable = False
                if no_invisable == True:
                    stay_invisable = False
                    self.invisable += 1
                    if self.invisable == 500:
                        no_invisable = False
                Maps(self.screen, self.numberofmap, self.map_level).draw_map()
                self.screen.blit(self.text1, (5,5))
                self.screen.blit(self.text2, (5,25))
                self.screen.blit(self.text3, (5,45))
                self.screen.blit(self.text4, (self.text1.get_rect().right + 5,5))
                self.screen.blit(self.text5, (self.text2.get_rect().right + 5,25))
                self.screen.blit(self.text6, (self.text3.get_rect().right + 5,45))

                if self.knightx <= 0:
                    self.knightx = 0 + self.knight.get_rect().x
                if self.knightx >= stop1:
                    self.knightx = stop1
                if self.knighty <= 0:
                    self.knighty = 0 + self.knight.get_rect().y
                if self.knighty >= stop2:
                    self.knighty = stop2


                if stay_invisable == False:
                    self.screen.blit(self.knight, (self.knightx,self.knighty))
                else:
                    self.screen.blit(self.invisable_knight, (self.knightx,self.knighty))

                self.monstersonboard.draw(self.screen)
                if count == 20:
                    self.monstersonboard.update((self.knightx, self.knighty), (self.knight.get_width(), self.knight.get_height()), stay_invisable, self.monstersonboard)
                    count = 0


                while number != 0:
                    beginx = 0 + self.enemy.get_width()
                    endx = self.screen.get_width() - self.enemy.get_width()
                    beginy = 0 + self.enemy.get_height()
                    endy = self.screen.get_height() - self.enemy.get_height()
                    x = random.randint(beginx,endx)
                    y = random.randint(beginy,endy)
                    if len(self.monstersonboard) == 0:
                        monster = Monster((x,y), self.enemy, self.screen)
                        self.monstersonboard.add(monster)
                    for monster in self.monstersonboard:
                        if monster.rect.collidepoint(self.knight.get_rect().topleft[0], self.knight.get_rect().topleft[1]):
                            x = random.randrange(beginx,endx)
                            y = random.randrange(beginy,endy)
                            self.monstersonboard.remove(monster)
                            number += 1
                        elif monster.rect.collidepoint(self.knight.get_rect().bottomleft[0], self.knight.get_rect().bottomleft[1]):
                            x = random.randrange(beginx,endx)
                            y = random.randrange(beginy,endy)
                            self.monstersonboard.remove(monster)
                            number += 1
                        elif monster.rect.collidepoint(self.knight.get_rect().bottomright[0], self.knight.get_rect().bottomright[1]):
                            x = random.randrange(beginx,endx)
                            y = random.randrange(beginy,endy)
                            self.monstersonboard.remove(monster)
                            number += 1
                        if len(self.monstersonboard) < Maps(self.screen, 2, self.map_level).numberofmonsters:
                            newMonster = Monster((x,y), self.enemy, self.screen)
                            self.monstersonboard.add(newMonster)
                        else:
                            for monster_check in self.monstersonboard:
                                if monster == monster_check:
                                    continue
                                else:
                                    if monster_check.rect.collidepoint(monster.rect.topleft[0], monster.rect.topleft[1]):
                                        x = random.randrange(beginx,endx)
                                        y = random.randrange(beginy,endy)
                                        self.monstersonboard.remove(monster)
                                        number += 1
                                    elif monster_check.rect.collidepoint(monster.rect.topright[0], monster.rect.topright[1]):
                                        x = random.randrange(beginx,endx)
                                        y = random.randrange(beginy,endy)
                                        self.monstersonboard.remove(monster)
                                        number += 1
                                    elif monster_check.rect.collidepoint(monster.rect.bottomleft[0], monster.rect.bottomleft[1]):
                                        x = random.randrange(beginx,endx)
                                        y = random.randrange(beginy,endy)
                                        self.monstersonboard.remove(monster)
                                        number += 1
                                    elif monster_check.rect.collidepoint(monster.rect.bottomright[0], monster.rect.bottomright[1]):
                                        x = random.randrange(beginx,endx)
                                        y = random.randrange(beginy,endy)
                                        self.monstersonboard.remove(monster)
                                if len(self.monstersonboard) < Maps(self.screen, 2, self.map_level).numberofmonsters:
                                    newMonster = Monster((x,y), self.enemy, self.screen)
                                    self.monstersonboard.add(newMonster)

                    number -= 1
                count += 1


                pygame.display.update()

            while pause_game:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pause_game = False
                        run_game = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_F5:
                            pause_game = False

                gametext = pygame.sysfont.SysFont("Helvetica", 150, bold=True).render("Game", True, (255,255,255))
                pausedtext = pygame.sysfont.SysFont("Helvetica", 150, bold=True).render("Paused", True, (255,255,255))
                game_rect = gametext.get_rect()
                paused_rect = pausedtext.get_rect()
                game_rect.midtop = (round(self.screen.get_width() / 2), round(self.screen.get_height() / 2) - game_rect.height)
                paused_rect.midtop = (round(self.screen.get_width() / 2), game_rect.height + paused_rect.height + 35)
                self.screen.blit(gametext, game_rect)
                self.screen.blit(pausedtext, paused_rect)
                pygame.display.update()

        pygame.quit()
        quit()


    def loadify(self, imgname):
        return pygame.image.load(imgname).convert_alpha()

class Start:

    def __init__(self):
        self.screen = pygame.display.set_mode([800,800])
        pygame.display.set_caption("Battle Royale!")
        pic = pygame.image.load("Pics/Backgrounds/Title.png")
        self.pic = pygame.transform.scale(pic, (self.screen.get_width(), self.screen.get_height()))
        self.knight = pygame.image.load("Pics/People/Title_Knight.png")
        self.orc = pygame.image.load("Pics/People/Title_Orc.png")
        texts = ["Battle Royal!", "Press Enter To Start!"]
        font = pygame.sysfont.SysFont("Helvetica", 50, bold=True, italic=True)
        self.text1 = font.render(texts[0], True, (255,0,0))
        self.text2 = font.render(texts[1], True, (255,0,0))
        self.text2switch = font.render(texts[1], True, (0,255,0))

    def init(self):
        keep_going = True
        x = 0
        y = True
        switchcount = 0
        switch = True
        text_change = [self.text2switch, ((round(self.screen.get_width()/2))-self.text2.get_rect().centerx,round(self.screen.get_height()-80))]
        while keep_going:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keep_going = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        keep_going = False
                        Main().main()
            if switch == True and 0 < switchcount == 55:
                text_change = [self.text2, ((round(self.screen.get_width()/2))-self.text2.get_rect().centerx,round(self.screen.get_height()-80))]
                switch = False
                if switchcount == 55:
                    switchcount = 0
            elif switch == False and 0 > switchcount == -55:
                text_change = [self.text2switch, ((round(self.screen.get_width()/2))-self.text2.get_rect().centerx,round(self.screen.get_height()-80))]
                switch = True
                if switchcount == -55:
                    switchcount = 0
            if switch == True:
                switchcount += 1
            elif switch == False:
                switchcount -= 1

            if y == True:
                x -= 1
                if x == -20:
                    y = False
            elif y == False:
                x += 1
                if x == 20:
                    y = True
            self.screen.blit(self.pic, (0,0))
            self.screen.blit(self.knight, (500,300))
            self.screen.blit(self.orc, (50,300))
            self.screen.blit(self.text1, ((round(self.screen.get_width()/2))-self.text1.get_rect().centerx,round(self.screen.get_height()/20)+x))
            self.screen.blit(text_change[0], text_change[1])
            time.sleep(0.01)


            pygame.display.update()
        pygame.quit()

Start().init()
