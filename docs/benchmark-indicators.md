# Benchmark Indicators

## 1. Objectif

Ajouter au radar des indicateurs classiques et comparables pour suivre les startups dans le temps : chiffre d'affaires, valorisation, croissance, financement, effectifs, traction technique et signaux marché.

Le but est de passer d'un score statique à un suivi dynamique avec historique timestampé.

---

## 2. Indicateurs classiques

| Indicateur | Champ | Fréquence cible | Commentaire |
|---|---|---|---|
| Chiffre d'affaires latest | `revenue_latest` | mensuelle / trimestrielle | souvent estimé pour startups privées |
| Croissance CA YoY | `revenue_growth_yoy_pct` | trimestrielle | très utile pour SaaS |
| Croissance CA QoQ | `revenue_growth_qoq_pct` | trimestrielle | utile en early stage |
| Valorisation latest | `valuation_latest` | à chaque levée | donnée clé mais souvent opaque |
| Total funding | `total_funding` | à chaque levée | cumul des capitaux levés |
| Dernier round | `latest_round_amount` | à chaque levée | momentum funding |
| Effectifs | `employees_latest` | mensuelle | proxy de croissance |
| Croissance effectifs 6 mois | `employee_growth_6m_pct` | mensuelle | signal fort de scaling |
| Web traffic growth | `web_traffic_growth_3m_pct` | mensuelle | proxy traction marché |
| GitHub stars | `github_stars` | quotidienne / hebdo | utile open source |
| GitHub growth 3 mois | `github_stars_growth_3m_pct` | hebdo / mensuelle | adoption développeur |
| Clients estimés | `customer_count_estimate` | mensuelle / trimestrielle | à valider avec sources |
| Data confidence | `data_confidence` | chaque observation | 1 faible, 5 forte |

---

## 3. Fréquences de suivi

### Quotidien

- news critiques ;
- GitHub stars / forks ;
- Product Hunt / Hacker News ;
- annonces de levée ;
- signaux négatifs : shutdown, lawsuit, breach.

### Hebdomadaire

- signaux techniques ;
- recrutements ;
- nouvelles démos ;
- nouveaux clients annoncés ;
- évolution watchlist.

### Mensuel

- rapport benchmark ;
- classement Top 10 ;
- évolution valorisation estimée ;
- évolution effectifs ;
- traction web ;
- ajustement des scores.

### Trimestriel

- chiffre d'affaires estimé ;
- croissance ARR/MRR si disponible ;
- comparaison sectorielle ;
- revue risque de bulle ;
- réallocation watchlist.

---

## 4. Tables ajoutées

### `benchmark_metrics`

Stocke le dernier état connu : CA, valorisation, funding, effectifs, croissance.

### `metric_observations`

Stocke les observations timestampées : quotidien, hebdo, mensuel, trimestriel.

Cette table permet de générer des graphes d'évolution.

---

## 5. Module Python

Commande :

```bash
python src/benchmarks.py
```

Sorties :

```text
reports/benchmarks/benchmark_table.csv
reports/benchmarks/observations_daily.csv
reports/benchmarks/observations_weekly.csv
reports/benchmarks/observations_monthly.csv
reports/benchmarks/top_valuations.png
reports/benchmarks/valuation_history_monthly.png
```

---

## 6. Important

Les données du seed benchmark sont des placeholders à vérifier. Les valorisations et chiffres privés doivent être sourcés et datés.

Chaque métrique doit idéalement avoir :

- source ;
- date ;
- niveau de confiance ;
- type d'observation ;
- devise ;
- commentaire.
