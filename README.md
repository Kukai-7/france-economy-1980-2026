# France 1980 to 2026: Governments, Debt and the Economy

[Dataset on Hugging Face](https://huggingface.co/datasets/Kukai-7/france-economy-1980-2026) · code in this repository

**How did the French economy, public finances, pensions and electricity change across six presidents and twenty-three prime ministers?** This dataset puts official series for 1978 to 2025 next to the calendar of governments, the pension reforms and the nuclear fleet, in one place and without commentary on who was right.

*L'économie française de 1980 à 2026, gouvernement par gouvernement, sans parti pris.*

![Debt and deficits, 1978 to 2025](https://huggingface.co/datasets/Kukai-7/france-economy-1980-2026/resolve/main/assets/debt_governments.png)

*Reading the chart: the black line is public debt, the bars below zero the yearly deficit, both as a share of GDP; dashed lines mark presidents, names along the top the prime ministers, grey bands the cohabitations. Debt rises in steps after 1993, 2009 and 2020 and is never brought back down.*

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

*Reading the chart: four panels, with dotted lines at each change of president. Growth dips in 1993, 2009 and 2020; unemployment stays between 7% and 11% from the mid-1980s; inflation falls below 4% from 1986 to 2021; spending (red) exceeds revenue (blue) every year, the gap being the deficit.*

![Fifty-seven reactors on eighteen sites](https://huggingface.co/datasets/Kukai-7/france-economy-1980-2026/resolve/main/assets/map_nuclear.png)

*Reading the map: circle size is the number of reactors in service, colour the decade of the first unit, hollow circles the closed sites. Sites sit on large rivers or the coast, for cooling water.*

![Nuclear power](https://huggingface.co/datasets/Kukai-7/france-economy-1980-2026/resolve/main/assets/nuclear.png)

*Reading the chart: the blue area is nuclear generation in TWh (left axis), the red line its share of electricity (right axis). The fleet was built between 1977 and 1993; output dips in 2022 during the corrosion checks.*

![Pensions](https://huggingface.co/datasets/Kukai-7/france-economy-1980-2026/resolve/main/assets/pensions.png)

*Reading the chart: left, the minimum legal age by year of birth, under the 2023 law (grey) and after the 2026 suspension (red); right, old-age and total social protection spending as a share of GDP, with the reforms marked.*

![Who owes the debt](https://huggingface.co/datasets/Kukai-7/france-economy-1980-2026/resolve/main/assets/debt_structure.png)

*Reading the chart: left, debt by sub-sector, mostly the State, with social security growing from the 1990s; right, France against its euro-area neighbours, where it moves from the middle of the pack to second place behind Italy.*

![What moves with what, 1980 to 2025](https://huggingface.co/datasets/Kukai-7/france-economy-1980-2026/resolve/main/assets/scatter_matrix.png)

*Reading the chart: see "Reading the correlations" below. The strong links are the cyclical ones: weak growth, larger deficit, more debt.*

## Reading the correlations

**How to read r.** Pearson's r measures how closely two variables move along a straight line: +1 is a perfect positive line, 0 no linear link, -1 a perfect negative line. r² is the share of the variance of one variable that a straight line on the other accounts for (r = 0.7 means about half). The labels used here: under 0.1 negligible, 0.1 to 0.3 weak, 0.3 to 0.5 moderate, 0.5 to 0.7 strong, 0.7 and above very strong.

**How sure is it?** The 95% confidence interval gives the range of r compatible with the data; when it excludes zero, p is below 0.05 and the link is distinguishable from chance. Strength and certainty are different things: a weak r can be certain with many observations, and a strong r can be uncertain with few. Spearman's ρ repeats the exercise on ranks, so a large gap between r and ρ points to outliers or a curved relationship.

**Yearly changes.** Two series that both trend upward will correlate even if they are unrelated. The last column correlates the year-on-year changes instead, which removes shared trends: a link that survives in changes is more convincing than one that exists only in levels.

In the scatter-plot matrix (`scatter_matrix.png`), the panels below the diagonal show the points with a least-squares line, the diagonal shows each distribution, and the panels above the diagonal give r, its 95% confidence interval, p and n for the pair in that row and column. A figure is in colour only when p < 0.05.

**What stands out**

- **Recessions make debt.** Growth and the change in debt correlate at -0.80 (95% CI -0.89 to -0.67), and at -0.85 in yearly changes: a year of weak growth is a year of fast debt accumulation.
- **The deficit follows the cycle.** Growth and the public balance correlate at +0.51 (+0.57 in changes); the balance and the change in debt at -0.64.
- **Unemployment and inflation move in opposite directions (-0.65)**, a Phillips-curve pattern driven by the high-inflation, lower-unemployment 1980s; it weakens but holds in changes (-0.48).
- **Growth and unemployment are not linked year by year (+0.01).** Unemployment reacts slowly and with a lag, which a same-year correlation cannot see.

**All pairs**, sorted by the size of r. The same figures are in the `correlations` configuration.

| Pair | r | 95% CI | p | n | Spearman ρ | r of yearly changes | Reading |
|---|---|---|---|---|---|---|---|
| GDP growth (%) × Change in debt (points of GDP) | **-0.80** | -0.89 to -0.67 | < 0.001 | 46 | -0.58 | -0.85 (p < 0.001) | very strong, negative; distinguishable from zero |
| Unemployment (%) × Inflation (%) | **-0.65** | -0.79 to -0.44 | < 0.001 | 46 | -0.53 | -0.48 (p < 0.001) | strong, negative; distinguishable from zero |
| Public balance (% of GDP) × Change in debt (points of GDP) | **-0.64** | -0.78 to -0.43 | < 0.001 | 46 | -0.55 | -0.71 (p < 0.001) | strong, negative; distinguishable from zero |
| GDP growth (%) × Public balance (% of GDP) | **+0.51** | +0.26 to +0.70 | < 0.001 | 46 | +0.46 | +0.57 (p < 0.001) | strong, positive; distinguishable from zero |
| Inflation (%) × Public balance (% of GDP) | **+0.38** | +0.10 to +0.60 | 0.010 | 46 | +0.31 | +0.36 (p = 0.01) | moderate, positive; distinguishable from zero |
| Unemployment (%) × Public balance (% of GDP) | **-0.21** | -0.47 to +0.08 | 0.16 | 46 | -0.23 | -0.29 (p = 0.05) | weak, negative; not distinguishable from zero |
| Inflation (%) × Change in debt (points of GDP) | **-0.16** | -0.43 to +0.14 | 0.29 | 46 | -0.02 | -0.28 (p = 0.06) | weak, negative; not distinguishable from zero |
| Unemployment (%) × Change in debt (points of GDP) | **+0.12** | -0.17 to +0.40 | 0.42 | 46 | +0.21 | +0.08 (p = 0.60) | weak, positive; not distinguishable from zero |
| GDP growth (%) × Inflation (%) | **+0.08** | -0.22 to +0.36 | 0.60 | 46 | +0.16 | +0.11 (p = 0.48) | negligible; not distinguishable from zero |
| GDP growth (%) × Unemployment (%) | **+0.01** | -0.28 to +0.30 | 0.94 | 46 | -0.03 | -0.02 (p = 0.90) | negligible; not distinguishable from zero |

**What it does not say**

- Same-year correlations miss lags, which matter for unemployment and debt.
- The 2020 and 2021 swings weigh heavily on the growth correlations; Spearman's ρ, less sensitive to them, is lower for growth and debt (-0.58).
- Nothing here says which government did better; see the limitations below.

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

### `correlations`, 10 rows

One row per pair of variables in the scatter-plot matrix: `x`, `y` and their labels, `n`, `pearson_r`, `r_squared`, `ci95_low`, `ci95_high` (Fisher z interval), `p_value` (two-sided t test), `spearman_rho`, `strength`, `direction`, and for annual series `n_changes`, `pearson_r_changes` and `p_value_changes`, the same correlation on year-on-year differences. Made by `correlations.py`.

## How it was built

1. **Public finances.** [INSEE](https://www.insee.fr/) national accounts (base 2014) through its open SDMX service for 1978 to 1994 and the sub-sectors; [Eurostat](https://ec.europa.eu/eurostat) (`gov_10dd_edpt1`, `gov_10a_main`, `gov_10a_exp`) from 1995, downloaded in October 2026.
2. **Economy.** World Bank Open Data for growth, inflation and GDP per head; INSEE quarterly ILO unemployment.
3. **Energy.** [Our World in Data energy dataset](https://github.com/owid/energy-data) for generation and shares; Wikidata for the sites, with reactor counts set by hand.
4. **Politics and pensions.** Dates of presidents, prime ministers and reforms curated for this dataset from official sources (Légifrance, vie-publique.fr, service-public.fr) and the press; legal ages by generation from the 2010 and 2023 laws and the 2026 social security budget (loi n° 2025-1403 du 30 décembre 2025).
5. **Charts.** Python and Matplotlib; borders from Natural Earth. The pipeline is in [`code/`](./). The correlation figures come from `correlations.py`, which reads only the published Parquet files.

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
