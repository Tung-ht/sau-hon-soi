# 🚨 QUY TẮC BẮT BUỘC: QUY TRÌNH CHỈNH SỬA VÀ VIẾT LẠI TIỂU THUYẾT (MANDATORY REVISION WORKFLOW)

> **HIỆU LỰC TUYỆT ĐỐI:** Quy tắc này **BẮT BUỘC PHẢI ÁP DỤNG 100%** bất cứ khi nào Người dùng/Tác giả nhắc đến các yêu cầu:  
> *"sửa truyện"*, *"sửa chương X"*, *"chỉnh sửa"*, *"viết lại"*, *"viết lại chương X"*, *"tinh chỉnh văn phong"*, *"đổi tình tiết"*, *"sửa nhân vật"*, *"fix cốt truyện"*, *"so sánh bản nháp"*, *"thay đổi kết cục"*.

---

## ⛔ 1. CÁC ĐIỀU CẤM TUYỆT ĐỐI (NON-NEGOTIABLE)

1. **CẤM chỉnh sửa chay bằng mắt hoặc sửa trực tiếp vào file chính `chapters/XX.md`:** Mọi sửa đổi bắt buộc phải đi qua cơ chế Revision (`revisions/XX/r00X.md`).
2. **CẤM sửa nội dung mà không cập nhật Fact:** Mọi bản sửa đổi phải đi kèm `facts/XX/r00X.json` để Engine cập nhật lại dòng thời gian và phục bút.
3. **CẤM bỏ qua bước phân tích ảnh hưởng (Impact Analysis):** Khi sửa chương $N$, phải kiểm tra xem các chương $N+1, N+2...$ có bị hỏng logic hay không.
4. **CẤM tự ý commit/accept khi chưa có sự đồng ý của Tác giả** (trong chế độ `guided` và `manual`).

---

## 🔄 2. BẢY BƯỚC BẮT BUỘC TRONG QUY TRÌNH CHỈNH SỬA

Bất cứ khi nào nhận được yêu cầu sửa tiểu thuyết, AI Agent **BẮT BUỘC** phải thực thi tuần tự đầy đủ 7 bước sau:

```text
[Yêu cầu sửa chương N]
         │
         ▼
1. Phân tích ảnh hưởng (`impact --chapter N`) & Nạp context (`context --chapter N`)
         │
         ▼
2. Tái ký Hợp đồng chương (`plan --chapter N`) nếu đổi tình tiết
         │
         ▼
3. Soạn Revision mới (`draft --chapter N` / `branch --name ...`) + Trích xuất Facts
   (Áp dụng nghiêm ngặt: vietnamese-novel-prose.md & anti-ai-tone.md)
         │
         ▼
4. Quét chất lượng văn phong tĩnh (`style-lint --chapter N`)
         │
         ▼
5. Đối chiếu Diff (`diff --chapter N`) & Chấm điểm 7 chiều (`save-review --chapter N`)
         │
         ▼
6. Trình bày Text Diff / Fact Diff cho Tác giả & Chờ phê duyệt (`accept` / `reject`)
         │
         ▼
7. Khi được Accept: Dựng lại Projections (`rebuild`) & Xử lý Cascading Downstream (nếu có)
```

---

### Chi Tiết Từng Bước:

### 🔹 Bước 1: Phân tích ảnh hưởng & Lấy ngữ cảnh
Trước khi sửa dù chỉ 1 câu, phải chạy:
```bash
python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/<slug>" impact --chapter N
python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/<slug>" context --chapter N
```
* Báo cáo cho tác giả: Những phục bút nào, nhân vật nào, và những chương sau nào ($N+1, N+2...$) có nguy cơ bị ảnh hưởng.

### 🔹 Bước 2: Tái ký Hợp đồng chương (`plan`)
Nếu việc sửa đổi làm thay đổi mục tiêu (goal), phân cảnh (scenes) hoặc nhịp bắt buộc (beats), phải cập nhật lại:
```bash
python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/<slug>" plan --chapter N --data '<json_plan>'
```

### 🔹 Bước 3: Soạn bản thảo Revision mới (`draft` hoặc `branch`)
Viết lại hoặc tinh chỉnh nội dung và lưu thành **Revision kế tiếp** (ví dụ `r002`, `r003` hoặc `r002_branch_A`), đi kèm `facts` mới:
```bash
python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/<slug>" draft --chapter N --content-file "<path>" --facts '<json_facts>'
```
* **Bắt buộc tuân thủ:**
  - Quy chuẩn văn phong thuần Việt: [`rules/vietnamese-novel-prose.md`](./vietnamese-novel-prose.md).
  - Quy chuẩn chống văn mẫu AI & văn convert: [`rules/anti-ai-tone.md`](./anti-ai-tone.md).

### 🔹 Bước 4: Quét kiểm tra phong cách (`style-lint`)
Chạy linter tĩnh để đảm bảo bản thảo mới không dính từ cấm AI, không lặp từ n-gram và nhịp câu tự nhiên:
```bash
python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/<slug>" style-lint --chapter N
```

### 🔹 Bước 5: So sánh Diff & Đánh giá biên tập 7 chiều
* Tạo báo cáo so sánh giữa bản cũ và bản mới:
  ```bash
  python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/<slug>" diff --chapter N
  ```
* Chấm điểm 7 chiều theo [`rules/quality-checklist.md`](./quality-checklist.md):
  ```bash
  python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/<slug>" save-review --chapter N --data '<json_review>'
  ```

### 🔹 Bước 6: Trình bày cho Tác giả & Chờ lệnh
Hiển thị rõ ràng cho Tác giả:
1. **Tóm tắt thay đổi:** Những điểm cốt lõi đã được sửa.
2. **Text Diff:** Đoạn văn thay đổi trước/sau.
3. **Fact Diff:** Dòng thời gian, phục bút, nhân vật thay đổi thế nào.
4. **Điểm Quality Scorecard:** 7 chiều đánh giá và điểm trung bình.
5. **Hỏi ý kiến:** Chờ Tác giả duyệt `accept` hoặc yêu cầu sửa tiếp/`reject`.

### 🔹 Bước 7: Phê duyệt & Tái đồng bộ hệ thống (`accept` & `rebuild`)
Khi Tác giả duyệt:
```bash
python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/<slug>" accept --chapter N --rev "r00X"
```
* Engine sẽ tự động cập nhật `chapters/NN.md`, dựng lại toàn bộ `world/timeline.jsonl`, `world/foreshadow_ledger.json`, `characters/cast_ledger.json`, `world/relationships.json`, và `summaries/arcs/`.
* Nếu có các chương sau bị lệch logic, tự động đưa vào hàng đợi `pending_rewrites` để lên kế hoạch sửa tiếp.

---

## 🎯 3. BẢNG CHECKLIST BẮT BUỘC TRƯỚC KHI TRẢ LỜI NGƯỜI DÙNG

Trước khi đưa ra câu trả lời cuối cùng cho bất kỳ yêu cầu sửa truyện nào, AI Agent phải tự kiểm tra:

- [ ] Đã chạy `impact` để kiểm tra ảnh hưởng downstream chưa?
- [ ] Đã lưu nội dung sửa đổi vào `revisions/` chứ không ghi đè `chapters/` chưa?
- [ ] Đã trích xuất đầy đủ `facts` (timeline, foreshadows, cast, relationships) cho revision mới chưa?
- [ ] Đã chạy `style-lint` quét từ cấm AI chưa?
- [ ] Đã chạy `save-review` chấm điểm 7 chiều chưa?
- [ ] Đã hiển thị bản Diff trực quan cho tác giả duyệt chưa?
- [ ] Đã hướng dẫn tác giả dùng lệnh `accept` hoặc `reject` chưa?
