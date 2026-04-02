"""
Transform the synthesized parquet dataset into NuExtract 2.0-compatible (text, template, target) triples.

No LLM involved — purely mechanical de-normalization of the SQL-like source data.

Input:  data/synthesized_data/train-00000-of-00001.parquet
Output: data/synthesized_data/nuextract_prompts.parquet

Output columns (only these three):
  text      — original source text (unchanged)
  template  — per-row NuExtract template reverse-engineered from entity_types/relation_types
  target    — de-normalized JSON NuExtract should produce (integer IDs resolved to entity names)

Template format:
  {
      "EntityType1": [],
      "EntityType2": [],
      "Relations": {
          "predicate1": [{"subject": "", "object": ""}]
      }
  }
"""

import json
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path

INPUT_PATH  = Path("data/synthesized_data/train-00000-of-00001.parquet")
OUTPUT_PATH = Path("data/synthesized_data/nuextract_prompts.parquet")


def build_template(entity_types: list, relation_types: list) -> str:
    """
    Reverse-engineer a NuExtract template from the entity and relation types in this row.
    Entity types become top-level keys mapping to [] (list of names).
    Relation types are nested under "Relations", each mapping to [{"subject": "", "object": ""}].
    """
    template = {}
    for et in sorted(entity_types):
        template[et] = []
    if relation_types:
        template["Relations"] = {
            rt: [{"subject": "", "object": ""}]
            for rt in sorted(relation_types)
        }
    return json.dumps(template, indent=4)


def build_target(entities: list, relations: list, entity_types: list, relation_types: list) -> str:
    """
    Build the target JSON NuExtract should produce, matching the template structure.
    De-normalizes the SQL-like source data by resolving integer IDs to entity names.
    """
    id_to_name = {e["id"]: e["name"] for e in entities}

    gt = {}
    for et in sorted(entity_types):
        gt[et] = [e["name"] for e in entities if e["type"] == et]

    if relation_types:
        gt["Relations"] = {}
        for rt in sorted(relation_types):
            gt["Relations"][rt] = [
                {
                    "subject": id_to_name.get(r["subject"], str(r["subject"])),
                    "object":  id_to_name.get(r["object"],  str(r["object"])),
                }
                for r in relations if r["predicate"] == rt
            ]

    return json.dumps(gt, indent=2)


def transform(input_path: Path, output_path: Path) -> None:
    table = pq.read_table(input_path)
    data  = table.to_pydict()

    templates = []
    targets   = []

    for entities, relations, entity_types, relation_types in zip(
        data["entities"], data["relations"], data["entity_types"], data["relation_types"]
    ):
        templates.append(build_template(entity_types, relation_types))
        targets.append(build_target(entities, relations, entity_types, relation_types))

    new_table = pa.table({
        "text":     pa.array(data["text"],  type=pa.string()),
        "template": pa.array(templates,     type=pa.string()),
        "target":   pa.array(targets,       type=pa.string()),
    })

    pq.write_table(new_table, output_path)
    print(f"Wrote {len(templates)} rows to {output_path}")
    print(f"Columns: {new_table.column_names}")


def spot_check(output_path: Path, n: int = 2) -> None:
    table = pq.read_table(output_path)
    data  = table.to_pydict()
    print(f"\n{'='*60}")
    print(f"SPOT CHECK — first {n} rows")
    print(f"{'='*60}")
    for i in range(n):
        print(f"\n--- Row {i} ---")
        print("TEXT:\n", data["text"][i])
        print("\nTEMPLATE:\n", data["template"][i])
        print("\nTARGET:\n", data["target"][i])


if __name__ == "__main__":
    transform(INPUT_PATH, OUTPUT_PATH)
    spot_check(OUTPUT_PATH)
