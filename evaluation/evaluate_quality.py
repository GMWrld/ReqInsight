import csv
from pathlib import Path

from reqinsight.models.requirement import Requirement
from reqinsight.nlp.requirement_analyzer import RequirementAnalyzer
from reqinsight.quality.quality_rule_engine import QualityRuleEngine


# ============================================================
# ReqInsight Quality Evaluation
# ============================================================
#
# This script evaluates the existing ReqInsight quality-analysis
# pipeline against the manually annotated 100-requirement dataset.
#
# It does NOT modify the ReqInsight analysis logic.
#
# Evaluation metrics:
#   - True Positive (TP)
#   - False Positive (FP)
#   - False Negative (FN)
#   - True Negative (TN)
#   - Precision
#   - Recall
#   - F1-score
#   - Accuracy
#
# ============================================================


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    PROJECT_ROOT
    / "evaluation"
    / "evaluation_dataset.csv"
)


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Evaluation dataset not found: {DATASET_PATH}"
        )

    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        return list(csv.DictReader(file))


# ============================================================
# LABEL CONVERSION
# ============================================================

def to_binary(value):

    return 1 if str(value).strip().lower() in {
        "1",
        "true",
        "yes",
        "y"
    } else 0


# ============================================================
# RUN REQINSIGHT QUALITY ANALYSIS
# ============================================================

def analyze_requirement(
    requirement_id,
    requirement_text,
    analyzer,
    rule_engine
):

    requirement = Requirement(
        requirement_id=requirement_id,
        text=requirement_text
    )

    # Use the same analysis path used by the actual
    # ReqInsight quality-analysis pipeline.
    analysis = analyzer.analyze(requirement)

    findings = rule_engine.evaluate(analysis)

    predictions = {
        "modal_issue": 0,
        "vague_issue": 0,
        "measurability_issue": 0,
        "verifiability_issue": 0,
    }

    for finding in findings:

        rule = finding.get("rule")

        if rule == "MODAL-CONSISTENCY":

            predictions["modal_issue"] = 1

        elif rule in {
            "VAGUE-TERM",
            "VAGUENESS"
        }:

            predictions["vague_issue"] = 1

        elif rule == "MEASURABILITY":

            predictions["measurability_issue"] = 1

        elif rule == "VERIFIABILITY":

            predictions["verifiability_issue"] = 1

    return predictions, findings


# ============================================================
# CONFUSION MATRIX
# ============================================================

def classify(ground_truth, prediction):

    if ground_truth == 1 and prediction == 1:
        return "TP"

    if ground_truth == 0 and prediction == 1:
        return "FP"

    if ground_truth == 1 and prediction == 0:
        return "FN"

    return "TN"


# ============================================================
# METRICS
# ============================================================

def calculate_metrics(results):

    tp = results["TP"]
    fp = results["FP"]
    fn = results["FN"]
    tn = results["TN"]

    precision = (
        tp / (tp + fp)
        if tp + fp > 0
        else 0
    )

    recall = (
        tp / (tp + fn)
        if tp + fn > 0
        else 0
    )

    f1 = (
        2 * precision * recall
        / (precision + recall)
        if precision + recall > 0
        else 0
    )

    accuracy = (
        (tp + tn)
        / (tp + fp + fn + tn)
        if tp + fp + fn + tn > 0
        else 0
    )

    return {
        "TP": tp,
        "FP": fp,
        "FN": fn,
        "TN": tn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "accuracy": accuracy,
    }


# ============================================================
# MAIN EVALUATION
# ============================================================

def main():

    rows = load_dataset()

    print()
    print("=" * 70)
    print("REQINSIGHT QUALITY ANALYSIS EVALUATION")
    print("=" * 70)

    print(
        f"Dataset: {DATASET_PATH}"
    )

    print(
        f"Requirements evaluated: {len(rows)}"
    )

    print("=" * 70)

    analyzer = RequirementAnalyzer()
    rule_engine = QualityRuleEngine()

    rules = [
        "modal_issue",
        "vague_issue",
        "measurability_issue",
        "verifiability_issue",
    ]

    results = {
        rule: {
            "TP": 0,
            "FP": 0,
            "FN": 0,
            "TN": 0,
        }
        for rule in rules
    }

    errors = {
        rule: []
        for rule in rules
    }

    # ========================================================
    # PROCESS ALL REQUIREMENTS
    # ========================================================

    for row in rows:

        requirement_id = row["requirement_id"]
        requirement_text = row["requirement_text"]

        predictions, findings = analyze_requirement(
            requirement_id,
            requirement_text,
            analyzer,
            rule_engine
        )

        for rule in rules:

            ground_truth = to_binary(
                row.get(rule, 0)
            )

            prediction = predictions[rule]

            result = classify(
                ground_truth,
                prediction
            )

            results[rule][result] += 1

            if result in {"FP", "FN"}:

                errors[rule].append({
                    "id": requirement_id,
                    "domain": row["domain"],
                    "text": requirement_text,
                    "type": result,
                    "findings": findings,
                })

    # ========================================================
    # PERFORMANCE RESULTS
    # ========================================================

    print()
    print("QUALITY DETECTION PERFORMANCE")
    print("-" * 70)

    all_results = {
        rule: calculate_metrics(results[rule])
        for rule in rules
    }

    for rule in rules:

        metrics = all_results[rule]

        print()
        print(rule.upper())
        print("-" * 50)

        print(
            f"TP: {metrics['TP']}   "
            f"FP: {metrics['FP']}   "
            f"FN: {metrics['FN']}   "
            f"TN: {metrics['TN']}"
        )

        print(
            f"Precision: {metrics['precision']:.4f} "
            f"({metrics['precision'] * 100:.2f}%)"
        )

        print(
            f"Recall:    {metrics['recall']:.4f} "
            f"({metrics['recall'] * 100:.2f}%)"
        )

        print(
            f"F1-score:  {metrics['f1']:.4f} "
            f"({metrics['f1'] * 100:.2f}%)"
        )

        print(
            f"Accuracy:  {metrics['accuracy']:.4f} "
            f"({metrics['accuracy'] * 100:.2f}%)"
        )

    # ========================================================
    # ERROR ANALYSIS
    # ========================================================

    print()
    print("=" * 70)
    print("FALSE POSITIVES AND FALSE NEGATIVES")
    print("=" * 70)

    for rule in rules:

        print()
        print(rule.upper())
        print("-" * 70)

        if not errors[rule]:

            print("None.")

            continue

        for error in errors[rule]:

            print(
                f"[{error['type']}] "
                f"{error['id']} "
                f"({error['domain']})"
            )

            print(
                f"Text: {error['text']}"
            )

            detected_rules = [
                finding.get("rule")
                for finding in error["findings"]
            ]

            print(
                f"ReqInsight findings: "
                f"{detected_rules}"
            )

            print()

    # ========================================================
    # IMPLEMENTATION NOTES
    # ========================================================

    print()
    print("=" * 70)
    print("IMPLEMENTATION NOTES")
    print("=" * 70)

    print(
        "The current QualityRuleEngine actively evaluates:"
    )

    print(
        "  - MODAL-CONSISTENCY"
    )

    print(
        "  - VAGUE-TERM"
    )

    print(
        "  - MEASURABILITY"
    )

    print()

    print(
        "VERIFIABILITY is retained in the evaluation schema "
        "for future/extended evaluation, but is not currently "
        "an independently emitted QualityRuleEngine finding."
    )

    print()
    print("=" * 70)
    print("EVALUATION COMPLETE")
    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()