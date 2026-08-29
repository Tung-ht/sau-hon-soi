# 📚 AI Novel Studio 2.0 — Hướng Dẫn Sử Dụng Toàn Diện

> **Kiến trúc:** Agent-Led, Engine-Guarded (Đồng tác giả thông minh)  
> **Tối ưu hóa cho:** Gemini 3.7 Flash High & Antigravity  
> **Phiên bản:** 2.0 Enterprise (Đạt chuẩn Production-Ready)

---

## 🌟 1. Giới Thiệu Tổng Quan

**AI Novel Studio 2.0** là hệ thống đồng sáng tác tiểu thuyết phân tầng tự chủ, kết hợp giữa sự linh hoạt, sáng tạo tự nhiên của **AI Agent** và sự an toàn, kỷ luật dữ liệu tuyệt đối của **Python Guarded Engine**.

### 🎯 Triết Lý "Agent-Led, Engine-Guarded":
* **Bạn & AI Agent quyết định sáng tác:** Không còn máy trạng thái (FSM) ép buộc. Bạn có thể tự do lập kế hoạch, viết nháp, rẽ nhánh thử nghiệm, sửa chương cũ hoặc nhảy cóc theo ý muốn.
* **Engine bảo vệ dữ liệu 100%:** Ghi file nguyên tử (Atomic Write), quản lý lịch sử revision bất biến (`r001`, `r002`), tự động dựng lại toàn bộ dòng thời gian và phục bút từ Facts (Event Sourcing), khóa đa tác nhân (`StudioLock`), và cơ chế phục hồi Snapshot hai pha (Two-Phase Atomic Swap).

```text
       Bạn ↔ AI Agent (Gemini 3.7 Flash)
                    │
                    ├─ Dashboard `status` & `suggest-next` (Đề xuất bước đi tiếp theo)
                    ├─ Lập kế hoạch `plan` / Viết bản thảo `draft` (Revision-First an toàn)
                    ├─ So sánh `diff` (Text Diff & Fact Diff) / Rẽ nhánh `branch A/B`
                    ├─ Đánh giá biên tập `save-review` / Quét phong cách `style-lint`
                    └─ Phê duyệt `accept` hoặc `reject`
                            │
                    Studio Core Engine
                    ├─ Multi-Agent Lock (`StudioLock` liveness & heartbeat)
                    ├─ Revision State Machine (`pending` → `accepted` / `rejected` → `superseded`)
                    ├─ Dynamic Projection Builder (Rebuild Timeline, Foreshadows, Cast, Arcs)
                    ├─ Two-Phase Disaster Recovery (Staging Snapshot Swap & Projections Rollback)
                    └─ Quality Gate Policy (Strict vs Advisory)
                            │
                    Novel Store (novels/<slug>/)
```

---

## 📁 2. Cấu Trúc Thư Mục Dự Án

Workspace hỗ trợ **không giới hạn số lượng tiểu thuyết** cùng lúc. Mỗi bộ truyện được cách ly hoàn toàn trong `novels/<slug>/`:

```text
c:\zNovel/
├── .agents/skills/ai-novel-studio/   # Mã nguồn Skill Studio & Rules
│   ├── scripts/studio/               # Gói mô-đun Engine (store, revision, projector, quality, snapshot, cli)
│   ├── rules/                        # Quy chuẩn văn phong & kiểm soát chất lượng
│   └── tests/                        # Bộ kiểm thử tự động cố định
│
└── novels/
    └── loi-tran-troi/                # Một bộ tiểu thuyết cụ thể
        ├── meta/
        │   ├── progress.json         # Tiến độ, số từ, tập/cung, accepted map
        │   ├── config.json           # Cấu hình mode (guided/manual/auto), quality gate
        │   └── checkpoints/          # Các bản sao lưu Snapshot Zip an toàn
        ├── outlines/                 # Premise, Layered Outline, Compass
        ├── characters/               # Cast Ledger (Hồ sơ nhân vật tự động cập nhật)
        ├── world/
        │   ├── timeline.jsonl        # Dòng thời gian tự động dựng từ Facts đã duyệt
        │   ├── foreshadow_ledger.json# Sổ tay phục bút tự động theo dõi tuổi & trạng thái
        │   ├── relationships.json    # Mạng lưới quan hệ nhân vật
        │   └── reviews/              # Bảng chấm điểm 7 chiều từng chương
        ├── revisions/                # Kho lưu trữ bản thảo bất biến (01/r001.md, 01/r002.md)
        ├── facts/                    # Sự thật dữ liệu từng revision (01/r001.json)
        ├── drafts/                   # Bản nháp và kế hoạch chương đang soạn
        ├── chapters/                 # Bản chính thức của các chương đã được DUYỆT (01.md, 02.md)
        ├── summaries/arcs/           # Tóm tắt phân cấp theo từng Cung truyện
        └── decisions.jsonl           # Nhật ký kiểm toán mọi quyết định của tác giả & AI
```

---

## ⚙️ 3. Ba Chế Độ Tương Tác (`interaction_mode`)

Bạn có thể chuyển đổi chế độ bất kỳ lúc nào bằng lệnh `set-mode`:

1. **`guided` (Mặc định & Khuyến nghị):**
   * AI tự động lập dàn ý, viết nháp chương, tự soát lỗi, nhưng **dừng lại trước khi commit** để bạn duyệt Diff và bấm `accept`.
   * Phù hợp cho việc đồng sáng tác hàng ngày: AI làm việc nặng, bạn giữ quyền kiểm soát tối cao.
2. **`manual` (Thủ công tuyệt đối):**
   * Mọi bước đi (từ kế hoạch, bản thảo đến biên tập) đều cần sự xác nhận và chỉ đạo chi tiết của bạn.
3. **`auto` (Tự động hóa):**
   * Đề xuất các luồng tự động chấp nhận và viết liên tục, phù hợp cho việc cắm máy thử nghiệm viết hàng loạt.

---

## 🚀 4. Hướng Dẫn Quy Trình Sáng Tác Từ A Đến Z

### 🔹 Bước 1: Khởi tạo tác phẩm mới hoặc Nhập truyện cũ
* **Tạo truyện mới:**
  ```bash
  python .agents/skills/ai-novel-studio/scripts/novel_state.py init --name "Tên Truyện Mới" --scale long --premise "Giới thiệu tác phẩm..."
  ```
* **Nhập truyện có sẵn từ file text thô:**
  ```bash
  python .agents/skills/ai-novel-studio/scripts/novel_state.py import-novel --file "ban_thao.txt" --name "Tên Truyện"
  ```
* **Xem danh sách tất cả các tiểu thuyết hiện có:**
  ```bash
  python .agents/skills/ai-novel-studio/scripts/novel_state.py list-novels
  ```

---

### 🔹 Bước 2: Kiểm tra Dashboard & Đề xuất hành động
Trước khi viết, luôn kiểm tra tình trạng tổng thể của bộ truyện:
```bash
python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/loi-tran-troi" status
```
* **Kết quả trả về:** Tiến độ chương, tổng số từ, vị trí hiện tại (Tập X · Cung Y), danh sách bản nháp chờ duyệt, các phục bút đang mở (kèm cảnh báo phục bút già hóa $\ge 30$ chương) và 2–3 đề xuất hợp lý nhất.

---

### 🔹 Bước 3: Lập kế hoạch chương mới (`plan`)
Ký kết Hợp đồng chương (Chapter Contract) đảm bảo không bị lạc đề:
```bash
python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/loi-tran-troi" plan --chapter 11 --data '{
  "goal": "Nam thâm nhập vào kho lưu trữ tài liệu mật",
  "scenes": ["Đêm mưa trước cổng kho", "Vượt qua trạm gác", "Mở két sắt tìm thấy tài liệu K-19"],
  "required_beats": ["Gặp người gác cổng mù", "Tìm thấy hồ sơ bị cháy một góc"],
  "hook_goal": "Phát hiện dấu vân tay của người quen trên mép tài liệu"
}'
```

---

### 🔹 Bước 4: Viết bản thảo an toàn (`draft` / `branch`)
Soạn bản thảo mới (bản chính `chapters/` **chưa bị đè**, dữ liệu được lưu an toàn vào `revisions/11/r001.md`):
```bash
python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/loi-tran-troi" draft --chapter 11 --content-file "draft_ch11.md" --facts '{
  "summary": "Nam đột nhập vào kho tài liệu mật và phát hiện hồ sơ K-19.",
  "timeline_events": [{"time": "23:00", "event": "Nam đột nhập kho lưu trữ"}],
  "foreshadow_updates": [{"id": "ho_so_k19", "description": "Hồ sơ K-19 bị cháy mép", "action": "plant", "status": "active"}],
  "cast": [{"name": "Nam", "brief_role": "Thám tử"}, {"name": "Ông lão mù", "brief_role": "Người gác kho"}]
}'
```

* **Muốn thử nghiệm phương án khác (Rẽ nhánh A/B)?**
  ```bash
  python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/loi-tran-troi" branch --chapter 11 --name "huong_kich_tinh" --content "Nội dung phương án rẽ nhánh..."
  ```

---

### 🔹 Bước 5: So sánh Diff & Phê duyệt (`diff` & `accept`)
* **Xem Text Diff & Fact Diff giữa hai bản nháp hoặc với bản chính:**
  ```bash
  python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/loi-tran-troi" diff --chapter 11
  ```
* **Chấp nhận revision làm bản chính thức:**
  ```bash
  python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/loi-tran-troi" accept --chapter 11 --rev "r001"
  ```
  *(Khi bạn gõ lệnh này, Engine tự động cập nhật `chapters/11.md`, đồng thời tái tạo lại 100% dòng thời gian, hồ sơ nhân vật và tóm tắt Cung truyện).*

---

### 🔹 Bước 6: Kiểm soát văn phong & Đánh giá chất lượng
* **Quét linter chống văn mẫu AI & đếm từ lặp:**
  ```bash
  python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/loi-tran-troi" style-lint --chapter 11
  ```
* **Lưu bảng đánh giá biên tập 7 chiều:**
  ```bash
  python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/loi-tran-troi" save-review --chapter 11 --data '{
    "dimensions": [
      {"dimension": "consistency", "score": 85},
      {"dimension": "character", "score": 90},
      {"dimension": "continuity", "score": 85},
      {"dimension": "pacing", "score": 80},
      {"dimension": "foreshadow", "score": 85},
      {"dimension": "hook", "score": 85},
      {"dimension": "aesthetic", "score": 85}
    ],
    "contract_status": "met",
---

## 🚨 5. Quy Định Bắt Buộc Khi Chỉnh Sửa & Viết Lại Tiểu Thuyết

Bất cứ khi nào nhận được yêu cầu **sửa truyện, sửa chương, viết lại, đổi tình tiết, chỉnh văn phong**, AI Agent **BẮT BUỘC** phải tuân thủ 100% quy trình trong [`rules/mandatory-revision-workflow.md`](./rules/mandatory-revision-workflow.md):

1. **Phân tích ảnh hưởng (`impact`):** Quét các chương phía sau và các tuyến phục bút bị tác động trước khi sửa.
2. **Nạp đúng ngữ cảnh (`context`):** Nạp gói bộ nhớ 4 tầng tương ứng với chương đang sửa.
3. **Soạn bản thảo dưới dạng Revision mới (`draft` hoặc `branch`):** Tuyệt đối **CẤM** ghi đè trực tiếp vào `chapters/`. Phải đính kèm `facts` cập nhật mới.
4. **Kiểm tra văn phong thuần Việt:** Áp dụng [`rules/vietnamese-novel-prose.md`](./rules/vietnamese-novel-prose.md), [`rules/anti-ai-tone.md`](./rules/anti-ai-tone.md) và chạy `style-lint`.
5. **So sánh Diff & Đánh giá 7 chiều:** Chạy `diff` để hiển thị Text Diff/Fact Diff cho tác giả và chạy `save-review` theo [`rules/quality-checklist.md`](./quality-checklist.md).
---

## 🔄 6. Quy Định Bắt Buộc Về Đồng Bộ Toàn Diện Ngữ Cảnh (Zero Stale Context)

Theo [`rules/context_synchronization_rule.md`](./rules/context_synchronization_rule.md), khi có bất kỳ thay đổi nào từ văn bản chương hoặc từ yêu cầu của tác giả, toàn bộ các tệp dữ liệu sau **BẮT BUỘC PHẢI ĐƯỢC CẬP NHẬT ĐỒNG BỘ 100%**:

* **Khi cập nhật / viết / duyệt 1 chương:**
  - `facts/NN/r00X.json`: Trích xuất sự kiện, phục bút, nhân vật, quan hệ, trạng thái thế giới.
  - `world/timeline.jsonl`: Cập nhật dòng thời gian sự kiện.
  - `world/foreshadow_ledger.json`: Cập nhật trạng thái phục bút (`plant`, `advance`, `resolve`, tuổi chương).
  - `characters/cast_ledger.json`: Cập nhật `last_seen` và vai trò nhân vật.
  - `world/relationships.json`: Cập nhật quan hệ nhân vật.
  - `world/state_changes.json`: Cập nhật biến số trạng thái thế giới.
  - `summaries/` & `summaries/arcs/`: Tóm tắt chương và tóm tắt Cung truyện.
  - `meta/progress.json`: Số từ, chương hiện tại, tập/cung.
  - `decisions.jsonl`: Ghi nhận nhật ký quyết định.
* **Khi Tác giả đưa ra yêu cầu mới:** Cập nhật ngay `outlines/premise.md`, `layered_outline.json`, `characters/characters.json`, `world/world_rules.json`, `meta/directives.json`, chạy ngay `impact --chapter X` để tìm các chương bị ảnh hưởng, và ghi nhận vào `decisions.jsonl`.

---

### 🔹 Bước 7: Sao lưu Snapshot & Xuất bản
* **Tạo điểm lưu dự án (Checkpoint Zip):**
  ```bash
  python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/loi-tran-troi" snapshot create --name "truoc_khi_danh_lon" --note "Lưu trước trận chiến lớn"
  ```
* **Khôi phục lại dữ liệu khi cần (An toàn 100% qua Two-Phase Swap):**
  ```bash
  python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/loi-tran-troi" snapshot restore --name "truoc_khi_danh_lon"
  ```
* **Xuất toàn bộ tác phẩm thành một file Markdown duy nhất:**
  ```bash
  python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/loi-tran-troi" export
  ```

---

## 📖 5. Bảng Tra Cứu Toàn Bộ Lệnh CLI

| Lệnh CLI | Tham số chính | Chức năng |
| :--- | :--- | :--- |
| `list-novels` | `[--root <path>]` | Liệt kê tất cả các bộ truyện trong workspace |
| `init` | `--name <str> [--scale short\|mid\|long] [--premise <str>] [--force] [--resume]` | Khởi tạo tiểu thuyết mới (có guard chống xóa đè) |
| `set-mode` | `--mode <manual\|guided\|auto>` | Thay đổi chính sách điều phối tương tác của Studio |
| `status` | | **Dashboard tổng thể:** Tiến độ, số từ, draft pending, phục bút mở, đề xuất |
| `suggest-next` | | Đưa ra 2–3 hướng hành động tiếp theo dựa trên trạng thái thực tế |
| `summary` | `[--chapter N]` | Xem tóm tắt phân cấp theo từng chương hoặc theo Cung truyện |
| `threads` | | Danh sách các phục bút và tuyến truyện đang mở kèm số chương tuổi |
| `context` | `--chapter N` | Lắp ráp gói bộ nhớ 4 tầng nạp ngữ cảnh cho việc viết chương N |
| `plan` | `--chapter N <--data <json> \| --file <path>>` | Ký kết hợp đồng chương (Goal, Scenes, Required Beats) |
| `draft` | `--chapter N <--content <str> \| --content-file <path>> [--facts <json>] [--mode write\|append]` | Soạn bản thảo thành revision mới an toàn |
| `branch` | `--chapter N --name <str> <--content <str> \| --content-file <path>>` | Rẽ nhánh A/B thử nghiệm diễn biến cốt truyện khác |
| `diff` | `--chapter N [--rev-a <id>] [--rev-b <id>]` | So sánh Text Diff và Fact Diff trực quan |
| `accept` | `--chapter N [--rev <id>] [--reason <str>] [--force]` | Duyệt revision làm bản chính $\rightarrow$ Rebuild 100% Projections |
| `reject` | `--chapter N [--rev <id>] [--reason <str>] [--force]` | Hủy bỏ bản nháp mà không ảnh hưởng bản chính |
| `impact` | `--chapter N` | Phân tích ảnh hưởng của việc sửa chương N lên các chương sau |
| `rebuild` | | Tái tạo lại toàn bộ Projections (Timeline, Foreshadows, Cast, Arcs) từ Facts |
| `style-lint` | `[--chapter N]` | Linter tĩnh: quét từ cấm AI, đếm lặp n-gram, kiểm tra nhịp điệu |
| `save-review`| `--chapter N <--data <json> \| --file <path>>` | Lưu bảng điểm biên tập 7 chiều có kiểm soát Quality Gate |
| `snapshot` | `create --name <str> \| list \| restore --name <str>` | Tạo và khôi phục checkpoint Zip an toàn tuyệt đối |
| `export` | `[--output <path>]` | Xuất toàn bộ tiểu thuyết thành 1 file Markdown hoàn chỉnh |

---

## 🛡️ 6. Kiểm Thử Tự Động (Automated Test Suite)

Gói skill được tích hợp sẵn bộ kiểm thử đơn vị và kiểm thử chịu tải đa tác nhân chuẩn mực trong thư mục `tests/`:

```bash
python -m unittest discover -s .agents/skills/ai-novel-studio/tests -p "test_*.py"
```
* **`test_core_studio.py`:** Kiểm thử toàn bộ chu trình Plan $\rightarrow$ Draft $\rightarrow$ Accept $\rightarrow$ Projections $\rightarrow$ Quality Review.
* **`test_fault_recovery.py`:** Kiểm thử khả năng chịu lỗi, chứng minh Snapshot ZIP hỏng không bao giờ làm mất dữ liệu truyện.
* **`test_concurrency.py`:** Kiểm thử 8 tác nhân đồng thời truy cập qua `StudioLock` mà không bị đụng độ tài nguyên hay xung đột revision.
