import json
import shutil
import subprocess
import sys
from datetime import date, timedelta
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
            "data_limit": None,
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


def test_gs04_creacio_amb_data_limit(app):
    executar, fitxer_tasques = app

    resultat = executar(
        "add",
        "--title",
        "Entrega RS",
        "--subject",
        "RS",
        "--due",
        "2026-12-01",
    )

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "Tasca [ID: 1] creada amb èxit"
    dades = json.loads(fitxer_tasques.read_text(encoding="utf-8"))
    assert dades[0]["data_limit"] == "2026-12-01"


def test_gs05_llistat_tasca_caducada(app):
    executar, fitxer_tasques = app
    data_caducada = date.today() - timedelta(days=1)
    fitxer_tasques.write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "títol": "Pràctica antiga",
                    "assignatura": "RS",
                    "estat": "pendent",
                    "data_limit": data_caducada.isoformat(),
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    resultat = executar("list")

    assert resultat.returncode == 0
    assert resultat.stdout.strip().splitlines() == [
        "[1] Pràctica antiga (RS) - estat: pendent [CADUCADA]"
    ]


def test_gs06_llistat_tasca_urgent(app):
    executar, fitxer_tasques = app
    data_urgent = date.today() + timedelta(days=2)
    fitxer_tasques.write_text(
        json.dumps(
            [
                {
                    "id": 2,
                    "títol": "Examen demà",
                    "assignatura": "SO",
                    "estat": "pendent",
                    "data_limit": data_urgent.isoformat(),
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    resultat = executar("list")

    assert resultat.returncode == 0
    assert resultat.stdout.strip().splitlines() == [
        "[2] Examen demà (SO) - estat: pendent [URGENT]"
    ]


def test_gs07_modificacio_atributs_per_id(app):
    executar, fitxer_tasques = app
    fitxer_tasques.write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "títol": "Pràctica 1",
                    "assignatura": "RS",
                    "estat": "pendent",
                    "data_limit": None,
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    resultat = executar(
        "edit",
        "--id",
        "1",
        "--title",
        "Pràctica 1 Corregida",
        "--due",
        "2026-12-15",
    )

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "Tasca [ID: 1] modificada amb èxit"
    dades = json.loads(fitxer_tasques.read_text(encoding="utf-8"))
    assert dades == [
        {
            "id": 1,
            "títol": "Pràctica 1 Corregida",
            "assignatura": "RS",
            "estat": "pendent",
            "data_limit": "2026-12-15",
        }
    ]


def test_gs08_marcar_tasca_completada_per_id(app):
    executar, fitxer_tasques = app
    fitxer_tasques.write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "títol": "Pràctica 1",
                    "assignatura": "RS",
                    "estat": "pendent",
                    "data_limit": None,
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    resultat = executar("complete", "--id", "1")

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == (
        "Tasca [ID: 1] marcada com a completada"
    )
    dades = json.loads(fitxer_tasques.read_text(encoding="utf-8"))
    assert dades[0]["estat"] == "completada"


def test_gs09_resum_estadistic(app):
    executar, fitxer_tasques = app
    avui = date.today()
    tasques = [
        {
            "id": 1,
            "títol": "Pràctica feta",
            "assignatura": "RS",
            "estat": "completada",
            "data_limit": None,
        },
        {
            "id": 2,
            "títol": "Pràctica antiga",
            "assignatura": "RS",
            "estat": "pendent",
            "data_limit": (avui - timedelta(days=1)).isoformat(),
        },
        {
            "id": 3,
            "títol": "Examen proper",
            "assignatura": "SO",
            "estat": "pendent",
            "data_limit": (avui + timedelta(days=2)).isoformat(),
        },
    ]
    fitxer_tasques.write_text(
        json.dumps(tasques, ensure_ascii=False), encoding="utf-8"
    )

    resultat = executar("list", "--summary")

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == (
        "Total: 3 | Pendents: 2 | Completades: 1 | "
        "Caducades: 1 | Urgents: 1"
    )


def test_gs10_filtrat_per_assignatura(app):
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

    resultat = executar("list", "--subject", "RS")

    assert resultat.returncode == 0
    assert resultat.stdout.strip().splitlines() == [
        "[1] Pràctica 1 (RS) - estat: pendent"
    ]

    resultat = executar("list", "--subject", "rs")

    assert resultat.returncode == 0
    assert resultat.stdout.strip().splitlines() == [
        "[1] Pràctica 1 (RS) - estat: pendent"
    ]


def test_gs11_filtrat_per_paraula_clau(app):
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

    resultat = executar("list", "--keyword", "Examen")

    assert resultat.returncode == 0
    assert resultat.stdout.strip().splitlines() == [
        "[2] Examen parcial (SO) - estat: pendent"
    ]

    resultat = executar("list", "--keyword", "examen")

    assert resultat.returncode == 0
    assert resultat.stdout.strip().splitlines() == [
        "[2] Examen parcial (SO) - estat: pendent"
    ]
