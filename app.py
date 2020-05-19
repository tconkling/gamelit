import random

import streamlit as st

import SessionState
from gamelit import GamelitComponent, set_tile, Pos, get_tile, TileGrid

# Register Gamelit
st.register_component("gamelit", GamelitComponent)

# Hello!
st.title("⚔️ Gamelit Demo")

st.markdown("""
A super-simple tile-based game framework.

Gamelit is a "dumb terminal". All the game logic and state is maintained
in the Streamlit app, which runs the game and tells the component to render
new tiles.
""")

# Initialize state
game_state = SessionState.get(
	player_pos=Pos(1, 1),
	player_facing="left",
	room=None,
	depth=1,
	score=0,
)

# Tiles
WALL = "wall.png"
FLOOR = "floor.png"
KNIGHT_LEFT = "knight_left.png"
KNIGHT_RIGHT = "knight_right.png"
SKULL = "skull1.png"
CHEST = "chest.png"
STAIRS = "stairs.png"

# Keys
LEFT = "ArrowLeft"
RIGHT = "ArrowRight"
UP = "ArrowUp"
DOWN = "ArrowDown"

ROOM_WIDTH = 14
ROOM_HEIGHT = 12

def generate_room() -> TileGrid:
	tiles = []

	# Fill floors
	for yy in range(0, ROOM_HEIGHT):
		for xx in range(0, ROOM_WIDTH):
			set_tile(tiles, Pos(xx, yy), FLOOR)

	# Top/bottom walls
	for yy in (0, ROOM_HEIGHT - 1):
		for xx in range(0, ROOM_WIDTH):
			set_tile(tiles, Pos(xx, yy), WALL)

	# Left/right walls
	for xx in (0, ROOM_WIDTH - 1):
		for yy in range(0, ROOM_HEIGHT):
			set_tile(tiles, Pos(xx, yy), WALL)

	# Pick a spot for the stairs. Ensure it's not where the player is standing.
	while True:
		stairs_pos = Pos(
			random.randint(1, ROOM_WIDTH - 2),
			random.randint(1, ROOM_HEIGHT - 2),
		)
		if stairs_pos != game_state.player_pos:
			break

	set_tile(tiles, stairs_pos, STAIRS)

	return tiles

tile_layers = []

# Create a room if need be! This will replace any existing room.
# We only send the room tiles when the room is generated, rather than
# every tick.
if game_state.room is None:
	game_state.room = generate_room()
	tile_layers.append({"layer": 0, "tiles": game_state.room})

# Create our foreground tiles. We always send these.
fg_tiles = []
tile_layers.append({"layer": 1, "tiles": fg_tiles})

# Add the player to the foreground
player_tile = KNIGHT_LEFT if game_state.player_facing == "left" else KNIGHT_RIGHT
set_tile(fg_tiles, game_state.player_pos, player_tile)

# Update the game, and get the new keyboard state
keys = st.gamelit("game", tile_layers)

# Show stats
st.markdown(f"**Depth**: {game_state.depth * 10} meters")
st.markdown(f"**Score**: {game_state.score * 100} gold")

# Process input. Move the player around with the arrow keys.
new_pos = game_state.player_pos
new_facing = game_state.player_facing
if keys.get(LEFT):
	new_pos += Pos(-1, 0)
	new_facing = "left"
if keys.get(RIGHT):
	new_pos += Pos(1, 0)
	new_facing = "right"
if keys.get(UP):
	new_pos += Pos(0, -1)
if keys.get(DOWN):
	new_pos += Pos(0, 1)

# Detect collisions. Only update the player's position if it's on a floor tile.
tile = get_tile(game_state.room, new_pos)
if tile == FLOOR or tile == STAIRS:
	game_state.player_pos = new_pos
	game_state.player_facing = new_facing

	# Go down a level!
	if tile == STAIRS:
		game_state.room = None
		game_state.depth += 1

# Show help
st.text("Controls: arrow keys to move")
st.text("(Click inside the game to give it keyboard focus)")
