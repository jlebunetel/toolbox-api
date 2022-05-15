import logging
import requests

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, validator
from typing import Union

logger = logging.getLogger(__name__)


class City(str, Enum):
    rennes = "rennes"


class Horaire(BaseModel):
    nomcourtligne: str  # "11"
    destination: str  # "Z.I. Ouest"
    idarret: str  # "1056"
    nomarret: str  # "Gares"
    depart: str  # "2022-05-15T15:19:00+02:00"

    @validator("depart")
    def convert_time(cls, v):
        depart = v
        depart_datetime: datetime = datetime.fromisoformat(depart)
        depart_short: str = depart_datetime.strftime("%H:%M")
        return depart_short

    def __str__(self):
        return "Départ du bus {nomcourtligne} à l'arrêt {nomarret} direction {destination} à {depart}".format(
            nomcourtligne=self.nomcourtligne,
            nomarret=self.nomarret,
            destination=self.destination,
            depart=self.depart,
        )


def get_next_bus(idarret: str = "1259", limit: int = 3) -> Union[list[Horaire], None]:
    # https://data.explore.star.fr/api/v2/console
    url = "https://data.explore.star.fr/api/v2/catalog/datasets/tco-bus-circulation-passages-tr/records/"

    headers = {
        "content-type": "application/json",
    }

    payload = {
        # "where": 'idarret = "1259" and idligne = "0005"',
        "where": 'idarret = "{}"'.format(idarret),
        "order_by": "depart",
        "timezone": "Europe/Paris",
        # "select": "nomcourtligne,destination,idarret,nomarret,depart",
        "limit": str(limit),
    }

    r = requests.get(
        url,
        headers=headers,
        params=payload,
    )
    logger.debug("url: %s", r.url)
    logger.debug("status code: %s", r.status_code)

    if r.status_code != requests.codes.ok:
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
