# Forecasting Methodology — Growth Scenarios

## 1. Avons-nous assez d'éléments pour prédire la croissance future ?

Pas encore pour prédire de manière fiable.

Nous avons assez d'éléments pour construire des **hypothèses prévisionnelles** et des **scénarios probabilisés**, mais pas encore assez pour parler de prédiction robuste.

La différence est importante :

| Approche | Définition | Niveau de confiance |
|---|---|---|
| Prédiction | estimation forte d'un futur probable | faible aujourd'hui |
| Prévision | projection à partir de tendances et hypothèses | moyenne si données sourcées |
| Scénario | hypothèse structurée bear/base/bull | utilisable dès maintenant |
| Signal | indice partiel à surveiller | utile mais insuffisant seul |

---

## 2. Pourquoi ajouter le court terme ?

Les startups IA, robotique et infrastructure peuvent évoluer très vite : levée de fonds, partenariat industriel, nouveau modèle, changement de valorisation, lancement produit ou contrat stratégique.

Le radar doit donc suivre deux couches :

- **short-term momentum** : 1, 2, 3 et 6 mois ;
- **long-term scenario** : 12, 36 et 60 mois.

Le court terme ne prédit pas la valeur fondamentale. Il sert à capter l'accélération ou le ralentissement du momentum.

---

## 3. Données nécessaires pour une vraie prédiction

Pour améliorer la fiabilité, il faut plusieurs séries historiques :

- CA / ARR / MRR ;
- croissance CA YoY et QoQ ;
- valorisation historique ;
- total funding ;
- effectifs historiques ;
- croissance effectifs ;
- trafic web ;
- GitHub stars / forks / commits ;
- clients annoncés ;
- nouveaux contrats ;
- recrutement ;
- signaux négatifs ;
- comparables sectoriels.

Le minimum utile : 6 à 12 mois d'observations. Le bon niveau : 24 à 36 mois.

---

## 4. Méthode MVP retenue

Le module `src/forecasting.py` utilise une approche de scénarios :

- **Bear** : croissance ralentie, risque élevé ;
- **Base** : continuité raisonnable des signaux actuels ;
- **Bull** : forte accélération, traction confirmée.

Horizons court terme :

- 1 mois ;
- 2 mois ;
- 3 mois ;
- 6 mois.

Horizons long terme :

- 12 mois ;
- 36 mois ;
- 60 mois.

Métrique principale MVP :

- valorisation future estimée.

---

## 5. Variables utilisées dans le MVP

Le moteur utilise des proxies :

- croissance effectifs 6 mois ;
- croissance CA si disponible ;
- traction web si disponible ;
- croissance GitHub si disponible ;
- secteur ;
- data confidence.

Pour les horizons 1 à 6 mois, un boost prudent de momentum peut être appliqué aux secteurs très rapides :

- Physical AI / Robotics ;
- AI Infrastructure ;
- GPU Cloud.

Ce boost doit être remplacé plus tard par de vrais signaux quotidiens et hebdomadaires.

---

## 6. Sorties générées

Commande :

```bash
python src/forecasting.py
```

Sorties :

```text
reports/forecasts/scenario_forecasts.csv
reports/forecasts/scenario_forecasts_short_term.csv
reports/forecasts/expected_values.csv
reports/forecasts/expected_values_short_term.csv
reports/forecasts/forecast_<startup>_full.png
reports/forecasts/forecast_<startup>_short_term.png
```

---

## 7. Interprétation

Le résultat ne doit jamais être lu comme une vérité.

Il faut lire les scénarios ainsi :

- si les hypothèses bear se réalisent, la valeur pourrait aller vers X ;
- si le scénario base se réalise, la valeur pourrait aller vers Y ;
- si le scénario bull se réalise, la valeur pourrait aller vers Z ;
- l'expected value combine ces scénarios avec des probabilités arbitraires à ajuster.

Le court terme doit être interprété comme **momentum forecast**, pas comme valorisation fondamentale.

---

## 8. Limites

- Les données privées sont souvent incomplètes.
- Les valorisations peuvent être anciennes ou non confirmées.
- Les croissances d'effectifs ne prouvent pas les revenus.
- Les startups hardware/robotique nécessitent beaucoup de capital.
- Les bulles peuvent gonfler les valorisations malgré une faible traction.
- Les scénarios doivent être revus à chaque nouveau signal.
- Le court terme est sensible aux annonces et au bruit médiatique.

---

## 9. Prochaine amélioration

Ajouter un `Forecast Confidence Score` basé sur :

- nombre de sources ;
- fraîcheur des données ;
- historique disponible ;
- cohérence entre CA, effectifs, funding et clients ;
- volatilité du secteur ;
- risque de valorisation excessive ;
- intensité du momentum sur 7, 30 et 90 jours.

---

## 10. Position recommandée

Le radar doit afficher :

> Scénarios prévisionnels, pas prédictions certaines.

Le bon usage est d'aider à décider quelles startups méritent une due diligence plus poussée, pas d'automatiser une décision d'investissement.
