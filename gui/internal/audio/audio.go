package audio

import (
	"bytes"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"sync"

	"github.com/gen2brain/malgo"
	"github.com/youpy/go-wav"
)

var (
	ctx     *malgo.AllocatedContext
	ctxOnce sync.Once
	ctxErr  error
)
var devices []malgo.DeviceInfo

func getContext() (*malgo.AllocatedContext, error) {
	ctxOnce.Do(func() {
		ctx, ctxErr = malgo.InitContext(nil, malgo.ContextConfig{}, nil)
	})
	return ctx, ctxErr
}

func CloseContext() {
	if ctx != nil {
		_ = ctx.Uninit()
		ctx.Free()
	}
}

func GetListPlaybackDevice() ([]malgo.DeviceInfo, error) {
	ctx, ctxErr := getContext()

	if ctxErr != nil {
		return nil, ctxErr
	}
	var err error
	devices, err = ctx.Devices(malgo.Playback)
	if err != nil {
		return nil, err
	}

	return devices, nil
}

func StartPlaybackDevice(keyDevice int, textVoice string, nameVoice string) error {
	var reader io.Reader
	var channels, sampleRate uint32

	baseURL := os.Getenv("URL_API") + "/synthesize_speech/"
	params := url.Values{}
	params.Add("text", textVoice)
	params.Add("voice", nameVoice)
	params.Add("accent", "en-newest")
	params.Add("speed", "1.0")

	resp, err := http.Get(baseURL + "?" + params.Encode())

	if err != nil {
		return err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("error get file voice")
	}

	// Read the entire body into memory (this could be optimized if the file is large)
	data, err := io.ReadAll(resp.Body)
	if err != nil {
		return err
	}
	datafile := bytes.NewReader(data)
	w := wav.NewReader(datafile)
	f, err := w.Format()
	if err != nil {
		return err
	}

	reader = w
	channels = uint32(f.NumChannels)
	sampleRate = f.SampleRate

	// Thiết lập cho thiết bị đã chọn
	deviceConfig1 := malgo.DefaultDeviceConfig(malgo.Playback)
	deviceConfig1.Playback.Format = malgo.FormatS16
	deviceConfig1.Playback.DeviceID = devices[keyDevice].ID.Pointer()
	deviceConfig1.Playback.Channels = channels
	deviceConfig1.SampleRate = sampleRate

	// Thiết lập cho thiết bị mặc định
	deviceConfig2 := malgo.DefaultDeviceConfig(malgo.Playback)
	deviceConfig2.Playback.Format = malgo.FormatS16
	deviceConfig2.Playback.Channels = channels
	deviceConfig2.SampleRate = sampleRate

	// Channel để báo hiệu khi phát xong
	done := make(chan struct{})

	// Sử dụng WaitGroup để theo dõi khi cả hai thiết bị đã hoàn thành
	var wg sync.WaitGroup
	var once1, once2 sync.Once
	wg.Add(2) // Chờ 2 thiết bị

	buf := bytes.NewBuffer(nil)
	if _, err := io.Copy(buf, reader); err != nil {
		return err
	}

	// Tạo reader mới cho mỗi device
	reader1 := bytes.NewReader(buf.Bytes())
	reader2 := bytes.NewReader(buf.Bytes())

	// Callback cho thiết bị đã chọn
	onSamples1 := func(pOut []byte, pIn []byte, frames uint32) {
		_, err := io.ReadFull(reader1, pOut)
		if err == io.EOF || err != nil {
			once1.Do(func() {
				wg.Done()
			})
			return
		}
	}

	// Callback cho thiết bị mặc định
	onSamples2 := func(pOut []byte, pIn []byte, frames uint32) {
		_, err := io.ReadFull(reader2, pOut)
		if err == io.EOF || err != nil {
			once2.Do(func() {
				wg.Done()
			})
			return
		}
	}

	// Khởi tạo và chạy thiết bị đã chọn
	deviceCallbacks1 := malgo.DeviceCallbacks{
		Data: onSamples1,
	}
	device1, err := malgo.InitDevice(ctx.Context, deviceConfig1, deviceCallbacks1)
	if err != nil {
		return err
	}
	defer device1.Uninit()

	// Khởi tạo và chạy thiết bị (mặc định)
	deviceCallbacks2 := malgo.DeviceCallbacks{
		Data: onSamples2,
	}
	device2, err := malgo.InitDevice(ctx.Context, deviceConfig2, deviceCallbacks2)
	if err != nil {
		return err
	}
	defer device2.Uninit()

	// Start voice
	err = device1.Start()
	if err != nil {
		return err
	}
	err = device2.Start()
	if err != nil {
		return err
	}

	// Chạy một goroutine để đợi cả hai thiết bị hoàn thành rồi đóng kênh done
	go func() {
		wg.Wait()
		close(done)
	}()

	// Chờ tín hiệu kết thúc
	<-done
	device1.Stop()
	device2.Stop()
	return nil
}
