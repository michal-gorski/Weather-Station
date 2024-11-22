import sys
import os
from PIL import Image, ImageDraw, ImageFont

libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib")
if os.path.exists(libdir):
    sys.path.append(libdir)


class Plotter:
    screen = ""
    draw = ""
    epd = ""
    width = 0
    height = 0

    firstVertical = 0
    secondHorizontal = 0
    firstHorizontal = 0
    secondVertical = 0

    fonts = {}
    icons = {}

    def __init__(self, width, height) -> None:
        self.screen = Image.new("L", (width, height), 255)  # 255: clear the frame
        self.draw = ImageDraw.Draw(self.screen)

        self.width = self.screen.width
        self.height = self.screen.height

        self.firstHorizontal = round(self.height * 0.2)
        self.secondHorizontal = round(self.height * 0.2)
        self.thirdHorizontal = round(self.height * 0.6)
        self.fourthHorizontal = self.height - round(self.height * 0.2)

        self.firstVertical = round(self.width * 0.3)
        self.secondVertical = round(self.width - self.width * 0.2)

        # load fonts
        path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "Roboto-Medium.ttf"
        )
        self.fonts["font30"] = ImageFont.truetype(path, 30)
        self.fonts["font24"] = ImageFont.truetype(path, 24)
        self.fonts["font18"] = ImageFont.truetype(path, 18)
        self.fonts["font16"] = ImageFont.truetype(path, 16)
        self.fonts["font14"] = ImageFont.truetype(path, 14)
        self.fonts["font10"] = ImageFont.truetype(path, 10)
        self.fonts["font8"] = ImageFont.truetype(path, 8)

        path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "Roboto-Light.ttf"
        )
        self.fonts["font30light"] = ImageFont.truetype(path, 30)
        self.fonts["font24light"] = ImageFont.truetype(path, 24)
        self.fonts["font18light"] = ImageFont.truetype(path, 18)
        self.fonts["font16light"] = ImageFont.truetype(path, 16)
        self.fonts["font14light"] = ImageFont.truetype(path, 14)
        self.fonts["font10light"] = ImageFont.truetype(path, 10)
        self.fonts["font8light"] = ImageFont.truetype(path, 8)

        path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "Roboto-Bold.ttf"
        )
        self.fonts["font30bold"] = ImageFont.truetype(path, 30)
        self.fonts["font24bold"] = ImageFont.truetype(path, 24)
        self.fonts["font18bold"] = ImageFont.truetype(path, 18)
        self.fonts["font16bold"] = ImageFont.truetype(path, 16)
        self.fonts["font14bold"] = ImageFont.truetype(path, 14)
        self.fonts["font10bold"] = ImageFont.truetype(path, 10)
        self.fonts["font8bold"] = ImageFont.truetype(path, 8)

        # load icons
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Icons")
        self.icons["cloudy_small"] = Image.open(os.path.join(path, "cloudy_small.png"))
        self.icons["partly_cloudy_small"] = Image.open(
            os.path.join(path, "partly_cloudy_small.png")
        )
        self.icons["rain_and_snow_small"] = Image.open(
            os.path.join(path, "rain_and_snow_small.png")
        )
        self.icons["scattered_showers_small"] = Image.open(
            os.path.join(path, "scattered_showers_small.png")
        )
        self.icons["mostly_cloudy_small"] = Image.open(
            os.path.join(path, "mostly_cloudy_small.png")
        )
        self.icons["mostly_cloudy_night_small"] = Image.open(
            os.path.join(path, "mostly_cloudy_night_small.png")
        )
        self.icons["mostly_clear_night_small"] = Image.open(
            os.path.join(path, "mostly_clear_night_small.png")
        )
        self.icons["clear_night_small"] = Image.open(
            os.path.join(path, "clear_night_small.png")
        )
        self.icons["snow_small"] = Image.open(os.path.join(path, "snow_small.png"))
        self.icons["mostly_sunny_small"] = Image.open(
            os.path.join(path, "mostly_sunny_small.png")
        )

        self.icons["wind_small"] = Image.open(os.path.join(path, "wind_small.png"))
        self.icons["rain_percent_small"] = Image.open(
            os.path.join(path, "rain_percent_small.png")
        )

    def PrepareGrid(self):
        import imageHelper

        self.screen = Image.new("L", (800, 480), 255)  # 255: clear the frame
        self.draw = ImageDraw.Draw(self.screen)

        # horizontal line 1
        self.draw.line(
            (0, self.firstHorizontal, self.width, self.firstHorizontal), fill=0
        )
        imageHelper.DrawDottedHorizontalLine(
            self.draw, 0, self.firstHorizontal + 2, self.width, 4
        )

        # vertical line 1
        self.draw.line(
            (self.firstVertical, self.firstHorizontal, self.firstVertical, self.height),
            fill=0,
        )
        imageHelper.DrawDottedVerticalLine(
            self.draw, self.firstVertical + 2, self.firstHorizontal, self.height, 4
        )

        # horizontal line2
        self.draw.line(
            (
                self.firstVertical,
                self.secondHorizontal,
                self.width,
                self.secondHorizontal,
            ),
            fill=0,
        )
        imageHelper.DrawDottedHorizontalLine(
            self.draw, self.firstVertical, self.secondHorizontal + 2, self.width, 4
        )

        # horizontal line3
        self.draw.line(
            (
                self.firstVertical,
                self.thirdHorizontal,
                self.width,
                self.thirdHorizontal,
            ),
            fill=0,
        )
        imageHelper.DrawDottedHorizontalLine(
            self.draw, self.firstVertical, self.thirdHorizontal + 2, self.width, 4
        )

        # horizontal line 4
        self.draw.line(
            (
                self.firstVertical,
                self.fourthHorizontal,
                self.width,
                self.fourthHorizontal,
            ),
            fill=0,
        )
        imageHelper.DrawDottedHorizontalLine(
            self.draw, self.firstVertical, self.fourthHorizontal + 2, self.width, 4
        )

        # vertical line 2
        self.draw.line(
            (self.secondVertical, 0, self.secondVertical, self.firstHorizontal), fill=0
        )
        imageHelper.DrawDottedVerticalLine(
            self.draw, self.secondVertical + 2, 0, self.firstHorizontal, 4
        )

    def EpdInit(self):

        try:
            from waveshare_epd import epd7in5_V2

            self.epd = epd7in5_V2.EPD()
            self.epd.init()
            self.epd.Clear()
            return True
        except Exception as e:
            print("Screen not found", str(e))
            return False

    def EpdSleep(self):
        self.epd.init()
        self.epd.Clear()
        self.epd.sleep()
        from waveshare_epd import epd7in5_V2

        epd7in5_V2.epdconfig.module_exit(cleanup=True)

    def Display(self):

        self.epd.display(self.epd.getbuffer(self.screen))

    def ShowImage(self):
        self.screen.show()
