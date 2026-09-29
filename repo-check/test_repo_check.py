import json
import tempfile
from pathlib import Path

from repo_check import check, main


def test_leerer_ordner_hat_null_punkte():
    with tempfile.TemporaryDirectory() as d:
        _, score, total = check(Path(d))
        assert score == 0 and total == 13


def test_readme_und_lizenz_geben_sechs_punkte():
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "README.md").write_text("hi")
        (Path(d) / "LICENSE").write_text("MIT")
        _, score, _ = check(Path(d))
        assert score == 6


def test_vollstaendiges_projekt_gibt_exit_code_null():
    with tempfile.TemporaryDirectory() as d:
        for f in ["README.md", "LICENSE", ".gitignore", "CONTRIBUTING.md",
                  "CHANGELOG.md", "test_x.py"]:
            (Path(d) / f).write_text("x")
        (Path(d) / ".github" / "workflows").mkdir(parents=True)
        (Path(d) / ".github" / "workflows" / "ci.yml").write_text("x")
        assert main([d]) == 0


def test_ungueltiger_pfad():
    assert main(["/gibt/es/nicht"]) == 2


def test_json_ausgabe(capsys):
    with tempfile.TemporaryDirectory() as d:
        main([d, "--json"])
        data = json.loads(capsys.readouterr().out)
        assert data["score"] == 0 and data["total"] == 13
        assert len(data["checks"]) == 7
