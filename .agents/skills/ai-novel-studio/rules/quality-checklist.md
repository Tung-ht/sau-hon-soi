# 📋 7-Dimensional Editorial Quality Scorecard
*(Bảng kiểm định chất lượng biên tập 7 chiều)*

Editor Subagent bắt buộc phải sử dụng bảng kiểm định 7 chiều này để rà soát bản thảo chương trước khi quyết định `accept` (chấp nhận), `polish` (trau chuốt lại) hoặc `rewrite` (viết lại hoàn toàn).

---

## 1. Bảy Chiều Đánh Giá (7 Evaluation Dimensions)

| Chiều (Dimension) | Thang điểm | Yêu cầu kiểm tra & Tiêu chí đạt chuẩn | Hậu quả khi dưới chuẩn |
| :--- | :---: | :--- | :--- |
| **1. `consistency` (Tính nhất quán)** | 0 - 100 | Nhân vật, bối cảnh, mốc thời gian, năng lực/sức mạnh có mâu thuẫn với các chương trước không? | $< 60$: Nâng cấp thành **Rewrite** |
| **2. `character` (Tính cách nhân vật)** | 0 - 100 | Lời nói, hành vi, động cơ nhân vật có nhất quán với hồ sơ (`characters.json`) không? Có bị OOC (Out of Character) không? | $< 60$: Nâng cấp thành **Rewrite** |
| **3. `continuity` (Tính liên tục)** | 0 - 100 | Chương này có kế thừa mượt mà từ kết thúc chương trước không? Có bước nhảy logic nào thiếu giải thích không? | $< 60$: Nâng cấp thành **Rewrite** |
| **4. `pacing` (Nhịp điệu cốt truyện)** | 0 - 100 | Nhịp truyện có bị lê thê giải thích quá nhiều, hoặc dồn ép sự kiện quá nhanh khiến người đọc bị hụt hơi không? | $< 60$: Nâng cấp thành **Polish** |
| **5. `foreshadow` (Phục bút & Manh mối)** | 0 - 100 | Các phục bút cũ có được đẩy tiến/thu hồi hợp lý không? Manh mối mới cài cắm có tự nhiên không? | $< 60$: Cảnh báo (Warning) |
| **6. `hook` (Móc câu cuối chương)** | 0 - 100 | Đuôi chương có để lại điểm neo căng thẳng (khủng hoảng, bí ẩn, cảm xúc, lựa chọn) kích thích đọc tiếp không? | $< 60$: Nâng cấp thành **Polish** |
| **7. `aesthetic` (Thẩm mỹ & Văn phong)** | 0 - 100 | Văn phong có bị sáo rỗng, dính từ cấm AI (xem `anti-ai-tone.md`), từ lặp quá nhiều, hoặc lời thoại khô cứng không? | $< 60$: Nâng cấp thành **Polish** |

---

## 2. Quy Tắc Nâng Cấp Verdict Tự Động (Scorecard Gate)

* **`accept` (Thông qua):**
  - Tất cả 7 chiều đều $\ge 80$ điểm.
  - Hợp đồng chương (`contract_status`) đạt `met`.
* **`polish` (Trau chuốt):**
  - Có chiều đạt từ $60 - 79$ điểm, hoặc chiều `aesthetic`/`pacing`/`hook` $< 60$.
  - Hợp đồng chương đạt `partial`.
* **`rewrite` (Viết lại toàn bộ):**
  - Bất kỳ chiều quan trọng nào (`consistency`, `character`, `continuity`) rơi vào $< 60$ điểm.
  - Hợp đồng chương bị `missed` (bỏ sót hoàn toàn sự kiện cốt lõi đã cam kết).

---

## 3. Định Dạng Kết Quả Đánh Giá (`Review JSON Schema`)

Editor Subagent xuất kết quả đánh giá theo cấu trúc chuẩn:

```json
{
  "chapter": 5,
  "scope": "chapter",
  "contract_status": "met",
  "contract_misses": [],
  "verdict": "accept",
  "summary": "Chương 5 có nhịp điệu dồn dập, giải quyết tốt nút thắt về thân thế của Hoàng, móc câu cuối chương xuất sắc.",
  "dimensions": [
    {"dimension": "consistency", "score": 90, "comment": "Dữ liệu thời gian và địa điểm hoàn toàn khớp với chương 4."},
    {"dimension": "character", "score": 85, "comment": "Thái độ gằn giọng của Nam thể hiện đúng tâm lý bức xúc."},
    {"dimension": "continuity", "score": 90, "comment": "Nối tiếp hoàn hảo từ tách trà vỡ ở cuối chương 4."},
    {"dimension": "pacing", "score": 85, "comment": "Đoạn đối chất có độ căng tốt, không bị dông dài."},
    {"dimension": "foreshadow", "score": 80, "comment": "Đã cài thêm chi tiết chiếc nhẫn bạc của lão Tứ."},
    {"dimension": "hook", "score": 90, "comment": "Kết thúc bằng phát súng trong đêm, kích thích người đọc."},
    {"dimension": "aesthetic", "score": 85, "comment": "Không dính từ cấm AI, đối thoại gãy gọn."}
  ],
  "issues": [],
  "affected_chapters": []
}
```
