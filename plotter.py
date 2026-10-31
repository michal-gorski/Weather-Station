import sys
import os
from PIL import Image, ImageChops, ImageDraw, ImageFont
import logging
logger = logging.getLogger(__name__)

libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib")
if os.path.exists(libdir):
    sys.path.append(libdir)


class Plotter:
    # True for the black/white/red 7.5" e-Paper (B) V2 panel (driver epd7in5b_V2),
    # False for the black/white 7.5" V2 panel (driver epd7in5_V2), where red shows as grey.
    # Run epd_red_test.py on the Pi to find out which panel is connected.
    RED_DISPLAY = True

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
    epdReady = False

    def __init__(self, width, height) -> None:
        logger.info("Preparing plotter")
        self.screen = Image.new("RGB", (width, height), "white")  # RGB so modules can draw in imageHelper.RED
        self.draw = ImageDraw.Draw(self.screen)

        self.width = self.screen.width
        self.height = self.screen.height

        self.firstHorizontal = round(self.height * 0.2)
        self.secondHorizontal = round(self.height * 0.2)
        self.thirdHorizontal = round(self.height * 0.6)
        self.fourthHorizontal = self.height - round(self.height * 0.2)

        self.firstVertical = round(self.width * 0.25)
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
        self.fonts["font48bold"] = ImageFont.truetype(path, 48)
        self.fonts["font30bold"] = ImageFont.truetype(path, 30)
        self.fonts["font24bold"] = ImageFont.truetype(path, 24)
        self.fonts["font18bold"] = ImageFont.truetype(path, 18)
        self.fonts["font16bold"] = ImageFont.truetype(path, 16)
        self.fonts["font14bold"] = ImageFont.truetype(path, 14)
        self.fonts["font10bold"] = ImageFont.truetype(path, 10)
        self.fonts["font8bold"] = ImageFont.truetype(path, 8)

        # load icons: every Icons/<name>_small.png becomes icons["<name>_small"]
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Icons")
        for fileName in os.listdir(path):
            if fileName.endswith("_small.png"):
                self.icons[fileName[:-4]] = Image.open(os.path.join(path, fileName))

    def PrepareGrid(self):
        import imageHelper
        logger.info("Drawing grid")
        self.screen = Image.new("RGB", (self.width, self.height), "white")
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

    def EpdDriver(self):
        if self.RED_DISPLAY:
            from waveshare_epd import epd7in5b_V2
            return epd7in5b_V2
        from waveshare_epd import epd7in5_V2
        return epd7in5_V2

    def EpdInit(self):
        logger.info("Starting EPD init")
        try:
            self.epd = self.EpdDriver().EPD()
            self.epd.init()
            self.epd.Clear()
            self.epdReady = True
            logger.info("EPD Init OK")
            return True
        except Exception as e:
            logger.warning("Screen not found: "+ str(e))
            self.epdReady = False
            return False

    def EpdSleep(self):
        if not self.epdReady:
            return
        logger.info("Putting EPD to sleep")
        self.epd.init()
        self.epd.Clear()
        self.epd.sleep()
        self.EpdDriver().epdconfig.module_exit(cleanup=True)

    def SplitColors(self):
        """Split the RGB frame into black and red layers, both drawn black-on-white
        as the epd7in5b_V2 driver's getbuffer expects."""
        r, g, b = self.screen.split()
        # red-ish pixels (including anti-aliased red text edges) have much more red than green
        isRed = ImageChops.subtract(r, g).point(lambda v: 255 if v > 100 else 0)
        black = ImageChops.lighter(self.screen.convert("L"), isRed)  # red pixels -> white
        red = ImageChops.invert(isRed)  # red pixels -> black
        return black, red

    def Display(self):
        logger.info("Displaying forecast")
        if self.RED_DISPLAY:
            black, red = self.SplitColors()
            self.epd.display(self.epd.getbuffer(black), self.epd.getbuffer(red))
        else:
            self.epd.display(self.epd.getbuffer(self.screen.convert("L")))

    def ShowImage(self):
        self.screen.show()
