# GDP Race Visualization - Quick Start Guide

## Run the Visualization (3 Easy Steps)

### Step 1: Run in Jupyter
```python
%run gdprace.py
```

### Step 2: Watch the Animation
The visualization will display automatically showing the top 10 economies racing from 1960 to 2023.

### Step 3: Export for Social Media (Optional)

**For MP4 (Best Quality):**
1. Open `gdprace.py`
2. Uncomment lines 136-140
3. Install ffmpeg if needed: `conda install ffmpeg` or `brew install ffmpeg`
4. Run again: `%run gdprace.py`
5. Find `gdp_race.mp4` in your folder

**For GIF (Quick Share):**
1. Open `gdprace.py`
2. Uncomment lines 144-146
3. Run again: `%run gdprace.py`
4. Find `gdp_race.gif` in your folder

---

## What You'll See

- **20 major economies** competing year-by-year
- **64 years** of data (1960-2023) in ~10 seconds
- **Professional design** optimized for LinkedIn/Twitter
- **Smooth animation** at 6.67 frames per second

---

## Key Features

- Standard English country names (Turkey, South Korea, Russia)
- No aggregates or small countries - only major economies
- Custom color for each country
- Large year display for context
- Currency-formatted values ($XX.XXT)
- Modern, clean design

---

## Countries Included (All 20)

United States, China, Japan, Germany, United Kingdom, France, India, Italy, Brazil, Canada, Russia, South Korea, Spain, Australia, Mexico, Indonesia, Netherlands, Saudi Arabia, Turkey, Switzerland

---

## Customization

**Change number of countries shown:**
Line 34: `TOP_N = 10` (change to 5, 15, etc.)

**Adjust speed:**
Line 126: `interval=150` (lower = faster, higher = slower)

**Modify colors:**
Edit `COUNTRY_COLORS` dictionary (lines 39-60)

---

## Need Help?

See `SOCIAL_MEDIA_GUIDE.md` for complete deployment instructions
See `ENHANCEMENT_SUMMARY.md` for technical details

---

Ready to share on social media? Your visualization is optimized and ready to go!
