# Concept
The game is a singleplayer, top-down game that revolves around exploring a location and retrieving valuable items, which need to be brought back to a depository. There is an inherent risk/reward system built in, because the location can be explored as many times as the player wants before cashing out with their loot; but doing so is *always* risky, and could cause them to lose everything if they try. Very much inspired by [Lethal Company](https://store.steampowered.com/app/1966720/Lethal_Company/).
# Turn-Based Structure
The game will be very loosely **turn-based.** When the player does an action (like moving, attacking, stashing items, etc.), the entire world will take one "step." This system can be likened to the ones in [Baba Is You](https://store.steampowered.com/app/736260/Baba_Is_You/) or [Crypt of the NecroDancer](https://store.steampowered.com/app/247080/Crypt_of_the_NecroDancer/) (without enforcing a rhythm). During a step, the following happens in this order:
1. Player action
2. Enemy actions
3. Environment actions
There will more than likely be multiple different enemies and environmental factors causing changes during each step. To break ties in this order, enemies and environmental factors will be given internal IDs that can be used to track them and determine which one goes first.
# Items & Inventory
When picked up, an item is placed in the player's hands. Items can be stashed into an inventory, where they can be accessed in the inventory menu.
## Item Types
All items have some kind of value, but some have particular uses.
- **Loot** - Serves no functional purpose. Tends to be marginally more valuable than most other item types.
	- **Heavy Loot** - Much more valuable than standard loot, but slows you down a lot.
- **Weapon** - Allows you to defend yourself, but has a chance of breaking and becoming worthless when used too often.
	- **Lethal Weapon** - Instantly dispatches any enemy, but is very valuable if kept.
- **Gear** - Can be equipped, which provides a persistent bonus, but can be lost in a variety of ways.
- **Consumable** - Can be destroyed to gain a bonus of some kind, like healing or a temporary buff.
## Inventory System
You can hold a limited number of items. If your inventory has too many items in it, you won't be able to stash items from your hands into your inventory. **Your hands are *not* an inventory slot,** and should not be treated as such; items in your hands are not in your inventory, and un-stashing an item to put it in your hands removes it from your inventory.
# Combat
*Screenshot created using [Isocon](https://github.com/delzhand/isocon) with assets from [Risk of Rain Returns](https://riskofrainreturns.wiki.gg/wiki/Risk_of_Rain_Returns_Wiki). The game does not need to look like this.*
![[isocon-screenshot.png]]