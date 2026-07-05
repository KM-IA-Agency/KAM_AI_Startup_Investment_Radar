# IPO and Public Market Tracking

## Objectif

Ajouter une vue dédiée aux sociétés passées en bourse ou aux comparables publics.

La vue permet de suivre :

- prix d'introduction en bourse ;
- clôture du premier jour ;
- dernier cours disponible ;
- évolution du cours dans le temps ;
- market cap ;
- ticker ;
- place de cotation ;
- niveau de confiance des données.

---

## Fichiers seed

```text
data/seeds/ipo_events_seed.csv
data/seeds/public_market_observations_seed.csv
```

---

## Page Streamlit

Un onglet dédié a été ajouté :

```text
IPO & Actions
```

Cet onglet est séparé de `Financial Timeline` car une startup privée n'a pas forcément de ticker ni de cours de bourse.

---

## Important

Les données seed sont des placeholders de structure.

Pour une vraie analyse, chaque observation doit être remplacée par des données vérifiées :

- source ;
- date ;
- ticker ;
- exchange ;
- prix action ;
- market cap ;
- niveau de confiance.

---

## Prochaines améliorations

- Intégrer une source de prix boursiers officielle ou API.
- Ajouter variation depuis IPO.
- Ajouter performance 1 mois, 3 mois, 6 mois, 1 an.
- Ajouter comparaison avec valorisation privée pré-IPO.
- Ajouter multiples CA / market cap quand CA disponible.
