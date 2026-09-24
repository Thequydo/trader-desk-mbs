# -*- coding: utf-8 -*-
"""
Revert to f9a11e3 (Sector Grouped KwangTae / SVCC Terminal) + PHỦ KÍN ẢNH MU 2 BÊN HÔNG
"""
import re

with open('f9a11e3_source.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Title and Add MU Theme accents
html = html.replace(
    "<title>Sinh Viên Chơi Chứng | Quản Lý Tài Khoản & Giao Dịch Chứng Khoán</title>",
    "<title>KwangTae Quant Terminal | Manchester United Fan Edition • Phân Nhóm Ngành</title>"
)

# 2. Add full-coverage side flanks CSS to <style>
side_flank_css = r'''
    /* PHỦ KÍN ẢNH MANCHESTER UNITED Ở 2 BÊN HÔNG (FULL-HEIGHT WALLPAPER WINGS) */
    @media (min-width: 1180px) {
      body {
        position: relative;
        overflow-x: hidden;
      }

      .mu-full-flank-left {
        position: fixed;
        top: 0;
        bottom: 0;
        left: 0;
        width: calc((100vw - 1120px) / 2);
        max-width: 420px;
        min-width: 160px;
        background-image: 
          linear-gradient(to right, rgba(7, 9, 18, 0.25) 0%, rgba(7, 9, 18, 0.7) 70%, rgba(7, 9, 18, 0.98) 100%),
          url('/images/mu_players.jpg');
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        border-right: 1.5px solid rgba(218, 2, 14, 0.45);
        box-shadow: inset -30px 0 50px rgba(7, 9, 18, 0.85), 0 0 35px rgba(218, 2, 14, 0.25);
        z-index: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 28px 18px;
        pointer-events: none;
      }

      .mu-full-flank-right {
        position: fixed;
        top: 0;
        bottom: 0;
        right: 0;
        width: calc((100vw - 1120px) / 2);
        max-width: 420px;
        min-width: 160px;
        background-image: 
          linear-gradient(to left, rgba(7, 9, 18, 0.25) 0%, rgba(7, 9, 18, 0.7) 70%, rgba(7, 9, 18, 0.98) 100%),
          url('/images/mu_old_trafford.jpg');
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        border-left: 1.5px solid rgba(218, 2, 14, 0.45);
        box-shadow: inset 30px 0 50px rgba(7, 9, 18, 0.85), 0 0 35px rgba(218, 2, 14, 0.25);
        z-index: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 28px 18px;
        pointer-events: none;
      }
    }

    @media (max-width: 1179px) {
      .mu-full-flank-left, .mu-full-flank-right {
        display: none !important;
      }
    }

    .mu-flank-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(10, 14, 26, 0.85);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(218, 2, 14, 0.45);
      border-radius: 12px;
      padding: 8px 12px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
      width: fit-content;
    }
    .mu-flank-crest-icon {
      width: 28px;
      height: 28px;
      filter: drop-shadow(0 0 8px rgba(218, 2, 14, 0.7));
    }
    .mu-flank-txt-title {
      font-size: 11.5px;
      font-weight: 900;
      color: #fff;
      letter-spacing: 0.5px;
      line-height: 1.2;
    }
    .mu-flank-txt-sub {
      font-size: 9px;
      color: #fbe122;
      font-weight: 800;
    }

    .mu-flank-center-tag {
      background: rgba(10, 14, 26, 0.85);
      backdrop-filter: blur(6px);
      border: 1px solid rgba(251, 225, 34, 0.35);
      border-radius: 12px;
      padding: 12px;
      color: #f8fafc;
      font-size: 11px;
      line-height: 1.5;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.7);
    }
    .mu-flank-center-tag strong {
      color: #fbe122;
    }

    .mu-flank-bottom-badge {
      background: rgba(10, 14, 26, 0.85);
      backdrop-filter: blur(6px);
      border: 1px solid rgba(218, 2, 14, 0.35);
      border-radius: 10px;
      padding: 8px 12px;
      font-size: 10px;
      color: #94a3b8;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .container {
      position: relative;
      z-index: 10;
    }
'''

html = html.replace("</style>", side_flank_css + "\n  </style>")

# 3. Add the two full-height side flanks directly inside <body>
flanks_html = r'''
  <!-- PHỦ KÍN ẢNH MU BÊN HÔNG TRÁI: MANCHESTER UNITED PLAYERS & UNITED TILL I DIE -->
  <div class="mu-full-flank-left">
    <div class="mu-flank-badge">
      <img src="/images/mu_crest.svg" alt="MU" class="mu-flank-crest-icon">
      <div>
        <div class="mu-flank-txt-title">RED DEVILS 🔱</div>
        <div class="mu-flank-txt-sub">MAN UTD VIP DESK</div>
      </div>
    </div>

    <div class="mu-flank-center-tag">
      <div style="font-size:12px; font-weight:900; color:#da020e; margin-bottom:4px; letter-spacing:0.5px;">UNITED TILL I DIE 🔱</div>
      "From the ashes of Munich to the summit of Europe — United never surrender."
    </div>

    <div class="mu-flank-bottom-badge">
      <span>VIP Red Devil:</span>
      <strong style="color:#fbe122; font-family:var(--font-mono);">Thế Quang 🔱</strong>
    </div>
  </div>

  <!-- PHỦ KÍN ẢNH MU BÊN HÔNG PHẢI: OLD TRAFFORD THEATRE OF DREAMS -->
  <div class="mu-full-flank-right">
    <div class="mu-flank-badge">
      <img src="/images/mu_crest.svg" alt="MU" class="mu-flank-crest-icon">
      <div>
        <div class="mu-flank-txt-title">OLD TRAFFORD 🏟️</div>
        <div class="mu-flank-txt-sub">THEATRE OF DREAMS</div>
      </div>
    </div>

    <div class="mu-flank-center-tag">
      <div style="font-size:12px; font-weight:900; color:#fbe122; margin-bottom:4px; letter-spacing:0.5px;">MORE THAN A CLUB 🔱</div>
      "It's not just a club, it's a way of life."
      <div style="text-align:right; font-size:9.5px; color:#da020e; font-weight:800; margin-top:3px;">— Sir Matt Busby</div>
    </div>

    <div class="mu-flank-bottom-badge">
      <span>Kỷ luật đầu tư:</span>
      <strong style="color:#10b981; font-family:var(--font-mono);">100% Tuân Thủ</strong>
    </div>
  </div>
'''

html = html.replace('<body>', '<body>\n' + flanks_html)

# 4. Update Header with MU Crest & Red Devil accent
html = html.replace(
    '<div class="brand-logo-icon">SVCC</div>',
    '<div class="brand-logo-icon" style="background:rgba(218,2,14,0.18); border:1.5px solid rgba(218,2,14,0.5); padding:4px; box-shadow:0 0 16px rgba(218,2,14,0.5);"><img src="/images/mu_crest.svg" alt="MU" style="width:36px; height:36px; filter:drop-shadow(0 0 6px rgba(218,2,14,0.6));"></div>'
)
html = html.replace(
    '<div class="brand-title">SINH VIÊN CHƠI CHỨNG • TRADING TERMINAL</div>',
    '<div class="brand-title">KWANGTAE QUANT TERMINAL • MAN UTD EDITION <span style="color:#fbe122;">🔱</span></div>'
)

# 5. Add footer glory message
html = html.replace(
    'Tài khoản: Ngô Quang Thế (2512T51) • Đồng bộ hóa trực tuyến 24/7 trên Vercel Cloud Serverless',
    'Tài khoản: Ngô Quang Thế (2512T51) • Đồng bộ hóa trực tuyến 24/7 trên Vercel Cloud Serverless<br><span style="color:#da020e; font-weight:800;">United Till I Die 🔱 • Glory Glory Man United!</span>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('scripts/build_mu_terminal.py', 'w', encoding='utf-8') as f:
    f.write(f'# -*- coding: utf-8 -*-\nHTML = r"""{html}"""\nwith open("index.html", "w", encoding="utf-8") as f: f.write(HTML)\nwith open("public/index.html", "w", encoding="utf-8") as f: f.write(HTML)\n')

print("Successfully restored sector grouped version with FULL MU COVERAGE on both flanks!")
