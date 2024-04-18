from combat import Combat
from backpack import Backpack

class ItemEffects:
    def __init__(self, backpack: Backpack):
        self.dice_level = 0
        self.extra_rolls = 0
        self.multiplier = 1.0
        self.constant = 0.0

        # apply all effects
        for item in backpack.items:
            item.effect(self)

    def upgrade_die(self, count: int = 1):
        self.dice_level += count

    def downgrade_die(self, count: int = 1):
        self.dice_level -= count

    def give_advantage(self, count: int = 1):
        self.extra_rolls += count

    def give_disadvantage(self, count: int = 1):
        self.extra_rolls -= count

    def multiply_roll(self, multiplier: float):
        self.multiplier *= multiplier

    def add_to_roll(self, constant: float):
        self.constant += constant

    def roll_die(self, combat: Combat, die):
        real_die = die

        # changing level of die
        if (self.dice_level > 0):
            for _ in range(self.dice_level):
                real_die = combat.upgrade_die(real_die)
        else:
            for _ in range(self.dice_level):
                real_die = combat.downgrade_die(real_die)

        roll = combat.roll_die(real_die)

        # advantage / disadvantage
        for _ in range(self.extra_rolls):
            if (self.extra_rolls > 0):
                roll = max(roll, combat.roll_die(real_die))
            else:
                roll = min(roll, combat.roll_die(real_die))

        # apply multiplier and scalar
        roll *= self.multiplier
        roll += self.constant

        return roll