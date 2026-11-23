import argparse
import json
from pathlib import Path

from models import Task

FITXER_TASQUES = (
    Path(__file__).resolve().parent.parent / "data" / "tasks.json"
)


def carregar_tasques() -> list[Task]:
    if not FITXER_TASQUES.exists():
        FITXER_TASQUES.parent.mkdir(parents=True, exist_ok=True)
        FITXER_TASQUES.write_text("[]", encoding="utf-8")
    with FITXER_TASQUES.open(encoding="utf-8") as fitxer:
        dades = json.load(fitxer)
    return [Task.from_dict(registre) for registre in dades]


def desar_tasques(tasques: list[Task]) -> None:
    registres = [tasca.to_dict() for tasca in tasques]
    with FITXER_TASQUES.open("w", encoding="utf-8") as fitxer:
        json.dump(registres, fitxer, ensure_ascii=False, indent=2)


def afegir_tasca(títol: str, assignatura: str) -> None:
    tasques = carregar_tasques()
    nou_id = max((tasca.id for tasca in tasques), default=0) + 1
    tasca = Task(
        id=nou_id, títol=títol, assignatura=assignatura, estat="pendent"
    )
    tasques.append(tasca)
    desar_tasques(tasques)
    print(f"Tasca [ID: {tasca.id}] creada amb èxit")


def llistar_tasques() -> None:
    tasques = carregar_tasques()
    if not tasques:
        print("Registre de tasques buit.")
        return
    for tasca in tasques:
        print(
            f"[{tasca.id}] {tasca.títol} "
            f"({tasca.assignatura}) - estat: {tasca.estat}"
        )


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tasks_app",
        description="Gestor CLI de tasques acadèmiques",
    )
    subparsers = parser.add_subparsers(dest="comandament", required=True)

    parser_add = subparsers.add_parser("add", help="Crear una nova tasca")
    parser_add.add_argument(
        "--title", required=True, help="Títol de la tasca"
    )
    parser_add.add_argument(
        "--subject", required=True, help="Assignatura de la tasca"
    )

    subparsers.add_parser("list", help="Llistar totes les tasques")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = crear_parser()
    args = parser.parse_args(argv)
    if args.comandament == "add":
        afegir_tasca(args.title, args.subject)
    elif args.comandament == "list":
        llistar_tasques()


if __name__ == "__main__":
    main()