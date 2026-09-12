import json
import argparse
import os

def analyze_benchmarks(json_path="benchmark_results.json", selected_case="case_2"):
    if not os.path.exists(json_path):
        print(f"❌ Error: Results file '{json_path}' not found. Run batch_runner.py first.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Filter records matching the requested prompt case
    filtered_data = [
        item for item in data 
        if item.get("prompt_case", "case_2") == selected_case
    ]

    total_runs = len(filtered_data)
    if total_runs == 0:
        print(f"⚠️ No evaluation records found for prompt case '{selected_case}'.")
        return

    print("\n" + "=" * 60)
    print(f"   ANALYTICS DASHBOARD: [{selected_case.upper()}]")
    print("=" * 60)
    print(f"Total Resumes Evaluated : {total_runs}")

    # Case-specific analytics computation
    if selected_case == "case_1":
        unanchored_metric_penalties = 0
        stuffer_penalties = 0
        total_metrics_scanned = 0
        total_scores = []

        for entry in filtered_data:
            eval_body = entry.get("evaluation", {})
            total_scores.append(eval_body.get("adjusted_technical_score", 0))
            
            metrics = eval_body.get("metrics_audit", [])
            total_metrics_scanned += len(metrics)
            for m in metrics:
                if "Unverified" in m.get("validation_status", ""):
                    unanchored_metric_penalties += 1

            proofs = eval_body.get("skill_proofs", [])
            for p in proofs:
                if not p.get("is_anchored_in_project", True):
                    stuffer_penalties += 1

        avg_score = sum(total_scores) / max(1, total_runs)
        capture_rate = (unanchored_metric_penalties / max(1, total_metrics_scanned)) * 100

        print(f"Average Adjusted Score   : {avg_score:.1f}/100")
        print(f"Total Quantitative Claims : {total_metrics_scanned}")
        print(f"Unanchored Claims Caught  : {unanchored_metric_penalties}")
        print(f"Unbacked Skills Flagged   : {stuffer_penalties}")
        print("-" * 60)
        print(f"Metric Severity Capture Rate : {capture_rate:.1f}%")

    elif selected_case == "case_2":
        ats_scores = []
        total_missing_techs = 0

        for entry in filtered_data:
            eval_body = entry.get("evaluation", {})
            ats_scores.append(eval_body.get("overall_ats_match_score", 0))
            total_missing_techs += len(eval_body.get("missing_required_technologies", []))

        avg_ats = sum(ats_scores) / max(1, total_runs)
        print(f"Average ATS Match Score  : {avg_ats:.1f}%")
        print(f"Total Missing Tech Gaps   : {total_missing_techs}")

    elif selected_case == "case_3":
        scores = []
        unanchored_flags = 0

        for entry in filtered_data:
            eval_body = entry.get("evaluation", {})
            scores.append(eval_body.get("adjusted_technical_score", 0))
            unanchored_flags += len(eval_body.get("unanchored_claims_flagged", []))

        avg_score = sum(scores) / max(1, total_runs)
        print(f"Average Architect Score  : {avg_score:.1f}/100")
        print(f"Total Unanchored Flags   : {unanchored_flags}")

    elif selected_case == "case_4":
        high_gaps = 0
        for entry in filtered_data:
            eval_body = entry.get("evaluation", {})
            for dim in eval_body.get("benchmark_matrix", []):
                if dim.get("gap_severity") == "High":
                    high_gaps += 1

        print(f"Total High-Severity Gaps Flagged : {high_gaps}")

    elif selected_case == "case_5":
        verified_metrics_count = 0
        for entry in filtered_data:
            eval_body = entry.get("evaluation", {})
            verified_metrics_count += len(eval_body.get("verified_metrics_used", []))

        print(f"Total Verified Metrics in Letters : {verified_metrics_count}")

    print("=" * 60 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zero-Token Analytics Dashboard for Benchmarks")
    parser.add_argument(
        "--case",
        type=str,
        default="case_1",
        choices=["case_1", "case_2", "case_3", "case_4", "case_5"],
        help="Prompt case to analyze (default: case_1)"
    )
    args = parser.parse_args()
    analyze_benchmarks(json_path="benchmark_results.json", selected_case=args.case)