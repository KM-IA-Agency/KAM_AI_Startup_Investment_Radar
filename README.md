# KAM AI Startup Investment Radar

**KAM AI Startup Investment Radar** est un projet de plateforme de veille, scoring et due diligence assistée pour identifier les startups IA, deeptech et data à fort potentiel de valorisation future.

> ⚠️ Ce dépôt ne constitue pas un conseil en investissement financier. Les contenus produits par la plateforme restent des analyses, signaux, scores et scénarios, sans recommandation personnalisée.

## Vision

Construire un **Radar Startup IA & Deeptech** capable de :

1. suivre la vitesse de développement de l'IA ;
2. identifier les tendances émergentes ;
3. pré-sélectionner des startups prometteuses ;
4. produire des fiches de due diligence technique et business ;
5. classer un Top 5 / Top 10 mensuel ;
6. détecter les signaux de bulle, survalorisation ou fausse promesse IA.

## Domaines prioritaires

- AI agents, orchestration, RAG, memory layers ;
- infrastructure IA, observability, evaluation, security ;
- data platform, BI, Microsoft Fabric, Power BI, data governance ;
- satellites, remote sensing, AgriTech, irrigation, climat ;
- MRV carbone/méthane, énergie, pipeline monitoring ;
- GPU cloud, inference optimization, routing multi-modèles ;
- biotech data, knowledge graph biomédical.

## Structure MVP

```text
.
├── app/streamlit_app.py
├── data/seeds/startups_seed.csv
├── docs/
├── sql/schema.sql
├── src/scoring.py
├── requirements.txt
└── README.md
```

## Lancer le MVP

```bash
python -m venv .venv
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Générer le dataset scoré :

```bash
python src/scoring.py
```

Sortie : `data/processed/scored_startups.csv`

## MVP actuel

Le dépôt contient maintenant :

- un dataset seed de 20 startups ;
- un moteur de scoring Python ;
- une app Streamlit de watchlist ;
- un schéma PostgreSQL initial ;
- une documentation projet complète.

## Scores utilisés

- Market Score
- Problem Pain Score
- Product Maturity Score
- Traction Score
- Team Score
- Technical Moat Score
- Valuation Score
- Investor Quality Score
- Exit Potential Score
- Risk Score
- Kamel Edge Score

## Décisions produites

- `Pass`
- `Watch`
- `Deep dive`
- `Strong watch`
- `Priority investigation`
- `Investable potential`

## Prochaines étapes

1. Vérifier et enrichir les 20 startups seed.
2. Ajouter 80 startups pour atteindre une base de 100.
3. Ajouter génération automatique de fiche startup Markdown.
4. Ajouter un rapport mensuel Top 10.
5. Connecter PostgreSQL.
6. Ajouter ingestion RSS / GitHub / Hugging Face / Product Hunt.
