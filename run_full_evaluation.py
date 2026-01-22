import csv
from modules.evaluation import evaluate_simplification
from modules.fir_simplifier import simplify_fir_text
import pandas as pd

DATASET_FILE = "evaluation_dataset.csv"   # Make sure this file exists

def run_full_evaluation(dataset_path):
    results = []

    with open(dataset_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            original = row["original_text"]
            reference = row["reference_simplified"]

            print("\nEvaluating Case...")
            print("---------------------------------------------------")
            print(f"Original Length: {len(original)} characters")

            # STEP 1: Generate output using your system
            simplified_output = simplify_fir_text(original)

            # STEP 2: Evaluate using the scoring function
            metrics = evaluate_simplification(original, simplified_output)

            # Add useful info for report
            metrics["reference"] = reference
            metrics["system_output"] = simplified_output

            print(f"Score for this entry: {metrics['accuracy_score']}%")

            results.append(metrics)

    return results


if __name__ == "__main__":
    print("\n📊 Starting Full System Evaluation...\n")

    output = run_full_evaluation(DATASET_FILE)

    # Compute average score
    avg_accuracy = sum(o["accuracy_score"] for o in output) / len(output)

    print("\n===================================================")
    print(f" FINAL PROJECT ACCURACY: {round(avg_accuracy,2)} %")
    print("===================================================\n")

    # Save results in a CSV for report
    df = pd.DataFrame(output)
    df.to_csv("full_evaluation_results.csv", index=False)

    print("📁 Results saved as: full_evaluation_results.csv\n")
    print("✅ Evaluation Completed Successfully.\n")
