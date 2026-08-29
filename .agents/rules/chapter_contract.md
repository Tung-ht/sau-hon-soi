# 📜 Chapter Contract & Plan Guide
*(Quy chuẩn lập kế hoạch & Ký kết hợp đồng chương)*

Trước khi viết bất kỳ chương nào, `Writer Subagent` bắt buộc phải tạo một bản kế hoạch hợp đồng (`plan_chapter`) để đảm bảo không bị trượt khỏi mục tiêu tổng thể của tác phẩm.

---

## 1. Các Thành Phần Của Hợp Đồng Chương (Chapter Contract Structure)

Bản hợp đồng chương bao gồm 6 thành phần bắt buộc:

1. **`goal` (Mục tiêu cốt lõi của chương):** Một câu ngắn gọn mô tả sự kiện then chốt phải xảy ra.
2. **`scenes` (Phân cảnh chi tiết):** Danh sách 3-5 cảnh nối tiếp nhau (Địa điểm, nhân vật có mặt, xung đột/hành động chính).
3. **`required_beats` (Các nhịp cảm xúc/tình tiết bắt buộc):** Những chi tiết không thể bỏ qua (ví dụ: *"Nam phát hiện thư tống tiền dưới gối"*, *"Lão Tứ lộ vết sẹo sau lưng"*).
4. **`forbidden_moves` (Những điều cấm kỵ trong chương):** Những hành vi không được phép xuất hiện (ví dụ: *"Không được cho Nam tha thứ cho Hoàng quá dễ dàng"*, *"Không tiết lộ kẻ chủ mưu trước cảnh 3"*).
5. **`payoff_points` (Điểm thu hồi / Gặt hái):** Thu hồi phần thưởng cảm xúc hoặc giải tỏa một nghi vấn đã gieo từ các chương trước.
6. **`hook_goal` (Mục tiêu móc câu cuối chương):** Xác định loại hook sẽ dùng (`crisis` - khủng hoảng, `mystery` - bí ẩn, `desire` - khao khát, `emotion` - cảm xúc, `choice` - lựa chọn khó khăn).

---

## 2. Mẫu JSON Hợp Đồng Chương (`Plan JSON Schema`)

```json
{
  "chapter": 5,
  "title": "Bóng Đen Sau Cánh Cửa",
  "goal": "Nam đối chất với Hoàng về số tiền bị mất và phát hiện manh mối về lão Tứ",
  "scenes": [
    "Cảnh 1: Phòng khách nhà Nam - Không khí căng thẳng khi Hoàng bước vào.",
    "Cảnh 2: Đối thoại gắt gao - Hoàng chối bỏ nhưng để lộ chi tiết chiếc nhẫn bạc.",
    "Cảnh 3: Tiếng súng nổ ngoài hiên nhà - Hoàng tháo chạy, Nam nhìn thấy bóng lưng lão Tứ."
  ],
  "contract": {
    "required_beats": [
      "Nam chỉ ra vết bầm trên cổ tay Hoàng",
      "Hoàng buột miệng nhắc đến tên lão Tứ",
      "Tiếng súng nổ cắt ngang cuộc đối chất"
    ],
    "forbidden_moves": [
      "Không để Hoàng nhận tội ngay lập tức",
      "Không để Nam nổ súng trước"
    ],
    "continuity_checks": [
      "Vết thương ở bả vai Nam từ chương 4 vẫn còn đau khi cử động mạnh"
    ],
    "emotion_target": "Bức bối -> Căng thẳng tột độ -> Bàng hoàng",
    "payoff_points": [
      "Giải thích lý do Hoàng vắng mặt trong đêm xảy ra án mạng ở chương 3"
    ],
    "hook_goal": "Tiếng súng bất ngờ và phát hiện lão Tứ đang theo dõi ngoài cửa"
  }
}
```
