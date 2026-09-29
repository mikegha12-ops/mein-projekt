#!/usr/bin/env python3
"""repo-check: prüft, ob ein Projektordner die wichtigsten Dateien hat."""
import argparse
import json
import sys
from pathlib import Path

# (Name, Dateimuster, Punkte, Tipp)
CHECKS = [
    ("README", ["README.md", "README.rst", "README.txt"], 3,
     "Erkläre, was dein Projekt tut und wie man es benutzt."),
    ("Lizenz", ["LICENSE", "LICENSE.md", "LICENSE.txt"], 3,
     "Ohne Lizenz darf niemand deinen Code legal nutzen (z. B. MIT)."),
    (".gitignore", [".gitignore"], 1,
     "Verhindert, dass Müll-Dateien im Repository landen."),
    ("Tests", ["tests", "test", "test_*.py", "*.test.js"], 2,
     "Tests zeigen, dass dein Code funktioniert."),
    ("CONTRIBUTING", ["CONTRIBUTING.md"], 1,
     "Erkläre anderen, wie sie mithelfen können."),
    ("CI", [".github/workflows/*.yml", ".github/workflows/*.yaml"], 2,
     "Automatische Tests bei jedem Push (GitHub Actions)."),
    ("CHANGELOG", ["CHANGELOG.md"], 1,
     "Halte fest, was sich in jeder Version geändert hat."),
]


def has_any(root: Path, patterns) -> bool:
    return any(next(root.glob(p), None) is not None for p in patterns)


def check(root: Path):
    """Gibt (Ergebnisliste, Punkte, Maximalpunkte) zurück."""
    results, score, total = [], 0, 0
    for name, patterns, points, tip in CHECKS:
        ok = has_any(root, patterns)
        results.append((name, ok, tip))
        total += points
        if ok:
            score += points
    return results, score, total


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Prüft die Gesundheit eines Projektordners.")
    parser.add_argument("pfad", nargs="?", default=".", help="Projektordner (Standard: aktueller Ordner)")
    parser.add_argument("--json", action="store_true", help="Ausgabe als JSON")
    args = parser.parse_args(argv)

    root = Path(args.pfad)
    if not root.is_dir():
        print(f"Fehler: '{root}' ist kein Ordner.", file=sys.stderr)
        return 2

    results, score, total = check(root)
    if args.json:
        print(json.dumps({
            "score": score,
            "total": total,
            "checks": [{"name": n, "ok": ok, "tip": tip} for n, ok, tip in results],
        }, ensure_ascii=False, indent=2))
        return 0 if score == total else 1
    for name, ok, tip in results:
        print(f"[{'x' if ok else ' '}] {name}" + ("" if ok else f"  -> {tip}"))
    print(f"\nPunkte: {score}/{total}")
    return 0 if score == total else 1


if __name__ == "__main__":
    sys.exit(main())
