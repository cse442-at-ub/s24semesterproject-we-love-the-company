from combat import Combat

from grid import Grid

# this should all be static but oh well
strike = Combat()

class EnemyManager:
    def __init__(self, grid: Grid):
        self.grid = grid
    
    def list_of_enemies(self):
        """Gets a list of all enemies in the grid."""
        return self.grid.find_object_with_properties({"name":"enemy"})
    
    def player_position(self):
        """Finds the player in the grid."""
        player_list = list(self.grid.find_object_with_properties({"name":"player"}))
        if len(player_list) != 1:
            raise Exception(f"{len(player_list)} players were found in the grid, expected 1.")
        x,y = player_list[0]
        return (x,y)
    
    def create_enemy(self,x:int,y:int,image,hitDie:str,movementDelay:int):
        """Creates an enemy on the grid."""
        """hitDie is their starting dice value for Strikes."""
        """movementDelay determines how many steps must pass before they are able to move."""
        enemy_object = {
            "name":"enemy",
            "hitDie":hitDie,
            "movementDelay":movementDelay,
            "stepsUntilMove":movementDelay,
            "obstruction":True,
            "image":image
        }
        return self.grid.insert(enemy_object,x,y)
    
    def check_obstruction(self,x:int,y:int):
        obj = self.grid.get_object(x,y)
        if obj is None:
            return False
        else:
            return obj.get("obstruction",False)
    
    def next_position(self,enemy_x,enemy_y,player_x,player_y):
        if enemy_x < player_x and not self.check_obstruction(enemy_x+1,enemy_y):
            return (enemy_x+1,enemy_y)
        elif enemy_y < player_y and not self.check_obstruction(enemy_x,enemy_y+1):
            return (enemy_x,enemy_y+1)
        elif enemy_x > player_x and not self.check_obstruction(enemy_x-1,enemy_y):
            return (enemy_x-1,enemy_y)
        elif enemy_y > player_y and not self.check_obstruction(enemy_x,enemy_y-1):
            return (enemy_x,enemy_y-1)
        else:
            return (enemy_x,enemy_y)

    def enemy_step(self):
        enemies = self.list_of_enemies()
        player_x,player_y = self.player_position()
        for enemy in enemies:
            x,y=enemy
            enemy = self.grid.get_object(x,y)
            enemy["stepsUntilMove"] -= 1
            if enemy["stepsUntilMove"] <= 0:
                enemy["stepsUntilMove"] = enemy["movementDelay"]
                new_x,new_y = self.next_position(x,y,player_x,player_y)
                if new_x != x or new_y != y:
                    self.grid.insert(enemy,new_x,new_y)
                    self.grid.remove_at_location(x,y)