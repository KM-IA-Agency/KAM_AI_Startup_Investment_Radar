# Roadmap — MVP Startup Investment Radar

## Phase 0 — Initialisation projet

Objectif : poser la vision et la structure documentaire.

Livrables :

- README ;
- vision ;
- product plan ;
- scoring framework ;
- data sources ;
- architecture cible ;
- backlog MVP.

Statut : en cours.

---

## Phase 1 — Dataset manuel de départ

Objectif : construire une première base de 100 startups.

Durée cible : 1 à 2 semaines.

### Contenu

- 40 startups AI infra / agents / devtools ;
- 20 startups data platform / BI / governance ;
- 15 startups satellite / MRV / climate ;
- 10 startups GPU cloud / inference ;
- 10 startups biotech data / healthtech ;
- 5 startups AgriTech Algérie / MENA.

### Livrables

- fichier CSV ou table PostgreSQL `startups` ;
- taxonomy secteurs ;
- première watchlist brute ;
- première version du score manuel.

---

## Phase 2 — Scoring MVP

Objectif : transformer la base startup en classement priorisé.

Durée cible : 1 à 2 semaines.

### Scores à implémenter

- Market Score ;
- Product Score ;
- Technical Moat Score ;
- Traction Score ;
- Team Score ;
- Valuation Score ;
- Risk Score ;
- Kamel Edge Score.

### Livrables

- notebook ou script Python de scoring ;
- table `scores` ;
- Top 20 automatique ;
- règles de rejet rapide.

---

## Phase 3 — Prototype interface

Objectif : rendre le radar utilisable.

Durée cible : 2 semaines.

### Interface MVP

- Streamlit ou FastAPI + frontend simple ;
- filtres par pays/secteur/score ;
- fiche startup ;
- watchlist ;
- notes manuelles ;
- export CSV/Markdown.

### Livrables

- écran liste startups ;
- écran fiche startup ;
- écran scoring ;
- écran Top 10.

---

## Phase 4 — Enrichissement assisté IA

Objectif : générer automatiquement des résumés et fiches d'analyse.

Durée cible : 2 à 4 semaines.

### Fonctions

- résumé startup ;
- classification secteur ;
- extraction fondateurs / investisseurs ;
- analyse moat ;
- détection red flags ;
- génération investment memo.

### Livrables

- prompt templates ;
- extraction JSON structurée ;
- fiche d'analyse standard ;
- comparatif startups similaires.

---

## Phase 5 — Veille automatisée

Objectif : suivre les signaux faibles.

Durée cible : 4 semaines.

### Sources

- RSS articles ;
- GitHub trending ;
- Product Hunt ;
- Hugging Face ;
- arXiv ;
- newsletters VC ;
- pages startups ;
- LinkedIn manuel au départ.

### Livrables

- table `signals` ;
- score momentum ;
- alerte hebdomadaire ;
- rapport mensuel.

---

## Phase 6 — Rapport vendable

Objectif : produire un premier livrable commercial.

Durée cible : après MVP interne.

### Rapport type

- Top 10 startups ;
- Top 5 tendances IA ;
- Top 5 risques de bulle ;
- Top 5 opportunités France/Suisse/Algérie ;
- 3 deep dives ;
- 1 carte sectorielle.

---

## Décision Go / No-Go

Le projet devient commercialisable si :

- le radar identifie des startups non évidentes ;
- les fiches sont utiles pour décider ;
- le Top 10 est compréhensible par un investisseur ;
- les scores sont explicables ;
- au moins 3 personnes externes trouvent le rapport utile.