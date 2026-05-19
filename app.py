import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = "https://movie-recommender-backend-tau.vercel.app/" or "http://127.0.0.1:8000/"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="REELHAUS — Film Discovery",
    page_icon="📽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================
# NEON BRUTALIST FILM LAB AESTHETIC
# =============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:ital,wght@0,300;0,400;0,600;1,300&family=Archivo+Black&display=swap');

:root {
    --neon-cyan:   #00f5ff;
    --neon-magenta:#ff00a8;
    --neon-yellow: #f5ff00;
    --ink:         #0a0a0a;
    --paper:       #f0ede6;
    --mid:         #1a1a1a;
    --border:      rgba(0,245,255,0.25);
    --text-main:   #e8e4dc;
    --text-dim:    rgba(232,228,220,0.45);
}

/* ── BASE ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: var(--ink) !important;
    color: var(--text-main) !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

/* Film grain overlay */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
    opacity: 0.55;
}

/* Scanlines */
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background: repeating-linear-gradient(
        0deg,
        transparent 0px,
        transparent 2px,
        rgba(0,0,0,0.08) 2px,
        rgba(0,0,0,0.08) 4px
    );
}

[data-testid="stHeader"] { background: transparent !important; display: none; }
.block-container {
    padding: 0 2.5rem 5rem !important;
    max-width: 1600px !important;
    position: relative; z-index: 1;
}

/* ── TOPBAR ── */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.2rem 0 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
}
.logo-mark {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem;
    letter-spacing: 0.12em;
    color: var(--text-main);
    position: relative;
    display: inline-block;
}
.logo-mark .neon-r {
    color: var(--neon-cyan);
    text-shadow: 0 0 12px var(--neon-cyan), 0 0 30px rgba(0,245,255,0.4);
}
.logo-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.4em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-top: -6px;
}
.topbar-right {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    color: var(--text-dim);
    text-align: right;
}
.topbar-right span {
    color: var(--neon-magenta);
    text-shadow: 0 0 8px rgba(255,0,168,0.6);
}

/* ── SEARCH ── */
[data-testid="stTextInput"] input {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid var(--neon-cyan) !important;
    border-radius: 0 !important;
    color: var(--text-main) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 1.1rem !important;
    padding: 0.6rem 0.2rem !important;
    box-shadow: 0 4px 20px rgba(0,245,255,0.0) !important;
    transition: box-shadow 0.3s, border-color 0.3s !important;
    caret-color: var(--neon-cyan) !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--neon-magenta) !important;
    box-shadow: 0 6px 24px rgba(255,0,168,0.15) !important;
    outline: none !important;
}
[data-testid="stTextInput"] input::placeholder {
    color: var(--text-dim) !important;
    font-style: italic !important;
}
[data-testid="stTextInput"] label { display: none !important; }
[data-testid="stTextInput"] > div { border: none !important; background: transparent !important; }

/* ── SELECTBOX ── */
[data-testid="stSelectbox"] > div > div {
    background: rgba(0,245,255,0.04) !important;
    border: 1px solid var(--border) !important;
    border-radius: 0 !important;
    color: var(--text-main) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.85rem !important;
}

/* ── CATEGORY TABS ── */
.cat-strip {
    display: flex; gap: 0; margin: 0 0 2.5rem;
    border: 1px solid var(--border);
    overflow: hidden;
}
.cat-item {
    flex: 1; text-align: center;
    padding: 0.6rem 0.4rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-dim);
    border-right: 1px solid var(--border);
    cursor: pointer;
    transition: all 0.2s;
}
.cat-item:last-child { border-right: none; }
.cat-item.active {
    background: var(--neon-cyan);
    color: var(--ink);
    font-weight: 600;
}

/* ── SECTION HEADER ── */
.sec-head {
    display: flex; align-items: baseline; gap: 1rem;
    margin: 2.8rem 0 1.4rem;
}
.sec-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.5rem;
    line-height: 1;
    color: rgba(0,245,255,0.12);
    min-width: 3rem;
}
.sec-title {
    font-family: 'Archivo Black', sans-serif;
    font-size: 0.78rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: var(--text-main);
}
.sec-accent {
    flex: 1; height: 1px;
    background: linear-gradient(90deg, var(--neon-cyan) 0%, transparent 100%);
    opacity: 0.3;
}

/* ── MOVIE CARD ── */
.rh-card {
    position: relative;
    overflow: hidden;
    background: #111;
    cursor: pointer;
    border: 1px solid rgba(255,255,255,0.06);
    transition: border-color 0.2s;
}
.rh-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--neon-cyan), var(--neon-magenta));
    transform: scaleX(0); transform-origin: left;
    transition: transform 0.3s ease;
    z-index: 5;
}
.rh-card:hover::before { transform: scaleX(1); }
.rh-card:hover { border-color: rgba(0,245,255,0.3); }

.rh-card img {
    width: 100%; aspect-ratio: 2/3;
    object-fit: cover; display: block;
    filter: saturate(0.75) contrast(1.1);
    transition: filter 0.35s, transform 0.35s;
}
.rh-card:hover img {
    filter: saturate(1.1) contrast(1.05);
    transform: scale(1.04);
}
.rh-no-img {
    width: 100%; aspect-ratio: 2/3;
    background: repeating-linear-gradient(
        45deg, #111 0px, #111 10px,
        #161616 10px, #161616 20px
    );
    display: flex; align-items: center; justify-content: center;
    font-size: 3rem; color: rgba(0,245,255,0.15);
}

/* Glitch overlay on hover */
.rh-card-overlay {
    position: absolute; inset: 0;
    background: linear-gradient(
        to top,
        rgba(10,10,10,0.97) 0%,
        rgba(10,10,10,0.5) 40%,
        transparent 65%
    );
    display: flex; flex-direction: column; justify-content: flex-end;
    padding: 10px 10px 8px;
    opacity: 0; transition: opacity 0.25s;
    z-index: 3;
}
.rh-card:hover .rh-card-overlay { opacity: 1; }

.rh-card-title {
    font-family: 'Archivo Black', sans-serif;
    font-size: 0.82rem;
    color: var(--text-main);
    line-height: 1.2;
    margin-bottom: 3px;
}
.rh-card-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    color: var(--neon-cyan);
    letter-spacing: 0.08em;
}

/* Film strip holes decorative */
.film-strip-left, .film-strip-right {
    position: fixed; top: 0; bottom: 0; width: 28px;
    z-index: 0; pointer-events: none;
    display: flex; flex-direction: column; align-items: center;
    gap: 18px; padding: 24px 0;
    opacity: 0.06;
}
.film-hole {
    width: 12px; height: 16px;
    border: 2px solid var(--text-main);
    border-radius: 2px; flex-shrink: 0;
}
.film-strip-left { left: 0; border-right: 2px solid var(--text-main); }
.film-strip-right { right: 0; border-left: 2px solid var(--text-main); }

/* ── BUTTONS ── */
[data-testid="stButton"] > button {
    background: transparent !important;
    border: 1px solid rgba(0,245,255,0.35) !important;
    border-radius: 0 !important;
    color: var(--neon-cyan) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    padding: 0.4rem 0.6rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
    position: relative !important;
    overflow: hidden !important;
}
[data-testid="stButton"] > button::after {
    content: '';
    position: absolute; inset: 0;
    background: var(--neon-cyan);
    transform: translateX(-100%);
    transition: transform 0.25s ease;
    z-index: -1;
}
[data-testid="stButton"] > button:hover::after { transform: translateX(0); }
[data-testid="stButton"] > button:hover {
    color: var(--ink) !important;
    border-color: var(--neon-cyan) !important;
    box-shadow: 0 0 20px rgba(0,245,255,0.35) !important;
}

/* ── DETAILS ── */
.d-backdrop-wrap {
    position: relative; width: 100%;
    border: 1px solid var(--border);
    overflow: hidden; margin-bottom: 2rem;
}
.d-backdrop-wrap img {
    width: 100%; height: 320px; object-fit: cover; display: block;
    filter: saturate(0.4) brightness(0.45);
}
.d-backdrop-gradient {
    position: absolute; inset: 0;
    background: linear-gradient(
        to right,
        rgba(10,10,10,1) 0%,
        rgba(10,10,10,0.7) 45%,
        rgba(10,10,10,0.15) 100%
    );
}
.d-backdrop-text {
    position: absolute; left: 2.5rem; top: 50%;
    transform: translateY(-50%);
}
.d-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem; letter-spacing: 0.35em;
    text-transform: uppercase; color: var(--neon-cyan);
    margin-bottom: 0.5rem;
}
.d-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    line-height: 0.95;
    color: var(--text-main);
    letter-spacing: 0.04em;
}
.d-title .glitch-line {
    color: var(--neon-magenta);
    text-shadow: 2px 0 var(--neon-cyan), -2px 0 var(--neon-magenta);
}

/* Details info panel */
.d-info-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid var(--border);
    padding: 1.8rem;
    position: relative;
}
.d-info-panel::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--neon-magenta), var(--neon-cyan), transparent);
}
.d-title-sm {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem;
    letter-spacing: 0.05em;
    color: var(--text-main);
    line-height: 1;
    margin-bottom: 1rem;
}
.d-meta-row {
    display: flex; flex-wrap: wrap; gap: 0.5rem;
    margin-bottom: 1.2rem;
}
.d-badge {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.2rem 0.7rem;
    border: 1px solid rgba(0,245,255,0.3);
    color: var(--neon-cyan);
}
.d-badge.magenta {
    border-color: rgba(255,0,168,0.3);
    color: var(--neon-magenta);
}
.d-rule {
    width: 100%; height: 1px;
    background: linear-gradient(90deg, var(--neon-cyan), transparent);
    opacity: 0.2; margin: 1.2rem 0;
}
.d-overview {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.9;
    color: rgba(232,228,220,0.65);
    font-style: italic;
    font-weight: 300;
}

/* Poster */
.d-poster-frame {
    border: 1px solid var(--border);
    position: relative;
    overflow: hidden;
}
.d-poster-frame::after {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(0,245,255,0.06) 0%, transparent 60%);
    pointer-events: none;
}

/* ── SLIDER ── */
[data-testid="stSlider"] .stSlider > div { background: var(--border) !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #080808 !important;
    border-right: 1px solid var(--border) !important;
}

/* ── INFO / ALERTS ── */
.stAlert {
    background: rgba(0,245,255,0.05) !important;
    border: 1px solid rgba(0,245,255,0.2) !important;
    border-radius: 0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.8rem !important;
}

hr { border-color: var(--border) !important; }
[data-testid="stMarkdownContainer"] p {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.85rem !important;
    color: rgba(232,228,220,0.6) !important;
}

/* Glitch animation */
@keyframes glitch {
    0%  { text-shadow: 2px 0 var(--neon-cyan), -2px 0 var(--neon-magenta); }
    25% { text-shadow: -2px 0 var(--neon-cyan),  2px 0 var(--neon-magenta); }
    50% { text-shadow: 2px 2px var(--neon-cyan), -2px -2px var(--neon-magenta); }
    75% { text-shadow: -3px 0 var(--neon-cyan),   3px 0 var(--neon-magenta); }
    100%{ text-shadow: 2px 0 var(--neon-cyan), -2px 0 var(--neon-magenta); }
}
.logo-mark:hover .neon-r { animation: glitch 0.35s step-end infinite; }

@keyframes flicker {
    0%, 95%, 100% { opacity: 1; }
    96% { opacity: 0.6; }
    98% { opacity: 0.8; }
}
.neon-blink { animation: flicker 4s infinite; }

/* back button override */
.back-wrap [data-testid="stButton"] > button {
    width: auto !important;
    color: var(--text-dim) !important;
    border-color: rgba(255,255,255,0.1) !important;
    font-size: 0.65rem !important;
}
.back-wrap [data-testid="stButton"] > button:hover {
    color: var(--neon-cyan) !important;
    border-color: var(--neon-cyan) !important;
    background: transparent !important;
}
.back-wrap [data-testid="stButton"] > button::after { display: none !important; }
</style>

<!-- Film strip holes -->
<div class="film-strip-left">
  <div class="film-hole"></div><div class="film-hole"></div><div class="film-hole"></div>
  <div class="film-hole"></div><div class="film-hole"></div><div class="film-hole"></div>
  <div class="film-hole"></div><div class="film-hole"></div><div class="film-hole"></div>
  <div class="film-hole"></div><div class="film-hole"></div><div class="film-hole"></div>
  <div class="film-hole"></div><div class="film-hole"></div><div class="film-hole"></div>
</div>
<div class="film-strip-right">
  <div class="film-hole"></div><div class="film-hole"></div><div class="film-hole"></div>
  <div class="film-hole"></div><div class="film-hole"></div><div class="film-hole"></div>
  <div class="film-hole"></div><div class="film-hole"></div><div class="film-hole"></div>
  <div class="film-hole"></div><div class="film-hole"></div><div class="film-hole"></div>
  <div class="film-hole"></div><div class="film-hole"></div><div class="film-hole"></div>
</div>
""", unsafe_allow_html=True)

# =============================
# STATE + ROUTING
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None
if "home_category" not in st.session_state:
    st.session_state.home_category = "trending"

qp_view = st.query_params.get("view")
qp_id   = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except: 
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=60)
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def sec_head(num: str, title: str):
    st.markdown(f"""
    <div class="sec-head">
      <div class="sec-num">{num}</div>
      <div class="sec-title">{title}</div>
      <div class="sec-accent"></div>
    </div>
    """, unsafe_allow_html=True)


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.markdown("<div style='font-family:IBM Plex Mono,monospace;font-size:0.8rem;color:rgba(232,228,220,0.35);padding:2rem 0;'>// NO RESULTS FOUND</div>", unsafe_allow_html=True)
        return

    rows = (len(cards) + cols - 1) // cols
    idx  = 0
    for r in range(rows):
        colset = st.columns(cols, gap="small")
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]; idx += 1
            tmdb_id = m.get("tmdb_id")
            title   = m.get("title", "Untitled")
            poster  = m.get("poster_url")

            with colset[c]:
                img_html = (
                    f"<img src='{poster}' loading='lazy'/>"
                    if poster
                    else "<div class='rh-no-img'>📽</div>"
                )
                st.markdown(f"""
                <div class="rh-card">
                  {img_html}
                  <div class="rh-card-overlay">
                    <div class="rh-card-title">{title}</div>
                    <div class="rh-card-tag">// OPEN RECORD</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("OPEN", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append({
                "tmdb_id": tmdb["tmdb_id"],
                "title":   tmdb.get("title") or x.get("title") or "Untitled",
                "poster_url": tmdb.get("poster_url"),
            })
    return cards


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    keyword_l = keyword.strip().lower()
    if isinstance(data, dict) and "results" in data:
        raw_items = []
        for m in data.get("results") or []:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id": int(tmdb_id), "title": title,
                "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                "release_date": m.get("release_date", ""),
            })
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title   = (m.get("title") or "").strip()
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id": int(tmdb_id), "title": title,
                "poster_url": m.get("poster_url"),
                "release_date": m.get("release_date", ""),
            })
    else:
        return [], []

    matched    = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year  = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards


# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.markdown("""
    <div style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;letter-spacing:0.12em;
    color:#00f5ff;text-shadow:0 0 12px rgba(0,245,255,0.5);margin-bottom:1rem;'>
    📽 REELHAUS</div>
    """, unsafe_allow_html=True)
    if st.button("[ HOME ]"):
        goto_home()
    st.markdown("---")
    st.markdown("<div style='font-family:IBM Plex Mono,monospace;font-size:0.62rem;letter-spacing:0.2em;color:rgba(0,245,255,0.5);margin-bottom:0.5rem;'>// GRID WIDTH</div>", unsafe_allow_html=True)
    grid_cols = st.slider("", 4, 8, 6, label_visibility="collapsed")


# =============================
# TOPBAR
# =============================
st.markdown("""
<div class="topbar">
  <div>
    <div class="logo-mark"><span class="neon-r">R</span>EELHAUS</div>
    <div class="logo-sub">Film Discovery System v1.0</div>
  </div>
  <div class="topbar-right neon-blink">
    SYSTEM <span>ONLINE</span><br/>
    <span style='color:rgba(232,228,220,0.35);'>CATALOGUE LOADED</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":

    # Search input
    _, sc, _ = st.columns([1, 4, 1])
    with sc:
        typed = st.text_input(
            "search",
            placeholder="SEARCH",
            label_visibility="collapsed",
        )

    if typed.strip():
        if len(typed.strip()) < 2:
            st.markdown("<div style='font-family:IBM Plex Mono,monospace;font-size:0.75rem;color:rgba(0,245,255,0.4);'>// MIN 2 CHARS REQUIRED</div>", unsafe_allow_html=True)
        else:
            data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})
            if err or data is None:
                st.error(f"SEARCH ERROR: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(data, typed.strip(), limit=24)

                if suggestions:
                    _, sel_col, _ = st.columns([1, 4, 1])
                    with sel_col:
                        labels   = ["SELECT FROM RESULTS"] + [s[0] for s in suggestions]
                        selected = st.selectbox("", labels, index=0, label_visibility="collapsed")
                        if selected != "SELECT FROM RESULTS":
                            label_to_id = {s[0]: s[1] for s in suggestions}
                            goto_details(label_to_id[selected])
                else:
                    st.info("NO MATCHES — TRY ANOTHER QUERY")

                sec_head("01", f'RESULTS FOR "{typed.strip().upper()}"')
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")
        st.stop()

    # Category selector
    categories  = ["trending", "popular", "top_rated", "now_playing", "upcoming"]
    cat_labels  = {
        "trending":   "🔥 Trending",
        "popular":    "⭐ Popular",
        "top_rated":  "🏆 Top Rated",
        "now_playing":"🎭 Now Playing",
        "upcoming":   "📅 Upcoming",
    }
    # Render HTML pills (cosmetic) then actual buttons
    pill_html = '<div class="cat-strip">'
    for cat in categories:
        cls = "cat-item active" if cat == st.session_state.home_category else "cat-item"
        pill_html += f'<div class="{cls}">{cat_labels[cat]}</div>'
    pill_html += '</div>'
    st.markdown(pill_html, unsafe_allow_html=True)

    cat_cols = st.columns(len(categories))
    for i, cat in enumerate(categories):
        with cat_cols[i]:
            if st.button(cat_labels[cat], key=f"cat_{cat}", use_container_width=True):
                st.session_state.home_category = cat
                st.rerun()

    sec_head("01", cat_labels.get(st.session_state.home_category, "MOVIES").upper())

    home_cards, err = api_get_json(
        "/home", params={"category": st.session_state.home_category, "limit": 24}
    )
    if err or not home_cards:
        st.error(f"FEED ERROR: {err or 'UNKNOWN'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")


# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("NO RECORD SELECTED")
        if st.button("[ BACK TO HOME ]"):
            goto_home()
        st.stop()

    st.markdown('<div class="back-wrap">', unsafe_allow_html=True)
    if st.button("← BACK"):
        goto_home()
    st.markdown("</div>", unsafe_allow_html=True)

    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"LOAD ERROR: {err or 'UNKNOWN'}")
        st.stop()

    title   = data.get("title", "UNKNOWN")
    release = data.get("release_date", "")
    year    = release[:4] if release else ""
    genres  = data.get("genres", [])

    # Backdrop
    if data.get("backdrop_url"):
        st.markdown(f"""
        <div class="d-backdrop-wrap">
          <img src="{data['backdrop_url']}" />
          <div class="d-backdrop-gradient"></div>
          <div class="d-backdrop-text">
            <div class="d-eyebrow">// NOW VIEWING</div>
            <div class="d-title">{title.upper()}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Poster + Info
    left, right = st.columns([1, 2.5], gap="large")

    with left:
        if data.get("poster_url"):
            st.markdown('<div class="d-poster-frame">', unsafe_allow_html=True)
            st.image(data["poster_url"], use_column_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='text-align:center;font-size:5rem;color:rgba(0,245,255,0.1);padding:5rem 0;'>📽</div>", unsafe_allow_html=True)

    with right:
        badges = ""
        if year:
            badges += f'<span class="d-badge">{year}</span>'
        for g in genres:
            badges += f'<span class="d-badge">{g["name"].upper()}</span>'
        if data.get("vote_average"):
            badges += f'<span class="d-badge magenta">★ {round(data["vote_average"],1)}</span>'
        if data.get("runtime"):
            badges += f'<span class="d-badge magenta">{data["runtime"]} MIN</span>'

        st.markdown(f"""
        <div class="d-info-panel">
          <div class="d-title-sm">{title.upper()}</div>
          <div class="d-meta-row">{badges}</div>
          <div class="d-rule"></div>
          <div class="d-overview">{data.get('overview') or '// NO SYNOPSIS AVAILABLE.'}</div>
        </div>
        """, unsafe_allow_html=True)

    # Recommendations
    sec_head("02", "SIGNAL MATCH — CONTENT SIMILARITY")

    rec_title = (data.get("title") or "").strip()
    if rec_title:
        bundle, err2 = api_get_json(
            "/movie/search",
            params={"query": rec_title, "tfidf_top_n": 12, "genre_limit": 12},
        )

        if not err2 and bundle:
            poster_grid(
                to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
                cols=grid_cols,
                key_prefix="details_tfidf",
            )
            sec_head("03", "GENRE CLUSTER — MORE LIKE THIS")
            poster_grid(
                bundle.get("genre_recommendations", []),
                cols=grid_cols,
                key_prefix="details_genre",
            )
        else:
            genre_only, err3 = api_get_json(
                "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
            )
            if not err3 and genre_only:
                poster_grid(genre_only, cols=grid_cols, key_prefix="details_genre_fallback")
            else:
                st.warning("// NO RECOMMENDATIONS IN DATABASE")
    else:
        st.warning("// TITLE UNAVAILABLE — CANNOT COMPUTE MATCHES")
