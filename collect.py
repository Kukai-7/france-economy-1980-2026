"""Download the raw inputs of build.py into raw/ (INSEE SDMX, Eurostat, World Bank, Our World in Data, Wikidata, Natural Earth). No key needed."""
import json, os, re, requests

def insee_flow(flow):
    return requests.get(f'https://bdm.insee.fr/series/sdmx/data/{flow}', timeout=120).text
def insee_series(xml, idbank):
    m = re.search(r'<Series [^>]*IDBANK="' + idbank + r'"[^>]*>([\s\S]*?)</Series>', xml)
    return [[t, float(v)] for t, v in re.findall(r'TIME_PERIOD="([^"]+)"[^>]*OBS_VALUE="([^"]*)"', m.group(1))]
def eurostat(ds, qs):
    j = requests.get(f'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{ds}?{qs}&format=JSON&lang=EN', timeout=120).json()
    ids, size = j['id'], j['size']
    dims = [[k for k, _ in sorted(j['dimension'][d]['category']['index'].items(), key=lambda e: e[1])] for d in ids]
    rows = []
    for k, v in j['value'].items():
        i, lab = int(k), [None] * len(ids)
        for d in range(len(ids) - 1, -1, -1):
            lab[d] = dims[d][i % size[d]]; i //= size[d]
        rows.append(lab + [v])
    return dict(ids=ids, rows=rows, updated=j.get('updated'))
def wb(countries, ind):
    rows = requests.get(f'https://api.worldbank.org/v2/country/{countries}/indicator/{ind}?format=json&per_page=2000&date=1960:2026', timeout=60).json()[1] or []
    return [[r['countryiso3code'], int(r['date']), float(f"{float(r['value']):.6g}")] for r in rows if r['value'] is not None]

if __name__ == '__main__':
    os.makedirs('raw', exist_ok=True)
    O = {}
    dette, cho = insee_flow('CNA-2014-DETTE-APU'), insee_flow('CHOMAGE-TRIM-NATIONAL')
    for i in ['010562164', '010562166', '010562172', '010562174', '010562129']: O['insee_' + i] = insee_series(dette, i)
    O['insee_unemp'] = insee_series(cho, '001688527')
    O['es_debt'] = eurostat('gov_10dd_edpt1', 'geo=FR&unit=PC_GDP&sector=S13&na_item=GD&na_item=B9')
    O['es_exp'] = eurostat('gov_10a_exp', 'geo=FR&unit=PC_GDP&sector=S13&na_item=TE&cofog99=TOTAL&cofog99=GF10&cofog99=GF1002&cofog99=GF07&cofog99=GF09&cofog99=GF02')
    O['es_main'] = eurostat('gov_10a_main', 'geo=FR&unit=PC_GDP&sector=S13&na_item=TR&na_item=TE&na_item=D995')
    O['es_debt_eu'] = eurostat('gov_10dd_edpt1', 'geo=DE&geo=IT&geo=ES&geo=EA20&unit=PC_GDP&sector=S13&na_item=GD')
    for ind in ['NY.GDP.MKTP.KD.ZG', 'FP.CPI.TOTL.ZG', 'NY.GDP.PCAP.KD']: O['wb_FRA_' + ind] = wb('FRA;DEU;GBR;ITA', ind)
    q = ('SELECT ?p ?pLabel ?coord ?cap ?start ?end WHERE { ?p wdt:P31/wdt:P279* wd:Q134447; wdt:P17 wd:Q142. OPTIONAL{?p wdt:P625 ?coord} '
         'OPTIONAL{?p wdt:P2109 ?cap} OPTIONAL{?p wdt:P729 ?start} OPTIONAL{?p wdt:P730 ?end} SERVICE wikibase:label { bd:serviceParam wikibase:language "fr,en". } }')
    b = requests.get('https://query.wikidata.org/sparql', params=dict(format='json', query=q), timeout=120).json()['results']['bindings']
    O['wd_nuke'] = [dict(qid=x['p']['value'].split('/')[-1], name=x.get('pLabel', {}).get('value'), coord=x.get('coord', {}).get('value'),
                         cap=x.get('cap', {}).get('value'), start=x.get('start', {}).get('value'), end=x.get('end', {}).get('value')) for x in b]
    json.dump(O, open('raw/bundle.json', 'w'))
    for name, url in [('owid-energy-data.csv', 'https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv'),
                      ('ne_50m_admin_0_countries.geojson', 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson')]:
        open(f'raw/{name}', 'wb').write(requests.get(url, timeout=300).content)
    print({k: len(v) for k, v in O.items()})
