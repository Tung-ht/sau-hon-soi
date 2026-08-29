# 📚 AI Novel Studio 2.0 (Workspace Hub)

Chào mừng bạn đến với không gian sáng tác tiểu thuyết phân tầng tự chủ **AI Novel Studio 2.0** theo mô hình **Agent-Led, Engine-Guarded** (Đồng tác giả thông minh) tối ưu cho **Gemini 3.7 Flash High** và **Antigravity**.

---

## ⚡ 1. Khởi Động Nhanh (Quickstart)

### 📌 Kiểm tra tình trạng bộ truyện đang viết:
```bash
python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/loi-tran-troi" status
```

### 📌 Xem danh sách tất cả các bộ tiểu thuyết trong workspace:
```bash
python .agents/skills/ai-novel-studio/scripts/novel_state.py list-novels
```

### 📌 Khởi tạo một bộ tiểu thuyết mới:
```bash
python .agents/skills/ai-novel-studio/scripts/novel_state.py init --name "Tên Truyện Mới" --scale long --premise "Giới thiệu tác phẩm..."
```

---

## 📖 2. Tài Liệu Hướng Dẫn Chi Tiết

* 📄 **[Hướng Dẫn Sử Dụng Đầy Đủ (Tất cả 15+ lệnh CLI)](.agents/skills/ai-novel-studio/README.md)**
* 🚨 **[Quy Chuẩn Bắt Buộc Khi Sửa Tiểu Thuyết (mandatory_revision_workflow.md)](.agents/rules/mandatory_revision_workflow.md)**
* 🔄 **[Quy Tắc Bắt Buộc Đồng Bộ Ngữ Cảnh (context_synchronization_rule.md)](.agents/rules/context_synchronization_rule.md)**
* 📄 **[Chỉ Dẫn Hệ Thống Subagents (SKILL.md)](.agents/skills/ai-novel-studio/SKILL.md)**
* 📁 **[Bộ Quy Chuẩn Văn Phong Thuần Việt & Chống Văn Mẫu AI](.agents/rules/)**

---

## 🧪 3. Chạy Kiểm Thử Hệ Thống (Automated Test Suite)
```bash
python -m unittest discover -s .agents/skills/ai-novel-studio/tests -p "test_*.py"
```

---

## 🏆 4. Dự Án Đang Hoạt Động
* **Tác phẩm:** *Lời Trăn Trối* (`novels/loi-tran-troi/`)
* **Tiến độ hiện tại:** 10 chương hoàn thành (14.100 từ) — Vị trí: **Tập 2 · Cung 1**
* **Chương tiếp theo:** **Chương 11 (Mở đầu Cung 3)**
