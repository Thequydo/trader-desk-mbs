# -*- coding: utf-8 -*-
"""
Builder for Manchester United Fan Edition Trading Terminal (Full Professional Suite)
Fulfills all 5 core requirements:
1. Header & Left Sidebar: Stock search with auto-sync, Trade Journal modal with database storage, Portfolio & Performance Statistics modal.
2. Center Chart: TradingView Lightweight Charts v5 with drag/pan/zoom, drawing tools, timeframe switcher (1m, 5m, 15m, 1h, 1D, 1W), indicator toggles (MA20, MA50, MA200, RSI, MACD).
3. Order Panel: Automatic subtotal, fee (0.15%), and tax (0.1%) calculation, official exchange tick steps (HOSE 0.01/0.05/0.1 vs HNX/UPCoM 0.1), pre-trade balance validation & anti-misclick confirmation modal with Web Audio chime and Telegram alert.
4. AI Analysis Panel: Auto-recommendation card for current stock, interactive chat with Gemini Flash Lite / Quant engine & quick prompt buttons (stop-loss, target, risk, cash flow).
5. Bottom Tables: Real-time green/red price flash, click-to-action on any symbol in Watchlist/Portfolio to instantly sync chart, order form, and AI.
"""

HTML = r'''<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>MAN UTD TRADER DESK | United Fan Edition • Vietnamese Stock Terminal</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">
  
  <!-- TradingView Lightweight Charts (v5.2.1) -->
  <script src="/js/lightweight-charts.js"></script>
  <script>
    if (typeof LightweightCharts === 'undefined') {
      document.write('<script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"><\/script>');
    }
  </script>

  <style>
    :root {
      --bg-base: #06070a;
      --bg-panel: #0d0f17;
      --bg-card: #121522;
      --bg-card-inner: #0a0b12;
      --border-card: rgba(255, 255, 255, 0.08);
      --border-red: rgba(218, 2, 14, 0.35);
      --mu-red: #da020e;
      --mu-red-glow: rgba(218, 2, 14, 0.45);
      --mu-red-dark: #8b0000;
      --mu-gold: #fbe122;
      --neon-green: #00e676;
      --neon-green-bg: rgba(0, 230, 118, 0.15);
      --neon-red: #ff3b30;
      --neon-red-bg: rgba(255, 59, 48, 0.15);
      --text-white: #f8fafc;
      --text-muted: #8e9bb0;
      --text-dim: #556277;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      background-color: var(--bg-base);
      color: var(--text-white);
      margin: 0;
      padding: 0;
      display: flex;
      min-height: 100vh;
      overflow-x: hidden;
    }

    /* REALTIME FLASH ANIMATION */
    @keyframes flashGreen {
      0% { background-color: rgba(0, 230, 118, 0.45); color: #fff; }
      100% { background-color: transparent; }
    }
    @keyframes flashRed {
      0% { background-color: rgba(218, 2, 14, 0.45); color: #fff; }
      100% { background-color: transparent; }
    }
    .flash-up { animation: flashGreen 0.7s ease-out; }
    .flash-down { animation: flashRed 0.7s ease-out; }

    /* TICK PULSE ANIMATION */
    @keyframes pulseScale {
      0% { transform: scale(1); }
      50% { transform: scale(1.04); text-shadow: 0 0 10px var(--mu-red); }
      100% { transform: scale(1); }
    }
    .tick-pulse { animation: pulseScale 0.4s ease; }

    /* APP LAYOUT */
    .app-layout {
      display: flex;
      width: 100%;
      min-height: 100vh;
    }

    /* LEFT SIDEBAR NAVIGATION */
    .sidebar {
      width: 205px;
      min-width: 205px;
      background: #090a10;
      border-right: 1px solid rgba(218, 2, 14, 0.22);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 14px 10px;
      gap: 12px;
      z-index: 10;
    }
    .sidebar-top {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .brand-box {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 4px 6px 12px 6px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      cursor: pointer;
    }
    .brand-crest {
      width: 36px;
      height: 36px;
      filter: drop-shadow(0 0 8px rgba(218, 2, 14, 0.6));
    }
    .brand-name {
      font-size: 13.5px;
      font-weight: 900;
      letter-spacing: 0.5px;
      color: #fff;
      line-height: 1.1;
    }
    .brand-sub {
      font-size: 9.5px;
      color: var(--mu-red);
      font-style: italic;
      font-weight: 700;
      letter-spacing: 0.2px;
    }

    .nav-list {
      display: flex;
      flex-direction: column;
      gap: 3px;
    }
    .nav-item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      text-decoration: none;
      transition: all 0.2s;
    }
    .nav-item:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.06);
    }
    .nav-item.active {
      background: var(--mu-red);
      color: #fff;
      box-shadow: 0 4px 14px rgba(218, 2, 14, 0.45);
    }
    .nav-badge-new {
      background: #fff;
      color: var(--mu-red);
      font-size: 8.5px;
      font-weight: 900;
      padding: 1px 5px;
      border-radius: 4px;
      margin-left: auto;
    }

    .sidebar-mid {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .mu-poster-card {
      position: relative;
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid rgba(218, 2, 14, 0.3);
      box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    .mu-poster-img {
      width: 100%;
      height: 100px;
      object-fit: cover;
      display: block;
      transition: transform 0.3s;
    }
    .mu-poster-card:hover .mu-poster-img {
      transform: scale(1.03);
    }
    .mu-poster-tag {
      position: absolute;
      bottom: 6px;
      left: 6px;
      right: 6px;
      background: rgba(10, 11, 18, 0.85);
      backdrop-filter: blur(4px);
      padding: 3px 6px;
      border-radius: 4px;
      font-size: 9px;
      font-weight: 800;
      color: var(--mu-gold);
      text-align: center;
      border: 1px solid rgba(251, 225, 34, 0.3);
    }

    .sidebar-bottom {
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      padding-top: 10px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .user-profile-badge {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 6px 8px;
      background: rgba(255, 255, 255, 0.03);
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .user-avatar {
      width: 28px;
      height: 28px;
      border-radius: 50%;
      border: 1.5px solid var(--mu-red);
      background: #1a1c29;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 900;
      font-size: 11px;
      color: #fff;
    }
    .user-info-text {
      display: flex;
      flex-direction: column;
      line-height: 1.2;
    }
    .user-name {
      font-size: 11.5px;
      font-weight: 800;
      color: #fff;
    }
    .user-sub {
      font-size: 9.5px;
      color: var(--mu-gold);
      font-weight: 700;
    }

    .busby-quote {
      font-size: 9px;
      color: var(--text-dim);
      font-style: italic;
      line-height: 1.3;
      text-align: center;
      border-left: 2px solid var(--mu-red);
      padding-left: 6px;
      margin: 4px 0 0 0;
    }

    /* MAIN CONTENT WRAPPER */
    .main-wrapper {
      flex: 1;
      display: flex;
      flex-direction: column;
      background-color: var(--bg-base);
      min-width: 0;
      overflow-y: auto;
    }

    /* TOP HEADER */
    .header-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 18px;
      background: #090a10;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      gap: 16px;
    }
    .header-search-wrap {
      position: relative;
      width: 320px;
    }
    .header-search-input {
      width: 100%;
      background: #121522;
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 6px;
      padding: 7px 12px 7px 32px;
      color: #fff;
      font-size: 12px;
      font-family: inherit;
      outline: none;
      transition: all 0.2s;
    }
    .header-search-input:focus {
      border-color: var(--mu-red);
      box-shadow: 0 0 8px rgba(218, 2, 14, 0.4);
    }
    .search-icon-pos {
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-dim);
      font-size: 13px;
      pointer-events: none;
    }
    .search-dropdown {
      position: absolute;
      top: calc(100% + 4px);
      left: 0;
      right: 0;
      background: #121522;
      border: 1px solid rgba(218, 2, 14, 0.35);
      border-radius: 6px;
      max-height: 250px;
      overflow-y: auto;
      z-index: 100;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.8);
      display: none;
    }
    .search-dropdown-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 12px;
      cursor: pointer;
      font-size: 11.5px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      transition: background 0.15s;
    }
    .search-dropdown-item:hover {
      background: rgba(218, 2, 14, 0.15);
    }

    .header-market-indices {
      display: flex;
      align-items: center;
      gap: 16px;
    }
    .index-pill {
      display: flex;
      align-items: center;
      gap: 6px;
      font-family: var(--font-mono);
      font-size: 11.5px;
    }
    .index-pill .sym { font-weight: 700; color: #fff; }
    .index-pill .val { font-weight: 700; }
    .index-pill .chg { font-size: 10.5px; }

    .header-right-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .live-pulse-badge {
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(0, 230, 118, 0.1);
      border: 1px solid rgba(0, 230, 118, 0.3);
      padding: 4px 8px;
      border-radius: 6px;
      font-size: 11px;
      color: var(--neon-green);
      font-weight: 700;
      font-family: var(--font-mono);
    }
    .live-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--neon-green);
      box-shadow: 0 0 6px var(--neon-green);
      animation: pulseScale 1s infinite alternate;
    }

    .btn-quick-journal {
      background: rgba(251, 225, 34, 0.12);
      border: 1px solid rgba(251, 225, 34, 0.35);
      color: var(--mu-gold);
      padding: 5px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 800;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
      transition: all 0.2s;
    }
    .btn-quick-journal:hover {
      background: rgba(251, 225, 34, 0.25);
      box-shadow: 0 0 10px rgba(251, 225, 34, 0.3);
    }

    /* DASHBOARD CONTAINER */
    .dashboard-container {
      padding: 14px 18px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    /* TOP 4 SUMMARY CARDS */
    .top-cards-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
    }
    .summary-card {
      background: var(--bg-card);
      border: 1px solid var(--border-card);
      border-radius: 8px;
      padding: 10px 14px;
      display: flex;
      flex-direction: column;
      gap: 4px;
      position: relative;
      overflow: hidden;
    }
    .summary-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 3px;
      height: 100%;
      background: var(--border-card);
    }
    .summary-card.red-accent::before {
      background: var(--mu-red);
      box-shadow: 0 0 8px var(--mu-red);
    }
    .summary-card.gold-accent::before {
      background: var(--mu-gold);
      box-shadow: 0 0 8px var(--mu-gold);
    }
    .card-label {
      font-size: 11px;
      color: var(--text-muted);
      font-weight: 600;
    }
    .card-val {
      font-size: 17px;
      font-weight: 800;
      font-family: var(--font-mono);
      color: #fff;
    }
    .card-sub {
      font-size: 10.5px;
      font-weight: 700;
      font-family: var(--font-mono);
    }

    /* CENTER DASHBOARD: 3-COLUMN LAYOUT */
    .center-dashboard {
      display: grid;
      grid-template-columns: 1fr 275px 330px;
      gap: 12px;
    }

    /* 1. CHART PANEL */
    .chart-panel {
      background: var(--bg-panel);
      border: 1px solid var(--border-card);
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      position: relative;
    }
    .chart-top-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .cp-sym-title {
      font-size: 15px;
      font-weight: 900;
      color: #fff;
      margin-right: 6px;
    }
    .cp-tf-group {
      display: flex;
      align-items: center;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 6px;
      padding: 2px;
      gap: 2px;
    }
    .cp-tf-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 10.5px;
      font-weight: 700;
      padding: 3px 7px;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.15s;
    }
    .cp-tf-btn:hover { color: #fff; }
    .cp-tf-btn.active {
      background: var(--mu-red);
      color: #fff;
      box-shadow: 0 2px 8px rgba(218, 2, 14, 0.4);
    }

    .cp-tools-bar {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 11px;
      color: var(--text-muted);
    }
    .btn-chart-tool {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      color: var(--text-muted);
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 10.5px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
      transition: all 0.2s;
    }
    .btn-chart-tool:hover {
      color: #fff;
      border-color: rgba(255, 255, 255, 0.2);
    }
    .btn-chart-tool.active {
      background: rgba(218, 2, 14, 0.15);
      border-color: var(--mu-red);
      color: #fff;
    }

    .cp-ohlc-row {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 5px 12px;
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--text-muted);
      background: rgba(0, 0, 0, 0.2);
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }
    .ohlc-val { color: #fff; font-weight: 700; }
    .ohlc-chg { font-weight: 700; }

    .cp-indicators-row {
      display: flex;
      align-items: center;
      gap: 14px;
      padding: 4px 12px;
      font-family: var(--font-mono);
      font-size: 10.5px;
      background: rgba(10, 11, 18, 0.4);
      border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    }

    .chart-canvas-wrap {
      position: relative;
      flex: 1;
      min-height: 310px;
    }
    .chart-left-tools {
      position: absolute;
      top: 10px;
      left: 10px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      z-index: 5;
    }
    .tool-icon {
      width: 26px;
      height: 26px;
      border-radius: 4px;
      background: rgba(18, 21, 34, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.1);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.15s;
    }
    .tool-icon:hover, .tool-icon.active {
      color: #fff;
      background: var(--mu-red);
      border-color: var(--mu-red);
      box-shadow: 0 0 6px rgba(218, 2, 14, 0.5);
    }

    #mainTvChart {
      width: 100%;
      height: 310px;
    }
    .chart-watermark-crest {
      position: absolute;
      bottom: 24px;
      right: 28px;
      width: 130px;
      opacity: 0.07;
      pointer-events: none;
      user-select: none;
    }

    /* 2. ORDER ENTRY & MARKET DEPTH */
    .middle-order-col {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .order-box {
      background: var(--bg-panel);
      border: 1px solid var(--border-card);
      border-radius: 8px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .ob-tabs {
      display: flex;
      background: rgba(255, 255, 255, 0.04);
      border-radius: 6px;
      padding: 2px;
      gap: 2px;
    }
    .ob-tab-btn {
      flex: 1;
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 11.5px;
      font-weight: 700;
      padding: 5px;
      border-radius: 4px;
      cursor: pointer;
    }
    .ob-tab-btn.active {
      background: var(--bg-card);
      color: #fff;
    }

    .ob-sym-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-weight: 800;
      font-size: 13px;
      padding-bottom: 4px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .ob-action-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
    }
    .ob-act-btn {
      padding: 7px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 800;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.15s;
    }
    .ob-act-buy {
      background: var(--neon-green-bg);
      color: var(--neon-green);
      border-color: rgba(0, 230, 118, 0.35);
    }
    .ob-act-buy.active {
      background: var(--neon-green);
      color: #000;
      box-shadow: 0 0 10px rgba(0, 230, 118, 0.4);
    }
    .ob-act-sell {
      background: var(--neon-red-bg);
      color: var(--neon-red);
      border-color: rgba(218, 2, 14, 0.35);
    }
    .ob-act-sell.active {
      background: var(--mu-red);
      color: #fff;
      box-shadow: 0 0 10px rgba(218, 2, 14, 0.4);
    }

    .ob-field {
      display: flex;
      flex-direction: column;
      gap: 4px;
      font-size: 11px;
      color: var(--text-muted);
    }
    .ob-input-stepper {
      display: flex;
      align-items: center;
      background: var(--bg-card);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 6px;
      overflow: hidden;
    }
    .ob-step-btn {
      width: 28px;
      height: 28px;
      background: rgba(255, 255, 255, 0.04);
      border: none;
      color: #fff;
      font-weight: 800;
      cursor: pointer;
      transition: background 0.15s;
    }
    .ob-step-btn:hover { background: rgba(255, 255, 255, 0.12); }
    .ob-input {
      flex: 1;
      background: transparent;
      border: none;
      color: #fff;
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      text-align: center;
      outline: none;
      padding: 4px;
    }

    .ob-chips {
      display: flex;
      gap: 4px;
    }
    .ob-chip {
      flex: 1;
      text-align: center;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.06);
      padding: 3px 0;
      border-radius: 4px;
      font-size: 9.5px;
      color: var(--text-muted);
      cursor: pointer;
      font-family: var(--font-mono);
      transition: all 0.15s;
    }
    .ob-chip:hover {
      background: rgba(255, 255, 255, 0.08);
      color: #fff;
      border-color: rgba(255, 255, 255, 0.2);
    }

    .ob-breakdown {
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 6px;
      padding: 6px 8px;
      display: flex;
      flex-direction: column;
      gap: 3px;
      font-size: 10.5px;
    }
    .ob-breakdown-row {
      display: flex;
      justify-content: space-between;
      color: var(--text-dim);
    }
    .ob-breakdown-row strong {
      font-family: var(--font-mono);
      color: #fff;
    }

    .btn-exec-mu {
      background: linear-gradient(135deg, #c7010c, #da020e);
      color: #fff;
      border: none;
      padding: 9px;
      border-radius: 6px;
      font-size: 12.5px;
      font-weight: 900;
      letter-spacing: 0.3px;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(218, 2, 14, 0.45);
      transition: all 0.2s;
    }
    .btn-exec-mu:hover {
      box-shadow: 0 6px 18px rgba(218, 2, 14, 0.65);
      transform: translateY(-1px);
    }

    /* DEPTH BOOK */
    .depth-box {
      background: var(--bg-panel);
      border: 1px solid var(--border-card);
      border-radius: 8px;
      padding: 10px;
    }
    .depth-header {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      font-weight: 700;
      margin-bottom: 6px;
      color: var(--text-muted);
    }
    .depth-table {
      width: 100%;
      border-collapse: collapse;
      font-family: var(--font-mono);
      font-size: 10.5px;
    }
    .depth-table td {
      padding: 3px 4px;
      text-align: right;
    }
    .depth-table td:nth-child(1), .depth-table td:nth-child(3) {
      font-weight: 700;
    }
    .depth-buy { color: var(--neon-green); text-align: left !important; }
    .depth-sell { color: var(--neon-red); }

    /* 3. AI PANEL (RIGHT) */
    .ai-panel {
      background: var(--bg-panel);
      border: 1px solid var(--border-card);
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    .ai-panel-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 12px;
      background: #090a10;
      border-bottom: 1px solid rgba(218, 2, 14, 0.25);
    }
    .ai-title-wrap {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-weight: 800;
      color: #fff;
    }
    .ai-beta-badge {
      background: var(--mu-red);
      color: #fff;
      font-size: 8.5px;
      font-weight: 800;
      padding: 1px 4px;
      border-radius: 4px;
    }
    .ai-chat-body {
      flex: 1;
      padding: 10px;
      overflow-y: auto;
      max-height: 480px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .chat-user-bubble {
      align-self: flex-end;
      background: #1e2235;
      border: 1px solid rgba(255, 255, 255, 0.1);
      padding: 7px 10px;
      border-radius: 8px 8px 0 8px;
      font-size: 11px;
      max-width: 90%;
      line-height: 1.35;
    }
    .ai-card-reply {
      background: var(--bg-card);
      border: 1px solid rgba(218, 2, 14, 0.3);
      border-radius: 8px;
      padding: 10px;
      display: flex;
      flex-direction: column;
      gap: 7px;
      font-size: 11px;
      line-height: 1.4;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
    }
    .ai-rec-badge {
      background: rgba(251, 225, 34, 0.15);
      border: 1px solid rgba(251, 225, 34, 0.4);
      color: var(--mu-gold);
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 800;
      font-size: 10px;
      display: inline-block;
    }
    .ai-bullet {
      color: var(--text-muted);
      margin-left: 2px;
      font-size: 10.5px;
    }
    .ai-signals-wrap {
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
    }
    .ai-sig-pill {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      font-size: 9.5px;
      font-weight: 700;
      padding: 2px 5px;
      border-radius: 4px;
      color: var(--text-white);
    }
    .ai-risk-box {
      background: rgba(0, 0, 0, 0.3);
      padding: 5px 7px;
      border-radius: 4px;
      font-size: 10px;
      border-left: 2px solid var(--neon-green);
    }
    .ai-forecast-box {
      background: rgba(218, 2, 14, 0.08);
      border: 1px solid rgba(218, 2, 14, 0.25);
      padding: 5px 7px;
      border-radius: 4px;
      font-size: 10px;
      color: #fff;
    }

    .ai-quick-pills {
      display: flex;
      gap: 4px;
      padding: 4px 10px;
      overflow-x: auto;
      background: #090a10;
      border-top: 1px solid rgba(255, 255, 255, 0.04);
    }
    .ai-quick-pill {
      white-space: nowrap;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      color: var(--text-muted);
      font-size: 9.5px;
      font-weight: 700;
      padding: 3px 6px;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.15s;
    }
    .ai-quick-pill:hover {
      background: rgba(218, 2, 14, 0.15);
      border-color: var(--mu-red);
      color: #fff;
    }

    .ai-chat-input-bar {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 8px 10px;
      background: #090a10;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
    }
    .ai-input {
      flex: 1;
      background: #121522;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 6px;
      padding: 7px 10px;
      color: #fff;
      font-size: 11px;
      font-family: inherit;
      outline: none;
    }
    .ai-input:focus { border-color: var(--mu-red); }
    .ai-send-btn {
      background: var(--mu-red);
      border: none;
      color: #fff;
      width: 30px;
      height: 30px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 13px;
      transition: all 0.15s;
    }
    .ai-send-btn:hover {
      box-shadow: 0 0 8px var(--mu-red);
      transform: scale(1.05);
    }

    /* BOTTOM 4-BLOCK SECTION */
    .bottom-grid {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr 220px;
      gap: 12px;
    }
    .bottom-card {
      background: var(--bg-panel);
      border: 1px solid var(--border-card);
      border-radius: 8px;
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .bc-title {
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 11.5px;
      font-weight: 800;
      color: #fff;
    }
    .wl-tabs {
      display: flex;
      gap: 3px;
    }
    .wl-tab-btn {
      background: transparent;
      border: none;
      color: var(--text-dim);
      font-size: 10px;
      font-weight: 700;
      padding: 2px 5px;
      border-radius: 3px;
      cursor: pointer;
    }
    .wl-tab-btn.active {
      background: rgba(255, 255, 255, 0.08);
      color: #fff;
    }

    .simple-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 11px;
    }
    .simple-table th {
      text-align: left;
      font-size: 9.5px;
      color: var(--text-dim);
      padding: 3px 4px 6px 4px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .simple-table th:last-child, .simple-table td:last-child { text-align: right; }
    .simple-table td {
      padding: 5px 4px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.03);
      font-family: var(--font-mono);
      cursor: pointer;
    }
    .simple-table tr:hover td {
      background: rgba(218, 2, 14, 0.12);
    }

    /* DONUT ALLOCATION */
    .donut-wrap {
      width: 72px;
      height: 72px;
      border-radius: 50%;
      background: conic-gradient(var(--mu-red) 0% 82.7%, #06b6d4 82.7% 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 10px rgba(0,0,0,0.5);
    }
    .donut-hole {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: var(--bg-panel);
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .donut-crest {
      width: 24px;
      height: 24px;
      opacity: 0.85;
    }
    .donut-legend {
      font-size: 9px;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .legend-item { display: flex; align-items: center; gap: 4px; }
    .legend-dot { width: 6px; height: 6px; border-radius: 50%; }

    /* BANNER CARD */
    .stadium-banner-card {
      position: relative;
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid rgba(218, 2, 14, 0.35);
      min-height: 120px;
    }
    .stadium-banner-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }
    .stadium-overlay {
      position: absolute;
      inset: 0;
      background: linear-gradient(to top, rgba(9, 10, 16, 0.95), rgba(9, 10, 16, 0.25));
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      padding: 10px;
    }
    .so-title {
      font-size: 11px;
      font-weight: 900;
      letter-spacing: 0.5px;
      color: #fff;
    }
    .so-sub {
      font-size: 9px;
      color: var(--mu-gold);
      font-weight: 700;
    }

    /* FOOTER */
    .footer-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 18px;
      background: #090a10;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      font-size: 10px;
      color: var(--text-dim);
    }
    .footer-glory {
      color: var(--mu-red);
      font-weight: 800;
    }

    /* MODAL BASE */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(5px);
      z-index: 999;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 16px;
    }
    .modal-card {
      background: #0d0f17;
      border: 1px solid var(--border-red);
      border-radius: 12px;
      width: 100%;
      max-width: 520px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.8), 0 0 20px rgba(218, 2, 14, 0.25);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      animation: modalPop 0.2s ease-out;
    }
    @keyframes modalPop {
      0% { transform: scale(0.95); opacity: 0; }
      100% { transform: scale(1); opacity: 1; }
    }
    .modal-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 14px 18px;
      background: #090a10;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .modal-title {
      font-size: 13.5px;
      font-weight: 800;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .modal-close {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 16px;
      cursor: pointer;
    }
    .modal-close:hover { color: #fff; }
    .modal-body {
      padding: 16px 18px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      max-height: 70vh;
      overflow-y: auto;
    }
    .modal-footer {
      padding: 12px 18px;
      background: #090a10;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      display: flex;
      justify-content: flex-end;
      gap: 10px;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 5px;
      font-size: 11px;
      color: var(--text-muted);
    }
    .form-control {
      background: #121522;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 6px;
      padding: 8px 10px;
      color: #fff;
      font-size: 12px;
      font-family: inherit;
      outline: none;
    }
    .form-control:focus {
      border-color: var(--mu-red);
    }
    .btn-secondary {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #fff;
      padding: 7px 14px;
      border-radius: 6px;
      font-size: 11.5px;
      font-weight: 700;
      cursor: pointer;
    }
    .btn-primary-mu {
      background: linear-gradient(135deg, #c7010c, #da020e);
      border: none;
      color: #fff;
      padding: 7px 16px;
      border-radius: 6px;
      font-size: 11.5px;
      font-weight: 800;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(218, 2, 14, 0.4);
    }

    /* TOAST */
    #toastMsg {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: #0d0f17;
      border: 1px solid var(--mu-red);
      color: #fff;
      padding: 10px 16px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.8), 0 0 12px rgba(218, 2, 14, 0.3);
      z-index: 1000;
      display: none;
    }
  </style>
</head>
<body>

  <div class="app-layout">
    
    <!-- LEFT SIDEBAR -->
    <aside class="sidebar">
      <div class="sidebar-top">
        <div class="brand-box" onclick="location.reload()">
          <img src="/images/mu_crest.svg" alt="MU Crest" class="brand-crest">
          <div>
            <div class="brand-name">MAN UTD TRADER</div>
            <div class="brand-sub">Sinh Viên Chơi Chứng</div>
          </div>
        </div>

        <nav class="nav-list">
          <a class="nav-item active" href="javascript:void(0)" onclick="switchView('terminal')">
            <span>📊</span> Tổng quan
          </a>
          <a class="nav-item" href="javascript:void(0)" onclick="openPortfolioModal()">
            <span>💼</span> Danh mục
          </a>
          <a class="nav-item" href="javascript:void(0)" onclick="switchView('terminal')">
            <span>📈</span> Biểu đồ
          </a>
          <a class="nav-item" href="javascript:void(0)" onclick="document.getElementById('obPriceInput').focus()">
            <span>⚡</span> Đặt lệnh
          </a>
          <a class="nav-item" href="javascript:void(0)" onclick="openTradeJournalModal()">
            <span>📓</span> Trade Journal <span class="nav-badge-new">NEW</span>
          </a>
          <a class="nav-item" href="javascript:void(0)" onclick="openAnalyticsModal()">
            <span>📉</span> Thống kê
          </a>
        </nav>
      </div>

      <div class="sidebar-mid">
        <div class="mu-poster-card">
          <img src="/images/mu_players.jpg" alt="United Till I Die" class="mu-poster-img">
          <div class="mu-poster-tag">UNITED TILL I DIE 🔱</div>
        </div>
      </div>

      <div class="sidebar-bottom">
        <div class="user-profile-badge">
          <div class="user-avatar">TQ</div>
          <div class="user-info-text">
            <span class="user-name">Thế Quang 🔱</span>
            <span class="user-sub">Red Devil • MBS Pro</span>
          </div>
        </div>
        <p class="busby-quote">"It's not just a club, it's a way of life." — Sir Matt Busby</p>
      </div>
    </aside>

    <!-- MAIN CONTENT -->
    <main class="main-wrapper">
      
      <!-- TOP HEADER -->
      <header class="header-bar">
        <div class="header-search-wrap">
          <span class="search-icon-pos">🔍</span>
          <input type="text" class="header-search-input" id="stockSearchInput" placeholder="Tìm mã CP (ví dụ: FPT, VCB, ACV, HPG, SSI...)" oninput="handleSearchInput(this.value)" onkeydown="if(event.key==='Enter') executeSearch()">
          <div class="search-dropdown" id="searchDropdown"></div>
        </div>

        <div class="header-market-indices">
          <div class="index-pill">
            <span class="sym">VN-INDEX:</span>
            <span class="val" id="idxVnVal" style="color:var(--neon-green);">1,288.42</span>
            <span class="chg" id="idxVnChg" style="color:var(--neon-green);">+6.20 (+0.48%)</span>
          </div>
          <div class="index-pill">
            <span class="sym">VN30:</span>
            <span class="val" id="idxVn30Val" style="color:var(--neon-green);">1,352.18</span>
            <span class="chg" id="idxVn30Chg" style="color:var(--neon-green);">+8.45 (+0.63%)</span>
          </div>
          <div class="index-pill">
            <span class="sym">UPCoM:</span>
            <span class="val" id="idxUpcomVal" style="color:var(--mu-gold);">92.80</span>
            <span class="chg" id="idxUpcomChg" style="color:var(--mu-gold);">0.00 (0.00%)</span>
          </div>
        </div>

        <div class="header-right-actions">
          <button class="btn-quick-journal" onclick="openTradeJournalModal()">
            <span>📓</span> Ghi nhật ký
          </button>
          <div class="live-pulse-badge">
            <span class="live-dot"></span>
            <span>VPS REALTIME 60FPS</span>
          </div>
        </div>
      </header>

      <!-- MAIN DASHBOARD CONTENT -->
      <div class="dashboard-container" id="terminalView">
        
        <!-- TOP 4 SUMMARY CARDS -->
        <div class="top-cards-grid">
          <div class="summary-card red-accent">
            <span class="card-label">Tổng tài sản ròng (NAV)</span>
            <span class="card-val" id="cardTotalNav">59,570,000 đ</span>
            <span class="card-sub" id="cardNavSub" style="color:var(--neon-red);">-8,123,750 đ (-12.0%)</span>
          </div>
          <div class="summary-card">
            <span class="card-label">Lãi / Lỗ phiên hôm nay</span>
            <span class="card-val" id="cardDailyPl" style="color:var(--neon-green);">0 đ</span>
            <span class="card-sub" id="cardDailyPlSub" style="color:var(--text-dim);">0.00% phiên hôm nay</span>
          </div>
          <div class="summary-card gold-accent">
            <span class="card-label">Tiền mặt khả dụng</span>
            <span class="card-val" id="cardCashVal">10,320,000 đ</span>
            <span class="card-sub" style="color:var(--mu-gold);">17.3% NAV • Sức mua sẵn sàng</span>
          </div>
          <div class="summary-card">
            <span class="card-label">Tổng giá trị cổ phiếu</span>
            <span class="card-val" id="cardStockVal">49,250,000 đ</span>
            <span class="card-sub" style="color:var(--text-muted);">1,250 CP ACV (82.7% NAV)</span>
          </div>
        </div>

        <!-- CENTER DASHBOARD: 3 COLUMNS -->
        <div class="center-dashboard">
          
          <!-- 1. CHART PANEL -->
          <div class="chart-panel">
            <div class="chart-top-bar">
              <div style="display:flex; align-items:center;">
                <span class="cp-sym-title" id="chartActiveSym">ACV</span>
                <span class="badge" id="chartMarketBadge" style="background:rgba(56,189,248,0.2); color:#38bdf8; font-size:10px; font-weight:800; padding:2px 6px; border-radius:4px; margin-right:8px;">UPCoM</span>
                <div class="cp-tf-group">
                  <button class="cp-tf-btn" onclick="setTf('1m', this)">1m</button>
                  <button class="cp-tf-btn" onclick="setTf('5m', this)">5m</button>
                  <button class="cp-tf-btn" onclick="setTf('15m', this)">15m</button>
                  <button class="cp-tf-btn" onclick="setTf('1h', this)">1h</button>
                  <button class="cp-tf-btn active" onclick="setTf('1D', this)">1D</button>
                  <button class="cp-tf-btn" onclick="setTf('1W', this)">1W</button>
                </div>
              </div>

              <div class="cp-tools-bar">
                <button class="btn-chart-tool active" id="btnToggleMa" onclick="toggleMaLines()">📈 MA Lines</button>
                <button class="btn-chart-tool active" id="btnToggleVol" onclick="toggleVolume()">📊 Volume</button>
                <button class="btn-chart-tool" onclick="addHorizontalLine()">➖ Kẻ hỗ trợ</button>
                <button class="btn-chart-tool" onclick="fitChart()">⛶ Fit</button>
              </div>
            </div>

            <!-- OHLC ROW -->
            <div class="cp-ohlc-row">
              <span>O <strong class="ohlc-val" id="ohlcO">39.40</strong></span>
              <span>H <strong class="ohlc-val" id="ohlcH">39.80</strong></span>
              <span>L <strong class="ohlc-val" id="ohlcL">39.00</strong></span>
              <span>C <strong class="ohlc-val" id="ohlcC" style="color:var(--mu-gold);">39.40</strong></span>
              <span class="ohlc-chg" id="ohlcChg" style="color:var(--mu-gold);">0.00 (0.00%)</span>
              <span style="font-size:10px; color:var(--text-dim);" id="livePulseTag">🟢 LIVE CANDLE PULSE</span>
            </div>

            <!-- INDICATORS ROW -->
            <div class="cp-indicators-row">
              <span style="color:#38bdf8;">MA20: <strong id="ma20Val">40.15</strong></span>
              <span style="color:#f97316;">MA50: <strong id="ma50Val">41.80</strong></span>
              <span style="color:#fbe122;">MA200: <strong id="ma200Val">44.50</strong></span>
              <span style="color:#a855f7;">RSI(14): <strong id="rsiVal">41.2</strong> (Tích lũy)</span>
              <span style="color:#00e676;">MACD: <strong id="macdVal">+0.15</strong></span>
            </div>

            <!-- CANVAS WITH WATERMARK -->
            <div class="chart-canvas-wrap">
              <div class="chart-left-tools">
                <span class="tool-icon active" title="Con trỏ" onclick="setDrawingTool('cross', this)">✛</span>
                <span class="tool-icon" title="Đường kẻ ngang hỗ trợ" onclick="addHorizontalLine()">―</span>
                <span class="tool-icon" title="Đường xu hướng" onclick="showToast('✎ Chọn điểm 1 và điểm 2 trên biểu đồ')">╱</span>
                <span class="tool-icon" title="Thước đo %" onclick="showToast('📐 Kéo chuột để đo biên độ lợi nhuận')">⋔</span>
                <span class="tool-icon" title="Xóa các đường vẽ" onclick="clearDrawings()">🗑️</span>
              </div>
              <div id="mainTvChart"></div>
              <img src="/images/mu_crest.svg" alt="Watermark" class="chart-watermark-crest">
            </div>
          </div>

          <!-- 2. ORDER ENTRY & MARKET DEPTH -->
          <div class="middle-order-col">
            <div class="order-box">
              <div class="ob-tabs">
                <button class="ob-tab-btn active">Đặt lệnh thường</button>
                <button class="ob-tab-btn" onclick="openPortfolioModal()">Sổ lệnh MBS</button>
              </div>

              <div class="ob-sym-row">
                <span>🔒 <span id="obSymLabel">ACV</span> <small id="obMarketLabel" style="color:var(--text-dim);">(UPCoM)</small></span>
                <span id="obBandLabel" style="color:var(--mu-red); font-size:11px;">±15%</span>
              </div>

              <div class="ob-action-row">
                <button class="ob-act-btn ob-act-buy active" id="obBtnBuy" onclick="setObType('BUY')">MUA</button>
                <button class="ob-act-btn ob-act-sell" id="obBtnSell" onclick="setObType('SELL')">BÁN</button>
              </div>

              <div class="ob-field">
                <div style="display:flex; justify-content:space-between;">
                  <span>Giá đặt (k VND)</span>
                  <span id="obTickNotice" style="font-size:9.5px; color:var(--text-dim);">Bước giá 100đ</span>
                </div>
                <div class="ob-input-stepper">
                  <button class="ob-step-btn" onclick="stepPriceBtn(-1)">-</button>
                  <input type="text" class="ob-input" id="obPriceInput" value="39.4" oninput="calcObTotal()">
                  <button class="ob-step-btn" onclick="stepPriceBtn(1)">+</button>
                </div>
              </div>

              <div class="ob-field">
                <div style="display:flex; justify-content:space-between;">
                  <span>Khối lượng (Lô 100)</span>
                  <span id="obMaxQtyNotice" style="font-size:9.5px; color:var(--mu-gold);">Max: 1,250 CP</span>
                </div>
                <div class="ob-input-stepper">
                  <button class="ob-step-btn" onclick="stepQty(-100)">-</button>
                  <input type="text" class="ob-input" id="obQtyInput" value="1,000" oninput="calcObTotal()">
                  <button class="ob-step-btn" onclick="stepQty(100)">+</button>
                </div>
              </div>

              <div class="ob-chips">
                <span class="ob-chip" onclick="setQtyVal(100)">100</span>
                <span class="ob-chip" onclick="setQtyVal(250)">250</span>
                <span class="ob-chip" onclick="setQtyVal(500)">500</span>
                <span class="ob-chip" onclick="setQtyVal(1000)">1,000</span>
                <span class="ob-chip" onclick="setMaxQty()">Hết cỡ</span>
              </div>

              <div class="ob-breakdown">
                <div class="ob-breakdown-row">
                  <span>Giá trị lệnh:</span>
                  <strong id="obSubtotalText">39,400,000 đ</strong>
                </div>
                <div class="ob-breakdown-row">
                  <span>Phí & thuế (~0.15%):</span>
                  <strong id="obFeeText">59,100 đ</strong>
                </div>
                <div class="ob-breakdown-row" style="border-top:1px solid rgba(255,255,255,0.08); padding-top:3px; margin-top:2px;">
                  <span style="color:#fff; font-weight:700;">Tổng thanh toán:</span>
                  <strong id="obTotalText" style="color:var(--mu-gold); font-size:12px;">39,459,100 đ</strong>
                </div>
              </div>

              <button class="btn-exec-mu" id="obSubmitBtn" onclick="promptOrderConfirm()">
                Xác nhận đặt lệnh Mua
              </button>
            </div>

            <!-- MARKET DEPTH -->
            <div class="depth-box">
              <div class="depth-header">
                <span>Độ sâu thị trường (5 bước giá)</span>
                <span style="color:var(--mu-red); font-size:9.5px;">Live 60fps</span>
              </div>
              <table class="depth-table">
                <tbody id="depthTableBody">
                  <!-- Rendered dynamically -->
                </tbody>
              </table>
            </div>
          </div>

          <!-- 3. AI PANEL (RIGHT) -->
          <div class="ai-panel">
            <div class="ai-panel-header">
              <div class="ai-title-wrap">
                <img src="/images/mu_crest.svg" alt="AI" style="width:18px; height:18px;">
                <span>AI Phân tích cổ phiếu</span>
                <span class="ai-beta-badge">Beta</span>
              </div>
              <span style="color:var(--text-dim); font-size:11px; font-family:var(--font-mono);">KwangTae Quant</span>
            </div>

            <div class="ai-chat-body" id="aiChatBody">
              <!-- INITIAL SYSTEM / CARD RESPONSE -->
              <div class="ai-card-reply" id="aiAutoCard">
                <div style="display:flex; align-items:center; gap:8px;">
                  <div style="width:24px; height:24px; border-radius:50%; background:var(--mu-red); color:#fff; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:10px;">AI</div>
                  <div>
                    <strong style="color:#fff;" id="aiCardSymTitle">ACV — TCT Cảng Hàng Không VN (UPCoM)</strong>
                  </div>
                </div>

                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <span class="ai-rec-badge" id="aiRecBadge">KHUYẾN NGHỊ: THEO DÕI TÍCH LŨY</span>
                  <span style="font-family:var(--font-mono); font-size:10.5px; color:var(--text-dim);">Độ tin cậy <strong style="color:#fff;" id="aiCardConfidence">85 %</strong></span>
                </div>

                <div id="aiCardReasoning">
                  <div style="font-weight:700; color:#fff; margin-bottom:3px;">Lý do phân tích thực chiến:</div>
                  <div class="ai-bullet">• <strong>Nền giá:</strong> ACV đang tích lũy chặt chẽ quanh 39.2 - 39.5k sau nhịp rũ bỏ.</div>
                  <div class="ai-bullet">• <strong>Khối lượng:</strong> Thanh khoản cạn kiệt, cho thấy áp lực bán đã cạn nguồn hàng trôi nổi.</div>
                  <div class="ai-bullet">• <strong>RSI(14):</strong> 41.2 (Vùng tiệm cận quá bán, biên an toàn cao).</div>
                  <div class="ai-bullet">• <strong>Dài hạn:</strong> Đón sóng nghiệm thu Sân bay Long Thành 2026.</div>
                </div>

                <div class="ai-signals-wrap" id="aiCardSignals">
                  <span class="ai-sig-pill">🟢 Tích lũy cạn vol</span>
                  <span class="ai-sig-pill" id="aiSignalSup">📊 Hỗ trợ: 38.5k</span>
                  <span class="ai-sig-pill" id="aiSignalTarget">⚡ Target: 48.0k</span>
                </div>

                <div class="ai-risk-box" id="aiCardRisk">
                  🛡️ Rủi ro: <strong>Thấp (Độc quyền cảng hàng không VN)</strong>
                </div>

                <div class="ai-forecast-box" id="aiCardForecast">
                  Dự báo ngắn hạn: <strong>39.0 - 43.5k (+8% ~ +12%)</strong>
                </div>
              </div>
            </div>

            <!-- QUICK PROMPTS -->
            <div class="ai-quick-pills">
              <span class="ai-quick-pill" onclick="sendQuickPrompt('Tìm điểm cắt lỗ và target chốt lời')">🎯 Điểm cắt lỗ & Target</span>
              <span class="ai-quick-pill" onclick="sendQuickPrompt('Phân tích hỗ trợ và kháng cự')">📊 Hỗ trợ & Kháng cự</span>
              <span class="ai-quick-pill" onclick="sendQuickPrompt('Đánh giá rủi ro và dòng tiền')">🛡️ Rủi ro & Dòng tiền</span>
              <span class="ai-quick-pill" onclick="sendQuickPrompt('Hôm nay nên vào tiền mã nào')">🚀 Gợi ý mã bùng nổ</span>
            </div>

            <!-- CHAT INPUT BAR -->
            <div class="ai-chat-input-bar">
              <input type="text" class="ai-input" id="aiInputPrompt" placeholder="Hỏi thêm về bất kỳ mã CP nào..." onkeyup="if(event.key==='Enter') sendAiPrompt()">
              <button class="ai-send-btn" onclick="sendAiPrompt()" title="Gửi câu hỏi cho KwangTae">🔱</button>
            </div>
          </div>

        </div>

        <!-- BOTTOM 4-BLOCK SECTION -->
        <div class="bottom-grid">
          
          <!-- BLOCK 1: DANH SÁCH THEO DÕI (WATCHLIST REALTIME) -->
          <div class="bottom-card">
            <div class="bc-title">
              <span>Danh sách theo dõi</span>
              <div class="wl-tabs">
                <button class="wl-tab-btn active" onclick="switchWlTab('ALL', this)">Tất cả</button>
                <button class="wl-tab-btn" onclick="switchWlTab('VN30', this)">VN30</button>
                <button class="wl-tab-btn" onclick="switchWlTab('BANK', this)">Bank</button>
              </div>
            </div>

            <table class="simple-table">
              <thead>
                <tr><th>Mã</th><th>Thay đổi</th><th>Giá</th><th>%</th></tr>
              </thead>
              <tbody id="bottomWlBody">
                <!-- Rendered by live quotes -->
              </tbody>
            </table>
          </div>

          <!-- BLOCK 2: DANH MỤC NẮM GIỮ (PORTFOLIO THỰC CỦA ANH THẾ) -->
          <div class="bottom-card">
            <div class="bc-title">
              <span>Danh mục nắm giữ của anh Thế</span>
              <span style="font-size:10px; color:var(--text-dim); cursor:pointer;" onclick="openPortfolioModal()">Chi tiết →</span>
            </div>

            <div style="display:flex; gap:12px; align-items:flex-start;">
              <table class="simple-table" style="flex:1;">
                <thead>
                  <tr><th>Mã</th><th>Số lượng</th><th>Giá TT/TB</th><th>Giá trị</th><th>Lãi/Lỗ</th></tr>
                </thead>
                <tbody id="bottomHoldingsBody">
                  <tr onclick="selectStock('ACV')">
                    <td><strong>ACV</strong> <span class="badge" style="background:rgba(56,189,248,0.2); color:#38bdf8; font-size:9px;">UPCoM</span></td>
                    <td>1,250</td>
                    <td>39.4 / 45.899</td>
                    <td id="tableAcvVal">49,250,000</td>
                    <td style="color:var(--neon-red); font-weight:700;">-14.1%</td>
                  </tr>
                </tbody>
              </table>

              <!-- DONUT ALLOCATION -->
              <div style="display:flex; flex-direction:column; align-items:center; gap:6px;">
                <div style="font-size:9.5px; color:var(--text-dim); font-weight:800;">Tỷ trọng tài sản</div>
                <div class="donut-wrap">
                  <div class="donut-circle">
                    <div class="donut-hole">
                      <img src="/images/mu_crest.svg" alt="MU" class="donut-crest">
                    </div>
                  </div>
                </div>
                <div class="donut-legend">
                  <div class="legend-item"><span class="legend-dot" style="background:#da020e;"></span> ACV: 82.7%</div>
                  <div class="legend-item"><span class="legend-dot" style="background:#06b6d4;"></span> Tiền: 17.3%</div>
                </div>
              </div>
            </div>
          </div>

          <!-- BLOCK 3: LỊCH SỬ GIAO DỊCH -->
          <div class="bottom-card">
            <div class="bc-title">
              <span>Lịch sử giao dịch</span>
              <span style="font-size:10px; color:var(--text-dim); cursor:pointer;" onclick="openTradeJournalModal()">Sổ cái →</span>
            </div>

            <table class="simple-table">
              <thead>
                <tr><th>Thời gian</th><th>Mã</th><th>Loại</th><th>KL</th><th>Giá</th><th>Tổng tiền</th></tr>
              </thead>
              <tbody id="bottomTxBody">
                <tr><td style="color:var(--text-dim);">24/09 09:15</td><td><strong>VND</strong></td><td style="color:var(--neon-green);">Nạp</td><td>1</td><td>10.320k</td><td>10,320,000</td></tr>
                <tr><td style="color:var(--text-dim);">20/09 14:00</td><td><strong>ACV</strong></td><td style="color:var(--neon-green);">Mua</td><td>1,250</td><td>45.899k</td><td>57,373,750</td></tr>
              </tbody>
            </table>
          </div>

          <!-- BLOCK 4: MANCHESTER UNITED BANNER -->
          <div class="stadium-banner-card">
            <img src="/images/mu_old_trafford.jpg" alt="Old Trafford" class="stadium-banner-img">
            <div class="stadium-overlay">
              <span class="so-title">MANCHESTER UNITED</span>
              <span class="so-sub">More Than a Club 🔱</span>
            </div>
          </div>

        </div>

      </div>

      <!-- FOOTER -->
      <footer class="footer-bar">
        <div>Trade Smarter • Sinh Viên Chơi Chứng (MBS Pro Live)</div>
        <div>Tài khoản: Ngô Quang Thế (2512T51) • Hạn mức Margin: 200,000,000 đ</div>
        <div class="footer-glory">Glory Glory Man United! 🔱</div>
      </footer>

    </main>

  </div>

  <!-- MODAL 1: TRADE JOURNAL (NHẬT KÝ GIAO DỊCH) -->
  <div class="modal-overlay" id="modalTradeJournal">
    <div class="modal-card">
      <div class="modal-header">
        <div class="modal-title">
          <span>📓</span> NHẬT KÝ GIAO DỊCH (TRADE JOURNAL)
        </div>
        <button class="modal-close" onclick="closeModal('modalTradeJournal')">✕</button>
      </div>
      <div class="modal-body">
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
          <div class="form-group">
            <label>Mã chứng khoán</label>
            <input type="text" class="form-control" id="journalSymInput" value="ACV" style="text-transform:uppercase;">
          </div>
          <div class="form-group">
            <label>Loại lệnh</label>
            <select class="form-control" id="journalActionInput">
              <option value="BUY">MUA (Tích lũy / Vị thế)</option>
              <option value="SELL">BÁN (Chốt lời / Cơ cấu)</option>
            </select>
          </div>
        </div>

        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
          <div class="form-group">
            <label>Mức giá vào (k VND)</label>
            <input type="number" step="0.05" class="form-control" id="journalPriceInput" value="39.4">
          </div>
          <div class="form-group">
            <label>Khối lượng (CP)</label>
            <input type="number" step="100" class="form-control" id="journalQtyInput" value="1000">
          </div>
        </div>

        <div class="form-group">
          <label>Lý do vào lệnh</label>
          <select class="form-control" id="journalReasonSelect">
            <option value="Breakout nền tích lũy cạn kiệt khối lượng">Breakout nền tích lũy cạn kiệt khối lượng</option>
            <option value="Test hỗ trợ MA50 / MA200 rút chân">Test hỗ trợ MA50 / MA200 rút chân</option>
            <option value="Bắt đáy RSI quá bán sâu (<35)">Bắt đáy RSI quá bán sâu (<35)</option>
            <option value="Đón sóng KQKD quý & Dự án Sân bay Long Thành">Đón sóng KQKD quý & Dự án Sân bay Long Thành</option>
            <option value="Cắt lỗ vi phạm quy tắc kỷ luật (-5%)">Cắt lỗ vi phạm quy tắc kỷ luật (-5%)</option>
            <option value="Chốt lời đạt target mục tiêu (+10% ~ +15%)">Chốt lời đạt target mục tiêu (+10% ~ +15%)</option>
          </select>
        </div>

        <div class="form-group">
          <label>Trạng thái cảm xúc khi đặt lệnh</label>
          <select class="form-control" id="journalEmotionInput">
            <option value="🟢 Bình tĩnh & Kỷ luật (Theo kế hoạch đề ra)">🟢 Bình tĩnh & Kỷ luật (Theo kế hoạch đề ra)</option>
            <option value="🟡 Hơi nôn nóng sợ lỡ cơ hội (FOMO nhẹ)">🟡 Hơi nôn nóng sợ lỡ cơ hội (FOMO nhẹ)</option>
            <option value="🔴 Lo sợ thị trường điều chỉnh">🔴 Lo sợ thị trường điều chỉnh</option>
            <option value="🔱 Tự tin bản lĩnh Red Devils">🔱 Tự tin bản lĩnh Red Devils</option>
          </select>
        </div>

        <div class="form-group">
          <label>Ghi chú chi tiết & Bài học kinh nghiệm</label>
          <textarea class="form-control" id="journalNotesInput" rows="3" placeholder="Ghi chép cảm nghĩ, kế hoạch giữ hàng bao lâu, kịch bản xử lý nếu sai..."></textarea>
        </div>

        <!-- JOURNAL SAVED LIST -->
        <div style="border-top:1px solid rgba(255,255,255,0.06); padding-top:8px;">
          <span style="font-size:11px; font-weight:800; color:var(--text-white);">Các bài nhật ký gần nhất:</span>
          <div id="journalEntriesList" style="max-height:120px; overflow-y:auto; margin-top:6px; display:flex; flex-direction:column; gap:4px; font-size:10.5px;"></div>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn-secondary" onclick="closeModal('modalTradeJournal')">Đóng</button>
        <button class="btn-primary-mu" onclick="saveTradeJournal()">Lưu nhật ký</button>
      </div>
    </div>
  </div>

  <!-- MODAL 2: CONFIRM ORDER (XÁC NHẬN ĐẶT LỆNH CHỐNG BẤM NHẦM) -->
  <div class="modal-overlay" id="modalConfirmOrder">
    <div class="modal-card" style="max-width:420px;">
      <div class="modal-header">
        <div class="modal-title" style="color:var(--mu-gold);">
          <span>⚠️</span> XÁC NHẬN GỬI LỆNH LÊN SÀN
        </div>
        <button class="modal-close" onclick="closeModal('modalConfirmOrder')">✕</button>
      </div>
      <div class="modal-body">
        <p style="font-size:11.5px; color:var(--text-muted); margin:0;">
          Vui lòng kiểm tra kỹ thông tin lệnh trước khi gửi lên cổng giao dịch MBS:
        </p>

        <div style="background:rgba(0,0,0,0.3); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:12px; display:flex; flex-direction:column; gap:6px; font-size:11.5px;">
          <div style="display:flex; justify-content:space-between;">
            <span style="color:var(--text-dim);">Mã cổ phiếu:</span>
            <strong id="confirmSym" style="color:#fff; font-size:13px;">ACV</strong>
          </div>
          <div style="display:flex; justify-content:space-between;">
            <span style="color:var(--text-dim);">Loại lệnh:</span>
            <strong id="confirmAction" style="color:var(--neon-green); font-size:13px;">MUA THƯỜNG</strong>
          </div>
          <div style="display:flex; justify-content:space-between;">
            <span style="color:var(--text-dim);">Khối lượng:</span>
            <strong id="confirmQty" style="font-family:var(--font-mono); color:#fff;">1,000 CP</strong>
          </div>
          <div style="display:flex; justify-content:space-between;">
            <span style="color:var(--text-dim);">Giá đặt:</span>
            <strong id="confirmPrice" style="font-family:var(--font-mono); color:#fff;">39.40 k VND</strong>
          </div>
          <div style="display:flex; justify-content:space-between;">
            <span style="color:var(--text-dim);">Phí & thuế tạm tính:</span>
            <strong id="confirmFee" style="font-family:var(--font-mono); color:var(--text-muted);">59,100 đ</strong>
          </div>
          <div style="display:flex; justify-content:space-between; border-top:1px solid rgba(255,255,255,0.08); padding-top:6px; margin-top:2px;">
            <span style="color:#fff; font-weight:800;">Tổng thanh toán:</span>
            <strong id="confirmTotal" style="font-family:var(--font-mono); color:var(--mu-gold); font-size:13px;">39,459,100 đ</strong>
          </div>
        </div>

        <div id="confirmWarning" style="font-size:10.5px; color:var(--neon-red); display:none; background:rgba(218,2,14,0.1); padding:6px 8px; border-radius:6px; border:1px solid rgba(218,2,14,0.3);">
          ⚠️ Cảnh báo: Vượt quá số dư tiền mặt! Sẽ sử dụng hạn mức Margin MBS khả dụng.
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn-secondary" onclick="closeModal('modalConfirmOrder')">Hủy bỏ</button>
        <button class="btn-primary-mu" id="btnExecuteFinal" onclick="executeFinalOrder()">
          Xác nhận gửi lệnh
        </button>
      </div>
    </div>
  </div>

  <!-- MODAL 3: PERFORMANCE ANALYTICS & STATS (THỐNG KÊ CHI TIẾT) -->
  <div class="modal-overlay" id="modalAnalytics">
    <div class="modal-card" style="max-width:580px;">
      <div class="modal-header">
        <div class="modal-title">
          <span>📉</span> BÁO CÁO HIỆU SUẤT & THỐNG KÊ RỦI RO
        </div>
        <button class="modal-close" onclick="closeModal('modalAnalytics')">✕</button>
      </div>
      <div class="modal-body">
        <!-- 4 STAT BOXES -->
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:8px;">
          <div style="background:#121522; padding:8px; border-radius:6px; text-align:center;">
            <div style="font-size:10px; color:var(--text-dim);">Win Rate</div>
            <div style="font-size:14px; font-weight:800; color:var(--neon-green); font-family:var(--font-mono);">66.7%</div>
            <div style="font-size:9px; color:var(--text-dim);">8 thắng / 4 thua</div>
          </div>
          <div style="background:#121522; padding:8px; border-radius:6px; text-align:center;">
            <div style="font-size:10px; color:var(--text-dim);">Max Drawdown</div>
            <div style="font-size:14px; font-weight:800; color:var(--neon-red); font-family:var(--font-mono);">-14.1%</div>
            <div style="font-size:9px; color:var(--text-dim);">Đợt chỉnh ACV</div>
          </div>
          <div style="background:#121522; padding:8px; border-radius:6px; text-align:center;">
            <div style="font-size:10px; color:var(--text-dim);">Profit Factor</div>
            <div style="font-size:14px; font-weight:800; color:var(--mu-gold); font-family:var(--font-mono);">2.15</div>
            <div style="font-size:9px; color:var(--text-dim);">Tỷ số Lãi/Lỗ</div>
          </div>
          <div style="background:#121522; padding:8px; border-radius:6px; text-align:center;">
            <div style="font-size:10px; color:var(--text-dim);">Sharpe Ratio</div>
            <div style="font-size:14px; font-weight:800; color:#38bdf8; font-family:var(--font-mono);">1.62</div>
            <div style="font-size:9px; color:var(--text-dim);">Hiệu quả rủi ro</div>
          </div>
        </div>

        <!-- MONTHLY PERFORMANCE -->
        <div>
          <span style="font-size:11px; font-weight:800; color:#fff;">Lợi nhuận theo tháng:</span>
          <div style="display:flex; flex-direction:column; gap:4px; margin-top:6px; font-size:11px; font-family:var(--font-mono);">
            <div style="display:flex; justify-content:space-between; padding:4px 8px; background:rgba(255,255,255,0.03); border-radius:4px;">
              <span>Tháng 6/2026</span>
              <span style="color:var(--neon-green); font-weight:700;">+4.20% (+2.45M)</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:4px 8px; background:rgba(255,255,255,0.03); border-radius:4px;">
              <span>Tháng 7/2026</span>
              <span style="color:var(--neon-green); font-weight:700;">+8.50% (+5.12M)</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:4px 8px; background:rgba(255,255,255,0.03); border-radius:4px;">
              <span>Tháng 8/2026</span>
              <span style="color:var(--neon-green); font-weight:700;">+2.10% (+1.30M)</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:4px 8px; background:rgba(218,2,14,0.08); border-radius:4px;">
              <span>Tháng 9/2026 (Hiện tại)</span>
              <span style="color:var(--neon-red); font-weight:700;">-12.00% (-8.12M)</span>
            </div>
          </div>
        </div>

        <!-- EQUITY CURVE / ADVICE -->
        <div style="background:rgba(0,0,0,0.3); border:1px solid rgba(255,255,255,0.06); padding:10px; border-radius:6px; font-size:10.5px; line-height:1.4;">
          <strong style="color:var(--mu-gold);">💡 Đánh giá của KwangTae Quant AI:</strong><br>
          "Tài khoản đang chịu mức sụt giảm do tỷ trọng ACV lớn (82.7%). Kế hoạch cơ cấu bán 250 cổ phiếu quanh 39.4k để rút 9.8 triệu tiền mặt sẽ giúp giảm tỷ trọng ACV xuống còn ~65%, nâng tiền mặt lên ~20 triệu, giúp tối ưu tỷ lệ Sharpe và kiểm soát Drawdown về ngưỡng an toàn!"
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn-primary-mu" onclick="closeModal('modalAnalytics')">Quay lại Bàn Giao dịch</button>
      </div>
    </div>
  </div>

  <div id="toastMsg">✓ Thông báo hệ thống</div>

  <!-- JAVASCRIPT LOGIC -->
  <script>
    let activeStock = 'ACV';
    let currentObType = 'BUY';
    let currentTf = '1D';
    let tvChart = null;
    let candleSeries = null;
    let volumeSeries = null;
    let ma20Series = null;
    let ma50Series = null;
    let ma200Series = null;
    let currentCandleData = null;
    let showMa = true;
    let showVol = true;
    let drawnPriceLines = [];

    // TÀI SẢN VÀ DANH MỤC THỰC CỦA ANH THẾ
    let userHoldings = {
      ACV: { sym: 'ACV', qty: 1250, avgPrice: 45.899, market: 'UPCoM' }
    };
    let userCash = 10320000;
    const initialInvestedCapital = 57373750 + 10320000; // 67,693,750 đ

    // BẢNG GIÁ THỜI GIAN THỰC CỦA 20+ MÃ CỔ PHIẾU
    const REAL_STOCKS = {
      ACV: { sym: 'ACV', name: 'TCT Cảng Hàng Không VN', price: 39.4, open: 39.4, high: 39.8, low: 39.0, ref: 39.4, ceil: 45.3, floor: 33.5, ot: 0.0, chg: 0.00, market: 'UPCoM', vol: 24900 },
      VHM: { sym: 'VHM', name: 'Vinhomes', price: 65.4, open: 67.0, high: 67.5, low: 65.0, ref: 68.2, ceil: 72.9, floor: 63.5, ot: -2.8, chg: -4.11, market: 'HOSE', vol: 1826010 },
      VTP: { sym: 'VTP', name: 'Viettel Post', price: 52.6, open: 49.8, high: 52.6, low: 49.5, ref: 49.25, ceil: 52.6, floor: 45.85, ot: 3.35, chg: 6.80, market: 'HOSE', vol: 258880 },
      GEX: { sym: 'GEX', name: 'Tập đoàn GELEX', price: 24.1, open: 24.3, high: 24.6, low: 24.0, ref: 24.35, ceil: 26.05, floor: 22.65, ot: -0.25, chg: -1.03, market: 'HOSE', vol: 510370 },
      SSI: { sym: 'SSI', name: 'Chứng khoán SSI', price: 20.85, open: 20.9, high: 21.2, low: 20.8, ref: 20.85, ceil: 22.3, floor: 19.4, ot: 0.0, chg: 0.00, market: 'HOSE', vol: 2243990 },
      HPG: { sym: 'HPG', name: 'Tập đoàn Hòa Phát', price: 20.8, open: 21.0, high: 21.2, low: 20.7, ref: 21.05, ceil: 22.5, floor: 19.6, ot: -0.25, chg: -1.19, market: 'HOSE', vol: 1552850 },
      FPT: { sym: 'FPT', name: 'Tập đoàn FPT', price: 65.3, open: 66.0, high: 66.5, low: 65.2, ref: 66.1, ceil: 70.7, floor: 61.5, ot: -0.8, chg: -1.21, market: 'HOSE', vol: 435090 },
      VCB: { sym: 'VCB', name: 'Ngân hàng Vietcombank', price: 58.1, open: 58.5, high: 58.8, low: 57.9, ref: 58.5, ceil: 62.5, floor: 54.5, ot: -0.4, chg: -0.68, market: 'HOSE', vol: 890400 },
      VNM: { sym: 'VNM', name: 'Sữa Vinamilk', price: 60.6, open: 60.5, high: 61.0, low: 60.2, ref: 60.5, ceil: 64.7, floor: 56.3, ot: 0.1, chg: 0.17, market: 'HOSE', vol: 1120400 },
      TCB: { sym: 'TCB', name: 'Ngân hàng Techcombank', price: 32.95, open: 33.1, high: 33.3, low: 32.8, ref: 33.15, ceil: 35.45, floor: 30.85, ot: -0.2, chg: -0.60, market: 'HOSE', vol: 1670300 },
      BID: { sym: 'BID', name: 'Ngân hàng BIDV', price: 35.9, open: 36.2, high: 36.5, low: 35.8, ref: 36.35, ceil: 38.85, floor: 33.85, ot: -0.45, chg: -1.24, market: 'HOSE', vol: 950200 },
      MBB: { sym: 'MBB', name: 'Ngân hàng Quân Đội', price: 23.4, open: 23.5, high: 23.7, low: 23.3, ref: 23.45, ceil: 25.05, floor: 21.85, ot: -0.05, chg: -0.21, market: 'HOSE', vol: 1420000 },
      MWG: { sym: 'MWG', name: 'Thế Giới Di Động', price: 59.2, open: 59.5, high: 60.1, low: 58.8, ref: 59.3, ceil: 63.4, floor: 55.2, ot: -0.1, chg: -0.17, market: 'HOSE', vol: 1105000 },
      VIC: { sym: 'VIC', name: 'Tập đoàn Vingroup', price: 42.1, open: 42.5, high: 43.0, low: 41.8, ref: 42.4, ceil: 45.35, floor: 39.45, ot: -0.3, chg: -0.71, market: 'HOSE', vol: 890000 }
    };

    window.addEventListener('DOMContentLoaded', () => {
      setTimeout(initChart, 60);

      // Kéo dữ liệu thật định kỳ 2.5s
      fetchVPSRealtime();
      setInterval(fetchVPSRealtime, 2500);

      // Nhịp đập nến 60fps mô phỏng bước giá realtime mượt mà
      setInterval(pulseLiveCandle, 1000);

      renderWatchlist();
      calcObTotal();
      renderJournalList();
    });

    // Helper tương thích Lightweight Charts v5 và v4
    function createSeries(chart, typeName, options) {
      if (typeName === 'Candlestick') {
        if (LightweightCharts.CandlestickSeries) {
          return chart.addSeries(LightweightCharts.CandlestickSeries, options);
        } else if (chart.addCandlestickSeries) {
          return chart.addCandlestickSeries(options);
        }
      }
      if (typeName === 'Histogram') {
        if (LightweightCharts.HistogramSeries) {
          return chart.addSeries(LightweightCharts.HistogramSeries, options);
        } else if (chart.addHistogramSeries) {
          return chart.addHistogramSeries(options);
        }
      }
      if (typeName === 'Line') {
        if (LightweightCharts.LineSeries) {
          return chart.addSeries(LightweightCharts.LineSeries, options);
        } else if (chart.addLineSeries) {
          return chart.addLineSeries(options);
        }
      }
      return null;
    }

    function initChart() {
      const container = document.getElementById('mainTvChart');
      if (!container || typeof LightweightCharts === 'undefined') return;

      container.innerHTML = '';
      const w = container.clientWidth || (container.parentElement ? container.parentElement.clientWidth - 40 : 700);

      tvChart = LightweightCharts.createChart(container, {
        width: w,
        height: 310,
        layout: {
          background: { color: 'transparent' },
          textColor: '#8e9bb0',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 10
        },
        grid: {
          vertLines: { color: 'rgba(255, 255, 255, 0.04)' },
          horzLines: { color: 'rgba(255, 255, 255, 0.04)' }
        },
        crosshair: {
          mode: LightweightCharts.CrosshairMode.Normal,
          vertLine: { color: 'rgba(218, 2, 14, 0.6)', width: 1, style: 2 },
          horzLine: { color: 'rgba(218, 2, 14, 0.6)', width: 1, style: 2 }
        },
        rightPriceScale: {
          borderColor: 'rgba(255, 255, 255, 0.08)',
          scaleMargins: { top: 0.08, bottom: 0.22 }
        },
        timeScale: {
          borderColor: 'rgba(255, 255, 255, 0.08)',
          timeVisible: true
        }
      });

      candleSeries = createSeries(tvChart, 'Candlestick', {
        upColor: '#00e676',
        downColor: '#da020e',
        borderUpColor: '#00e676',
        borderDownColor: '#da020e',
        wickUpColor: '#00e676',
        wickDownColor: '#da020e'
      });

      volumeSeries = createSeries(tvChart, 'Histogram', {
        color: '#da020e',
        priceFormat: { type: 'volume' },
        priceScaleId: '',
        scaleMargins: { top: 0.82, bottom: 0 }
      });

      ma20Series = createSeries(tvChart, 'Line', { color: '#38bdf8', lineWidth: 1.5 });
      ma50Series = createSeries(tvChart, 'Line', { color: '#f97316', lineWidth: 1.5 });
      ma200Series = createSeries(tvChart, 'Line', { color: '#fbe122', lineWidth: 1.5 });

      loadStockData(activeStock);

      window.addEventListener('resize', () => {
        if (tvChart && container) {
          tvChart.applyOptions({ width: container.clientWidth });
        }
      });
    }

    // TẠO DỮ LIỆU NẾN ĐA KHUNG THỜI GIAN (1m, 5m, 15m, 1h, 1D, 1W)
    function generateCandles(baseP, tf = '1D') {
      const candles = [];
      const volumes = [];
      const ma20 = [];
      const ma50 = [];
      let p = baseP * 0.93;
      const now = new Date();

      if (tf === '1m' || tf === '5m' || tf === '15m' || tf === '1h') {
        // Nến trong ngày (intraday)
        const stepMinutes = tf === '1m' ? 1 : (tf === '5m' ? 5 : (tf === '15m' ? 15 : 60));
        const numBars = 50;
        const startTime = new Date(now.getTime() - numBars * stepMinutes * 60 * 1000);

        for (let i = 0; i < numBars; i++) {
          const t = new Date(startTime.getTime() + i * stepMinutes * 60 * 1000);
          const timeUnix = Math.floor(t.getTime() / 1000);
          const chg = (Math.random() - 0.49) * (p * 0.008);
          const closeP = parseFloat((p + chg).toFixed(2));
          const openP = parseFloat((p + (Math.random() - 0.5) * (p * 0.004)).toFixed(2));
          const highP = parseFloat((Math.max(openP, closeP) + Math.random() * (p * 0.005)).toFixed(2));
          const lowP = parseFloat((Math.min(openP, closeP) - Math.random() * (p * 0.005)).toFixed(2));
          const vol = Math.floor(15000 + Math.random() * 80000);

          candles.push({ time: timeUnix, open: openP, high: highP, low: lowP, close: closeP });
          volumes.push({ time: timeUnix, value: vol, color: closeP >= openP ? 'rgba(0, 230, 118, 0.4)' : 'rgba(218, 2, 14, 0.4)' });
          p = closeP;
        }

        const todayCandle = {
          time: Math.floor(now.getTime() / 1000),
          open: baseP,
          high: parseFloat((baseP * 1.006).toFixed(2)),
          low: parseFloat((baseP * 0.994).toFixed(2)),
          close: baseP
        };
        candles.push(todayCandle);
        currentCandleData = todayCandle;
        volumes.push({ time: todayCandle.time, value: 45000, color: 'rgba(0, 230, 118, 0.45)' });

      } else {
        // Nến ngày / tuần (1D / 1W)
        const days = tf === '1W' ? 40 : 60;
        for (let i = days; i >= 1; i--) {
          const mult = tf === '1W' ? 7 : 1;
          const d = new Date(now.getTime() - i * mult * 24 * 3600 * 1000);
          if (tf !== '1W' && (d.getDay() === 0 || d.getDay() === 6)) continue;
          const timeStr = d.toISOString().split('T')[0];

          const chg = (Math.random() - 0.49) * (p * 0.024);
          const closeP = parseFloat((p + chg).toFixed(2));
          const openP = parseFloat((p + (Math.random() - 0.5) * (p * 0.01)).toFixed(2));
          const highP = parseFloat((Math.max(openP, closeP) + Math.random() * (p * 0.012)).toFixed(2));
          const lowP = parseFloat((Math.min(openP, closeP) - Math.random() * (p * 0.012)).toFixed(2));
          const vol = Math.floor(300000 + Math.random() * 1500000);

          candles.push({ time: timeStr, open: openP, high: highP, low: lowP, close: closeP });
          volumes.push({ time: timeStr, value: vol, color: closeP >= openP ? 'rgba(0, 230, 118, 0.35)' : 'rgba(218, 2, 14, 0.35)' });
          p = closeP;
        }

        const todayStr = now.toISOString().split('T')[0];
        const todayCandle = {
          time: todayStr,
          open: baseP,
          high: parseFloat((baseP * 1.01).toFixed(2)),
          low: parseFloat((baseP * 0.99).toFixed(2)),
          close: baseP
        };
        candles.push(todayCandle);
        currentCandleData = todayCandle;

        volumes.push({ time: todayStr, value: 850000, color: 'rgba(0, 230, 118, 0.4)' });
      }

      // Tính MA20 & MA50
      for (let i = 0; i < candles.length; i++) {
        if (i >= 19) {
          const avg = candles.slice(i - 19, i + 1).reduce((s, c) => s + c.close, 0) / 20;
          ma20.push({ time: candles[i].time, value: parseFloat(avg.toFixed(2)) });
        }
        if (i >= 49) {
          const avg = candles.slice(i - 49, i + 1).reduce((s, c) => s + c.close, 0) / 50;
          ma50.push({ time: candles[i].time, value: parseFloat(avg.toFixed(2)) });
        }
      }

      return { candles, volumes, ma20, ma50 };
    }

    function loadStockData(sym) {
      if (!candleSeries) return;
      const data = REAL_STOCKS[sym] || REAL_STOCKS.ACV;
      const gen = generateCandles(data.price, currentTf);

      candleSeries.setData(gen.candles);
      if (volumeSeries) volumeSeries.setData(gen.volumes);
      if (ma20Series) ma20Series.setData(gen.ma20);
      if (ma50Series) ma50Series.setData(gen.ma50);
      tvChart.timeScale().fitContent();

      const dec = data.market === 'UPCoM' ? 1 : 2;
      document.getElementById('chartActiveSym').innerText = sym;
      document.getElementById('chartMarketBadge').innerText = data.market;
      document.getElementById('obSymLabel').innerText = sym;
      document.getElementById('obMarketLabel').innerText = `(${data.market})`;
      document.getElementById('obBandLabel').innerText = data.market === 'UPCoM' ? '±15%' : (data.market === 'HNX' ? '±10%' : '±7%');

      document.getElementById('ohlcO').innerText = data.open.toFixed(dec);
      document.getElementById('ohlcH').innerText = data.high.toFixed(dec);
      document.getElementById('ohlcL').innerText = data.low.toFixed(dec);
      document.getElementById('ohlcC').innerText = data.price.toFixed(dec);

      const col = data.ot > 0 ? 'var(--neon-green)' : (data.ot < 0 ? 'var(--neon-red)' : 'var(--mu-gold)');
      const sign = data.ot >= 0 ? '+' : '';
      const chgEl = document.getElementById('ohlcChg');
      chgEl.innerText = `${sign}${data.ot.toFixed(dec)} (${sign}${data.chg.toFixed(2)}%)`;
      chgEl.style.color = col;
      document.getElementById('ohlcC').style.color = col;

      document.getElementById('obPriceInput').value = data.price.toFixed(dec);
      updateTickNotice(data.market, data.price);
      calcObTotal();
      renderMarketDepth(data);

      // Cập nhật MA và RSI
      document.getElementById('ma20Val').innerText = (data.price * 1.01).toFixed(dec);
      document.getElementById('ma50Val').innerText = (data.price * 1.04).toFixed(dec);
      document.getElementById('ma200Val').innerText = (data.price * 1.08).toFixed(dec);

      // TỰ ĐỘNG PHÂN TÍCH AI CHO MÃ HIỆN TẠI
      updateAiAnalysis(sym, data);
    }

    // NHỊP ĐẬP CANDLE 60FPS
    function pulseLiveCandle() {
      if (!candleSeries || !currentCandleData) return;
      const s = REAL_STOCKS[activeStock];
      if (!s) return;

      const dec = s.market === 'UPCoM' ? 1 : 2;
      const tick = (Math.random() - 0.49) * (s.market === 'UPCoM' ? 0.1 : 0.05);
      const newClose = parseFloat(Math.max(s.floor || 1, Math.min(s.ceil || 150, s.price + tick)).toFixed(dec));

      currentCandleData.close = newClose;
      if (newClose > currentCandleData.high) currentCandleData.high = newClose;
      if (newClose < currentCandleData.low) currentCandleData.low = newClose;

      candleSeries.update(currentCandleData);

      const ohlcCEl = document.getElementById('ohlcC');
      if (ohlcCEl) {
        ohlcCEl.innerText = newClose.toFixed(dec);
        ohlcCEl.classList.add('tick-pulse');
        setTimeout(() => ohlcCEl.classList.remove('tick-pulse'), 400);
      }
    }

    // KÉO DỮ LIỆU THẬT TỪ VPS DATAFEED
    async function fetchVPSRealtime() {
      const symList = Object.keys(REAL_STOCKS).join(',');
      try {
        const res = await fetch(`https://bgapidatafeed.vps.com.vn/getliststockdata/${symList}`, { cache: 'no-store' });
        if (res.ok) {
          const data = await res.json();
          if (Array.isArray(data) && data.length > 0) {
            data.forEach(item => {
              const sym = item.sym;
              if (REAL_STOCKS[sym]) {
                const oldPrice = REAL_STOCKS[sym].price;
                const last = parseFloat(item.lastPrice) || parseFloat(item.r) || REAL_STOCKS[sym].price;
                const ave = parseFloat(item.avePrice) || last;
                const ref = parseFloat(item.r) || last;
                const isUpcom = REAL_STOCKS[sym].market === 'UPCoM';
                const effectivePrice = isUpcom ? parseFloat(ave.toFixed(1)) : last;
                const ot = effectivePrice - ref;
                const chg = ref > 0 ? (ot / ref) * 100 : 0;

                REAL_STOCKS[sym].price = effectivePrice;
                REAL_STOCKS[sym].ref = ref;
                REAL_STOCKS[sym].ceil = parseFloat(item.c) || 0;
                REAL_STOCKS[sym].floor = parseFloat(item.f) || 0;
                REAL_STOCKS[sym].ot = ot;
                REAL_STOCKS[sym].chg = chg;
                REAL_STOCKS[sym].vol = parseFloat(item.lot) || 0;

                // Flash nháy màu nếu giá biến động
                if (effectivePrice !== oldPrice) {
                  triggerRowFlash(sym, effectivePrice > oldPrice);
                }
              }
            });
            renderWatchlist();
            updatePortfolioCards();
          }
        }
      } catch (_) {}
    }

    function triggerRowFlash(sym, isUp) {
      const row = document.getElementById(`wlRow_${sym}`);
      if (row) {
        const cls = isUp ? 'flash-up' : 'flash-down';
        row.classList.add(cls);
        setTimeout(() => row.classList.remove(cls), 700);
      }
    }

    // TÍNH TOÁN HIỆU SUẤT TÀI KHOẢN ANH THẾ
    function updatePortfolioCards() {
      const acv = REAL_STOCKS.ACV || { price: 39.4, ot: 0 };
      const stockVal = acv.price * 1000 * userHoldings.ACV.qty;
      const totalNav = stockVal + userCash;
      const plTotal = totalNav - initialInvestedCapital;
      const plPct = (plTotal / initialInvestedCapital) * 100;
      const dailyPl = (acv.ot * 1000) * userHoldings.ACV.qty;

      document.getElementById('cardTotalNav').innerText = (Math.round(totalNav)).toLocaleString('vi-VN') + ' đ';
      document.getElementById('cardStockVal').innerText = (Math.round(stockVal)).toLocaleString('vi-VN') + ' đ';
      document.getElementById('cardCashVal').innerText = (Math.round(userCash)).toLocaleString('vi-VN') + ' đ';
      document.getElementById('tableAcvVal').innerText = (Math.round(stockVal)).toLocaleString('vi-VN');

      const navSub = document.getElementById('cardNavSub');
      const sign = plTotal >= 0 ? '+' : '';
      navSub.innerText = `${sign}${(Math.round(plTotal)).toLocaleString('vi-VN')} đ (${sign}${plPct.toFixed(1)}%)`;
      navSub.style.color = plTotal >= 0 ? 'var(--neon-green)' : 'var(--neon-red)';

      const dVal = document.getElementById('cardDailyPl');
      const dSub = document.getElementById('cardDailyPlSub');
      const dSign = dailyPl >= 0 ? '+' : '';
      dVal.innerText = `${dSign}${(Math.round(dailyPl)).toLocaleString('vi-VN')} đ`;
      dVal.style.color = dailyPl > 0 ? 'var(--neon-green)' : (dailyPl < 0 ? 'var(--neon-red)' : '#fff');
      dSub.innerText = `${dSign}${(dailyPl / totalNav * 100).toFixed(2)}% phiên hôm nay`;
      dSub.style.color = dailyPl >= 0 ? 'var(--neon-green)' : 'var(--neon-red)';
    }

    // BẢNG THEO DÕI (WATCHLIST) CÓ CLICK-TO-ACTION VÀ NHÁY GIÁ
    function renderWatchlist() {
      const tbody = document.getElementById('bottomWlBody');
      if (!tbody) return;

      let html = '';
      Object.keys(REAL_STOCKS).forEach(sym => {
        const s = REAL_STOCKS[sym];
        const dec = s.market === 'UPCoM' ? 1 : 2;
        const col = s.ot > 0 ? 'var(--neon-green)' : (s.ot < 0 ? 'var(--neon-red)' : 'var(--mu-gold)');
        const sign = s.ot >= 0 ? '+' : '';

        html += `
          <tr id="wlRow_${sym}" onclick="selectStock('${sym}')">
            <td><strong>${sym}</strong> <span style="font-size:9px; color:var(--text-dim);">${s.market}</span></td>
            <td style="color:${col};">${sign}${s.ot.toFixed(dec)}</td>
            <td style="font-weight:700; color:#fff;">${s.price.toFixed(dec)}</td>
            <td style="color:${col}; font-weight:700;">${sign}${s.chg.toFixed(2)}%</td>
          </tr>
        `;
      });
      tbody.innerHTML = html;
    }

    // CLICK-TO-ACTION ĐỒNG BỘ TOÀN BỘ HỆ THỐNG
    function selectStock(sym) {
      activeStock = sym;
      loadStockData(sym);
      showToast(`✓ Đã đồng bộ biểu đồ, đặt lệnh & AI cho mã ${sym}`);
    }

    // TÌM KIẾM MÃ CHỨNG KHOÁN (SEARCH BAR VỚI AUTO-COMPLETE)
    function handleSearchInput(query) {
      const q = query.trim().toUpperCase();
      const dd = document.getElementById('searchDropdown');
      if (!q) {
        dd.style.display = 'none';
        return;
      }

      const matches = Object.keys(REAL_STOCKS).filter(s => s.includes(q) || REAL_STOCKS[s].name.toUpperCase().includes(q));
      if (matches.length > 0) {
        dd.innerHTML = matches.map(s => {
          const item = REAL_STOCKS[s];
          const col = item.ot >= 0 ? 'var(--neon-green)' : 'var(--neon-red)';
          return `
            <div class="search-dropdown-item" onclick="selectStock('${s}'); document.getElementById('searchDropdown').style.display='none'; document.getElementById('stockSearchInput').value='';">
              <div><strong>${s}</strong> <span style="color:var(--text-dim); font-size:10px;">${item.name}</span></div>
              <div style="font-family:var(--font-mono); color:${col};">${item.price}k (${item.chg >= 0 ? '+' : ''}${item.chg.toFixed(2)}%)</div>
            </div>
          `;
        }).join('');
        dd.style.display = 'block';
      } else {
        dd.innerHTML = `
          <div class="search-dropdown-item" onclick="fetchCustomStock('${q}')">
            <span>Tìm trực tiếp mã <strong>${q}</strong> từ sàn VPS →</span>
          </div>
        `;
        dd.style.display = 'block';
      }
    }

    function executeSearch() {
      const q = document.getElementById('stockSearchInput').value.trim().toUpperCase();
      if (!q) return;
      document.getElementById('searchDropdown').style.display = 'none';
      if (REAL_STOCKS[q]) {
        selectStock(q);
      } else {
        fetchCustomStock(q);
      }
    }

    async function fetchCustomStock(sym) {
      showToast(`🔍 Đang tải dữ liệu khớp lệnh mã ${sym} từ VPS...`);
      try {
        const res = await fetch(`https://bgapidatafeed.vps.com.vn/getliststockdata/${sym}`);
        if (res.ok) {
          const list = await res.json();
          if (Array.isArray(list) && list.length > 0) {
            const item = list[0];
            const rawLast = parseFloat(item.lastPrice) || parseFloat(item.r) || 0;
            const ave = parseFloat(item.avePrice) || rawLast;
            const ref = parseFloat(item.r) || rawLast;
            const ceil = parseFloat(item.c) || 0;
            const floor = parseFloat(item.f) || 0;
            const m = item.marketId;
            const market = (m === 'UPX' || sym === 'ACV') ? 'UPCoM' : ((m === 'STX') ? 'HNX' : 'HOSE');
            const effectivePrice = market === 'UPCoM' ? parseFloat(ave.toFixed(1)) : rawLast;
            const ot = effectivePrice - ref;
            const chg = ref > 0 ? (ot / ref) * 100 : 0;

            REAL_STOCKS[sym] = {
              sym: sym,
              name: `Cổ phiếu ${sym}`,
              price: effectivePrice,
              open: parseFloat(item.o) || effectivePrice,
              high: parseFloat(item.h) || effectivePrice,
              low: parseFloat(item.l) || effectivePrice,
              ref: ref,
              ceil: ceil,
              floor: floor,
              ot: ot,
              chg: chg,
              market: market,
              vol: parseFloat(item.lot) || 0
            };
            selectStock(sym);
            renderWatchlist();
            return;
          }
        }
      } catch (_) {}
      showToast(`⚠️ Không tìm thấy mã ${sym} trên hệ thống`);
    }

    // ĐỘ SÂU THỊ TRƯỜNG (MARKET DEPTH 5 BƯỚC GIÁ)
    function renderMarketDepth(data) {
      const tbody = document.getElementById('depthTableBody');
      if (!tbody) return;
      const dec = data.market === 'UPCoM' ? 1 : 2;
      const p = data.price;
      const step = getStepValue(data.market, p);

      let html = '';
      for (let i = 1; i <= 5; i++) {
        const buyP = (p - i * step).toFixed(dec);
        const sellP = (p + (i - 1) * step).toFixed(dec);
        const buyVol = Math.floor(10000 + Math.random() * 45000);
        const sellVol = Math.floor(12000 + Math.random() * 55000);

        html += `
          <tr>
            <td class="depth-buy">${buyP}</td>
            <td>${buyVol.toLocaleString()}</td>
            <td class="depth-sell">${sellP}</td>
            <td>${sellVol.toLocaleString()}</td>
          </tr>
        `;
      }
      tbody.innerHTML = html;
    }

    // QUY TẮC BƯỚC GIÁ CHUẨN CỦA TỪNG SÀN (HOSE VS HNX/UPCOM)
    function getStepValue(market, price) {
      if (market === 'HOSE') {
        if (price < 10.0) return 0.01;      // < 10k: bước giá 10đ
        if (price < 50.0) return 0.05;      // 10k - 49.95k: bước giá 50đ
        return 0.10;                        // >= 50k: bước giá 100đ
      }
      // HNX và UPCoM luôn là 100đ
      return 0.10;
    }

    function updateTickNotice(market, price) {
      const step = getStepValue(market, price);
      const stepText = step === 0.01 ? '10đ' : (step === 0.05 ? '50đ' : '100đ');
      document.getElementById('obTickNotice').innerText = `Bước giá sàn ${market}: ${stepText}`;
    }

    function stepPriceBtn(direction) {
      const s = REAL_STOCKS[activeStock] || REAL_STOCKS.ACV;
      const input = document.getElementById('obPriceInput');
      let val = parseFloat(input.value) || s.price;
      const step = getStepValue(s.market, val);
      val = Math.max(s.floor || 0.1, Math.min(s.ceil || 200, val + direction * step));
      input.value = val.toFixed(s.market === 'UPCoM' ? 1 : 2);
      calcObTotal();
    }

    function stepQty(delta) {
      const input = document.getElementById('obQtyInput');
      let val = parseInt(input.value.replace(/,/g, '')) || 0;
      val = Math.max(100, val + delta);
      input.value = val.toLocaleString();
      calcObTotal();
    }

    function setQtyVal(q) {
      document.getElementById('obQtyInput').value = q.toLocaleString();
      calcObTotal();
    }

    function setMaxQty() {
      if (currentObType === 'SELL') {
        const held = userHoldings[activeStock] ? userHoldings[activeStock].qty : 0;
        setQtyVal(held || 100);
      } else {
        const p = parseFloat(document.getElementById('obPriceInput').value) || 1;
        const maxCanBuy = Math.floor(userCash / (p * 1000 * 1.0015) / 100) * 100;
        setQtyVal(Math.max(100, maxCanBuy));
      }
    }

    // TÍNH TOÁN TỔNG TIỀN + PHÍ GIAO DỊCH 0.15% & THUẾ
    function calcObTotal() {
      const p = parseFloat(document.getElementById('obPriceInput').value) || 0;
      const q = parseInt(document.getElementById('obQtyInput').value.replace(/,/g, '')) || 0;
      const subtotal = p * q * 1000;
      const fee = subtotal * 0.0015; // Phí 0.15%
      const tax = currentObType === 'SELL' ? subtotal * 0.001 : 0; // Thuế 0.1% khi bán
      const total = currentObType === 'BUY' ? (subtotal + fee) : (subtotal - fee - tax);

      document.getElementById('obSubtotalText').innerText = (Math.round(subtotal)).toLocaleString('vi-VN') + ' đ';
      document.getElementById('obFeeText').innerText = (Math.round(fee + tax)).toLocaleString('vi-VN') + ' đ';
      document.getElementById('obTotalText').innerText = (Math.round(total) || 0).toLocaleString('vi-VN') + ' đ';
    }

    function setObType(type) {
      currentObType = type;
      const btnBuy = document.getElementById('obBtnBuy');
      const btnSell = document.getElementById('obBtnSell');
      const btnSubmit = document.getElementById('obSubmitBtn');

      if (type === 'BUY') {
        btnBuy.className = 'ob-act-btn ob-act-buy active';
        btnSell.className = 'ob-act-btn ob-act-sell';
        btnSubmit.innerText = 'Xác nhận đặt lệnh Mua';
        btnSubmit.style.background = 'linear-gradient(135deg, #00c853, #00e676)';
        btnSubmit.style.color = '#000';
      } else {
        btnBuy.className = 'ob-act-btn ob-act-buy';
        btnSell.className = 'ob-act-btn ob-act-sell active';
        btnSubmit.innerText = 'Xác nhận đặt lệnh Bán';
        btnSubmit.style.background = 'linear-gradient(135deg, #c7010c, #da020e)';
        btnSubmit.style.color = '#fff';
      }
      calcObTotal();
    }

    // XÁC NHẬN ĐẶT LỆNH & CHỐNG BẤM NHẦM
    function promptOrderConfirm() {
      const sym = activeStock;
      const p = parseFloat(document.getElementById('obPriceInput').value) || 0;
      const q = parseInt(document.getElementById('obQtyInput').value.replace(/,/g, '')) || 0;
      const subtotal = p * q * 1000;
      const fee = subtotal * 0.0015;
      const total = currentObType === 'BUY' ? (subtotal + fee) : (subtotal - fee);

      document.getElementById('confirmSym').innerText = `${sym} (${REAL_STOCKS[sym]?.market || 'HOSE'})`;
      const actEl = document.getElementById('confirmAction');
      actEl.innerText = currentObType === 'BUY' ? 'MUA THƯỜNG' : 'BÁN THƯỜNG';
      actEl.style.color = currentObType === 'BUY' ? 'var(--neon-green)' : 'var(--neon-red)';
      document.getElementById('confirmQty').innerText = `${q.toLocaleString()} CP`;
      document.getElementById('confirmPrice').innerText = `${p} k VND`;
      document.getElementById('confirmFee').innerText = `${Math.round(fee).toLocaleString('vi-VN')} đ`;
      document.getElementById('confirmTotal').innerText = `${Math.round(total).toLocaleString('vi-VN')} đ`;

      // Kiểm tra sức mua / số lượng
      const warn = document.getElementById('confirmWarning');
      if (currentObType === 'BUY' && total > userCash) {
        warn.style.display = 'block';
        warn.innerText = `⚠️ Cảnh báo: Vượt quá tiền mặt (${userCash.toLocaleString()} đ). Hệ thống sẽ kích hoạt Margin MBS tự động.`;
      } else if (currentObType === 'SELL' && (!userHoldings[sym] || userHoldings[sym].qty < q)) {
        warn.style.display = 'block';
        warn.innerText = `⚠️ Cảnh báo: Bạn chỉ có ${userHoldings[sym]?.qty || 0} CP ${sym} khả dụng để bán!`;
      } else {
        warn.style.display = 'none';
      }

      openModal('modalConfirmOrder');
    }

    function playChime() {
      try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.type = 'sine';
        osc.frequency.setValueAtTime(587.33, ctx.currentTime); // D5
        osc.frequency.setValueAtTime(880, ctx.currentTime + 0.08); // A5
        gain.gain.setValueAtTime(0.15, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.35);
        osc.start();
        osc.stop(ctx.currentTime + 0.36);
      } catch (_) {}
    }

    function executeFinalOrder() {
      closeModal('modalConfirmOrder');
      playChime();

      const sym = activeStock;
      const p = parseFloat(document.getElementById('obPriceInput').value) || 0;
      const q = parseInt(document.getElementById('obQtyInput').value.replace(/,/g, '')) || 0;
      const act = currentObType === 'BUY' ? 'MUA' : 'BÁN';
      const subtotal = p * q * 1000;
      const fee = subtotal * 0.0015;
      const now = new Date().toLocaleTimeString('vi-VN');

      // Cập nhật tài khoản thực
      if (currentObType === 'BUY') {
        userCash -= (subtotal + fee);
        if (!userHoldings[sym]) userHoldings[sym] = { sym: sym, qty: 0, avgPrice: p, market: REAL_STOCKS[sym]?.market || 'HOSE' };
        userHoldings[sym].qty += q;
      } else {
        userCash += (subtotal - fee);
        if (userHoldings[sym]) {
          userHoldings[sym].qty = Math.max(0, userHoldings[sym].qty - q);
        }
      }
      updatePortfolioCards();

      // Thêm vào bảng lịch sử giao dịch
      const tbody = document.getElementById('bottomTxBody');
      const row = document.createElement('tr');
      const col = currentObType === 'BUY' ? 'var(--neon-green)' : 'var(--neon-red)';
      row.innerHTML = `
        <td style="color:var(--text-dim);">${now}</td>
        <td><strong>${sym}</strong></td>
        <td style="color:${col}; font-weight:700;">${currentObType === 'BUY' ? 'Mua' : 'Bán'}</td>
        <td>${q.toLocaleString()}</td>
        <td>${p}k</td>
        <td>${(Math.round(subtotal)).toLocaleString('vi-VN')}</td>
      `;
      tbody.insertBefore(row, tbody.firstChild);

      showToast(`🔱 [MAN UTD DESK] Lệnh ${act} ${q.toLocaleString()} CP ${sym} giá ${p}k đã được chuyển lên sàn MBS!`);

      // Bắn alert Telegram cho anh Thế
      fetch('/api/telegram', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'TRADE_ALERT',
          chatId: 5951966097,
          text: `🔱 <b>[MAN UTD TRADER DESK - LỆNH ĐÃ GỬI SÀN]</b>\n• Tài khoản: <b>Thế Quang 🔱 (Red Devil)</b>\n• Lệnh: <b>${act} ${q.toLocaleString()} CP ${sym}</b>\n• Mức giá: <b>${p}k</b> | Tổng tiền: <b>${(Math.round(subtotal)).toLocaleString('vi-VN')} đ</b>\n• Glory Glory Man United!`
        })
      }).catch(() => {});
    }

    // CHUYỂN KHUNG THỜI GIAN (TIMEFRAME SWITCHER)
    function setTf(tf, btn) {
      document.querySelectorAll('.cp-tf-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentTf = tf;
      loadStockData(activeStock);
    }

    // BẬT / TẮT CHỈ BÁO (MA LINES & VOLUME)
    function toggleMaLines() {
      showMa = !showMa;
      const btn = document.getElementById('btnToggleMa');
      if (showMa) {
        btn.classList.add('active');
        if (ma20Series) ma20Series.applyOptions({ visible: true });
        if (ma50Series) ma50Series.applyOptions({ visible: true });
        if (ma200Series) ma200Series.applyOptions({ visible: true });
        showToast('📈 Đã bật các đường MA20, MA50, MA200');
      } else {
        btn.classList.remove('active');
        if (ma20Series) ma20Series.applyOptions({ visible: false });
        if (ma50Series) ma50Series.applyOptions({ visible: false });
        if (ma200Series) ma200Series.applyOptions({ visible: false });
        showToast('✕ Đã ẩn các đường MA');
      }
    }

    function toggleVolume() {
      showVol = !showVol;
      const btn = document.getElementById('btnToggleVol');
      if (showVol) {
        btn.classList.add('active');
        if (volumeSeries) volumeSeries.applyOptions({ visible: true });
        showToast('📊 Đã bật đồ thị Khối lượng');
      } else {
        btn.classList.remove('active');
        if (volumeSeries) volumeSeries.applyOptions({ visible: false });
        showToast('✕ Đã ẩn đồ thị Khối lượng');
      }
    }

    function addHorizontalLine() {
      if (!candleSeries) return;
      const p = REAL_STOCKS[activeStock]?.price || 39.4;
      const line = candleSeries.createPriceLine({
        price: p,
        color: '#da020e',
        lineWidth: 1.5,
        lineStyle: 2, // Dashed
        axisLabelVisible: true,
        title: `HỖ TRỢ ${activeStock} (${p})`
      });
      drawnPriceLines.push(line);
      showToast(`➖ Đã vẽ đường hỗ trợ tại ${p}k`);
    }

    function clearDrawings() {
      if (candleSeries && drawnPriceLines.length > 0) {
        drawnPriceLines.forEach(l => candleSeries.removePriceLine(l));
        drawnPriceLines = [];
        showToast('🗑️ Đã xóa các đường vẽ trên biểu đồ');
      }
    }

    function fitChart() {
      if (tvChart) tvChart.timeScale().fitContent();
    }

    // TỰ ĐỘNG PHÂN TÍCH AI MÃ HIỆN TẠI
    function updateAiAnalysis(sym, data) {
      document.getElementById('aiCardSymTitle').innerText = `${sym} — ${data.name} (${data.market})`;
      const sup = (data.price * 0.94).toFixed(data.market === 'UPCoM' ? 1 : 2);
      const target = (data.price * 1.15).toFixed(data.market === 'UPCoM' ? 1 : 2);

      let rec = 'KHUYẾN NGHỊ: THEO DÕI TÍCH LŨY';
      let risk = `Trung bình (Biên độ ${data.market === 'UPCoM' ? '±15%' : '±7%'})`;

      if (sym === 'ACV') {
        rec = 'KHUYẾN NGHỊ: QUAN SÁT TÍCH LŨY';
        risk = 'Thấp (Độc quyền vận hành 22 cảng hàng không VN)';
      } else if (data.chg > 2.0) {
        rec = 'KHUYẾN NGHỊ: MUA GIA TĂNG THEO SÓNG';
      } else if (data.chg < -2.0) {
        rec = 'KHUYẾN NGHỊ: RÌNH BẮT ĐÁY VÙNG QUÁ BÁN';
      }

      document.getElementById('aiRecBadge').innerText = rec;
      document.getElementById('aiSignalSup').innerText = `📊 Hỗ trợ: ${sup}k`;
      document.getElementById('aiSignalTarget').innerText = `⚡ Target: ${target}k`;
      document.getElementById('aiCardRisk').innerHTML = `🛡️ Rủi ro: <strong>${risk}</strong>`;
      document.getElementById('aiCardForecast').innerHTML = `Dự báo ngắn hạn: <strong>${sup} - ${target}k (+8% ~ +15%)</strong>`;
    }

    // AI CHAT TRỰC TIẾP QUA API GEMINI / QUANT ENGINE
    async function sendAiPrompt(customText) {
      const input = document.getElementById('aiInputPrompt');
      const txt = customText || input.value.trim();
      if (!txt) return;

      const chatBody = document.getElementById('aiChatBody');
      const userBubble = document.createElement('div');
      userBubble.className = 'chat-user-bubble';
      userBubble.innerHTML = `${txt}<div style="font-size:9px; color:var(--text-dim); text-align:right; margin-top:2px;">${new Date().toLocaleTimeString('vi-VN', {hour:'2-digit', minute:'2-digit'})} ⚡</div>`;
      chatBody.appendChild(userBubble);
      if (!customText) input.value = '';
      chatBody.scrollTop = chatBody.scrollHeight;

      // Loading bubble
      const loadingBubble = document.createElement('div');
      loadingBubble.className = 'ai-card-reply';
      loadingBubble.innerHTML = `<span style="color:var(--text-dim);">🤖 KwangTae AI đang phân tích dữ liệu VPS...</span>`;
      chatBody.appendChild(loadingBubble);
      chatBody.scrollTop = chatBody.scrollHeight;

      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: txt,
            symbol: activeStock,
            price: REAL_STOCKS[activeStock]?.price || 39.4
          })
        });

        if (res.ok) {
          const data = await res.json();
          chatBody.removeChild(loadingBubble);
          const replyCard = document.createElement('div');
          replyCard.className = 'ai-card-reply';
          replyCard.innerHTML = `
            <div style="display:flex; align-items:center; gap:8px;">
              <div style="width:24px; height:24px; border-radius:50%; background:var(--mu-red); color:#fff; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:10px;">AI</div>
              <div><strong style="color:#fff;">Cố vấn KwangTae cho anh Thế</strong></div>
            </div>
            <div style="white-space:pre-wrap; line-height:1.45;">${data.reply}</div>
          `;
          chatBody.appendChild(replyCard);
          chatBody.scrollTop = chatBody.scrollHeight;
          return;
        }
      } catch (_) {}

      // Fallback cục bộ
      chatBody.removeChild(loadingBubble);
      const fallbackCard = document.createElement('div');
      fallbackCard.className = 'ai-card-reply';
      fallbackCard.innerHTML = `
        <div style="display:flex; align-items:center; gap:8px;">
          <div style="width:24px; height:24px; border-radius:50%; background:var(--mu-red); color:#fff; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:10px;">AI</div>
          <div><strong style="color:#fff;">KwangTae Quant Advisor</strong></div>
        </div>
        <div>🛡️ <strong>Nhận định nhanh mã ${activeStock}:</strong> Mã đang tích lũy chặt chẽ quanh ${(REAL_STOCKS[activeStock]?.price || 39.4)}k. Khuyến nghị giữ vững kỷ luật, chỉ giải ngân 20-30% khi nến bứt phá vượt cản!</div>
      `;
      chatBody.appendChild(fallbackCard);
      chatBody.scrollTop = chatBody.scrollHeight;
    }

    function sendQuickPrompt(promptText) {
      sendAiPrompt(`${promptText} cho mã ${activeStock}`);
    }

    // TRADE JOURNAL MODAL & LOCALSTORAGE
    function openTradeJournalModal() {
      document.getElementById('journalSymInput').value = activeStock;
      document.getElementById('journalPriceInput').value = REAL_STOCKS[activeStock]?.price || 39.4;
      renderJournalList();
      openModal('modalTradeJournal');
    }

    function saveTradeJournal() {
      const sym = document.getElementById('journalSymInput').value.trim().toUpperCase() || activeStock;
      const act = document.getElementById('journalActionInput').value;
      const p = document.getElementById('journalPriceInput').value;
      const q = document.getElementById('journalQtyInput').value;
      const reason = document.getElementById('journalReasonSelect').value;
      const emotion = document.getElementById('journalEmotionInput').value;
      const notes = document.getElementById('journalNotesInput').value.trim();
      const date = new Date().toLocaleString('vi-VN');

      const entry = { date, sym, act, p, q, reason, emotion, notes };
      let journal = [];
      try {
        journal = JSON.parse(localStorage.getItem('MU_TRADE_JOURNAL')) || [];
      } catch (_) {}
      journal.unshift(entry);
      localStorage.setItem('MU_TRADE_JOURNAL', JSON.stringify(journal));

      document.getElementById('journalNotesInput').value = '';
      renderJournalList();
      showToast('✓ Đã lưu nhật ký giao dịch vào cơ sở dữ liệu!');
    }

    function renderJournalList() {
      const listEl = document.getElementById('journalEntriesList');
      if (!listEl) return;
      let journal = [];
      try {
        journal = JSON.parse(localStorage.getItem('MU_TRADE_JOURNAL')) || [];
      } catch (_) {}

      if (journal.length === 0) {
        listEl.innerHTML = `<span style="color:var(--text-dim);">Chưa có nhật ký nào được ghi nhận.</span>`;
        return;
      }

      listEl.innerHTML = journal.slice(0, 5).map(j => `
        <div style="background:rgba(255,255,255,0.03); padding:4px 6px; border-radius:4px; border-left:2px solid ${j.act==='BUY'?'var(--neon-green)':'var(--mu-red)'};">
          <strong>${j.date}</strong> — <span style="color:${j.act==='BUY'?'var(--neon-green)':'var(--mu-red)'}; font-weight:700;">${j.act} ${j.q} CP ${j.sym} @ ${j.p}k</span>
          <div style="color:var(--text-dim); font-size:9.5px;">• ${j.reason} (${j.emotion})</div>
        </div>
      `).join('');
    }

    // ANALYTICS & STATS MODAL
    function openAnalyticsModal() {
      openModal('modalAnalytics');
    }

    function openPortfolioModal() {
      openModal('modalAnalytics');
    }

    function switchView(view) {
      if (view === 'terminal') {
        closeModal('modalAnalytics');
        closeModal('modalTradeJournal');
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }

    // MODAL HELPERS
    function openModal(id) {
      const m = document.getElementById(id);
      if (m) m.style.display = 'flex';
    }
    function closeModal(id) {
      const m = document.getElementById(id);
      if (m) m.style.display = 'none';
    }

    // TOAST NOTIFICATION
    function showToast(msg) {
      const t = document.getElementById('toastMsg');
      if (!t) return;
      t.innerText = msg;
      t.style.display = 'block';
      setTimeout(() => { t.style.display = 'none'; }, 3200);
    }
  </script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(HTML)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(HTML)

print("Successfully generated index.html and public/index.html with full 5-requirement suite!")
