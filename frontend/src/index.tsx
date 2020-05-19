import * as PIXI from "pixi.js"
import { RenderData, Streamlit } from "./streamlit"

import "bootstrap/dist/css/bootstrap.min.css"
import "./streamlit.css"

// Constants
const TILE_SIZE = 24

// Globals
let spritesheet: PIXI.Spritesheet
let tileLayerRoot = new PIXI.Container()
let tileLayers = new Map<number, PIXI.Container>()

// Create a PIXI app
PIXI.settings.SCALE_MODE = PIXI.SCALE_MODES.NEAREST
const app = new PIXI.Application({width: window.innerWidth, transparent: true})
document.body.appendChild(app.view)

app.stage.scale.set(2, 2)
app.stage.addChild(tileLayerRoot)

// Load resources
PIXI.Loader.shared.add("spritesheet.json").load(onResourcesLoaded)
function onResourcesLoaded () {
	spritesheet = PIXI.Loader.shared.resources["spritesheet.json"].spritesheet!

	// Tell Streamlit we're ready to start receiving data. We won't get our
	// first RENDER_EVENT until we call this function.
	Streamlit.setComponentReady()

	// Finally, tell Streamlit to update our intiial height. We omit the
	// `height` parameter here to have it default to our scrollHeight.
	Streamlit.setFrameHeight()
}

/** Draw a tile grid. The grid, its rows, and individual cells can all be null. */
function drawGrid (layerIndex: number, grid: string[][]) {
	// Create the layer if it doesn't already exist
	let layer = tileLayers.get(layerIndex)
	if (layer != null) {
		layer.removeChildren()
	} else {
		layer = new PIXI.Container()
		layer.zIndex = layerIndex
		tileLayerRoot.addChild(layer)
		tileLayers.set(layerIndex, layer)
	}

	if (grid == null) {
		return
	}

	for (let yy = 0; yy < grid.length; ++yy) {
		const row = grid[yy]
		if (row == null) {
			continue
		}

		for (let xx = 0; xx < row.length; ++xx) {
			const tileName = row[xx]
			if (tileName == null) {
				continue
			}

			const tileTex = spritesheet.textures[tileName]
			if (tileTex == null) {
				console.warn(`Missing tile texture "${tileName}"`)
				continue
			}

			const tile = new PIXI.Sprite(tileTex)
			tile.position.set(xx * TILE_SIZE, yy * TILE_SIZE)
			layer.addChild(tile)
		}
	}
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, event => {
	const renderData = (event as CustomEvent<RenderData>).detail
	const layers = renderData.args["layers"]
	if (layers == null) {
		console.warn("Missing 'layers' arg")
		return
	}

	for (let layerData of layers) {
		const index = layerData["layer"]
		const tiles = layerData["tiles"]
		drawGrid(index, tiles)
	}
});
