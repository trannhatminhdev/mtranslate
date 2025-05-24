package main

import (
	"context"
	"mtranslate/internal/audio"
	"os"

	"github.com/wailsapp/wails/v2/pkg/runtime"
)

// App struct
type App struct {
	ctx context.Context
}

// NewApp creates a new App application struct
func NewApp() *App {
	return &App{}
}

// startup is called when the app starts. The context is saved
// so we can call the runtime methods
func (a *App) startup(ctx context.Context) {
	a.ctx = ctx
	runtime.WindowSetDarkTheme(ctx)
	runtime.WindowSetSize(ctx, 700, 550)
}

type DeviceInfo struct {
	Key  int
	Name string
}

func (a *App) ListPlaybackDevice() []DeviceInfo {
	var deviceInfoList []DeviceInfo

	devices, err := audio.GetListPlaybackDevice()
	if err != nil {
		return deviceInfoList
	}

	for i, device := range devices {
		deviceInfoList = append(deviceInfoList, DeviceInfo{
			Key:  i,
			Name: device.Name(),
		})
	}

	return deviceInfoList
}

func (a *App) StartPlaybackDevice(keyDevice int, textVoice string, nameVoice string) error {
	err := audio.StartPlaybackDevice(keyDevice, textVoice, nameVoice)
	if err != nil {
		return err
	}
	return nil
}

func (a *App) GetUrlApi() string {
	return os.Getenv("URL_API")
}
