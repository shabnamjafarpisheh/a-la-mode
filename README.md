# StyleMate — Free Streamlit Outfit Planner

A free, open-source Streamlit app for building outfits from photos of your own clothes,
bags, and shoes — personalized with your height, weight, gender, and style taste,
and informed by live fashion headlines.

## Run it locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually http://localhost:8501).

## Deploy for free

1. Push `app.py` and `requirements.txt` to a public GitHub repo.
2. Go to https://share.streamlit.io, sign in, and click "New app."
3. Point it at your repo/branch/`app.py`. That's it — free hosting.

## What it actually does

- **Upload & tag**: upload photos of your items, tag each as Top / Bottom / Dress /
  Outerwear / Shoes / Bag / Accessory.
- **Auto color detection**: each photo's dominant color is extracted automatically
  (used for outfit color-matching).
- **Live trends**: pulls recent headlines from public fashion RSS feeds (Vogue, Elle,
  Harper's Bazaar, WWD) when you have internet access; falls back to a curated trend
  palette list if a feed can't be reached.
- **Outfit generation**: combines your items using a color-harmony heuristic
  (analogous / complementary / triadic hue matching, with neutrals always safe).
- **Fit tips**: general silhouette suggestions based on an optional body-shape
  selector and height — framed as guidelines, not rules.

## Honest limitations (so you can extend it)

- "Connected to all fashion websites" isn't literally possible — there's no single
  API that aggregates every fashion site. This app uses public RSS feeds as a
  realistic, free stand-in, with a curated fallback dataset.
- Color detection is a simple average-color heuristic, not real garment
  segmentation — a busy background in a photo will skew the detected color.
  For production quality, swap in a proper image-segmentation or vision model.
- Outfit "trend matching" against live headlines is keyword-based and fairly
  shallow, since headline text is limited. A production version would want a
  real, licensed fashion-trend dataset or a vision-language model.

## Files

- `app.py` — the full Streamlit app
- `requirements.txt` — dependencies
