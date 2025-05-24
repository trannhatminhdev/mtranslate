# 🚀 **Project Build Instructions**

## 🧪 Development Mode

Để khởi chạy ứng dụng ở chế độ phát triển:

```bash
cd gui
wails dev
```

> ⚙️ Lệnh này sẽ chạy frontend với hot-reload và backend đồng thời, giúp bạn phát triển nhanh chóng và hiệu quả.

---

## 🛠️ Build Project

Khi đã sẵn sàng build ứng dụng production, sử dụng lệnh sau:

```bash
wails build -clean -trimpath
```

### ✅ Tham số giải thích:

* `-clean`: Xóa các tệp build cũ trước khi build mới
* `-trimpath`: Loại bỏ thông tin đường dẫn tuyệt đối trong binary (giúp giảm dung lượng và tăng bảo mật)

> 💡 Yêu cầu: Đảm bảo đã cài đặt [Wails CLI](https://wails.io/docs/gettingstarted/installation/).
> Nếu chưa, cài đặt bằng:

```bash
go install github.com/wailsapp/wails/v2/cmd/wails@latest
```
