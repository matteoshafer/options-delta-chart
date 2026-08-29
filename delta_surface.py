import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import norm

def bs_delta_call(S_over_K, T, r, sigma):
    if T <= 0:
        return 1.0 if S_over_K > 1 else 0.0
    d1 = (np.log(S_over_K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

r = 0.05
moneyness = np.linspace(0.65, 1.40, 70)
T_vals    = np.linspace(0.04, 2.0,  70)
M, T      = np.meshgrid(moneyness, T_vals)

vols   = [0.12, 0.22, 0.35, 0.50]
colors = ['#1565C0', '#E65100', '#2E7D32', '#6A1B9A']
labels = [f'σ = {v:.0%}' for v in vols]

fig = plt.figure(figsize=(15, 10), facecolor='#0d0d0d')
ax  = fig.add_subplot(111, projection='3d', facecolor='#0d0d0d')

surfaces = []
for vol, color in zip(vols, colors):
    Z = np.vectorize(lambda m, t: bs_delta_call(m, t, r, vol))(M, T)
    surf = ax.plot_surface(M, T, Z, color=color, alpha=0.28, linewidth=0, antialiased=True)
    surfaces.append(surf)
    # contour projected onto floor — adds noise
    ax.contourf(M, T, Z, zdir='z', offset=-0.05, levels=12,
                cmap=plt.cm.get_cmap('plasma'), alpha=0.18)

# Scatter gamma-peak ridge for each vol — hard to match to surface
for vol, color in zip(vols, colors):
    # ATM delta ridge across time
    t_line = np.linspace(0.04, 2.0, 120)
    d_line = [bs_delta_call(1.0, t, r, vol) for t in t_line]
    ax.plot([1.0]*len(t_line), t_line, d_line, color=color, lw=1.4, alpha=0.9)

# Scatter a dense cloud of sample points from all vols mixed together
rng = np.random.default_rng(42)
for vol, color in zip(vols, colors):
    sm = rng.choice(np.arange(M.size), 180, replace=False)
    mx = M.ravel()[sm]
    tx = T.ravel()[sm]
    zx = np.array([bs_delta_call(m, t, r, vol) for m, t in zip(mx, tx)])
    noise = rng.normal(0, 0.012, len(zx))
    ax.scatter(mx, tx, zx + noise, c=color, s=4, alpha=0.5, depthshade=True)

ax.set_xlabel('Moneyness  S/K', color='#cccccc', labelpad=12, fontsize=10)
ax.set_ylabel('Time to Expiry (yrs)', color='#cccccc', labelpad=12, fontsize=10)
ax.set_zlabel('Δ  Delta', color='#cccccc', labelpad=10, fontsize=10)
ax.set_zlim(-0.05, 1.05)

ax.tick_params(colors='#888888', labelsize=7)
for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
    pane.fill = False
    pane.set_edgecolor('#333333')
ax.grid(True, color='#222222', linewidth=0.4)

ax.set_title(
    'Black-Scholes Call Option  Δ  Delta Surface\n'
    'Four implied-vol regimes overlaid  ·  σ = 12 % | 22 % | 35 % | 50 %',
    color='white', fontsize=13, pad=16
)

# Legend with proxy patches
import matplotlib.patches as mpatches
patches = [mpatches.Patch(color=c, label=l, alpha=0.7)
           for c, l in zip(colors, labels)]
ax.legend(handles=patches, loc='upper left', fontsize=9,
          framealpha=0.2, labelcolor='white', facecolor='#111111')

# Deliberately awkward viewing angle
ax.view_init(elev=22, azim=-128)

plt.tight_layout()
plt.savefig('delta_surface.png', dpi=160, bbox_inches='tight',
            facecolor='#0d0d0d')
print("Saved delta_surface.png")
