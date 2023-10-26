from random import randint
import requests
import math

class Opponent:
    def __init__(self, name = "Bob", strength = 1, speed = 1, agility = 1, lvl = 1) -> None:
        # stats
        self.__name : str = name
        self.__strength : int = strength
        self.__speed : int = speed
        self.__agility : int = agility
        self.__lvl : int = lvl
        # attributes
        self.__hp : int = (self.strength * 20) + 100
        self.__attack : int = (self.strength * 6) + (self.agility * 2)
        self.__atk_speed : int = (self.agility * 3) + self.speed
        # position
        self.position: list= [0,0]

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def strength(self):
        return self.__strength
    
    @strength.setter
    def strength(self, strength):
        self.__strength = strength

    @property
    def speed(self):
        return self.__speed
    
    @speed.setter
    def speed(self, speed):
        self.__speed = speed
    
    @property
    def agility(self):
        return self.__agility
    
    @agility.setter
    def agility(self, agility):
        self.__agility = agility
    
    @property
    def lvl(self):
        return self.__lvl
    
    @lvl.setter
    def lvl(self, lvl):
        self.__lvl = lvl

    @property
    def hp(self):
        return self.__hp
    
    @hp.setter
    def hp(self, hp):
        self.__hp = hp
    
    @property
    def attack(self):
        return self.__attack
    
    @attack.setter
    def attack(self, attack):
        self.__attack = attack
    
    @property
    def atk_speed(self):
        return self.__atk_speed
    
    @atk_speed.setter
    def atk_speed(self, atk_speed):
        self.__atk_speed = atk_speed
    
    def set_stats(self, strength = 0, speed = 0, agility = 0):
        self.strength += strength
        self.speed += speed
        self.agility += agility
        self._set_attributes()
    
    def _set_attributes(self):
        self.hp = (self.strength * 20) + 100
        self.attack = (self.strength * 10) + (self.agility * 2)
        self.atk_speed = (self.agility * 3) + self.speed
    
    def __str__(self) -> str:
        return f"\nname: {self.name}\nstrength: {self.strength}\nspeed: {self.speed}\nagility: {self.agility}\n\nlvl: {self.lvl}\nhp: {self.hp}\nattack: {self.attack}\nattack speed: {self.atk_speed}\n"

class Player(Opponent):
    def __init__(self, name="Bob", strength=1, speed=1, agility=1, position=[0, 0]) -> None:
        super().__init__(name, strength, speed, agility)
        self.position = position
    
    # implementation of a singleton
    def __new__(cls, name="Bob", strength=1, speed=1, agility=1, position=[100,100]):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Player, cls).__new__(cls)
        return cls.instance
    
    def lvlup(self, strength=0, speed=0, agility=0):
        self.lvl += 1
        self.set_stats(strength, speed, agility)

class Monster_generator:
    monsters = ["troll", "orc", "goatmen", "goblin", "skeleton"]

    @staticmethod
    def generate_monster(lvl):
        monster = Monster_generator.monsters[randint(0,len(Monster_generator.monsters)-1)]
        # match monster:
        match monster:
            case "troll":
                return Troll(lvl=lvl)
            case "orc":
                return Orc(lvl=lvl)
            case "goatmen":
                return Goatmen(lvl=lvl)
            case "goblin":
                return Goblin(lvl=lvl)
            case "skeleton":
                return Skeleton(lvl=lvl)
    
    @staticmethod
    def get_monster_name(type_monster):
        url = "http://monsternames-api.com/api/v1.0/" + type_monster
        try:
            res = requests.get(url)
            return res.json()["fullName"]
        except Exception as err:
            print(err)
            return "Bob Razowski"
    
# à faire: possibilité de factoriser le code: créer une classe Monster (non static)
#   -> remplacer la classe monster actuelle par la nouvelle
#   -> renommer l'actuelle par Monster_generator
# éléments redondants: assign_stats(), déclaration du type dans init
# concernant les mouvements des monsters: ajouter une acceleration comme au player

class Monster(Opponent):
    def __init__(self, name="Bob Razowski", base_strength = 0, base_agility = 0, base_speed = 0, type = "monster") -> None:
        self.__base_strength = base_strength
        self.__base_agility = base_agility
        self.__base_speed = base_speed
        super().__init__(name, self.__base_strength, self.__base_speed, self.__base_agility)

class Troll(Monster):
    def __init__(self, name="Bob Razowski", lvl=1) -> None:
        self.__base_strength = 4
        self.__base_agility = 1
        self.__base_speed = 1
        self.type = "Troll"
        self.color = (63, 63, 63)

        super().__init__(name, self.__base_strength, self.__base_speed, self.__base_agility, lvl)
        self.name = Monster_generator.get_monster_name("troll")
        self.assign_stats()

    def assign_stats(self):
        # 2/3 chance to set strength
        # 1/6 chance to set agilily
        # 1/6 chance to set speed
        for _ in range(self.lvl):
            rand = randint(1,6)
            if rand > 2:
                self.strength += 1
            elif rand == 1:
                self.agility += 1
            elif rand == 2:
                self.speed += 1
            self._set_attributes()
    
    def move(self, player:Player):
        a = player.position[0] - self.position[0]
        b = player.position[1] - self.position[1]

        distance = math.sqrt(a**2 + b**2)
        
        if a == 0 or b == 0 or distance <= 20:
            return [0,0]

        angle = math.atan(a/b)
        direction_x = math.cos(angle)*self.speed
        direction_y = math.sin(angle)*self.speed
        if b < 0:
            direction_x = -direction_x
            direction_y = -direction_y

        direction = [direction_y, direction_x]
        return direction
    
    def attack_check(self, player:Player):
        a = player.position[0] - self.position[0]
        b = player.position[1] - self.position[1]

        distance = math.sqrt(a**2 + b**2)
        if distance < 35:
            return True
        return False

class Orc(Monster):    
    def __init__(self, name="Bob Razowski", lvl=1) -> None:
        self.__base_strength = 3
        self.__base_agility = 1
        self.__base_speed = 2
        self.type = "Orc"
        self.color = (0, 63, 0)

        super().__init__(name, self.__base_strength, self.__base_speed, self.__base_agility, lvl)
        self.name = Monster_generator.get_monster_name("orc")
        self.assign_stats()

    def assign_stats(self):
        # 1/2 chance to set strength
        # 1/6 chance to set agilily
        # 1/3 chance to set speed
        for _ in range(self.lvl):
            rand = randint(1,6)
            if rand > 3:
                self.strength += 1
            elif rand == 1:
                self.agility += 1
            elif rand > 1:
                self.speed += 1
            self._set_attributes()

    def move(self, player:Player):
        a = player.position[0] - self.position[0]
        b = player.position[1] - self.position[1]

        distance = math.sqrt(a**2 + b**2)
        
        if a == 0 or b == 0 or (distance >= 35 and distance <= 40):
            return [0,0]

        angle = math.atan(a/b)
        direction_x = math.cos(angle)*self.speed
        direction_y = math.sin(angle)*self.speed
        if b < 0:
            direction_x = -direction_x
            direction_y = -direction_y

        if distance < 35:
            direction = [-direction_y, -direction_x]
        else:
            direction = [direction_y, direction_x]
        return direction
        
    def attack_check(self, player:Player):
        a = player.position[0] - self.position[0]
        b = player.position[1] - self.position[1]

        distance = math.sqrt(a**2 + b**2)
        if distance < 35:
            return True
        return False

class Goatmen(Monster):
    def __init__(self, name="Bob Razowski", lvl=1) -> None:
        self.__base_strength = 2
        self.__base_agility = 2
        self.__base_speed = 2
        self.type = "Goatmen"
        self.color = (95, 63, 0)

        super().__init__(name, self.__base_strength, self.__base_speed, self.__base_agility, lvl)
        self.name = Monster_generator.get_monster_name("goatmen")
        self.assign_stats()

    def assign_stats(self):
        # 1/3 chance to set strength
        # 1/3 chance to set agilily
        # 1/3 chance to set speed
        for _ in range(self.lvl):
            rand = randint(1,6)
            if rand >= 5:
                self.strength += 1
            elif rand >= 3:
                self.agility += 1
            elif rand >= 1:
                self.speed += 1
            self._set_attributes()

    def move(self, player:Player):
        a = player.position[0] - self.position[0]
        b = player.position[1] - self.position[1]

        distance = math.sqrt(a**2 + b**2)
        
        if a == 0 or b == 0 or (distance >= 75 and distance <= 80):
            return [0,0]

        angle = math.atan(a/b)
        direction_x = math.cos(angle)*self.speed
        direction_y = math.sin(angle)*self.speed
        if b < 0:
            direction_x = -direction_x
            direction_y = -direction_y

        if distance < 35:
            direction = [-direction_y, -direction_x]
        else:
            direction = [direction_y, direction_x]
        return direction

    def attack_check(self, player:Player):
        a = player.position[0] - self.position[0]
        b = player.position[1] - self.position[1]

        distance = math.sqrt(a**2 + b**2)
        if distance < 35:
            return True
        return False

class Goblin(Monster):
    def __init__(self, name="Bob Razowski", lvl=1) -> None:
        self.__base_strength = 1
        self.__base_agility = 3
        self.__base_speed = 2
        self.type = "Goblin"
        self.color = (0, 191, 0)

        super().__init__(name, self.__base_strength, self.__base_speed, self.__base_agility, lvl)
        self.name = Monster_generator.get_monster_name("goblin")
        self.assign_stats()

    def assign_stats(self):
        # 1/6 chance to set strength
        # 1/2 chance to set agilily
        # 1/3 chance to set speed
        for _ in range(self.lvl):
            rand = randint(1,6)
            if rand == 1:
                self.strength += 1
            elif rand <= 4:
                self.agility += 1
            elif rand > 4:
                self.speed += 1
            self._set_attributes()

    def move(self, player:Player):
        a = player.position[0] - self.position[0]
        b = player.position[1] - self.position[1]

        distance = math.sqrt(a**2 + b**2)
        
        if a == 0 or b == 0 or (distance >= 100 and distance <= 105):
            return [0,0]

        angle = math.atan(a/b)
        direction_x = math.cos(angle)*self.speed
        direction_y = math.sin(angle)*self.speed
        if b < 0:
            direction_x = -direction_x
            direction_y = -direction_y

        if distance < 35:
            direction = [-direction_y, -direction_x]
        else:
            direction = [direction_y, direction_x]
        return direction
    
    def attack_check(self, player:Player):
        a = player.position[0] - self.position[0]
        b = player.position[1] - self.position[1]

        distance = math.sqrt(a**2 + b**2)
        if distance < 35:
            return True
        return False
    
class Skeleton(Monster):
    def __init__(self, name="Bob Razowski", lvl=1) -> None:
        self.__base_strength = 1
        self.__base_agility = 2
        self.__base_speed = 3
        self.type = "Skeleton"
        self.color = (127, 127, 127)

        super().__init__(name, self.__base_strength, self.__base_speed, self.__base_agility, lvl)
        self.name = Monster_generator.get_monster_name("skeleton")
        self.assign_stats()

    def assign_stats(self):
        # 1/6 chance to set strength
        # 1/3 chance to set agilily
        # 1/2 chance to set speed
        for _ in range(self.lvl):
            rand = randint(1,6)
            if rand == 1:
                self.strength += 1
            elif rand <= 3:
                self.agility += 1
            elif rand > 3:
                self.speed += 1
            self._set_attributes()
    
    def move(self, player:Player):
        a = player.position[0] - self.position[0]
        b = player.position[1] - self.position[1]

        distance = math.sqrt(a**2 + b**2)
        
        if a == 0 or b == 0 or (distance >= 150 and distance <= 155):
            return [0,0]

        angle = math.atan(a/b)
        direction_x = math.cos(angle)*self.speed
        direction_y = math.sin(angle)*self.speed
        if b < 0:
            direction_x = -direction_x
            direction_y = -direction_y

        if distance < 35:
            direction = [-direction_y, -direction_x]
        else:
            direction = [direction_y, direction_x]
        return direction
    
    def attack_check(self, player:Player):
        a = player.position[0] - self.position[0]
        b = player.position[1] - self.position[1]

        distance = math.sqrt(a**2 + b**2)
        if distance < 35:
            return True
        return False