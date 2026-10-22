import json, os, glob, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Polygon as MPoly, Rectangle
from matplotlib.lines import Line2D
from shapely.geometry import shape, box

for f in glob.glob('fonts/*.otf') + ['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc']:
    if os.path.exists(f): fm.fontManager.addfont(f)
_n = {f.name for f in fm.fontManager.ttflist}
FONT = next((n for n in ('Noto Sans CJK SC', 'Noto Sans CJK JP') if n in _n), 'DejaVu Sans')
plt.rcParams.update({'font.family': FONT, 'font.size': 10, 'axes.edgecolor': '#BBBBBB', 'axes.linewidth': .6,
                     'xtick.color': '#666666', 'ytick.color': '#666666', 'axes.labelcolor': '#444444', 'text.color': '#1F1F1F',
                     'savefig.dpi': 200})
INK, MID, LIGHT, LAND, PAPER = '#1F1F1F', '#8A8A8A', '#C9C6BF', '#ECE9E3', '#FFFFFF'
RED, RED_SOFT, BLUE, BLUE_SOFT = '#B33A2B', '#E3B5AE', '#2F4B7C', '#B9C4D6'
os.makedirs('out/assets', exist_ok=True)

a = pd.read_parquet('out/data/annual.parquet').set_index('year')
gov = pd.read_parquet('out/data/governments.parquet')
pres = pd.read_parquet('out/data/presidents.parquet')
nuke = pd.read_parquet('out/data/nuclear_sites.parquet')
pens = pd.read_parquet('out/data/pension_reforms.parquet')
lg = pd.read_parquet('out/data/legal_age_by_generation.parquet')
peers = pd.read_parquet('out/data/debt_peers.parquet')
sub = pd.read_parquet('out/data/debt_by_subsector.parquet').set_index('year')

def title(fig, t, s, y=.95):
    fig.text(.05, y, t, fontsize=15, weight='bold')
    fig.text(.05, y - .045, s, fontsize=9, color='#555555')
def fy(d):
    t = pd.Timestamp(d); return t.year + (t.dayofyear - 1) / 365.25
END = 2026.8

# ------------------------------------------------------------------ 1. map of nuclear sites
EXT = (-5.4, 9.9, 41.2, 51.4)
clip = box(EXT[0] - 1, EXT[2] - 1, EXT[1] + 1, EXT[3] + 1)
cs = json.load(open('raw/ne_50m_admin_0_countries.geojson'))['features']
fig, ax = plt.subplots(figsize=(9, 9))
for f in cs:
    g = shape(f['geometry'])
    if not g.intersects(clip): continue
    g = g.intersection(clip); fr = f['properties']['ADM0_A3'] == 'FRA'
    for p in getattr(g, 'geoms', [g]):
        if p.geom_type == 'Polygon':
            ax.add_patch(MPoly(np.array(p.exterior.coords), closed=True, fc=LAND if fr else '#F5F3EF', ec=LIGHT if fr else '#E2DFD9', lw=.6 if fr else .4))
op, cl = nuke[nuke.status == 'operating'], nuke[nuke.status == 'closed']
dec = lambda y: RED if y >= 1985 else (BLUE if y >= 1977 else INK)
ax.scatter(op.longitude, op.latitude, s=op.power_reactors_in_2026 * 70, c=[dec(y) for y in op.first_in_service], alpha=.85, edgecolors=PAPER, lw=1, zorder=4)
ax.scatter(cl.longitude, cl.latitude, s=60, facecolors='none', edgecolors=MID, lw=1.1, zorder=4)
OFF = {'Saint-Laurent-des-Eaux': (-9, -3, 'right'), 'Dampierre': (10, 4, 'left'), 'Paluel': (-10, -3, 'right'), 'Bugey': (10, -8, 'left')}
for r in op.itertuples():
    dx, dy, ha = OFF.get(r.site, (9, -3, 'left'))
    ax.annotate(f'{r.site} {r.power_reactors_in_2026}', (r.longitude, r.latitude), xytext=(dx, dy), ha=ha, textcoords='offset points', fontsize=7.5, color=INK, zorder=5)
for r in cl.itertuples():
    if r.site in ('Fessenheim', 'Superphénix', 'Brennilis'):
        ax.annotate(f'{r.site}, closed {int(r.closed)}', (r.longitude, r.latitude), xytext=(7, 9 if r.site == 'Superphénix' else 5), textcoords='offset points', fontsize=7, color=MID)
ax.set_xlim(EXT[0], EXT[1]); ax.set_ylim(EXT[2], EXT[3]); ax.set_aspect(1 / np.cos(np.radians(46.5)))
ax.set_xticks([]); ax.set_yticks([])
for s_ in ax.spines.values(): s_.set_visible(False)
h = [Line2D([], [], marker='o', ls='', mfc=INK, mec=PAPER, ms=9, label='First unit before 1977'), Line2D([], [], marker='o', ls='', mfc=BLUE, mec=PAPER, ms=9, label='1977 to 1984'),
     Line2D([], [], marker='o', ls='', mfc=RED, mec=PAPER, ms=9, label='1985 and after'), Line2D([], [], marker='o', ls='', mfc='none', mec=MID, ms=8, label='Closed site')]
ax.legend(handles=h, loc='lower left', frameon=False, fontsize=8.5)
title(fig, 'Fifty-seven reactors on eighteen sites', 'France\'s nuclear power stations in 2026; circle size is the number of reactors, colour the date of the first unit.', y=.955)
fig.text(.05, .03, 'Sites, coordinates and dates: Wikidata. Reactor counts set by hand. Borders: Natural Earth.', fontsize=7, color=MID)
plt.subplots_adjust(left=.02, right=.98, top=.88, bottom=.05)
fig.savefig('out/assets/map_nuclear.png', facecolor=PAPER); plt.close(fig)

# ------------------------------------------------------------------ 2. debt and deficit under each government
fig, ax = plt.subplots(figsize=(13, 6))
ax.set_xlim(1978, END); ax.set_ylim(-12, 125)
for i, g in enumerate(gov.itertuples()):
    s, e = max(fy(g.start), 1978), (fy(g.end) if g.end else END)
    if g.cohabitation: ax.add_patch(Rectangle((s, -12), e - s, 137, fc=BLUE_SOFT, alpha=.35, lw=0, zorder=0))
    ax.axvline(s, color=LIGHT, lw=.6, zorder=1)
    if e - s > .9:
        ax.text((s + e) / 2, 121, g.prime_minister.split()[-1], fontsize=7, color=MID, ha='center', va='top', rotation=90)
for p in pres.itertuples():
    s = max(fy(p.start), 1978)
    ax.plot([s, s], [-12, 125], color=INK, lw=.9, ls=(0, (2, 2)), zorder=1)
    ax.text(s + .15, 94, p.president.split()[-1] if 'Estaing' not in p.president else 'Giscard', fontsize=8, color=INK, rotation=90, va='top')
ax.bar(a.index, a.public_balance_pct_gdp, color=RED, alpha=.75, width=.7, zorder=2, label='Public balance, % of GDP (negative: deficit)')
ax.plot(a.index, a.public_debt_pct_gdp, color=INK, lw=2.2, zorder=3, label='Public debt, % of GDP (Maastricht)')
for y in (1980, 1995, 2007, 2019, 2025):
    ax.annotate(f'{a.loc[y, "public_debt_pct_gdp"]:.0f}%', (y, a.loc[y, 'public_debt_pct_gdp']), xytext=(-4, 8), textcoords='offset points', fontsize=8.5, ha='center')
ax.axhline(0, color=MID, lw=.6); ax.axhline(60, color=MID, lw=.5, ls=':'); ax.text(1978.3, 61.5, 'Maastricht ceiling, 60%', fontsize=7.5, color=MID)
ax.axhline(-3, color=RED, lw=.5, ls=':'); ax.text(1978.3, -2.4, '−3% rule', fontsize=7.5, color=RED)
ax.set_ylabel('% of GDP'); ax.spines[['top', 'right']].set_visible(False)
ax.legend(handles=ax.get_legend_handles_labels()[0] + [Rectangle((0, 0), 1, 1, fc=BLUE_SOFT, alpha=.6)], labels=ax.get_legend_handles_labels()[1] + ['Cohabitation'],
          loc='lower left', bbox_to_anchor=(0, 1.0), ncol=3, frameon=False, fontsize=8.2)
title(fig, 'Debt and deficits, 1978 to 2025', 'Every year since 1975 has closed in deficit. Debt rises in steps, after the downturns of 1993, 2009 and 2020. Dashed lines: presidents; names: prime ministers.', y=.965)
plt.subplots_adjust(left=.06, right=.985, top=.8, bottom=.07)
fig.savefig('out/assets/debt_governments.png', facecolor=PAPER); plt.close(fig)

# ------------------------------------------------------------------ 3. the economy in four panels
P = [('gdp_growth_pct', 'Real GDP growth, %', INK, 'bar'), ('unemployment_pct', 'Unemployment, % (ILO)', BLUE, 'line'),
     ('cpi_inflation_pct', 'Consumer price inflation, %', RED, 'line'), (('revenue_pct_gdp', 'expenditure_pct_gdp'), 'Public revenue and spending, % of GDP', None, 'two')]
fig, axs = plt.subplots(2, 2, figsize=(12, 7))
for ax, (c, t, col, kind) in zip(axs.flat, P):
    ax.set_xlim(1977.5, 2025.8)
    for p in pres.itertuples(): ax.axvline(max(fy(p.start), 1978), color=LIGHT, lw=.6, ls=(0, (2, 2)))
    if kind == 'bar':
        ax.bar(a.index, a[c], color=[RED if v < 0 else INK for v in a[c]], width=.7); ax.axhline(0, color=MID, lw=.6)
    elif kind == 'line':
        ax.plot(a.index, a[c], color=col, lw=2); ax.set_ylim(0, a[c].max() * 1.15)
    else:
        ax.plot(a.index, a[c[1]], color=RED, lw=2, label='Spending'); ax.plot(a.index, a[c[0]], color=BLUE, lw=2, label='Revenue')
        ax.fill_between(a.index, a[c[0]], a[c[1]], color=RED_SOFT, alpha=.5, lw=0); ax.set_ylim(45, 65); ax.legend(frameon=False, fontsize=8, loc='upper left')
        ax.text(1979, 46.5, 'Eurostat series start in 1995', fontsize=7.5, color=MID)
    ax.set_title(t, fontsize=10, loc='left'); ax.spines[['top', 'right']].set_visible(False); ax.tick_params(labelsize=8)
title(fig, 'The economy since 1978', 'Dotted lines: change of president. Shocks: 1993, 2009, 2020; inflation returns in 2022 after thirty years below 4%.', y=.965)
plt.subplots_adjust(left=.05, right=.98, top=.84, bottom=.06, hspace=.36, wspace=.14)
fig.savefig('out/assets/economy.png', facecolor=PAPER); plt.close(fig)

# ------------------------------------------------------------------ 4. nuclear electricity
en = a[['nuclear_share_electricity_pct', 'nuclear_generation_twh']]
fig, ax = plt.subplots(figsize=(12, 4.8))
ax.fill_between(en.index, 0, en.nuclear_generation_twh, color=BLUE_SOFT, lw=0, label='Nuclear generation, TWh')
ax.plot(en.index, en.nuclear_generation_twh, color=BLUE, lw=1.6)
ax.set_ylim(0, 480); ax.set_ylabel('TWh'); ax.set_xlim(1977.5, 2025.8)
ax2 = ax.twinx(); ax2.plot(en.index, en.nuclear_share_electricity_pct, color=RED, lw=2, label='Share of electricity, %'); ax2.set_ylim(0, 100)
ax2.set_ylabel('% of electricity', color=RED); ax2.tick_params(axis='y', colors=RED)
for y, t in [(1986.3, 'Chernobyl'), (1997, 'Superphénix\nstopped'), (2011.2, 'Fukushima'), (2020.4, 'Fessenheim\nclosed'), (2022.5, 'Corrosion\nchecks'), (2024.7, 'Flamanville 3 ')]:
    yy = {2022.5: 438, 2024.7: 410}.get(y, 470)
    ax.axvline(y, color=MID, lw=.6, ls=':'); ax.text(y + (-.2 if y > 2024 else .2), yy, t, fontsize=7.3, color=MID, va='top', ha='right' if y > 2024 else 'left')
for s_ in (ax, ax2): s_.spines[['top']].set_visible(False)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc='lower left', bbox_to_anchor=(0, 1.0), ncol=2, frameon=False, fontsize=8.2)
title(fig, 'Nuclear power', 'Built mostly between 1977 and 1993; about seven tenths of French electricity since the late 1980s. Share data from 1985.', y=.965)
plt.subplots_adjust(left=.06, right=.94, top=.8, bottom=.08)
fig.savefig('out/assets/nuclear.png', facecolor=PAPER); plt.close(fig)

# ------------------------------------------------------------------ 5. pensions: legal age by generation and old-age spending
fig, (ax, bx) = plt.subplots(1, 2, figsize=(13, 5), gridspec_kw=dict(width_ratios=[1.1, 1]))
ax.step(lg.generation, lg.legal_age_2023_law_years, where='post', color=LIGHT, lw=2, label='Under the 2023 law')
ax.step(lg.generation, lg.legal_age_after_suspension_years, where='post', color=RED, lw=2.2, label='After the 2026 suspension')
ax.set_ylim(59.5, 64.6); ax.set_xlim(1949.5, 1969.8); ax.set_xticks(range(1950, 1970, 5)); ax.set_xlabel('Year of birth'); ax.set_ylabel('Minimum legal retirement age')
ax.text(1950.2, 60.15, '60 since 1983', fontsize=8, color=INK); ax.text(1955.2, 62.15, '62, Woerth reform (2010)', fontsize=8, color=INK)
ax.text(1960.6, 64.15, '64, Borne reform (2023)', fontsize=8, color=MID)
ax.legend(frameon=False, fontsize=8.2, loc='lower right'); ax.set_title('Legal age by generation', fontsize=10, loc='left')
ax.spines[['top', 'right']].set_visible(False)
bx.plot(a.index, a.old_age_spending_pct_gdp, color=BLUE, lw=2, label='Old-age spending (Eurostat, from 1995)')
bx.plot(a.index, a.social_protection_spending_pct_gdp, color=INK, lw=1.4, ls='--', label='All social protection (Eurostat, from 1995)')
bx.set_ylim(0, 37); bx.set_xlim(1979.5, 2026.6); bx.legend(frameon=False, fontsize=8.2, loc='lower right')
for r in pens.itertuples():
    y = int(r.date[:4]) + (int(r.date[5:]) - .5) / 12
    if y < 1979.5: continue
    bx.axvline(y, color=RED, lw=.6, ls=':'); bx.text(y + .2, 36, {'Universal points system': 'Points system', 'Suspension of the 2023 reform': 'Suspension', 'Retirement at 60': 'Age 60'}.get(r.reform, r.reform.replace(' reform', '')),
                                                    rotation=90, fontsize=7, color=RED, va='top')
bx.set_title('Pension spending and the reforms, % of GDP', fontsize=10, loc='left'); bx.spines[['top', 'right']].set_visible(False)
title(fig, 'Pensions', 'Ten reforms since 1982. Old-age pensions take about a seventh of national income, the largest item of public spending.', y=.965)
plt.subplots_adjust(left=.06, right=.985, top=.82, bottom=.11, wspace=.18)
fig.savefig('out/assets/pensions.png', facecolor=PAPER); plt.close(fig)

# ------------------------------------------------------------------ 6. scatter-plot matrix, 1980 to 2025
a['debt_change_pts'] = a.public_debt_pct_gdp.diff()
V = [('gdp_growth_pct', 'GDP growth\n(%)'), ('unemployment_pct', 'Unemployment\n(%)'), ('cpi_inflation_pct', 'Inflation\n(%)'),
     ('public_balance_pct_gdp', 'Public balance\n(% of GDP)'), ('debt_change_pts', 'Change in debt\n(points of GDP)')]
d = a.loc[1980:2025].dropna(subset=[v for v, _ in V]).copy()
DEC = {'1980s': (1980, 1989, INK), '1990s': (1990, 1999, BLUE), '2000s': (2000, 2009, MID), '2010s': (2010, 2019, RED_SOFT), '2020s': (2020, 2029, RED)}
d['dec'] = [next(k for k, (lo, hi, _) in DEC.items() if lo <= y <= hi) for y in d.index]
k = len(V)
fig, axs = plt.subplots(k, k, figsize=(11, 11))
for i, (vi, li) in enumerate(V):
    for j, (vj, lj) in enumerate(V):
        ax = axs[i, j]; x, y = d[vj].astype(float), d[vi].astype(float)
        if i == j:
            lo, hi = x.min(), x.max(); pad = (hi - lo) * .06
            ax.set_xlim(lo - pad, hi + pad); ax.set_ylim(lo - pad, hi + pad)
            hx = ax.twinx(); hx.set_yticks([]); hx.spines[['top', 'right', 'left']].set_visible(False)
            e = np.histogram_bin_edges(x, 12)
            hx.hist([x[d.dec == kk] for kk in DEC], bins=e, color=[c for _, _, c in DEC.values()], stacked=True, edgecolor=PAPER)
        else:
            for kk, (_, _, c) in DEC.items():
                m = d.dec == kk; ax.scatter(x[m], y[m], s=16, c=c, alpha=.9, lw=0)
            r = np.corrcoef(x, y)[0, 1]; ax.text(.04, .88, f'r = {r:.2f}', transform=ax.transAxes, fontsize=7.5, color=INK)
        ax.tick_params(labelsize=6.5, length=2)
        if i < k - 1: ax.set_xticklabels([])
        if j > 0: ax.set_yticklabels([])
        if i == k - 1: ax.set_xlabel(lj, fontsize=8)
        if j == 0: ax.set_ylabel(li, fontsize=8)
        ax.spines[['top', 'right']].set_visible(False)
fig.legend(handles=[Line2D([], [], marker='o', ls='', c=c, label=kk) for kk, (_, _, c) in DEC.items()], loc='upper right', bbox_to_anchor=(.98, .935), ncol=5, frameon=False, fontsize=8.5)
title(fig, 'What moves with what, 1980 to 2025', f'{len(d)} years. Colour: decade. r: Pearson correlation. Deficits and debt jumps follow recessions.', y=.965)
plt.subplots_adjust(left=.1, right=.98, top=.88, bottom=.08, wspace=.08, hspace=.08)
fig.savefig('out/assets/scatter_matrix.png', facecolor=PAPER); plt.close(fig)

# ------------------------------------------------------------------ 7. debt: who owes it, and the neighbours
fig, (ax, bx) = plt.subplots(1, 2, figsize=(13, 4.8))
ax.stackplot(sub.index, sub.central_government, sub.social_security, sub.local_government, colors=[BLUE, RED, LIGHT], labels=['State and central bodies', 'Social security', 'Local government'], lw=0)
ax.set_xlim(1978, 2022); ax.set_ylim(0, 125); ax.legend(frameon=False, fontsize=8.2, loc='upper left'); ax.set_title('Public debt by sub-sector, % of GDP (INSEE, to 2022)', fontsize=10, loc='left')
ax.spines[['top', 'right']].set_visible(False)
ST = {'FR': (INK, 2.4, 'France'), 'DE': (BLUE, 1.5, 'Germany'), 'IT': (RED, 1.5, 'Italy'), 'ES': (MID, 1.5, 'Spain'), 'EA20': (LIGHT, 1.5, 'Euro area')}
for g, (c, lw, lab) in ST.items():
    s = peers[peers.geo == g].set_index('year').public_debt_pct_gdp
    bx.plot(s.index, s.values, color=c, lw=lw); bx.annotate(f'{lab} {s.iloc[-1]:.0f}%', (s.index[-1], s.iloc[-1]), xytext=(5, 0), textcoords='offset points', fontsize=8, color=c, va='center')
bx.set_xlim(1995, 2029.5); bx.set_ylim(0, 160); bx.set_title('Public debt in the euro area, % of GDP (Eurostat)', fontsize=10, loc='left'); bx.spines[['top', 'right']].set_visible(False)
title(fig, 'Who owes the debt', 'Most of it is the State\'s; the social security share grows from the 1990s. Among large euro economies, France moves from the middle of the pack to second place.', y=.965)
plt.subplots_adjust(left=.05, right=.97, top=.8, bottom=.08, wspace=.16)
fig.savefig('out/assets/debt_structure.png', facecolor=PAPER); plt.close(fig)
print('ok')
