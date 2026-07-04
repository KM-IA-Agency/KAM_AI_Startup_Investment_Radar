from pathlib import Path
from datetime import date

import pandas as pd

from src.scoring import score_dataframe


REPORT_DIR = Path("reports/generated")
SEED_PATH = Path("data/seeds/startups_seed.csv")


def section_table(df, columns):
    if df.empty:
        return "No data.\n"
    return df[columns].to_markdown(index=False)


def generate_monthly_report(input_path=SEED_PATH, output_dir=REPORT_DIR):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = score_dataframe(pd.read_csv(input_path))
    top10 = df.head(10)
    priority = df[df["decision"].isin(["Priority investigation", "Investable potential"])]
    strong_watch = df[df["decision"].isin(["Strong watch", "Deep dive"])]

    by_sector = (
        df.groupby("sector")
        .agg(startups=("name", "count"), avg_score=("total_score", "mean"), max_score=("total_score", "max"))
        .reset_index()
        .sort_values(["max_score", "avg_score"], ascending=False)
    )
    by_sector["avg_score"] = by_sector["avg_score"].round(1)

    today = date.today().isoformat()
    report = f"""# Radar IA & Deeptech — Rapport MVP

Date : {today}

## 1. Résumé exécutif

Ce rapport est généré automatiquement à partir du dataset seed et du moteur de scoring MVP.
Il sert à prioriser la veille et la due diligence. Il ne constitue pas un conseil financier personnalisé.

- Startups analysées : {len(df)}
- Score moyen : {round(df['total_score'].mean(), 1)}
- Meilleur score : {int(df['total_score'].max())}
- Startups en investigation prioritaire : {len(priority)}

## 2. Top 10 Watchlist

{section_table(top10, ['name', 'country', 'sector', 'sub_sector', 'stage', 'total_score', 'kamel_edge_score', 'decision'])}

## 3. Investigation prioritaire

{section_table(priority, ['name', 'country', 'sector', 'total_score', 'kamel_edge_score', 'decision', 'score_explanation'])}

## 4. Strong Watch / Deep Dive

{section_table(strong_watch, ['name', 'country', 'sector', 'total_score', 'kamel_edge_score', 'decision'])}

## 5. Classement par secteur

{section_table(by_sector, ['sector', 'startups', 'avg_score', 'max_score'])}

## 6. Prochaines actions recommandées

1. Vérifier les sources des 10 premières startups.
2. Tester les produits lorsque c'est possible.
3. Comparer chaque startup avec 3 concurrents directs.
4. Vérifier les valorisations et derniers tours de financement.
5. Produire 3 fiches deep dive avec `python src/memo.py`.
6. Ajouter les signaux faibles via `python src/signals.py`.

---

Note : ce rapport est un outil de veille et d'analyse. Il ne remplace pas une due diligence financière, juridique ou réglementaire.
"""

    path = output_dir / f"radar_report_{today}.md"
    path.write_text(report, encoding="utf-8")
    return path


if __name__ == "__main__":
    print(generate_monthly_report())
