import os
import sys
import glob
import re
import markdown
import json

sys.stdout.reconfigure(encoding='utf-8')

CHAPTERS_DIR = r'c:\zNovel\novels\loi-tran-troi\chapters'
OUTPUT_INDEX = r'c:\zNovel\index.html'

VOLUMES = [
    {
        "id": "tap-1",
        "vol_num": 1,
        "title": "TẬP 1: DƯỚI XUÔI",
        "subtitle": "Mắt Xích Thứ Tư & Bẫy Đánh Lạc Hướng",
        "image": "assets/images/hoi_1.jpg",
        "epigraph": "“Sông Lam Châu chảy từ đại ngàn Mường Biên xuôi về biển cả, cuốn theo những xác tàu rỉ sét và những phận người trôi dạt.”",
        "chapters": [1, 2, 3, 4, 5, 6]
    },
    {
        "id": "tap-2",
        "vol_num": 2,
        "title": "TẬP 2: NGƯỢC NGÀN",
        "subtitle": "Vết Dấu Nội Bộ & Kỳ Án 2005",
        "image": "assets/images/hoi_2.jpg",
        "epigraph": "“Cái cây trong rừng cong queo thì mình đẽo cho thẳng được, chứ cái bụng người mình mà cong queo thì dựng cái nhà nào lên rồi cũng sập thôi con à.”",
        "author_quote": "— Lời dặn của người thợ mộc Trần Văn Cửu (1958 – 2005)",
        "chapters": [7, 8, 9, 10, 11]
    },
    {
        "id": "tap-3",
        "vol_num": 3,
        "title": "TẬP 3: ÁNH SÁNG CÔNG LÝ",
        "subtitle": "Bó Chứng Cứ & Vĩ Thanh Bản Dền",
        "image": "assets/images/hoi_3.jpg",
        "epigraph": "“Sáu sỏi thước mộc giải oan đất trời.”",
        "author_quote": "— Đồng dao cổ truyền Mường Biên",
        "chapters": [12, 13, 14, 15]
    }
]

def clean_markdown(md_content):
    lines = md_content.strip().split('\n')
    title = ""
    if lines and lines[0].startswith('# '):
        title = lines[0].replace('# ', '').strip()
        lines = lines[1:]
    
    processed_text = '\n'.join(lines)
    html = markdown.markdown(processed_text, extensions=['extra', 'smarty'])
    html = re.sub(r'<p>—', r'<p class="dialogue">—', html)
    return title, html

def build_web():
    chapter_files = sorted(glob.glob(os.path.join(CHAPTERS_DIR, '*.md')))
    chapters_data = {}
    for f in chapter_files:
        filename = os.path.basename(f)
        match = re.search(r'(\d+)', filename)
        if match:
            ch_num = int(match.group(1))
            with open(f, 'r', encoding='utf-8') as fp:
                content = fp.read()
            title, html = clean_markdown(content)
            
            raw_title = title
            parts = raw_title.split("—")
            if len(parts) > 1:
                num_str = f"Chương {parts[0].strip()}"
                name_str = parts[1].strip()
            else:
                num_str = f"Chương {ch_num}"
                name_str = raw_title
                
            chapters_data[ch_num] = {
                "num": ch_num,
                "num_str": num_str,
                "name_str": name_str,
                "title": title,
                "html": html
            }

    web_html = f'''<!DOCTYPE html>
<html lang="vi" data-theme="dark" data-font="be-vietnam">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sáu Hòn Sỏi — Hoàng Tùng | Tiểu Thuyết Trinh Thám Procedural Noir</title>
    <meta name="description" content="Tiểu thuyết trinh thám hình sự procedural noir 'Sáu Hòn Sỏi' của tác giả Hoàng Tùng. Khám phá kỳ án Lũng Nậm và di vật chiếc thước mộc.">
    
    <!-- Google Fonts with full Vietnamese support -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,500;1,600&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&family=Merriweather:ital,wght@0,300;0,400;0,700;0,900;1,300;1,400&display=swap" rel="stylesheet">
    
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>

    <style>
    :root {{
        /* Theme: Dark (Default Noir) */
        --bg-main: #0b132b;
        --bg-card: #1c2541;
        --bg-glass: rgba(28, 37, 65, 0.88);
        --hero-bg: radial-gradient(circle at center, #1e293b 0%, #0b132b 100%);
        --text-main: #e2e8f0;
        --text-muted: #94a3b8;
        --accent-gold: #d4af37;
        --accent-blue: #38bdf8;
        --border-color: rgba(212, 175, 55, 0.25);
        --reading-bg: #0f172a;
        --reading-text: #f1f5f9;
        --shadow-elevation: 0 10px 30px -10px rgba(0, 0, 0, 0.7);
        --font-content: 'Be Vietnam Pro', sans-serif;
        --content-font-size: 1.08rem;
        --content-line-height: 1.75;
    }}

    [data-theme="light"] {{
        /* Theme: Light */
        --bg-main: #f8fafc;
        --bg-card: #ffffff;
        --bg-glass: rgba(255, 255, 255, 0.92);
        --hero-bg: linear-gradient(180deg, #ffffff 0%, #f1f5f9 60%, #e2e8f0 100%);
        --text-main: #0f172a;
        --text-muted: #64748b;
        --accent-gold: #b45309;
        --accent-blue: #0284c7;
        --border-color: rgba(180, 83, 9, 0.2);
        --reading-bg: #ffffff;
        --reading-text: #1e293b;
        --shadow-elevation: 0 10px 30px -10px rgba(0, 0, 0, 0.08);
    }}

    [data-theme="sepia"] {{
        /* Theme: Sepia (Warm Paper) */
        --bg-main: #f4ecd8;
        --bg-card: #faf3e0;
        --bg-glass: rgba(250, 243, 224, 0.92);
        --hero-bg: linear-gradient(180deg, #faf3e0 0%, #f4ecd8 60%, #ebe0cb 100%);
        --text-main: #3d2f1d;
        --text-muted: #7c6853;
        --accent-gold: #8c531b;
        --accent-blue: #2c6e80;
        --border-color: rgba(140, 83, 27, 0.25);
        --reading-bg: #faf3e0;
        --reading-text: #3d2f1d;
        --shadow-elevation: 0 10px 30px -10px rgba(61, 47, 29, 0.12);
    }}

    [data-font="lora"] {{ --font-content: 'Lora', 'Times New Roman', serif; }}
    [data-font="merriweather"] {{ --font-content: 'Merriweather', Georgia, serif; }}
    [data-font="be-vietnam"] {{ --font-content: 'Be Vietnam Pro', 'Segoe UI', sans-serif; }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    html {{
        scroll-behavior: smooth;
    }}

    body {{
        font-family: var(--font-content);
        background-color: var(--bg-main);
        color: var(--text-main);
        line-height: var(--content-line-height);
        transition: background-color 0.3s ease, color 0.3s ease;
        overflow-x: hidden;
    }}

    /* READING PROGRESS BAR */
    #progress-bar {{
        position: fixed;
        top: 0;
        left: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-gold), var(--accent-blue));
        z-index: 1000;
        width: 0%;
        transition: width 0.1s ease;
    }}

    /* NAVBAR */
    .navbar {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 64px;
        background: var(--bg-glass);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-bottom: 1px solid var(--border-color);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 1.5rem;
        z-index: 999;
        transition: all 0.3s ease;
    }}

    .nav-brand {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        text-decoration: none;
        color: var(--text-main);
    }}

    .nav-logo-icon {{
        color: var(--accent-gold);
    }}

    .nav-title {{
        font-family: 'Be Vietnam Pro', sans-serif;
        font-size: 1.1rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        color: var(--accent-gold);
        text-transform: uppercase;
    }}

    .nav-author {{
        font-size: 0.82rem;
        color: var(--text-muted);
        border-left: 1px solid var(--border-color);
        padding-left: 0.75rem;
        margin-left: 0.25rem;
        font-weight: 600;
    }}

    .nav-controls {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}

    .btn-icon {{
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        color: var(--text-main);
        width: 38px;
        height: 38px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s ease;
    }}

    .btn-icon:hover {{
        background: rgba(212, 175, 55, 0.15);
        color: var(--accent-gold);
        border-color: var(--accent-gold);
    }}

    /* SIDEBAR DRAWER (TOC & SETTINGS) */
    .drawer-overlay {{
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(4px);
        z-index: 1001;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s ease;
    }}

    .drawer-overlay.active {{
        opacity: 1;
        pointer-events: auto;
    }}

    .drawer {{
        position: fixed;
        top: 0;
        bottom: 0;
        left: -380px;
        width: 360px;
        max-width: 85vw;
        background: var(--bg-card);
        border-right: 1px solid var(--border-color);
        z-index: 1002;
        display: flex;
        flex-direction: column;
        transition: left 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: 10px 0 40px rgba(0,0,0,0.5);
    }}

    .drawer.active {{
        left: 0;
    }}

    .drawer-header {{
        padding: 1.25rem;
        border-bottom: 1px solid var(--border-color);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}

    .drawer-title {{
        font-family: 'Be Vietnam Pro', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--accent-gold);
        letter-spacing: 0.5px;
    }}

    .drawer-content {{
        padding: 1rem 1.25rem;
        overflow-y: auto;
        flex-grow: 1;
    }}

    .toc-group-title {{
        font-size: 0.8rem;
        font-weight: 700;
        color: var(--accent-blue);
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin: 1.2rem 0 0.5rem 0;
        padding-bottom: 4px;
        border-bottom: 1px dashed var(--border-color);
        font-family: 'Be Vietnam Pro', sans-serif;
    }}

    .toc-item-link {{
        display: block;
        padding: 0.5rem 0.6rem;
        color: var(--text-main);
        text-decoration: none;
        font-size: 0.9rem;
        border-radius: 6px;
        transition: all 0.2s ease;
        line-height: 1.4;
    }}

    .toc-item-link:hover, .toc-item-link.active {{
        background: rgba(212, 175, 55, 0.12);
        color: var(--accent-gold);
        padding-left: 0.85rem;
    }}

    /* SETTINGS MODAL */
    .settings-panel {{
        padding: 1rem;
        background: var(--bg-main);
        border-radius: 8px;
        margin-bottom: 1.2rem;
        border: 1px solid var(--border-color);
    }}

    .setting-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.75rem;
    }}

    .setting-row:last-child {{ margin-bottom: 0; }}

    .setting-label {{ font-size: 0.85rem; color: var(--text-muted); }}

    .segmented-control {{
        display: flex;
        background: var(--bg-card);
        border-radius: 6px;
        padding: 2px;
        border: 1px solid var(--border-color);
    }}

    .seg-btn {{
        background: transparent;
        border: none;
        color: var(--text-muted);
        font-size: 0.75rem;
        padding: 4px 10px;
        border-radius: 4px;
        cursor: pointer;
        font-family: inherit;
        transition: all 0.2s ease;
    }}

    .seg-btn.active {{
        background: var(--accent-gold);
        color: #000;
        font-weight: 700;
    }}

    /* HERO COVER */
    .hero {{
        min-height: 85vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 6rem 1.5rem 3.5rem 1.5rem;
        background: var(--hero-bg);
        border-bottom: 1px solid var(--border-color);
        position: relative;
        transition: background 0.3s ease;
    }}

    .hero-container {{
        max-width: 1000px;
        width: 100%;
        display: grid;
        grid-template-columns: 1fr 1.1fr;
        gap: 3rem;
        align-items: center;
    }}

    .hero-art {{
        position: relative;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: var(--shadow-elevation);
        border: 2px solid var(--border-color);
        background: var(--bg-card);
    }}

    .hero-img {{
        width: 100%;
        height: auto;
        display: block;
        transition: transform 0.5s ease;
    }}

    .hero-art:hover .hero-img {{
        transform: scale(1.03);
    }}

    .hero-info {{
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
    }}

    .hero-badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(212, 175, 55, 0.15);
        color: var(--accent-gold);
        border: 1px solid var(--accent-gold);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        width: fit-content;
        font-family: 'Be Vietnam Pro', sans-serif;
    }}

    .hero-title {{
        font-family: 'Be Vietnam Pro', 'Merriweather', sans-serif;
        font-size: 2.8rem;
        font-weight: 900;
        line-height: 1.15;
        color: var(--text-main);
        letter-spacing: 1px;
        text-transform: uppercase;
    }}

    .hero-subtitle {{
        font-size: 1.1rem;
        color: var(--accent-gold);
        font-style: italic;
        letter-spacing: 0.5px;
        font-family: 'Lora', serif;
    }}

    .hero-author-tag {{
        font-size: 1.05rem;
        color: var(--text-muted);
    }}

    .hero-author-tag strong {{
        color: var(--text-main);
        font-weight: 700;
    }}

    .hero-tagline {{
        font-size: 0.95rem;
        font-style: italic;
        color: var(--text-muted);
        border-left: 3px solid var(--accent-gold);
        padding-left: 1rem;
        line-height: 1.6;
        font-family: 'Lora', serif;
    }}

    .hero-meta-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-top: 0.5rem;
    }}

    .meta-box {{
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        padding: 0.75rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: var(--shadow-elevation);
    }}

    .meta-num {{
        font-size: 1.25rem;
        font-weight: 800;
        color: var(--accent-gold);
        font-family: 'Be Vietnam Pro', sans-serif;
    }}

    .meta-lbl {{
        font-size: 0.75rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-family: 'Be Vietnam Pro', sans-serif;
    }}

    .hero-actions {{
        display: flex;
        gap: 1rem;
        margin-top: 0.5rem;
    }}

    .btn-primary {{
        background: linear-gradient(135deg, #d4af37, #b45309);
        color: #000;
        font-weight: 700;
        padding: 0.75rem 1.75rem;
        border-radius: 8px;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.35);
        transition: all 0.2s ease;
        font-family: 'Be Vietnam Pro', sans-serif;
    }}

    .btn-primary:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
    }}

    .btn-secondary {{
        background: var(--bg-card);
        color: var(--text-main);
        border: 1px solid var(--border-color);
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        transition: all 0.2s ease;
        font-family: 'Be Vietnam Pro', sans-serif;
    }}

    .btn-secondary:hover {{
        border-color: var(--accent-gold);
        color: var(--accent-gold);
    }}

    /* MAIN NOVEL CONTAINER */
    .novel-wrapper {{
        max-width: 820px;
        margin: 0 auto;
        padding: 3rem 1.5rem;
    }}

    /* VOLUME DIVIDER HERO */
    .volume-hero {{
        margin: 5rem 0 3rem 0;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--border-color);
        background: var(--bg-card);
        box-shadow: var(--shadow-elevation);
    }}

    .volume-hero-img-wrap {{
        width: 100%;
        height: 320px;
        position: relative;
        overflow: hidden;
    }}

    .volume-hero-img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}

    .volume-hero-overlay {{
        position: absolute;
        inset: 0;
        background: linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.88) 100%);
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        padding: 2rem;
    }}

    .volume-badge {{
        font-family: 'Be Vietnam Pro', sans-serif;
        font-size: 0.8rem;
        font-weight: 700;
        color: var(--accent-gold);
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }}

    .volume-hero-title {{
        font-family: 'Be Vietnam Pro', sans-serif;
        font-size: 1.85rem;
        color: #ffffff;
        font-weight: 800;
        line-height: 1.2;
    }}

    .volume-hero-sub {{
        font-size: 0.95rem;
        color: #cbd5e1;
        font-style: italic;
        margin-top: 0.25rem;
        font-family: 'Lora', serif;
    }}

    .volume-epigraph-box {{
        padding: 1.5rem 2rem;
        font-style: italic;
        font-size: 0.95rem;
        color: var(--text-muted);
        text-align: center;
        border-top: 1px solid var(--border-color);
        font-family: 'Lora', serif;
    }}

    /* CHAPTER CARD */
    .chapter-card {{
        background: var(--reading-bg);
        color: var(--reading-text);
        border-radius: 12px;
        border: 1px solid var(--border-color);
        padding: 3rem 2.5rem;
        margin-bottom: 3.5rem;
        box-shadow: var(--shadow-elevation);
    }}

    .chapter-header-wrap {{
        text-align: center;
        margin-bottom: 2.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid var(--border-color);
    }}

    .chapter-num-tag {{
        font-family: 'Be Vietnam Pro', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        color: var(--accent-gold);
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }}

    .chapter-main-heading {{
        font-family: 'Be Vietnam Pro', 'Merriweather', sans-serif;
        font-size: 1.85rem;
        font-weight: 800;
        color: var(--reading-text);
        line-height: 1.3;
    }}

    .chapter-content p {{
        text-align: justify;
        text-justify: inter-word;
        text-indent: 1.75em;
        margin-bottom: 1rem;
        font-size: var(--content-font-size);
        line-height: var(--content-line-height);
    }}

    .chapter-content p.dialogue {{
        text-indent: 0;
        padding-left: 0.5rem;
    }}

    .chapter-content > p:first-of-type {{
        text-indent: 0;
    }}

    .chapter-content > p:first-of-type::first-letter {{
        font-family: 'Merriweather', 'Lora', serif;
        font-size: 3.2em;
        float: left;
        line-height: 0.8;
        margin-right: 0.15em;
        margin-top: 0.05em;
        color: var(--accent-gold);
        font-weight: 700;
    }}

    .chapter-content hr {{
        border: none;
        text-align: center;
        margin: 2rem 0;
    }}

    .chapter-content hr::before {{
        content: "❖   ❖   ❖";
        color: var(--accent-gold);
        font-size: 0.85rem;
        letter-spacing: 8px;
    }}

    .chapter-content blockquote {{
        margin: 1.5rem 0 1.5rem 1rem;
        padding-left: 1rem;
        border-left: 3px solid var(--accent-gold);
        font-style: italic;
        color: var(--text-muted);
    }}

    .chapter-footer-nav {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 2.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--border-color);
        font-size: 0.85rem;
        font-family: 'Be Vietnam Pro', sans-serif;
    }}

    .chapter-nav-btn {{
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        color: var(--text-muted);
        text-decoration: none;
        transition: color 0.2s ease;
    }}

    .chapter-nav-btn:hover {{
        color: var(--accent-gold);
    }}

    /* APPENDIX SECTIONS */
    .appendix-card {{
        background: var(--bg-card);
        border-radius: 12px;
        border: 1px solid var(--border-color);
        padding: 2.5rem 2rem;
        margin-bottom: 3rem;
        box-shadow: var(--shadow-elevation);
    }}

    .appendix-heading {{
        font-family: 'Be Vietnam Pro', sans-serif;
        font-size: 1.2rem;
        font-weight: 800;
        color: var(--accent-gold);
        text-align: center;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    }}

    .custom-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
        font-size: 0.88rem;
    }}

    .custom-table th, .custom-table td {{
        border: 1px solid var(--border-color);
        padding: 0.65rem 0.85rem;
        text-align: left;
    }}

    .custom-table th {{
        background: rgba(212, 175, 55, 0.1);
        color: var(--accent-gold);
        font-family: 'Be Vietnam Pro', sans-serif;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }}

    /* BACK TO TOP */
    .btn-back-top {{
        position: fixed;
        bottom: 25px;
        right: 25px;
        background: var(--accent-gold);
        color: #000;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        cursor: pointer;
        opacity: 0;
        pointer-events: none;
        transition: all 0.3s ease;
        z-index: 900;
        border: none;
    }}

    .btn-back-top.visible {{
        opacity: 1;
        pointer-events: auto;
    }}

    /* FOOTER */
    .site-footer {{
        background: var(--bg-card);
        border-top: 1px solid var(--border-color);
        padding: 3rem 1.5rem;
        text-align: center;
        font-size: 0.85rem;
        color: var(--text-muted);
    }}

    /* RESPONSIVE */
    @media (max-width: 868px) {{
        .hero-container {{ grid-template-columns: 1fr; gap: 2rem; }}
        .hero-title {{ font-size: 2.2rem; }}
        .chapter-card {{ padding: 2rem 1.25rem; }}
        .volume-hero-img-wrap {{ height: 220px; }}
        .volume-hero-title {{ font-size: 1.5rem; }}
    }}
    </style>
</head>
<body>

    <!-- PROGRESS BAR -->
    <div id="progress-bar"></div>

    <!-- NAVBAR -->
    <nav class="navbar">
        <a href="#hero" class="nav-brand">
            <i data-lucide="book-open" class="nav-logo-icon"></i>
            <span class="nav-title">SÁU HÒN SỎI</span>
            <span class="nav-author">Hoàng Tùng</span>
        </a>
        <div class="nav-controls">
            <button class="btn-icon" id="btn-theme" title="Đổi giao diện (Dark / Light / Sepia)">
                <i data-lucide="moon" id="theme-icon"></i>
            </button>
            <button class="btn-icon" id="btn-font-size" title="Cỡ chữ">
                <i data-lucide="type"></i>
            </button>
            <button class="btn-icon" id="btn-toc" title="Mục lục & Cài đặt">
                <i data-lucide="menu"></i>
            </button>
        </div>
    </nav>

    <!-- DRAWER (TOC & SETTINGS) -->
    <div class="drawer-overlay" id="drawer-overlay"></div>
    <aside class="drawer" id="drawer">
        <div class="drawer-header">
            <span class="drawer-title">Mục Lục & Cài Đặt</span>
            <button class="btn-icon" id="btn-close-drawer" style="border: none;">
                <i data-lucide="x"></i>
            </button>
        </div>
        <div class="drawer-content">
            <div class="settings-panel">
                <div class="setting-row">
                    <span class="setting-label">Font chữ</span>
                    <div class="segmented-control" id="font-selector">
                        <button class="seg-btn active" data-font="be-vietnam">Modern</button>
                        <button class="seg-btn" data-font="lora">Lora</button>
                        <button class="seg-btn" data-font="merriweather">Merri</button>
                    </div>
                </div>
                <div class="setting-row">
                    <span class="setting-label">Giao diện</span>
                    <div class="segmented-control" id="theme-selector">
                        <button class="seg-btn active" data-theme="dark">Tối</button>
                        <button class="seg-btn" data-theme="light">Sáng</button>
                        <button class="seg-btn" data-theme="sepia">Sepia</button>
                    </div>
                </div>
            </div>

            <div class="toc-group-title">Phần Mở Đầu</div>
            <a href="#hero" class="toc-item-link">Trang bìa & Giới thiệu</a>
            <a href="#epigraph" class="toc-item-link">Lời đề từ & Đồng dao</a>

            <div class="toc-group-title">TẬP 1: DƯỚI XUÔI</div>
            <a href="#chuong-1" class="toc-item-link">1. Đêm mưa phố Đò Cũ</a>
            <a href="#chuong-2" class="toc-item-link">2. Người cố vấn</a>
            <a href="#chuong-3" class="toc-item-link">3. Bóng đen bãi xác tàu</a>
            <a href="#chuong-4" class="toc-item-link">4. Đấu trí dưới đáy bùn</a>
            <a href="#chuong-5" class="toc-item-link">5. Bốn cái chết</a>
            <a href="#chuong-6" class="toc-item-link">6. Tiếng hát bản Dền</a>

            <div class="toc-group-title">TẬP 2: NGƯỢC NGÀN</div>
            <a href="#chuong-7" class="toc-item-link">7. Dấu truy cập lúc nửa đêm</a>
            <a href="#chuong-8" class="toc-item-link">8. Thung lũng oan khuất</a>
            <a href="#chuong-9" class="toc-item-link">9. Bến đò trong sương</a>
            <a href="#chuong-10" class="toc-item-link">10. Dưới đáy rương</a>
            <a href="#chuong-11" class="toc-item-link">11. Người thầy giữ im lặng</a>

            <div class="toc-group-title">TẬP 3: ÁNH SÁNG CÔNG LÝ</div>
            <a href="#chuong-12" class="toc-item-link">12. Cuộc gọi thứ sáu</a>
            <a href="#chuong-13" class="toc-item-link">13. Dấu chân trên đèo</a>
            <a href="#chuong-14" class="toc-item-link">14. Chiếc thước mộc</a>
            <a href="#chuong-15" class="toc-item-link">15. Ánh sáng thung lũng</a>

            <div class="toc-group-title">Phụ Lục & Hậu Từ</div>
            <a href="#appendix-1" class="toc-item-link">Phụ lục 1: Bài đồng dao Lũng Nậm</a>
            <a href="#appendix-2" class="toc-item-link">Phụ lục 2: Ma trận 6 Vật chứng</a>
            <a href="#author-note" class="toc-item-link">Lời bạt của Tác giả</a>
        </div>
    </aside>

    <!-- HERO SECTION -->
    <header class="hero" id="hero">
        <div class="hero-container">
            <div class="hero-art">
                <img src="assets/images/key_visual.jpg" alt="Sáu Hòn Sỏi Key Visual" class="hero-img">
            </div>
            <div class="hero-info">
                <div class="hero-badge">
                    <i data-lucide="shield-alert" style="width: 14px; height: 14px;"></i>
                    Tiểu Thuyết Trinh Thám Procedural Noir
                </div>
                <h1 class="hero-title">SÁU HÒN SỎI</h1>
                <div class="hero-subtitle">Lời Trăn Trối & Kỳ Án Lũng Nậm</div>
                <div class="hero-author-tag">Tác giả: <strong>Hoàng Tùng</strong></div>
                <p class="hero-tagline">“Khi lưỡi dao báo thù tì sát cổ họng kẻ chủ mưu, thứ duy nhất có thể hóa giải mười chín năm oan khuất không phải là họng súng, mà là một chiếc thước mộc gỗ lim mòn vẹt...”</p>
                
                <div class="hero-meta-grid">
                    <div class="meta-box">
                        <div class="meta-num">15</div>
                        <div class="meta-lbl">Chương</div>
                    </div>
                    <div class="meta-box">
                        <div class="meta-num">21K</div>
                        <div class="meta-lbl">Từ ngữ</div>
                    </div>
                    <div class="meta-box">
                        <div class="meta-num">100%</div>
                        <div class="meta-lbl">Fair-Play</div>
                    </div>
                </div>

                <div class="hero-actions">
                    <a href="#chuong-1" class="btn-primary">
                        <i data-lucide="book-open"></i> Đọc Ngay
                    </a>
                    <a href="Sau_Hon_Soi_Tieu_Thuyet_Trinh_Tham.pdf" target="_blank" class="btn-secondary">
                        <i data-lucide="download"></i> Tải Bản PDF
                    </a>
                </div>
            </div>
        </div>
    </header>

    <!-- MAIN READING CONTAINER -->
    <main class="novel-wrapper">

        <!-- EPIGRAPH -->
        <section class="appendix-card" id="epigraph" style="text-align: center;">
            <div class="appendix-heading" style="font-size: 1.1rem;">LỜI ĐỀ TỪ</div>
            <p style="font-style: italic; font-size: 1.1rem; line-height: 1.7; margin-bottom: 0.5rem; color: var(--accent-gold); font-family: 'Lora', serif;">
                “Cái cây gỗ trong rừng có cong queo thì mình đẽo cho thẳng được, chứ cái bụng người mình mà cong queo thì dựng cái nhà nào lên rồi cũng sập thôi con à.”
            </p>
            <p style="font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; font-family: 'Be Vietnam Pro', sans-serif; font-weight: 600;">
                — Lời dặn của người thợ mộc Trần Văn Cửu (1958 – 2005)
            </p>
        </section>
'''

    for vol in VOLUMES:
        web_html += f'''
        <!-- {vol["title"]} -->
        <section class="volume-hero" id="{vol["id"]}">
            <div class="volume-hero-img-wrap">
                <img src="{vol["image"]}" alt="{vol["title"]}" class="volume-hero-img">
                <div class="volume-hero-overlay">
                    <span class="volume-badge">Tập {vol["vol_num"]}</span>
                    <h2 class="volume-hero-title">{vol["title"]}</h2>
                    <p class="volume-hero-sub">{vol["subtitle"]}</p>
                </div>
            </div>
            <div class="volume-epigraph-box">
                {vol["epigraph"]}
                {f'<div style="font-size: 0.8rem; margin-top: 0.25rem; font-weight: 600;">{vol["author_quote"]}</div>' if "author_quote" in vol else ''}
            </div>
        </section>
        '''

        for ch_num in vol["chapters"]:
            if ch_num in chapters_data:
                ch = chapters_data[ch_num]
                prev_ch = ch_num - 1 if ch_num > 1 else None
                next_ch = ch_num + 1 if ch_num < 15 else None
                
                web_html += f'''
                <!-- CHƯƠNG {ch_num} -->
                <article class="chapter-card" id="chuong-{ch_num}">
                    <div class="chapter-header-wrap">
                        <div class="chapter-num-tag">{ch["num_str"]}</div>
                        <h3 class="chapter-main-heading">{ch["name_str"]}</h3>
                    </div>
                    <div class="chapter-content">
                        {ch["html"]}
                    </div>
                    <div class="chapter-footer-nav">
                        {f'<a href="#chuong-{prev_ch}" class="chapter-nav-btn"><i data-lucide="chevron-left"></i> Chương trước</a>' if prev_ch else '<span></span>'}
                        <a href="#hero" class="chapter-nav-btn"><i data-lucide="arrow-up"></i> Về đầu trang</a>
                        {f'<a href="#chuong-{next_ch}" class="chapter-nav-btn">Chương tiếp <i data-lucide="chevron-right"></i></a>' if next_ch else '<a href="#appendix-1" class="chapter-nav-btn">Phụ lục <i data-lucide="chevron-right"></i></a>'}
                    </div>
                </article>
                '''

    # APPENDICES
    web_html += '''
        <!-- PHỤ LỤC 1 -->
        <section class="appendix-card" id="appendix-1">
            <h3 class="appendix-heading">PHỤ LỤC 1: BÀI ĐỒNG DAO ĐẾM SỎI LŨNG NẬM</h3>
            <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1rem; text-align: justify;">
                Bài đồng dao đếm 6 nấc sỏi là trò chơi truyền miệng ngàn đời của trẻ con đồng bào bản Dền, thung lũng Lũng Nậm bên dòng suối Nậm. Dưới đây là văn bản nguyên tác đối chiếu bản dịch thơ tiếng phổ thông của Giáo sư Lê Đăng Khoa:
            </p>
            <div style="overflow-x: auto;">
                <table class="custom-table">
                    <thead>
                        <tr>
                            <th style="width: 15%;">Nấc</th>
                            <th style="width: 45%;">Nguyên tác tiếng Lũng Nậm cổ</th>
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
        </section>

        <!-- PHỤ LỤC 2 -->
        <section class="appendix-card" id="appendix-2">
            <h3 class="appendix-heading">PHỤ LỤC 2: MA TRẬN 6 VẬT CHỨNG & PHÁP CHỨNG</h3>
            <div style="overflow-x: auto;">
                <table class="custom-table">
                    <thead>
                        <tr>
                            <th>Nấc</th>
                            <th>Nạn nhân / Đối tượng</th>
                            <th>Địa bàn</th>
                            <th>Vật chứng</th>
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
                            <td>Bút tích phôi lệnh xe TN-1479 & Cưa đĩa 4mm</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>

        <!-- LỜI BẠT -->
        <section class="appendix-card" id="author-note">
            <h3 class="appendix-heading">LỜI BẠT CỦA TÁC GIẢ HOÀNG TÙNG</h3>
            <p style="text-align: justify; text-indent: 1.5em; line-height: 1.7; font-size: 0.95rem; margin-bottom: 1rem; font-family: 'Lora', serif;">
                <em>Sáu Hòn Sỏi</em> được khởi thảo từ khát khao khắc họa một tác phẩm trinh thám hình sự mang đậm linh hồn và bản sắc hiện thực Việt Nam. Nơi đó, cuộc đấu tranh bảo vệ công lý không chỉ diễn ra giữa các thiết bị đo quang phổ XRF sắc lạnh hay những quy chuẩn tố tụng tư pháp khắt khe, mà trước hết là cuộc đấu tranh thầm lặng trong tâm khảm của mỗi con người trước lằn ranh tha hóa của quyền lực.
            </p>
            <p style="text-align: justify; text-indent: 1.5em; line-height: 1.7; font-size: 0.95rem; font-family: 'Lora', serif;">
                Hình ảnh chiếc thước mộc bằng gỗ lim của người thợ mộc Trần Văn Cửu — với những vết khắc mòn vẹt sau mười chín năm oan khuất — chính là chiếc neo đạo đức bất biến. Dù giông bão thời cuộc hay sự toan tính cá nhân có bẻ cong những phán quyết tạm thời, thì sự ngay thẳng và phẩm giá của người lao động lương thiện vẫn luôn tìm được con đường trở về với ánh sáng.
            </p>
            <p style="text-align: right; font-style: italic; margin-top: 1.5rem; font-size: 0.9rem; color: var(--text-muted); font-family: 'Be Vietnam Pro', sans-serif;">
                <strong>Tác giả: Hoàng Tùng</strong><br>
                Hạ An – Mường Biên – Mùa thu 2026
            </p>
        </section>

    </main>

    <!-- BACK TO TOP BUTTON -->
    <button class="btn-back-top" id="btn-back-top" title="Lên đầu trang">
        <i data-lucide="arrow-up"></i>
    </button>

    <!-- FOOTER -->
    <footer class="site-footer">
        <div style="font-family: 'Be Vietnam Pro', sans-serif; font-size: 1.1rem; font-weight: 800; color: var(--accent-gold); margin-bottom: 0.5rem; text-transform: uppercase;">
            SÁU HÒN SỎI
        </div>
        <p>Tiểu thuyết Trinh thám Procedural Noir • Tác giả: Hoàng Tùng</p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem; color: var(--text-muted);">
            Bản quyền tác phẩm © 2026 Hoàng Tùng. Mọi quyền được bảo lưu.
        </p>
    </footer>

    <!-- INTERACTIVE SCRIPT -->
    <script>
        lucide.createIcons();

        // Reading Progress
        window.addEventListener('scroll', () => {
            const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            document.getElementById('progress-bar').style.width = scrolled + '%';

            const backTop = document.getElementById('btn-back-top');
            if (winScroll > 400) {
                backTop.classList.add('visible');
            } else {
                backTop.classList.remove('visible');
            }
        });

        // Back to top
        document.getElementById('btn-back-top').addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        // Drawer
        const drawer = document.getElementById('drawer');
        const overlay = document.getElementById('drawer-overlay');
        const btnToc = document.getElementById('btn-toc');
        const btnCloseDrawer = document.getElementById('btn-close-drawer');

        function openDrawer() {
            drawer.classList.add('active');
            overlay.classList.add('active');
        }

        function closeDrawer() {
            drawer.classList.remove('active');
            overlay.classList.remove('active');
        }

        btnToc.addEventListener('click', openDrawer);
        btnCloseDrawer.addEventListener('click', closeDrawer);
        overlay.addEventListener('click', closeDrawer);

        document.querySelectorAll('.toc-item-link').forEach(link => {
            link.addEventListener('click', closeDrawer);
        });

        // Theme Toggle (Dark / Light / Sepia)
        const themeBtns = document.querySelectorAll('#theme-selector .seg-btn');
        const btnThemeNav = document.getElementById('btn-theme');
        const themes = ['dark', 'light', 'sepia'];

        function updateThemeIcon(t) {
            const iconEl = document.getElementById('theme-icon');
            if (!iconEl) return;
            if (t === 'dark') {
                iconEl.setAttribute('data-lucide', 'moon');
            } else if (t === 'light') {
                iconEl.setAttribute('data-lucide', 'sun');
            } else {
                iconEl.setAttribute('data-lucide', 'coffee');
            }
            lucide.createIcons();
        }

        function setTheme(t) {
            document.documentElement.setAttribute('data-theme', t);
            themeBtns.forEach(btn => {
                btn.classList.toggle('active', btn.getAttribute('data-theme') === t);
            });
            updateThemeIcon(t);
            localStorage.setItem('novel_theme', t);
        }

        themeBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                setTheme(btn.getAttribute('data-theme'));
            });
        });

        btnThemeNav.addEventListener('click', () => {
            const current = document.documentElement.getAttribute('data-theme') || 'dark';
            const nextIdx = (themes.indexOf(current) + 1) % themes.length;
            setTheme(themes[nextIdx]);
        });

        // Font Selector
        const fontBtns = document.querySelectorAll('#font-selector .seg-btn');
        function setFont(f) {
            document.documentElement.setAttribute('data-font', f);
            fontBtns.forEach(btn => {
                btn.classList.toggle('active', btn.getAttribute('data-font') === f);
            });
            localStorage.setItem('novel_font', f);
        }

        fontBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                setFont(btn.getAttribute('data-font'));
            });
        });

        // Font Size Adjuster
        const btnFontSize = document.getElementById('btn-font-size');
        const fontSizes = ['0.95rem', '1.08rem', '1.2rem', '1.35rem'];
        let currentSizeIdx = 1;

        btnFontSize.addEventListener('click', () => {
            currentSizeIdx = (currentSizeIdx + 1) % fontSizes.length;
            document.documentElement.style.setProperty('--content-font-size', fontSizes[currentSizeIdx]);
        });

        const savedTheme = localStorage.getItem('novel_theme');
        if (savedTheme) setTheme(savedTheme);
        const savedFont = localStorage.getItem('novel_font');
        if (savedFont) setFont(savedFont);
    </script>
</body>
</html>
'''

    with open(OUTPUT_INDEX, 'w', encoding='utf-8') as fp:
        fp.write(web_html)
    print(f"Web version successfully regenerated at {OUTPUT_INDEX} (Size: {len(web_html):,} bytes)")

if __name__ == '__main__':
    build_web()
