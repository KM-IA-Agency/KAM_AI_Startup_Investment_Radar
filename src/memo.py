from pathlib import Path

import pandas as pd

from src.scoring import score_dataframe


def safe(value):
    if pd.isna(value):
        return ""
    return str(value)


def generate_memo(row):
    name = safe(row.get("name"))
    return f"""# Startup Memo — {name}

## 1. Identité

- Nom : {name}
- Pays : {safe(row.get('country'))}
- Région : {safe(row.get('region'))}
- Secteur : {safe(row.get('sector'))}
- Sous-secteur : {safe(row.get('sub_sector'))}
- Stade : {safe(row.get('stage'))}
- Site : {safe(row.get('website'))}
- Source : {safe(row.get('source_url'))}

## 2. Résumé

{safe(row.get('description'))}

## 3. Scores

- Score total : {safe(row.get('total_score'))}/100
- Kamel Edge : {safe(row.get('kamel_edge_score'))}/25
- Risque : {safe(row.get('risk_score'))}/10
- Décision : {safe(row.get('decision'))}

## 4. Explication

{safe(row.get('score_explanation'))}

## 5. Questions de due diligence

- Le produit est-il testable directement ?
- La startup a-t-elle des clients payants vérifiables ?
- Le moat est-il technique, data, distribution ou réglementaire ?
- La valorisation laisse-t-elle encore un potentiel x5 / x10 ?
- Le risque de dilution est-il acceptable ?
- Quel accès réel existe pour investir ?

## 6. Prochaine décision

Décision actuelle : **{safe(row.get('decision'))}**

Prochaine action recommandée : vérifier les sources, tester le produit et comparer avec 3 concurrents directs.

---

Note : ce memo est un outil d'analyse et ne constitue pas un conseil financier personnalisé.
"""


def generate_all_memos(input_path="data/seeds/startups_seed.csv", output_dir="reports/memos"):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    df = score_dataframe(pd.read_csv(input_path))
    paths = []
    for _, row in df.iterrows():
        slug = safe(row.get("name")).lower().replace(" ", "-").replace("/", "-")
        path = output_dir / f"{slug}.md"
        path.write_text(generate_memo(row), encoding="utf-8")
        paths.append(path)
    return paths


if __name__ == "__main__":
    for path in generate_all_memos():
        print(path)
