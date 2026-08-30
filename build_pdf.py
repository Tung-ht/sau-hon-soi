import os
import sys
import glob
import re
import subprocess
import markdown

sys.stdout.reconfigure(encoding='utf-8')

CHAPTERS_DIR = r'c:\zNovel\novels\loi-tran-troi\chapters'
OUTPUT_HTML = r'c:\zNovel\Sau_Hon_Soi_Book.html'
OUTPUT_PDF = r'c:\zNovel\Sau_Hon_Soi_Master_Edition.pdf'
EDGE_PATH = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
ASSETS_DIR = r'c:\zNovel\assets\images'

VOLUMES = [
    {
        "title": "TẬP 1: DƯỚI XUÔI",
        "subtitle": "Mắt Xích Thứ Tư & Bẫy Đánh Lạc Hướng",
        "image": "hoi_1.jpg",
        "epigraph": "“Sông Lam Châu chảy từ đại ngàn Mường Biên xuôi về biển cả, cuốn theo những xác tàu rỉ sét và những phận người trôi dạt.”",
        "chapters": [1, 2, 3, 4, 5, 6]
    },
    {
        "title": "TẬP 2: NGƯỢC NGÀN",
        "subtitle": "Vết Dấu Nội Bộ & Kỳ Án 2005",
        "image": "hoi_2.jpg",
        "epigraph": "“Cái cây trong rừng cong queo thì mình đẽo cho thẳng được, chứ cái bụng người mình mà cong queo thì dựng cái nhà nào lên rồi cũng sập thôi con à.”",
        "author_quote": "— Lời dặn của người thợ mộc Trần Văn Cửu (1958 – 2005)",
        "chapters": [7, 8, 9, 10, 11]
    },
    {
        "title": "TẬP 3: ÁNH SÁNG CÔNG LÝ",
        "subtitle": "Bó Chứng Cứ & Vĩ Thanh Bản Dền",
        "image": "hoi_3.jpg",
        "epigraph": "“Sáu sỏi thước mộc giải oan đất trời.”",
        "author_quote": "— Đồng dao cổ truyền Mường Biên",
        "chapters": [12, 13, 14, 15]
    }
]

CSS_STYLES = """
@page {
    size: 145mm 205mm;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-center {
        content: counter(page);
        font-family: 'Times New Roman', 'Georgia', serif;
        font-size: 8.5pt;
        color: #555555;
    }
}

@page :left {
    @top-left {
        content: "HOÀNG TÙNG — SÁU HÒN SỎI";
        font-family: 'Segoe UI', 'Arial', sans-serif;
        font-size: 7.5pt;
        letter-spacing: normal;
        color: #666666;
    }
}

@page :right {
    @top-right {
        content: "TIỂU THUYẾT TRINH THÁM HÌNH SỰ";
        font-family: 'Times New Roman', 'Georgia', serif;
        font-size: 7.5pt;
        font-style: italic;
        letter-spacing: normal;
        color: #666666;
    }
}

@page :first {
    @top-left { content: normal; }
    @top-right { content: normal; }
    @bottom-center { content: normal; }
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-variant-ligatures: none;
    font-feature-settings: "liga" 0;
}

body {
    font-family: 'Times New Roman', 'Georgia', serif;
    font-size: 10.5pt;
    line-height: 1.65;
    color: #111111;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
    text-rendering: geometricPrecision;
    -webkit-font-smoothing: antialiased;
}

/* COVER PAGE: Fits STRICTLY in 150mm height */
.cover-page {
    width: 100%;
    height: 150mm !important;
    max-height: 150mm !important;
    box-sizing: border-box !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
    page-break-after: always !important;
    break-after: page !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    align-items: center !important;
    text-align: center !important;
    background: linear-gradient(135deg, #0a1128 0%, #1c2541 50%, #0b132b 100%) !important;
    color: #f8f9fa !important;
    padding: 4mm 6mm !important;
    border: 2px double rgba(212, 175, 55, 0.5) !important;
    position: relative;
    overflow: hidden !important;
}

.cover-badge {
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 6.8pt;
    font-weight: 600;
    letter-spacing: normal;
    color: #d4af37;
    text-transform: uppercase;
    padding-bottom: 2px;
    border-bottom: 1px solid rgba(212, 175, 55, 0.4);
}

.cover-author {
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 11pt;
    font-weight: 700;
    letter-spacing: normal;
    color: #ffffff;
    text-transform: uppercase;
    margin-top: 2mm;
    margin-bottom: 1mm;
}

.cover-title-group {
    margin: 1mm 0;
}

.cover-main-title {
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 20pt;
    font-weight: 700;
    letter-spacing: normal;
    color: #f4e8c1;
    text-transform: uppercase;
    line-height: 1.1;
    margin: 0;
}

.cover-subtitle {
    font-family: 'Times New Roman', 'Georgia', serif;
    font-size: 8.5pt;
    font-style: italic;
    letter-spacing: normal;
    color: #cbd5e1;
    margin-top: 1.5mm;
}

.cover-img-preview {
    width: 75mm !important;
    height: 24mm !important;
    max-height: 24mm !important;
    object-fit: cover !important;
    border-radius: 4px !important;
    border: 1px solid rgba(212, 175, 55, 0.4) !important;
    box-shadow: 0 3px 8px rgba(0,0,0,0.5) !important;
    margin: 1mm auto !important;
    display: block !important;
}

.cover-ornament {
    font-size: 8pt;
    color: #d4af37;
    margin: 1mm 0;
}

.cover-tagline {
    font-family: 'Times New Roman', 'Georgia', serif;
    font-size: 7.2pt;
    line-height: 1.35;
    color: #94a3b8;
    max-width: 95%;
    margin: 1mm auto;
    font-style: italic;
}

.cover-footer {
    border-top: 1px solid rgba(212, 175, 55, 0.3);
    padding-top: 2mm;
    width: 80%;
}

.cover-edition {
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 6.5pt;
    font-weight: 600;
    letter-spacing: normal;
    color: #d4af37;
    text-transform: uppercase;
}

/* TITLE PAGE: Fits strictly in Page 2 */
.title-page {
    width: 100%;
    height: 155mm;
    max-height: 155mm;
    box-sizing: border-box;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
    page-break-before: always;
    break-before: page;
    page-break-after: always;
    break-after: page;
    text-align: center;
    padding-top: 15mm;
    padding-bottom: 5mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
}

.title-author-name {
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 11.5pt;
    font-weight: 700;
    letter-spacing: normal;
    color: #334155;
    text-transform: uppercase;
    margin-bottom: 4mm;
}

.title-book-name {
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 21pt;
    font-weight: 700;
    letter-spacing: normal;
    color: #0f172a;
    text-transform: uppercase;
    margin-bottom: 3mm;
}

.title-book-genre {
    font-size: 8.5pt;
    font-style: italic;
    color: #64748b;
    letter-spacing: normal;
    text-transform: uppercase;
    font-family: 'Segoe UI', 'Arial', sans-serif;
}

.title-page-divider {
    width: 35px;
    height: 2px;
    background: #cbd5e1;
    margin: 5mm auto;
}

.title-page-publisher {
    font-size: 7.8pt;
    letter-spacing: normal;
    color: #475569;
    font-family: 'Segoe UI', 'Arial', sans-serif;
    text-transform: uppercase;
}

/* EPIGRAPH PAGE */
.epigraph-page {
    page-break-before: always;
    break-before: page;
    page-break-after: always;
    break-after: page;
    padding-top: 25mm;
    padding-left: 10mm;
    padding-right: 10mm;
    text-align: center;
}

.epigraph-quote {
    font-style: italic;
    font-size: 10pt;
    line-height: 1.65;
    color: #1e293b;
    margin-bottom: 4mm;
    text-indent: 0 !important;
}

.epigraph-author {
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 8pt;
    font-weight: 600;
    color: #64748b;
    letter-spacing: normal;
    text-transform: uppercase;
    text-indent: 0 !important;
}

/* TABLE OF CONTENTS */
.toc-page {
    page-break-before: always;
    break-before: page;
    page-break-after: always;
    break-after: page;
    padding-top: 6mm;
}

.toc-title {
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 14pt;
    font-weight: 700;
    letter-spacing: normal;
    text-align: center;
    text-transform: uppercase;
    margin-bottom: 5mm;
    color: #0f172a;
}

.toc-volume {
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 9pt;
    font-weight: 700;
    color: #1e3a8a;
    margin-top: 4mm;
    margin-bottom: 2mm;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 2px;
    letter-spacing: normal;
    text-transform: uppercase;
}

.toc-chapter {
    display: flex;
    justify-content: space-between;
    font-size: 8.5pt;
    line-height: 1.55;
    color: #334155;
    margin: 1mm 0;
}

.toc-chapter-title {
    flex-grow: 1;
}

/* VOLUME DIVIDER PAGE: Fits strictly in single page */
.volume-page {
    width: 100%;
    height: 155mm;
    max-height: 155mm;
    box-sizing: border-box;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
    page-break-before: always;
    break-before: page;
    page-break-after: always;
    break-after: page;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 4mm 4mm;
    overflow: hidden;
}

.volume-img {
    width: 95mm;
    height: 48mm;
    max-height: 48mm;
    object-fit: cover;
    border-radius: 4px;
    border: 1px solid #cbd5e1;
    box-shadow: 0 3px 10px rgba(0,0,0,0.15);
    margin-bottom: 3mm;
}

.volume-number {
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 13.5pt;
    font-weight: 700;
    letter-spacing: normal;
    color: #0f172a;
    text-transform: uppercase;
    margin: 0;
}

.volume-subtitle {
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 8.5pt;
    font-weight: 600;
    color: #475569;
    margin-top: 1.5mm;
    margin-bottom: 2.5mm;
    text-transform: uppercase;
    letter-spacing: normal;
}

.volume-divider {
    font-size: 9pt;
    color: #94a3b8;
    margin-bottom: 2.5mm;
}

.volume-epigraph {
    font-style: italic;
    font-size: 8.2pt;
    color: #64748b;
    max-width: 92%;
    line-height: 1.4;
    text-indent: 0 !important;
}

/* CHAPTER FORMATTING */
.chapter-container {
    page-break-before: always;
    break-before: page;
    padding-top: 6mm;
}

.chapter-header {
    text-align: center;
    margin-bottom: 8mm;
}

.chapter-number-label {
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 8.5pt;
    font-weight: 600;
    letter-spacing: normal;
    color: #64748b;
    text-transform: uppercase;
    margin-bottom: 2mm;
}

.chapter-title {
    font-family: 'Times New Roman', 'Georgia', serif;
    font-size: 14.5pt;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 3mm 0;
    line-height: 1.3;
}

.chapter-divider {
    font-size: 9pt;
    color: #cbd5e1;
}

.chapter-body p {
    text-align: justify;
    text-justify: inter-word;
    text-indent: 1.5em;
    margin: 0;
    margin-bottom: 0.55em;
    line-height: 1.65;
}

.chapter-body p.no-indent,
.chapter-body > p:first-of-type {
    text-indent: 0 !important;
}

.chapter-body p.dialogue {
    text-indent: 0 !important;
    text-align: justify;
    margin-top: 0.3em !important;
    margin-bottom: 0.45em !important;
    padding-left: 0.5em !important;
    line-height: 1.65 !important;
}

.chapter-body > p:first-of-type::first-letter {
    font-family: 'Times New Roman', 'Georgia', serif;
    font-size: 2.8em;
    float: left;
    line-height: 0.8;
    margin-right: 0.12em;
    margin-top: 0.08em;
    color: #0f172a;
    font-weight: 700;
}

/* BLOCKQUOTE & POETRY: STRICT ZERO INDENTATION ON ALL LINES */
.chapter-body blockquote,
blockquote,
.poetry-block {
    margin: 4mm 0 4mm 6mm !important;
    padding: 2.5mm 0 2.5mm 5mm !important;
    border-left: 2.5px solid #64748b !important;
    font-style: italic;
    color: #334155;
    background: transparent !important;
}

.chapter-body blockquote p,
blockquote p,
.poetry-block p {
    text-indent: 0 !important;
    text-align: left !important;
    margin: 0 !important;
    line-height: 1.65 !important;
}

.chapter-body hr {
    border: none;
    text-align: center;
    margin: 5mm 0;
}

.chapter-body hr::before {
    content: "❖   ❖   ❖";
    font-size: 8pt;
    color: #94a3b8;
}

/* APPENDIX & BACK MATTER */
.appendix-page {
    page-break-before: always;
    break-before: page;
    padding-top: 8mm;
}

.appendix-title {
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 12.5pt;
    font-weight: 700;
    letter-spacing: normal;
    text-align: center;
    text-transform: uppercase;
    color: #0f172a;
    margin-bottom: 5mm;
}

.clue-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    margin: 4mm 0;
}

.clue-table th, .clue-table td {
    border: 1px solid #cbd5e1;
    padding: 5px 7px;
    text-align: left;
}

.clue-table th {
    background-color: #f1f5f9;
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 7.5pt;
    font-weight: 700;
    letter-spacing: normal;
}

.colophon-page {
    page-break-before: always;
    break-before: page;
    height: 150mm;
    max-height: 150mm;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    font-size: 8pt;
    color: #64748b;
    line-height: 1.6;
    text-align: center;
    padding-bottom: 8mm;
    font-family: 'Segoe UI', 'Arial', sans-serif;
    overflow: hidden;
}
"""

def clean_markdown_for_book(md_content):
    lines = md_content.strip().split('\n')
    title = ""
    if lines and lines[0].startswith('# '):
        title = lines[0].replace('# ', '').strip()
        lines = lines[1:]
    
    processed_text = '\n'.join(lines)
    html = markdown.markdown(processed_text, extensions=['extra', 'smarty'])
    html = re.sub(r'<p>—', r'<p class="dialogue">—', html)
    return title, html

def build_complete_book():
    print("Reading all 15 chapters...")
    chapter_files = sorted(glob.glob(os.path.join(CHAPTERS_DIR, '*.md')))
    
    chapters_data = {}
    for f in chapter_files:
        filename = os.path.basename(f)
        match = re.search(r'(\d+)', filename)
        if match:
            ch_num = int(match.group(1))
            with open(f, 'r', encoding='utf-8') as fp:
                content = fp.read()
            title, html = clean_markdown_for_book(content)
            chapters_data[ch_num] = {
                "num": ch_num,
                "title": title,
                "html": html
            }
            print(f"  Loaded Chapter {ch_num}: {title}")

    # Build TOC Items
    toc_html = '<div class="toc-page">'
    toc_html += '<div class="toc-title">MỤC LỤC</div>'
    
    for vol in VOLUMES:
        toc_html += f'<div class="toc-volume">{vol["title"]}</div>'
        for ch_num in vol["chapters"]:
            if ch_num in chapters_data:
                ch = chapters_data[ch_num]
                toc_html += f'''
                <div class="toc-chapter">
                    <span class="toc-chapter-title">{ch["title"]}</span>
                </div>
                '''
    toc_html += '<div class="toc-volume">PHỤ LỤC & TÀI LIỆU</div>'
    toc_html += '<div class="toc-chapter"><span class="toc-chapter-title">Phụ lục 1: Toàn văn Bài đồng dao cổ Lũng Nậm</span></div>'
    toc_html += '<div class="toc-chapter"><span class="toc-chapter-title">Phụ lục 2: Sơ đồ Ma trận Pháp chứng & 6 Hòn Sỏi</span></div>'
    toc_html += '<div class="toc-chapter"><span class="toc-chapter-title">Lời bạt của Tác giả Hoàng Tùng</span></div>'
    toc_html += '</div>'

    key_visual_path = os.path.join(ASSETS_DIR, 'key_visual.jpg').replace(os.sep, '/')

    full_html = f'''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Sáu Hòn Sỏi - Tác giả Hoàng Tùng</title>
    <style>
    {CSS_STYLES}
    </style>
</head>
<body>

<!-- BÌA SÁCH (COVER) -->
<div class="cover-page">
    <div class="cover-badge">TIỂU THUYẾT TRINH THÁM HÌNH SỰ ĐIỀU TRA QUY CHUẨN</div>
    <div class="cover-author">HOÀNG TÙNG</div>
    <div class="cover-title-group">
        <h1 class="cover-main-title">SÁU HÒN SỎI</h1>
        <div class="cover-subtitle">LỜI TRĂN TRỐI & KỲ ÁN LŨNG NẬM</div>
        <div class="cover-ornament">❖ ❖ ❖</div>
        <img class="cover-img-preview" src="file:///{key_visual_path}" alt="Tranh minh họa chủ đạo">
        <p class="cover-tagline">“Khi lưỡi dao báo thù tì sát cổ họng kẻ chủ mưu, thứ duy nhất có thể hóa giải mười chín năm oan khuất không phải là họng súng, mà là một chiếc thước mộc gỗ lim mòn vẹt...”</p>
    </div>
    <div class="cover-footer">
        <div class="cover-edition">BẢN THẢO XUẤT BẢN CHÍNH THỨC — 2026</div>
    </div>
</div>

<!-- TRANG TÊN SÁCH (TITLE PAGE) -->
<div class="title-page">
    <div>
        <div class="title-author-name">HOÀNG TÙNG</div>
        <div class="title-book-name">SÁU HÒN SỎI</div>
        <div class="title-book-genre">Tiểu thuyết Trinh thám — Điều tra Quy chuẩn Hiện trường</div>
        <div class="title-page-divider"></div>
        <div style="font-size: 10pt; color: #444; font-style: italic;">Hành trình 11 năm đi tìm công lý và di vật chiếc thước mộc của người cha</div>
    </div>
    <div class="title-page-publisher">
        <div>DỰ ÁN VĂN HỌC TRINH THÁM ĐƯƠNG ĐẠI</div>
        <div style="font-size: 7.5pt; color: #888; margin-top: 2mm;">HOÀN TẤT & ĐỦ ĐIỀU KIỆN XUẤT BẢN TOÀN CẦU</div>
    </div>
</div>

<!-- TRANG ĐỀ TỪ (EPIGRAPH) -->
<div class="epigraph-page">
    <div class="epigraph-quote">
        “Cái cây gỗ trong rừng có cong queo thì mình đẽo cho thẳng được, chứ cái bụng người mình mà cong queo thì dựng cái nhà nào lên rồi cũng sập thôi con à.”
    </div>
    <div class="epigraph-author">— LỜI DẶN CỦA NGƯỜI THỢ MỘC TRẦN VĂN CỬU (1958 – 2005)</div>
    <div style="margin-top: 12mm;" class="epigraph-quote">
        “Một sỏi nhặt lá me rơi,<br>
        Hai sỏi gai nhọn cào phơi vách đèo.<br>
        Ba sỏi hạt đắng lưng đèo,<br>
        Bốn sỏi xương cá lạnh theo thác ngàn.<br>
        Năm sỏi bến nước đò tan,<br>
        Sáu sỏi thước mộc giải oan đất trời.”
    </div>
    <div class="epigraph-author">— ĐỒNG DAO ĐẾM SỎI DÂN GIAN MƯỜNG BIÊN</div>
</div>

<!-- MỤC LỤC -->
{toc_html}
'''

    # Render Chapters by Volume
    for vol in VOLUMES:
        vol_img_path = os.path.join(ASSETS_DIR, vol["image"]).replace(os.sep, '/')
        full_html += f'''
        <div class="volume-page">
            <img class="volume-img" src="file:///{vol_img_path}" alt="{vol['title']}">
            <h2 class="volume-number">{vol["title"]}</h2>
            <div class="volume-subtitle">{vol["subtitle"]}</div>
            <div class="volume-divider">❖   ❖   ❖</div>
            <div class="volume-epigraph">{vol["epigraph"]}</div>
            {f'<div style="font-size: 8.5pt; color: #94a3b8; margin-top: 3mm; text-indent: 0 !important;">{vol["author_quote"]}</div>' if "author_quote" in vol else ''}
        </div>
        '''
        
        for ch_num in vol["chapters"]:
            if ch_num in chapters_data:
                ch = chapters_data[ch_num]
                raw_title = ch["title"]
                parts = raw_title.split("—")
                if len(parts) > 1:
                    num_str = f"CHƯƠNG {parts[0].strip()}"
                    name_str = parts[1].strip()
                else:
                    num_str = f"CHƯƠNG {ch_num}"
                    name_str = raw_title
                
                full_html += f'''
                <div class="chapter-container">
                    <div class="chapter-header">
                        <div class="chapter-number-label">{num_str}</div>
                        <h3 class="chapter-title">{name_str}</h3>
                        <div class="chapter-divider">— ❖ —</div>
                    </div>
                    <div class="chapter-body">
                        {ch["html"]}
                    </div>
                </div>
                '''

    # BACK MATTER & APPENDICES
    full_html += '''
    <!-- PHỤ LỤC 1 -->
    <div class="appendix-page">
        <div class="appendix-title">PHỤ LỤC 1: BÀI ĐỒNG DAO ĐẾM SỎI LŨNG NẬM</div>
        <p style="text-align: justify; font-size: 9pt; color: #475569; margin-bottom: 4mm;">
            Bài đồng dao đếm 6 nấc sỏi là trò chơi truyền miệng ngàn đời của trẻ con đồng bào bản Dền, thung lũng Lũng Nậm bên dòng suối Nậm. Dưới đây là văn bản nguyên tác đối chiếu bản dịch thơ tiếng phổ thông của Giáo sư Lê Đăng Khoa:
        </p>
        
        <table class="clue-table">
            <thead>
                <tr>
                    <th style="width: 14%;">Nấc sỏi</th>
                    <th style="width: 46%;">Nguyên tác tiếng Lũng Nậm cổ</th>
                    <th style="width: 40%;">Bản dịch thơ Lục bát phổ thông</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Hòn 1</strong></td>
                    <td><em>Nừng thày — bạ mạy hua nặm</em></td>
                    <td>Một sỏi nhặt lá me rơi</td>
                </tr>
                <tr>
                    <td><strong>Hòn 2</strong></td>
                    <td><em>Sóng thày — nhả khảm phia hin</em></td>
                    <td>Hai sỏi gai nhọn cào phơi vách đèo</td>
                </tr>
                <tr>
                    <td><strong>Hòn 3</strong></td>
                    <td><em>Xảm thày — mác muồng nả bẩu</em></td>
                    <td>Ba sỏi hạt đắng lưng đèo</td>
                </tr>
                <tr>
                    <td><strong>Hòn 4</strong></td>
                    <td><em>Xí thày — pa nặm vảng sâu</em></td>
                    <td>Bốn sỏi xương cá lạnh theo thác ngàn</td>
                </tr>
                <tr>
                    <td><strong>Hòn 5</strong></td>
                    <td><em>Hả thày — tha đò bến lạnh</em></td>
                    <td>Năm sỏi bến nước đò tan</td>
                </tr>
                <tr>
                    <td><strong>Hòn 6</strong></td>
                    <td><em>Hốc thày — mạy lim dăng trời</em></td>
                    <td>Sáu sỏi thước mộc giải oan đất trời</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- PHỤ LỤC 2 -->
    <div class="appendix-page">
        <div class="appendix-title">PHỤ LỤC 2: MA TRẬN 6 VẬT CHỨNG & PHÁP CHỨNG</div>
        <table class="clue-table">
            <thead>
                <tr>
                    <th>Nấc</th>
                    <th>Nạn nhân / Đối tượng</th>
                    <th>Địa bàn</th>
                    <th>Vật chứng để lại</th>
                    <th>Cơ chế kỹ thuật / Pháp chứng</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td>Hoàng Văn Nhẫn (Lò Văn Thìn)</td>
                    <td>Rừng Quỳnh Lâm (2021)</td>
                    <td>1 lá me rừng khô</td>
                    <td>Rút chốt giá gỗ xưởng cưa</td>
                </tr>
                <tr>
                    <td>2</td>
                    <td>Phạm Văn Sáu (Sùng A Đở)</td>
                    <td>Mỏ đá Tây Phong (2022)</td>
                    <td>2 mẩu dây gai rừng</td>
                    <td>Kích nổ nêm nén vách đá vôi</td>
                </tr>
                <tr>
                    <td>3</td>
                    <td>Đặng Văn Mười (Bàn Văn Chắt)</td>
                    <td>Cảng Hải Khê (2023)</td>
                    <td>3 hạt muồng đen khô</td>
                    <td>Khóa van khí trơ buồng đáy tàu</td>
                </tr>
                <tr>
                    <td>4</td>
                    <td>Nguyễn Văn Tư (Lý Văn Mằn)</td>
                    <td>Hạ An (2024)</td>
                    <td>4 bộ xương cá bống đá</td>
                    <td>Siết cổ cơ học & D-Alkaloid Đoan Đắng</td>
                </tr>
                <tr>
                    <td>5</td>
                    <td>Bùi Văn Vượng (Nhân chứng gian)</td>
                    <td>Bến suối Lũng Nậm (2024)</td>
                    <td>5 hòn sỏi suối xám chì</td>
                    <td>Nhát đâm bó mạch nách lính trinh sát</td>
                </tr>
                <tr>
                    <td>6</td>
                    <td>Hoàng Đình Thao (Kẻ chủ mưu)</td>
                    <td>Biệt thự Mường Biên (2024)</td>
                    <td>Chiếc thước mộc gỗ lim</td>
                    <td>Bút tích phôi lệnh xe TN-1479, Keo Poly-resin & Cưa đĩa 4mm</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- LỜI BẠT -->
    <div class="appendix-page">
        <div class="appendix-title">LỜI BẠT CỦA TÁC GIẢ HOÀNG TÙNG</div>
        <p style="text-align: justify; text-indent: 1.5em; line-height: 1.6; font-size: 10pt;">
            <em>Sáu Hòn Sỏi</em> được khởi thảo từ khát khao khắc họa một tác phẩm trinh thám hình sự mang đậm linh hồn và bản sắc hiện thực Việt Nam. Nơi đó, cuộc đấu tranh bảo vệ công lý không chỉ diễn ra giữa các thiết bị đo quang phổ XRF sắc lạnh hay những quy chuẩn tố tụng tư pháp khắt khe, mà trước hết là cuộc đấu tranh thầm lặng trong tâm khảm của mỗi con người trước lằn ranh tha hóa của quyền lực.
        </p>
        <p style="text-align: justify; text-indent: 1.5em; line-height: 1.6; font-size: 10pt;">
            Hình ảnh chiếc thước mộc bằng gỗ lim của người thợ mộc Trần Văn Cửu — với những vết khắc mòn vẹt sau mười chín năm oan khuất — chính là chiếc neo đạo đức bất biến. Dù giông bão thời cuộc hay sự toan tính cá nhân có bẻ cong những phán quyết tạm thời, thì sự ngay thẳng và phẩm giá của người lao động lương thiện vẫn luôn tìm được con đường trở về với ánh sáng.
        </p>
        <p style="text-align: right; font-style: italic; margin-top: 6mm; font-size: 9.5pt; color: #475569;">
            <strong>Tác giả: Hoàng Tùng</strong><br>
            Hạ An – Mường Biên – Mùa thu 2026
        </p>
    </div>

    <!-- TRANG XUẤT BẢN (COLOPHON) -->
    <div class="colophon-page">
        <div style="font-weight: 700; color: #1e293b; margin-bottom: 2mm;">SÁU HÒN SỎI — TIỂU THUYẾT TRINH THÁM HÌNH SỰ ĐIỀU TRA</div>
        <div>Tác giả: Hoàng Tùng</div>
        <div>Định dạng: Sách in tiêu chuẩn A5 (145 x 205 mm) & Bản PDF Sách Điện Tử Xuất Bản</div>
        <div>Dung lượng: 40.800 từ / 15 Chương hoàn chỉnh</div>
        <div>Bản quyền tác phẩm © 2026 Hoàng Tùng. Mọi quyền được bảo lưu.</div>
    </div>

</body>
</html>
'''

    print(f"Writing master HTML to {OUTPUT_HTML}...")
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as fp:
        fp.write(full_html)
    print("Master HTML created successfully.")

    print(f"Rendering PDF using Microsoft Edge headless engine...")
    cmd = [
        EDGE_PATH,
        '--headless',
        '--disable-gpu',
        '--allow-file-access-from-files',
        f'--print-to-pdf={OUTPUT_PDF}',
        '--no-pdf-header-footer',
        f'file:///{OUTPUT_HTML.replace(os.sep, "/")}'
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        pdf_size = os.path.getsize(OUTPUT_PDF)
        print(f"PDF GENERATED SUCCESSFULLY! Path: {OUTPUT_PDF} (Size: {pdf_size:,} bytes)")
    else:
        print(f"PDF generation failed with error: {res.stderr}")

if __name__ == '__main__':
    build_complete_book()
