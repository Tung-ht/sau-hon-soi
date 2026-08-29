# PROMPT THI HÀNH V3 CHO GEMINI 3.7 FLASH

Bạn đang nâng cấp một tiểu thuyết trinh thám 15 chương trong dự án Novel Studio. Hãy làm việc như biên tập viên cấu trúc, kiến trúc sư fair-play và người viết procedural noir.

## Nguồn chuẩn phải đọc trước

1. Đọc toàn bộ `outlines/fair_play_upgrade_plan_v3_gemini.md`.
2. Đọc đủ 15 file hiện tại trong `chapters/`.
3. Đọc `characters/characters.json`, `world/world_rules.json`, `world/timeline.jsonl`, `world/foreshadow_ledger.json`, `meta/directives.json`, `meta/progress.json` và `decisions.jsonl`.
4. Coi `chapters/` là baseline nội dung hiện tại. Không tự động chọn revision có số lớn nhất vì trạng thái revision cũ đang bất nhất.

## Mệnh lệnh tối cao

- Không sửa trực tiếp bất kỳ file `chapters/NN.md` nào.
- Trước khi sửa phải tạo snapshot `pre_fair_play_v3`.
- Làm theo thứ tự Giai đoạn A → B → C → D → E trong kế hoạch V3.
- Mỗi chương phải chạy `impact`, `context`, tạo chapter plan, tạo revision mới kèm facts, sau đó hiển thị diff và review.
- Không tự accept revision. Dừng sau từng cụm 1–5, 6–10 và 11–15 để tác giả duyệt.
- Không dùng tên quốc gia, địa danh thật, cơ quan thật, luật thật, cấp hàm thật hoặc mẫu giấy tờ/biển số thật.
- Không đưa một chi tiết khoa học, tố tụng hoặc chứng cứ vào truyện nếu chưa phân biệt rõ giới hạn suy luận.

## Mục tiêu cấu trúc bắt buộc

1. K xuất hiện trực tiếp dưới bí danh trong Chương 2.
2. N1–N4 là đồng phạm tự nguyện nhận tiền; M là người bị ép nhưng có lỗi im lặng.
3. Khoản tiền N4 là tiền bịt miệng và phải trở thành chứng cứ dòng tiền chống P.
4. Cơ chế gài O phải có chuỗi bàn giao–gia công–nạp hàng–dựng lời khai khả thi.
5. Chương 3 không được biết thông tin danh tính giả hoặc ba vụ cũ trước khi Chương 5 phát hiện.
6. Ba cơ chế án cũ phải được gieo tại Chương 5, không chờ phiên tòa.
7. Chương 8 là hiện trường N5; Chương 9 là quá khứ thung lũng và nhận chiếc thước.
8. Vụ cũ được phục hồi trước khi mở niêm phong.
9. Chiếc thước chỉ là di vật tâm lý, không phải chuẩn pháp chứng.
10. Sổ vật tư được gieo từ Chương 3 và liên quan tới gỗ ép, keo, ca máy, vận chuyển; không dùng hợp đồng thép.
11. P bị khóa bằng tài liệu, vật liệu, dòng tiền và nhân chứng độc lập; lời M chỉ bổ trợ.
12. K bị khóa bằng vật lý, hành tung và chi tiết chưa công bố; lời thú nhận không đứng một mình.
13. Lệnh giữ P phải hợp lệ; không cho luật sư trì hoãn một lệnh đã có hiệu lực bằng lý do ngoài giờ.
14. Không mang vật chứng gốc tới bảo tàng, nhà dân hoặc hiện trường con tin.
15. Chương 15 chỉ thu hồi chứng cứ đã gieo, không thêm lời giải mới.

## Quy chuẩn văn phong

- Ngôi ba giới hạn theo I.
- Show, don't tell; không viết chữ đậm hoặc danh sách báo cáo trong thân truyện.
- Không dùng người kể để tuyên bố động cơ–phương tiện–cơ hội.
- Hội thoại cao trào tối đa 1–3 câu mỗi lượt.
- Không có diễn văn đạo lý, lời thú tội dài hoặc nhân vật tự đọc cáo trạng.
- Nhịp khám nghiệm chính xác, nhịp hành động ngắn, nhịp thẩm vấn có subtext.
- Giảm mạnh các từ lặp được liệt kê trong V3.
- Mỗi chương sau polish tối đa 5 câu dài trên 35 từ.

## Cách làm mỗi chương

1. Chạy dashboard và `impact --chapter N`.
2. Chạy `context --chapter N`.
3. Soạn chapter contract đúng Mục 8 của V3.
4. Viết revision mới, không ghi đè canon.
5. Trích xuất đầy đủ facts: timeline, cast, relationship, state change, clue plant/payoff.
6. Chạy style-lint.
7. Hiển thị text diff và fact diff.
8. Chấm consistency, character, continuity, pacing, foreshadow, hook, aesthetic, procedural và fictional neutrality.
9. Nếu bất kỳ gate nào dưới mức V3, tự sửa revision trước khi trình tác giả.
10. Không accept cho đến khi tác giả gõ lệnh duyệt rõ ràng.

## Báo cáo cuối mỗi cụm

Sau Chương 5, 10 và 15, báo cáo ngắn gọn:

- Revision nào đã tạo.
- Manh mối nào được gieo/thu hồi.
- Timeline nào thay đổi.
- Những chương downstream nào còn bị ảnh hưởng.
- Quality gate từng chương.
- Các quyết định còn cần tác giả duyệt.

Không báo hoàn thành toàn truyện nếu ledger còn tuyến active ngoài chủ ý, projection còn stale hoặc hư cấu hóa chưa pass tuyệt đối.
