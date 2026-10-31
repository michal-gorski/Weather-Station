import requests
from PIL import Image, ImageDraw, ImageFont
import imageHelper
import logging
logger = logging.getLogger(__name__)

class Smog:
    NO_DATA = "Brak danych"

    def __init__(self) -> None:
        logger.info("Getting data on smog")
        self.Smog10 = self.NO_DATA
        self.Smog25 = self.NO_DATA
        try:
            response = requests.get(
                "https://api.gios.gov.pl/pjp-api/v1/rest/aqindex/getIndex/736", timeout=10
            )
            response.raise_for_status()
            index = response.json()["AqIndex"]
            # "wskażnik" is misspelled in the GIOŚ API itself; values are null when there is no index
            self.Smog10 = index.get("Nazwa kategorii indeksu dla wskażnika PM10") or self.NO_DATA
            self.Smog25 = index.get("Nazwa kategorii indeksu dla wskażnika PM2.5") or self.NO_DATA
        except (requests.exceptions.RequestException, KeyError, ValueError) as e:
            logger.error("Error fetching smog data: " + str(e))

        logger.info("Smog collected: " + self.Smog10 + " | " + self.Smog25)

    def PrintSmog(self):
        print("Pył PM 2.5: ", self.Smog25)
        print("Pył PM 10: ", self.Smog10)

    def DrawSmog(
        self, draw: ImageDraw.ImageDraw, fonts, x1: int, y1: int, x2: int, y2: int
    ):
        draw.text((x1, y1 + 9), "Pył PM 2.5: ", fill=0, font=fonts["font14light"])
        draw.text((x1, y1 + 24), self.Smog25, fill=0, font=fonts["font14"])

        draw.text((x1, y1 + 51), "Pył PM 10: ", fill=0, font=fonts["font14light"])
        draw.text((x1, y1 + 66), self.Smog10, fill=0, font=fonts["font14"])

        imageHelper.DrawDottedVerticalLine(draw, x1 - 15, y1, y2, 4)
