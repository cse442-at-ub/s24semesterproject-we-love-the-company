# Scenes store state and behavior of "scenes"

A Scene is any distinct screen  
A Scene has 2 main parts, State and Handlers  
Scenes can be changed by doing `state.setScene(`*scene class*`)`

## Handlers

Handlers determine what happens when the game is rendered, updated, or when the user has some input. See the `Handler` class in [`gamestate.py`](../src/game/gamestate.py)  

`onRender` takes the `Gamestate` as an argument and should draw the scene to the screen. It is called every frame.  
  
`onUpdate` takes the `Gamestate` and a `deltaTime` (in seconds) and should update any state based on the delta time. It is called every tick.  
  
`onKeyPress` takes the `Gamestate`, the key, the modifiers, the unicode, and scancode of a keypress. It is called whenever a key is pressed.  
  
`onMouseMove` takes the `Gamestate`, the mouse position, buttons, and touch. It is called whenever the mouse is moved.  
  
`onMousePress` takes the `Gamestate`, the mouse position, buttons, and touch. It is caled whenever the mouse is moved.  
  
`doNothing` can be set as any of these if the behavior is no behavior.

## State

Scenes must have a state class unique to them.  
These classes **MUST** have a unique `id` field.  
They also **MUST** have a `initHandlers(self, state: gamestate.Gamestate)` function.  
  
`initHandlers` **MUST** set `state.handlers[self.id]` to a `Handler`  
  
the state can be accessed in any* handler through `state.scene.*`  
  
*please do not use handlers from other scenes for your scene.
