"""
hero_section.py
================
Your Canva design, converted into a plain HTML/CSS string with no external
JS dependencies (no Tailwind CDN, no Lucide script) so it renders reliably
inside Streamlit's sandboxed `components.html` iframe.

Why not just embed the original Canva export?
  - Its content comes from Canva's own /_sdk/ scripts, which only resolve
    on Canva's servers — inside Streamlit's iframe they'd 404 and the
    section would render blank.
  - Scripts injected via Streamlit's `st.markdown(..., unsafe_allow_html=True)`
    don't execute (browsers don't run <script> tags inserted that way), so
    the Tailwind CDN build step wouldn't run either. That's why every
    Tailwind utility class below has been converted into real, static CSS.

Why an iframe (`components.html`) instead of `st.markdown`?
  - `st.markdown` strips <style>/<script> in ways that break a design this
    size. `components.html` renders the whole thing in its own sandboxed
    document, so the layout, fonts, and gradients all render exactly as
    designed.
  - Trade-off: because it's a separate document, its internal links
    (#closet, #sources) only scroll within the banner itself — they can't
    jump to the Streamlit widgets below it. That's why the CTA buttons
    here scroll down to a marker at the bottom of the banner instead,
    with a prompt to keep scrolling into the app below.
"""

HERO_HTML = """
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0; font-family: -apple-system, "DM Sans", "Segoe UI", sans-serif;
    color: #292420; background: #faf7f2;
  }
  .editorial { font-family: Georgia, "Playfair Display", serif; }
  .wrap { max-width: 1100px; margin: 0 auto; padding: 0 20px; }
  a { text-decoration: none; color: inherit; }

  header.nav { padding: 20px 0; }
  header.nav .row { display: flex; align-items: center; justify-content: space-between; }
  .brand { font-size: 1.4rem; font-weight: 700; }
  .cta-btn {
    background: #26352d; color: #fff; border-radius: 999px; padding: 10px 22px;
    font-weight: 700; font-size: .9rem; border: none; cursor: pointer; display: inline-block;
  }

  .hero {
    background: radial-gradient(circle at 72% 32%, rgba(217,95,69,.28), transparent 55%),
                radial-gradient(circle at 18% 88%, rgba(224,184,111,.28), transparent 55%);
    padding: 50px 0 70px;
  }
  .hero .grid { display: flex; flex-wrap: wrap; gap: 40px; align-items: center; }
  .hero .col { flex: 1 1 420px; }
  .tag {
    display: inline-block; background: #eee6d8; color: #6b5a3a; border-radius: 999px;
    padding: 5px 14px; font-size: .72rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: .08em; margin-bottom: 18px;
  }
  h1.headline { font-size: 2.8rem; line-height: 1.05; margin: 0 0 20px; font-weight: 600; }
  .hero p.lead { font-size: 1.1rem; line-height: 1.7; margin: 0 0 26px; max-width: 480px; }
  .btn-row { display: flex; flex-wrap: wrap; gap: 12px; }
  .btn-outline {
    border: 1.5px solid #26352d; border-radius: 999px; padding: 10px 22px;
    font-weight: 700; font-size: .9rem; display: inline-block; cursor: pointer;
  }
  .placeholder {
    background: linear-gradient(135deg,#e7ded0,#c9b593); border-radius: 28px;
    display: flex; align-items: center; justify-content: center; color: #6b5a3a;
    font-size: .85rem; text-align: center; padding: 20px; min-height: 320px;
  }

  section.block { padding: 60px 0; }
  .block-head { max-width: 620px; margin-bottom: 34px; }
  h2.title { font-size: 2.2rem; margin: 6px 0 12px; font-weight: 600; }
  .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 22px; }
  .card {
    background: #fff; border: 1px solid #ece5da; border-radius: 26px; overflow: hidden;
  }
  .card .img { height: 170px; }
  .card .body { padding: 22px; }
  .icon-badge {
    display: inline-flex; align-items: center; justify-content: center; width: 40px; height: 40px;
    border-radius: 999px; color: #fff; font-size: 1.1rem; margin-bottom: 14px;
  }
  .card h3 { font-size: 1.35rem; margin: 0 0 8px; font-weight: 600; }
  .card p { margin: 0; line-height: 1.6; font-size: .95rem; }

  .quote-card { background: linear-gradient(135deg,#d9b774,#8b5d43); color: #fff;
    display: flex; align-items: flex-end; padding: 24px; min-height: 170px; font-size: 1.4rem;
    font-weight: 600; line-height: 1.25; }

  .sources-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 18px; }
  .source-card { background: #fff; border: 1px solid #ece5da; border-radius: 20px; padding: 22px; transition: transform .2s ease; }
  .source-card:hover { transform: translateY(-4px); }
  .source-card h3 { font-size: 1.5rem; margin: 10px 0; font-weight: 600; }
  .source-card p { font-size: .9rem; line-height: 1.55; margin: 0 0 14px; }
  .visit { font-weight: 700; font-size: .85rem; }

  .closing { background: #26352d; color: #fff; border-radius: 28px; text-align: center;
    padding: 60px 30px; margin: 20px auto; }
  .closing h2 { color: #fff; }
  .closing p { color: rgba(255,255,255,.8); max-width: 480px; margin: 0 auto 24px; }
  .btn-white { background: #fff; color: #292420; border-radius: 999px; padding: 12px 26px;
    font-weight: 700; display: inline-block; }

  .scroll-note { text-align: center; padding: 30px 0 50px; }
  .scroll-note p { font-weight: 700; font-size: 1rem; }
  .bounce { animation: bounce 1.4s infinite; display: inline-block; }
  @keyframes bounce { 0%,100%{transform:translateY(0);} 50%{transform:translateY(6px);} }
</style>
</head>
<body>

<header class="nav"><div class="wrap row" style="display:flex;align-items:center;justify-content:space-between;">
  <a href="#top" class="brand editorial">À La Mode</a>
  <a href="#scroll-target" class="cta-btn">Open the app ↓</a>
</div></header>

<section class="hero" id="top"><div class="wrap grid">
  <div class="col">
    <span class="tag">Your wardrobe, reimagined</span>
    <h1 class="headline editorial">Style yourself with what you already own.</h1>
    <p class="lead">Upload photos of your clothes, bags, and shoes. À La Mode pairs them into outfits built around current trends and the way you like to dress.</p>
    <div class="btn-row">
      <a href="#scroll-target" class="cta-btn">✨ Style my closet</a>
      <a href="#sources" class="btn-outline">See what inspires it</a>
    </div>
  </div>
  <div class="col">
    <div class="placeholder">Replace with your own hero photo<br>(e.g. a styled flat-lay)</div>
  </div>
</div></section>

<section class="block" id="closet"><div class="wrap">
  <div class="block-head">
    <span class="tag">How it works</span>
    <h2 class="title editorial">Three steps to a styled closet</h2>
    <p>No spreadsheets, no guesswork — just your actual pieces, organized and paired for you.</p>
  </div>
  <div class="cards">
    <div class="card"><div class="img placeholder" style="border-radius:0;">Closet photo</div>
      <div class="body"><div class="icon-badge" style="background:#26352d;">👕</div>
        <h3 class="editorial">Upload your pieces</h3>
        <p>Snap photos of tops, bottoms, shoes, and bags. We tag the category and pull the dominant color automatically.</p></div></div>
    <div class="card"><div class="img placeholder" style="border-radius:0;">Outfit photo</div>
      <div class="body"><div class="icon-badge" style="background:#cf6542;">✨</div>
        <h3 class="editorial">Get outfit combinations</h3>
        <p>We match pieces by color harmony and today's trends, then hand you a shortlist of full outfits.</p></div></div>
    <div class="card"><div class="quote-card editorial">"I stopped buying clothes I already own."</div>
      <div class="body"><div class="icon-badge" style="background:#875b45;">♥</div>
        <h3 class="editorial">Dress with confidence</h3>
        <p>Add your height, body shape, and taste for fit tips that actually fit you, not a generic size chart.</p></div></div>
  </div>
</div></section>

<section class="block" id="sources"><div class="wrap">
  <div class="block-head">
    <span class="tag">Where the trends come from</span>
    <h2 class="title editorial">Our fashion sources</h2>
    <p>Editorial voices we track for silhouette, color, and trend direction.</p>
  </div>
  <div class="sources-grid">
    <a class="source-card" href="https://www.vogue.com/" target="_blank" rel="noopener noreferrer">
      <span class="tag">Magazine</span><h3 class="editorial">Vogue</h3>
      <p>Runway collections and editorials from the industry's benchmark title.</p>
      <span class="visit">Visit →</span></a>
    <a class="source-card" href="https://www.elle.com/fashion/" target="_blank" rel="noopener noreferrer">
      <span class="tag">Magazine</span><h3 class="editorial">Elle</h3>
      <p>Modern, wearable takes on the trends moving down the runway.</p>
      <span class="visit">Visit →</span></a>
    <a class="source-card" href="https://www.harpersbazaar.com/fashion/" target="_blank" rel="noopener noreferrer">
      <span class="tag">Magazine</span><h3 class="editorial">Harper's Bazaar</h3>
      <p>Sophisticated styling and a long editorial eye on womenswear.</p>
      <span class="visit">Visit →</span></a>
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

</body>
</html>
"""
