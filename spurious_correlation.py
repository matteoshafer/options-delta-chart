import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

np.random.seed(7)

months = np.arange(1, 49)  # 48 months

# Series 1: fake "global temp anomaly" — slow upward drift + seasonal wobble
trend1 = 0.015 * months + np.sin(months * 0.52) * 0.3
series1 = trend1 + np.random.normal(0, 0.08, len(months))

# Series 2: completely unrelated random walk, then scaled for the right axis
rw = np.cumsum(np.random.normal(0, 1, len(months))) * 0.12
series2 = rw * 2.4 + 6.1   # different units, different scale

fig, ax1 = plt.subplots(figsize=(14, 7), facecolor='#1a1a2e')
ax2 = ax1.twinx()
ax1.set_facecolor('#1a1a2e')

# ── Series 1 (left axis) ──────────────────────────────────────────────────
ax1.fill_between(months, series1, alpha=0.28, color='#e94560', zorder=2)
ax1.plot(months, series1, color='#e94560', lw=2, zorder=3,
         label='Temp Anomaly (°C)')

# ── Series 2 (right axis — INVERTED so it appears to track series 1) ──────
ax2.fill_between(months, series2, alpha=0.22, color='#53d8fb', zorder=1)
ax2.plot(months, series2, color='#53d8fb', lw=2, zorder=3,
         label='Avocado Index')
ax2.invert_yaxis()   # <── the deception: right axis reads top-to-bottom

# ── Irregular grid (not at uniform intervals) ─────────────────────────────
for y in [-0.35, 0.08, 0.41, 0.73, 1.05]:
    ax1.axhline(y, color='#2a2a4a', lw=0.6, ls='--', alpha=0.7)

# ── Non-uniform x ticks (gaps of 3, 3, 2, 4, 4, 3, 4…) ──────────────────
xtick_pos  = [1, 4, 7, 9, 13, 17, 20, 24, 28, 31, 36, 40, 44, 48]
xlabels    = [
    "Jan\n'22", "Apr", "Jul", "Sep\n'22",
    "Jan\n'23", "May", "Aug", "Dec\n'23",
    "Apr\n'24", "Jul", "Dec", "Apr\n'25",
    "Aug",      "Dec\n'25",
]
ax1.set_xticks(xtick_pos)
ax1.set_xticklabels(xlabels, color='#aaaaaa', fontsize=7, rotation=35)

# ── Axis styling ──────────────────────────────────────────────────────────
ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
ax1.tick_params(axis='y', colors='#e94560', labelsize=8)
ax1.tick_params(axis='x', colors='#888888')
ax1.set_ylabel('Temperature Anomaly  (°C)  ←', color='#e94560', fontsize=9)

ax2.tick_params(axis='y', colors='#53d8fb', labelsize=8)
ax2.set_ylabel('→  Avocado Consumption Index', color='#53d8fb', fontsize=9)

for ax in [ax1, ax2]:
    for spine in ax.spines.values():
        spine.set_edgecolor('#2a2a4a')

# ── Fake "key event" annotations at arbitrary points ─────────────────────
events = [
    (10, 'El Niño\nonset',   series1[9]  + 0.05),
    (22, 'Policy\nshift',    series1[21] - 0.18),
    (35, 'Peak\ndemand',     series1[34] + 0.08),
    (43, '???',              series1[42] - 0.12),
]
for xpos, label, yval in events:
    ax1.annotate(
        label,
        xy=(xpos, yval),
        xytext=(xpos + 1.8, yval + 0.22),
        arrowprops=dict(arrowstyle='->', color='#ffcc00', lw=0.8),
        color='#ffcc00', fontsize=7, ha='left',
    )

# ── Watermark correlation coefficient (looks authoritative) ──────────────
ax1.text(0.5, 0.5, 'r = 0.91', transform=ax1.transAxes,
         fontsize=52, color='white', alpha=0.04,
         ha='center', va='center', rotation=12)

# ── Legend (combined, placed near clutter) ───────────────────────────────
l1, lab1 = ax1.get_legend_handles_labels()
l2, lab2 = ax2.get_legend_handles_labels()
ax1.legend(l1 + l2, lab1 + lab2,
           loc='lower right', fontsize=9, framealpha=0.15,
           labelcolor='white', facecolor='#111122')

ax1.set_title(
    'Global Temperature Anomaly  vs.  Avocado Consumption Index\n'
    'Monthly, Jan 2022 – Dec 2025   ·   r = 0.91  (p < 0.001)',
    color='white', fontsize=12, pad=14,
)

plt.tight_layout()
plt.savefig('spurious_correlation.png', dpi=160, bbox_inches='tight',
            facecolor='#1a1a2e')
print("Saved spurious_correlation.png")
