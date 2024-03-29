from combat import Combat
from random import choice

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
            "image":image,
            "path":[]
        }
        return self.grid.insert(enemy_object,x,y)
    
    def check_obstruction(self,x:int,y:int):
        obj = self.grid.get_object(x,y)
        if obj is None:
            return False
        else:
            return obj.get("obstruction",False)
    
    def next_position(self,enemy_x,enemy_y,player_x,player_y):
        obj = self.grid.get_object(enemy_x,enemy_y)

        def bresenham_line(x0, y0, x1, y1):
            # draws a bresenham line between two points
            points = []
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            sx = 1 if x0 < x1 else -1
            sy = 1 if y0 < y1 else -1
            err = dx - dy

            while x0 != x1 or y0 != y1:
                points.append((x0, y0))
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x0 += sx
                if e2 < dx:
                    err += dx
                    y0 += sy

            points.append((x1, y1))
            return points
        
        # draw potential line of sight between enemy and player
        new_line = bresenham_line(enemy_x,enemy_y,player_x,player_y)[1:-1]

        # check each point in the line for something blocking line of sight
        for point in new_line:
            x,y = point
            if self.check_obstruction(x,y):
                # the new line is obstructed, line of sight is broken
                # go to next location in queue instead
                if len(obj["path"]) >= 1:
                    next = obj["path"][0]
                    obj["path"] = obj["path"][1:]
                    if self.check_obstruction(next[0],next[1]):
                        # if something is in the way, stop and retry
                        obj["path"] = []
                        return self.next_position(self,enemy_x,enemy_y,player_x,player_y)
                    return next
                else:
                    # if there is no known path, wander instead
                    options = [(enemy_x+1,enemy_y),(enemy_x,enemy_y+1),(enemy_x-1,enemy_y),(enemy_x,enemy_y-1)]
                    real_options = []
                    for x,y in options:
                        if not self.check_obstruction(x,y):
                            real_options.append((x,y))
                    if len(real_options) > 0:
                        return choice(real_options)
                    else:
                        # if you're stuck, don't move
                        return (enemy_x,enemy_y)
        
        # if we exit the loop without returning, then the player is visible to this enemy
        # make a new pursuit path and start following it
        if len(new_line) > 0:
            next_step = new_line[0]
            obj["path"] = new_line[1:]
            return next_step
        else:
            # if the path is too short to move, don't move
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