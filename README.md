# KAM AI Startup Investment Radar

**KAM AI Startup Investment Radar** est un projet de plateforme de veille, scoring et due diligence assistée pour identifier les startups IA, deeptech et data à fort potentiel de valorisation future.

Le projet vise d'abord un **MVP interne** pour aider à construire une watchlist d'investissement personnelle, puis pourra évoluer vers une activité de **conseil, intelligence marché, rapports sectoriels ou SaaS spécialisé**.

> ⚠️ Ce dépôt ne constitue pas un conseil en investissement financier. Les contenus produits par la plateforme devront rester des analyses, signaux, scores et scénarios, sans recommandation personnalisée d'achat/vente adaptée à une situation patrimoniale individuelle.

---

## Vision courte

Construire un **Radar Startup IA & Deeptech** capable de :

1. suivre la vitesse de développement de l'IA ;
2. identifier les tendances émergentes avant leur diffusion massive ;
3. pré-sélectionner des startups prometteuses ;
4. produire des fiches de due diligence technique et business ;
5. classer un Top 5 / Top 10 mensuel des startups à suivre ;
6. détecter les signaux de bulle, survalorisation ou fausse promesse IA.

---

## Domaines prioritaires

Le radar se concentre sur les domaines où l'analyse technique peut créer un avantage informationnel :

- AI agents, orchestration, RAG, memory layers ;
- infrastructure IA, observability, evaluation, security ;
- data platform, BI, Microsoft Fabric, Power BI, data governance ;
- satellites, remote sensing, AgriTech, irrigation, climat ;
- MRV carbone/méthane, énergie, pipeline monitoring ;
- GPU cloud, inference optimization, routing multi-modèles ;
- biotech data, knowledge graph biomédical, moteur d'hypothèses scientifiques.

---

## Première proposition de valeur

### Pour usage interne

- construire une watchlist d'investissement startup ;
- filtrer les startups trop risquées ou trop chères ;
- analyser la viabilité technique et business ;
- comparer les opportunités France, Suisse, Algérie, Europe, MENA ;
- produire un Top 5 / Top 10 des startups à suivre.

### Pour usage commercial futur

- rapports mensuels IA & Deeptech ;
- due diligence technique pour business angels, family offices, incubateurs ou fonds ;
- cartographie sectorielle ;
- scoring startup ;
- plateforme SaaS de veille et scoring.

---

## Structure documentaire

```text
.
├── README.md
├── docs/
│   ├── vision.md
│   ├── product-plan.md
│   ├── roadmap.md
│   ├── scoring-framework.md
│   ├── data-sources.md
│   ├── architecture.md
│   ├── mvp-backlog.md
│   └── legal-disclaimer.md
└── .gitignore
```

---

## MVP cible

Le MVP doit permettre de créer une base de 100 à 300 startups, enrichie avec :

- secteur ;
- pays ;
- stade de développement ;
- financement connu ;
- fondateurs ;
- produit ;
- traction ;
- signaux faibles ;
- score technique ;
- score business ;
- score valorisation ;
- score `Kamel Edge` ;
- décision : `Pass`, `Watch`, `Deep Dive`, `Investigation`, `Investable`.

---

## Stack MVP proposée

- **Collecte** : Python, RSS, APIs publiques, scraping léger conforme aux CGU.
- **Base** : PostgreSQL, puis pgvector pour recherche sémantique.
- **Backend** : FastAPI.
- **Interface MVP** : Streamlit.
- **Dashboard** : Power BI ou Metabase.
- **Automatisation** : n8n.
- **IA** : extraction structurée, scoring assisté, génération de fiches startup.

---

## Statut

Projet initialisé. Première étape : structurer la documentation produit, puis créer le schéma de données et un prototype de scoring.