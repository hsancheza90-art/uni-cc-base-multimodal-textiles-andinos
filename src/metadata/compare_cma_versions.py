from pathlib import Path

import pandas as pd


def main() -> int:
    v1 = pd.read_csv("data/metadata/cma_andes_textiles_candidates.csv")
    v2 = pd.read_csv("data/metadata/cma_andes_textiles_candidates_v2.csv")

    v1_candidates = set(
        v1.loc[v1["curation_status"] == "candidate", "source_id"].astype(str)
    )

    v2_candidates = v2[v2["curation_status"] == "candidate"].copy()
    new_candidates = v2_candidates[
        ~v2_candidates["source_id"].astype(str).isin(v1_candidates)
    ]

    output_path = Path("data/metadata/cma_candidates_new_in_v2.csv")
    new_candidates.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"Candidatos v1: {len(v1_candidates)}")
    print(f"Candidatos v2: {len(v2_candidates)}")
    print(f"Nuevos candidatos en v2: {len(new_candidates)}")
    print(f"Archivo: {output_path}")

    if not new_candidates.empty:
        print(
            new_candidates[
                ["source_id", "title", "culture", "medium", "url"]
            ].to_string(index=False)
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())