# Concept
The game is a singleplayer, top-down game that revolves around exploring a location and retrieving valuable items, which need to be brought back to a depository. There is an inherent risk/reward system built in, because the location can be explored as many times as the player wants before cashing out with their loot; but doing so is *always* risky, and could cause them to lose everything if they try. Very much inspired by [Lethal Company](https://store.steampowered.com/app/1966720/Lethal_Company/).
# Turn-Based Structure
The game will be very loosely **turn-based.** When the player does an action (like moving, attacking, stashing items, etc.), the entire world will take one "Step." This system can be likened to the ones in [Baba Is You](https://store.steampowered.com/app/736260/Baba_Is_You/) or [Crypt of the NecroDancer](https://store.steampowered.com/app/247080/Crypt_of_the_NecroDancer/) (without enforcing a rhythm). During a Step, the following happens in this order:
1. Player action
2. Enemy actions
3. Environment actions

There will more than likely be multiple different enemies and environmental factors causing changes during each Step. To break ties in this order, enemies and environmental factors will be given internal IDs that can be used to track them and determine which one goes first.
## Player Actions
Each of these actions incur a Step. Things that involve a menu (e.g. opening and inspecting items in the inventory) *usually* do not incur a Step.
- Movement
- Interaction
- Picking up items
- Stashing items to inventory
- Retrieving items from inventory
- Using items
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
You can hold a limited number of items. If your inventory has too many items in it, you won't be able to stash items from your hands into your inventory. **Your hands are *not* an inventory slot, and should not be treated as such.** Items in your hands are not in your inventory, and un-stashing an item to put it in your hands removes it from your inventory.
# Combat
![An isometric screenshot of a character facing 3 enemies.](https://github.com/cse442-at-ub/s24semesterproject-we-love-the-company/blob/design/isocon-screenshot.png?raw=true)
*Screenshot created using [Isocon](https://github.com/delzhand/isocon) with assets from [Risk of Rain Returns](https://riskofrainreturns.wiki.gg/wiki/Risk_of_Rain_Returns_Wiki). The game does not need to look like this.*
****
The combat ability of any character (player or NPC) is determined solely by their **Combat Die**. The Combat Die can be a d4, d6, d8, d10, d12, or d20. The player starts the game with a d4, and most enemies start higher.

When one character attacks another, it is called a **Strike**.

**Initiating a Strike:**
- Enemies can (usually) initiate a Strike by simply entering a space adjacent to the player.
- The player can initiate a Strike as an action (incurring a Step) by targeting an enemy that they are already adjacent to.

**Resolving a Strike:**
- Both participants of the Strike each roll their **Combat Die.**
- Whoever rolls the higher number wins the strike, and the other loses.
- The loser of the strike **reduces their Combat Die by 1 step.**
	- d20 becomes d12
	- d12 becomes d10
	- d10 becomes d8
	- etc.
- If a character's Combat Die would ever be reduced from a d4, they are instead **Defeated.**
	- Defeated enemies are removed from the map, and may drop items.
	- Defeated players lose the game. :)
