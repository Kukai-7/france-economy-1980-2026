# France 1980 to 2026: Governments, Debt and the Economy

[Dataset on Hugging Face](https://huggingface.co/datasets/Kukai-7/france-economy-1980-2026) · code in this repository

**How did the French economy, public finances, pensions and electricity change across six presidents and twenty-three prime ministers?** This dataset puts official series for 1978 to 2025 next to the calendar of governments, the pension reforms and the nuclear fleet, in one place and without commentary on who was right.

*L'économie française de 1980 à 2026, gouvernement par gouvernement, sans parti pris.*

![Debt and deficits, 1978 to 2025](https://huggingface.co/datasets/Kukai-7/france-economy-1980-2026/resolve/main/assets/debt_governments.png)

## At a glance

| | |
|---|---|
| Period | 1978 to 2025, annual; governments to October 2026 |
| Public finances | Debt and balance (INSEE before 1995, Eurostat after), revenue, spending, social protection, pensions, health, education, defence |
| Economy | Growth, inflation, unemployment (ILO), GDP per head |
| Energy | Nuclear share of electricity and generation; 23 nuclear sites with coordinates |
| Politics | 6 presidents, 23 prime ministers, 3 cohabitations |
| Pensions | 10 reforms, legal age by generation before and after the 2026 suspension |
| Format | Parquet, eight configurations |

## What it shows

- **Debt rises in steps.** Public debt goes from 21% of GDP in 1980 to 116% in 2025. The largest one-year jumps follow the recessions of 1993 (+6 points), 2009 (+14) and 2020 (+17); the ratio was never brought back down to its level before each shock.
- **No surplus since 1974.** Every year from 1975 has closed in deficit, under every majority. The deficit was smaller than 3% of GDP in 19 of the 48 years covered.
- **Growth slows decade after decade.** Average real growth: 2.4% in the 1980s, 2.1% in the 1990s, 1.6% in the 2000s, 1.4% in the 2010s, 0.9% so far in the 2020s.
- **Unemployment high but lower.** The ILO rate climbs from 4.7% in 1978 to a peak of 10.6% in 1997, back to about 10% from 2013 to 2016, and stands around 7.5% in 2025.
- **Spending above 55% of GDP.** Public spending is 57% of GDP in 2025, revenue 52%; old-age pensions alone are about 13% of GDP, the largest single item.
- **Nuclear power, built in fifteen years.** Most of the 57 reactors running today came online between 1977 and 1993; nuclear has produced about seven tenths of the country's electricity since the late 1980s, with a low of 63% in 2022 during the corrosion checks.

![The economy since 1978](https://huggingface.co/datasets/Kukai-7/france-economy-1980-2026/resolve/main/assets/economy.png)

![Fifty-seven reactors on eighteen sites](https://huggingface.co/datasets/Kukai-7/france-economy-1980-2026/resolve/main/assets/map_nuclear.png)

![Nuclear power](https://huggingface.co/datasets/Kukai-7/france-economy-1980-2026/resolve/main/assets/nuclear.png)

![Pensions](https://huggingface.co/datasets/Kukai-7/france-economy-1980-2026/resolve/main/assets/pensions.png)

![Who owes the debt](https://huggingface.co/datasets/Kukai-7/france-economy-1980-2026/resolve/main/assets/debt_structure.png)

![What moves with what, 1980 to 2025](https://huggingface.co/datasets/Kukai-7/france-economy-1980-2026/resolve/main/assets/scatter_matrix.png)

## Load it

```python
from datasets import load_dataset

france = load_dataset("Kukai-7/france-economy-1980-2026", "annual", split="train").to_pandas()
governments = load_dataset("Kukai-7/france-economy-1980-2026", "governments", split="train").to_pandas()

# Debt ratio when each president took office
france.groupby("president", sort=False).public_debt_pct_gdp.first()
```

## Configurations

### `annual` (default), 48 rows, 1978 to 2025

| column | description |
|---|---|
| `public_debt_pct_gdp`, `public_debt_source` | Maastricht gross debt; Eurostat from 1995, INSEE (base 2014) before |
| `public_balance_pct_gdp` | Net lending (+) or borrowing (−) of general government, same sources |
| `revenue_pct_gdp`, `expenditure_pct_gdp` | Total revenue and spending, Eurostat, from 1995 |
| `social_protection_spending_pct_gdp`, `old_age_spending_pct_gdp`, `health_spending_pct_gdp`, `education_spending_pct_gdp`, `defence_spending_pct_gdp` | Spending by function (COFOG), Eurostat, from 1995 |
| `gdp_growth_pct`, `cpi_inflation_pct`, `gdp_per_capita_usd2015` | World Bank |
| `unemployment_pct` | ILO unemployment rate, France excluding Mayotte, average of four quarters, INSEE |
| `nuclear_share_electricity_pct`, `nuclear_generation_twh`, `fossil_share_electricity_pct` | Our World in Data (Ember, Energy Institute); shares from 1985 |
| `president`, `prime_minister_mid_year`, `cohabitation_mid_year` | Who was in office on 1 July |

### `governments`, 23 rows, and `presidents`, 6 rows

Name, party and political family at appointment, start and end dates, president, cohabitation flag, and for prime ministers the averages of growth, unemployment and public balance over the full calendar years they held office (`full_calendar_years` says how many; short tenures have none).

### `pension_reforms`, 10 rows, and `legal_age_by_generation`, 16 rows

Date, name, prime minister and content of each reform since 1982; minimum legal age and quarters required by year of birth under the 2023 law and after the suspension voted in December 2025.

### `nuclear_sites`, 23 rows

Site, Wikidata identifier, coordinates, capacity in MW (as recorded in Wikidata), year of the first unit, year of closure, power reactors in service in 2026 and status.

### `debt_by_subsector` and `debt_peers`

Debt of the State and central bodies, local government and social security, 1978 to 2022 (INSEE); debt of France, Germany, Italy, Spain and the euro area, 1995 to 2025 (Eurostat).

## How it was built

1. **Public finances.** [INSEE](https://www.insee.fr/) national accounts (base 2014) through its open SDMX service for 1978 to 1994 and the sub-sectors; [Eurostat](https://ec.europa.eu/eurostat) (`gov_10dd_edpt1`, `gov_10a_main`, `gov_10a_exp`) from 1995, downloaded in October 2026.
2. **Economy.** World Bank Open Data for growth, inflation and GDP per head; INSEE quarterly ILO unemployment.
3. **Energy.** [Our World in Data energy dataset](https://github.com/owid/energy-data) for generation and shares; Wikidata for the sites, with reactor counts set by hand.
4. **Politics and pensions.** Dates of presidents, prime ministers and reforms curated for this dataset from official sources (Légifrance, vie-publique.fr, service-public.fr) and the press; legal ages by generation from the 2010 and 2023 laws and the 2026 social security budget (loi n° 2025-1403 du 30 décembre 2025).
5. **Charts.** Python and Matplotlib; borders from Natural Earth. The pipeline is in [`code/`](./).

## Limitations

- **Governments do not set the cycle.** Growth, unemployment and deficits depend on world demand, interest rates, oil prices, the pandemic and decisions taken years earlier. The per-government averages describe the years in office; they do not measure what a government caused, and the dataset makes no such claim.
- **A break in 1995.** The debt series switches from INSEE base 2014 to Eurostat in 1995; the two differ by about 1.7 points of GDP that year.
- **Spending by function from 1995 only.** Older figures exist in INSEE's archives but follow other definitions.
- **Unemployment scope.** The long series covers France excluding Mayotte, so that 1978 and 2025 are comparable.
- **Pension ages by generation for 1964 to 1968** come from summaries of the December 2025 law; the path after 1 January 2028 depends on future legislation.
- **Nuclear capacities** are Wikidata's figures and mix net and gross values; the reactor counts are the reliable column.
- **Correlation only.** The scatter-plot matrix describes 46 years; it does not identify causes.

## Credits and licences

- INSEE (Licence Ouverte 2.0), Eurostat (CC BY 4.0), World Bank (CC BY 4.0), Our World in Data (CC BY 4.0), Wikidata (CC0), Natural Earth (public domain).
- This compilation, curated tables and charts: CC BY 4.0.

## Related

- [China under Deng](https://huggingface.co/datasets/Kukai-7/deng-era-china), money and growth in China, 1978 to 1997.
- [BoJ Tone Tracker](https://huggingface.co/spaces/Kukai-7/boj-tone-tracker), Bank of Japan statements read by a language model.
- [GitHub: Kukai-7](https://github.com/Kukai-7)
