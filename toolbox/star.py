import logging
from datetime import datetime
from enum import Enum
from typing import Union

import requests
from pydantic import BaseModel, field_validator

logger = logging.getLogger(__name__)


class City(str, Enum):
    RENNES = "rennes"


class Horaire(BaseModel):
    nomcourtligne: str  # "11"
    destination: str  # "Z.I. Ouest"
    idarret: str  # "1056"
    nomarret: str  # "Gares"
    depart: str  # "2022-05-15T15:19:00+02:00"

    @field_validator("depart")
    @classmethod
    def convert_time(cls, v: str):
        depart_datetime = datetime.fromisoformat(v)
        depart_short = depart_datetime.strftime("%H:%M")
        return depart_short

    def __str__(self):
        return (
            f"Départ du bus {self.nomcourtligne} à l'arrêt {self.nomarret} direction "
            f"{self.destination} à {self.depart}"
        )


def get_next_bus(idarret: str = "1259", limit: int = 3) -> Union[list[Horaire], None]:
    # https://data.explore.star.fr/api/v2/console
    url = (
        "https://data.explore.star.fr/"
        "api/v2/catalog/datasets/tco-bus-circulation-passages-tr/records/"
    )

    headers = {
        "content-type": "application/json",
    }

    payload = {
        # "where": 'idarret = "1259" and idligne = "0005"',
        "where": f'idarret = "{idarret}"',
        "order_by": "depart",
        "timezone": "Europe/Paris",
        # "select": "nomcourtligne,destination,idarret,nomarret,depart",
        "limit": str(limit),
    }

    r = requests.get(
        url,
        headers=headers,
        params=payload,
        timeout=1000,
    )
    logger.debug("url: %s", r.url)
    logger.debug("status code: %s", r.status_code)

    if r.status_code != requests.codes.ok:  # pylint: disable=no-member
        return None

    horaires = []
    for record in r.json()["records"]:
        fields = record["record"]["fields"]
        horaires.append(Horaire(**fields))
    return horaires


def main() -> int:
    horaires = get_next_bus()

    if horaires:
        for horaire in horaires:
            logger.info(horaire)
    else:
        logger.info("Pas d'horaire")

    return 0


if __name__ == "__main__":
    # Rich traceback in the REPL:
    from rich import traceback

    _ = traceback.install()

    # Log to sys.stderr with rich text:
    from rich.logging import RichHandler

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True)],
    )

    # Call main function:
    import sys

    sys.exit(main())
