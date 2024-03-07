from combat import Combat

from grid import Grid

# this should all be static but oh well
strike = Combat()

class EnemyManager:
    def __init__(self, grid: Grid):
        self.grid = grid
    
    def list_of_enemies(self):
        return self.grid.find_object_with_properties({"name":"enemy"})
    
    def player_position(self):
        player_list = list(self.grid.find_object_with_properties({"name":"player"}))
        if len(player_list) > 1:
            raise Exception("More than 1 player was found on the grid, cannot pathfind.")
        x,y = player_list[0]
        return (x,y)
    
    def create_enemy(self,x:int,y:int,image,hitDie:str,movementDelay:int):
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
        return self.grid.get_object(x,y).get("obstruction",False)
    
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
            if enemy["stepsUntilMove"] > 0:
                enemy["stepsUntilMove"] -= 1
            else:
                new_x,new_y = self.next_position(x,y,player_x,player_y)
                if new_x != x or new_y != y:
                    self.grid.insert(enemy,new_x,new_y)
                    self.grid.remove_at_location(x,y)