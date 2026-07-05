# Number Formatting Conventions

## Objectif

Simplifier la lecture des grands chiffres dans le dashboard et les rapports.

Au lieu d'afficher :

```text
13000000000
```

Le radar affiche :

```text
13.00 Mrd
```

## Règles

| Valeur brute | Affichage |
|---:|---:|
| 13 000 000 000 | 13.00 Mrd |
| 2 500 000 000 | 2.50 Mrd |
| 450 000 000 | 450.0 M |
| 12 000 | 12.0 k |

## Fichier utilitaire

Les fonctions sont centralisées dans :

```text
src/formatting.py
```

Fonctions disponibles :

- `format_number()`
- `format_percent()`
- `add_readable_columns()`

## Colonnes concernées

- valorisation ;
- total funding ;
- dernier round ;
- chiffre d'affaires ;
- expected value ;
- forecast value ;
- effectifs importants.

## Convention

- `Mrd` = milliard ;
- `M` = million ;
- `k` = millier.

Les valeurs brutes restent conservées dans les CSV pour les calculs.
Les valeurs lisibles sont uniquement utilisées pour l'affichage.
