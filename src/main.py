"""Deterministic offline workflow example; no LLM is called."""
import argparse
import json
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "materials.json"
REQUIRED = ("topic", "audience", "platform", "duration_seconds", "style", "product_id")


def run(request):
    if not isinstance(request, dict):
        raise ValueError("input must be a JSON object")
    missing = [key for key in REQUIRED if request.get(key) is None or request.get(key) == ""]
    if missing:
        return {"status": "needs_input", "missing": missing, "trace": ["validate"]}
    for key in REQUIRED:
        if key != "duration_seconds" and not isinstance(request[key], str):
            raise ValueError(key + " must be a string")
    duration = request["duration_seconds"]
    if isinstance(duration, bool) or not isinstance(duration, int) or not 10 <= duration <= 120:
        raise ValueError("duration_seconds must be an integer between 10 and 120")
    if request.get("simulate_tool_failure"):
        return {"status": "tool_error", "error": "simulated material lookup failure",
                "retryable": True, "trace": ["validate", "lookup_failed"]}
    materials = json.loads(DATA.read_text(encoding="utf-8"))
    matches = [item for item in materials["items"] if item["product_id"] == request["product_id"]]
    if not matches:
        return {"status": "insufficient_evidence", "shots": [], "evidence": [],
                "risks": ["没有产品资料，请补充后再生成事实描述"], "trace": ["validate", "lookup"]}
    item = matches[0]
    # shortcut: fixed templates demonstrate delivery only; replace with a model for real generation.
    text = "；".join(item["facts"])
    minimum = (len(text) + 3) // 4
    if minimum > duration:
        return {"status": "duration_exceeded", "required_seconds": minimum,
                "trace": ["validate", "lookup", "estimate"]}
    return {"status": "completed", "mode": "offline_mock", "title": request["topic"],
            "audience": request["audience"], "platform": request["platform"],
            "style": request["style"],
            "shots": [{"start_seconds": 0, "end_seconds": duration,
                       "visual": "展示合成产品操作", "subtitle": text, "source_id": item["id"]}],
            "estimated_duration_seconds": duration,
            "evidence": [{"source_id": item["id"], "facts": item["facts"]}],
            "risks": ["离线模板；未进行语义合规审查和真实语速测量"],
            "trace": ["validate", "lookup", "template", "estimate", "output"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    try:
        request = json.loads(Path(args.input).read_text(encoding="utf-8"))
        print(json.dumps(run(request), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "invalid_input", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
