import json


class Task:
    def __init__(
        self,
        id: int,
        títol: str,
        assignatura: str,
        estat: str = "pendent",
        data_limit: str | None = None,
    ) -> None:
        self.id = id
        self.títol = títol
        self.assignatura = assignatura
        self.estat = estat
        self.data_limit = data_limit

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "títol": self.títol,
            "assignatura": self.assignatura,
            "estat": self.estat,
            "data_limit": self.data_limit,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, dades: dict) -> "Task":
        return cls(
            id=dades["id"],
            títol=dades["títol"],
            assignatura=dades["assignatura"],
            estat=dades["estat"],
            data_limit=dades.get("data_limit"),
        )

    @classmethod
    def from_json(cls, text: str) -> "Task":
        return cls.from_dict(json.loads(text))
