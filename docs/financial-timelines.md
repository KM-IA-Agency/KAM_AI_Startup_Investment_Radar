# Financial Timelines

## Objectif

Ajouter une lecture chronologique de la trajectoire financière d'une startup :

- levées de fonds ;
- montants levés ;
- valorisations successives ;
- événements majeurs ;
- IPO / introduction en bourse ;
- prix de l'action si société cotée ;
- capitalisation boursière ;
- scénarios futurs de valorisation.

---

## Tables ajoutées

### `financial_events`

Stocke tous les événements financiers majeurs :

- funding ;
- valuation update ;
- IPO ;
- acquisition ;
- down round ;
- strategic partnership ;
- major contract ;
- public market event.

### `public_market_observations`

Stocke les observations de marché pour les sociétés cotées :

- ticker ;
- exchange ;
- share price ;
- market cap ;
- enterprise value ;
- date d'observation.

---

## Dataset seed

Fichier :

```text
data/seeds/financial_events_seed.csv
```

Il contient les premiers événements financiers pour :

- Figure AI ;
- Physical Intelligence ;
- Skild AI ;
- 1X Technologies ;
- Apptronik ;
- Agility Robotics ;
- Mistral AI ;
- Hugging Face ;
- Baseten ;
- Kayrros.

Certaines valeurs sont des placeholders et doivent être vérifiées.

---

## Module Python

Commande :

```bash
python src/timeline_charts.py
```

Sorties :

```text
reports/timelines/financial_events_table.csv
reports/timelines/timeline_<startup>.png
reports/timelines/valuation_future_<startup>.png
```

---

## Lecture recommandée

Un bon graphique de timeline doit montrer :

1. la progression des levées ;
2. la progression de la valorisation ;
3. le temps entre deux tours ;
4. les changements de rythme ;
5. les événements de rupture ;
6. le scénario futur bear/base/bull.

---

## Cas des sociétés cotées

Pour une société cotée, suivre aussi :

- prix de l'action ;
- capitalisation boursière ;
- volume ;
- évolution post-IPO ;
- multiple de revenus ;
- comparaison avec valorisation privée pré-IPO.

---

## Attention

Pour les startups privées, la valorisation est souvent :

- non publique ;
- estimée ;
- issue de presse ;
- arrondie ;
- parfois contradictoire.

Chaque donnée doit donc avoir :

- source ;
- date ;
- niveau de confiance ;
- commentaire.
