
import pygame, random, time

""" initilize """

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode([1200,800])
menu_pic = pygame.image.load("img/battleship.jpg")
pygame.mixer.music.load("snds/battleship.mp3")
banner = pygame.image.load("img/battleship_banner.png")
menu_pic = pygame.transform.scale(menu_pic, (screen.get_width(), screen.get_height()))
font = pygame.font.Font("fonts/Battleship.ttf", 50)
end_font = pygame.font.Font("fonts/Battleship.ttf", 80)
pygame.mouse.set_cursor(*pygame.cursors.broken_x)

""" Variables """

# Players
player2_ships = {"Carrier": 5, "Battleship":4, "Cruiser":3, "Submarine":3, "Destroyer":2}
player2_health = player2_ships.copy()
player2_directions = []
player2_locations = []
second_player = font.render("2 Players", 1, (255,0,0))
button_rect_second_player = pygame.Rect(0,0,second_player.get_width() + 30,150)
button_rect_second_player.center = screen.get_width() // 2 + button_rect_second_player.width - 200, screen.get_height() // 2
second_player_rect = second_player.get_rect()
second_player_rect.center = button_rect_second_player.center

player1_ships = {"Carrier": 5, "Battleship":4, "Cruiser":3, "Submarine":3, "Destroyer":2}
player1_health = player1_ships.copy()
player1_directions = []
player1_locations = []
first_player = font.render("1 Player ", 1, (255,0,0))
button_rect_first_player = pygame.Rect(0,0,second_player.get_width() + 30,150)
button_rect_first_player.center =  screen.get_width() // 2 - button_rect_first_player.width + 200, screen.get_height() // 2
first_player_rect = first_player.get_rect()
first_player_rect.center = button_rect_first_player.center

current_player = 1
winner = None
shots = []
hits = []

# End Game
end = end_font.render("Game Over", 1, (255,0,0))
new_game = end_font.render("New Game?", 1, (255,0,0))
yes = font.render("Yes", 1, (255,0,0))
no = font.render("No", 1, (255,0,0))
button_rect_yes = pygame.Rect(0,0,yes.get_width() + 30,150)
button_rect_no = pygame.Rect(0,0,yes.get_width() + 30,150)
button_rect_yes.center =  screen.get_width() // 2 - button_rect_yes.width, screen.get_height() // 2
button_rect_no.center = screen.get_width() // 2 + button_rect_no.width, screen.get_height() // 2
yes_rect = yes.get_rect()
no_rect = no.get_rect()
yes_rect.center = button_rect_yes.center
no_rect.center = button_rect_no.center

# Game Boards
player_surface = pygame.Surface((screen.get_width() // 2 - 60, screen.get_height() - 40))
attack_surface = pygame.Surface((screen.get_width() // 2 - 60, screen.get_height() - 40))
player_rect = player_surface.get_rect()
attack_rect = attack_surface.get_rect()
player_rect.topleft = 20,20
attack_rect.topleft = screen.get_width() // 2 + 40,20

# Game
menu_break = True
battle_ship = True
game_mode = 1
directions = ["up","down","left","right"]
color = (255,255,255)
exit = font.render("Exit", 1, (255,0,0))
button_rect_exit = pygame.Rect(0,0,exit.get_width() + 30,150)
button_rect_exit.center = screen.get_height() // 2 + 200, screen.get_width() // 2
exit_rect = exit.get_rect()
exit_rect.center = button_rect_exit.center
pygame.mixer.music.play()
banner_rect = banner.get_rect()
banner_rect.center = screen.get_width() // 2, 100

""" AI """
next_shot = []
shot = (random.randrange(player_rect.x, player_rect.x + player_rect.width, 20), random.randrange(player_rect.y, player_rect.y + player_rect.height, 20))

def ai():
    global next_shot,shot,battle_ship,end_game,winner
    ai_miss = True

    if len(next_shot) != 0:
        shot = next_shot[0]
    else:
        shot = (random.randrange(player_rect.x, player_rect.x + player_rect.width, 20), random.randrange(player_rect.y, player_rect.y + player_rect.height, 20))
        while shot in shots:
            shot = (random.randrange(player_rect.x, player_rect.x + player_rect.width, 20), random.randrange(player_rect.y, player_rect.y + player_rect.height, 20))

    for ship in player1_locations:
        index = player1_locations.index(ship)
        ship_index = list(player1_ships)[index]
        if shot in ship:
            shots.append(shot)
            hits.append((255,0,0))
            player1_health[ship_index] -= 1
            if len(next_shot) == 0:
                next_shot = ship.copy()
                next_shot.remove(shot)
            else:
                del next_shot[0]
            ai_miss = False
    for health in player1_ships:
        if health in player1_health:
            index = player1_health[health]
            if index <= 0:
                del player1_health[health]
    if ai_miss:
        shots.append(shot)
        hits.append((255,255,255))
    if len(player1_health) == 0:
        print("Debug")
        winner = "Computer"
        battle_ship = False
        end_game = True

def draw_grid(surface):
    for x in range(0,surface.get_width(), 20):
        pygame.draw.line(surface, (154,154,154), (x,0),(x,surface.get_height()))
    pygame.draw.line(surface, (154,154,154), (x + 19,0),(x + 19,surface.get_height()))
    for y in range(0,surface.get_height(), 20):
        pygame.draw.line(surface, (154,154,154), (0,y),(surface.get_width(),y))
    pygame.draw.line(surface, (154,154,154), (0,y+19),(surface.get_width(),y+19))

def draw_lines(surface):
    x1 = surface.x
    y1 = surface.y
    x2 = pygame.mouse.get_pos()[0]
    y2 = pygame.mouse.get_pos()[1]
    if pygame.mouse.get_pos()[0] > surface.x + surface.width:
        x2 = surface.x + surface.width
    if pygame.mouse.get_pos()[1] > surface.y + surface.height:
        y2 = surface.y + surface.height
    if pygame.mouse.get_pos()[0] < surface.x:
        x2 = surface.x
    if pygame.mouse.get_pos()[1] < surface.y:
        y2 = surface.y
    pygame.draw.line(screen, (255,0,0), (x2, y1), (x2,y1 + surface.height), 2)
    pygame.draw.line(screen, (255,0,0), (x1, y2), (x1 + surface.width,y2), 2)


def start_game():
    player=(player1_ships, player1_locations, player_rect)
    for player_change in range(2):
        if player_change == 1:
            player=(player2_ships, player2_locations, attack_rect)
        for ship in player[0]:
            size = player[0][ship]
            direction = random.choice(directions)
            locationx = random.randrange(player[2].x + size * 20,player[2].x + player[2].width + 1 - size * 20,20)
            locationy = random.randrange(player[2].y + size * 20,player[2].y + player[2].height + 1 - size * 20,20)
            locations = []
            if len(player[1]) != 0:
                for location in player[1]:
                    for x in range(size):
                        while (locationx + x * 20 + 20,locationy) in location:
                            locationx -= size * 20 - 20
                    for x in range(size):
                        while (locationx - x * 20 - 20,locationy) in location:
                            locationx += size * 20 + 20
                    for x in range(size):
                        while (locationx,locationy + x * 20 + 20) in location:
                            locationy -= size * 20 - 20
                    for x in range(size):
                        while (locationx,locationy - x * 20 - 20) in location:
                            locationy += size * 20 + 20
            if direction == "up":
                for x in range(size):
                    locations.append((locationx, locationy + x * 20))
            elif direction == "down":
                for x in range(size):
                    locations.append((locationx, locationy - x * 20))
            elif direction == "left":
                for x in range(size):
                    locations.append((locationx - x * 20, locationy))
            elif direction == "right":
                for x in range(size):
                    locations.append((locationx + x * 20, locationy))
            player[1].append(locations)

def check_event(player=(player2_locations, player2_ships, player2_health, attack_rect)):
    global winner,current_player,battle_ship,end_game
    miss = True
    pause = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                for y in range(player[3].y,player[3].y + player[3].height, 20):
                    if y < pygame.mouse.get_pos()[1] < y + 20:
                        for x in range(player[3].x,player[3].x + player[3].width, 20):
                            if x < pygame.mouse.get_pos()[0] < x + 20:
                                if (x,y) not in shots:
                                    for ship in player[0]:
                                        index = player[0].index(ship)
                                        ship_index = list(player[1])[index]
                                        if player[0] == player1_locations:
                                            current_player = 1
                                        else:
                                            current_player = 2
                                        if (x,y) in ship:
                                            shots.append((x,y))
                                            hits.append((255,0,0))
                                            miss = False
                                            if ship_index in player[2]:
                                                player[2][ship_index] -= 1
                                    if miss:
                                        shots.append((x,y))
                                        hits.append((255,255,255))
                                        miss = False
                                    if game_mode != 1:
                                        if len(shots) != 0:
                                            for shot in shots:
                                                index = shots.index(shot)
                                                pygame.draw.rect(screen, hits[index], (shot[0] + 1,shot[1] + 1,18,18))
                                        if pause:
                                            change_player()
                                            pause = False

    print(shots)
    for health in player[1]:
        if health in player[2]:
            index = player[2][health]
            if index <= 0:
                del player[2][health]


    if len(player[2]) == 0:
        print(len(player[2]))
        if player[0] == player1_locations:
            winner = "Player 2"
        else:
            winner = "Player 1"
            print("Debug1")
        battle_ship = False
        end_game = True


def place_ships(player=(player1_locations, player1_ships, player1_health)):
    for ship in player[0]:
        index = player[0].index(ship)
        count = list(player[1])[index]
        for location in ship:
            pygame.draw.rect(screen, (0,255,0), (location[0] + 1, location[1] + 1, 18,18))

def collide(rect):
    if rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, (0,255,0), rect, 25)
        if pygame.mouse.get_pressed()[0]:
            return True

def change_player():
    pygame.mouse.set_visible(True)
    pygame.display.update()
    change = True
    switch_player = font.render("Switching Player", 1, (255,0,0))
    continue_text = font.render("Continue", 1, (255,0,0))
    button = pygame.Rect(0,0,continue_text.get_width() + 30, 150)
    continue_text_rect = continue_text.get_rect()
    button.center = screen.get_width() // 2, screen.get_height() // 2
    continue_text_rect.center = button.center
    mouseup = False
    time.sleep(0.5)
    while change:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if not pygame.mouse.get_pressed()[0]:
                mouseup = True


        screen.fill((0,0,0))
        screen.blit(continue_text, continue_text_rect)
        screen.blit(switch_player, (screen.get_width() // 2 - switch_player.get_width() // 2, 200))
        pygame.draw.rect(screen, (255,0,0), button, 10)
        if mouseup:
            if collide(button):
                change = False

        pygame.display.update()
        pygame.time.Clock().tick(10)

    screen.blit(menu_pic, (0,0))
    screen.blit(player_surface, player_rect)
    screen.blit(attack_surface, attack_rect)

end_game = False
while menu_break:
    battle_ship = False
    screen.blit(menu_pic, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.draw.rect(screen, (0,0,0), button_rect_first_player, 10)
    pygame.draw.rect(screen, (0,0,0), button_rect_second_player, 10)
    pygame.draw.rect(screen, (0,0,0), button_rect_exit, 10)

    screen.blit(first_player, first_player_rect)
    screen.blit(second_player, second_player_rect)
    screen.blit(exit, exit_rect)
    screen.blit(banner, banner_rect)

    if collide(button_rect_first_player):
        start_game()
        pygame.mixer.music.stop()
        menu_break = False
        battle_ship = True
    if collide(button_rect_second_player):
        start_game()
        pygame.mixer.music.stop()
        game_mode = 2
        menu_break = False
        battle_ship = True
    if collide(button_rect_exit):
        pygame.quit()
        quit()
        battle_ship = True

    while battle_ship:

        screen.blit(menu_pic, (0,0))
        screen.blit(player_surface, player_rect)
        screen.blit(attack_surface, attack_rect)
        #pygame.mouse.set_visible(False)
        player_surface.fill((0,0,255))
        attack_surface.fill((0,0,255))
        draw_grid(player_surface)
        draw_grid(attack_surface)

        if game_mode == 1:
            place_ships()
            if current_player == 1:
                check_event()
            else:
                ai()
                current_player = 1
        if game_mode == 2:
            if current_player == 1:
                place_ships()
                check_event()
            else:
                place_ships(player=(player2_locations, player2_ships, player2_health))
                check_event(player=(player1_locations, player1_ships, player1_health, player_rect))

        if len(shots) != 0:
            for shot in shots:
                index = shots.index(shot)
                pygame.draw.rect(screen, hits[index], (shot[0] + 1,shot[1] + 1,18,18))
        if current_player == 1:
            draw_lines(attack_rect)
        else:
            draw_lines(player_rect)
        pygame.display.update()
        pygame.time.Clock().tick(10)




    while end_game:
        pygame.mouse.set_visible(True)
        win = font.render("Winner: " + winner, 1, (255,0,0))
        screen.blit(menu_pic, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.draw.rect(screen, (0,0,0), button_rect_yes, 10)
        pygame.draw.rect(screen, (0,0,0), button_rect_no, 10)

        screen.blit(yes, yes_rect)
        screen.blit(no, no_rect)
        screen.blit(end, (screen.get_width() // 2 - end.get_width() // 2, 20))
        screen.blit(new_game, (screen.get_width() // 2 - new_game.get_width() // 2, 80))
        screen.blit(win, (screen.get_width() // 2 - win.get_width() // 2, 600))

        if collide(button_rect_yes):
            end_game = False
            menu_break = True
            battle_ship = False
            shots = []
            hits = []
            player1_health = player1_ships.copy()
            player1_directions = []
            player1_locations = []
            player2_health = player2_ships.copy()
            player2_directions = []
            player2_locations = []
            next_shot = []
            shot = (random.randrange(player_rect.x, player_rect.x + player_rect.width, 20), random.randrange(player_rect.y, player_rect.y + player_rect.height, 20))
            print(len(player2_health))
        if collide(button_rect_no):
            end_game = False
            menu_break = False
        pygame.display.update()
        pygame.time.Clock().tick(10)

    pygame.display.update()
    pygame.time.Clock().tick(10)


