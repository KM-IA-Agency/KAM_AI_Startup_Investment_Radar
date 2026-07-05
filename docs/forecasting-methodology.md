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

## 2. Données nécessaires pour une vraie prédiction

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

## 3. Méthode MVP retenue

Le module `src/forecasting.py` utilise une approche de scénarios :

- **Bear** : croissance ralentie, risque élevé ;
- **Base** : continuité raisonnable des signaux actuels ;
- **Bull** : forte accélération, traction confirmée.

Horizon :

- 12 mois ;
- 36 mois ;
- 60 mois.

Métrique principale MVP :

- valorisation future estimée.

---

## 4. Variables utilisées dans le MVP

Le moteur utilise des proxies :

- croissance effectifs 6 mois ;
- croissance CA si disponible ;
- traction web si disponible ;
- croissance GitHub si disponible ;
- secteur ;
- data confidence.

Si aucune donnée de croissance fiable n'existe, le moteur applique une hypothèse sectorielle par défaut.

---

## 5. Sorties générées

Commande :

```bash
python src/forecasting.py
```

Sorties :

```text
reports/forecasts/scenario_forecasts.csv
reports/forecasts/expected_values.csv
reports/forecasts/forecast_<startup>.png
```

---

## 6. Interprétation

Le résultat ne doit jamais être lu comme une vérité.

Il faut lire les scénarios ainsi :

- si les hypothèses bear se réalisent, la valeur pourrait aller vers X ;
- si le scénario base se réalise, la valeur pourrait aller vers Y ;
- si le scénario bull se réalise, la valeur pourrait aller vers Z ;
- l'expected value combine ces scénarios avec des probabilités arbitraires à ajuster.

---

## 7. Limites

- Les données privées sont souvent incomplètes.
- Les valorisations peuvent être anciennes ou non confirmées.
- Les croissances d'effectifs ne prouvent pas les revenus.
- Les startups hardware/robotique nécessitent beaucoup de capital.
- Les bulles peuvent gonfler les valorisations malgré une faible traction.
- Les scénarios doivent être revus à chaque nouveau signal.

---

## 8. Prochaine amélioration

Ajouter un `Forecast Confidence Score` basé sur :

- nombre de sources ;
- fraîcheur des données ;
- historique disponible ;
- cohérence entre CA, effectifs, funding et clients ;
- volatilité du secteur ;
- risque de valorisation excessive.

---

## 9. Position recommandée

Le radar doit afficher :

> Scénarios prévisionnels, pas prédictions certaines.

Le bon usage est d'aider à décider quelles startups méritent une due diligence plus poussée, pas d'automatiser une décision d'investissement.
