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


def draw_tile(tiles: TileGrid, tile: Tile, pos: Pos) -> TileGrid:
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

	return tiles

