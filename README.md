# 📘 **Mtranslate – Hướng dẫn Cài đặt & Sử dụng**

## ▶️ Bắt đầu nhanh

### 🔹 Bước 1: Tải source code

```bash
git clone https://github.com/trannhatminhdev/mtranslate.git
```

---

### 🔹 Bước 2: Khởi động Backend

Di chuyển đến thư mục Docker của backend:

```bash
cd backend/docker
```

Khởi chạy dịch vụ bằng Docker Compose:

```bash
docker compose up
```

> 🛠 Nếu gặp lỗi liên quan đến GPU, tham khảo hướng dẫn tại mục [Fix GPU](https://github.com/trannhatminhdev/mtranslate/blob/main/backend/README.md)

---

### 🔹 Bước 3: Chạy ứng dụng `mtranslate.exe`

* Mở file `.env`
* Cập nhật giá trị `URL_API` trỏ về địa chỉ của backend bạn vừa chạy

---

### 🔹 Bước 4: Cài đặt **VB-CABLE Virtual Audio Device**

Ứng dụng sử dụng micro ảo để thu âm đầu vào.
Tải xuống tại: [🔗 VB-CABLE Virtual Audio](https://vb-audio.com/Cable/)

---

### 🔹 Bước 5: Cấu hình thiết bị đầu vào

Trong cài đặt âm thanh của hệ điều hành, chọn **CABLE Input (VB-Audio Virtual Cable)** làm micro đầu vào.

---

## 📷 Video hướng dẫn

[![Xem video hướng dẫn](https://img.youtube.com/vi/hoCIieo1NT8/0.jpg)](https://www.youtube.com/watch?v=hoCIieo1NT8)

---

## 📬 Ghi chú

* ✅ Đảm bảo Docker đã được cấu hình để hỗ trợ GPU nếu bạn chạy trên hệ thống có NVIDIA GPU.
* 🔧 Tham khảo hướng dẫn chi tiết tại: [`backend/README.md`](https://github.com/trannhatminhdev/mtranslate/blob/main/backend/README.md)