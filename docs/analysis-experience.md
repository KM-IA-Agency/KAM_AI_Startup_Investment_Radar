# Analysis Experience — Dashboard Views

## 1. Objectif

Améliorer l'exploration et la présentation des résultats pour permettre une vraie analyse startup : scoring, benchmark, valorisation, risque, momentum et scénarios.

Le dashboard Streamlit est organisé en onglets.

---

## 2. Onglet Overview

Vue exécutive du radar.

Indicateurs affichés :

- nombre de startups ;
- score moyen ;
- meilleur score ;
- Kamel Edge moyen ;
- risque moyen ;
- répartition par secteur ;
- score moyen par secteur ;
- Top opportunités.

Objectif : comprendre rapidement où se trouvent les zones les plus prometteuses.

---

## 3. Onglet Watchlist

Tableau filtrable complet.

Colonnes clés :

- pays ;
- secteur ;
- sous-secteur ;
- stade ;
- score total ;
- score marché ;
- traction ;
- moat technique ;
- valorisation ;
- risque ;
- Kamel Edge ;
- décision.

Objectif : prioriser les startups à analyser manuellement.

---

## 4. Onglet Benchmark

Vue quantitative classique.

Indicateurs :

- valorisation latest ;
- date de valorisation ;
- total funding ;
- dernier round ;
- effectifs ;
- croissance effectifs ;
- CA / ARR si disponible ;
- croissance CA ;
- niveau de confiance des données.

Objectif : comparer les startups avec des métriques classiques d'investissement.

---

## 5. Onglet Forecasts

Vue de scénarios prévisionnels.

Deux modes :

- court terme : 1, 2, 3, 6 mois ;
- complet : 1 à 60 mois.

Scénarios :

- pessimiste ;
- base ;
- optimiste.

Objectif : visualiser le momentum potentiel et les hypothèses de croissance.

Important : il s'agit de scénarios, pas de prédictions certaines.

---

## 6. Onglet Physical AI

Vue dédiée aux startups robotique / IA incarnée.

Pourquoi une vue séparée ?

La robotique a des risques spécifiques :

- hardware coûteux ;
- téléopération ;
- autonomie réelle difficile à vérifier ;
- manufacturing ;
- sécurité ;
- cycles industriels longs.

Objectif : ne pas comparer naïvement une startup humanoïde avec une startup SaaS IA.

---

## 7. Onglet Startup Detail

Fiche détaillée d'une startup sélectionnée.

Contenu :

- description ;
- score total ;
- Kamel Edge ;
- risque ;
- moat technique ;
- décision ;
- explication du score ;
- site et source.

Objectif : passer de la vue portefeuille à la due diligence individuelle.

---

## 8. Lecture recommandée

Une startup intéressante combine idéalement :

- score total élevé ;
- Kamel Edge élevé ;
- risque maîtrisé ;
- données benchmark crédibles ;
- momentum court terme positif ;
- scénario base solide ;
- scénario bear acceptable ;
- red flags identifiés et vérifiables.

---

## 9. Prochaines améliorations UI

- Ajouter une heatmap secteur x score.
- Ajouter une matrice risque / rendement potentiel.
- Ajouter une page Comparables.
- Ajouter un export HTML/PDF du dashboard.
- Ajouter une vue signaux faibles quotidiens.
- Ajouter un mode due diligence checklist.
- Ajouter une synthèse automatique Top 5 mensuelle.
