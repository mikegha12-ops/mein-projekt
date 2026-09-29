# repo-check

Ein kleines Kommandozeilen-Tool, das prüft, ob dein Projektordner die wichtigsten
Dateien für ein gesundes Open-Source-Projekt hat: README, Lizenz, `.gitignore`,
Tests und CONTRIBUTING.

Keine Abhängigkeiten, nur Python 3.8+.

## Benutzung

```bash
python repo_check.py            # aktueller Ordner
python repo_check.py ./mein-projekt
python repo_check.py --json     # maschinenlesbar
```

Beispielausgabe:

```
[x] README
[x] Lizenz
[ ] .gitignore  -> Verhindert, dass Müll-Dateien im Repository landen.
[ ] Tests  -> Tests zeigen, dass dein Code funktioniert.
[ ] CONTRIBUTING  -> Erkläre anderen, wie sie mithelfen können.
[ ] CI  -> Automatische Tests bei jedem Push (GitHub Actions).
[ ] CHANGELOG  -> Halte fest, was sich in jeder Version geändert hat.

Punkte: 6/13
```

Exit-Code: `0` = alles vorhanden, `1` = etwas fehlt, `2` = ungültiger Pfad.
Damit lässt es sich auch in CI-Pipelines nutzen.

## Tests

```bash
pip install pytest
pytest
```

## Ideen für die Zukunft

- Weitere Checks (Code of Conduct, Issue-Templates)
- Veröffentlichung auf PyPI
- Konfigurierbare Regeln

Beiträge sind willkommen. Öffne gern ein Issue.

## Lizenz

MIT, siehe [LICENSE](LICENSE).
