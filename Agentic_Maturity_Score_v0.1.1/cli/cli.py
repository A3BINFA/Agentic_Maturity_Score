import argparse, json
import pandas as pd
from scoring.core import assess_dataframe

def main():
    p = argparse.ArgumentParser(description="Agentic Maturity CLI")
    p.add_argument("input", help="Path to XLSX Questionnaire sheet")
    p.add_argument("--out", default="results.json", help="Output JSON path")
    args = p.parse_args()
    df = pd.read_excel(args.input, sheet_name="Questionnaire")
    result = assess_dataframe(df)
    with open(args.out, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
