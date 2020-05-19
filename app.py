import streamlit as st
import SessionState

from gamelit import GamelitComponent, draw_tile, Pos

# Register Gamelit
st.register_component("gamelit", GamelitComponent)

# Initialize state
state = SessionState.get(
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

# Build layers
layers = []
if not state.initialized:
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

	layers.append({"layer": 0, "tiles": bg_tiles})
	state.initialized = True

# Create empty foreground layer
fg_tiles = []
layers.append({"layer": 1, "tiles": fg_tiles})

# Add the player to the foreground
draw_tile(fg_tiles, SKULL, state.player_pos)

# Move the player around with the keyboard
keys = st.gamelit("game", layers)
if keys.get(LEFT):
	state.player_pos += Pos(-1, 0)
if keys.get(RIGHT):
	state.player_pos += Pos(1, 0)
if keys.get(UP):
	state.player_pos += Pos(0, -1)
if keys.get(DOWN):
	state.player_pos += Pos(0, 1)
