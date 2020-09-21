#! /usr/bin/python
import pygame, os, random
pygame.init()
screen = pygame.display.set_mode([900,900])

class Invader(pygame.sprite.Sprite):

        invaders = os.listdir("Pics/Invaders")
        image = pygame.image.load("Pics/Invaders/" + random.choice(invaders)).convert_alpha()


        def __init__(self, pos, screen):
            pygame.sprite.Sprite.__init__(self)
            self.rect = self.image.get_rect()
            self.rect.x = pos[0]
            self.rect.y = pos[1]
            self.count = 0
            self.screen = screen

        def update(self, change, change2):
            if change:
                self.rect.x += 1
            if change == False:
                self.rect.x -= 1
            if change2:
                self.rect.y += 10

class Main:

    def __init__(self, screen):
        self.screen = screen
        self.screen.fill((0,0,0))
        pygame.display.update()
        self.building = self.loadify("Pics/Building.png")
        self.turret = self.loadify("Pics/Turret.png")
        self.invaders = pygame.sprite.Group()
        self.numberofinvaders = 5
        self.numberofinvaderrows = 1
        self.level = 1
        self.invader_healths = []
        self.invader_health = 100
        self.buildings = []
        self.numberofbuildings = 4
        self.building_health = [100,100,100,100]
        self.bullet_strength = 10
        self.invader_strength = 10

    def game_over(self):
        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = False
                    else:
                        Start().main()

            self.screen.fill((0,0,0))

            game_text = pygame.sysfont.SysFont("Helvetica", 40, bold=True).render("Game", True, (255,0,0))
            over_text = pygame.sysfont.SysFont("Helvetica", 40, bold=True).render("Over", True, (255,0,0))
            game_rect = game_text.get_rect()
            over_rect = over_text.get_rect()

            game_rect.midtop = (round(self.screen.get_width() / 2), round(self.screen.get_height() / 2) - game_rect.height)
            over_rect.midtop = (round(self.screen.get_width() / 2), round(self.screen.get_width() / 2) - game_rect.height + over_rect.height + 35)

            self.screen.blit(game_text, (game_rect))
            self.screen.blit(over_text, (over_rect))
            pygame.display.update()
        pygame.quit()
        quit()

    def game_paused(self):
        pause_game = True
        while pause_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pause_game = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F5:
                        pause_game = False

            game_text = pygame.sysfont.SysFont("Helvetica", 40, bold=True).render("Game", True, (255,255,255))
            paused_text = pygame.sysfont.SysFont("Helvetica", 40, bold=True).render("Paused", True, (255,255,255))
            game_rect = game_text.get_rect()
            paused_rect = paused_text.get_rect()

            game_rect.midtop = (round(self.screen.get_width() / 2), round(self.screen.get_height() / 2) - game_rect.height)
            paused_rect.midtop = (round(self.screen.get_width() / 2), round(self.screen.get_width() / 2) - game_rect.height + paused_rect.height + 35)

            self.screen.blit(game_text, (game_rect))
            self.screen.blit(paused_text, (paused_rect))
            pygame.display.update()


    def main(self):
        continue_game = True

        while continue_game:
            run_game = True
            mousedown = False
            change = True
            change2 = False
            first = True
            wait = 0
            bullets = []

            while run_game:
                self.screen.fill((0,0,0))
                turret_pos = pygame.mouse.get_pos()
                y = self.screen.get_height() - self.turret.get_rect().height

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run_game = False
                        continue_game = False
                        pause_game = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mousedown = True
                    if event.type == pygame.MOUSEBUTTONUP:
                        mousedown = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_F5:
                            self.game_paused()
                        if event.key == pygame.K_ESCAPE:
                            run_game = False
                            pause_game = False
                            continue_game = False

                keys = pygame.mouse.get_pressed()
                if wait == 5:
                    if keys[0] == 1:
                        bullets.append([turret_pos[0] + self.turret.get_width() // 2,y])
                if len(bullets) != 0:
                    for bullet in bullets:
                        bullet[1] -= 5
                        if bullet[1] <= 0:
                            bullets.remove(bullet)
                        pygame.draw.rect(screen, (255,0,0), (bullet[0], bullet[1], 3,9))
                wait += 1
                if wait > 5:
                    wait = 0

                if first:
                    for x in range(0 + round(self.screen.get_width()/14), self.screen.get_width(), round(self.screen.get_width()/self.numberofbuildings)):
                        building = self.screen.blit(self.building, (x, 750))
                        self.buildings.append(building)
                    first = False
                else:
                    for building in self.buildings:
                        self.screen.blit(self.building, (building))
                self.screen.blit(self.turret, (turret_pos[0], y))
                for invader in self.invaders:
                    if invader.rect.x <= 0:
                        change = True
                        change2 = True
                    if invader.rect.x >= self.screen.get_width() - invader.rect.width:
                        change = False
                        change2 = True
                self.invaders.update(change, change2)
                self.invaders.draw(self.screen)
                change2 = False
                row = 0
                while self.numberofinvaderrows != 0:
                    for x in range(0,self.screen.get_width(), round(self.screen.get_width() / self.numberofinvaders)):
                        newInvader = Invader((x,0 - row), self.screen)
                        self.invaders.add(newInvader)
                        self.invader_healths.append(self.invader_health)
                    self.numberofinvaderrows -= 1
                    row += 104

                for bullet in bullets:
                    for invader in self.invaders:
                        check_collide = 0
                        while check_collide != 3:
                            if invader.rect.collidepoint(bullet[0] + check_collide, bullet[1]):
                                bullets.remove(bullet)
                                index = list(self.invaders).index(invader)
                                self.invader_healths[index] -= self.bullet_strength
                                invader_health = self.invader_healths[index]
                                check_collide = 2
                            check_collide += 1
                for invader_health in self.invader_healths:
                    if invader_health <= 0:
                        index = self.invader_healths.index(invader_health)
                        invader = list(self.invaders)[index]
                        self.invaders.remove(invader)
                        self.invader_healths.remove(invader_health)
                for building in self.buildings:
                    for invader in self.invaders:
                        check_collide = 0
                        while check_collide != invader.rect.width:
                            if building.collidepoint(invader.rect.x + check_collide, invader.rect.y + invader.rect.height):
                                index = self.buildings.index(building)
                                self.building_health[index] -= self.invader_strength
                            check_collide += 1
                for building_health in self.building_health:
                    if building_health <= 0:
                        index = self.building_health.index(building_health)
                        self.numberofbuildings -= 1
                        self.building_health.remove(building_health)
                        del self.buildings[index]

                if len(self.building_health) == 0:
                    self.game_over()
                if len(list(self.invaders)) == 0:
                    self.level += 1
                    self.numberofinvaderrows = self.level
                    if self.level == 3:
                        self.invader_health *= 2
                pygame.time.Clock().tick(180)
                pygame.display.update()

    def loadify(self,image):
        return pygame.image.load(image).convert_alpha()





class Start():

    def __init__(self):
        self.screen = pygame.display.set_mode([900,900])
        self.logo = pygame.image.load("Pics/SpaceInvaders.png")
        self.text = pygame.sysfont.SysFont("Helvetica", 40, bold=True).render("Press Enter To Start!", True, (255,255,0))

    def main(self):
        start = True
        while start:
            self.screen.fill((0,0,0))
            logo_rect = self.logo.get_rect()
            logo_rect.midtop = (int(self.screen.get_width() / 2), 0)
            self.screen.blit(self.logo, logo_rect)
            text_rect = self.text.get_rect()
            text_rect.midtop = (int(self.screen.get_width() / 2), 500)
            self.screen.blit(self.text, (text_rect))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        start = False
                        Main(self.screen).main()
                    if event.key == pygame.K_ESCAPE:
                        start = False

        pygame.quit()

if __name__ == "__main__":
    Start().main()
