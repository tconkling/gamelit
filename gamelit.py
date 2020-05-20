from typing import Optional, List, NamedTuple

import streamlit as st

GamelitComponent = st.declare_component(url="http://localhost:3001")
# GamelitComponent = st.declare_component(path="frontend/build")


@GamelitComponent
def component(f, name, layers):
	return f(key=name, layers=layers, default={})


# Tiles, rows, and grids can all be null
Tile = Optional[str]
TileRow = Optional[List[Tile]]
TileGrid = Optional[List[TileRow]]


class Pos(NamedTuple):
	x: int
	y: int

	def __add__(self, other):
		return Pos(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Pos(self.x - other.x, self.y - other.y)

	def __invert__(self):
		return Pos(-self.x, -self.y)


def get_tile(tiles: TileGrid, pos: Pos) -> Tile:
	"""Return the tile at the given position."""
	if tiles is None:
		return None
	if pos.y < 0 or pos.y >= len(tiles):
		return None

	row = tiles[pos.y]
	if row is None or pos.x < 0 or pos.x >= len(row):
		return None

	return row[pos.x]


def set_tile(tiles: TileGrid, pos: Pos, tile: Tile) -> None:
	"""Draw a tile into a TileGrid. Return the updated TileGrid."""
	if tiles is None:
		tiles = []

	# Add missing rows
	while len(tiles) <= pos.y:
		tiles.append(None)
	row = tiles[pos.y]
	if row is None:
		row = []
		tiles[pos.y] = row

	# Add missing row entries
	while len(row) <= pos.x:
		row.append(None)

	row[pos.x] = tile


def move_tile(tiles: TileGrid, from_pos: Pos, to_pos: Pos) -> None:
	"""Move a tile to a new position. Clear its previous position."""
	set_tile(tiles, to_pos, get_tile(tiles, from_pos))
	set_tile(tiles, from_pos, None)


def clear_tile(tiles: TileGrid, pos: Pos) -> None:
	set_tile(tiles, pos, None)

