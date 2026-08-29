# QUY TẮC BẮT BUỘC VỀ QUẢN LÝ PHIÊN BẢN GIT (AI NOVEL STUDIO & WRITING WORKSPACE)

## 1. Duy Trì Kho Lưu Trữ Git Dự Án
- Workspace `zNovel` duy trì một kho lưu trữ Git độc lập (`.git`) để quản lý phiên bản các bản thảo chương truyện, đề cương, hồ sơ nhân vật và cấu hình agent.
- Luôn kiểm tra `git status` trước và sau khi hoàn thành các mốc sáng tác lớn (hoàn thành chương, tinh chỉnh đề cương, cập nhật nhân vật).

## 2. Quy Trình Quản Lý Phiên Bản & Commit
- **Kích hoạt commit:** Khi hoàn thành một chương truyện (`output/novel/chapters/*.md`), cập nhật đề cương (`layered_outline.md`), chốt hồ sơ nhân vật (`characters.md`) hoặc cải tiến kỹ năng agent (`.agents/skills/`).
- **Quy chuẩn thông điệp Commit (Semantic):**
  - `feat(chapter)`: Thêm mới hoặc hoàn thành chương truyện (VD: `feat(chapter): Hoàn thành Chương 05 - Đêm lật hồ sơ`).
  - `refactor(chapter)`: Tinh gọn, đánh bóng hoặc viết lại chương theo phản hồi review (VD: `refactor(chapter): Tinh gọn Chương 01 và làm rõ logic điều tra`).
  - `refactor(plot)`: Cập nhật đề cương, sơ đồ phân lớp, phục bút (VD: `refactor(plot): Cập nhật đề cương Arc 1 và sổ phục bút`).
  - `fix(lore)`: Sửa mâu thuẫn dòng thời gian, nhân vật hoặc quy tắc thế giới.
  - `feat(agent)`: Cải tiến prompt, checklist hoặc quy tắc sáng tác của Agent.
  - `docs(export)`: Cập nhật tài liệu xuất bản, định dạng PDF/HTML.

## 3. Điều Cấm Tuyệt Đối & Quy Tắc An Toàn
- ❌ **CẤM COMMIT DỮ LIỆU NHẠY CẢM:**
  - API Keys / Secret Tokens: DeepSeek, OpenRouter, OpenAI, B.AI, Google Gemini (`sk-...`, `sk-or-v1-...`).
  - File cấu hình chứa key cá nhân: `config.json`, `.ainovel/config.json`, `.env`, `secrets.*`.
- ❌ **CẤM COMMIT LOG VÀ FILE DUMP QUÁ NẶNG:**
  - Session chat traces của LLM: `output/**/meta/sessions/*.jsonl` (các file hàng chục MB chứa prompt thô của subagents).
  - Runtime queue và log: `output/**/meta/runtime/`, `output/**/logs/`, `*.log`.
  - File nhị phân biên dịch: `*.exe`, `ainovel-cli.exe`, `*.dll`.
  - File tạm: `scratch/`, `*.tmp`, `*.bak`.

## 4. Danh Mục Tệp Luôn Được Theo Dõi (Tracked Assets)
- Bản thảo hoàn chỉnh: `output/novel/chapters/*.md`
- Đề cương & Thế giới: `output/novel/layered_outline.md`, `characters.md`, `world_rules.md`, `foreshadow_ledger.md`
- Đánh giá & Tóm tắt: `output/novel/reviews/*.json`, `output/novel/summaries/*.json`
- Prompt & Kỹ năng: `.agents/skills/ai-novel-studio/` và `.agents/rules/`

