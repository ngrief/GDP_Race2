import pandas as pd, numpy as np, matplotlib.pyplot as plt, matplotlib.animation as anim
import IPython.display as ipd
from matplotlib import rcParams
import os

# Configure FFmpeg path from imageio-ffmpeg if available
try:
    import imageio_ffmpeg
    plt.rcParams['animation.ffmpeg_path'] = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    pass  # Fall back to system FFmpeg if imageio-ffmpeg not installed

# ── Load World Bank GDP data (sample CSV) ───────
gdp = pd.read_csv("https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv")
gdp = gdp[gdp['Year']>=1960]

# ── Country name standardization ────────────────
# Map dataset names to standard English names
COUNTRY_NAME_MAP = {
    'Korea, Rep.': 'South Korea',
    'Turkiye': 'Turkey',
    'Russian Federation': 'Russia'
}
gdp['Country Name'] = gdp['Country Name'].replace(COUNTRY_NAME_MAP)

gdp_pivot = gdp.pivot(index='Year', columns='Country Name', values='Value').fillna(0)

# ── Filter to major/relevant countries ──────────
# Include only top 20 major economies (no aggregates, no small countries)
MAJOR_COUNTRIES = [
    'United States', 'China', 'Japan', 'Germany', 'United Kingdom',
    'France', 'India', 'Italy', 'Brazil', 'Canada',
    'Russia', 'South Korea', 'Spain', 'Australia', 'Mexico',
    'Indonesia', 'Netherlands', 'Saudi Arabia', 'Turkey', 'Switzerland'
]

# Filter to only include countries that exist in the dataset
available_countries = [c for c in MAJOR_COUNTRIES if c in gdp_pivot.columns]
gdp_pivot = gdp_pivot[available_countries]

# ── Visualization Setup ─────────────────────────
TOP_N = 10
years = gdp_pivot.index

# Modern, vibrant color palette for social media impact
# Custom colors designed to be eye-catching and professional
COUNTRY_COLORS = {
    'United States': '#1f77b4',  # Blue
    'China': '#d62728',          # Red
    'Japan': '#ff7f0e',          # Orange
    'Germany': '#2ca02c',        # Green
    'United Kingdom': '#9467bd', # Purple
    'France': '#8c564b',         # Brown
    'India': '#e377c2',          # Pink
    'Italy': '#7f7f7f',          # Gray
    'Brazil': '#bcbd22',         # Yellow-green
    'Canada': '#17becf',         # Cyan
    'Russia': '#ff9896',         # Light red
    'South Korea': '#98df8a',    # Light green
    'Spain': '#ffbb78',          # Light orange
    'Australia': '#c5b0d5',      # Light purple
    'Mexico': '#c49c94',         # Light brown
    'Indonesia': '#f7b6d2',      # Light pink
    'Netherlands': '#c7c7c7',    # Light gray
    'Saudi Arabia': '#dbdb8d',   # Light yellow
    'Turkey': '#9edae5',         # Light cyan
    'Switzerland': '#aec7e8'     # Light blue
}

# Enhanced figure with golden ratio proportions for aesthetic appeal
# Dimensions adjusted to ensure even pixel counts for video encoding
fig, ax = plt.subplots(figsize=(14, 8.68))
fig.patch.set_facecolor('#f8f9fa')  # Light background for contrast

# Modern typography settings
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']

def draw(year):
    ax.clear()
    ax.set_facecolor('#ffffff')

    top = gdp_pivot.loc[year].nlargest(TOP_N)[::-1]  # bottom → top

    # Assign colors based on country names
    bar_colors = [COUNTRY_COLORS.get(country, '#cccccc') for country in top.index]

    # Create bars with enhanced styling
    bars = ax.barh(top.index, top.values/1e12, color=bar_colors,
                   edgecolor='white', linewidth=1.5, alpha=0.9)

    # Add gradient effect by varying alpha slightly
    for i, bar in enumerate(bars):
        bar.set_alpha(0.85 + (i * 0.015))

    # Enhanced title with bold styling
    ax.set_title(f"Global GDP Race: Top {TOP_N} Economies",
                fontsize=24, fontweight='bold', pad=20, color='#2c3e50')

    # Year display - large and prominent (bottom right to avoid bar overlap)
    ax.text(0.98, 0.15, str(year), transform=ax.transAxes,
            fontsize=64, fontweight='bold', ha='right', va='bottom',
            color='#34495e', alpha=0.15)

    # Axis labels with modern styling
    ax.set_xlabel("GDP (Trillions USD)", fontsize=14, fontweight='bold', color='#2c3e50')
    ax.set_xlim(0, top.values.max()/1e12*1.15)

    # Add value labels with currency formatting
    for i, (v, country) in enumerate(zip(top.values, top.index)):
        ax.text(v/1e12 + top.values.max()/1e12*0.02, i,
               f"${v/1e12:,.2f}T",
               va='center', fontsize=11, fontweight='600', color='#2c3e50')

    # Modern grid styling
    ax.grid(axis='x', alpha=0.2, linestyle='--', linewidth=0.8, color='#7f8c8d')
    ax.set_axisbelow(True)

    # Remove top and right spines for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#bdc3c7')
    ax.spines['bottom'].set_color('#bdc3c7')

    # Enhanced tick styling
    ax.tick_params(axis='both', labelsize=11, colors='#2c3e50', length=0)

    # Add subtle watermark for branding
    ax.text(0.02, 0.02, 'Data: World Bank', transform=ax.transAxes,
            fontsize=9, color='#95a5a6', style='italic', alpha=0.7)

# ── Animation Configuration ─────────────────────
# Smooth animation: 150ms interval (6.67 frames per second) for optimal viewing
# Slower than video (too fast to read) but faster than slideshow (too slow to engage)
ani = anim.FuncAnimation(fig, draw, frames=years, interval=150, repeat=True)

# ── Display and Export Options ──────────────────
# Create output folder if it doesn't exist
os.makedirs('output', exist_ok=True)

# Try MP4 first (best for LinkedIn), fall back to GIF if FFmpeg unavailable
output_path_mp4 = os.path.join('output', 'gdp_race.mp4')
output_path_gif = os.path.join('output', 'gdp_race.gif')

print("Attempting to save animation...")
print("=" * 60)
mp4_success = False

# Try MP4 export (BEST for LinkedIn - smaller files, better quality)
try:
    print("Trying MP4 export (recommended for LinkedIn)...")
    from matplotlib.animation import FFMpegWriter

    # Create writer with optimized settings for LinkedIn
    writer = FFMpegWriter(fps=6.67, metadata=dict(artist='GDP Race Visualization'),
                         bitrate=2000, codec='libx264', extra_args=['-pix_fmt', 'yuv420p'])

    print(f"Saving to: {output_path_mp4}")
    ani.save(output_path_mp4, writer=writer, dpi=150, progress_callback=lambda i, n: print(f"Progress: {i}/{n} frames", end='\r'))

    file_size = os.path.getsize(output_path_mp4) / (1024*1024)
    print(f"\n[SUCCESS] MP4 saved: {output_path_mp4}")
    print(f"File size: {file_size:.2f} MB")
    print(f"Format: MP4 (H.264) - Perfect for LinkedIn!")
    print(f"Ready to upload to LinkedIn")
    mp4_success = True

except Exception as e:
    print(f"\n[FAILED] MP4 export failed: {str(e)}")
    print("Trying GIF fallback...")

# Fallback to GIF if MP4 fails
if not mp4_success:
    try:
        print(f"\nSaving as GIF: {output_path_gif}")
        from matplotlib.animation import PillowWriter

        writer = PillowWriter(fps=6.67)
        ani.save(output_path_gif, writer=writer, dpi=100, progress_callback=lambda i, n: print(f"Progress: {i}/{n} frames", end='\r'))

        file_size = os.path.getsize(output_path_gif) / (1024*1024)
        print(f"\n[SUCCESS] GIF saved: {output_path_gif}")
        print(f"File size: {file_size:.2f} MB")

        if file_size > 15:
            print(f"[WARNING] Large file ({file_size:.2f} MB)")
            print("  LinkedIn performs best with files under 15MB")
            print("  Install FFmpeg for better MP4 compression:")
            print("  - Windows: choco install ffmpeg  OR  download from ffmpeg.org")
            print("  - Mac: brew install ffmpeg")
            print("  - Linux: sudo apt install ffmpeg")
        else:
            print(f"Ready to upload to LinkedIn")

    except Exception as e:
        print(f"\n[FAILED] GIF export also failed: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Install Pillow: pip install pillow")
        print("2. For better results, install FFmpeg for MP4 export")

print("=" * 60)

# Show the animation
plt.show()
