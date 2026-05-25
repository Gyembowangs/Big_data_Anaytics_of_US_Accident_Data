import streamlit as st
from PIL import Image
import os

# Page config 
st.set_page_config(
    page_title="US Accident Analytics Dashboard",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Path helper
BASE = os.path.dirname(__file__)
IMG  = os.path.join(BASE, "image")

def img(name):
    path = os.path.join(IMG, name)
    return Image.open(path)

# Custom CSS
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Global background ── */
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1526 50%, #0a1220 100%);
    color: #e2e8f0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1c35 0%, #0a1628 100%);
    border-right: 1px solid rgba(99,179,237,0.15);
}
[data-testid="stSidebar"] .stMarkdown p {
    color: #94a3b8;
}

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #0f2044 0%, #1a3a6b 50%, #0f2044 100%);
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 20px;
    padding: 3rem 2.5rem;
    margin-bottom: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle at 60% 40%, rgba(99,179,237,0.07) 0%, transparent 60%);
    pointer-events: none;
}
.hero h1 {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(90deg, #63b3ed, #90cdf4, #fbb6ce);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.hero p {
    color: #94a3b8;
    font-size: 1.1rem;
    margin: 0;
}

/* ── KPI cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.2rem;
    margin-bottom: 2rem;
}
.kpi-card {
    background: linear-gradient(135deg, #0f1e38 0%, #162847 100%);
    border: 1px solid rgba(99,179,237,0.18);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    text-align: center;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    position: relative;
    overflow: hidden;
}
.kpi-card::after {
    content: "";
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 0 0 16px 16px;
}
.kpi-card.blue::after   { background: linear-gradient(90deg, #3182ce, #63b3ed); }
.kpi-card.red::after    { background: linear-gradient(90deg, #e53e3e, #fc8181); }
.kpi-card.green::after  { background: linear-gradient(90deg, #38a169, #68d391); }
.kpi-card.amber::after  { background: linear-gradient(90deg, #d69e2e, #f6e05e); }
.kpi-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(99,179,237,0.12); }
.kpi-icon  { font-size: 2.2rem; margin-bottom: 0.5rem; }
.kpi-value {
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.3rem;
    background: linear-gradient(90deg, #63b3ed, #90cdf4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.kpi-label { color: #94a3b8; font-size: 0.82rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.08em; }

/* Section headers*/
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 2.2rem 0 1.2rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid rgba(99,179,237,0.15);
}
.section-header h2 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0;
}
.section-icon {
    font-size: 1.5rem;
    background: linear-gradient(135deg, #1a3a6b, #0f2044);
    border: 1px solid rgba(99,179,237,0.25);
    border-radius: 10px;
    width: 44px; height: 44px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}

/*  Plot card wrapper */
.plot-card {
    background: linear-gradient(135deg, #0f1e38 0%, #0d1a30 100%);
    border: 1px solid rgba(99,179,237,0.15);
    border-radius: 16px;
    padding: 1.2rem;
    margin-bottom: 1.2rem;
    transition: box-shadow 0.25s ease;
}
.plot-card:hover { box-shadow: 0 8px 32px rgba(99,179,237,0.1); }
.plot-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #63b3ed;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 0.8rem;
}

/* ── Insight boxes ── */
.insight {
    background: linear-gradient(135deg, #0f1e38, #0a1a2e);
    border-left: 3px solid #63b3ed;
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    color: #cbd5e0;
    line-height: 1.6;
}
.insight strong { color: #90cdf4; }
.insight.red    { border-left-color: #fc8181; }
.insight.green  { border-left-color: #68d391; }
.insight.amber  { border-left-color: #f6e05e; }

/* Sidebar nav buttons */
div[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: transparent;
    border: 1px solid rgba(99,179,237,0.15);
    border-radius: 10px;
    color: #94a3b8;
    font-size: 0.9rem;
    font-weight: 500;
    text-align: left;
    padding: 0.6rem 1rem;
    margin-bottom: 0.35rem;
    transition: all 0.2s;
}
/* ── THE HOVER STATE ── */
/* Using multiple selectors and !important to ensure it applies */
section[data-testid="stSidebar"] div.stButton > button:hover {
    background-color: #63b3ed !important; /* Vibrant Blue background on hover */
    color: #ffffff !important;           /* White text on hover */
    border-color: #90cdf4 !important;    /* Lighter blue border */
    transform: scale(1.02) !important;   /* Subtle pop effect */
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3) !important;
}

/* Active/Focus state for the clicked button */
section[data-testid="stSidebar"] div.stButton > button:active,
section[data-testid="stSidebar"] div.stButton > button:focus {
    background-color: #3182ce !important;
    color: white !important;
}

/* Divider */
hr { border-color: rgba(99,179,237,0.1); }

/* Footer */
.footer {
    text-align: center;
    padding: 2rem;
    color: #4a5568;
    font-size: 0.8rem;
    border-top: 1px solid rgba(99,179,237,0.1);
    margin-top: 3rem;
}
</style>
""", unsafe_allow_html=True)


# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.5rem 0 1rem;">
        <div style="font-size:2.8rem;">🚨</div>
        <div style="font-size:1.1rem; font-weight:700; color:#e2e8f0; line-height:1.3;">US Accident<br>Analytics</div>
        <div style="font-size:0.75rem; color:#4a5568; margin-top:0.3rem;">2016 – 2023 · 7.7M Records</div>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-size:0.72rem; color:#4a5568; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.5rem;'>Navigation</p>", unsafe_allow_html=True)

    pages = {
        "🏠  Overview":            "Overview",
        "📅  Temporal Analysis":   "Temporal",
        "🗺️  Geographic Analysis": "Geographic",
        "⚠️  Severity Analysis":   "Severity",
        "🌦️  Weather & Environment":"Weather",
    }

    if "page" not in st.session_state:
        st.session_state.page = "Overview"

    for label, key in pages.items():
        if st.button(label, key=f"nav_{key}"):
            st.session_state.page = key

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="padding: 0.8rem; background: #ffffff;
         border-radius:10px; border:1px solid rgba(99,179,237,0.15);">
        <p style="font-size:0.78rem; color:#63b3ed; font-weight:600; margin:0 0 0.4rem;">📊 Dataset Info</p>
        <p style="font-size:0.75rem; color:#94a3b8; margin:0; line-height:1.6;">
        Source: US Accidents (Kaggle)<br>
        Records: ~7.7 Million<br>
        Period: 2016 – 2023<br>
        States: 49 US States<br>
        Size: 3.7 GB
        </p>
    </div>
    """, unsafe_allow_html=True)

page = st.session_state.page


# PAGE 1 — OVERVIEW
if page == "Overview":

    st.markdown("""
    <div class="hero">
        <h1>🚨 US Traffic Accident Analytics</h1>
        <p>Comprehensive big-data analysis of 7.7 million traffic accidents across 49 US states (2016–2023)</p>
    </div>
    """, unsafe_allow_html=True)

    # KPI Cards
    st.markdown("""
    <div class="kpi-grid">
        <div class="kpi-card blue">
            <div class="kpi-icon">📋</div>
            <div class="kpi-value">7.7M+</div>
            <div class="kpi-label">Total Accidents</div>
        </div>
        <div class="kpi-card red">
            <div class="kpi-icon">🏴</div>
            <div class="kpi-value">49</div>
            <div class="kpi-label">States Covered</div>
        </div>
        <div class="kpi-card green">
            <div class="kpi-icon">📅</div>
            <div class="kpi-value">8 Years</div>
            <div class="kpi-label">Time Span (2016–2023)</div>
        </div>
        <div class="kpi-card amber">
            <div class="kpi-icon">⚡</div>
            <div class="kpi-value">1,762k</div>
            <div class="kpi-label">Peak Year (2022)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Two columns: Yearly trend + State map
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="plot-card"><p class="plot-title">📈 Yearly Accident Trend (2016–2023)</p>', unsafe_allow_html=True)
        st.image(img("Yearly_Accident_Trend.png"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="plot-card"><p class="plot-title">🗺️ Accident Count by State</p>', unsafe_allow_html=True)
        st.image(img("Accident_count_by_state.png"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Key Insights
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">💡</div>
        <h2>Key Insights</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="insight">
            📈 <strong>Rapid Growth:</strong> Accidents rose from 411k in 2016 to a peak of 1.76M in 2022 — a <strong>329% increase</strong> over 6 years, driven by better reporting and increased road usage.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="insight red">
            🏆 <strong>California Leads:</strong> CA accounts for the most accidents (~1.75M), followed by Florida and Texas. The top 3 states together represent over <strong>40%</strong> of all US accidents.
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="insight green">
            🕗 <strong>Rush Hour Risk:</strong> The AM rush (7–9am) and PM rush (4–6pm) account for the highest accident volumes daily. Friday is the single most accident-prone weekday.
        </div>
        """, unsafe_allow_html=True)

    # Full hotspot map
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🗺️</div>
        <h2>US Traffic Accident Hotspot Map</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="plot-card"><p class="plot-title">🔴 Geospatial Hotspots — All Severity Levels</p>', unsafe_allow_html=True)
    st.image(img("Us_Traffic_Accident_Hotspots.png"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight amber">
        🌎 <strong>Coastal Concentration:</strong> The Eastern Seaboard, California coast, and I-10/I-20 corridors show the highest accident density.
        Rural interior states (MT, ND, WY) have significantly fewer accidents. Severity 2 (Moderate) dominates nationally.
    </div>
    """, unsafe_allow_html=True)


# PAGE 2 — TEMPORAL ANALYSIS
elif page == "Temporal":

    st.markdown("""
    <div class="hero">
        <h1>📅 Temporal Analysis</h1>
        <p>When do accidents happen? Explore trends across years, months, days and hours.</p>
    </div>
    """, unsafe_allow_html=True)

    # Row 1: Yearly + Monthly
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📈</div>
        <h2>Long-Term & Seasonal Trends</h2>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="plot-card"><p class="plot-title">📈 Yearly Accident Trend (2016–2023)</p>', unsafe_allow_html=True)
        st.image(img("Yearly_Accident_Trend.png"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="insight">
            <strong>2016→2022:</strong> Steady upward trajectory peaking at 1.76M in 2022.
            The sharp drop in 2023 reflects partial-year data or improved reporting cutoffs.
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="plot-card"><p class="plot-title">📅 Accidents by Month</p>', unsafe_allow_html=True)
        st.image(img("Accidents_by_Month.png"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="insight amber">
            <strong>Dec & Jan</strong> are the deadliest months (847k & 752k).
            Summer months (Jul) see a dip — possibly due to school breaks reducing commuter traffic.
        </div>
        """, unsafe_allow_html=True)

    # Row 2: Day of week + Hour
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🕐</div>
        <h2>Weekly & Daily Patterns</h2>
    </div>
    """, unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="plot-card"><p class="plot-title">📆 Accidents by Day of Week</p>', unsafe_allow_html=True)
        st.image(img("Accidents_by_Day_of_Week.png"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="insight green">
            <strong>Weekdays dominate</strong> (Mon–Fri ≈ 83.7% of all accidents).
            Saturday (17.7%) is the busiest weekend day. Sunday drops sharply to just 8.7%.
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="plot-card"><p class="plot-title">⏰ Accidents by Hour of Day</p>', unsafe_allow_html=True)
        st.image(img("Accidents_by_Hour_of_Day.png"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="insight red">
            Two clear <strong>rush-hour spikes</strong>: AM rush (7–8am) and PM rush (4–6pm).
            The overnight hours (1–4am) record the fewest accidents of any time of day.
        </div>
        """, unsafe_allow_html=True)

    # Row 3: Hourly line chart
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📉</div>
        <h2>Hourly Accident Curve</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="plot-card"><p class="plot-title">📉 Accidents by Hour of Day — Line View</p>', unsafe_allow_html=True)
    st.image(img("accident_by_hour.png"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight">
        The bimodal distribution is unmistakable — accident frequency mirrors commuter traffic volumes exactly.
        The PM peak (4–5pm) is slightly higher than AM (7–8am), suggesting <strong>fatigue and end-of-day distraction</strong> play a role.
    </div>
    """, unsafe_allow_html=True)


# PAGE 3 — GEOGRAPHIC ANALYSIS
elif page == "Geographic":

    st.markdown("""
    <div class="hero">
        <h1>🗺️ Geographic Analysis</h1>
        <p>Where do accidents cluster? State-level, city-level and hotspot breakdowns across the United States.</p>
    </div>
    """, unsafe_allow_html=True)

    # State choropleth
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🏛️</div>
        <h2>State-Level Overview</h2>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown('<div class="plot-card"><p class="plot-title">🗺️ Accident Count by State (2016–2023)</p>', unsafe_allow_html=True)
        st.image(img("Accident_count_by_state.png"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="plot-card"><p class="plot-title">🏆 Top 10 Accident States</p>', unsafe_allow_html=True)
        st.image(img("top_10_accident_state.png"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight">
        <strong>California (CA)</strong> is the clear leader with ~1.75M accidents, nearly double the second-place Florida (FL, ~875k).
        Texas (TX) ranks 3rd. The top 10 states account for the vast majority of all reported US accidents.
    </div>
    """, unsafe_allow_html=True)

    # City hotspots
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🏙️</div>
        <h2>City-Level Hotspots</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="plot-card"><p class="plot-title">🏙️ Top 10 Accident Hotspot Cities</p>', unsafe_allow_html=True)
    st.image(img("Top 10_Accident_Hotspot_cities.png"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    cols = st.columns(2)
    with cols[0]:
        st.markdown("""
        <div class="insight green">
            <strong>Houston, TX (169k)</strong> is the top accident city, followed by Miami, FL (187k) and Los Angeles, CA (156k).
            All top 10 cities are major metropolitan areas with dense freeway networks.
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown("""
        <div class="insight amber">
            <strong>Charlotte & Raleigh, NC</strong> both appear in the top 10, suggesting North Carolina's rapid urban growth
            has outpaced road safety infrastructure improvements.
        </div>
        """, unsafe_allow_html=True)

    # Full hotspot + severity map
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🔥</div>
        <h2>Geospatial Hotspot & Severity Maps</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="plot-card"><p class="plot-title">🌍 US Traffic Accident Hotspots (Severity-Based)</p>', unsafe_allow_html=True)
    st.image(img("Us_Traffic_Accident_Hotspots.png"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="plot-card"><p class="plot-title">🗺️ Accident Distribution by Severity Level</p>', unsafe_allow_html=True)
    st.image(img("Accident_Distribution_by_Serverity_level.png"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight red">
        The severity maps reveal a stark contrast: <strong>Severity 2 (Moderate)</strong> blankets the entire country with 39,747 hotspot clusters,
        while <strong>Severity 4 (Critical)</strong> is concentrated in just 1,271 very dense urban corridors —
        particularly California's I-5/US-101 and Florida's I-95.
    </div>
    """, unsafe_allow_html=True)


# PAGE 4 — SEVERITY ANALYSIS

elif page == "Severity":

    st.markdown("""
    <div class="hero">
        <h1>⚠️ Severity Analysis</h1>
        <p>Understanding the four severity levels and how time of day, geography and conditions affect crash severity.</p>
    </div>
    """, unsafe_allow_html=True)

    # Severity KPI cards
    st.markdown("""
    <div class="kpi-grid">
        <div class="kpi-card green">
            <div class="kpi-icon">🟢</div>
            <div class="kpi-value">397</div>
            <div class="kpi-label">Severity 1 — Minor</div>
        </div>
        <div class="kpi-card blue">
            <div class="kpi-icon">🔵</div>
            <div class="kpi-value">6.1M+</div>
            <div class="kpi-label">Severity 2 — Moderate</div>
        </div>
        <div class="kpi-card amber">
            <div class="kpi-icon">🟡</div>
            <div class="kpi-value">1.3M+</div>
            <div class="kpi-label">Severity 3 — Serious</div>
        </div>
        <div class="kpi-card red">
            <div class="kpi-icon">🔴</div>
            <div class="kpi-value">1,271</div>
            <div class="kpi-label">Severity 4 — Critical</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Distribution + vs hour
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📊</div>
        <h2>Severity Distribution & Time Patterns</h2>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="plot-card"><p class="plot-title">📊 Severity Distribution</p>', unsafe_allow_html=True)
        st.image(img("siverity_distribution.png"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="insight blue">
            <strong>Severity 2</strong> (Moderate) dominates overwhelmingly — representing ~80% of all accidents.
            Severity 1 is extremely rare (only 397 records), while Severity 4 Critical accounts for ~1,271 cases.
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="plot-card"><p class="plot-title">🕐 Severity vs Hour of Day</p>', unsafe_allow_html=True)
        st.image(img("severity_vs_hour.png"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="insight red">
            All severity levels peak during the <strong>AM (7–8am) and PM (4–6pm) rush hours</strong>.
            Severity 3 (Serious) shows a pronounced mid-day secondary peak, possibly linked to higher-speed rural driving.
        </div>
        """, unsafe_allow_html=True)

    # Geographic severity
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🗺️</div>
        <h2>Geographic Distribution by Severity Level</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="plot-card"><p class="plot-title">🗺️ Accident Distribution by Severity Level — Geospatial</p>', unsafe_allow_html=True)
    st.image(img("Accident_Distribution_by_Serverity_level.png"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="insight green">
            <strong>Severity 1 (Minor):</strong> Sparsely distributed, mostly isolated incidents.
            Only 397 total cases in 8 years — suggesting very minor fender-benders are rarely formally reported.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="insight amber">
            <strong>Severity 3 (Serious):</strong> 8,585 incidents concentrated along major interstate highways,
            especially the I-10 corridor across the South and I-5 in California.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="insight">
            <strong>Severity 2 (Moderate):</strong> The dominant category with 39,747 accidents, covering virtually
            every urban area and corridor in the nation — the backbone of US traffic safety data.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="insight red">
            <strong>Severity 4 (Critical):</strong> 1,271 incidents, tightly clustered in the densest metro areas.
            These are life-altering crashes requiring significant emergency response.
        </div>
        """, unsafe_allow_html=True)


# PAGE 5 — WEATHER & ENVIRONMENT
elif page == "Weather":

    st.markdown("""
    <div class="hero">
        <h1>🌦️ Weather & Environment</h1>
        <p>How do weather conditions, temperature and visibility affect accident frequency and severity?</p>
    </div>
    """, unsafe_allow_html=True)

    # Weather conditions
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">☁️</div>
        <h2>Weather Conditions</h2>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="plot-card"><p class="plot-title">☁️ Top Weather Conditions During Accidents</p>', unsafe_allow_html=True)
        st.image(img("top_weather.png"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="insight amber">
            <strong>Fair weather</strong> accounts for the most accidents (2.5M+) — not because it's more dangerous,
            but because fair weather drives the most traffic. <strong>Overconfidence</strong> in clear conditions
            may also reduce driver caution.
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="plot-card"><p class="plot-title">🌩️ Weather Condition vs Accident Severity</p>', unsafe_allow_html=True)
        st.image(img("weather_condition_vs_severity.png"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="insight red">
            <strong>Clear and fair conditions</strong> dominate Severity 2 accidents.
            However, <strong>light rain and overcast</strong> conditions disproportionately elevate Severity 3 (Serious),
            suggesting wet roads significantly increase crash severity.
        </div>
        """, unsafe_allow_html=True)

    # Temperature + Visibility
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🌡️</div>
        <h2>Environmental Factors</h2>
    </div>
    """, unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="plot-card"><p class="plot-title">🌡️ Temperature Distribution During Accidents</p>', unsafe_allow_html=True)
        st.image(img("temperture_distribution.png"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="insight green">
            Accidents peak around <strong>55–75°F</strong> — typical commuting temperature ranges in spring and fall.
            Both extreme cold (below 20°F) and extreme heat (above 100°F) see fewer accidents,
            likely due to reduced driving activity in harsh conditions.
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="plot-card"><p class="plot-title">👁️ Visibility vs Accident Frequency</p>', unsafe_allow_html=True)
        st.image(img("visibility_vs_accident.png"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="insight">
            An overwhelming <strong>spike at ~10 miles visibility</strong> (standard clear-day reading) confirms that
            most accidents happen in perfect visibility. Low-visibility conditions (under 1 mile)
            represent a small but disproportionately severe subset of accidents.
        </div>
        """, unsafe_allow_html=True)

    # Summary callout
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🧠</div>
        <h2>Environmental Summary</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="insight amber">
            ☀️ <strong>Fair weather paradox:</strong> Most accidents occur in clear conditions — volume-driven,
            not danger-driven. Driver complacency in ideal conditions is a key risk factor.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="insight red">
            🌧️ <strong>Rain amplifies severity:</strong> Even light rain shifts the severity distribution toward
            Severity 3. Wet roads reduce braking efficiency and increase reaction distance significantly.
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="insight green">
            🌡️ <strong>Temperature sweet spot:</strong> The 55–75°F range sees peak accident volumes,
            aligning with peak commuter hours and moderate outdoor activity levels across the US.
        </div>
        """, unsafe_allow_html=True)


# Footer
st.markdown("""
<div class="footer">
    🚨 US Accident Analytics Dashboard &nbsp;|&nbsp; Data: 2016–2023 &nbsp;|&nbsp;
    Built with Streamlit · Big Data Analytics Project
</div>
""", unsafe_allow_html=True)
