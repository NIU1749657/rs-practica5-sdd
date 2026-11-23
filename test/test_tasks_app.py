import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ARREL_PROJECTE = Path(__file__).resolve().parent.parent


@pytest.fixture
def app(tmp_path):
    desti_src = tmp_path / "src"
    shutil.copytree(
        ARREL_PROJECTE / "src",
        desti_src,
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    fitxer_tasques = tmp_path / "data" / "tasks.json"
    fitxer_tasques.parent.mkdir(parents=True)
    fitxer_tasques.write_text("[]", encoding="utf-8")

    def executar(*arguments):
        return subprocess.run(
            [sys.executable, str(desti_src / "tasks_app.py"), *arguments],
            cwd=tmp_path,
            capture_output=True,
            text=True,
        )

    return executar, fitxer_tasques


def test_gs01_creacio_correcta_duna_tasca(app):
    executar, fitxer_tasques = app

    resultat = executar(
        "add", "--title", "Pràctica 1", "--subject", "RS"
    )

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "Tasca [ID: 1] creada amb èxit"
    dades = json.loads(fitxer_tasques.read_text(encoding="utf-8"))
    assert dades == [
        {
            "id": 1,
            "títol": "Pràctica 1",
            "assignatura": "RS",
            "estat": "pendent",
        }
    ]


def test_gs02_llistat_amb_registre_buit(app):
    executar, _ = app

    resultat = executar("list")

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "Registre de tasques buit."


def test_gs03_llistat_amb_registres(app):
    executar, fitxer_tasques = app
    tasques = [
        {
            "id": 1,
            "títol": "Pràctica 1",
            "assignatura": "RS",
            "estat": "pendent",
        },
        {
            "id": 2,
            "títol": "Examen parcial",
            "assignatura": "SO",
            "estat": "pendent",
        },
    ]
    fitxer_tasques.write_text(
        json.dumps(tasques, ensure_ascii=False), encoding="utf-8"
    )

    resultat = executar("list")

    assert resultat.returncode == 0
    assert resultat.stdout.strip().splitlines() == [
        "[1] Pràctica 1 (RS) - estat: pendent",
        "[2] Examen parcial (SO) - estat: pendent",
    ]