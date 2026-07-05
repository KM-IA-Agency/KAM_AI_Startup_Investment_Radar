from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.scoring import score_dataframe

OUTPUT_DIR = Path("reports/enrichment")


def slugify(value: str) -> str:
    return str(value).lower().replace(" ", "-").replace("/", "-").replace(".", "-")


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

Return JSON with:
- summary
- facts
- assumptions
- open_questions
- technical_due_diligence
- business_due_diligence
- valuation_questions
- red_flags
- next_actions
""".strip()


def infer_red_flags(row: pd.Series) -> list[str]:
    flags = []
    text = " ".join(str(row.get(col, "")) for col in ["sector", "sub_sector", "description", "stage"]).lower()
    if "gpu" in text or "cloud" in text:
        flags.append("Check capital intensity and gross margin under GPU price pressure.")
    if "biotech" in text or "medical" in text or "clinical" in text:
        flags.append("Check regulatory and scientific validation milestones.")
    if "foundation" in text or "model" in text:
        flags.append("Check differentiation versus larger foundation model providers.")
    if int(row.get("risk_score", 0)) >= 7:
        flags.append("Risk score is high; require deeper validation before investment decision.")
    if int(row.get("valuation_score", 0)) <= 5:
        flags.append("Valuation score is weak; entry price may already be demanding.")
    return flags or ["No major red flag detected from seed data; requires manual verification."]


def structured_offline_analysis(row: pd.Series) -> dict:
    name = row.get("name", "")
    sector = row.get("sector", "")
    sub_sector = row.get("sub_sector", "")
    decision = row.get("decision", "")
    total_score = int(row.get("total_score", 0))
    kamel_edge = int(row.get("kamel_edge_score", 0))

    return {
        "startup": {
            "name": name,
            "country": row.get("country", ""),
            "region": row.get("region", ""),
            "sector": sector,
            "sub_sector": sub_sector,
            "stage": row.get("stage", ""),
            "website": row.get("website", ""),
            "source_url": row.get("source_url", ""),
        },
        "summary": f"{name} is a {sector} startup focused on {sub_sector}.",
        "facts": [
            f"Country: {row.get('country', '')}",
            f"Sector: {sector}",
            f"Stage: {row.get('stage', '')}",
            f"Seed description: {row.get('description', '')}",
        ],
        "assumptions": [
            "Scores are initial MVP estimates and must be validated with fresh sources.",
            "Market and valuation attractiveness are approximate until funding and revenue data are verified.",
        ],
        "scores": {
            "total_score": total_score,
            "kamel_edge_score": kamel_edge,
            "decision": decision,
            "score_explanation": row.get("score_explanation", ""),
        },
        "technical_due_diligence": [
            "Check product architecture and dependency on third-party APIs.",
            "Verify whether the startup owns data, workflows, IP, integrations or distribution advantage.",
            "Look for demos, documentation, benchmarks, GitHub activity or technical publications.",
        ],
        "business_due_diligence": [
            "Verify paying customers, pilots, revenue, retention and sales cycle.",
            "Map 3 to 5 direct competitors and compare positioning.",
            "Check whether the product solves a painful and budgeted problem.",
        ],
        "valuation_questions": [
            "What was the last round size and implied valuation?",
            "What revenue or usage metric supports this valuation?",
            "Is a x5 or x10 outcome still plausible from the current entry price?",
        ],
        "red_flags": infer_red_flags(row),
        "open_questions": [
            "Can the product be tested directly?",
            "Who are the real users and economic buyers?",
            "What evidence proves traction beyond press and fundraising?",
            "What is the likely dilution path before exit?",
        ],
        "next_actions": [
            "Collect latest funding data.",
            "Review website, product docs and founder profiles.",
            "Compare with direct competitors.",
            "Update scoring manually after verification.",
        ],
        "disclaimer": "Analytical output only. Not personalized investment advice.",
    }


def write_markdown_report(analysis: dict, path: Path) -> None:
    startup = analysis["startup"]
    lines = [
        f"# Enrichment — {startup['name']}",
        "",
        f"Sector: {startup['sector']} / {startup['sub_sector']}",
        f"Country: {startup['country']}",
        f"Decision: {analysis['scores']['decision']}",
        f"Total score: {analysis['scores']['total_score']}",
        f"Kamel Edge: {analysis['scores']['kamel_edge_score']}",
        "",
        "## Summary",
        analysis["summary"],
        "",
        "## Facts",
        *[f"- {item}" for item in analysis["facts"]],
        "",
        "## Assumptions",
        *[f"- {item}" for item in analysis["assumptions"]],
        "",
        "## Technical due diligence",
        *[f"- {item}" for item in analysis["technical_due_diligence"]],
        "",
        "## Business due diligence",
        *[f"- {item}" for item in analysis["business_due_diligence"]],
        "",
        "## Valuation questions",
        *[f"- {item}" for item in analysis["valuation_questions"]],
        "",
        "## Red flags",
        *[f"- {item}" for item in analysis["red_flags"]],
        "",
        "## Next actions",
        *[f"- {item}" for item in analysis["next_actions"]],
        "",
        f"_{analysis['disclaimer']}_",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def generate_enrichment_files(input_path="data/seeds/startups_seed.csv", output_dir=OUTPUT_DIR):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    df = score_dataframe(pd.read_csv(input_path))
    paths = []
    for _, row in df.iterrows():
        slug = slugify(row.get("name", "startup"))
        prompt_path = output_dir / f"{slug}_prompt.md"
        json_path = output_dir / f"{slug}_analysis.json"
        md_path = output_dir / f"{slug}_analysis.md"
        analysis = structured_offline_analysis(row)
        prompt_path.write_text(build_enrichment_prompt(row), encoding="utf-8")
        json_path.write_text(json.dumps(analysis, indent=2, ensure_ascii=False), encoding="utf-8")
        write_markdown_report(analysis, md_path)
        paths.extend([prompt_path, json_path, md_path])
    return paths


if __name__ == "__main__":
    for path in generate_enrichment_files():
        print(path)
