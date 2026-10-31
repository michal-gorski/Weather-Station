#!/usr/bin/python
# Checks whether the connected 7.5" panel can show red.
# Run on the Raspberry Pi:  python3 epd_red_test.py
#
# Expected on a black/white/red e-Paper (B) V2 panel: the screen flickers for ~20 s,
# then shows black text on the left and a red box with white text on the right.
# If no red appears (or the image is garbled), the panel is the black/white V2 model,
# which cannot show red: set Plotter.RED_DISPLAY = False in plotter.py.
import logging
import os
from PIL import Image, ImageDraw, ImageFont

from waveshare_epd import epd7in5b_V2

logging.basicConfig(level=logging.DEBUG)

fontPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Roboto-Bold.ttf")
font = ImageFont.truetype(fontPath, 40)

epd = epd7in5b_V2.EPD()
try:
    logging.info("init and Clear")
    if epd.init() != 0:
        raise RuntimeError("EPD init failed")
    epd.Clear()

    # the driver takes two black-on-white images: one for black pixels, one for red pixels
    black = Image.new("1", (epd.width, epd.height), 255)
    red = Image.new("1", (epd.width, epd.height), 255)
    blackDraw = ImageDraw.Draw(black)
    redDraw = ImageDraw.Draw(red)

    blackDraw.text((40, 60), "CZARNY", font=font, fill=0)
    blackDraw.rectangle((40, 160, 360, 420), outline=0, width=4)

    redDraw.text((440, 60), "CZERWONY", font=font, fill=0)
    redDraw.rectangle((440, 160, 760, 420), fill=0)
    # white text inside the red box: clear those pixels from the red layer
    redDraw.text((480, 260), "RED OK", font=font, fill=255)

    logging.info("display black + red")
    epd.display(epd.getbuffer(black), epd.getbuffer(red))

    logging.info("sleep (the image stays on the panel)")
    epd.sleep()
finally:
    epd7in5b_V2.epdconfig.module_exit(cleanup=True)
