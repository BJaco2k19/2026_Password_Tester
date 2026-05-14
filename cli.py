import argparse
import json
import sys
from getpass import getpass

from password_strength import score_password, classify_score, suggest_improvements


def main(argv=None):
    p = argparse.ArgumentParser(description="Simple password strength tester")
    p.add_argument("--password", "-p", help="Password to score (unsafe on shared terminals)")
    p.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = p.parse_args(argv)

    if args.password:
        pw = args.password
    else:
        try:
            pw = getpass("Password: ")
        except Exception:
            print("Unable to read password interactively.")
            sys.exit(2)

    result = score_password(pw)
    classification = classify_score(result["score"]) if isinstance(result, dict) else ""

    if args.json:
        out = {
            "score": result["score"],
            "classification": classification,
            "breakdown": result.get("breakdown"),
            "components": result.get("components"),
            "suggestions": suggest_improvements(pw),
        }
        print(json.dumps(out, indent=2))
        return

    print(f"Score: {result['score']} / 100 — {classification}")
    # print component scores if available
    comps = result.get("components")
    if comps:
        print("Components:")
        for name, info in comps.items():
            print(f"  {name.capitalize()}: {info['score']} — {info['classification']}")

    bd = result.get("breakdown", {})
    if bd:
        print("Breakdown:")
        for k, v in bd.items():
            print(f"  {k}: {v}")
    suggestions = suggest_improvements(pw)
    if suggestions:
        print("Suggestions:")
        for s in suggestions:
            print(f" - {s}")


if __name__ == "__main__":
    main()
