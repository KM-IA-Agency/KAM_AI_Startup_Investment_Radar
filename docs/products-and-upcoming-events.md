# Products and Upcoming Events

## Objectif

Faire le lien entre :

- société cotée ;
- nom public ;
- produit phare ;
- ticker ;
- segment comparable ;
- startup privée équivalente ;
- prochains événements probables.

Cette couche évite de confondre la société, le ticker et le produit.

---

## Fichiers seed

```text
data/seeds/company_product_mapping_seed.csv
data/seeds/upcoming_events_seed.csv
```

---

## Exemples

| Société | Produit phare | Ticker | Segment |
|---|---|---|---|
| UiPath | UiPath Business Automation Platform | PATH | AI Agents / automation |
| C3.ai | C3 AI Applications | AI | Enterprise AI |
| Arm Holdings | Arm IP / Neoverse | ARM | AI infrastructure |
| Figure AI | Figure robot / Helix AI | private | Physical AI |
| Apptronik | Apollo robot | private | Physical AI |
| Agility Robotics | Digit robot | private | Warehouse robotics |

---

## Événements probables suivis

- levée de fonds ;
- IPO candidate ;
- dilution risk ;
- annonce produit majeure ;
- nouvelle version ;
- partenariat industriel ;
- commercial rollout ;
- acquisition ;
- earnings event ;
- guidance update.

---

## Champs clés

- `event_window` : 0-6 mois, 6-18 mois, etc.
- `event_type` : funding, ipo_candidate, product_major, partnership...
- `probability_pct` : probabilité indicative.
- `impact_score` : impact potentiel sur valorisation / momentum.
- `confidence_score` : confiance dans l'hypothèse.
- `watch_signals` : signaux à surveiller.

---

## Page Streamlit

Un onglet dédié a été ajouté :

```text
Products & Events
```

---

## Attention

Les événements probables ne sont pas des prédictions certaines.
Ils servent à organiser la veille et à identifier ce qu'il faut surveiller.
