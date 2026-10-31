import streamlit as st

PALETTE = ["#6366F1", "#14B8A6", "#F59E0B", "#EC4899", "#38BDF8", "#A78BFA", "#34D399"]

CSS = """
<style>
/* ---- remove Deploy button, menu and footer ---- */
[data-testid="stToolbar"], [data-testid="stAppDeployButton"],
.stDeployButton, .stAppDeployButton, #MainMenu, footer {display: none !important; visibility: hidden !important;}
[data-testid="stHeader"] {background: transparent;}

/* ---- page background ---- */
.stApp {
    background:
        radial-gradient(1100px 560px at 8% -10%, rgba(99,102,241,.22), transparent 60%),
        radial-gradient(900px 500px at 100% 0%, rgba(20,184,166,.16), transparent 55%),
        #0B1020;
}
.block-container {padding-top: 1.6rem; max-width: 1250px;}

/* ---- sidebar ---- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #131A3A 0%, #0E1428 100%);
    border-right: 1px solid rgba(255,255,255,.06);
}
.brand {display:flex; align-items:center; gap:10px; margin-bottom:6px;}
.brand .logo {width:38px; height:38px; border-radius:11px; display:flex; align-items:center; justify-content:center;
    font-size:20px; background:linear-gradient(135deg,#6366F1,#14B8A6);}
.brand .name {font-weight:700; font-size:1.02rem; line-height:1.15;}
.brand .tag {font-size:.74rem; opacity:.65;}

/* ---- hero ---- */
.hero {
    padding: 30px 34px; border-radius: 20px; margin-bottom: 22px;
    background: linear-gradient(120deg, rgba(99,102,241,.95) 0%, rgba(20,184,166,.85) 100%);
    box-shadow: 0 18px 40px rgba(99,102,241,.25);
}
.hero h1 {margin:0; font-size:2.1rem; font-weight:800; color:#fff; letter-spacing:-.5px; padding:0;}
.hero p {margin:8px 0 0 0; font-size:1.02rem; color:rgba(255,255,255,.92);}
.hero .chips {margin-top:16px; display:flex; gap:8px; flex-wrap:wrap;}
.hero .chip {background:rgba(255,255,255,.18); border:1px solid rgba(255,255,255,.28); color:#fff;
    padding:4px 12px; border-radius:999px; font-size:.78rem; font-weight:600;}

/* ---- feature cards (empty state) ---- */
.cards {display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:16px; margin:18px 0;}
.card {padding:20px; border-radius:16px; background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.08);
    transition:transform .15s ease, border-color .15s ease;}
.card:hover {transform:translateY(-3px); border-color:rgba(99,102,241,.7);}
.card .icon {font-size:1.7rem; margin-bottom:8px;}
.card h4 {margin:0 0 6px 0; font-size:1.02rem; font-weight:700;}
.card p {margin:0; font-size:.88rem; opacity:.75;}

/* ---- metric cards ---- */
[data-testid="stMetric"] {
    padding: 16px 18px; border-radius: 16px;
    background: linear-gradient(160deg, rgba(255,255,255,.07), rgba(255,255,255,.02));
    border: 1px solid rgba(255,255,255,.09); border-left: 4px solid #6366F1;
    box-shadow: 0 8px 22px rgba(0,0,0,.25);
}
[data-testid="stMetricLabel"] {opacity:.75;}
[data-testid="stMetricValue"] {font-weight:800;}

/* ---- tabs ---- */
.stTabs [data-baseweb="tab-list"] {gap: 8px; border-bottom: none; flex-wrap: wrap;}
.stTabs [data-baseweb="tab"] {
    height: 42px; padding: 0 18px; border-radius: 999px;
    background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.08); font-weight:600;
}
.stTabs [aria-selected="true"] {background: linear-gradient(120deg,#6366F1,#14B8A6); color:#fff; border-color:transparent;}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {display:none;}

/* ---- buttons, uploader, tables ---- */
.stButton > button, .stDownloadButton > button {
    border-radius: 12px; border: none; font-weight: 700; color:#fff; padding: .55rem 1.2rem;
    background: linear-gradient(120deg,#6366F1,#14B8A6);
    box-shadow: 0 8px 20px rgba(99,102,241,.3); transition: transform .12s ease, filter .12s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {transform: translateY(-2px); filter: brightness(1.08); color:#fff;}
[data-testid="stFileUploader"] section {
    border: 2px dashed rgba(99,102,241,.6); border-radius: 16px; background: rgba(99,102,241,.07);
}
[data-testid="stDataFrame"] {border-radius: 14px; overflow: hidden; border: 1px solid rgba(255,255,255,.08);}
h2, h3 {letter-spacing: -.2px;}
</style>
"""


def apply_style():
    st.markdown(CSS, unsafe_allow_html=True)


def brand_sidebar():
    st.markdown(
        '<div class="brand"><div class="logo">📊</div><div><div class="name">SmartData<br>Cleaner &amp; Analyzer</div>'
        '<div class="tag">Profile · Clean · Analyze</div></div></div>',
        unsafe_allow_html=True,
    )


def hero(title, subtitle, chips=()):
    chip_html = "".join(f'<span class="chip">{c}</span>' for c in chips)
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p><div class="chips">{chip_html}</div></div>',
        unsafe_allow_html=True,
    )


def feature_cards(items):
    html = "".join(
        f'<div class="card"><div class="icon">{i}</div><h4>{t}</h4><p>{d}</p></div>' for i, t, d in items
    )
    st.markdown(f'<div class="cards">{html}</div>', unsafe_allow_html=True)


def style_fig(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E5E7EB"), colorway=PALETTE,
        margin=dict(l=10, r=10, t=50, b=10), title_font=dict(size=16),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,.07)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,.07)", zeroline=False)
    return fig


def show_df(data):
    """Full-width dataframe that works on old and new Streamlit versions."""
    try:
        st.dataframe(data, width="stretch")
    except Exception:
        st.dataframe(data, use_container_width=True)
