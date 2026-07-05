from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.scoring import score_dataframe

OUTPUT_DIR = Path("reports/enrichment")


def build_enrichment_prompt(row: pd.Series) -> str:
    return f"""
You are an investment and technical due-diligence analyst.
Analyze the startup below using only verifiable facts from provided data.
Clearly separate facts, assumptions and open questions.

Startup:
- Name: {row.get('name', '')}
- Country: {row.get('country', '')}
- Sector: {row.get('sector', '')}
- Sub-sector: {row.get('sub_sector', '')}
- Stage: {row.get('stage', '')}
- Website: {row.get('website', '')}
- Description: {row.get('description', '')}

Return a structured analysis with:
1. one-sentence summary
2. problem
3. product
4. market
5. technical moat
6. business traction signals
7. valuation questions
8. red flags
9. missing information
10. next due-diligence actions
""".strip()


def generate_prompt_files(input_path="data/seeds/startups_seed.csv", output_dir=OUTPUT_DIR):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    df = score_dataframe(pd.read_csv(input_path))
    paths = []
    for _, row in df.iterrows():
        slug = str(row.get("name", "startup")).lower().replace(" ", "-").replace("/", "-")
        path = output_dir / f"{slug}_prompt.md"
        path.write_text(build_enrichment_prompt(row), encoding="utf-8")
        paths.append(path)
    return paths


if __name__ == "__main__":
    for path in generate_prompt_files():
        print(path)
