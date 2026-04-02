# Benchmarking Methodology

## Task Type
This is a **named entity recognition (NER) + relation extraction (RE)** benchmark. The model receives a text and a JSON schema template, and must output a filled JSON matching the template structure.

## Why Micro-F1

We use **micro-averaged F1** rather than macro-averaged F1 (per-row average).

Micro-F1 aggregates TP, FP, and FN counts across the entire dataset before computing precision, recall, and F1:

```
micro-precision = total_TP / (total_TP + total_FP)
micro-recall    = total_TP / (total_TP + total_FN)
micro-F1        = 2 * P * R / (P + R)
```

**Why this matters:**
- Rows with more entities contribute proportionally more to the score — this reflects real extraction difficulty
- Avoids over-weighting short sentences (1 entity) vs long ones (10 entities)
- Directly comparable to published NER/RE benchmarks (CoNLL-2003, DocRED, TACRED all report micro-F1)

## Why Per-Class Breakdown

We report F1 separately for each entity type (e.g. "Person", "Organization") and each relation predicate (e.g. "is_part_of", "executes").

This reveals *where* the model fails — a high overall F1 can hide poor performance on rare or complex types.

## Matching Rules

| Decision | Choice | Reason |
|----------|--------|--------|
| Case sensitivity | Case-insensitive | Model may capitalize differently without being semantically wrong |
| Entity match | Name must match within its entity-type key | Type accuracy matters for zero-hallucination extraction |
| Relation match | (subject, object) pair must match within its predicate key | Predicate accuracy is part of the extraction task |
| Empty prediction | Counted as FN for all ground truth items | Model silence is a failure mode |

## TP, FP, FN — and why there is no TN

In extraction tasks there are no True Negatives. A TN would be "the model correctly didn't extract something" — but the space of things a model could hallucinate is infinite, so absence of hallucination cannot be counted as a score.

| Term | Meaning | Example |
|------|---------|---------|
| **TP** | Model extracted something that's in the ground truth | Predicted `"executive branch"` → it's there ✓ |
| **FP** | Model extracted something NOT in the ground truth (hallucination) | Predicted `"congress"` → not in ground truth |
| **FN** | Ground truth has something the model missed (omission) | `"executive branch"` in ground truth, model didn't output it |
| **TN** | ~~Correctly didn't extract something~~ | Undefined — infinite search space |

**Entity example** — ground truth: `"Government Entity": ["executive branch"]`, model predicts: `"Government Entity": ["executive branch", "congress"]`
- `"executive branch"` → TP
- `"congress"` → FP (hallucination)

**Relation example** — ground truth has `is_part_of: [{subject: "executive branch", object: "government"}]`, model outputs nothing for that predicate:
- The missing relation → FN (omission)

This is why F1 (which only uses TP, FP, FN) is the standard metric for extraction tasks rather than accuracy, which requires TN. Accuracy is used here only for **exact match** — did the model get the entire JSON perfectly right — which is a different question from per-entity correctness.

## Exact Match Accuracy

A row is an exact match only if **all** entities and relations match perfectly (no FP, no FN anywhere in the row). This is a strict upper-bound metric — useful for tracking progress toward zero-hallucination.

## References

- CoNLL-2003 shared task evaluation: Tjong Kim Sang & De Meulder (2003)
- DocRED evaluation: Yao et al. (2019)
- NuExtract-2.0 baseline: NuMind (2024) — https://huggingface.co/collections/numind/nuextract-20
