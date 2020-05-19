from typing import Optional, List

import streamlit as st

GamelitComponent = st.declare_component(url="http://localhost:3001")
# Gamelit = st.declare_component(path="frontend/build")

# Tiles, rows, and grids can all be null
Tile = Optional[str]
TileRow = Optional[List[Tile]]
TileGrid = Optional[List[TileRow]]


def draw_tile(tiles: TileGrid, tile: Tile, x: int, y: int) -> TileGrid:
	"""Draw a tile into a TileGrid. Return the updated TileGrid."""
	if tiles is None:
		tiles = []

	# Add missing rows
	while len(tiles) <= y:
		tiles.append(None)
	row = tiles[y]
	if row is None:
		row = []
		tiles[y] = row

	# Add missing row entries
	while len(row) <= x:
		row.append(None)

	row[x] = tile

	return tiles

