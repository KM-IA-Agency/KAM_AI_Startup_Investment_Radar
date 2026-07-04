# Data Sources — Startup Radar

## 1. Objectif

Construire une veille multi-sources pour identifier les startups, tendances, signaux faibles, levées de fonds, publications techniques et indicateurs de traction.

Le MVP doit commencer avec des sources simples, accessibles et conformes aux conditions d'utilisation.

---

## 2. Sources startup / funding

| Source | Usage | Priorité |
|---|---|---:|
| Dealroom | startups Europe, écosystèmes, funding | Haute |
| Crunchbase | funding, fondateurs, investisseurs | Haute |
| CB Insights | rapports, AI 100, tendances | Haute |
| PitchBook | rapports VC, multiples, tendances | Moyenne / premium |
| Tracxn | startups émergentes, Algérie, MENA | Moyenne |
| StartupBlink | cartographie écosystèmes | Moyenne |
| F6S | startups early stage | Moyenne |

---

## 3. Sources France

| Source | Usage |
|---|---|
| La French Tech Next40/120 | scaleups françaises validées |
| Bpifrance | deeptech, financement, accélérateurs |
| Maddyness | news startups France |
| Sifted France/Benelux | classements growth |
| French Tech Journal | analyses écosystème |

---

## 4. Sources Suisse

| Source | Usage |
|---|---|
| Startupticker | levées suisses, news |
| Swiss Venture Capital Report | rapport annuel VC suisse |
| Venturelab TOP 100 | startups suisses sélectionnées |
| Innosuisse | innovation et soutien public |
| ETH / EPFL spin-offs | deeptech de qualité |

---

## 5. Sources Algérie / MENA

| Source | Usage |
|---|---|
| Algeria Venture | écosystème local |
| ASF / Startup Fund | financements publics |
| MagStartup | startups Maghreb / MENA |
| StartupBlink Algeria | classement et cartographie |
| Tracxn Algeria | base structurée |
| LinkedIn | signaux terrain, fondateurs |
| incubateurs universitaires | sourcing local |
| événements startup DZ | validation terrain |

---

## 6. Sources techniques IA

| Source | Usage |
|---|---|
| GitHub Trending | adoption développeur |
| Hugging Face Trending | modèles, datasets, spaces |
| arXiv | recherche émergente |
| Papers with Code | benchmarks et SOTA |
| Product Hunt | lancement produit |
| Hacker News | signaux développeurs |
| Reddit spécialisé | bruit faible, veille qualitative |

---

## 7. Sources analystes et market maps

| Source | Usage |
|---|---|
| a16z | thèses IA, infra, data |
| Menlo Ventures | IA infrastructure |
| Sequoia | AI, market maps, company building |
| Bessemer | cloud, SaaS, AI |
| Index Ventures | Europe, SaaS, IA |
| Atomico State of European Tech | Europe |
| Sifted | Europe, VC, startups |
| CB Insights Research | market maps, top startups |
| Awesome AI Market Maps | agrégation GitHub de market maps |

---

## 8. Signaux faibles à collecter

| Signal | Exemple |
|---|---|
| Funding | nouvelle levée, montant, investisseurs |
| Hiring | recrutement sales, ML, cloud, regulatory |
| Product | lancement API, changelog, démo |
| GitHub | stars, forks, commits, issues |
| Research | publication arXiv, brevet, benchmark |
| Customer | logos clients, cas d'usage, contrats |
| Media | articles, interviews fondateurs |
| Partnerships | universités, corporates, cloud providers |
| Regulation | conformité, agréments, risques |
| Competition | nouveaux concurrents, acquisition |

---

## 9. Approche conformité

- éviter le scraping agressif ;
- privilégier API, RSS, exports manuels et sources publiques ;
- documenter l'origine de chaque donnée ;
- garder les liens sources ;
- distinguer donnée brute, inférence IA et jugement humain ;
- respecter les CGU des plateformes.

---

## 10. Priorité MVP

Commencer par :

1. collecte manuelle structurée de 100 startups ;
2. enrichissement via sources publiques ;
3. veille RSS / newsletters ;
4. GitHub / Hugging Face / Product Hunt pour signaux techniques ;
5. rapports analystes pour market maps.