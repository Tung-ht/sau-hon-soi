# KẾ HOẠCH NÂNG CẤP FAIR-PLAY V3 — BẢN THI HÀNH CHO GEMINI 3.7 FLASH

## 0. Mục đích, phạm vi và quy ước

- Đây là kế hoạch sửa **bản canon 15 chương hiện đang nằm trong `chapters/`**, không phải kế hoạch chuyển từ bản 12 chương cũ.
- Bản canon hiện tại dài khoảng 21.000 từ; đích nâng cấp là **40.000–46.000 từ**, vẫn giữ 15 chương.
- Mục tiêu thể loại: procedural revenge noir có cấu trúc fair-play; độc giả được quyền suy luận cả K lẫn P trước lời giải.
- Mọi nhân vật, địa danh, cơ quan, luật lệ và vụ án thuộc một thế giới hư cấu hoàn toàn.
- Trong tài liệu này không ghi tên riêng. Gemini phải tự tra tên hiện có trong `characters/characters.json` và giữ nhất quán khi viết revision.
- Ký hiệu:
  - **I**: điều tra viên chính.
  - **H**: cộng sự trực tiếp của I.
  - **M**: người thầy/chỉ huy nội bộ.
  - **P**: cựu chỉ huy, chủ mưu vụ cũ.
  - **K**: người báo thù, thủ phạm năm vụ giết người.
  - **L**: chủ xưởng cứu hộ, red herring vật chứng.
  - **O**: người thợ bị kết án oan trong vụ cũ.
  - **N1–N5**: năm đồng phạm vụ cũ đã bị K giết.
- Hard guard: **không sửa trực tiếp `chapters/NN.md`**. Mọi thay đổi phải đi qua revision mới, facts, diff và review; chỉ accept khi tác giả yêu cầu.
- Do trạng thái revision hiện tại không đồng nhất với `decisions.jsonl`, Gemini phải coi `chapters/` là baseline nội dung duy nhất, không tự chọn revision có số lớn nhất.

---

## 1. Mười lăm quyết định khóa của V3

1. Giữ cấu trúc 15 chương và motif sáu hòn sỏi.
2. K phải xuất hiện trực tiếp dưới bí danh trong **Chương 2**, không chỉ tồn tại qua lời kể.
3. N1–N4 là đồng phạm **tự nguyện nhận tiền**, trực tiếp giúp đánh tráo và dựng lời khai; bỏ hoàn toàn chi tiết họ bị ép nhận tội.
4. N5 biết rõ O vô tội nhưng nhận tiền ký lời chứng gian.
5. M không nằm trong sáu mục tiêu vì M bị đe dọa, từng phản đối, giữ chứng cứ và về sau cố gửi cảnh báo; M vẫn chịu trách nhiệm vì im lặng lâu năm.
6. Khoản tiền lớn N4 nhận sáu tháng trước khi chết là **tiền bịt miệng từ pháp nhân trung gian của P**, phải được thu hồi thành chứng cứ dòng tiền.
7. Bốn danh tính giả cũng do cùng mạng lưới tài chính–vận tải trung gian của P cung cấp; không để chi tiết này chỉ nằm trong world rules.
8. K lần ra N1–N4 nhờ bám chuỗi tiền bịt miệng và danh sách liên lạc cũ của N5; quá trình truy tìm kéo dài tám năm phải được kể bằng dấu vết cụ thể.
9. Cơ chế gài O được đổi thành: O hoàn tất và bàn giao sáu thân rương; nhóm N1–N4 chuyển rương sang xưởng công nghiệp lắp đáy giả, nạp hàng cấm, rồi dựng lời khai rằng O trực tiếp giao rương đã có khoang bí mật.
10. Chiếc thước chỉ là di vật tâm lý, tuyệt đối không dùng làm mẫu định danh tay nghề hay chứng cứ khoa học.
11. Chương 8 và Chương 9 đổi chức năng: tổ án đến thẳng hiện trường N5 trước; chỉ sau khi N5 đã chết và hiện trường được bảo vệ, I mới vào bản tìm quá khứ và nhận chiếc thước.
12. Vụ cũ phải được phục hồi hợp lệ trước khi mở niêm phong; giám định rương chia thành nhận định sơ bộ và kết luận phòng thí nghiệm vào ngày hôm sau.
13. Phiếu vật tư của L phải liên quan trực tiếp đến **tấm đáy gỗ công nghiệp, keo nhiệt, ca máy và vận chuyển**, không dùng hợp đồng thép không liên quan.
14. P bị khóa bằng bó chứng cứ tối thiểu bốn nguồn độc lập: tài liệu–bút tích, vật liệu–sản xuất, dòng tiền–pháp nhân, nhân chứng–nhật ký kho. Lời M chỉ củng cố.
15. K đầu hàng vì ba lực cùng lúc: quyết định phục hồi danh dự O đã có hiệu lực; P đã bị khóa đường thoát bằng lệnh hợp lệ; K tự chọn không tạo nạn nhân thứ sáu. Di vật của cha chỉ là lực kéo tâm lý cuối, không phải phép màu.

---

## 2. Sự thật tuyệt đối của vụ cũ

### 2.1. Động cơ của P

P đồng thời có hai động cơ:

1. Nhận lợi ích từ một đường dây hàng cấm để bảo vệ tuyến vận chuyển thật.
2. Cần một vụ án lớn để củng cố vị thế nghề nghiệp.

P chọn O vì O nghèo, ít quan hệ, có nghề đóng rương và vừa nhận đơn hàng từ một khách hàng do pháp nhân trung gian của P dựng lên.

### 2.2. Cơ chế gài tang vật từng bước

1. Pháp nhân trung gian đặt O đóng sáu thân rương theo thiết kế bình thường, không có đáy giả.
2. O hoàn tất, ký phiếu bàn giao và giao rương cho nhóm vận chuyển gồm N1–N4 lúc cuối buổi chiều.
3. N1–N4 đưa rương đến xưởng công nghiệp do người thân P quản lý, dùng máy cưa đa lưỡi tạo khoang đáy, lắp tấm gỗ ép đã đánh mã lô và dán keo nhiệt.
4. Hàng cấm được nạp vào khoang đáy tại xưởng công nghiệp; nhật ký ca máy bị rút khỏi hồ sơ nhưng bản lưu kế toán còn dấu thời gian.
5. Xe 1479 chở rương đến điểm kiểm soát do P sắp đặt. M nhận lệnh lái xe nhưng không tham gia gia công.
6. N1–N4 ký lời khai rằng O tự tay giám sát việc đóng kín đáy; N5 ký lời khai rằng đã thấy O nhận và giao hàng cấm.
7. Một biên bản kiểm tra phụ ghi mùi keo mới và vết máy bị P loại khỏi hồ sơ chính.
8. O bị kết án dựa trên tang vật và năm lời khai gian. O chết trước khi thủ tục kháng nghị hoàn tất.

### 2.3. Vì sao O được giải oan

Không dùng một chứng cứ đơn lẻ. Việc giải oan phải dựa trên tổ hợp:

- Phiếu bàn giao ghi O đã giao thân rương trước thời điểm ca máy công nghiệp bắt đầu.
- Dấu cưa và keo thuộc dây chuyền công nghiệp không có tại xưởng O.
- Mã lô tấm đáy dẫn tới kho vật tư của xưởng công nghiệp.
- Nhật ký ca máy và phiếu cấp keo ghi đúng sáu bộ vật tư.
- Dòng tiền pháp nhân trung gian chi cho xưởng và N1–N5.
- Biên bản phụ bị loại khỏi hồ sơ.
- Lời M và một nhân chứng kho xác nhận chuỗi vận chuyển.

### 2.4. Mức độ tội lỗi của sáu mục tiêu

| Mục tiêu | Hành vi trong vụ cũ | Mức độ chủ động | Vì sao K chọn |
|---|---|---|---|
| N1 | Điều phối lấy sáu rương từ O | Tự nguyện, nhận tiền | Trực tiếp mở chuỗi đánh tráo |
| N2 | Vận hành ca máy tạo khoang đáy | Tự nguyện, nhận tiền | Trực tiếp gia công tang vật giả |
| N3 | Nạp và hàn/khóa khoang chứa | Tự nguyện, nhận tiền | Trực tiếp đặt hàng cấm |
| N4 | Làm đầu mối vận chuyển, ký lời khai | Tự nguyện, tiếp tục nhận tiền bịt miệng | Giữ liên hệ hiện tại với mạng lưới P |
| N5 | Ký lời chứng gian về O | Tự nguyện vì tiền | Lời khai quyết định việc kết án |
| P | Thiết kế, trả tiền, loại biên bản, chỉ đạo bắt | Chủ mưu | Mục tiêu cuối |

M không thuộc sáu mục tiêu vì có bằng chứng ông từng ghi nhận sai lệch, bị đe dọa và không nhận tiền. Tuy vậy, M đã che giấu chứng cứ gần hai thập kỷ nên vẫn phải chịu trách nhiệm pháp lý và đạo đức.

### 2.5. Hành trình K tìm sáu người

1. Sau khi rời lực lượng cũ, K tìm được bản sao phiếu bàn giao trong đồ của một cựu thư ký kho.
2. K lần tới N5, bí mật sao chụp một sổ địa chỉ cũ ghi tên bốn người vận chuyển.
3. Bốn người đã đổi danh tính qua cùng một đường dây; K mất nhiều năm lần từng pháp nhân thuê lao động và các khoản trợ cấp bất thường.
4. Khoản tiền định kỳ từ công ty vận tải trung gian giúp K xác định N1 đầu tiên. Từ N1, K lần ra ba người còn lại.
5. K chỉ bắt đầu giết khi đã xác định đủ sáu người, dựng kho thực nghiệm và chuẩn bị cách buộc vụ cũ được mở lại.
6. Trước mỗi vụ, K gửi M một cảnh báo vì biết M giữ bản nháp lệnh xe. Đây vừa là cơ hội để M cứu người, vừa là cách ép M chấm dứt im lặng.

---

## 3. Kiến trúc ba tầng điều tra

| Tầng | Câu hỏi | Các phương án độc giả có thể tin | Câu trả lời |
|---|---|---|---|
| 1 | Ai giết N4 và gây ba tai nạn cũ? | L, M, K dưới bí danh | K |
| 2 | Ai biết trước danh sách và đang rò rỉ dữ liệu? | M, P, tài khoản bị xâm nhập | M nhận cảnh báo nhưng che giấu; P theo dõi qua mạng lưới xã hội |
| 3 | Ai dựng vụ oan và vì sao có sáu mục tiêu? | P, M, nhóm vận chuyển | P chủ mưu; N1–N5 tự nguyện đồng lõa; M bị ép nhưng có lỗi im lặng |

### Điều kiện fair-play bắt buộc

1. K xuất hiện trực tiếp trước hết 15% dung lượng.
2. Các dấu cơ học của ba vụ đầu phải xuất hiện trước Chương 7, không chờ phiên tòa.
3. Khoản tiền N4 phải có payoff trước Chương 13.
4. Độc giả được thấy phiếu vật tư của L từ Hồi I, dù chưa hiểu ý nghĩa.
5. Mọi manh mối pháp chứng đều có giới hạn được nêu trên trang.
6. P không bị kết tội bằng lời thú nhận của M.
7. L và M đều được loại khỏi vai trò hung thủ bằng chứng khách quan, nhưng không được tẩy trắng các sai phạm khác.
8. Chương 15 không được đưa ra một cơ chế giết người hoặc tài liệu kết tội hoàn toàn mới.

---

## 4. Master timeline V3

| Mốc | Sự kiện khóa |
|---|---|
| Tối thứ Hai 18:30–20:00 | I gặp mẹ; P gặp M và I trong hoạt động xã hội; P không biết vụ án chưa xảy ra. |
| Tối thứ Hai 21:00–23:00 | K giết N4, dàn túi vật thứ tư; K không lấy tiền. |
| Sáng thứ Ba 05:30–08:00 | Phát hiện N4; khám nghiệm và niêm phong. |
| Thứ Ba 08:30–17:30 | Xác minh danh tính giả, khoản tiền và nghi phạm nợ. I gặp K dưới bí danh tại bãi phế liệu. |
| Tối thứ Ba–trưa thứ Tư | Xác minh L, lấy mẫu theo lệnh hợp lệ, thu dữ liệu tàu và lập danh mục sổ cũ. |
| Chiều–tối thứ Tư | Thẩm vấn L; xác nhận ngoại phạm N4; K biến mất; P hỏi tiến độ qua kênh xã hội. |
| Sáng thứ Năm | Có kết quả độc chất thận trọng; xác minh chòi; nối bốn danh tính; mở lại hồ sơ ba tai nạn để đọc dấu cơ học. |
| Chiều thứ Năm | Chuyên gia văn hóa chỉ thu hẹp nguồn túi tới vùng thượng lưu, không chỉ đúng một người. |
| 18:00–20:00 thứ Năm | Audit cho thấy M đã tra N1–N5; một phong bì mới ghi tên N5 được tìm thấy; M rời trụ sở lúc 18:45. |
| 21:00 thứ Năm | I và H xuất phát; đơn vị độc lập được báo về nghi vấn M. |
| 22:00–22:45 thứ Năm | K giết N5 trước khi M đến. |
| 23:15 thứ Năm | M đến bến, phát hiện N5 đã chết, gọi báo ẩn danh rồi rời đi vì hoảng loạn; camera cầu và trạm nhiên liệu khóa lịch trình. |
| 03:00 thứ Sáu | I đến địa bàn sau một đoạn đường tắc vì sạt lở nhỏ; đi thẳng tới hiện trường đã được lực lượng địa phương bảo vệ. |
| 03:15–06:30 thứ Sáu | Khám N5, phát hiện dấu M nhưng không định danh tuyệt đối; M bị đơn vị độc lập giữ lại để làm việc. |
| 07:00–10:00 thứ Sáu | I vào bản tìm gốc túi, xác định K bằng ba nguồn và nhận chiếc thước như di vật ngoài chuỗi pháp chứng. |
| 10:00–13:00 thứ Sáu | Cơ quan cấp cao ra quyết định phục hồi vụ cũ và lệnh mở niêm phong. |
| 13:00–17:00 thứ Sáu | Đọc hồ sơ, mở đủ sáu rương, ghi nhận sơ bộ, lấy mẫu và gửi phòng lab. |
| 20:30–23:45 thứ Sáu | M được hỏi cung có ghi âm và luật sư/người giám sát độc lập; giao bản nháp, nhật ký, phong bì cảnh báo. |
| Sáng thứ Bảy | Kết luận lab, giám định bút tích và dòng tiền hoàn tất đủ mức xin lệnh; K gọi I. |
| Chiều thứ Bảy | P bị giám sát, cấm xuất cảnh và triệu tập; chứng cứ khẩn tiếp tục được củng cố. |
| 02:00–04:40 Chủ nhật | Có dữ liệu P chuẩn bị hủy/chuyển chứng cứ và K đã tiếp cận; lệnh giữ khẩn cấp được ký lúc 04:40. |
| 04:45–05:30 Chủ nhật | Tổ chiến thuật thi hành lệnh; K đồng thời xâm nhập đường kỹ thuật. |
| 05:30–06:15 Chủ nhật | Đối đầu I–K–P; K đầu hàng; P bị giữ theo lệnh riêng. |
| Mười tám tháng sau | Phiên tòa chỉ thu hồi chứng cứ đã gieo; O được phục hồi danh dự. |
| Một tuần sau | Vĩ thanh đời thường của I. |

### Quy tắc thời gian

- Không dùng quãng đường 130 km mất 7,5 giờ nếu không có tắc đường cụ thể.
- Hành trình đêm của I dài hơn M vì xuất phát muộn và bị giữ tại điểm sạt lở; phải ghi rõ trên trang.
- M đến sau án N5 khoảng 30 phút; camera cầu, hóa đơn nhiên liệu và log cuộc gọi phải chứng minh.
- Kết luận lab không xuất hiện trong cùng buổi lấy mẫu.
- Lệnh giữ P chỉ có sau khi bó chứng cứ đủ và/hoặc có nguy cơ tiêu hủy chứng cứ cụ thể.

---

## 5. Ma trận manh mối hai mặt V3

| Mã | Gieo | Manh mối bề mặt | Hiểu sai hợp lý | Sự thật | Payoff |
|---|---:|---|---|---|---:|
| C01 | 1 | P là tiền bối tử tế, nhớ tuyến vận tải | Kinh nghiệm nghề nghiệp | P theo dõi xem vụ mới có chạm mạng lưới cũ | 10–13 |
| C02 | 1 | M phản ứng với câu nói về hồ sơ cũ | M quá nhạy cảm vì nghề | M nhận ra P đang thử phản ứng mình | 7, 11 |
| C03 | 2 | N4 nhận khoản tiền lớn từ công ty vận tải | Nợ nần hoặc giao dịch hàng lậu | Tiền bịt miệng từ pháp nhân P | 5, 12 |
| C04 | 2 | K dưới bí danh giúp xử lý một chi tiết kim loại | Thợ lưu động vô danh | K đang quan sát cách tổ án phản ứng | 4, 8–9 |
| C05 | 3 | Xỉ và vật tư cùng nhóm với xưởng L | L giết N4 | K từng làm ở xưởng, dấu chỉ phân nhóm | 4–5 |
| C06 | 3 | Tàu L từng qua ba địa bàn | L gây ba tai nạn | Tuyến việc làm giúp K tiếp cận các địa bàn | 4–5 |
| C07 | 3 | Sổ vật tư cũ có sáu tấm gỗ ép và keo | Hợp đồng thông thường | Vật liệu đáy giả của vụ cũ | 10, 12 |
| C08 | 4 | L xóa dữ liệu và giấu dụng cụ | L che án mạng | L che chuyến ngoài sổ và việc K lấy dụng cụ thải loại | 4 |
| C09 | 5 | Ba tai nạn có lỗi cơ khí nhỏ | Sơ suất lao động độc lập | Cùng một người can thiệp có phương pháp | 12, 15 |
| C10 | 5 | Bốn danh tính giả cùng batch | Nhóm tội phạm tự bảo vệ nhau | Mạng lưới P phân tán người cũ | 10–12 |
| C11 | 6 | Túi dệt chỉ về vùng thượng lưu | Chỉ là bùa quê | K dùng motif để buộc nối vụ án | 8–9, 15 |
| C12 | 6 | M tra dữ liệu trước các cái chết | M là kẻ rò rỉ hoặc đồng phạm giết người | M nhận cảnh báo, cố cứu nhưng che vụ cũ | 7–11 |
| C13 | 7 | Tài khoản M hoạt động từ IP công vụ | M tự tra cứu | Đúng là M, loại giả thuyết bị hack | 11 |
| C14 | 8 | Dấu bùn và loại lốp của M gần N5 | M giết N5 | M đến sau án; vết mòn, camera và log gọi xác nhận lịch trình | 11 |
| C15 | 9 | Chiếc thước của O | Có thể là chuẩn tay nghề | Chỉ là di vật đạo đức; không dùng pháp chứng | 14–15 |
| C16 | 10 | Bút tích P về phương án B | Chỉ dẫn vận chuyển thông thường | Ghép với ca máy, biên bản phụ và tiền mới có nghĩa phạm tội | 11–15 |
| C17 | 10 | Mã lô đáy dẫn tới xưởng người thân P | Trùng nguồn vật liệu | Nhật ký kho và dòng tiền chứng minh sáu bộ cụ thể | 12 |
| C18 | 11 | M giữ tài liệu trái quy trình | M đồng lõa muốn khống chế chứng cứ | M vừa hèn nhát vừa giữ đường phục hồi | 11, 15 |
| C19 | 12 | K gọi đặt hạn | Khiêu khích hệ thống | Một phần K muốn được ngăn trước mục tiêu sáu | 14 |
| C20 | 13 | P trì hoãn, chuyển tài liệu | Quyền tự bảo vệ | Hành vi cản trở hiện tại, chỉ là chứng cứ bổ trợ | 14–15 |
| C21 | 14 | Kho thực nghiệm của K | Bộ sưu tập chiến tích | Hồ sơ nhận tội; phải kiểm chứng độc lập | 15 |

### Quy tắc payoff

- Không còn manh mối tiền bạc nào bị bỏ quên.
- C07 phải nhìn thấy từ Chương 3; Chương 12 chỉ tái diễn giải, không được tạo cuốn sổ từ hư không.
- C09 phải cho độc giả biết cơ chế cơ bản của ba vụ cũ trước khi xác nhận K.
- C14 chỉ định vị M ở khu vực; việc loại M cần camera, thời gian, log gọi và tình trạng thi thể.
- C16–C17 không được viết là tự thân đủ kết tội P.

---

## 6. Bó chứng cứ cuối cùng

### 6.1. Đối với K

| Vụ | Vật lý | Hành tung/dữ liệu | Lời khai/tài liệu | Chi tiết chỉ hung thủ biết |
|---|---|---|---|---|
| N1 | Chốt chịu lực bị thay bằng chốt gia công cùng chuẩn ren | K làm thời vụ gần xưởng trong tuần xảy ra án | Sổ chấm công bí danh và lời quản đốc | Vị trí chốt phụ bị che dưới lớp dầu |
| N2 | Nêm phụ và kíp thứ cấp có kiểu đấu nối riêng | Vé xe/nhà trọ và mua vật tư gần mỏ | Người bán vật tư nhớ vết sẹo tay, không định danh một mình | Thứ tự hai lần kích hoạt |
| N3 | Khóa thông gió bị chèn, adapter cấp khí trơ tự chế | K có thẻ ra vào nhà thầu trong ngày bảo dưỡng | Danh sách nhân công và vật tư adapter | Vị trí van bypass không công bố |
| N4 | Vi sợi áo sửa tay, xỉ nghề nghiệp, dấu giằng co | K ở bãi phế liệu và chòi gần hiện trường | L cùng chủ bãi xác nhận bí danh | Vật bị di chuyển trong hộp đồ nghề |
| N5 | Dấu tiếp cận, vết giày nhóm, dao thu sau này có đặc điểm phù hợp | Camera cầu, khoảng thời gian K rời bản | M nghe tiếng xe máy rời bến; nhân chứng chỉ mô tả nhóm | Vị trí túi được dàn dưới sạp, không phải trong tay tử thi |

Lời thú nhận, kho thực nghiệm và sổ K chỉ có giá trị khi đối chiếu được với các dấu chưa công bố. Không dùng cụm “trùng khớp hoàn toàn” nếu kỹ thuật chỉ cho phép kết luận tương thích.

### 6.2. Đối với P

1. **Tài liệu:** bút tích phương án B, biên bản phụ bị loại, lịch xe và phiếu bàn giao rương.
2. **Vật liệu–sản xuất:** sáu tấm đáy cùng mã lô, keo cùng batch, nhật ký ca máy và phiếu lĩnh vật tư.
3. **Tài chính:** pháp nhân trung gian trả tiền xưởng, N1–N5 và khoản bịt miệng gần thời điểm N4 chết.
4. **Nhân chứng:** nhân viên kho hoặc kế toán cũ xác nhận ca máy đặc biệt; M xác nhận bị đe dọa nhưng không phải nhân chứng duy nhất.
5. **Dấu vết số hiện tại:** P truy cập tài khoản pháp nhân, chuyển tài liệu và chuẩn bị rời địa bàn sau khi vụ cũ được mở.
6. **Giám định tài liệu:** chữ viết có cùng đặc điểm với mẫu chuẩn; giám định viên không kết luận tội danh.

Muốn kết tội nhận hối lộ phải có dòng tiền hoặc lợi ích cụ thể. Nếu không xây được nhánh này, bỏ tội danh đó khỏi phiên tòa thay vì để lời M gánh toàn bộ.

### 6.3. Đối với M

- Chữ ký nhận xe.
- Bút ghi chú phản đối bị gạch khỏi biên bản.
- Audit N1–N5.
- Năm phong bì cảnh báo và bản sao các cuộc gọi ẩn danh M từng gửi.
- Camera và log cuộc gọi tại N5.
- Việc giữ tài liệu trái quy trình gần hai thập kỷ.
- Lời thú nhận có ghi âm, được luật sư/người giám sát độc lập chứng kiến.

M được loại khỏi năm vụ giết người, không được miễn trách nhiệm che giấu.

---

## 7. Thiết kế lại nhân vật

### 7.1. I

- Hồi I: tin P, kính M, đôi lúc quá phụ thuộc vào uy tín người đi trước.
- Hồi II: học cách tách con người khỏi chức danh; chủ động báo đơn vị độc lập khi M thành nghi phạm.
- Hồi III: chiến thắng bằng cách dựng lựa chọn có căn cứ, không bằng bài giảng đạo đức.
- Neo đời thường: mẹ và món ăn quen chỉ xuất hiện đầu–cuối; tránh dùng như nút bấm cảm xúc lặp lại.

### 7.2. H

- Có nhiệm vụ riêng: kiểm tra timeline và dữ liệu tuyến đường.
- Là người phát hiện mâu thuẫn tài khoản M có thể bị hack, buộc tổ án kiểm tra IP và thiết bị.
- Ở cao trào, H phụ trách an toàn con tin hoặc khóa lối thoát, không chỉ đứng nghe I nói.

### 7.3. K

- Xuất hiện trực tiếp ở Chương 2 dưới bí danh, có hành vi đời thường bình tĩnh.
- Kỹ năng cao nhưng không toàn năng: mỗi vụ có sai số, dấu vết và rủi ro.
- Không gọi các nạn nhân là quỷ dữ; K biết mình giết người và chuẩn bị chịu án.
- Việc muốn được ngăn lại phải biểu hiện qua hành động: gửi cảnh báo, để manh mối có kiểm soát và hỏi trạng thái phục hồi hồ sơ.

### 7.4. M

- Không độc thoại thú nhận quá hai đoạn liên tục.
- Từng nỗ lực cảnh báo phải có tài liệu kiểm chứng, không chỉ kể miệng.
- Sự hèn nhát gây hậu quả thật: mất chức, bị xét xử, gia đình chịu điều tiếng.

### 7.5. P

- Chương 1–6 không dùng ánh sáng, nụ cười hoặc câu chữ quá phản diện.
- Lời khuyên phải đúng một nửa và thật sự giúp tìm K.
- Khi thất thế, P vẫn chống đỡ bằng lập luận ngắn, không tự kể tội.
- P không có quyền vào họp án mật nếu không được mời xem bản tóm tắt đã lược thông tin.

### 7.6. L

- L nói dối vì công việc ngoài sổ và lao động không đăng ký.
- K tự lấy dụng cụ thải loại hoặc L cho mượn trước khi nghe câu báo thù; không để L biết nguy cơ rồi vẫn trao hung khí.
- Sổ vật tư được lập danh mục ngay ở Chương 3, không xuất hiện đột ngột ở Chương 12.

### 7.7. N1–N5

- Mỗi người cần một đoạn hồ sơ ngắn cho thấy mức độ tham gia, khoản tiền và đời sống hiện tại.
- Không biến họ thành những cái tên để K giết. Ít nhất một người đã muốn khai nhưng lại tiếp tục nhận tiền, tạo phức tạp đạo đức.
- Gia đình hoặc hậu quả sau cái chết của họ cần được nhắc tại phiên tòa để không lãng mạn hóa K.

---

## 8. Hợp đồng nâng cấp từng chương

### Chương 1 — Mở án

- **Giữ:** cảnh đời thường của I, không khí mưa, hiện trường N4, túi vật thứ tư.
- **Sửa:** P chỉ xuất hiện vì hoạt động xã hội; không biết dữ liệu án; bỏ mọi danh xưng ngoài hệ hư cấu.
- **Pháp y:** PMI là một khoảng rộng; test nhanh chỉ sơ bộ; không kết luận chất cụ thể tại hiện trường.
- **Gieo:** C01, C02; một chi tiết nhỏ cho thấy P nhớ quá rõ tên pháp nhân vận tải nhưng chưa đủ đáng ngờ.
- **Cấm:** kể lịch sử toàn vùng trong một đoạn dài; câu kết “mở đầu cuộc điều tra trắc trở”.
- **Dung lượng:** 2.600–3.000 từ.

### Chương 2 — Tiền và người thợ bí danh

- **Mục tiêu:** xác minh danh tính giả, khoản tiền, P đưa lời khuyên đúng một nửa và K xuất hiện trực tiếp.
- **K xuất hiện:** I gặp một thợ lưu động dưới bí danh tại bãi phế liệu; họ trao đổi ngắn về một thanh kim loại bị ăn mòn. K không hành xử khả nghi lộ liễu.
- **Khoản tiền:** xác định người chuyển là pháp nhân vận tải có liên hệ với cảng và quỹ của P, nhưng chưa chứng minh tiền bịt miệng.
- **Red herring nợ:** alibi không được xác minh hoàn toàn trong 15 phút; kết quả camera đến cuối chương.
- **Gieo:** C03, C04.
- **Cấm:** P ngồi tự do trong cuộc họp mật; gọi K là bậc thầy cơ khí siêu phàm.
- **Dung lượng:** 2.500–2.900 từ.

### Chương 3 — L và xưởng cứu hộ

- **Mục tiêu:** dựng L bằng động cơ–phương tiện–cơ hội mà chưa biết ba nạn nhân cũ dùng danh tính giả.
- **Bắt buộc sửa continuity:** H không được nói ba địa bàn trùng với ba người mang giấy tờ giả; lúc này chỉ biết lịch tàu bất thường và vụ N4.
- **Lệnh khám:** nêu căn cứ và thẩm quyền ngắn gọn; nếu khám đêm phải có tình huống khẩn cụ thể, nếu không chuyển sang sáng thứ Tư.
- **Sổ vật tư:** lập danh mục, chụp trang có sáu tấm gỗ ép/keo nhưng chưa hiểu liên quan.
- **XRF:** chỉ kết luận cùng nhóm vật liệu.
- **Gieo:** C05, C06, C07.
- **Cấm:** chữ đậm “động cơ–phương tiện–cơ hội” trong văn xuôi.
- **Dung lượng:** 2.700–3.100 từ.

### Chương 4 — Phá alibi L, mở đường tới K

- **Mục tiêu:** loại L khỏi N4 bằng bốn nguồn: camera bến, log cứu hộ, dữ liệu máy phụ và nhân chứng độc lập.
- **Giữ nghi vấn:** L vẫn có thể liên quan ba vụ cũ vì từng đi qua các địa bàn.
- **Dụng cụ:** K lấy dụng cụ thải loại trước khi L hiểu mục đích; bỏ câu K báo thù rõ rồi L vẫn trao đồ.
- **P:** chỉ gọi hỏi áp lực cộng đồng và đề nghị đừng bỏ sót người thợ khác; không biết chi tiết niêm phong.
- **H:** phát hiện bí danh ở xưởng trùng người đã gặp Chương 2.
- **Thu hồi:** C04–C06 một phần.
- **Dung lượng:** 2.500–2.900 từ.

### Chương 5 — Bốn cái chết và ba cơ chế

- **Mục tiêu:** nối N1–N4 bằng danh tính giả, dòng tiền và các dị vật; cho độc giả biết dấu cơ học cơ bản của ba vụ đầu.
- **Độc chất N4:** chỉ nói có sử dụng kéo dài trong một khoảng; lời người bán thuốc hỗ trợ khả năng N4 tự dùng, không khẳng định tuyệt đối.
- **Đối soát giấy tờ:** gồm mã batch, ảnh lưu, xác minh từng địa phương; không phải một cú bấm máy.
- **Ba hồ sơ tai nạn:** mỗi vụ có một ảnh/dấu kỹ thuật bất thường để I nghi can thiệp cơ học.
- **Khoản tiền:** pháp nhân đã trả khoản tương tự cho ít nhất một người cũ khác.
- **P:** xuất hiện trong ảnh vụ cũ nhưng I chưa kết luận.
- **Gieo:** C09, C10.
- **Cấm:** tóm tắt ba vụ bằng danh sách gạch đầu dòng.
- **Dung lượng:** 3.200–3.700 từ.

### Chương 6 — Nguồn gốc motif và audit M

- **Vật chứng:** chuyên gia chỉ xem ảnh, mẫu sợi tách hợp lệ hoặc swatch đối chứng; không mang bốn túi gốc đi khỏi kho.
- **Chuyên gia:** so sánh tối thiểu ba vùng dệt, nêu giới hạn và chỉ thu hẹp đến vùng thượng lưu.
- **Bài hát:** chỉ giải số đếm và hình ảnh bến nước, không chỉ thẳng N5.
- **Audit:** một phong bì cảnh báo mới trong két M chứa tên N5; log hệ thống cho thấy M tra cứu trước.
- **Đơn vị độc lập:** I báo bộ phận giám sát dữ liệu, không tự điều tra cấp trên hoàn toàn một mình.
- **Gieo:** C11–C13.
- **Dung lượng:** 2.500–2.900 từ.

### Chương 7 — Cuộc đua có căn cứ

- **Mục tiêu:** kiểm tra khả năng tài khoản M bị xâm nhập, xác nhận chính thiết bị M đã dùng và phát hiện M rời trụ sở.
- **Không dùng bullet:** chuyển audit thành cảnh đối chiếu màn hình, thời gian và lời thoại ngắn.
- **Timeline:** M rời 18:45; I rời 21:00; camera cầu và trạm nhiên liệu khóa tuyến M.
- **P:** gọi M không được, sau đó hỏi I một câu chung; P không biết I đang nghi M.
- **Hook:** đường đèo bị sạt nhỏ, liên lạc chập chờn; I nhận tin địa phương đã có báo án vô danh gần bến.
- **Dung lượng:** 2.400–2.800 từ.

### Chương 8 — Bến nước trong sương

- **Đảo với bản cũ:** tổ án đi thẳng tới N5, không vào bản nghe kể chuyện trước.
- **Hiện trường:** túi thứ năm được đặt dưới sạp hoặc trong hộp chè, không nằm trong bàn tay co quắp nếu không giải thích cadaveric spasm.
- **PMI:** dùng nhiệt độ, hoen, co cứng và môi trường để cho khoảng; không chốt chính xác đến một giờ.
- **Dấu M:** lốp chỉ là cùng nhóm; camera cầu, log cuộc gọi và bùn xe mới đặt M tại khu vực.
- **M:** bị đơn vị độc lập yêu cầu ở lại; không thể tự dập máy rồi đi tiếp.
- **Loại M sơ bộ:** dữ liệu chứng minh M đến sau K khoảng 30 phút và chính M gọi báo ẩn danh.
- **Hook:** M nói vụ cũ có một biên bản phụ bị loại và chiếc rương phải được bảo toàn.
- **Dung lượng:** 2.700–3.100 từ.

### Chương 9 — Thung lũng oan khuất

- **Mục tiêu:** sau khi hiện trường N5 đã ổn định, I mới vào bản xác định K và nhận di vật.
- **Thông tin quá khứ:** chia cho ba nguồn; không để một cụ già kể toàn bộ vụ án trong một độc thoại.
- **Xác định K:** ảnh cũ, sổ cư trú/nghề và lời L; hồ sơ huấn luyện không được truy xuất thần kỳ.
- **Chiếc thước:** lập biên nhận di vật gửi K, ghi rõ không phải vật chứng vụ án.
- **Cơ chế gài:** chỉ hé việc sáu rương từng rời xưởng O trước khi bị bắt, chuẩn bị cho Chương 10.
- **Hook:** quyết định phục hồi vụ cũ được đề xuất; I nhận bản scan phiếu bàn giao.
- **Dung lượng:** 2.800–3.200 từ.

### Chương 10 — Mở lại vụ cũ đúng trình tự

- **Trình tự:** quyết định phục hồi → lệnh mở niêm phong → kiểm kê sáu rương → ghi hình → lấy mẫu.
- **Giám định:** trong ngày chỉ có nhận định sơ bộ; kết luận vật liệu đến sáng thứ Bảy.
- **Không dùng thước:** tuyệt đối không đặt chiếc thước cạnh mộng rương.
- **Sáu rương:** kiểm tra cả sáu hoặc nêu phương pháp lấy mẫu đại diện hợp lệ; tốt nhất kiểm tra đủ vì số lượng nhỏ.
- **Tài liệu:** phiếu bàn giao của O, ca máy xưởng, biên bản phụ, lệnh xe M, chỉ dẫn phương án B của P.
- **P:** từ tiền bối chuyển thành người cần điều tra, chưa gọi là tội phạm đã chứng minh.
- **Gieo/thu hồi:** C07, C10, C16, C17.
- **Dung lượng:** 3.300–3.800 từ.

### Chương 11 — M chịu trách nhiệm

- **Hỏi cung:** do đơn vị độc lập chủ trì, có ghi âm; I tham gia với tư cách người phát hiện chứng cứ.
- **Cấu trúc:** từng câu hỏi gắn với một vật chứng; không có bài độc thoại năm trang.
- **M giao:** bản nháp lệnh xe, nhật ký, năm phong bì, bản sao cảnh báo và bằng chứng không nhận tiền.
- **Giải thích chuyến N5:** camera và log cuộc gọi khớp lời khai.
- **Không tẩy trắng:** M bị tạm đình chỉ/tạm giữ theo luật hư cấu; I không tha thứ tại chỗ.
- **Hook:** kết luận lab và dữ liệu dòng tiền sắp về; K gọi đường dây của I.
- **Dung lượng:** 3.000–3.500 từ.

### Chương 12 — Bó chứng cứ và hạn chót

- **K gọi:** ngắn, hỏi ba việc: O đã được phục hồi chưa, P đã bị giữ chưa, hồ sơ có công khai không.
- **I:** đưa một chi tiết từ phiếu bàn giao mà K chưa biết để chứng minh vụ án thực sự được mở.
- **L:** không tự nhiên mang sổ đến; tổ án quay lại trang sổ đã lập danh mục ở Chương 3 và xin giao nộp/khám xét bổ sung.
- **Vật tư:** sáu tấm gỗ ép, keo, ca máy, hóa đơn vận chuyển; không có sáu tấm thép vô nghĩa.
- **Dòng tiền:** khoản N4 nhận được nối với P qua hai lớp pháp nhân và đối chiếu khoản chi N1–N5.
- **Kết quả:** đủ căn cứ cấm xuất cảnh, giám sát và xin lệnh; chưa để P bị luật sư vô hiệu hóa bằng lý do ngoài giờ.
- **Hook:** P đến căn nhà vùng núi đã được gieo là tài sản nghỉ dưỡng/quỹ; camera ghi việc chuyển thùng hồ sơ.
- **Dung lượng:** 2.800–3.200 từ.

### Chương 13 — Hai vòng vây

- **Mục tiêu:** một vòng giám sát P, một vòng truy K; không dựng trở ngại pháp lý giả.
- **P:** chưa bị bắt đầu chương vì lệnh giữ đang chờ chứng cứ cuối, nhưng bị giám sát và cấm rời địa bàn.
- **Nguy cơ khẩn:** P cho chuyển/hủy tài liệu; K cắt vào đường kỹ thuật. Hai sự kiện tạo căn cứ lệnh giữ lúc 04:40.
- **An ninh:** rút còn bốn vệ sĩ, không dùng chó; hai ở cổng bị tổ chiến thuật khóa, hai trong tầng kỹ thuật bị K khống chế.
- **Điện:** nguồn chính bị cắt nhưng máy phát dự phòng bật ánh sáng khẩn; không để biệt thự tối hoàn toàn vô lý.
- **Dấu K:** không suy ra toàn bộ kế hoạch từ một đoạn cáp; phải ghép dấu giày, camera mất tín hiệu cục bộ và bản vẽ thoát nước.
- **Hook:** lệnh được ký, đội vào vị trí đúng lúc K đã lọt tầng hầm.
- **Dung lượng:** 2.600–3.000 từ.

### Chương 14 — Lựa chọn thứ sáu

- **Chiến thuật:** I giữ khoảng cách và vũ khí ở tư thế kiểm soát; H xử lý con tin/vệ sĩ; không ai bước vào cự ly dao vô lý.
- **Không mang bản gốc:** chỉ dùng bản sao quyết định phục hồi, ảnh chiếc thước và lời nhắn đã ghi của người giữ di vật.
- **P:** ba lượt thoại ngắn: đòi I bắn K, viện bản án cũ, phủ nhận chứng cứ.
- **I:** không đọc cáo trạng; chỉ xác nhận P đã bị giữ, hồ sơ O đã phục hồi và K còn quyền tự thú.
- **K:** không kể toàn bộ quá khứ; phản ứng bằng im lặng, cử chỉ và hai câu ngắn.
- **Ba lực dừng tay:** lệnh hợp lệ khóa P; hồ sơ phục hồi O có số quyết định; ảnh thước/lời cha gọi lại nhân tính.
- **K đầu hàng:** đặt dao xuống, nói vị trí kho thực nghiệm và yêu cầu khai trong phòng ghi âm.
- **Cấm:** bản gốc chiếc thước tại hiện trường; hạ súng hoàn toàn; diễn văn đạo lý; lời thú tội năm vụ ngay giữa phòng.
- **Dung lượng:** 3.200–3.700 từ.

### Chương 15 — Phiên tòa và dư âm

- **Phiên tòa:** trình bày theo bốn bó chứng cứ đã gieo; không thêm phương thức giết người mới.
- **K:** bị kết tội bằng chứng cứ độc lập cộng lời thú nhận; ghi rõ năm gia đình nạn nhân cũng chịu hậu quả, không lãng mạn hóa báo thù.
- **P:** chỉ nhận tội danh có đủ chứng cứ. Nếu nhánh tài chính chưa đủ, không tự ý thêm tội nhận hối lộ.
- **M:** bản án không được gọi là sự giải thoát trọn vẹn; giữ hậu quả nghề nghiệp và gia đình.
- **O:** phục hồi danh dự dựa trên tổ hợp chứng cứ, không chỉ vì đáy rương dùng máy.
- **Vĩ thanh:** rút còn hai nhịp: chiếc thước trở về nơi cũ trong một cảnh ngắn; I về với mẹ. Bài ca có thể xuất hiện tối đa sáu dòng, bỏ đoạn giải thích thông điệp.
- **Câu cuối:** một hình ảnh đời thường hoặc dòng nước; không tuyên bố “công lý đã trở về”.
- **Dung lượng:** 3.200–3.700 từ.

---

## 9. Quy chuẩn pháp chứng và tố tụng

1. XRF chỉ xác định thành phần nguyên tố và mức tương thích nhóm vật liệu.
2. FTIR chỉ xác định nhóm chất kết dính; muốn nối tới batch cần mẫu chuẩn và hồ sơ mua hàng.
3. Toolmark chỉ xác định nhóm hoặc đặc điểm cá thể khi chất lượng dấu đủ; không suy ra người cầm công cụ.
4. PMI luôn là khoảng có sai số và phụ thuộc nhiệt độ, môi trường, hoen, co cứng cùng dữ liệu bổ trợ.
5. Không suy luận quan hệ hung thủ–nạn nhân từ mắt mở, nét mặt hay tư thế chết.
6. Mọi vật chứng: chụp tại chỗ → mã hóa → đóng gói riêng → niêm phong → ghi người giao nhận.
7. Chuyên gia văn hóa chỉ nhận ảnh/mẫu tách có biên bản; không cầm toàn bộ vật chứng gốc tại văn phòng riêng.
8. Phục hồi vụ cũ phải có trước lệnh mở niêm phong.
9. I không một mình nhận lời thú nhận và vật chứng của M; cần đơn vị độc lập và ghi âm.
10. Lệnh giữ P không bị luật sư “hoãn đến giờ làm việc” nếu đã có hiệu lực. Trở ngại phải đến từ việc lệnh chưa được ký hoặc nguy cơ chiến thuật, không từ thủ tục bịa đặt.
11. Không mang vật chứng gốc đến hiện trường con tin.
12. Tại phiên tòa, tài liệu tự viết và lời thú nhận phải được kiểm chứng bằng nguồn độc lập.

---

## 10. Quy chuẩn văn phong cho Gemini 3.7 Flash

### 10.1. POV và show-don't-tell

- Ngôi ba giới hạn theo I; chỉ rời POV khi chapter contract cho phép rõ.
- Không tuyên bố “L có đủ động cơ–phương tiện–cơ hội”; để ảnh, dụng cụ, lịch tàu và lời nói dối tự tạo nghi ngờ.
- Không dùng người kể để xác nhận một nhân vật nói thật trước khi I kiểm chứng.
- Mỗi suy luận theo thứ tự: quan sát → giả thuyết → kiểm tra → kết luận tạm thời.

### 10.2. Hội thoại

- Mỗi lượt thoại cao trào tối đa 1–3 câu.
- Nhân vật nghiệp vụ dùng khẩu ngữ nghề, không đọc văn bản hành chính.
- Không để P hoặc K tự kể toàn bộ tội trạng.
- M phải bị ngắt bởi câu hỏi, im lặng và vật chứng trong cảnh thú nhận.

### 10.3. Nhịp câu

- Khám nghiệm: 18–25 từ/câu, tuyến tính.
- Hành động: 5–12 từ/câu, động từ mạnh.
- Thẩm vấn: 10–18 từ/câu.
- Khoảng lặng: một hình ảnh cụ thể, không chồng ba ẩn dụ.
- Mỗi chương tối đa 5 câu trên 35 từ sau vòng polish.

### 10.4. Từ và mô-típ phải giảm

- Giảm mạnh: “khẽ”, “ánh mắt”, “cẩn thận”, “hoàn toàn”, “chính thức”, “lập tức”, “run rẩy”, “trĩu nặng”, “nghẹn ngào”.
- Không lặp cụm chỉ khoảng thời gian vụ cũ quá hai lần trong một chương.
- Không kết chương bằng câu tuyên bố “cuộc điều tra bắt đầu”, “đồng hồ đếm ngược kích hoạt” hoặc “sự thật đang chờ”.
- Mưa, sương, đèn vàng, khói thuốc chỉ dùng khi có chức năng cảnh hoặc chứng cứ.

### 10.5. Hư cấu hóa bắt buộc

- Không dùng tên quốc gia, địa danh thật, cơ quan thật, luật thật, cấp hàm thật hoặc mẫu biển số thật.
- Không dùng cụm phương hướng địa lý có thể chỉ thẳng tới một vùng ngoài đời; dùng “thượng lưu”, “hạ lưu”, “vùng biên viễn hư cấu”.
- Dùng danh xưng trung tính đã có trong `world_rules.json`.
- Không trích số điều luật hoặc mức hình phạt từ hệ thống ngoài đời.
- Trước khi đưa revision cho tác giả, chạy quét danh sách từ cấm trong `meta/directives.json`.

---

## 11. Trình tự thi hành bắt buộc

### Giai đoạn A — Sửa dữ liệu nền, chưa viết chương

1. Tạo snapshot tên `pre_fair_play_v3`.
2. Xác nhận baseline là 15 file trong `chapters/`, không lấy revision mới nhất tự động.
3. Cập nhật `outlines/layered_outline.json` theo thứ tự Chương 8 bến nước, Chương 9 thung lũng.
4. Cập nhật `characters/characters.json`: mức độ tội lỗi N1–N5, hành trình K, trách nhiệm M.
5. Cập nhật `world/world_rules.json`: cơ chế gài sáu rương, dòng tiền, timeline V3, quy tắc lệnh và chuỗi bảo quản.
6. Thay thế `world/foreshadow_ledger.json` bằng ma trận C01–C21; đóng các tuyến cũ không còn đúng.
7. Cập nhật `world/relationships.json` và `world/state_changes.json`; không để hai file trống.
8. Ghi quyết định V3 vào `decisions.jsonl` và đánh dấu directive kế hoạch cũ là superseded, không xóa lịch sử.
9. Chạy `rebuild` và xác nhận không còn projection stale trước khi viết.

### Giai đoạn B — Hồi I, Chương 1–5

1. Với từng chương: `impact` → `context` → `plan` → `draft` revision mới có facts.
2. Không accept ngay từng chương.
3. Sau Chương 5, đọc liền Hồi I và kiểm tra:
   - K đã xuất hiện trực tiếp.
   - Không còn knowledge leak ở Chương 3.
   - Khoản tiền và sổ vật tư đã được gieo.
   - Ba vụ cũ có dấu cơ học đủ để độc giả nghi án mạng.
4. Chạy diff, style-lint và review cả cụm.
5. Chờ tác giả duyệt rồi mới accept theo thứ tự 1→5.

### Giai đoạn C — Hồi II, Chương 6–10

1. Sửa Chương 6–7.
2. Viết revision Chương 8 mới theo chức năng hiện trường N5.
3. Viết revision Chương 9 mới theo chức năng thung lũng và K.
4. Sửa Chương 10 sau khi timeline 18:00 thứ Năm–17:00 thứ Sáu đã khóa.
5. Kiểm tra:
   - I không bỏ mặc N5 để nghe kể chuyện.
   - M đến sau án và có bốn nguồn khóa alibi.
   - Vụ cũ được phục hồi trước mở niêm phong.
   - Chiếc thước không tham gia giám định.
6. Chờ tác giả duyệt rồi accept 6→10.

### Giai đoạn D — Hồi III, Chương 11–15

1. Sửa M trước, rồi mới khóa bó chứng cứ P.
2. Chương 12 phải thu hồi tiền, sổ vật tư và kết luận lab.
3. Chương 13 chỉ viết sau khi căn cứ lệnh giữ và an ninh biệt thự đã hợp lý.
4. Chương 14 phải vượt tactical gate trước aesthetic gate.
5. Chương 15 không được thêm chứng cứ mới.
6. Chờ tác giả duyệt rồi accept 11→15.

### Giai đoạn E — Khóa bản xuất bản

1. Rebuild toàn bộ projection.
2. `threads` phải trả về 0 tuyến active không chủ ý.
3. Đối chiếu từng mốc timeline với chương.
4. Chạy style-lint và sửa 137 câu dài hiện tại xuống dưới 50 câu toàn truyện, tối đa 5 câu/chương.
5. Quét hard constraint hư cấu hóa phải pass tuyệt đối.
6. Xuất bản đọc liền mạch và kiểm tra không còn Markdown bullet trong thân truyện.
7. Chấm lại toàn tác phẩm theo bảng gate dưới đây.

---

## 12. Quality gates

### Gate từng chương

| Tiêu chí | Tối thiểu |
|---|---:|
| Consistency | 88/100 |
| Character | 84/100 |
| Continuity | 90/100 |
| Pacing | 82/100 |
| Foreshadow/Payoff | 88/100 |
| Hook | 80/100 |
| Aesthetic | 84/100 |
| Procedural | 85/100 |
| Fictional neutrality | Pass tuyệt đối |

### Gate toàn truyện

1. Không nhân vật nào biết thông tin chưa xuất hiện hoặc chưa được truyền đạt.
2. K xuất hiện trực tiếp trước 15% dung lượng.
3. Ba cơ chế án cũ được gieo trước Chương 7.
4. N1–N5 có mức độ culpability rõ và nhất quán.
5. Khoản tiền N4 có payoff pháp lý.
6. Sáu rương có một chuỗi vận chuyển khả thi từng bước.
7. P bị khóa bằng ít nhất bốn nguồn độc lập.
8. K bị khóa mỗi vụ bằng ít nhất hai nguồn độc lập ngoài lời thú nhận, toàn chuỗi có ít nhất ba loại nguồn.
9. M bị loại khỏi giết người nhưng vẫn chịu trách nhiệm.
10. Không phá chain of custody.
11. Không trì hoãn lệnh bằng thủ tục giả.
12. Cao trào không có diễn văn quá ba câu/lượt.
13. Chương 15 không tiết lộ manh mối mới.
14. `relationships.json`, `state_changes.json`, timeline và ledger đồng bộ.
15. Không còn tên/danh xưng/địa danh chỉ đích danh bối cảnh ngoài đời.

### Điểm mục tiêu thực tế

| Tiêu chí | Mục tiêu |
|---|---:|
| Premise và chủ đề | 8,8/10 |
| Logic nhân quả | 8,5/10 |
| Fair-play | 8,6/10 |
| Manh mối và payoff | 8,8/10 |
| Pháp chứng và tố tụng | 8,3/10 |
| Nhân vật | 8,4/10 |
| Nhịp truyện | 8,3/10 |
| Văn phong noir | 8,4/10 |
| Cao trào | 8,6/10 |
| Kết thúc | 8,4/10 |
| Hư cấu hóa | Pass 100% |

Điểm tổng hợp khả thi sau khi thực thi đúng: **8,4–8,7/10**.

---

## 13. Definition of Done dành cho Gemini

Gemini chỉ được báo “hoàn thành nâng cấp V3” khi đồng thời đạt tất cả điều kiện:

- Có 15 revision mới, mỗi revision có facts tương ứng.
- Tác giả đã duyệt và accept đủ 15 chương.
- Không còn mismatch giữa `chapters/`, `progress.json` và `decisions.jsonl`.
- Timeline V3 đã rebuild.
- C01–C21 đều có trạng thái resolved hoặc intentionally_open có lý do.
- Quan hệ và state changes không trống.
- Không còn knowledge leak Chương 3.
- Chương 8 đi thẳng hiện trường N5; Chương 9 mới vào bản.
- Không còn hợp đồng thép dùng để chứng minh đáy gỗ.
- Không còn dùng chiếc thước làm chuẩn pháp chứng.
- Không còn mang vật chứng gốc tới bảo tàng, nhà dân hoặc hiện trường con tin.
- Không còn phiên tòa tiết lộ ba cơ chế giết người lần đầu.
- Không còn thuật ngữ thuộc danh sách cấm hư cấu hóa.
- Đã xuất một bản đọc liền mạch và review tổng kết theo quality gates.

