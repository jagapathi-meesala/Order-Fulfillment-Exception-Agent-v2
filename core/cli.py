import argparse, json
from pathlib import Path
from .engine import analyze

def main():
    parser = argparse.ArgumentParser(description="Analyze order fulfillment exceptions from JSON.")
    parser.add_argument("input", help="Input JSON file")
    parser.add_argument("--output", help="Optional output JSON path")
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        parser.error(f"could not read valid JSON input: {exc}")
    report = analyze(data)
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if report["status"] != "invalid_input" else 2

if __name__ == "__main__":
    raise SystemExit(main())
