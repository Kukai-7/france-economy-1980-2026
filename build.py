"""Build the France 1980-2026 dataset from raw/bundle.json (INSEE, Eurostat, World Bank, Wikidata)
and raw/owid-energy-data.csv (Our World in Data, from Ember and the Energy Institute), plus curated tables."""
import io, json, os, numpy as np, pandas as pd

RAW, OUT = 'raw', 'out/data'
os.makedirs(OUT, exist_ok=True)
B = json.load(open(f'{RAW}/bundle.json'))
Y0, Y1 = 1978, 2025

def insee(key): return pd.Series({int(t): v for t, v in B[key]}).sort_index()
def es(key, **flt):
    ids = B[key]['ids']; rows = []
    for r in B[key]['rows']:
        d = dict(zip(ids + ['value'], r))
        if all(d[k] == v for k, v in flt.items()): rows.append((int(d['time']), d['value']))
    return pd.Series(dict(rows)).sort_index()
def wb(key, iso): return pd.Series({y: v for c, y, v in B[key] if c == iso}).sort_index()

# ------------------------------------------------------------------ governments (curated)
PRES = [('Valéry Giscard d\'Estaing', 'UDF', 'centre-right', '1974-05-27', '1981-05-21'), ('François Mitterrand', 'PS', 'left', '1981-05-21', '1995-05-17'),
        ('Jacques Chirac', 'RPR, then UMP', 'right', '1995-05-17', '2007-05-16'), ('Nicolas Sarkozy', 'UMP', 'right', '2007-05-16', '2012-05-15'),
        ('François Hollande', 'PS', 'left', '2012-05-15', '2017-05-14'), ('Emmanuel Macron', 'En Marche, then Renaissance', 'centre', '2017-05-14', None)]
PM = [('Raymond Barre', 'no party (UDF-aligned)', 'centre-right', '1976-08-25', '1981-05-21'), ('Pierre Mauroy', 'PS', 'left', '1981-05-22', '1984-07-17'),
      ('Laurent Fabius', 'PS', 'left', '1984-07-17', '1986-03-20'), ('Jacques Chirac', 'RPR', 'right', '1986-03-20', '1988-05-10'),
      ('Michel Rocard', 'PS', 'left', '1988-05-10', '1991-05-15'), ('Édith Cresson', 'PS', 'left', '1991-05-15', '1992-04-02'),
      ('Pierre Bérégovoy', 'PS', 'left', '1992-04-02', '1993-03-29'), ('Édouard Balladur', 'RPR', 'right', '1993-03-29', '1995-05-17'),
      ('Alain Juppé', 'RPR', 'right', '1995-05-17', '1997-06-02'), ('Lionel Jospin', 'PS', 'left', '1997-06-02', '2002-05-06'),
      ('Jean-Pierre Raffarin', 'UMP', 'right', '2002-05-06', '2005-05-31'), ('Dominique de Villepin', 'UMP', 'right', '2005-05-31', '2007-05-17'),
      ('François Fillon', 'UMP', 'right', '2007-05-17', '2012-05-15'), ('Jean-Marc Ayrault', 'PS', 'left', '2012-05-15', '2014-03-31'),
      ('Manuel Valls', 'PS', 'left', '2014-03-31', '2016-12-06'), ('Bernard Cazeneuve', 'PS', 'left', '2016-12-06', '2017-05-15'),
      ('Édouard Philippe', 'LR, then no party', 'centre-right', '2017-05-15', '2020-07-03'), ('Jean Castex', 'LREM', 'centre', '2020-07-03', '2022-05-16'),
      ('Élisabeth Borne', 'Renaissance', 'centre', '2022-05-16', '2024-01-09'), ('Gabriel Attal', 'Renaissance', 'centre', '2024-01-09', '2024-09-05'),
      ('Michel Barnier', 'LR', 'right', '2024-09-05', '2024-12-13'), ('François Bayrou', 'MoDem', 'centre', '2024-12-13', '2025-09-09'),
      ('Sébastien Lecornu', 'Renaissance', 'centre', '2025-09-09', None)]
pres = pd.DataFrame(PRES, columns=['president', 'party', 'family', 'start', 'end'])
gov = pd.DataFrame(PM, columns=['prime_minister', 'party', 'family', 'start', 'end'])
for d in (pres, gov):
    d['start'] = pd.to_datetime(d.start); d['end'] = pd.to_datetime(d.end)
def president_at(t): return pres[(pres.start <= t) & (pres.end.isna() | (pres.end > t))].iloc[0]
gov['president'] = gov.start.map(lambda t: president_at(t + pd.Timedelta(days=1)).president)
gov['cohabitation'] = gov.prime_minister.isin(['Jacques Chirac', 'Édouard Balladur', 'Lionel Jospin'])
gov['note'] = np.where(gov.prime_minister == 'Sébastien Lecornu', 'Resigned on 6 October 2025 and reappointed on 10 October 2025', '')

# ------------------------------------------------------------------ annual panel
yrs = pd.Index(range(Y0, Y1 + 1), name='year')
a = pd.DataFrame(index=yrs)
debt_es, debt_in = es('es_debt', na_item='GD', geo='FR'), insee('insee_010562164')
a['public_debt_pct_gdp'] = debt_es.reindex(yrs).fillna(debt_in.reindex(yrs))
a['public_debt_source'] = np.where(debt_es.reindex(yrs).notna(), 'Eurostat', 'INSEE base 2014')
def_es, def_in = es('es_debt', na_item='B9', geo='FR'), insee('insee_010562129')
a['public_balance_pct_gdp'] = def_es.reindex(yrs).fillna(def_in.reindex(yrs))
a['revenue_pct_gdp'] = es('es_main', na_item='TR').reindex(yrs)
a['expenditure_pct_gdp'] = es('es_main', na_item='TE').reindex(yrs)
for code, col in [('GF10', 'social_protection_spending_pct_gdp'), ('GF1002', 'old_age_spending_pct_gdp'), ('GF07', 'health_spending_pct_gdp'),
                  ('GF09', 'education_spending_pct_gdp'), ('GF02', 'defence_spending_pct_gdp')]:
    a[col] = es('es_exp', cofog99=code).reindex(yrs)
a['gdp_growth_pct'] = wb('wb_FRA_NY.GDP.MKTP.KD.ZG', 'FRA').reindex(yrs).round(3)
a['cpi_inflation_pct'] = wb('wb_FRA_FP.CPI.TOTL.ZG', 'FRA').reindex(yrs).round(3)
a['gdp_per_capita_usd2015'] = wb('wb_FRA_NY.GDP.PCAP.KD', 'FRA').reindex(yrs).round(1)
u = pd.DataFrame(B['insee_unemp'], columns=['q', 'v']); u['year'] = u.q.str[:4].astype(int)
uy = u.groupby('year').agg(v=('v', 'mean'), n=('v', 'size'))
a['unemployment_pct'] = uy.v.where(uy.n == 4).reindex(yrs).round(2)
en = pd.read_csv(f'{RAW}/owid-energy-data.csv'); en = en[en.country == 'France'].set_index('year')
a['nuclear_share_electricity_pct'] = en.nuclear_share_elec.reindex(yrs).round(2)
a['nuclear_generation_twh'] = en.nuclear_electricity.reindex(yrs).round(2)
a['fossil_share_electricity_pct'] = en.fossil_share_elec.reindex(yrs).round(2)
mid = pd.to_datetime([f'{y}-07-01' for y in yrs])
a['president'] = [president_at(t).president for t in mid]
a['prime_minister_mid_year'] = [gov[(gov.start <= t) & (gov.end.isna() | (gov.end > t))].iloc[0].prime_minister for t in mid]
a['cohabitation_mid_year'] = a.prime_minister_mid_year.map(gov.drop_duplicates('prime_minister', keep='last').set_index('prime_minister').cohabitation)
a.loc[a.prime_minister_mid_year == 'Jacques Chirac', 'cohabitation_mid_year'] = True
a = a.reset_index()
a.to_parquet(f'{OUT}/annual.parquet', index=False)

# ------------------------------------------------------------------ figures by government: descriptive, start and end of tenure
ann = a.set_index('year')
def yr(t): return t.year + (t.dayofyear - 1) / 365.25
rows = []
for g in gov.itertuples():
    s, e = g.start, (g.end if pd.notna(g.end) else pd.Timestamp('2026-10-01'))
    y0, y1 = s.year if s.month <= 6 else s.year + 1, e.year if e.month > 6 else e.year - 1
    span = ann.loc[max(y0, Y0):min(y1, Y1)] if y1 >= y0 else ann.iloc[0:0]
    rows.append(dict(prime_minister=g.prime_minister, start=s.date().isoformat(), end=None if pd.isna(g.end) else g.end.date().isoformat(),
                     years_in_office=round((e - s).days / 365.25, 2), full_calendar_years=len(span),
                     avg_gdp_growth_pct=round(span.gdp_growth_pct.mean(), 2) if len(span) else None,
                     avg_unemployment_pct=round(span.unemployment_pct.mean(), 2) if len(span) else None,
                     avg_public_balance_pct_gdp=round(span.public_balance_pct_gdp.mean(), 2) if len(span) else None))
gstats = pd.DataFrame(rows)
gov_out = gov.copy(); gov_out['start'] = gov_out.start.dt.date.astype(str); gov_out['end'] = gov_out.end.dt.date.astype(str).replace('NaT', None)
gov_out = gov_out.merge(gstats.drop(columns=['start', 'end']), on='prime_minister', how='left')
gov_out.to_parquet(f'{OUT}/governments.parquet', index=False)
pres_out = pres.copy(); pres_out['start'] = pres_out.start.dt.date.astype(str); pres_out['end'] = pres_out.end.dt.date.astype(str).replace('NaT', None)
pres_out.to_parquet(f'{OUT}/presidents.parquet', index=False)

# ------------------------------------------------------------------ public debt by sub-sector (INSEE base 2014) and peers (Eurostat)
sub = pd.DataFrame({'central_government': insee('insee_010562166'), 'local_government': insee('insee_010562172'),
                    'social_security': insee('insee_010562174'), 'total': insee('insee_010562164')}).rename_axis('year').reset_index()
sub.to_parquet(f'{OUT}/debt_by_subsector.parquet', index=False)
peers = pd.concat([es('es_debt_eu', geo=g).rename(g) for g in ['DE', 'IT', 'ES', 'EA20']] + [debt_es.rename('FR')], axis=1).rename_axis('year').reset_index()
peers = peers.melt(id_vars='year', var_name='geo', value_name='public_debt_pct_gdp').dropna()
peers.to_parquet(f'{OUT}/debt_peers.parquet', index=False)

# ------------------------------------------------------------------ pensions (curated)
P = [('1982-03', 'Retirement at 60', 'Mauroy', 'Legal age lowered from 65 to 60 from April 1983, with 37.5 years of contributions for a full pension.'),
     ('1993-07', 'Balladur reform', 'Balladur', 'Private sector: contribution period raised to 40 years, pension based on the best 25 years, indexation on prices.'),
     ('1995-12', 'Juppé plan', 'Juppé', 'Plan to align special regimes; withdrawn on pensions after weeks of strikes.'),
     ('2003-08', 'Fillon reform', 'Raffarin', 'Public sector aligned on 40 years; early departure for long careers.'),
     ('2008-01', 'Special regimes', 'Fillon', 'Contribution periods of several special regimes aligned on the public sector.'),
     ('2010-11', 'Woerth reform', 'Fillon', 'Legal age raised from 60 to 62, full-rate age from 65 to 67, step by step.'),
     ('2014-01', 'Touraine reform', 'Ayrault', 'Contribution period raised to 43 years by the 1973 generation.'),
     ('2020-03', 'Universal points system', 'Philippe', 'Adopted at first reading by the Assembly without a vote (article 49.3), then suspended with the pandemic and dropped.'),
     ('2023-04', 'Borne reform', 'Borne', 'Legal age raised from 62 to 64 by the 1968 generation and 43 years reached faster; passed without a vote (article 49.3).'),
     ('2025-12', 'Suspension of the 2023 reform', 'Lecornu', 'Social security budget for 2026: legal age frozen at 62 years and 9 months until 1 January 2028.')]
pens = pd.DataFrame(P, columns=['date', 'reform', 'prime_minister', 'description'])
pens.to_parquet(f'{OUT}/pension_reforms.parquet', index=False)
G = [(1950, '60y', '60y', 160), (1951, '60y4m', '60y4m', 163), (1952, '60y9m', '60y9m', 164), (1953, '61y2m', '61y2m', 165), (1954, '61y7m', '61y7m', 165),
     (1955, '62y', '62y', 166), (1958, '62y', '62y', 167), (1960, '62y', '62y', 167), (1961, '62y3m', '62y3m', 169), (1962, '62y6m', '62y6m', 169),
     (1963, '62y9m', '62y9m', 170), (1964, '63y', '62y9m', 170), (1966, '63y6m', '63y3m', 171), (1967, '63y9m', '63y6m', 172), (1968, '64y', '63y9m', 172), (1969, '64y', '64y', 172)]
def months(s): y, m = (s.replace('y', ' ').replace('m', '').split() + ['0'])[:2]; return int(y) * 12 + int(m)
lg = pd.DataFrame(G, columns=['generation', 'legal_age_2023_law', 'legal_age_after_2026_suspension', 'quarters_required'])
lg['legal_age_2023_law_years'] = (lg.legal_age_2023_law.map(months) / 12).round(3)
lg['legal_age_after_suspension_years'] = (lg.legal_age_after_2026_suspension.map(months) / 12).round(3)
lg.to_parquet(f'{OUT}/legal_age_by_generation.parquet', index=False)

# ------------------------------------------------------------------ nuclear sites (Wikidata, reactor counts set by hand)
REACT = {'Gravelines': 6, 'Paluel': 4, 'Penly': 2, 'Flamanville': 3, 'Chooz': 2, 'Cattenom': 4, 'Nogent': 2, 'Dampierre': 4, 'Belleville': 2,
         'Saint-Laurent-des-Eaux': 2, 'Chinon': 4, 'Civaux': 2, 'Blayais': 4, 'Golfech': 2, 'Bugey': 4, 'Saint-Alban': 2, 'Cruas': 4,
         'Tricastin': 4, 'Fessenheim': 2}
nk = []
for r in B['wd_nuke']:
    if not r.get('coord') or 'projet' in r['name']: continue
    lon, lat = map(float, r['coord'].replace('Point(', '').replace(')', '').split())
    short = r['name'].replace('centrale nucléaire de ', '').replace('centrale nucléaire du ', '').replace('centrale nucléaire des ', '').replace('site nucléaire de ', '')
    nk.append(dict(site=short, wikidata=r['qid'], latitude=round(lat, 4), longitude=round(lon, 4), capacity_mw=float(r['cap']) if r.get('cap') else None,
                   first_in_service=int(r['start'][:4]) if r.get('start') else None, closed=int(r['end'][:4]) if r.get('end') else None,
                   power_reactors_in_2026=0 if r.get('end') else REACT.get(short, 0)))
nuke = pd.DataFrame(nk).sort_values(['first_in_service', 'site']).reset_index(drop=True)
nuke['status'] = np.where(nuke.closed.notna(), 'closed', 'operating')
nuke.to_parquet(f'{OUT}/nuclear_sites.parquet', index=False)

stats = dict(debt_1980=float(ann.loc[1980, 'public_debt_pct_gdp']), debt_2025=float(ann.loc[2025, 'public_debt_pct_gdp']),
             reactors=int(nuke.power_reactors_in_2026.sum()), last_surplus=int(def_in[def_in >= 0].index.max()))
json.dump(stats, open('out/stats.json', 'w'), indent=1)
print(stats, len(a), len(gov_out))
