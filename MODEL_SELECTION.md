# Model selection

## The question
The model predicts whether a telecom customer is likely to churn.
A false negative may cause the company to miss a customer who is about to leave, while a false positive may lead to unnecessary retention offers.

## Candidates

| Candidate | Why I tried it | AUC | F1 | F1 per slice (lowest) | p95 latency (ms) | Size (KB) | MLflow run ID |
|---|---|---:|---:|---:|---:|---:|---|
| Logistic Regression | Simple, fast baseline | 0.7982 | 0.4948 | 0.2500 (one-year, two-year) | 2.8555 | 3.55 | b5b8fe303c7e45bb8e023559062baf05 |
| Random Forest | Captures nonlinear patterns | 0.7589 | 0.4536 | 0.2222 (one-year) | 12.8102 | 3160.13 | d90d7c918c804286b0c0ca7933d9646f |
| Gradient Boosting | Boosted tree-based model | 0.7476 | 0.4167 | 0.2222 (two-year) | 2.8388 | 141.68 | 7aa2accf998d44debc053666cedf9286 |

All candidates used the same dataset hash: `76a6447e764b`.

## The champion
Logistic Regression is the selected candidate because it achieved the highest F1 (0.4948) and AUC (0.7982), while maintaining low p95 latency (2.8555 ms) and the smallest model size (3.55 KB). Its weakest slice F1 is 0.25, which remains a limitation. The other models did not improve the weakest-slice performance.

## My promotion rules
- Latency budget (p95): 25 ms, because the prediction API should remain responsive.
- Minimum gain to replace the champion (F1 points): 0.01, because a new model should improve F1 by at least one percentage point before replacing the current production model.

## What I would check next
The one-year and two-year contract groups have low F1. I would inspect their sample sizes, collect more representative examples, and evaluate performance across time before relying on this model in production.
