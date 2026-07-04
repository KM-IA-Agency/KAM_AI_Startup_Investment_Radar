# Runbook MVP

Ce runbook décrit comment lancer les principaux modules du MVP.

## 1. Installation

```bash
python -m venv .venv
pip install -r requirements.txt
```

Sur Windows :

```bash
.venv\Scripts\activate
```

Sur macOS / Linux :

```bash
source .venv/bin/activate
```

## 2. Lancer l'interface Streamlit

```bash
streamlit run app/streamlit_app.py
```

L'interface permet de filtrer les startups par :

- pays ;
- secteur ;
- décision ;
- score minimum.

## 3. Générer le dataset scoré

```bash
python src/scoring.py
```

Sortie :

```text
data/processed/scored_startups.csv
```

## 4. Générer les fiches startup

```bash
python src/memo.py
```

Sortie :

```text
reports/memos/*.md
```

## 5. Collecter les signaux faibles MVP

```bash
python src/signals.py
```

Sortie :

```text
data/processed/signals.csv
```

## 6. Générer le rapport mensuel MVP

```bash
python src/report.py
```

Sortie :

```text
reports/generated/radar_report_YYYY-MM-DD.md
```

## 7. Ordre recommandé

```bash
python src/scoring.py
python src/memo.py
python src/signals.py
python src/report.py
streamlit run app/streamlit_app.py
```

## 8. Limites actuelles

- Dataset seed encore limité à 20 startups.
- Scores initiaux à valider manuellement.
- Ingestion de signaux très simple.
- Pas encore de PostgreSQL connecté à l'app.
- Pas encore de LLM pour enrichissement automatique.

## 9. Prochaine version

- Passer à 100 startups.
- Ajouter PostgreSQL.
- Ajouter un agent d'enrichissement IA.
- Ajouter un export PDF.
- Ajouter un dashboard historique des signaux.
