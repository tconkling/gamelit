import * as PIXI from "pixi.js"
import { Streamlit } from "./streamlit"

import "bootstrap/dist/css/bootstrap.min.css"
import "./streamlit.css"

// Create a PIXI app
PIXI.settings.SCALE_MODE = PIXI.SCALE_MODES.NEAREST
const app = new PIXI.Application({width: window.innerWidth})
app.stage.scale.set(2, 2)
document.body.appendChild(app.view)

// Load resources
PIXI.Loader.shared.add("spritesheet.json").load(onResourcesLoaded)

let spritesheet: PIXI.Spritesheet
function onResourcesLoaded () {
	spritesheet = PIXI.Loader.shared.resources["spritesheet.json"].spritesheet!

	// Tell Streamlit we're ready to start receiving data. We won't get our
	// first RENDER_EVENT until we call this function.
	Streamlit.setComponentReady()

	// Finally, tell Streamlit to update our intiial height. We omit the
	// `height` parameter here to have it default to our scrollHeight.
	Streamlit.setFrameHeight()
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, event => {

	const bunny = new PIXI.Sprite(spritesheet.textures["oryx_16bit_fantasy_world_612.png"])

	// Setup the position of the bunny
	bunny.x = 10;
	bunny.y = 10;

	// Add the bunny to the scene we are building
	app.stage.addChild(bunny);

});
