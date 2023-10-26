from gc import get_objects
import pygame
from opponent import Player, Monster_generator
import sys
from pygame import math as pymath
import math
from db_helper import CRUD_Player, CRUD_Monster

# à faire: créer 2 classes: Player_game et Monster_game, rassembler dans ses classes la gestion graphique de ces classes (move, attack, hp etc) pour eviter la redondance

class Game:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
        self.player:Player = Player(strength = 1, speed = 1, agility = 1, position=[Game.SCREEN_WIDTH/4, Game.SCREEN_HEIGHT/2])
        self.monster = None
        self.clock = pygame.time.Clock()
        self.game_loop = True
        self.player_time_attack = pygame.time.get_ticks()
        self.monster_time_attack = pygame.time.get_ticks()
        self.actual_hp_player = self.player.hp
        self.actual_hp_monster = None
        self.monsters:list = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Game, cls).__new__(cls)
        return cls.instance

    def __intro(self):
        self.__display_text("Hey you !\nYou are finnaly awake !")
        self.__display_text("You tried to escape the empire, right ? \nAnd they ended up capturing you.")
        self.__display_text("But there is still a way for you to get out of this.\nTo earn your release, you will have to face\n10 monsters.")
        self.__display_text("If you succeed, not only will you be alive,\nbut you will have a place in the hall of fame !")
        self.__display_text("So tell me, what is your name ?", 2000)
        self.player.name = self.__input_text()
        self.__display_text("And what are you good at ?", 2000)
        for i in range(3, 0, -1):
            self.__select_stats_up(i)
        self.__display_text(f"Strength: {self.player.strength}\nAgility: {self.player.agility}\nSpeed: {self.player.speed}")
    
    def __select_stats_up(self, pts_left = None, lvlup = False):
        font = pygame.font.Font('freesansbold.ttf', 32)
        
        X = Game.SCREEN_WIDTH
        Y = Game.SCREEN_HEIGHT
        surface = pygame.display.set_mode((X, Y))

        stats = ("Strength", "Agility", "Speed")
        stat_list = []

        select = 0

        while True:
            self.clock.tick(10)
            self.screen.fill((0, 0, 0))
            height = -32

            if pts_left != None:
                font_pts = pygame.font.Font('freesansbold.ttf', 40)
                pts_text = font_pts.render(f"Points left: {pts_left}", True, (255, 255, 255), (0, 0, 0))
                textRect = pts_text.get_rect()
                textRect.center = (X/2, Y/2 - 100)
                surface.blit(pts_text, textRect)

            for i in range(len(stats)):
                if i == select:
                    text = font.render(stats[i], True, (0, 0, 0), (255, 255, 255))
                else:
                    text = font.render(stats[i], True, (255, 255, 255), (0, 0, 0))
                stat_list.append(text)
                word_height = text.get_size()[1]
                textRect = text.get_rect()
                textRect.center = (X/2, Y/2 + height)
                surface.blit(text, textRect)
                height += word_height
            
            key = pygame.key.get_pressed()
            up = (key[pygame.K_UP] or key[pygame.K_z])
            down = (key[pygame.K_DOWN] or key[pygame.K_s])
            confirm = (key[pygame.K_SPACE] or key[pygame.K_RETURN])

            if up and select > 0:
                select -= 1
            elif down and select < 2:
                select += 1

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if confirm:
                if not lvlup:
                    if select == 0:
                        self.player.set_stats(strength=1)
                    elif select == 1:
                        self.player.set_stats(agility=1)
                    elif select == 2:
                        self.player.set_stats(speed=1)
                    return
                elif lvlup:
                    if select == 0:
                        self.player.lvlup(strength=1)
                    elif select == 1:
                        self.player.lvlup(agility=1)
                    elif select == 2:
                        self.player.lvlup(speed=1)
                    self.__display_text(f"Strength: {self.player.strength}\nAgility: {self.player.agility}\nSpeed: {self.player.speed}")
                    return

            pygame.display.update()
    
    def __display_text(self, msg:str, time:int = 4000):
        font = pygame.font.Font('freesansbold.ttf', 32)
        
        X = Game.SCREEN_WIDTH
        Y = Game.SCREEN_HEIGHT
        surface = pygame.display.set_mode((X, Y))

        msg_list = msg.split("\n")
        height = 0

        for lines in msg_list:
            text = font.render(lines, True, (255, 255, 255), (0, 0, 0))
            word_height = text.get_size()[1]
            textRect = text.get_rect()
            textRect.center = (X/2, Y/2 + height)
            surface.blit(text, textRect)
            height += word_height

        pygame.display.update()
        pygame.time.wait(time)
        
    def __input_text(self):
        X = Game.SCREEN_WIDTH
        Y = Game.SCREEN_HEIGHT
        surface = pygame.display.set_mode((X, Y))
        font = pygame.font.Font('freesansbold.ttf', 32)

        res_txt = ''
        input_rect = pygame.Rect(300, Y/2, 0, 32)
        
        loop = True
        while loop:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_BACKSPACE:
                        res_txt = res_txt[:-1]
                    elif e.key == pygame.K_RETURN:
                        loop = False
                    elif len(res_txt) <= 20:
                        res_txt += e.unicode
            surface.fill((0,0,0))
            
            pygame.draw.rect(surface, (32,32,32), input_rect)
            text_surface = font.render(res_txt, True, (255,255,255))
            surface.blit(text_surface, (input_rect.x+5, input_rect.y))
            input_rect.w = max(200, text_surface.get_width()+10)

            pygame.display.flip()

        return res_txt

    def __music_loop(self):
        pygame.mixer_music.load("./assets/music/game_intro.wav")
        music_loop = "./assets/music/game_loop.wav"
        pygame.mixer_music.play(loops=0, start=0)
        pygame.mixer.music.queue(music_loop, loops=-1)
        pygame.mixer.music.set_volume(0.5)

    def launch(self):
        pygame.init()
        self.__intro()
        while self.game_loop:
            pygame.mouse.set_visible(False)

            self.monster = Monster_generator.generate_monster(self.player.lvl)
            self.monsters.append(self.monster)
            self.actual_hp_monster = self.monster.hp

            for _ in range(9):
                self.monster.position = [3 * Game.SCREEN_WIDTH/4, Game.SCREEN_HEIGHT/2]
                self.__display_text(f"Your opponent is\n{self.monster.name} the {self.monster.type}")
                if self.__lvl_game():
                    self.__select_stats_up(1, lvlup = True)
                    self.player.lvlup()
                    self.monster = Monster_generator.generate_monster(self.player.lvl)
                    self.actual_hp_monster = self.monster.hp
                else:
                    self.__display_text("Game Over")
                    pygame.quit()
            self.__display_text("Congratulations !\nYou are now free,\nand have earned your place in the hall of fame!")
            # self.__save_hall_of_fame()

        pygame.quit()

    def __lvl_game(self):
        player_pos = [0, 0]
        monster_pos = [0, 0]
        self.__music_loop()
        run = True
        pygame.mouse.set_visible(False)

        self.actual_hp_player = self.player.hp
        self.actual_hp_monster = self.monster.hp

        player_hp_max = self.actual_hp_player
        monster_hp_max = self.actual_hp_monster

        while run:
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))
            bg = pygame.image.load("./assets/sprites/sand-background.jpg")
            background = pygame.transform.scale(bg, (Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
            self.screen.blit(background, (0, 0))

            self.__move_player(player_pos)
            self.__move_monster(monster_pos)

            self.__healthbar(player_hp_max, self.player.position, self.actual_hp_player)
            self.__healthbar(monster_hp_max, self.monster.position, self.actual_hp_monster)

            self.__display_triangle(self.player.position)

            if pygame.time.get_ticks() - self.player_time_attack >= 2000 - (self.player.atk_speed * 50):
                if pygame.mouse.get_pressed()[0]:
                    self.player_time_attack = pygame.time.get_ticks()
                    self.__attack(self.player, self.monster)
            
            if pygame.time.get_ticks() - self.monster_time_attack >= 2000 - (self.monster.atk_speed * 50):
                if self.monster.attack_check(self.player):
                    self.monster_time_attack = pygame.time.get_ticks()
                    self.__attack(self.monster, self.player)

            self.__cursor()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_SPACE:
                        self.__pause()
            
            pygame.display.update()

            if self.actual_hp_monster <= 0:
                run = False
                return True
            elif self.actual_hp_player <= 0:
                run = False
                return False

    def __cursor(self):
        pos = pygame.mouse.get_pos()
        pygame.draw.circle(self.screen, (0, 0, 0), pos, 2, 0)
    
    def __display_triangle(self, position = None, scale = 10):
        mouse_pos = pygame.mouse.get_pos()
        vMouse = pymath.Vector2(mouse_pos)
        vCenter = pymath.Vector2(position)
        angle = pymath.Vector2().angle_to(vMouse - vCenter)

        vDistance = pygame.math.Vector2(math.cos(math.radians(angle)) * 10, math.sin(math.radians(angle)) * 10)

        points = [(-0.5, -0.6), (-0.5, 0.6), (0.4, 0.0)]
        rotated_point = [pygame.math.Vector2(p).rotate(angle) for p in points]

        triangle_points = [(vCenter + p*scale + vDistance) for p in rotated_point]
        pygame.draw.polygon(self.screen, (0,0,255), triangle_points)

    # make a delay before attacking for monsters
    def __attack(self, opponent1, opponent2):
        position = (opponent1.position[0] - 15, opponent1.position[1] - 15)
        if type(opponent1) == Player:
            mouse_pos = pygame.mouse.get_pos()
            vMouse = pymath.Vector2(mouse_pos)
            vCenter = pymath.Vector2(position)
            angle = pymath.Vector2().angle_to(vMouse - vCenter)
            self.__display_attack(position, angle)

        # à modifier 
        # if type(opponent1) == Monster: (remplacer "else" par cette ligne lorsque la classe mère des monstres sera créée)
        else:
            vOpponent1 = pymath.Vector2(opponent1.position)
            vOpponent2 = pymath.Vector2(opponent2.position)
            angle = pymath.Vector2().angle_to(vOpponent2 - vOpponent1)
            self.__display_attack(position, angle)

        a = opponent1.position[0] - opponent2.position[0]
        b = opponent1.position[1] - opponent2.position[1]
        distance = math.sqrt(a**2 + b**2)

        if distance <= 40:
            self.__damage_dealing(opponent1)

        return pygame.time.get_ticks()

    def __damage_dealing(self, opponent):
        if type(opponent) == Player:
            self.actual_hp_monster -= self.player.attack
        # pareil ici, à modifier 
        # if type(opponent) == Monster: (remplacer "else" par cette ligne lorsque la classe mère des monstres sera créée)
        else:
            self.actual_hp_player -= self.monster.attack
    
    def __display_attack(self, position, angle):
        distance = pygame.math.Vector2(math.cos(math.radians(angle)) * 20, math.sin(math.radians(angle)) * 20)

        img = pygame.image.load("./assets/sprites/slash_attack.png")
        img = pygame.transform.scale(img, (30, 30))
        img = pygame.transform.rotate(img, - angle)
        slash_pos = position + distance
        self.screen.blit(img, slash_pos)

    # faire appel à self.__display_text() ici
    def __pause(self):
        pause = True
        pygame.mixer_music.pause()
        x = Game.SCREEN_WIDTH
        y = Game.SCREEN_HEIGHT
        display_surface = pygame.display.set_mode((x, y))
        pygame.display.set_caption('Show Text')
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('PAUSE', True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (x/2, y/2)

        while pause:
            display_surface.fill((0, 0, 0))
            display_surface.blit(text, textRect)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_SPACE:
                        pygame.mixer_music.unpause()
                        pause = False
            pygame.display.update()

    def __controls(self, speed, actual_direction):
        direction = actual_direction
        straight_speed = speed

        key = pygame.key.get_pressed()

        # à faire: corriger la vitesse de déplacement en diagonal (utiliser sin() et cos()?)
        # à faire: remplacer par des vecteur: pygame.math.Vector2
        left = (key[pygame.K_LEFT] or key[pygame.K_q])
        right = (key[pygame.K_RIGHT] or key[pygame.K_d])
        up = (key[pygame.K_UP] or key[pygame.K_z])
        down = (key[pygame.K_DOWN] or key[pygame.K_s])

        if left and not right and direction[0] >= -straight_speed:
            direction[0] -= straight_speed/10
        if right and not left and direction[0] <= straight_speed:
            direction[0] += straight_speed/10
        if not left and not right and not direction[0] == 0:
            if direction[0] > 0:
                direction[0] -= straight_speed/10
            elif direction[0] < 0:
                direction[0] += straight_speed/10

        if up and not down and direction[1] >= -straight_speed:
            direction[1] -= straight_speed/10
        if down and not up and direction[1] <= straight_speed:
            direction[1] += straight_speed/10
        if not up and not down and not direction[1] == 0:
            if direction[1] > 0:
                direction[1] -= straight_speed/10
            elif direction[1] < 0:
                direction[1] += straight_speed/10
        
        if (direction[0] > -0.0001 and direction[0] < 0.0001):
            direction[0] = 0
        if (direction[1] > -0.0001 and direction[1] < 0.0001):
            direction[1] = 0

        return direction
    
    # à faire: optimiser move_player et move_monster -> rassembler les 2 fonctions
    def __move_player(self, player_vector):
        player_vector = self.__controls(self.player.speed, player_vector)

        if not (self.player.position[0] <= 10 and player_vector[0] < 0) and not (self.player.position[0] >= Game.SCREEN_WIDTH - 10 and player_vector[0] > 0):
            self.player.position[0] += player_vector[0]
        if not (self.player.position[1] <= 10 and player_vector[1] < 0) and not (self.player.position[1] >= Game.SCREEN_HEIGHT - 10 and player_vector[1] > 0):
            self.player.position[1] += player_vector[1]
        pygame.draw.circle(self.screen, (0, 0, 255), self.player.position, 10, 0)
    
    def __move_monster(self, monster_vector):
        monster_vector = self.monster.move(self.player)

        if not (self.monster.position[0] <= 10 and monster_vector[0] < 0) and not (self.monster.position[0] >= Game.SCREEN_WIDTH - 10 and monster_vector[0] > 0):
            self.monster.position[0] += monster_vector[0]
        if not (self.monster.position[1] <= 10 and monster_vector[1] < 0) and not (self.monster.position[1] >= Game.SCREEN_HEIGHT - 10 and monster_vector[1] > 0):
            self.monster.position[1] += monster_vector[1]
        pygame.draw.circle(self.screen, self.monster.color, self.monster.position, 10, 0)
    
    def __healthbar(self, hp, position, actual_hp):
        pos_x = position[0] - 25
        pos_y = position[1] - 25
        ratio = actual_hp / hp

        pygame.draw.rect(self.screen, "red", (pos_x, pos_y, 50, 5))
        pygame.draw.rect(self.screen, "green", (pos_x, pos_y, 50 * ratio, 5))
    
    def __save_hall_of_fame(self):
        CRUD_Player(self.player.name, self.player.strength, self.player.agility, self.player.speed).save()
        print(CRUD_Player.player_id)
        for monster in self.monsters:
            CRUD_Monster(monster.name, monster.strength, monster.agility, monster.speed, CRUD_Player.player_id).save()

Game().launch()
