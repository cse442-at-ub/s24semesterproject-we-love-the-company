import random

class Combat:
    def __init__(self):
        # Define the dice and their ranges
        self.dice = {
            'd4': range(1, 5),
            'd6': range(1, 7),
            'd8': range(1, 9),
            'd10': range(1, 11),
            'd12': range(1, 13),
            'd20': range(1, 21),
        }
        # Define the upgrade and downgrade paths for combat dice
        self.upgrade_path = ['d4', 'd6', 'd8', 'd10', 'd12', 'd20']
        # Reverse of upgrade_path for downgrade
        self.downgrade_path = self.upgrade_path[::-1]

    def roll_die(self, die):
        """Rolls the specified die and returns the result."""
        return random.choice(list(self.dice[die]))

    def combat_outcome(self, player_die, enemy_die):
        """Simulates combat between player and enemy, returning the outcome."""
        player_roll = self.roll_die(player_die)
        enemy_roll = self.roll_die(enemy_die)

        if player_roll > enemy_roll:
            return 'player'
        elif enemy_roll > player_roll:
            return 'enemy'
        else:
            return 'draw'

    def downgrade_die(self, current_die):
        """Downgrades the die type, or marks as defeated if already at lowest."""
        if current_die == self.downgrade_path[0]:  # 'd20' is the first element after reversing
            return 'defeated'
        else:
            return self.downgrade_path[self.downgrade_path.index(current_die) - 1]

    def upgrade_die(self, current_die):
        """Upgrades the die type, or remains the same if already at highest."""
        if current_die == self.upgrade_path[-1]:  # 'd20' is the last element
            return current_die  # Cannot upgrade further
        else:
            return self.upgrade_path[self.upgrade_path.index(current_die) + 1]
