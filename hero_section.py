"""
hero_section.py
================
Your Canva design, converted into a plain HTML/CSS string with no external
JS dependencies, so it renders reliably inside Streamlit's sandboxed
`components.html` iframe. See the notes at the bottom of app.py for why
this approach (rather than pasting the raw Canva export) is used.

v2 changes:
  - Front page (hero) is now just the site name over a full-bleed photo,
    with a one-line description underneath — nothing else competes for
    attention up top.
  - Warmer, livelier color palette (berry / coral / gold) instead of the
    dark green + tan combination.
  - Full source list (magazines + luxury retailers + brands to study),
    filterable, styled as elegant wordmark cards rather than photographs.
    Real brand photography/logos aren't included here on purpose — most
    of it is copyrighted or trademarked, and embedding it on a public
    site without a license is a real legal risk. These wordmark cards are
    a placeholder you can swap for licensed brand imagery later if you
    get permission, or for your own product photography.
  - More breathing room, larger type, hover states, mobile breakpoints.
"""

HEADER_PHOTO_URL = "https://images.unsplash.com/photo-1603400521630-9f2de124b33b?fm=jpg&q=80&w=2000&auto=format&fit=crop"
# Photo by Thom Bradley on Unsplash — free to use under the Unsplash License (unsplash.com/license).

SOURCES = [
    # (name, category)  category: "magazine" | "retailer" | "brand"
    ("Vogue", "magazine"), ("Harper's Bazaar", "magazine"), ("Elle", "magazine"),
    ("L'Officiel", "magazine"), ("Numéro", "magazine"), ("Marie Claire", "magazine"),
    ("Porter Magazine", "magazine"), ("The Gentlewoman", "magazine"),
    ("Net-a-Porter", "retailer"), ("Mytheresa", "retailer"), ("Moda Operandi", "retailer"),
    ("Farfetch", "retailer"), ("SSENSE", "retailer"), ("Bergdorf Goodman", "retailer"),
    ("Ralph Lauren", "brand"), ("The Row", "brand"), ("Brunello Cucinelli", "brand"),
    ("Max Mara", "brand"), ("Loro Piana", "brand"), ("Totême", "brand"),
    ("Khaite", "brand"), ("Jil Sander", "brand"), ("Hermès", "brand"), ("Ferragamo", "brand"),
]

_PALETTE = ["#B23A6B", "#E8B54D", "#FF7A59", "#7A3B69"]  # rotates per card

def _source_cards():
    cards = []
    for i, (name, cat) in enumerate(SOURCES):
        color = _PALETTE[i % len(_PALETTE)]
        cat_label = {"magazine": "Magazine", "retailer": "Retailer", "brand": "Brand"}[cat]
        cards.append(f"""
        <div class="source-card" data-cat="{cat}" style="background:linear-gradient(135deg,{color}22,{color}0a);border-color:{color}33;">
          <span class="tag" style="background:{color}20;color:{color};">{cat_label}</span>
          <h3 class="editorial" style="color:{color};">{name}</h3>
        </div>""")
    return "\n".join(cards)


HERO_HTML = f"""
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; }}
  :root {{
    --ink: #2E1A22;
    --primary: #B23A6B;
    --accent: #FF7A59;
    --gold: #E8B54D;
    --blush: #FBE4E8;
    --cream: #FDF6F0;
  }}
  body {{
    margin: 0; font-family: -apple-system, "DM Sans", "Segoe UI", sans-serif;
    color: var(--ink); background: var(--cream);
  }}
  .editorial {{ font-family: Georgia, "Playfair Display", serif; }}
  .wrap {{ max-width: 1120px; margin: 0 auto; padding: 0 24px; }}
  a {{ text-decoration: none; color: inherit; }}

  /* ---------- FRONT PAGE ---------- */
  .front {{
    position: relative; min-height: 560px; display: flex; align-items: center;
    justify-content: center; text-align: center; overflow: hidden;
    background-image: linear-gradient(180deg, rgba(46,26,34,.55), rgba(178,58,107,.55)),
                       url('{HEADER_PHOTO_URL}');
    background-size: cover; background-position: center;
  }}
  .front .inner {{ position: relative; z-index: 2; padding: 40px 24px; }}
  .site-name {{
    font-size: 5rem; line-height: 1; color: #fff; margin: 0 0 22px; font-weight: 700;
    letter-spacing: .01em; text-shadow: 0 4px 30px rgba(0,0,0,.25);
  }}
  .front p.desc {{
    font-size: 1.2rem; color: #fff; max-width: 560px; margin: 0 auto 30px;
    line-height: 1.65; opacity: .95;
  }}
  .front .scroll-cue {{ color: #fff; font-size: .85rem; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; }}
  .bounce {{ display: inline-block; animation: bounce 1.5s infinite; }}
  @keyframes bounce {{ 0%,100%{{transform:translateY(0);}} 50%{{transform:translateY(7px);}} }}

  /* ---------- SECTIONS ---------- */
  section.block {{ padding: 64px 0; }}
  .block-head {{ max-width: 640px; margin: 0 auto 36px; text-align: center; }}
  .tag {{
    display: inline-block; background: var(--blush); color: var(--primary); border-radius: 999px;
    padding: 6px 16px; font-size: .75rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: .08em; margin-bottom: 16px;
  }}
  h2.title {{ font-size: 2.3rem; margin: 6px 0 14px; font-weight: 700; }}
  .block-head p {{ font-size: 1.05rem; line-height: 1.65; }}

  .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(270px, 1fr)); gap: 24px; }}
  .card {{ background: #fff; border: 1px solid #f0e2e7; border-radius: 26px; overflow: hidden; box-shadow: 0 8px 24px rgba(178,58,107,.06); }}
  .card .img {{ height: 175px; }}
  .card .body {{ padding: 26px; }}
  .icon-badge {{
    display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px;
    border-radius: 999px; color: #fff; font-size: 1.2rem; margin-bottom: 16px;
  }}
  .card h3 {{ font-size: 1.4rem; margin: 0 0 10px; font-weight: 700; }}
  .card p {{ margin: 0; line-height: 1.65; font-size: .97rem; }}

  .quote-card {{ background: linear-gradient(135deg,var(--gold),var(--accent)); color: #fff;
    display: flex; align-items: flex-end; padding: 26px; min-height: 175px; font-size: 1.45rem;
    font-weight: 700; line-height: 1.25; }}

  .placeholder {{
    background: linear-gradient(135deg,var(--blush),#f3cfd8); display: flex; align-items: center;
    justify-content: center; color: var(--primary); font-size: .85rem; text-align: center; padding: 16px;
  }}

  /* ---------- SOURCES ---------- */
  .filters {{ display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; margin-bottom: 32px; }}
  .filter-btn {{
    border: 1.5px solid var(--primary); color: var(--primary); background: #fff; border-radius: 999px;
    padding: 9px 20px; font-weight: 700; font-size: .88rem; cursor: pointer;
  }}
  .filter-btn.active {{ background: var(--primary); color: #fff; }}
  .sources-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap: 16px; }}
  .source-card {{
    border: 1.5px solid; border-radius: 20px; padding: 22px 18px; text-align: center;
    transition: transform .2s ease, box-shadow .2s ease;
  }}
  .source-card:hover {{ transform: translateY(-4px); box-shadow: 0 10px 26px rgba(46,26,34,.1); }}
  .source-card h3 {{ font-size: 1.25rem; margin: 4px 0 0; font-weight: 700; }}

  /* ---------- CLOSING ---------- */
  .closing {{
    background: linear-gradient(135deg, var(--primary), var(--accent)); color: #fff; border-radius: 30px;
    text-align: center; padding: 64px 30px; margin: 10px auto 0;
  }}
  .closing h2 {{ color: #fff; }}
  .closing p {{ color: rgba(255,255,255,.9); max-width: 500px; margin: 0 auto 26px; font-size: 1.05rem; }}
  .btn-white {{
    background: #fff; color: var(--primary); border-radius: 999px; padding: 13px 28px;
    font-weight: 700; display: inline-block; font-size: 1rem;
  }}
  .btn-white:hover {{ opacity: .92; }}

  .scroll-note {{ text-align: center; padding: 40px 0 56px; }}
  .scroll-note p {{ font-weight: 700; font-size: 1.05rem; color: var(--primary); }}

  @media (max-width: 640px) {{
    .site-name {{ font-size: 3rem; }}
    .front {{ min-height: 440px; }}
    h2.title {{ font-size: 1.8rem; }}
  }}
</style>
</head>
<body>

<section class="front" id="top">
  <div class="inner">
    <h1 class="site-name editorial">À La Mode</h1>
    <p class="desc">Your closet, styled. Upload photos of what you already own and get outfit combinations built around current trends and your own taste.</p>
    <a href="#scroll-target" class="scroll-cue">Scroll to begin <span class="bounce">⬇</span></a>
  </div>
</section>

<section class="block" id="closet"><div class="wrap">
  <div class="block-head">
    <span class="tag">How it works</span>
    <h2 class="title editorial">Three steps to a styled closet</h2>
    <p>No spreadsheets, no guesswork — just your actual pieces, organized and paired for you.</p>
  </div>
  <div class="cards">
    <div class="card"><div class="img placeholder" style="border-radius:0;">Closet photo</div>
      <div class="body"><div class="icon-badge" style="background:var(--primary);">👕</div>
        <h3 class="editorial">Upload your pieces</h3>
        <p>Snap photos of tops, bottoms, shoes, and bags. We tag the category and pull the dominant color automatically.</p></div></div>
    <div class="card"><div class="img placeholder" style="border-radius:0;">Outfit photo</div>
      <div class="body"><div class="icon-badge" style="background:var(--accent);">✨</div>
        <h3 class="editorial">Get outfit combinations</h3>
        <p>We match pieces by color harmony and today's trends, then hand you a shortlist of full outfits.</p></div></div>
    <div class="card"><div class="quote-card editorial">"I stopped buying clothes I already own."</div>
      <div class="body"><div class="icon-badge" style="background:var(--gold);">♥</div>
        <h3 class="editorial">Dress with confidence</h3>
        <p>Add your height, body shape, and taste for fit tips that actually fit you, not a generic size chart.</p></div></div>
  </div>
</div></section>

<section class="block" id="sources" style="background:#fff;"><div class="wrap">
  <div class="block-head">
    <span class="tag">Where the trends come from</span>
    <h2 class="title editorial">Our fashion sources</h2>
    <p>The magazines, retailers, and houses we track for silhouette, color, and trend direction.</p>
  </div>
  <div class="filters">
    <button class="filter-btn active" data-filter="all" onclick="filterSources('all', this)">All</button>
    <button class="filter-btn" data-filter="magazine" onclick="filterSources('magazine', this)">Magazines</button>
    <button class="filter-btn" data-filter="retailer" onclick="filterSources('retailer', this)">Retailers</button>
    <button class="filter-btn" data-filter="brand" onclick="filterSources('brand', this)">Brands</button>
  </div>
  <div class="sources-grid" id="sources-grid">
    {_source_cards()}
  </div>
</div></section>

<section class="block"><div class="wrap">
  <div class="closing">
    <h2 class="editorial">Your closet is more versatile than you think.</h2>
    <p>Upload a few photos and see what you can put together in the next five minutes.</p>
    <a href="#scroll-target" class="btn-white">✨ Try À La Mode free</a>
  </div>
</div></section>

<div class="scroll-note" id="scroll-target">
  <span class="bounce">⬇</span>
  <p>Your closet tool is right below — keep scrolling on the page.</p>
</div>

<script>
  function filterSources(cat, btn) {{
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('#sources-grid .source-card').forEach(card => {{
      card.style.display = (cat === 'all' || card.dataset.cat === cat) ? '' : 'none';
    }});
  }}
</script>

</body>
</html>
"""
