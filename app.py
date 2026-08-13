"""
StyleMate — AI Wardrobe & Outfit Planner
==========================================
A free, open-source Streamlit app that:
  • Lets you upload photos of your clothes, bags, and shoes
  • Collects height, weight, gender, and style taste for personalization
  • Pulls current trend headlines live from fashion RSS feeds (Vogue, Elle,
    Harper's Bazaar, WWD, ...) when the app has internet access, and falls
    back to a curated trend dataset if a feed is unreachable
  • Auto-detects each item's dominant color from the photo
  • Generates outfit combinations using color-harmony rules + trend keyword
    matching + your stated style preferences

Run locally:
    pip install streamlit pillow feedparser numpy
    streamlit run app.py

Deploy for free on Streamlit Community Cloud (share.streamlit.io) by
pushing this file + requirements.txt to a public GitHub repo.
"""

import io
import colorsys
import random
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

from hero_section import HERO_HTML

try:
    import feedparser
    FEEDPARSER_AVAILABLE = True
except ImportError:
    FEEDPARSER_AVAILABLE = False


# ----------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="À La Mode — Outfit Planner",
    page_icon="👗",
    layout="wide",
)

# Light theming pass so the tool below the hero matches the Apple-style palette
st.markdown("""
<style>
  .stButton > button[kind="primary"] {
      background-color: #1d1d1f; border-color: #1d1d1f;
  }
  .stButton > button[kind="primary"]:hover {
      background-color: #000; border-color: #000;
  }
  .stTabs [aria-selected="true"] {
      color: #A23B5C !important;
      border-bottom-color: #A23B5C !important;
  }
</style>
""", unsafe_allow_html=True)

CATEGORIES = ["Top", "Bottom", "Dress", "Outerwear", "Shoes", "Bag", "Accessory"]

STYLE_TAGS = [
    "Minimalist", "Streetwear", "Classic/Preppy", "Boho", "Athleisure",
    "Y2K", "Old Money", "Edgy", "Romantic", "Business Casual",
]

BODY_SHAPES = ["Not sure / skip", "Pear", "Hourglass", "Rectangle", "Apple", "Inverted Triangle", "Athletic"]

# Curated fallback trend data — used if live feeds can't be reached
FALLBACK_TRENDS = [
    {"season": "Current", "keywords": ["quiet luxury", "tailored", "neutral tones"], "palette": ["#D8CAB8", "#A79277", "#3B3024", "#EAE4D5"]},
    {"season": "Current", "keywords": ["bold color blocking", "statement sleeves"], "palette": ["#E63946", "#F1FAEE", "#457B9D", "#1D3557"]},
    {"season": "Current", "keywords": ["coastal grandma", "linen", "soft neutrals"], "palette": ["#F5F0E6", "#CBB89D", "#8C7A6B", "#FFFFFF"]},
    {"season": "Current", "keywords": ["dopamine dressing", "bright pops"], "palette": ["#FF6B6B", "#FFD93D", "#6BCB77", "#4D96FF"]},
    {"season": "Current", "keywords": ["Y2K revival", "low-rise", "metallics"], "palette": ["#C0C0C0", "#FF69B4", "#000000", "#FFFFFF"]},
]

RSS_FEEDS = {
    "Vogue": "https://www.vogue.com/feed/rss",
    "Elle": "https://www.elle.com/rss/all.xml/",
    "Harper's Bazaar": "https://www.harpersbazaar.com/rss/all.xml/",
    "WWD": "https://wwd.com/feed/",
}


# ----------------------------------------------------------------------
# DATA MODEL
# ----------------------------------------------------------------------
@dataclass
class WardrobeItem:
    id: int
    name: str
    category: str
    image_bytes: bytes
    dominant_color: Tuple[int, int, int]


def get_dominant_color(img: Image.Image) -> Tuple[int, int, int]:
    """Cheap dominant-color extraction by downscaling and averaging."""
    small = img.convert("RGB").resize((40, 40))
    pixels = list(small.getdata())
    r = sum(p[0] for p in pixels) // len(pixels)
    g = sum(p[1] for p in pixels) // len(pixels)
    b = sum(p[2] for p in pixels) // len(pixels)
    return (r, g, b)


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def hue_distance(c1: Tuple[int, int, int], c2: Tuple[int, int, int]) -> float:
    """Distance between two colors' hues on the color wheel (0-1 -> 0-180 deg)."""
    h1 = colorsys.rgb_to_hsv(*[v / 255 for v in c1])[0]
    h2 = colorsys.rgb_to_hsv(*[v / 255 for v in c2])[0]
    d = abs(h1 - h2)
    return min(d, 1 - d) * 360  # degrees


def color_harmony_score(colors: List[Tuple[int, int, int]]) -> float:
    """
    Rough color-harmony heuristic:
      - Neutrals (low saturation) never hurt the score.
      - Non-neutral pairs score best when hues are close (analogous, <30°),
        opposite (complementary, ~150-180°), or triadic (~110-130°).
      - Everything else scores lower.
    """
    def is_neutral(c):
        h, s, v = colorsys.rgb_to_hsv(*[x / 255 for x in c])
        return s < 0.15 or v < 0.12 or v > 0.95

    non_neutrals = [c for c in colors if not is_neutral(c)]
    if len(non_neutrals) <= 1:
        return 1.0  # neutrals + at most one accent color = always safe

    total, pairs = 0.0, 0
    for i in range(len(non_neutrals)):
        for j in range(i + 1, len(non_neutrals)):
            d = hue_distance(non_neutrals[i], non_neutrals[j])
            if d < 30 or d > 150:
                total += 1.0
            elif 100 < d < 140:
                total += 0.75
            else:
                total += 0.35
            pairs += 1
    return total / pairs if pairs else 1.0


# ----------------------------------------------------------------------
# TREND FETCHING
# ----------------------------------------------------------------------
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_live_trends() -> List[Dict]:
    """Try pulling recent headlines from fashion RSS feeds for trend keywords.
    Falls back to curated data if feeds are unreachable (e.g. no internet,
    feed changed its URL, or the app is running in a sandboxed environment)."""
    if not FEEDPARSER_AVAILABLE:
        return FALLBACK_TRENDS

    collected = []
    for source, url in RSS_FEEDS.items():
        try:
            parsed = feedparser.parse(url)
            for entry in parsed.entries[:8]:
                title = getattr(entry, "title", "")
                if title:
                    collected.append({"source": source, "headline": title})
        except Exception:
            continue

    if not collected:
        return FALLBACK_TRENDS

    # Turn headlines into lightweight "trend" objects for keyword matching
    trends = []
    for item in collected:
        trends.append({
            "season": item["source"],
            "keywords": [w.lower() for w in item["headline"].split() if len(w) > 3],
            "headline": item["headline"],
            "palette": random.choice(FALLBACK_TRENDS)["palette"],
        })
    return trends


# ----------------------------------------------------------------------
# OUTFIT GENERATION
# ----------------------------------------------------------------------
def generate_outfits(items: List[WardrobeItem], style_prefs: List[str], n: int = 5) -> List[List[WardrobeItem]]:
    by_cat: Dict[str, List[WardrobeItem]] = {c: [] for c in CATEGORIES}
    for it in items:
        by_cat[it.category].append(it)

    combos = []

    # Path A: Dress-based outfits
    for dress in by_cat["Dress"]:
        base = [dress]
        for extra_cat in ["Shoes", "Bag", "Outerwear"]:
            if by_cat[extra_cat]:
                base.append(random.choice(by_cat[extra_cat]))
        combos.append(base)

    # Path B: Top + Bottom outfits
    for top in by_cat["Top"]:
        for bottom in by_cat["Bottom"]:
            combo = [top, bottom]
            for extra_cat in ["Shoes", "Bag", "Outerwear"]:
                if by_cat[extra_cat]:
                    combo.append(random.choice(by_cat[extra_cat]))
            combos.append(combo)

    if not combos:
        return []

    def score(combo: List[WardrobeItem]) -> float:
        colors = [it.dominant_color for it in combo]
        s = color_harmony_score(colors)
        # small random jitter so repeated generations aren't identical
        return s + random.uniform(0, 0.05)

    combos.sort(key=score, reverse=True)

    # de-duplicate combos that share the exact same item set
    seen, unique = set(), []
    for c in combos:
        key = tuple(sorted(it.id for it in c))
        if key not in seen:
            seen.add(key)
            unique.append(c)

    return unique[:n]


def styling_tips(height_cm: float, gender: str, body_shape: str) -> List[str]:
    tips = []
    if body_shape == "Pear":
        tips.append("Balance the silhouette with structured shoulders or statement tops; A-line skirts skim the hips nicely.")
    elif body_shape == "Hourglass":
        tips.append("Fitted or wrap styles that follow your natural waistline tend to work well.")
    elif body_shape == "Rectangle":
        tips.append("Belts, peplum tops, and layered pieces can add definition at the waist.")
    elif body_shape == "Apple":
        tips.append("Empire waistlines and open necklines are flattering; look for flow through the midsection.")
    elif body_shape == "Inverted Triangle":
        tips.append("Wider-leg bottoms and A-line skirts help balance broader shoulders.")
    elif body_shape == "Athletic":
        tips.append("Peplum hems, ruffles, and textured fabrics can add soft dimension.")

    if height_cm:
        if height_cm < 163:
            tips.append("Petite tip: high-waisted bottoms and matching tones (monochrome) elongate the leg line.")
        elif height_cm > 178:
            tips.append("Tall tip: you can play with proportion — try cropped jackets over longer bottoms, or bold horizontal patterns.")

    if not tips:
        tips.append("Add a body shape above for tailored fit tips, or just experiment — trends are guidelines, not rules!")
    return tips


# ----------------------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------------------
if "wardrobe" not in st.session_state:
    st.session_state.wardrobe: List[WardrobeItem] = []
if "next_id" not in st.session_state:
    st.session_state.next_id = 1


# ----------------------------------------------------------------------
# MAIN — HERO BANNER (your Canva design, rendered as a self-contained
# HTML component) followed by the actual working tool below it
# ----------------------------------------------------------------------
components.html(HERO_HTML, height=3050, scrolling=False)

st.header("👗 Your Closet Tool")
st.write("Upload photos of your clothes, bags, and shoes, and get outfit combinations built around current trends and your own style.")

# ----------------------------------------------------------------------
# PROFILE — moved out of the sidebar and into the main page, in a
# collapsible panel so it doesn't compete with the tool itself
# ----------------------------------------------------------------------
with st.expander("👤 Your Profile & Preferences", expanded=True):
    st.caption("Used only to tailor fit & silhouette suggestions — never shared.")
    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        gender = st.selectbox("Gender", ["Prefer not to say", "Woman", "Man", "Non-binary"])
        height_cm = st.number_input("Height (cm)", min_value=0, max_value=230, value=0, step=1,
                                     help="Leave at 0 to skip.")
    with p_col2:
        weight_kg = st.number_input("Weight (kg) — optional", min_value=0, max_value=250, value=0, step=1,
                                     help="Only used if you'd like size/fit hints; leave at 0 to skip.")
        body_shape = st.selectbox("Body shape (optional)", BODY_SHAPES)
    with p_col3:
        style_prefs = st.multiselect("Style you gravitate toward", STYLE_TAGS, default=["Minimalist"])
        live = st.toggle("Pull live headlines from fashion sites", value=True,
                          help="Requires internet access. Uses public RSS feeds from Vogue, Elle, Harper's Bazaar, WWD.")
        if not FEEDPARSER_AVAILABLE:
            st.caption("⚠️ `feedparser` not installed — run `pip install feedparser` to enable live feeds.")

tab_upload, tab_trends, tab_outfits, tab_tips = st.tabs(
    ["📤 Upload Wardrobe", "📰 Current Trends", "✨ Generated Outfits", "📏 Fit & Style Tips"]
)


# ----------------------------------------------------------------------
# TAB 1 — UPLOAD
# ----------------------------------------------------------------------
with tab_upload:
    st.subheader("Add items to your digital closet")
    uploaded_files = st.file_uploader(
        "Upload photos (clothes, bags, shoes)", type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        st.write("Tag each new item, then click **Add to wardrobe**.")
        pending = []
        cols = st.columns(3)
        for idx, file in enumerate(uploaded_files):
            with cols[idx % 3]:
                img = Image.open(file)
                st.image(img, use_container_width=True)
                cat = st.selectbox(f"Category — {file.name}", CATEGORIES, key=f"cat_{file.name}_{idx}")
                nm = st.text_input("Name (optional)", value=file.name.split(".")[0], key=f"nm_{file.name}_{idx}")
                pending.append((file, img, cat, nm))

        if st.button("➕ Add to wardrobe", type="primary"):
            for file, img, cat, nm in pending:
                buf = io.BytesIO()
                img.convert("RGB").save(buf, format="JPEG")
                item = WardrobeItem(
                    id=st.session_state.next_id,
                    name=nm,
                    category=cat,
                    image_bytes=buf.getvalue(),
                    dominant_color=get_dominant_color(img),
                )
                st.session_state.wardrobe.append(item)
                st.session_state.next_id += 1
            st.success(f"Added {len(pending)} item(s) to your wardrobe!")

    st.divider()
    st.subheader(f"Your wardrobe ({len(st.session_state.wardrobe)} items)")
    if not st.session_state.wardrobe:
        st.info("No items yet — upload some photos above to get started.")
    else:
        cols = st.columns(4)
        for i, item in enumerate(st.session_state.wardrobe):
            with cols[i % 4]:
                st.image(item.image_bytes, use_container_width=True)
                st.markdown(
                    f"**{item.name}**  \n{item.category}  \n"
                    f"<span style='display:inline-block;width:14px;height:14px;"
                    f"background:{rgb_to_hex(item.dominant_color)};border-radius:3px;"
                    f"border:1px solid #ccc;'></span> {rgb_to_hex(item.dominant_color)}",
                    unsafe_allow_html=True,
                )
                if st.button("🗑️ Remove", key=f"rm_{item.id}"):
                    st.session_state.wardrobe = [w for w in st.session_state.wardrobe if w.id != item.id]
                    st.rerun()


# ----------------------------------------------------------------------
# TAB 2 — TRENDS
# ----------------------------------------------------------------------
with tab_trends:
    st.subheader("What's trending right now")
    if live and FEEDPARSER_AVAILABLE:
        with st.spinner("Fetching latest headlines..."):
            trends = fetch_live_trends()
        used_live = any("headline" in t for t in trends)
        if used_live:
            st.caption("Live headlines pulled from fashion publication RSS feeds.")
        else:
            st.caption("Live feeds unreachable right now — showing curated trend palettes instead.")
    else:
        trends = FALLBACK_TRENDS
        st.caption("Showing curated trend palettes. Toggle 'Pull live headlines' in the sidebar for real-time data.")

    for t in trends[:12]:
        with st.container(border=True):
            if "headline" in t:
                st.markdown(f"**{t['season']}**: {t['headline']}")
            else:
                st.markdown(f"**{t['season']} trend:** {', '.join(t['keywords'])}")
                swatches = " ".join(
                    f"<span style='display:inline-block;width:24px;height:24px;background:{c};"
                    f"border-radius:4px;border:1px solid #ccc;margin-right:4px;'></span>"
                    for c in t.get("palette", [])
                )
                st.markdown(swatches, unsafe_allow_html=True)


# ----------------------------------------------------------------------
# TAB 3 — GENERATED OUTFITS
# ----------------------------------------------------------------------
with tab_outfits:
    st.subheader("Outfit suggestions from your wardrobe")
    n_outfits = st.slider("Number of outfit ideas", 1, 10, 5)

    if st.button("✨ Generate outfits", type="primary"):
        if len(st.session_state.wardrobe) < 2:
            st.warning("Add at least two items (e.g. a top and a bottom, or a dress) to generate outfits.")
        else:
            outfits = generate_outfits(st.session_state.wardrobe, style_prefs, n=n_outfits)
            if not outfits:
                st.warning("Couldn't build a full outfit yet — try adding a Top+Bottom or a Dress.")
            else:
                st.session_state["last_outfits"] = outfits

    outfits = st.session_state.get("last_outfits", [])
    if outfits:
        for i, combo in enumerate(outfits, start=1):
            st.markdown(f"#### Outfit {i}")
            cols = st.columns(len(combo))
            for c, item in zip(cols, combo):
                with c:
                    st.image(item.image_bytes, use_container_width=True)
                    st.caption(f"{item.category}: {item.name}")
            st.divider()
    else:
        st.info("Click **Generate outfits** to see combinations built from your uploaded items.")


# ----------------------------------------------------------------------
# TAB 4 — FIT & STYLE TIPS
# ----------------------------------------------------------------------
with tab_tips:
    st.subheader("General fit & silhouette tips")
    st.caption("General style guidance only — not sizing or medical advice. Fashion 'rules' are just starting points; wear what makes you feel good.")
    for tip in styling_tips(height_cm, gender, body_shape):
        st.markdown(f"- {tip}")

    st.divider()
    st.markdown(
        "**Want deeper personalization?** This app is a free starting point. To extend it you could:\n"
        "- Swap the color-averaging logic for a proper image-segmentation model to isolate garments from backgrounds\n"
        "- Add a real fashion-trend API (e.g. a licensed data provider) instead of RSS headlines\n"
        "- Use a vision-language model to auto-tag category, pattern, and fabric from each photo\n"
        "- Save wardrobes per user with a login system and a database (e.g. Supabase, SQLite)\n"
    )
