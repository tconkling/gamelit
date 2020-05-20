import random
from typing import Tuple

import streamlit as st

import SessionState
from gamelit import GamelitComponent, set_tile, Pos, get_tile, TileGrid, clear_tile

# Register Gamelit
st.register_component("gamelit", GamelitComponent)

# Hello!
st.title("⚔️ Gamelit Demo")

st.markdown("""
A super-simple tile-based game framework.

Gamelit is a "dumb terminal". All the game logic and state is maintained
in the Streamlit app, which runs the game and tells the component to render
new tiles.

(This demo uses the SessionState patch to maintain game state.)
""")

# Initialize state
game_state = SessionState.get(
	player_pos=Pos(1, 1),
	player_facing="left",
	floor=None,
	objects=None,
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

# Keyboard keys
LEFT = "ArrowLeft"
RIGHT = "ArrowRight"
UP = "ArrowUp"
DOWN = "ArrowDown"

ROOM_WIDTH = 14
ROOM_HEIGHT = 12

def random_empty_tile(floor: TileGrid, objects: TileGrid) -> Pos:
	height = len(floor)
	width = len(floor[0])
	while True:
		pos = Pos(
			random.randint(0, width - 1),
			random.randint(0, height - 1),
		)
		if pos != game_state.player_pos and get_tile(floor, pos) == FLOOR and get_tile(objects, pos) is None:
			return pos

def generate_room() -> Tuple[TileGrid, TileGrid]:
	floor = []
	objects = []

	# Fill floors
	for yy in range(0, ROOM_HEIGHT):
		for xx in range(0, ROOM_WIDTH):
			set_tile(floor, Pos(xx, yy), FLOOR)

	# Top/bottom walls
	for yy in (0, ROOM_HEIGHT - 1):
		for xx in range(0, ROOM_WIDTH):
			set_tile(floor, Pos(xx, yy), WALL)

	# Left/right walls
	for xx in (0, ROOM_WIDTH - 1):
		for yy in range(0, ROOM_HEIGHT):
			set_tile(floor, Pos(xx, yy), WALL)

	# Pick a spot for the stairs.
	set_tile(floor, random_empty_tile(floor, objects), STAIRS)

	# Drop some chests.
	for _ in range(random.randint(1, 4)):
		set_tile(objects, random_empty_tile(floor, objects), CHEST)

	# Place the player.
	player_tile = KNIGHT_LEFT if game_state.player_facing == "left" else KNIGHT_RIGHT
	set_tile(objects, game_state.player_pos, player_tile)

	return floor, objects

tile_layers = []

# Create a room if need be! This will replace any existing floor.
# We only send the floor tiles when the floor is generated, rather than
# every tick.
if game_state.floor is None:
	floor, objects = generate_room()
	game_state.floor = floor
	game_state.objects = objects
	tile_layers.append({"layer": 0, "tiles": game_state.floor})

# We always send our objects tiles.
tile_layers.append({"layer": 1, "tiles": game_state.objects})

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
tile = get_tile(game_state.floor, new_pos)
if tile == FLOOR or tile == STAIRS:
	# Is there an object on the floor?
	object = get_tile(game_state.objects, new_pos)

	# Remove the player from their previous position
	clear_tile(game_state.objects, game_state.player_pos)

	# Move them to their new position
	game_state.player_pos = new_pos
	game_state.player_facing = new_facing
	player_tile = KNIGHT_LEFT if game_state.player_facing == "left" else KNIGHT_RIGHT
	set_tile(game_state.objects, new_pos, player_tile)

	# Handle object collisions
	if object == CHEST:
		game_state.score += 1

	# Go down a level! Setting floor to None will cause us to rebuild our room.
	if tile == STAIRS:
		game_state.floor = None
		game_state.depth += 1

# Show help
st.text("Controls: arrow keys to move")
st.text("(Click inside the game to give it keyboard focus)")
