import os
import sys
import glob
import re
import markdown

sys.stdout.reconfigure(encoding='utf-8')

CHAPTERS_DIR = r'c:\zNovel\novels\loi-tran-troi\chapters'
OUTPUT_WEB = r'c:\zNovel\index.html'
ASSETS_DIR = r'c:\zNovel\assets\images'

VOLUMES = [
    {
        "id": "tap-1",
        "title": "TẬP 1: DƯỚI XUÔI",
        "subtitle": "Mắt Xích Thứ Tư & Bẫy Đánh Lạc Hướng",
        "image": "assets/images/hoi_1.jpg",
        "epigraph": "“Sông Lam Châu chảy từ đại ngàn Mường Biên xuôi về biển cả, cuốn theo những xác tàu rỉ sét và những phận người trôi dạt.”",
        "chapters": [1, 2, 3, 4, 5, 6]
    },
    {
        "id": "tap-2",
        "title": "TẬP 2: NGƯỢC NGÀN",
        "subtitle": "Vết Dấu Nội Bộ & Kỳ Án 2005",
        "image": "assets/images/hoi_2.jpg",
        "epigraph": "“Cái cây trong rừng cong queo thì mình đẽo cho thẳng được, chứ cái bụng người mình mà cong queo thì dựng cái nhà nào lên rồi cũng sập thôi con à.”",
        "author_quote": "— Lời dặn của người thợ mộc Trần Văn Cửu (1958 – 2005)",
        "chapters": [7, 8, 9, 10, 11]
    },
    {
        "id": "tap-3",
        "title": "TẬP 3: ÁNH SÁNG CÔNG LÝ",
        "subtitle": "Bó Chứng Cứ & Vĩ Thanh Bản Dền",
        "image": "assets/images/hoi_3.jpg",
        "epigraph": "“Sáu sỏi thước mộc giải oan đất trời.”",
        "author_quote": "— Đồng dao cổ truyền Mường Biên",
        "chapters": [12, 13, 14, 15]
    }
]

CSS_WEB = """
    :root {
        /* Theme: Nền Tối */
        --bg-body: #0a0d14;
        --bg-surface: #111625;
        --bg-surface-elevated: #182032;
        --text-main: #e2e8f0;
        --text-muted: #94a3b8;
        --accent-gold: #d4af37;
        --accent-gold-light: #f4e8c1;
        --accent-blue: #38bdf8;
        --border-color: rgba(212, 175, 55, 0.2);
        --border-subtle: rgba(255, 255, 255, 0.08);
        --shadow-elevation: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        --font-content: 'Be Vietnam Pro', sans-serif;
        --content-font-size: 1.08rem;
    }

    [data-theme="light"] {
        /* Theme: Nền Sáng */
        --bg-body: #f8fafc;
        --bg-surface: #ffffff;
        --bg-surface-elevated: #f1f5f9;
        --text-main: #0f172a;
        --text-muted: #475569;
        --accent-gold: #b45309;
        --accent-gold-light: #78350f;
        --accent-blue: #0284c7;
        --border-color: rgba(180, 83, 9, 0.25);
        --border-subtle: rgba(0, 0, 0, 0.08);
        --shadow-elevation: 0 10px 25px -5px rgba(0, 0, 0, 0.08);
    }

    [data-theme="sepia"] {
        /* Theme: Giấy Cũ */
        --bg-body: #f4ecd8;
        --bg-surface: #faf4e8;
        --bg-surface-elevated: #ede3c8;
        --text-main: #2d241e;
        --text-muted: #6b5d52;
        --accent-gold: #964208;
        --accent-gold-light: #5c2805;
        --accent-blue: #1e5f74;
        --border-color: rgba(150, 66, 8, 0.25);
        --border-subtle: rgba(0, 0, 0, 0.06);
        --shadow-elevation: 0 10px 25px -5px rgba(92, 40, 5, 0.08);
    }

    [data-font="lora"] { --font-content: 'Lora', 'Times New Roman', serif; }
    [data-font="merriweather"] { --font-content: 'Merriweather', Georgia, serif; }
    [data-font="be-vietnam"] { --font-content: 'Be Vietnam Pro', 'Segoe UI', sans-serif; }

    html {
        scroll-behavior: smooth;
        scroll-snap-type: y proximity;
    }

    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }

    body {
        font-family: var(--font-content);
        background-color: var(--bg-body);
        color: var(--text-main);
        line-height: 1.8;
        transition: background-color 0.3s ease, color 0.3s ease;
        -webkit-font-smoothing: antialiased;
        overflow-x: hidden;
    }

    /* READING PROGRESS BAR */
    #progress-bar {
        position: fixed;
        top: 0;
        left: 0;
        height: 3.5px;
        background: linear-gradient(90deg, #d4af37, #38bdf8);
        width: 0%;
        z-index: 1000;
        transition: width 0.1s linear;
    }

    /* FLOATING TOP NAVBAR */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 60px;
        background: rgba(17, 22, 37, 0.85);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-bottom: 1px solid var(--border-subtle);
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 1.5rem;
        z-index: 999;
        transition: background 0.3s ease, border-color 0.3s ease;
    }

    [data-theme="light"] .navbar {
        background: rgba(255, 255, 255, 0.9);
    }

    [data-theme="sepia"] .navbar {
        background: rgba(250, 244, 232, 0.92);
    }

    .nav-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        text-decoration: none;
        color: var(--text-main);
    }

    .nav-logo-icon {
        color: var(--accent-gold);
    }

    .nav-title {
        font-family: 'Be Vietnam Pro', sans-serif;
        font-size: 1.1rem;
        font-weight: 800;
        letter-spacing: 0.5px;
        color: var(--accent-gold);
    }

    .nav-author {
        font-size: 0.82rem;
        color: var(--text-muted);
        border-left: 1px solid var(--border-subtle);
        padding-left: 0.75rem;
        margin-left: 0.25rem;
        display: none;
        font-weight: 600;
    }

    @media (min-width: 640px) {
        .nav-author { display: inline-block; }
    }

    .nav-controls {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .btn-icon {
        background: var(--bg-surface-elevated);
        border: 1px solid var(--border-subtle);
        color: var(--text-main);
        width: 38px;
        height: 38px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .btn-icon:hover {
        border-color: var(--accent-gold);
        color: var(--accent-gold);
        transform: translateY(-1px);
    }

    /* DRAWER / TABLE OF CONTENTS MODAL */
    .drawer-overlay {
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(4px);
        z-index: 1001;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s ease;
    }

    .drawer-overlay.active {
        opacity: 1;
        pointer-events: auto;
    }

    .drawer {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        width: 100%;
        max-width: 380px;
        background: var(--bg-surface);
        box-shadow: -10px 0 30px rgba(0,0,0,0.5);
        z-index: 1002;
        transform: translateX(100%);
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        display: flex;
        flex-direction: column;
    }

    .drawer.active {
        transform: translateX(0);
    }

    .drawer-header {
        padding: 1.25rem;
        border-bottom: 1px solid var(--border-subtle);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .drawer-title {
        font-family: 'Be Vietnam Pro', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--accent-gold);
    }

    .drawer-content {
        padding: 1rem 1.25rem;
        overflow-y: auto;
        flex-grow: 1;
    }

    .toc-group-title {
        font-size: 0.8rem;
        font-weight: 700;
        color: var(--accent-gold);
        text-transform: uppercase;
        margin-top: 1.25rem;
        margin-bottom: 0.5rem;
        border-bottom: 1px solid var(--border-subtle);
        padding-bottom: 0.25rem;
        font-family: 'Be Vietnam Pro', sans-serif;
    }

    .toc-item-link {
        display: block;
        padding: 0.45rem 0.5rem;
        color: var(--text-main);
        text-decoration: none;
        border-radius: 6px;
        font-size: 0.9rem;
        transition: all 0.2s;
    }

    .toc-item-link:hover {
        background: var(--bg-surface-elevated);
        color: var(--accent-gold);
        padding-left: 0.75rem;
    }

    /* SETTINGS IN DRAWER */
    .settings-panel {
        background: var(--bg-surface-elevated);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1.25rem;
        border: 1px solid var(--border-subtle);
    }

    .setting-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }

    .setting-row:last-child { margin-bottom: 0; }

    .setting-label { font-size: 0.85rem; color: var(--text-muted); }

    .segmented-control {
        display: flex;
        background: var(--bg-surface);
        padding: 2px;
        border-radius: 6px;
        border: 1px solid var(--border-subtle);
    }

    .seg-btn {
        border: none;
        background: transparent;
        color: var(--text-muted);
        font-size: 0.75rem;
        padding: 4px 8px;
        border-radius: 4px;
        cursor: pointer;
        font-family: inherit;
        transition: all 0.2s;
    }

    .seg-btn.active {
        background: var(--accent-gold);
        color: #000;
        font-weight: 700;
    }

    [data-theme="light"] .seg-btn.active {
        color: #fff;
    }

    /* HERO / LANDING PAGE: 100% Full Viewport Height */
    .hero {
        min-height: 100vh;
        min-height: 100dvh;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: calc(60px + 1.25rem) 1.5rem 1.5rem 1.5rem;
        background: radial-gradient(circle at 50% 30%, var(--bg-surface-elevated) 0%, var(--bg-body) 85%);
        border-bottom: 1px solid var(--border-subtle);
        position: relative;
        box-sizing: border-box;
        scroll-snap-align: start;
        scroll-snap-stop: always;
    }

    .hero-container {
        max-width: 1260px;
        width: 100%;
        margin: auto 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        gap: 2rem;
        z-index: 2;
    }

    @media (min-width: 768px) {
        .hero-container {
            flex-direction: row;
            text-align: left;
            align-items: center;
            justify-content: center;
            gap: 4rem;
        }
    }

    .hero-art {
        flex-shrink: 0;
        width: 100%;
        max-width: 380px;
        border-radius: 16px;
        overflow: hidden;
        border: 2px solid var(--border-color);
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6);
    }

    @media (min-width: 768px) {
        .hero-art {
            max-width: 480px;
        }
    }

    @media (min-width: 1024px) {
        .hero-art {
            max-width: 540px;
        }
    }

    .hero-img {
        width: 100%;
        height: auto;
        max-height: 72vh;
        object-fit: cover;
        display: block;
        transition: transform 0.5s ease;
    }

    .hero-img:hover {
        transform: scale(1.02);
    }

    .hero-info {
        flex-grow: 1;
        max-width: 600px;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.25rem 0.75rem;
        background: rgba(212, 175, 55, 0.12);
        border: 1px solid var(--border-color);
        border-radius: 9999px;
        color: var(--accent-gold);
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
        font-family: 'Be Vietnam Pro', sans-serif;
    }

    .hero-title {
        font-family: 'Be Vietnam Pro', 'Segoe UI', Arial, sans-serif;
        font-size: clamp(2rem, 3.8vw, 2.75rem);
        font-weight: 900;
        color: var(--accent-gold);
        line-height: 1.15;
        margin-bottom: 0.35rem;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        font-size: clamp(0.92rem, 1.8vw, 1.08rem);
        color: var(--text-muted);
        font-style: italic;
        margin-bottom: 0.75rem;
        font-family: 'Times New Roman', 'Lora', serif;
    }

    .hero-author-tag {
        font-size: 0.95rem;
        color: var(--text-main);
        margin-bottom: 0.75rem;
    }

    .hero-author-tag strong {
        color: var(--accent-gold);
        font-weight: 700;
    }

    .hero-tagline {
        font-size: clamp(0.85rem, 1.4vw, 0.95rem);
        font-style: italic;
        color: var(--text-muted);
        line-height: 1.55;
        border-left: 3px solid var(--border-color);
        padding-left: 0.9rem;
        margin-bottom: 1.25rem;
        font-family: 'Times New Roman', 'Lora', serif;
    }

    .hero-meta-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.75rem;
        margin-bottom: 1.25rem;
    }

    .meta-box {
        background: var(--bg-surface-elevated);
        border: 1px solid var(--border-subtle);
        border-radius: 8px;
        padding: 0.5rem 0.4rem;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .meta-num {
        font-size: 1.15rem;
        font-weight: 800;
        color: var(--accent-gold);
        font-family: 'Be Vietnam Pro', sans-serif;
    }

    .meta-lbl {
        font-size: 0.72rem;
        color: var(--text-muted);
        text-transform: uppercase;
        margin-top: 0.15rem;
        font-family: 'Be Vietnam Pro', sans-serif;
        font-weight: 600;
    }

    .hero-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        justify-content: center;
    }

    @media (min-width: 768px) {
        .hero-actions {
            justify-content: flex-start;
        }
    }

    .hero-scroll-indicator {
        margin-top: auto;
        padding: 0.65rem 1.4rem;
        background: rgba(212, 175, 55, 0.1);
        border: 1px solid var(--border-color);
        border-radius: 9999px;
        color: var(--accent-gold);
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 0.82rem;
        font-weight: 700;
        font-family: 'Be Vietnam Pro', sans-serif;
        box-shadow: 0 4px 15px rgba(0,0,0,0.25);
        transition: all 0.25s ease;
        animation: subtleFloat 2.6s infinite ease-in-out;
        z-index: 10;
    }

    .hero-scroll-indicator:hover {
        background: var(--accent-gold);
        color: #000;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.4);
    }

    @keyframes subtleFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-4px); }
    }

    .btn-primary {
        background: var(--accent-gold);
        color: #000;
        font-weight: 700;
        text-decoration: none;
        padding: 0.65rem 1.5rem;
        border-radius: 8px;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        font-family: 'Be Vietnam Pro', sans-serif;
        transition: all 0.2s;
    }

    .btn-primary:hover {
        opacity: 0.9;
        transform: translateY(-2px);
    }

    .btn-secondary {
        background: var(--bg-surface-elevated);
        color: var(--text-main);
        font-weight: 600;
        text-decoration: none;
        padding: 0.65rem 1.25rem;
        border-radius: 8px;
        border: 1px solid var(--border-color);
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        font-family: 'Be Vietnam Pro', sans-serif;
        transition: all 0.2s;
    }

    .btn-secondary:hover {
        border-color: var(--accent-gold);
        color: var(--accent-gold);
    }

    /* READING CONTAINER */
    .novel-wrapper {
        max-width: 760px;
        margin: 0 auto;
        padding: 2.5rem 1.25rem;
    }

    /* FULLSCREEN STANDALONE PAGES (100% Screen Height) */
    .fullscreen-page {
        min-height: 100vh;
        min-height: 100dvh;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: calc(60px + 1.5rem) 1.5rem 2rem 1.5rem;
        background: radial-gradient(circle at 50% 30%, var(--bg-surface-elevated) 0%, var(--bg-body) 90%);
        border-bottom: 1px solid var(--border-subtle);
        position: relative;
        box-sizing: border-box;
        scroll-snap-align: start;
        scroll-snap-stop: always;
    }

    .fullscreen-card {
        background: var(--bg-surface);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        max-width: 860px;
        width: 100%;
        margin: auto 0;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45);
        text-align: center;
        position: relative;
        z-index: 2;
    }

    @media (min-width: 768px) {
        .fullscreen-card {
            padding: 3.5rem 3rem;
        }
    }

    /* EPIGRAPH FULLSCREEN */
    .epigraph-fullscreen-quote {
        font-family: 'Lora', serif;
        font-style: italic;
        font-size: clamp(1.05rem, 2.2vw, 1.25rem);
        line-height: 1.75;
        color: var(--accent-gold);
        margin-bottom: 0.75rem;
    }

    .epigraph-fullscreen-author {
        font-family: 'Be Vietnam Pro', sans-serif;
        font-size: 0.82rem;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .epigraph-ornament {
        color: var(--accent-gold);
        font-size: 0.9rem;
        margin: 1.5rem 0;
        opacity: 0.75;
    }

    /* VOLUME HERO FULLSCREEN */
    .volume-fullscreen-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1.75rem;
        max-width: 1100px;
        width: 100%;
        margin: auto 0;
        text-align: center;
        z-index: 2;
    }

    @media (min-width: 768px) {
        .volume-fullscreen-container {
            flex-direction: row;
            text-align: left;
            align-items: center;
            justify-content: center;
            gap: 3.5rem;
        }
    }

    .volume-fullscreen-art {
        flex-shrink: 0;
        width: 100%;
        max-width: 320px;
        border-radius: 14px;
        overflow: hidden;
        border: 2px solid var(--border-color);
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.5);
    }

    @media (min-width: 768px) {
        .volume-fullscreen-art {
            max-width: 440px;
        }
    }

    .volume-fullscreen-img {
        width: 100%;
        height: auto;
        max-height: 55vh;
        object-fit: cover;
        display: block;
        transition: transform 0.5s ease;
    }

    .volume-fullscreen-img:hover {
        transform: scale(1.03);
    }

    .volume-fullscreen-info {
        flex-grow: 1;
        max-width: 560px;
    }

    .volume-fullscreen-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.25rem 0.75rem;
        background: rgba(212, 175, 55, 0.12);
        border: 1px solid var(--border-color);
        border-radius: 9999px;
        color: var(--accent-gold);
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 0.65rem;
        font-family: 'Be Vietnam Pro', sans-serif;
    }

    .volume-fullscreen-title {
        font-family: 'Be Vietnam Pro', 'Segoe UI', Arial, sans-serif;
        font-size: clamp(2rem, 3.5vw, 2.6rem);
        font-weight: 900;
        color: var(--text-main);
        line-height: 1.2;
        margin-bottom: 0.35rem;
    }

    .volume-fullscreen-subtitle {
        font-size: clamp(0.95rem, 1.8vw, 1.1rem);
        color: var(--text-muted);
        font-style: italic;
        margin-bottom: 1.25rem;
        font-family: 'Times New Roman', 'Lora', serif;
    }

    .volume-fullscreen-epigraph {
        font-style: italic;
        font-size: clamp(0.88rem, 1.5vw, 1rem);
        line-height: 1.65;
        color: var(--accent-gold);
        border-left: 3px solid var(--border-color);
        padding-left: 1rem;
        margin-bottom: 1.5rem;
        font-family: 'Times New Roman', 'Lora', serif;
        text-align: left;
    }

    /* APPENDIX FULLSCREEN */
    .appendix-fullscreen-card {
        background: var(--bg-surface);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 2.25rem 1.75rem;
        max-width: 960px;
        width: 100%;
        margin: auto 0;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45);
        z-index: 2;
    }

    @media (min-width: 768px) {
        .appendix-fullscreen-card {
            padding: 3rem 2.75rem;
        }
    }

    /* CHAPTER CARD */
    .chapter-card {
        background: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 2.5rem 1.5rem;
        margin-bottom: 2.5rem;
        box-shadow: var(--shadow-elevation);
        transition: border-color 0.2s;
    }

    @media (min-width: 640px) {
        .chapter-card {
            padding: 3.5rem 2.75rem;
        }
    }

    .chapter-card:hover {
        border-color: var(--border-color);
    }

    .chapter-header-wrap {
        text-align: center;
        margin-bottom: 2.5rem;
        border-bottom: 1px solid var(--border-subtle);
        padding-bottom: 1.5rem;
    }

    .chapter-num-tag {
        font-family: 'Be Vietnam Pro', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        color: var(--accent-gold);
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .chapter-main-heading {
        font-family: 'Be Vietnam Pro', 'Segoe UI', Arial, sans-serif;
        font-size: 1.85rem;
        font-weight: 800;
        color: var(--text-main);
        line-height: 1.25;
    }

    .chapter-content {
        font-size: var(--content-font-size);
        line-height: 1.85;
    }

    .chapter-content p {
        margin-bottom: 1.25rem;
        text-align: justify;
        text-justify: inter-word;
        text-indent: 1.5em;
    }

    .chapter-content > p:first-of-type::first-letter {
        font-family: 'Times New Roman', 'Georgia', serif;
        font-size: 3.2em;
        float: left;
        line-height: 0.8;
        margin-right: 0.12em;
        margin-top: 0.08em;
        color: var(--accent-gold);
        font-weight: 700;
    }

    .chapter-content hr {
        border: none;
        text-align: center;
        margin: 2rem 0;
    }

    .chapter-content hr::before {
        content: "❖   ❖   ❖";
        color: var(--accent-gold);
        font-size: 0.85rem;
    }

    .chapter-content blockquote {
        margin: 1.5rem 0 1.5rem 1rem;
        padding: 0.5rem 0 0.5rem 1.25rem;
        border-left: 3px solid var(--accent-gold);
        font-style: italic;
        color: var(--text-muted);
    }

    .chapter-content blockquote p,
    blockquote p {
        text-indent: 0 !important;
        text-align: left;
        line-height: 1.8;
    }

    .chapter-content p.dialogue {
        text-indent: 0 !important;
        padding-left: 0.75rem;
        margin-top: 0.4rem;
        margin-bottom: 0.95rem;
        font-weight: 500;
        line-height: 1.85;
    }

    .chapter-card,
    .fullscreen-page,
    #hero,
    #epigraph,
    #tap-1,
    #tap-2,
    #tap-3,
    #appendix-1,
    #appendix-2,
    #author-note {
        scroll-margin-top: 75px;
    }

    .chapter-footer-nav {
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        align-items: center;
        margin-top: 2.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--border-color);
        font-size: 0.85rem;
        font-family: 'Be Vietnam Pro', sans-serif;
        gap: 0.5rem;
    }

    .chapter-nav-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        text-decoration: none;
        color: var(--accent-gold);
        font-weight: 600;
        transition: opacity 0.2s, background-color 0.2s;
        padding: 0.45rem 0.75rem;
        border-radius: 6px;
    }

    .chapter-nav-btn:hover {
        opacity: 0.9;
        background: var(--bg-surface-elevated);
    }

    .chapter-nav-prev {
        justify-self: start;
        text-align: left;
    }

    .chapter-nav-center {
        justify-self: center;
        text-align: center;
        background: rgba(212, 175, 55, 0.08);
        border: 1px solid var(--border-subtle);
        color: var(--text-main);
    }

    .chapter-nav-center:hover {
        color: var(--accent-gold);
        border-color: var(--accent-gold);
    }

    .chapter-nav-next {
        justify-self: end;
        text-align: right;
    }

    @media (max-width: 640px) {
        .chapter-footer-nav {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }
        .chapter-nav-prev, .chapter-nav-center, .chapter-nav-next {
            width: 100%;
            justify-content: center;
            text-align: center;
            box-sizing: border-box;
        }
    }

    /* APPENDIX CARDS */
    .appendix-card {
        background: var(--bg-surface);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 2rem 1.5rem;
        margin-bottom: 2.5rem;
        box-shadow: var(--shadow-elevation);
    }

    @media (min-width: 640px) {
        .appendix-card { padding: 3rem 2.5rem; }
    }

    .appendix-heading {
        font-family: 'Be Vietnam Pro', sans-serif;
        font-size: 1.2rem;
        font-weight: 800;
        color: var(--accent-gold);
        text-transform: uppercase;
        margin-bottom: 1.25rem;
        text-align: center;
    }

    .clue-table-responsive {
        width: 100%;
        overflow-x: auto;
        margin-top: 1rem;
    }

    .web-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.88rem;
    }

    .web-table th, .web-table td {
        border: 1px solid var(--border-subtle);
        padding: 0.75rem 0.9rem;
        text-align: left;
    }

    .web-table th {
        background: var(--bg-surface-elevated);
        color: var(--accent-gold);
        font-family: 'Be Vietnam Pro', sans-serif;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
    }

    /* FOOTER */
    .site-footer {
        background: var(--bg-surface);
        border-top: 1px solid var(--border-subtle);
        text-align: center;
        padding: 3rem 1.5rem;
        color: var(--text-muted);
        font-size: 0.88rem;
    }

    .btn-back-top {
        position: fixed;
        bottom: 25px;
        right: 25px;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: var(--accent-gold);
        color: #000;
        border: none;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        opacity: 0;
        pointer-events: none;
        transition: all 0.3s ease;
        z-index: 998;
    }

    .btn-back-top.visible {
        opacity: 1;
        pointer-events: auto;
    }

    @media (max-width: 640px) {
        .hero, .fullscreen-page {
            padding: calc(60px + 1.25rem) 1rem 1.5rem 1rem;
            justify-content: flex-start;
        }
        .hero-container, .volume-fullscreen-container {
            gap: 1.25rem;
        }
        .hero-art {
            max-width: 310px;
        }
        .hero-img {
            max-height: 42vh;
        }
        .hero-title {
            font-size: 1.85rem;
            margin-bottom: 0.2rem;
        }
        .hero-subtitle {
            font-size: 0.88rem;
            margin-bottom: 0.35rem;
        }
        .hero-author-tag {
            font-size: 0.85rem;
            margin-bottom: 0.35rem;
        }
        .hero-tagline {
            font-size: 0.8rem;
            line-height: 1.45;
            margin-bottom: 0.75rem;
            padding-left: 0.65rem;
        }
        .hero-meta-grid {
            gap: 0.4rem;
            margin-bottom: 0.75rem;
        }
        .meta-box {
            padding: 0.35rem 0.2rem;
        }
        .meta-num {
            font-size: 0.95rem;
        }
        .meta-lbl {
            font-size: 0.62rem;
        }
        .btn-primary, .btn-secondary {
            padding: 0.5rem 1rem;
            font-size: 0.82rem;
        }
        
        .fullscreen-card, .appendix-fullscreen-card {
            padding: 1.75rem 1.25rem;
        }
        .volume-fullscreen-art {
            max-width: 280px;
        }
        .volume-fullscreen-img {
            max-height: 32vh;
        }
        .volume-fullscreen-title {
            font-size: 1.75rem;
        }
        .volume-fullscreen-subtitle {
            font-size: 0.9rem;
            margin-bottom: 0.85rem;
        }
        .volume-fullscreen-epigraph {
            font-size: 0.85rem;
            margin-bottom: 1.1rem;
        }
    }
"""

def clean_markdown_for_web(md_content):
    lines = md_content.strip().split('\n')
    title = ""
    if lines and lines[0].startswith('# '):
        title = lines[0].replace('# ', '').strip()
        lines = lines[1:]
    
    processed_text = '\n'.join(lines)
    html = markdown.markdown(processed_text, extensions=['extra', 'smarty'])
    html = re.sub(r'<p>—', r'<p class="dialogue">—', html)
    return title, html

def build_web_reader():
    print("Reading all 15 chapters for Web Reader...")
    chapter_files = sorted(glob.glob(os.path.join(CHAPTERS_DIR, '*.md')))
    
    chapters_data = {}
    for f in chapter_files:
        filename = os.path.basename(f)
        match = re.search(r'(\d+)', filename)
        if match:
            ch_num = int(match.group(1))
            with open(f, 'r', encoding='utf-8') as fp:
                content = fp.read()
            title, html = clean_markdown_for_web(content)
            
            parts = title.split("—")
            if len(parts) > 1:
                num_str = f"CHƯƠNG {parts[0].strip()}"
                name_str = parts[1].strip()
            else:
                num_str = f"CHƯƠNG {ch_num}"
                name_str = title

            chapters_data[ch_num] = {
                "num": ch_num,
                "title": title,
                "num_str": num_str,
                "name_str": name_str,
                "html": html
            }

    # Generate Drawer TOC Items Dynamically
    drawer_toc_html = '''
            <div class="toc-group-title">Phần Mở Đầu</div>
            <a href="#hero" class="toc-item-link">Trang bìa & Giới thiệu</a>
            <a href="#epigraph" class="toc-item-link">Lời đề từ & Đồng dao</a>
    '''
    for vol in VOLUMES:
        drawer_toc_html += f'<div class="toc-group-title">{vol["title"]}</div>'
        for ch_num in vol["chapters"]:
            if ch_num in chapters_data:
                ch = chapters_data[ch_num]
                drawer_toc_html += f'<a href="#chuong-{ch_num}" class="toc-item-link">{ch["num"]}. {ch["name_str"]}</a>\n'

    drawer_toc_html += '''
            <div class="toc-group-title">Phụ Lục & Hậu Từ</div>
            <a href="#appendix-1" class="toc-item-link">Phụ lục 1: Bài đồng dao Lũng Nậm</a>
            <a href="#appendix-2" class="toc-item-link">Phụ lục 2: Ma trận 6 Vật chứng</a>
            <a href="#author-note" class="toc-item-link">Lời bạt của Tác giả</a>
    '''

    full_html = f'''<!DOCTYPE html>
<html lang="vi" data-theme="dark" data-font="be-vietnam">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sáu Hòn Sỏi - Tiểu Thuyết Trinh Thám Hình Sự Điều Tra | Tác giả Hoàng Tùng</title>
    
    <!-- FONTS -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,600&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Merriweather:ital,wght@0,300;0,400;0,700;0,900;1,300;1,400&display=swap" rel="stylesheet">
    
    <!-- LUCIDE ICONS -->
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <style>
    {CSS_WEB}
    </style>
</head>
<body>

    <!-- READING PROGRESS BAR -->
    <div id="progress-bar"></div>

    <!-- NAVBAR -->
    <nav class="navbar">
        <a href="#hero" class="nav-brand">
            <i data-lucide="book-open" class="nav-logo-icon"></i>
            <span class="nav-title">SÁU HÒN SỎI</span>
            <span class="nav-author">Hoàng Tùng</span>
        </a>
        <div class="nav-controls">
            <button class="btn-icon" id="btn-theme" title="Đổi giao diện (Nền Tối / Nền Sáng / Giấy Cũ)">
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
                    <span class="setting-label">Kiểu chữ</span>
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
                        <button class="seg-btn" data-theme="sepia">Giấy cũ</button>
                    </div>
                </div>
            </div>

            {drawer_toc_html}
        </div>
    </aside>

    <!-- HERO SECTION -->
    <header class="hero" id="hero">
        <div class="hero-container">
            <div class="hero-art">
                <img src="assets/images/key_visual.jpg" alt="Tranh minh họa Sáu Hòn Sỏi" class="hero-img">
            </div>
            <div class="hero-info">
                <div class="hero-badge">
                    <i data-lucide="shield-alert" style="width: 14px; height: 14px;"></i>
                    Tiểu Thuyết Trinh Thám Hình Sự Điều Tra
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
                        <div class="meta-num">41K</div>
                        <div class="meta-lbl">Từ ngữ</div>
                    </div>
                    <div class="meta-box">
                        <div class="meta-num"><i data-lucide="scale" style="width: 22px; height: 22px; vertical-align: middle;"></i></div>
                        <div class="meta-lbl">Công Bằng Chứng Cứ</div>
                    </div>
                </div>

                <div class="hero-actions">
                    <a href="#chuong-1" class="btn-primary">
                        <i data-lucide="book-open"></i> Đọc Ngay
                    </a>
                    <a href="Sau_Hon_Soi_Master_Edition.pdf" target="_blank" class="btn-secondary">
                        <i data-lucide="download"></i> Tải Bản PDF
                    </a>
                </div>
            </div>
        </div>
        <a href="#epigraph" class="hero-scroll-indicator" title="Tiếp tục: Lời đề từ">
            <i data-lucide="book-open" style="width: 16px; height: 16px;"></i>
            <span>Tiếp tục: Khám phá tác phẩm</span>
            <i data-lucide="chevron-down" style="width: 16px; height: 16px;"></i>
        </a>
    </header>

    <!-- EPIGRAPH FULLSCREEN PAGE -->
    <section class="fullscreen-page" id="epigraph">
        <div class="fullscreen-card">
            <div class="hero-badge" style="margin-bottom: 1.5rem;">
                <i data-lucide="feather" style="width: 14px; height: 14px;"></i>
                LỜI ĐỀ TỪ & ĐỒNG DAO CỔ
            </div>
            
            <p class="epigraph-fullscreen-quote">
                “Cái cây gỗ trong rừng có cong queo thì mình đẽo cho thẳng được, chứ cái bụng người mình mà cong queo thì dựng cái nhà nào lên rồi cũng sập thôi con à.”
            </p>
            <p class="epigraph-fullscreen-author">
                — Lời dặn của người thợ mộc Trần Văn Cửu (1958 – 2005)
            </p>

            <div class="epigraph-ornament">❖   ❖   ❖</div>

            <p class="epigraph-fullscreen-quote" style="font-size: clamp(1rem, 2vw, 1.15rem);">
                “Một sỏi nhặt lá me rơi,<br>
                Hai sỏi gai nhọn cào phơi vách đèo.<br>
                Ba sỏi hạt đắng lưng đèo,<br>
                Bốn sỏi xương cá lạnh theo thác ngàn.<br>
                Năm sỏi bến nước đò tan,<br>
                Sáu sỏi thước mộc giải oan đất trời.”
            </p>
            <p class="epigraph-fullscreen-author">
                — Điệu đồng dao đếm sỏi dân gian Mường Biên
            </p>
        </div>
        <a href="#tap-1" class="hero-scroll-indicator" title="Tiếp tục: Bắt đầu Tập 1">
            <i data-lucide="compass" style="width: 16px; height: 16px;"></i>
            <span>Tiếp tục: Bắt đầu Tập 1 (Dưới Xuôi)</span>
            <i data-lucide="chevron-down" style="width: 16px; height: 16px;"></i>
        </a>
    </section>
'''

    for vol_idx, vol in enumerate(VOLUMES):
        first_ch = vol["chapters"][0]
        last_ch = vol["chapters"][-1]
        next_vol = VOLUMES[vol_idx + 1] if vol_idx + 1 < len(VOLUMES) else None
        
        author_quote_html = ""
        if "author_quote" in vol:
            author_quote_html = f'<div style="font-size: 0.8rem; margin-top: 0.4rem; color: var(--text-muted); font-family: sans-serif; font-weight: 600;">{vol["author_quote"]}</div>'
        
        full_html += f'''
        <!-- VOLUME FULLSCREEN PAGE: {vol["title"]} -->
        <section class="fullscreen-page" id="{vol["id"]}">
            <div class="volume-fullscreen-container">
                <div class="volume-fullscreen-art">
                    <img src="{vol["image"]}" alt="{vol["title"]}" class="volume-fullscreen-img">
                </div>
                <div class="volume-fullscreen-info">
                    <div class="volume-fullscreen-badge">
                        <i data-lucide="book" style="width: 14px; height: 14px;"></i>
                        Phần Sách · {vol["title"].split(":")[0]}
                    </div>
                    <h2 class="volume-fullscreen-title">{vol["title"]}</h2>
                    <div class="volume-fullscreen-subtitle">{vol["subtitle"]}</div>
                    
                    <div class="volume-fullscreen-epigraph">
                        {vol["epigraph"]}
                        {author_quote_html}
                    </div>

                    <div class="hero-actions">
                        <a href="#chuong-{first_ch}" class="btn-primary">
                            <i data-lucide="book-open"></i> Đọc Chương {first_ch}
                        </a>
                    </div>
                </div>
            </div>
            <a href="#chuong-{first_ch}" class="hero-scroll-indicator" title="Bắt đầu đọc các chương">
                <i data-lucide="play-circle" style="width: 16px; height: 16px;"></i>
                <span>Bắt đầu đọc {vol["title"].split(":")[0]} (Chương {first_ch})</span>
                <i data-lucide="chevron-down" style="width: 18px; height: 18px;"></i>
            </a>
        </section>

        <!-- CHAPTERS CONTAINER FOR {vol["title"]} -->
        <main class="novel-wrapper">
        '''

        for ch_num in vol["chapters"]:
            if ch_num in chapters_data:
                ch = chapters_data[ch_num]
                
                # Determine Previous Link & Label
                if ch_num == first_ch:
                    prev_href = f"#{vol['id']}"
                    prev_label = f"Trang trước ({vol['title'].split(':')[0]})"
                else:
                    prev_href = f"#chuong-{ch_num - 1}"
                    prev_label = f"Chương trước (Ch.{ch_num - 1})"
                
                # Determine Next Link & Label
                if ch_num == last_ch:
                    if next_vol:
                        next_href = f"#{next_vol['id']}"
                        next_label = f"Tập kế ({next_vol['title'].split(':')[0]})"
                    else:
                        next_href = "#appendix-1"
                        next_label = "Xem Phụ lục"
                else:
                    next_href = f"#chuong-{ch_num + 1}"
                    next_label = f"Chương kế (Ch.{ch_num + 1})"
                
                full_html += f'''
                <!-- CHAPTER {ch_num} -->
                <article class="chapter-card" id="chuong-{ch_num}">
                    <div class="chapter-header-wrap">
                        <div class="chapter-num-tag">{ch["num_str"]}</div>
                        <h3 class="chapter-main-heading">{ch["name_str"]}</h3>
                    </div>
                    <div class="chapter-content">
                        {ch["html"]}
                    </div>
                    <div class="chapter-footer-nav">
                        <a href="{prev_href}" class="chapter-nav-btn chapter-nav-prev">
                            <i data-lucide="chevron-left"></i> {prev_label}
                        </a>
                        <a href="#chuong-{ch_num}" class="chapter-nav-btn chapter-nav-center btn-chapter-top" data-target="chuong-{ch_num}" title="Cuộn lên đầu chương này">
                            <i data-lucide="arrow-up"></i> Về đầu chương
                        </a>
                        <a href="{next_href}" class="chapter-nav-btn chapter-nav-next">
                            {next_label} <i data-lucide="chevron-right"></i>
                        </a>
                    </div>
                </article>
                '''

        full_html += '''
        </main>
        '''

    # APPENDICES & AUTHOR NOTE FULLSCREEN PAGES
    full_html += '''
        <!-- PHỤ LỤC 1 FULLSCREEN PAGE -->
        <section class="fullscreen-page" id="appendix-1">
            <div class="appendix-fullscreen-card">
                <div style="text-align: center; margin-bottom: 1.25rem;">
                    <div class="hero-badge">
                        <i data-lucide="scroll" style="width: 14px; height: 14px;"></i>
                        TÀI LIỆU DÂN GIAN & KHẢO CỨU
                    </div>
                    <h3 class="appendix-heading" style="margin-bottom: 0;">PHỤ LỤC 1: BÀI ĐỒNG DAO ĐẾM SỎI LŨNG NẬM</h3>
                </div>
                <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1.25rem; text-align: justify; line-height: 1.6;">
                    Bài đồng dao đếm 6 nấc sỏi là trò chơi truyền miệng ngàn đời của trẻ con đồng bào bản Dền, thung lũng Lũng Nậm bên dòng suối Nậm. Dưới đây là văn bản nguyên tác đối chiếu bản dịch thơ tiếng phổ thông của Giáo sư Lê Đăng Khoa:
                </p>
                <div class="clue-table-responsive">
                    <table class="web-table">
                        <thead>
                            <tr>
                                <th style="width: 15%;">Nấc sỏi</th>
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
            </div>
            <a href="#appendix-2" class="hero-scroll-indicator" title="Xem tiếp Phụ lục 2">
                <i data-lucide="file-text" style="width: 16px; height: 16px;"></i>
                <span>Tiếp tục: Phụ lục 2 (Ma trận 6 Vật chứng)</span>
                <i data-lucide="chevron-down" style="width: 16px; height: 16px;"></i>
            </a>
        </section>

        <!-- PHỤ LỤC 2 FULLSCREEN PAGE -->
        <section class="fullscreen-page" id="appendix-2">
            <div class="appendix-fullscreen-card">
                <div style="text-align: center; margin-bottom: 1.25rem;">
                    <div class="hero-badge">
                        <i data-lucide="file-check-2" style="width: 14px; height: 14px;"></i>
                        HỒ SƠ TƯ PHÁP & KHOA HỌC PHÁP Y
                    </div>
                    <h3 class="appendix-heading" style="margin-bottom: 0;">PHỤ LỤC 2: MA TRẬN 6 VẬT CHỨNG & PHÁP CHỨNG</h3>
                </div>
                <div class="clue-table-responsive">
                    <table class="web-table">
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
            </div>
            <a href="#author-note" class="hero-scroll-indicator" title="Xem tiếp Lời bạt của Tác giả">
                <i data-lucide="pen-tool" style="width: 16px; height: 16px;"></i>
                <span>Tiếp tục: Lời bạt của Tác giả</span>
                <i data-lucide="chevron-down" style="width: 18px; height: 18px;"></i>
            </a>
        </section>

        <!-- LỜI BẠT FULLSCREEN PAGE -->
        <section class="fullscreen-page" id="author-note">
            <div class="fullscreen-card" style="text-align: left;">
                <div style="text-align: center; margin-bottom: 1.5rem;">
                    <div class="hero-badge">
                        <i data-lucide="pen-tool" style="width: 14px; height: 14px;"></i>
                        HẬU TỪ TÁC PHẨM
                    </div>
                    <h3 class="appendix-heading" style="margin-bottom: 0;">LỜI BẠT CỦA TÁC GIẢ HOÀNG TÙNG</h3>
                </div>
                <p style="text-align: justify; text-indent: 1.5em; line-height: 1.8; font-size: 1rem; margin-bottom: 1.25rem; font-family: 'Lora', serif;">
                    <em>Sáu Hòn Sỏi</em> được khởi thảo từ khát khao khắc họa một tác phẩm trinh thám hình sự mang đậm linh hồn và bản sắc hiện thực Việt Nam. Nơi đó, cuộc đấu tranh bảo vệ công lý không chỉ diễn ra giữa các thiết bị đo quang phổ XRF sắc lạnh hay những quy chuẩn tố tụng tư pháp khắt khe, mà trước hết là cuộc đấu tranh thầm lặng trong tâm khảm của mỗi con người trước lằn ranh tha hóa của quyền lực.
                </p>
                <p style="text-align: justify; text-indent: 1.5em; line-height: 1.8; font-size: 1rem; font-family: 'Lora', serif;">
                    Hình ảnh chiếc thước mộc bằng gỗ lim của người thợ mộc Trần Văn Cửu — với những vết khắc mòn vẹt sau mười chín năm oan khuất — chính là chiếc neo đạo đức bất biến. Dù giông bão thời cuộc hay sự toan tính cá nhân có bẻ cong những phán quyết tạm thời, thì sự ngay thẳng và phẩm giá của người lao động lương thiện vẫn luôn tìm được con đường trở về với ánh sáng.
                </p>
                <p style="text-align: right; font-style: italic; margin-top: 2rem; font-size: 0.95rem; color: var(--accent-gold); font-family: 'Be Vietnam Pro', sans-serif; font-weight: 600;">
                    <strong>Tác giả: Hoàng Tùng</strong><br>
                    <span style="font-size: 0.85rem; color: var(--text-muted); font-weight: normal;">Hạ An – Mường Biên – Mùa thu 2026</span>
                </p>
            </div>
            <a href="#hero" class="hero-scroll-indicator" style="margin-top: 1.5rem;" title="Về Trang bìa tác phẩm">
                <i data-lucide="arrow-up" style="width: 16px; height: 16px;"></i>
                <span>Về Trang bìa tác phẩm</span>
            </a>
        </section>

    <!-- BACK TO TOP BUTTON -->
    <button class="btn-back-top" id="btn-back-top" title="Lên đầu trang">
        <i data-lucide="arrow-up"></i>
    </button>

    <!-- FOOTER -->
    <footer class="site-footer">
        <div style="font-family: 'Be Vietnam Pro', sans-serif; font-size: 1.1rem; font-weight: 800; color: var(--accent-gold); margin-bottom: 0.5rem; text-transform: uppercase;">
            SÁU HÒN SỎI
        </div>
        <p>Tiểu thuyết Trinh thám Hình sự Điều tra • Tác giả: Hoàng Tùng</p>
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

            // Back to Top Visibility
            const backTop = document.getElementById('btn-back-top');
            if (winScroll > 400) {
                backTop.classList.add('visible');
            } else {
                backTop.classList.remove('visible');
            }
        });

        document.getElementById('btn-back-top').addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        // Top of Chapter Navigation Logic
        document.querySelectorAll('.btn-chapter-top').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = btn.getAttribute('data-target');
                const targetEl = document.getElementById(targetId);
                if (targetEl) {
                    const navHeight = 70;
                    const topPos = targetEl.getBoundingClientRect().top + window.pageYOffset - navHeight;
                    window.scrollTo({ top: topPos, behavior: 'smooth' });
                }
            });
        });

        // Drawer Control
        const drawer = document.getElementById('drawer');
        const overlay = document.getElementById('drawer-overlay');
        const btnToc = document.getElementById('btn-toc');
        const btnCloseDrawer = document.getElementById('btn-close-drawer');

        function toggleDrawer() {
            drawer.classList.toggle('active');
            overlay.classList.toggle('active');
        }

        btnToc.addEventListener('click', toggleDrawer);
        btnCloseDrawer.addEventListener('click', toggleDrawer);
        overlay.addEventListener('click', toggleDrawer);

        document.querySelectorAll('.toc-item-link').forEach(link => {
            link.addEventListener('click', () => {
                drawer.classList.remove('active');
                overlay.classList.remove('active');
            });
        });

        // Theme Toggle (Dark / Light / Sepia)
        const themeBtns = document.querySelectorAll('#theme-selector .seg-btn');
        const btnThemeNav = document.getElementById('btn-theme');
        const themes = ['dark', 'light', 'sepia'];
        
        function setTheme(t) {
            const iconEl = document.getElementById('theme-icon');
            if (t === 'dark') {
                iconEl.setAttribute('data-lucide', 'moon');
            } else if (t === 'light') {
                iconEl.setAttribute('data-lucide', 'sun');
            } else {
                iconEl.setAttribute('data-lucide', 'book-marked');
            }
            lucide.createIcons();

            document.documentElement.setAttribute('data-theme', t);
            themeBtns.forEach(btn => {
                btn.classList.toggle('active', btn.getAttribute('data-theme') === t);
            });
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

        // Restore Preferences
        const savedTheme = localStorage.getItem('novel_theme');
        if (savedTheme) setTheme(savedTheme);
        const savedFont = localStorage.getItem('novel_font');
        if (savedFont) setFont(savedFont);
    </script>
</body>
</html>
'''

    print(f"Writing web reader to {OUTPUT_WEB}...")
    with open(OUTPUT_WEB, 'w', encoding='utf-8') as fp:
        fp.write(full_html)
    print(f"Web version successfully regenerated at {OUTPUT_WEB} (Size: {os.path.getsize(OUTPUT_WEB):,} bytes)")

if __name__ == '__main__':
    build_web_reader()
