package main

import (
	"embed"
	"log"

	"github.com/joho/godotenv"
	"github.com/wailsapp/wails/v2"
	"github.com/wailsapp/wails/v2/pkg/options"
	"github.com/wailsapp/wails/v2/pkg/options/assetserver"
)

//go:embed all:frontend/dist
var assets embed.FS

func main() {
	// Load env
	err := godotenv.Load()
	if err != nil {
		log.Println("No .env file found")
	}

	// Create an instance of the app structure
	app := NewApp()

	// Create application with options
	appErr := wails.Run(&options.App{
		Title:     "Mtranslate",
		Width:     700,
		Height:    550,
		MinWidth:  450,
		MinHeight: 550,
		AssetServer: &assetserver.Options{
			Assets: assets,
		},
		BackgroundColour: &options.RGBA{R: 33, G: 33, B: 33, A: 1},
		OnStartup:        app.startup,
		Bind: []interface{}{
			app,
		},
	})

	if appErr != nil {
		println("Error:", appErr.Error())
	}
}
