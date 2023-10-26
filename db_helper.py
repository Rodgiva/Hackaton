import psycopg2

DB_NAME = "Hackaton"
USER = "postgres"
PASSWORD = "917364"
HOST = "localhost"
PORT = "5432"

try:
    connection = psycopg2.connect(
        dbname = DB_NAME,
        user = USER,
        password = PASSWORD,
        host = HOST,
        port = PORT
    )

except Exception as err:
    print(f"Error :{err}")

player_id = None

class CRUD_Player:
    player_id = None
    def __init__(self, name:str, strength:int, agility:int, speed:int) -> None:
        self.name = name
        self.strength = strength
        self.agility = agility
        self.speed = speed
    
    def save(self):
        query = f'''
        insert into Player (name, strength, agility, speed)
        values (%s, %s, %s, %s)
        '''
        cursor = connection.cursor()
        cursor.execute(query, (self.name, self.strength, self.agility, self.speed))
        CRUD_Player.player_id = cursor.lastrowid
        connection.commit()
        cursor.close()
    
    def delete(self, name):
        query = f'''
        delete from Player
        where item_name = '{name}'
        '''
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
        except Exception as err:
            print(f"Error :{err}")
            return False
        else:
            return True
    
    @staticmethod
    def get_player(id:int):
        query = f'''
        select * from Player
        where player_id = {id}
        '''
        cursor = connection.cursor()
        cursor.execute(query)
        output = cursor.fetchall()
        cursor.close()

        if len(output) == 0:
            return None

        return output
        
class CRUD_Monster:
    def __init__(self, name:str, strength:int, agility:int, speed:int, player_id:int) -> None:
        self.name = name
        self.strength = strength
        self.agility = agility
        self.speed = speed
        self.player_id = player_id
    
    def save(self):
        query = f'''
        insert into Monster (name, strength, agility, speed, player_id)
        values (%s, %s, %s, %s, %s)
        '''
        cursor = connection.cursor()
        cursor.execute(query, (self.name, self.strength, self.agility, self.speed, CRUD_Player.player_id))
        connection.commit()
        cursor.close()
    
    def delete(self, name):
        query = f'''
        delete from Monster
        where item_name = '{name}'
        '''
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
        except Exception as err:
            print(f"Error :{err}")
            return False
        else:
            return True
    
    @staticmethod
    def get_monsters_by_player(id:int):
        query = f'''
        select * from Player
        where player_id = {id}
        '''
        cursor = connection.cursor()
        cursor.execute(query)
        output = cursor.fetchall()
        cursor.close()

        if len(output) == 0:
            return None

        return output