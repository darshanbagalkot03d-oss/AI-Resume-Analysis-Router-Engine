import json

def analyze_benchmarks(json_path="benchmark_results_gemini.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_runs = len(data)
    if total_runs == 0:
        print("No evaluation records found.")
        return

    unanchored_metric_penalties = 0
    stuffer_penalties = 0
    total_metrics_scanned = 0
    hallucination_exceptions = 0

    for entry in data:
        eval_body = entry.get("evaluation", {})
        
        # Check Metric Severity Capture
        metrics = eval_body.get("metrics_audit", [])
        total_metrics_scanned += len(metrics)
        for m in metrics:
            if m.get("validation_status") == "Unverified Metric":
                unanchored_metric_penalties += 1

        # Check Anti-Stuffing Capture
        proofs = eval_body.get("skill_proofs", [])
        for p in proofs:
            if not p.get("has_project_proof"):
                stuffer_penalties += 1

    print("\n" + "=" * 60)
    print("           SYSTEM BENCHMARK EVALUATION DASHBOARD           ")
    print("=" * 60)
    print(f"Total Resumes Evaluated : {total_runs}")
    print(f"Total Quantitative Claims : {total_metrics_scanned}")
    print(f"Unanchored Claims Caught  : {unanchored_metric_penalties}")
    print(f"Unbacked Skills Flagged   : {stuffer_penalties}")
    print("-" * 60)
    
    # Severity & Penalty Metrics
    print(f"Metric Severity Capture Rate : {(unanchored_metric_penalties / max(1, total_metrics_scanned)) * 100:.1f}%")
    print(f"Hallucination / Schema Exception Rate : {(hallucination_exceptions / total_runs) * 100:.2f}%")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    analyze_benchmarks()