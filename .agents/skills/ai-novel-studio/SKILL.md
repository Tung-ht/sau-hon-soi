---
name: ai-novel-studio
description: >-
  Hệ thống sáng tác tiểu thuyết phân tầng tự chủ đa tác nhân (Autonomous Hierarchical Multi-Agent Novel Writing Studio)
  tối ưu cho Gemini 3.7 Flash theo mô hình Agent-Led, Engine-Guarded. TỰ ĐỘNG KÍCH HOẠT khi người dùng yêu cầu:
  "viết tiểu thuyết", "sáng tác truyện", "viết truyện", "tiếp tục viết chương", "sửa chương X", "sửa truyện",
  "chỉnh sửa chương", "viết lại chương", "viết lại", "tinh chỉnh văn phong", "đổi tình tiết", "sửa nhân vật",
  "fix cốt truyện", "lập dàn ý tiểu thuyết", "ai novel", "viết tiếp truyện", "tiến độ truyện", "so sánh bản nháp".
---

# 📚 AI Novel Studio 2.0 (Agent-Led, Engine-Guarded Architecture)

Hệ thống hoạt động theo triết lý **"Bạn & AI Agent quyết định sáng tác; Engine Python bảo vệ tính nhất quán, phiên bản và dữ liệu"**.

```text
       Bạn ↔ AI Agent (Gemini 3.7 Flash High)
                    │
                    ├─ Dashboard `status` & `suggest-next` (Đề xuất 2-3 hướng đi)
                    ├─ Kế hoạch `plan` / Viết bản thảo `draft` (Tạo revision an toàn)
                    ├─ So sánh `diff` (Text Diff & Fact Diff)
                    ├─ Phân tích ảnh hưởng `impact` / Rẽ nhánh `branch A/B`
                    └─ Quyết định `accept` hoặc `reject`
                            │
                    Studio Core Engine
                    ├─ Multi-Agent Lock (`StudioLock` liveness & heartbeat)
                    ├─ Revision Manager (r001, r002, facts, decisions.jsonl)
                    ├─ Projection Engine (Rebuild timeline, foreshadows, cast từ facts)
                    ├─ Context Assembler (4-Tier memory + Aging >= 30)
                    ├─ Two-Phase Disaster Recovery (Staging Snapshot Swap & Rollback)
                    └─ Quality Gate Policy (Strict vs Advisory)
                            │
                     Novel Store (novels/<slug>/)
```

---

## 🎯 1. Triết Lý & Ba Chế Độ Tương Tác

### A. Hard Guards vs. Soft Gates
- **Hard Guards (Bảo vệ cứng - Bắt buộc 100%):** Ghi file nguyên tử (Atomic Write), bảo toàn lịch sử revision (`r001`, `r002`), không ghi đè bản chính khi chưa được duyệt, khóa đa tác nhân `StudioLock`, tự động tái tạo Projections (timeline, phục bút, nhân vật) chuẩn xác từ Facts sạch.
- **Soft Gates (Cổng kiểm soát mềm - Tác giả có quyền Override):** Điểm review, độ dài chương, chapter contract, linter từ lặp. Nếu Override, hệ thống ghi lại lý do vào `decisions.jsonl` mà không làm nghẽn mạch sáng tác.

### B. Ba Chế Độ Tương Tác (`interaction_mode` trong `meta/config.json`)
1. **`guided` (Mặc định & Khuyến nghị):** AI tự động thực hiện chu trình `plan` $\rightarrow$ `draft` $\rightarrow$ `self-review`, nhưng **dừng lại trước khi commit và trước khi cascading rewrite** để hiển thị diff và xin ý kiến bạn.
2. **`manual`:** AI đề xuất từng bước nhỏ; mọi draft/revision đều chờ bạn gõ `accept`.
3. **`auto`:** Chạy tự động liên tục, phù hợp cho việc cắm máy thử nghiệm viết hàng loạt.

---

## 🚨 2. QUY TẮC BẮT BUỘC KHI CHỈNH SỬA / VIẾT LẠI TIỂU THUYẾT (MANDATORY)

> **QUY ĐỊNH BẮT BUỘC 100%:** Bất cứ khi nào người dùng nhắc đến **"sửa truyện", "sửa chương X", "chỉnh sửa", "viết lại", "viết lại chương", "tinh chỉnh văn phong", "đổi tình tiết", "sửa nhân vật", "fix cốt truyện"**, AI Agent **BẮT BUỘC PHẢI THỰC THI TOÀN BỘ WORKFLOW VÀ TẤT CẢ CÁC RULE SAU ĐÂY** theo [`rules/mandatory-revision-workflow.md`](./rules/mandatory-revision-workflow.md):

1. **TUYỆT ĐỐI CẤM** sửa trực tiếp vào file chính `chapters/XX.md`. Mọi chỉnh sửa bắt buộc phải tạo **Revision mới** qua `draft --chapter N` hoặc `branch --chapter N`.
2. **Bắt buộc phân tích ảnh hưởng (Impact Analysis):** Luôn chạy `impact --chapter N` để quét các chương sau và phục bút bị ảnh hưởng trước khi sửa.
3. **Bắt buộc nạp đúng ngữ cảnh:** Gọi `context --chapter N` để lấy bộ nhớ 4 tầng của đúng thời điểm chương đó.
4. **Bắt buộc trích xuất Facts đầy đủ:** Mọi revision sửa đổi phải đi kèm `facts` (timeline events, foreshadow updates, cast, relationship changes, state changes) để không làm đứt gãy continuity.
5. **Bắt buộc tuân thủ bộ quy chuẩn văn phong:**
   - [`rules/vietnamese-novel-prose.md`](./rules/vietnamese-novel-prose.md): Văn phong thuần Việt, ngũ giác, show don't tell.
   - [`rules/anti-ai-tone.md`](./rules/anti-ai-tone.md): Triệt tiêu văn convert, cấm từ sáo rỗng AI.
   - Chạy `style-lint --chapter N` để kiểm tra tĩnh.
6. **Bắt buộc hiển thị Diff & Đánh giá 7 chiều:**
   - Chạy `diff --chapter N` để hiển thị Text Diff và Fact Diff trực quan cho tác giả.
   - Chạy `save-review --chapter N` theo [`rules/quality-checklist.md`](./quality-checklist.md).
7. **Bắt buộc chờ Tác giả duyệt `accept`:** Khi tác giả gõ `accept`, Engine sẽ tự động chạy `rebuild` để cập nhật lại toàn bộ Projections.

---

## 🔄 3. QUY TẮC BẮT BUỘC ĐỒNG BỘ TOÀN DIỆN MỌI TỆP LIÊN QUAN (ZERO STALE CONTEXT)

> **QUY ĐỊNH BẮT BUỘC 100%:** Khi **cập nhật/viết/sửa bất kỳ chương nào** hoặc **khi có bất kỳ yêu cầu mới nào từ Tác giả** (về nhân vật, đề cương, luật thế giới, phục bút), AI Agent và Engine **BẮT BUỘC PHẢI CẬP NHẬT ĐỒNG THỜI TOÀN BỘ CÁC TỆP LIÊN QUAN** theo [`rules/context_synchronization_rule.md`](./rules/context_synchronization_rule.md):

* **Khi cập nhật chương:** Đồng bộ ngay `facts/`, `timeline.jsonl`, `foreshadow_ledger.json`, `cast_ledger.json`, `relationships.json`, `state_changes.json`, `summaries/`, `progress.json` và `decisions.jsonl`.
* **Khi có yêu cầu/chỉ thị mới từ tác giả:** Đồng bộ ngay `outlines/`, `characters/characters.json`, `world/world_rules.json`, `meta/directives.json`, chạy ngay `impact` để tìm các chương bị ảnh hưởng, và ghi lại vào `decisions.jsonl`.
* **Chủ động Rebuild:** Luôn chạy `rebuild` nếu phát hiện bất kỳ sự lệch pha dữ liệu nào.

---

## 🛠️ 4. Bộ Lệnh CLI Tương Tác Studio

| Lệnh CLI | Chức năng chính |
| :--- | :--- |
| `python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/slug" status` | **Dashboard tổng quan:** Tiến độ, số từ, draft chờ duyệt, tuyến mở, cảnh báo, 2–3 đề xuất |
| `python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/slug" suggest-next` | Đề xuất các lựa chọn bước tiếp theo kèm lý do |
| `python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/slug" summary [--chapter N]` | Tóm tắt phân cấp theo chương / cung / tập |
| `python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/slug" threads` | Danh sách các tuyến truyện và phục bút đang mở kèm số chương tuổi |
| `python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/slug" context --chapter N` | Lắp ráp gói ngữ cảnh 4 tầng để viết chương N |
| `python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/slug" plan --chapter N <--data <json> \| --file <path>>` | Ký kết hợp đồng chương (Goal, Scenes, Required Beats, Hook) |
| `python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/slug" draft --chapter N <--content <text> \| --content-file <path>> [--facts <json>]` | Soạn bản thảo dưới dạng **Revision mới** (không ghi đè bản chính) |
| `python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/slug" branch --chapter N --name <str> <--content <text> \| --content-file <path>>` | Rẽ nhánh A/B thử nghiệm phương án khác |
| `python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/slug" diff --chapter N [--rev-a r001 --rev-b r002]` | So sánh Text Diff & Fact Diff giữa hai bản nháp hoặc bản chính |
| `python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/slug" accept --chapter N [--rev r002]` | **Chấp nhận revision làm bản chính** $\rightarrow$ Dựng lại 100% Projections |
| `python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/slug" reject --chapter N [--rev r002]` | Hủy bỏ bản nháp mà không tác động tới bản chính |
| `python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/slug" impact --chapter N` | Phân tích ảnh hưởng của việc sửa chương N lên các chương sau |
| `python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/slug" rebuild` | Dựng lại toàn bộ Projections (Timeline, Foreshadows, Cast, Arcs) từ Facts |
| `python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/slug" style-lint [--chapter N]` | Quét từ cấm AI, đếm từ lặp n-gram, kiểm tra nhịp điệu câu |
| `python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/slug" save-review --chapter N <--data <json> \| --file <path>>` | Chấm điểm biên tập 7 chiều có kiểm soát Quality Gate |
| `python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/slug" snapshot <create|list|restore>` | Tạo điểm lưu (checkpoint zip) & Rollback 2 pha an toàn 100% |
| `python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/slug" export` | Xuất toàn bộ tiểu thuyết thành file Markdown duy nhất |

---

## 📖 4. Chu Trình Viết Mới & Sáng Tác Tiếp

1. **Bước 1 - Kiểm tra Dashboard & Đề xuất:** Agent chạy `status` hoặc `suggest-next`.
2. **Bước 2 - Lấy ngữ cảnh 4 tầng:** Agent gọi `context --chapter N`.
3. **Bước 3 - Lập kế hoạch chương (`plan`):** Agent ký chapter contract theo [`rules/chapter-contract.md`](./rules/chapter-contract.md).
4. **Bước 4 - Viết bản thảo an toàn (`draft`):** Áp dụng [`rules/vietnamese-novel-prose.md`](./rules/vietnamese-novel-prose.md) và [`rules/anti-ai-tone.md`](./rules/anti-ai-tone.md). Lưu vào revision mới qua `draft --chapter N`.
5. **Bước 5 - Đối chiếu & Xem Diff (`diff`):** Hiển thị Text Diff và Fact Diff cho tác giả duyệt.
6. **Bước 6 - Phê duyệt (`accept`):** Khi tác giả duyệt `accept`, Engine tự động cập nhật `chapters/NN.md` và tái tạo lại 100% dòng thời gian & phục bút.
