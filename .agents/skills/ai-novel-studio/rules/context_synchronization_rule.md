# 🔄 QUY TẮC BẮT BUỘC: ĐỒNG BỘ TOÀN DIỆN MỌI TỆP DỮ LIỆU LIÊN QUAN (MANDATORY CONTEXT SYNCHRONIZATION)

> **HIỆU LỰC TUYỆT ĐỐI:** Quy tắc này **BẮT BUỘC PHẢI ÁP DỤNG 100%** trong hai trường hợp:  
> 1. Khi bạn **cập nhật, viết mới, chỉnh sửa hoặc phê duyệt bất kỳ một chương nào**.  
> 2. Khi **Người dùng / Tác giả đưa ra bất kỳ yêu cầu, chỉ thị hoặc thay đổi mới nào** về cốt truyện, nhân vật, thế giới, phục bút hoặc cấu trúc tác phẩm.

---

## 🎯 1. NGUYÊN TẮC CỐT LÕI (ZERO STALE CONTEXT)

* **Tuyệt đối không để lại dữ liệu lệch pha (Stale Context):** Bất kỳ một sự kiện, manh mối hay quyết định nào được đưa ra trong văn bản chương hoặc trong yêu cầu của tác giả đều **BẮT BUỘC PHẢI ĐƯỢC PHẢN ÁNH ĐỒNG BỘ VÀO TOÀN BỘ CÁC TỆP CONTEXT PHỤ THUỘC**.
* **Đồng bộ hóa 2 chiều:**
  - *Từ Chương $\rightarrow$ Dữ liệu Context:* Viết chương xong phải cập nhật facts, timeline, phục bút, nhân vật, tóm tắt và progress.
  - *Từ Yêu Cầu Tác Giả $\rightarrow$ Thiết Lập & Kế Hoạch:* Tác giả yêu cầu đổi ý định gì phải cập nhật ngay vào outline, world rules, character ledger, directives và kích hoạt impact check.

---

## 📋 2. MA TRẬN ĐỒNG BỘ DỮ LIỆU BẮT BUỘC

### 🔹 Trường Hợp A: Khi Cập Nhật / Viết Mới / Phê Duyệt Chương $N$

Mỗi khi một revision chương $N$ được soạn thảo hoặc phê duyệt (`accept`), toàn bộ 9 tệp dữ liệu sau **BẮT BUỘC PHẢI ĐƯỢC CẬP NHẬT ĐỒNG THỜI**:

| STT | Tệp dữ liệu liên quan | Nội dung bắt buộc phải đồng bộ |
| :---: | :--- | :--- |
| **1** | `facts/NN/r00X.json` | Trích xuất đầy đủ sự thật: sự kiện mốc thời gian, phục bút gieo/tiến/thu, nhân vật xuất hiện, biến đổi quan hệ, trạng thái thế giới, dependencies. |
| **2** | `world/timeline.jsonl` | Dòng thời gian biên niên sử tự động cập nhật mốc sự kiện mới nhất của chương. |
| **3** | `world/foreshadow_ledger.json` | Cập nhật sổ phục bút: thêm phục bút mới (`plant`), đánh dấu tiến triển (`advance`), hoặc giải mã (`resolve`), tính lại tuổi chương (`age_chapters`). |
| **4** | `characters/cast_ledger.json` | Cập nhật hồ sơ nhân vật xuất hiện: vai trò, `first_seen`, và kéo dài `last_seen = N`. |
| **5** | `world/relationships.json` | Cập nhật trạng thái quan hệ mới giữa các cặp nhân vật (hoặc xóa quan hệ cũ nếu bị cắt đứt). |
| **6** | `world/state_changes.json` | Ghi nhận sự thay đổi trạng thái thế giới (ví dụ: lệnh phong tỏa, danh sách nạn nhân, vị trí đồ vật mật). |
| **7** | `summaries/NN.summary.json` & `summaries/arcs/` | Tạo tóm tắt chi tiết chương $N$ và tái tổng hợp tóm tắt Cung truyện tương ứng (`vX_aY.json`). |
| **8** | `meta/progress.json` | Cập nhật `current_chapter = N + 1`, tổng số từ `total_word_count`, danh sách `completed_chapters`, vị trí Tập/Cung. |
| **9** | `decisions.jsonl` | Ghi nhận bản ghi kiểm toán quyết định (action, actor, chapter, revision, reason). |

---

### 🔹 Trường Hợp B: Khi Có Yêu Cầu / Chỉ Thị Mới Từ Tác Giả

Mỗi khi Tác giả yêu cầu thay đổi thiết lập, đổi tính cách nhân vật, đổi luật thế giới, hoặc đổi hướng đi của cốt truyện:

| STT | Tệp dữ liệu cần cập nhật | Hành động bắt buộc |
| :---: | :--- | :--- |
| **1** | `outlines/premise.md` / `layered_outline.json` | Cập nhật lại đề cương tác phẩm hoặc sơ đồ phân lớp Cung/Tập theo hướng đi mới. |
| **2** | `characters/characters.json` | Cập nhật hồ sơ nhân vật gốc (tính cách, động cơ, bí mật, năng lực). |
| **3** | `world/world_rules.json` | Cập nhật quy tắc thế giới, bối cảnh không gian, dòng thời gian lịch sử. |
| **4** | `meta/directives.json` | Lưu lại chỉ thị định hướng của tác giả để các subagent luôn tuân thủ. |
| **5** | `impact --chapter X` | Chạy phân tích ảnh hưởng ngay lập tức để xác định các chương cũ nào bị lệch logic và đưa vào `pending_rewrites`. |
| **6** | `decisions.jsonl` | Ghi nhật ký quyết định ghi rõ yêu cầu mới của tác giả và lý do điều chỉnh. |

---

## 🛠️ 3. CƠ CHẾ ĐỒNG BỘ HÓA TỰ ĐỘNG CỦA ENGINE

1. **Sau khi chạy lệnh `accept --chapter N`:** Engine sẽ tự động chạy quy trình `rebuild_all_projections()` để tái tạo 100% các file Projections (`timeline`, `foreshadow_ledger`, `cast_ledger`, `relationships`, `state_changes`, `summaries/arcs/`).
2. **Khi có nghi vấn dữ liệu bị lệch pha:** AI Agent **BẮT BUỘC** phải chủ động chạy lệnh:
   ```bash
   python .agents/skills/ai-novel-studio/scripts/novel_state.py --dir "novels/<slug>" rebuild
   ```
   để Engine quét lại toàn bộ các Fact có hiệu lực và tái tạo ngữ cảnh chuẩn xác nhất.

---

## 🛑 4. CHECKLIST BẮT BUỘC TRƯỚC KHI BÁO CÁO HOÀN THÀNH

Trước khi xác nhận hoàn thành bất kỳ lượt trả lời nào với người dùng:

- [ ] Đã cập nhật đầy đủ tệp `facts/` cho revision chương mới/sửa đổi chưa?
- [ ] Dòng thời gian (`timeline.jsonl`) và Sổ phục bút (`foreshadow_ledger.json`) đã được cập nhật chưa?
- [ ] Hồ sơ nhân vật (`cast_ledger.json`) và Quan hệ (`relationships.json`) đã khớp với diễn biến mới chưa?
- [ ] Tóm tắt chương (`summaries/`) và tiến độ (`progress.json`) đã được cập nhật chưa?
- [ ] Nếu có yêu cầu mới của tác giả về đề cương/thế giới/nhân vật, các tệp trong `outlines/`, `world/`, `characters/` đã được lưu chưa?
- [ ] Đã ghi nhận quyết định vào `decisions.jsonl` chưa?
