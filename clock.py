from PIL import Image, ImageDraw, ImageFont
import imageHelper
import datetime


class Clock:
    def __init__(self) -> None:
        pass

    def PrintClock(self):
        print(datetime.datetime.now())

    def DrawClock(
        self, draw: ImageDraw.ImageDraw, fonts, x1: int, y1: int, x2: int, y2: int
    ):
        imageHelper.DrawDots(draw, x1, y1, x2, y2, 8)
        draw.text(
            (x1 + 45, y1 + 15),
            datetime.datetime.now().strftime("%H:%M"),
            font=fonts["font30bold"],
            fill=0,
        )
        draw.text(
            (x1 + 40, y1 + 55),
            datetime.datetime.now().strftime("%Y-%m-%d"),
            font=fonts["font18"],
            fill=0,
        )
