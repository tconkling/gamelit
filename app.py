import streamlit as st

from gamelit import GamelitComponent, draw_tile

WALL = "wall.png"
FLOOR = "floor.png"
SKULL = "skull1.png"

st.register_component("gamelit", GamelitComponent)

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

# Create empty foreground layer, and draw tiles into it
fg_tiles = []
draw_tile(fg_tiles, SKULL, 1, 1)

keys = st.gamelit(key="game", layers=[
	{"layer": 0, "tiles": bg_tiles},
	{"layer": 1, "tiles": fg_tiles},
])
