import streamlit as st

import SessionState
from gamelit import GamelitComponent, set_tile, Pos, get_tile

# Register Gamelit
st.register_component("gamelit", GamelitComponent)

# Hello!
st.title("Gamelit Demo")
st.text("Controls: arrow keys to move")

# Initialize state
game_state = SessionState.get(
	initialized=False,
	player_pos=Pos(1, 1),
)

# Tiles
WALL = "wall.png"
FLOOR = "floor.png"
SKULL = "skull1.png"

# Keys
LEFT = "ArrowLeft"
RIGHT = "ArrowRight"
UP = "ArrowUp"
DOWN = "ArrowDown"

# Create static background layer
bg_tiles = [
	[WALL] * 14,
	[WALL] + [FLOOR] * 12 + [WALL],
	[WALL] + [FLOOR] * 12 + [WALL],
	[WALL] + [FLOOR] * 12 + [WALL],
	[WALL] + [FLOOR] * 12 + [WALL],
	[WALL] + [FLOOR] * 12 + [WALL],
	[WALL] + [FLOOR] * 12 + [WALL],
	[WALL] + [FLOOR] * 12 + [WALL],
	[WALL] + [FLOOR] * 12 + [WALL],
	[WALL] + [FLOOR] * 12 + [WALL],
	[WALL] + [FLOOR] * 12 + [WALL],
	[WALL] * 14,
]

# Build layers
layers = []
if not game_state.initialized:
	layers.append({"layer": 0, "tiles": bg_tiles})
	game_state.initialized = True

# Create empty foreground layer
fg_tiles = []
layers.append({"layer": 1, "tiles": fg_tiles})

# Add the player to the foreground
set_tile(fg_tiles, SKULL, game_state.player_pos)

# Update the game, and get the new keyboard state
keys = st.gamelit("game", layers)

# Process input. Move the player around with the arrow keys.
new_pos = game_state.player_pos
if keys.get(LEFT):
	new_pos += Pos(-1, 0)
if keys.get(RIGHT):
	new_pos += Pos(1, 0)
if keys.get(UP):
	new_pos += Pos(0, -1)
if keys.get(DOWN):
	new_pos += Pos(0, 1)

# Detect collisions. Only update the player's position if it's on a floor tile.
if get_tile(bg_tiles, new_pos) == FLOOR:
	game_state.player_pos = new_pos
