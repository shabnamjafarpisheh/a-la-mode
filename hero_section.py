"""
hero_section.py
================
v3 — Apple.com-style design direction, applied to clothes instead of
devices: huge tight-tracked headlines, generous whitespace, alternating
white/black full-width sections, a big edge-to-edge photo under each
headline instead of a product render, and a minimal monochrome sources
grid (segmented-control style filters) instead of colored cards.

Photos are real, freely-licensed Unsplash photos (Unsplash License —
free for commercial use, no attribution required), swapped in for the
device photography Apple would normally use:
  - Thom Bradley: clothing racks
  - Priscilla Du Preez: a coat on a rack, minimal/neutral
  - Meg MacDonald: a stack of folded sweaters
"""

PHOTO_RACKS = "https://images.unsplash.com/photo-1603400521630-9f2de124b33b?fm=jpg&q=80&w=2400&auto=format&fit=crop"
PHOTO_COAT = "https://images.unsplash.com/photo-1604882767135-b41fac508fff?fm=jpg&q=80&w=2400&auto=format&fit=crop"
PHOTO_SWEATERS = "https://images.unsplash.com/photo-1646270968349-dafd9f758e93?fm=jpg&q=80&w=2400&auto=format&fit=crop"

PHOTO_RACKS = "https://images.unsplash.com/photo-1603400521630-9f2de124b33b?fm=jpg&q=80&w=2400&auto=format&fit=crop"
PHOTO_COAT = "https://images.unsplash.com/photo-1604882767135-b41fac508fff?fm=jpg&q=80&w=2400&auto=format&fit=crop"
PHOTO_SWEATERS = "https://images.unsplash.com/photo-1646270968349-dafd9f758e93?fm=jpg&q=80&w=2400&auto=format&fit=crop"
PHOTO_BAG = "https://images.unsplash.com/photo-1598532163257-ae3c6b2524b6?fm=jpg&q=80&w=2400&auto=format&fit=crop"
PHOTO_SHOES = "https://images.unsplash.com/photo-1676379827610-c380c52db0c6?fm=jpg&q=80&w=2400&auto=format&fit=crop"
# All photos: real, free-to-use Unsplash photography (Unsplash License —
# free for commercial use, no attribution required). Credits, in order:
# Thom Bradley, Priscilla Du Preez, Meg MacDonald, Irene Kredenets, Maria Fernanda Pissioli.

SHOWCASE_ITEMS = [
    (PHOTO_RACKS, "The Rack."),
    (PHOTO_COAT, "The Coat."),
    (PHOTO_SWEATERS, "The Knit."),
    (PHOTO_BAG, "The Bag."),
    (PHOTO_SHOES, "The Shoe."),
]

def _showcase_cards():
    cards = []
    for i, (url, label) in enumerate(SHOWCASE_ITEMS):
        cards.append(f'''
        <div class="sc-card" data-i="{i}">
          <div class="sc-photo"><img src="{url}" alt="{label}"></div>
          <p class="sc-label">{label}</p>
        </div>''')
    return "\n".join(cards)

def _showcase_dots():
    return "\n".join(f'<span class="sc-dot" data-i="{i}"></span>' for i in range(len(SHOWCASE_ITEMS)))


SHOWCASE_HTML = f"""
<!doctype html>
<html><head><meta charset="UTF-8"><style>
  * {{ box-sizing: border-box; -webkit-font-smoothing: antialiased; }}
  html, body {{ margin: 0; height: 100%; background: #000; overflow-x: hidden; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", Arial, sans-serif; }}

  #showcase-track {{ position: relative; height: 500vh; }}
  #showcase-sticky {{
    position: sticky; top: 0; height: 100vh; overflow: hidden;
    display: flex; align-items: center; justify-content: center;
    perspective: 1600px; background: #000;
  }}
  .sc-eyebrow {{
    position: absolute; top: 26px; left: 0; right: 0; text-align: center;
    color: #86868b; font-size: .78rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase;
  }}
  .sc-card {{
    position: absolute; width: min(72vw, 520px); text-align: center;
    transform-style: preserve-3d; will-change: transform, opacity;
  }}
  .sc-photo {{
    border-radius: 22px; overflow: hidden; box-shadow: 0 40px 90px rgba(0,0,0,.55);
  }}
  .sc-photo img {{ width: 100%; height: min(46vh, 380px); object-fit: cover; display: block; }}
  .sc-label {{
    color: #fff; font-size: 1.25rem; font-weight: 600; letter-spacing: -.01em; margin: 18px 0 0;
  }}
  .sc-dots {{
    position: absolute; bottom: 30px; left: 0; right: 0; display: flex; justify-content: center; gap: 8px;
  }}
  .sc-dot {{ width: 6px; height: 6px; border-radius: 50%; background: #48484a; transition: background .2s ease, transform .2s ease; }}
  .sc-dot.active {{ background: #fff; transform: scale(1.4); }}
</style></head>
<body>
  <div id="showcase-track">
    <div id="showcase-sticky">
      <p class="sc-eyebrow">The Closet, Up Close</p>
      {_showcase_cards()}
      <div class="sc-dots">{_showcase_dots()}</div>
    </div>
  </div>
<script>
  const track = document.getElementById('showcase-track');
  const cards = Array.from(document.querySelectorAll('.sc-card'));
  const dots = Array.from(document.querySelectorAll('.sc-dot'));
  const STAGES = cards.length;
  const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

  function render() {{
    const rect = track.getBoundingClientRect();
    const total = rect.height - window.innerHeight;
    let progress = total > 0 ? (-rect.top) / total : 0;
    progress = clamp(progress, 0, 1);
    const stageProgress = progress * (STAGES - 1);

    cards.forEach((card, i) => {{
      const local = clamp(stageProgress - i, -1.4, 1.4);
      const rotateY = -55 * clamp(local, -1, 1);
      const translateX = -60 * clamp(local, -1, 1);
      const scale = 1 - 0.18 * Math.min(Math.abs(local), 1);
      const opacity = Math.max(0, 1 - Math.abs(local) * 1.15);
      card.style.transform = `translateX(${{translateX}}%) rotateY(${{rotateY}}deg) scale(${{scale}})`;
      card.style.opacity = opacity;
      card.style.zIndex = 100 - Math.round(Math.abs(local) * 10);
    }});

    const activeIndex = clamp(Math.round(stageProgress), 0, STAGES - 1);
    dots.forEach((d, i) => d.classList.toggle('active', i === activeIndex));
  }}

  let ticking = false;
  window.addEventListener('scroll', () => {{
    if (!ticking) {{
      requestAnimationFrame(() => {{ render(); ticking = false; }});
      ticking = true;
    }}
  }}, {{ passive: true }});
  window.addEventListener('resize', render);
  render();
</script>
</body></html>
"""


SOURCES = [
    ("Vogue", "magazine"), ("Harper's Bazaar", "magazine"), ("Elle", "magazine"),
    ("L'Officiel", "magazine"), ("Numéro", "magazine"), ("Marie Claire", "magazine"),
    ("Porter Magazine", "magazine"), ("The Gentlewoman", "magazine"),
    ("Net-a-Porter", "retailer"), ("Mytheresa", "retailer"), ("Moda Operandi", "retailer"),
    ("Farfetch", "retailer"), ("SSENSE", "retailer"), ("Bergdorf Goodman", "retailer"),
    ("Ralph Lauren", "brand"), ("The Row", "brand"), ("Brunello Cucinelli", "brand"),
    ("Max Mara", "brand"), ("Loro Piana", "brand"), ("Totême", "brand"),
    ("Khaite", "brand"), ("Jil Sander", "brand"), ("Hermès", "brand"), ("Ferragamo", "brand"),
]

def _source_rows():
    rows = []
    for name, cat in SOURCES:
        rows.append(f'<div class="source-cell" data-cat="{cat}">{name}</div>')
    return "\n".join(rows)


HERO_HTML = f"""
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; -webkit-font-smoothing: antialiased; }}
  :root {{
    --ink: #1d1d1f;
    --gray: #6e6e73;
    --line: #d2d2d7;
    --bg-soft: #f5f5f7;
    --accent: #A23B5C;
  }}
  html, body {{ margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", "Helvetica Neue", Arial, sans-serif;
    color: var(--ink); background: #fff; letter-spacing: -0.01em;
  }}
  a {{ text-decoration: none; color: inherit; }}
  .wrap {{ max-width: 1100px; margin: 0 auto; padding: 0 24px; }}

  /* ---------- NAV ---------- */
  nav.topnav {{
    position: sticky; top: 0; z-index: 20; backdrop-filter: blur(14px);
    background: rgba(255,255,255,.82); border-bottom: 1px solid var(--line);
  }}
  nav.topnav .row {{ display: flex; align-items: center; justify-content: space-between; padding: 14px 24px; max-width: 1100px; margin: 0 auto; }}
  .wordmark {{ font-size: 1.05rem; font-weight: 600; }}
  .navlinks {{ display: flex; gap: 26px; font-size: .82rem; color: var(--gray); }}
  .navlinks a:hover {{ color: var(--ink); }}

  /* ---------- HERO ---------- */
  .hero {{ text-align: center; padding: 88px 24px 0; }}
  .eyebrow {{ font-size: .95rem; font-weight: 600; color: var(--gray); margin-bottom: 6px; }}
  h1.headline {{
    font-size: clamp(2.6rem, 7vw, 5.4rem); font-weight: 700; line-height: 1.04;
    letter-spacing: -0.02em; margin: 4px 0 12px;
  }}
  .hero .sub {{ font-size: clamp(1.1rem, 2vw, 1.4rem); color: var(--gray); margin: 0 auto 26px; max-width: 620px; }}
  .pill-links {{ display: flex; justify-content: center; gap: 26px; font-size: 1.1rem; margin-bottom: 46px; }}
  .pill-links a.primary {{ color: var(--accent); font-weight: 600; }}
  .pill-links a:hover {{ text-decoration: underline; }}
  .hero-photo {{
    width: 100%; max-width: 1100px; margin: 0 auto; border-radius: 28px; overflow: hidden;
    box-shadow: 0 30px 60px rgba(0,0,0,.12);
  }}
  .hero-photo img {{ width: 100%; display: block; height: clamp(280px, 46vw, 620px); object-fit: cover; }}

  /* ---------- FEATURE (alternating full-width) ---------- */
  section.feature {{ padding: 110px 24px; text-align: center; }}
  section.feature.dark {{ background: #000; color: #fff; }}
  section.feature.soft {{ background: var(--bg-soft); }}
  .feature h2 {{
    font-size: clamp(2.2rem, 5vw, 3.6rem); font-weight: 700; letter-spacing: -0.02em;
    line-height: 1.08; margin: 0 0 14px;
  }}
  .feature p.sub {{ font-size: 1.15rem; color: var(--gray); max-width: 560px; margin: 0 auto 44px; }}
  section.feature.dark p.sub {{ color: #a1a1a6; }}
  .feature-photo {{
    max-width: 980px; margin: 0 auto; border-radius: 26px; overflow: hidden;
  }}
  .feature-photo img {{ width: 100%; display: block; height: clamp(260px, 40vw, 520px); object-fit: cover; }}

  /* ---------- HIGHLIGHTS GRID ---------- */
  section.highlights {{ padding: 100px 24px; }}
  .highlights h2 {{ text-align: center; font-size: clamp(2rem, 4vw, 3rem); font-weight: 700; letter-spacing: -.02em; margin: 0 0 56px; }}
  .grid3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; max-width: 1100px; margin: 0 auto; }}
  .tile {{ background: var(--bg-soft); border-radius: 24px; padding: 40px 30px; text-align: left; }}
  .tile .num {{ font-size: .82rem; font-weight: 700; color: var(--accent); margin-bottom: 18px; letter-spacing: .04em; }}
  .tile h3 {{ font-size: 1.4rem; font-weight: 700; margin: 0 0 10px; letter-spacing: -.01em; }}
  .tile p {{ font-size: .98rem; color: var(--gray); line-height: 1.6; margin: 0; }}

  /* ---------- SOURCES (Apple-style compatibility list) ---------- */
  section.sources {{ padding: 100px 24px; border-top: 1px solid var(--line); }}
  .sources .block-head {{ text-align: center; max-width: 620px; margin: 0 auto 40px; }}
  .sources h2 {{ font-size: clamp(2rem, 4vw, 3rem); font-weight: 700; letter-spacing: -.02em; margin: 0 0 12px; }}
  .sources .block-head p {{ color: var(--gray); font-size: 1.05rem; }}
  .segmented {{ display: flex; justify-content: center; gap: 4px; background: var(--bg-soft); border-radius: 999px;
    padding: 4px; width: fit-content; margin: 0 auto 44px; }}
  .segmented button {{
    border: none; background: transparent; padding: 8px 20px; border-radius: 999px; font-size: .88rem;
    font-weight: 600; cursor: pointer; color: var(--gray);
  }}
  .segmented button.active {{ background: #fff; color: var(--ink); box-shadow: 0 1px 4px rgba(0,0,0,.12); }}
  .sources-grid {{ max-width: 1100px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(200px,1fr)); }}
  .source-cell {{
    border-top: 1px solid var(--line); padding: 22px 4px; font-size: 1.15rem; font-weight: 600;
    text-align: center;
  }}

  /* ---------- CLOSING ---------- */
  section.closing {{ padding: 120px 24px; text-align: center; background: var(--bg-soft); }}
  section.closing h2 {{ font-size: clamp(2.2rem, 5vw, 3.6rem); font-weight: 700; letter-spacing: -.02em; margin: 0 0 16px; }}
  section.closing p {{ color: var(--gray); font-size: 1.1rem; max-width: 480px; margin: 0 auto 34px; }}
  .btn-pill {{
    display: inline-block; background: var(--ink); color: #fff; border-radius: 999px;
    padding: 14px 32px; font-weight: 600; font-size: 1.02rem;
  }}
  .btn-pill:hover {{ background: #000; }}

  .scroll-note {{ text-align: center; padding: 40px 0 60px; color: var(--gray); font-size: .95rem; font-weight: 600; }}
  .bounce {{ display: inline-block; animation: bounce 1.5s infinite; }}
  @keyframes bounce {{ 0%,100%{{transform:translateY(0);}} 50%{{transform:translateY(6px);}} }}

  footer.foot {{ padding: 40px 24px; border-top: 1px solid var(--line); text-align: center; color: var(--gray); font-size: .82rem; }}

  @media (max-width: 640px) {{
    .pill-links {{ flex-direction: column; gap: 12px; }}
    section.feature, section.highlights, section.sources, section.closing {{ padding-top: 64px; padding-bottom: 64px; }}
  }}
</style>
</head>
<body>

<nav class="topnav"><div class="row">
  <a href="#top" class="wordmark">À La Mode</a>
  <div class="navlinks">
    <a href="#closet">How it works</a>
    <a href="#sources">Sources</a>
    <a href="#scroll-target">Open the app</a>
  </div>
</div></nav>

<section class="hero" id="top">
  <p class="eyebrow">À La Mode</p>
  <h1 class="headline">Your closet.<br>Reimagined.</h1>
  <p class="sub">Upload photos of what you already own. Get outfits built around current trends and your own taste.</p>
  <div class="pill-links">
    <a href="#scroll-target" class="primary">Style my closet &nbsp;›</a>
    <a href="#sources">See what inspires it &nbsp;›</a>
  </div>
  <div class="hero-photo"><img src="{PHOTO_RACKS}" alt="Clothing rack"></div>
</section>

<section class="feature dark" id="closet">
  <h2>Upload once.<br>Style forever.</h2>
  <p class="sub">Snap photos of your tops, bottoms, shoes, and bags. We tag the category and read the color automatically — no manual sorting.</p>
  <div class="feature-photo"><img src="{PHOTO_COAT}" alt="Coat on a minimal rack"></div>
</section>

<section class="highlights">
  <h2>Built to actually get worn.</h2>
  <div class="grid3">
    <div class="tile"><div class="num">01</div><h3>Color-matched</h3><p>Every combination is checked against real color-harmony rules, so pairings look intentional, not random.</p></div>
    <div class="tile"><div class="num">02</div><h3>Trend-aware</h3><p>Pulls current headlines from the fashion press, so suggestions reflect what's happening this season.</p></div>
    <div class="tile"><div class="num">03</div><h3>Fit-aware</h3><p>Add your height and body shape for silhouette tips that are actually about you, not a generic size chart.</p></div>
  </div>
</section>

<section class="feature soft">
  <h2>Nothing left folded in a drawer.</h2>
  <p class="sub">See every piece you own in one place, then let the pairing engine find the combinations you'd never have tried yourself.</p>
  <div class="feature-photo"><img src="{PHOTO_SWEATERS}" alt="Stack of folded sweaters"></div>
</section>

<section class="sources" id="sources">
  <div class="block-head">
    <h2>Our fashion sources.</h2>
    <p>The magazines, retailers, and houses we track for silhouette, color, and trend direction.</p>
  </div>
  <div class="segmented">
    <button class="active" onclick="filterSources('all', this)">All</button>
    <button onclick="filterSources('magazine', this)">Magazines</button>
    <button onclick="filterSources('retailer', this)">Retailers</button>
    <button onclick="filterSources('brand', this)">Brands</button>
  </div>
  <div class="sources-grid" id="sources-grid">
    {_source_rows()}
  </div>
</section>

<section class="closing">
  <h2>Your closet is more<br>versatile than you think.</h2>
  <p>Upload a few photos and see what you can put together in the next five minutes.</p>
  <a href="#scroll-target" class="btn-pill">Try À La Mode free</a>
</section>

<div class="scroll-note" id="scroll-target">
  <span class="bounce">⬇</span><br>Your closet tool is right below — keep scrolling on the page.
</div>

<footer class="foot">À La Mode — built with Streamlit. Not affiliated with the brands or publications listed above.</footer>

<script>
  function filterSources(cat, btn) {{
    document.querySelectorAll('.segmented button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('#sources-grid .source-cell').forEach(cell => {{
      cell.style.display = (cat === 'all' || cell.dataset.cat === cat) ? '' : 'none';
    }});
  }}
</script>

</body>
</html>
"""
