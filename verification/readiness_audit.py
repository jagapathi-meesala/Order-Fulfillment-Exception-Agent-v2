from pathlib import Path
import re, sys
ROOT = Path(__file__).resolve().parents[1]
required = ["agent.yaml", "SOUL.md", "RULES.md", "DUTIES.md", "AGENTS.md", "EXPLAINABILITY.md", "README.md", "requirements.txt", "core/engine.py", "core/cli.py", "tests/test_engine.py", "examples/fulfillment_case.json", "tools/validate-order-data.yaml", "tools/classify-fulfillment-exceptions.yaml", "tools/generate-exception-report.yaml", "skills/order-exception-triage/SKILL.md", "skills/inventory-reconciliation/SKILL.md", "skills/shipping-delay-analysis/SKILL.md"]
missing = [p for p in required if not (ROOT / p).is_file()]
text = (ROOT / "agent.yaml").read_text()
name_ok = bool(re.search(r'^name:\s*order-fulfillment-exception-agent\s*$', text, re.M))
explain = (ROOT / "EXPLAINABILITY.md").read_text()
sections_ok = all(f"## {s}" in explain for s in ["Inputs", "Decision", "Limits"])
print(f"Required files: {len(required)-len(missing)}/{len(required)}")
print(f"Agent name valid: {'PASS' if name_ok else 'FAIL'}")
print(f"Explainability sections: {'PASS' if sections_ok else 'FAIL'}")
if missing: print("Missing:", ", ".join(missing))
sys.exit(bool(missing) or not name_ok or not sections_ok)
