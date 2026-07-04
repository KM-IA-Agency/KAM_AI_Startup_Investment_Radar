# Architecture — MVP Startup Radar

## 1. Principe général

Le MVP doit rester simple : collecter, stocker, enrichir, scorer, visualiser et générer des fiches startup.

Architecture cible :

```text
Sources externes
  ↓
Collecte Python / n8n
  ↓
PostgreSQL
  ↓
Scoring Engine Python
  ↓
LLM Enrichment / Due Diligence Agent
  ↓
Streamlit / Dashboard
  ↓
Top 10 / Investment Memos / Reports
```

---

## 2. Stack MVP

| Couche | Choix MVP |
|---|---|
| Langage | Python |
| Base | PostgreSQL |
| Recherche sémantique future | pgvector |
| API | FastAPI |
| UI rapide | Streamlit |
| Automatisation | n8n |
| Dashboard | Power BI ou Metabase |
| IA | prompts structurés + extraction JSON |
| Versioning | GitHub |

---

## 3. Modèle de données initial

### Table `startups`

| Champ | Type | Description |
|---|---|---|
| id | uuid | identifiant |
| name | text | nom startup |
| website | text | site web |
| country | text | pays |
| region | text | Europe, MENA, Global |
| sector | text | secteur principal |
| sub_sector | text | sous-secteur |
| stage | text | pre-seed, seed, series A... |
| description | text | résumé |
| founded_year | int | année création |
| status | text | active, acquired, closed, unknown |
| created_at | timestamp | création fiche |
| updated_at | timestamp | mise à jour |

### Table `founders`

| Champ | Type |
|---|---|
| id | uuid |
| startup_id | uuid |
| name | text |
| role | text |
| linkedin_url | text |
| background | text |
| technical_score | int |

### Table `funding_rounds`

| Champ | Type |
|---|---|
| id | uuid |
| startup_id | uuid |
| round_type | text |
| amount | numeric |
| currency | text |
| date | date |
| investors | text |
| valuation_estimate | numeric |
| source_url | text |

### Table `signals`

| Champ | Type |
|---|---|
| id | uuid |
| startup_id | uuid |
| signal_type | text |
| signal_date | date |
| title | text |
| summary | text |
| source | text |
| source_url | text |
| impact_score | int |

### Table `scores`

| Champ | Type |
|---|---|
| startup_id | uuid |
| market_score | int |
| product_score | int |
| technical_moat_score | int |
| traction_score | int |
| team_score | int |
| valuation_score | int |
| investor_quality_score | int |
| exit_potential_score | int |
| risk_score | int |
| kamel_edge_score | int |
| total_score | int |
| decision | text |
| score_explanation | text |

### Table `investment_memos`

| Champ | Type |
|---|---|
| id | uuid |
| startup_id | uuid |
| memo_date | date |
| problem | text |
| solution | text |
| market | text |
| technology | text |
| traction | text |
| moat | text |
| valuation | text |
| risks | text |
| decision | text |

---

## 4. Services applicatifs

### `collector`

Collecte ou importe les données startup.

### `enricher`

Utilise des règles et LLM pour enrichir les fiches.

### `scorer`

Calcule les scores explicables.

### `memo_generator`

Produit une fiche startup standardisée.

### `watchlist_ranker`

Classe les startups par score, thème, pays et potentiel.

### `report_generator`

Produit un rapport mensuel Markdown / PDF.

---

## 5. Interface MVP

Pages :

1. Dashboard global ;
2. Liste startups ;
3. Fiche startup ;
4. Scoring ;
5. Watchlist Top 10 ;
6. Deep Dive ;
7. Sources & signaux ;
8. Export rapport.

---

## 6. Principes de conception

- explicabilité avant automatisation ;
- l'IA propose, l'humain valide ;
- distinguer données, hypothèses et jugements ;
- garder les sources ;
- éviter le conseil financier personnalisé ;
- construire petit, puis automatiser progressivement.