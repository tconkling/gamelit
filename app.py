import streamlit as st
from gamelit import GamelitComponent

WALL = "wall.png"
FLOOR = "floor.png"
SKULL = "skull1.png"

st.register_component("gamelit", GamelitComponent)

# Build background layer
bg_layer = {
	"layer": 0,
	"tiles": [
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
}

skull_layer = {
	"layer": 1,
	"tiles": [
		None,
		None,
		None,
		[None, None, None, SKULL]
	]
}

st.gamelit(key="game", layers=[bg_layer, skull_layer])
