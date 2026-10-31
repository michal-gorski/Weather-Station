import requests
from PIL import Image,ImageDraw,ImageFont
import imageHelper
import logging
logger = logging.getLogger(__name__)

class WeatherWarnings:
    def __init__(self) -> None:
        logger.info("Getting weather warnings")
        self.weatherWarning = []
        self.fetchFailed = False
        try:
            response = requests.get('https://danepubliczne.imgw.pl/api/data/warningsmeteo',timeout=10)
            parsed = response.json()
        except (requests.exceptions.RequestException, ValueError) as e:
            logger.error("Error fetching weather warnings: " + str(e))
            self.fetchFailed = True
            return

        # With no active warnings IMGW returns a dict like {"message": "Brak ostrzeżeń..."} instead of a list
        if isinstance(parsed, list):
            filteredEvent = [event for event in parsed if "2261" in event.get('teryt', [])]

            for event in filteredEvent:
                self.weatherWarning.append(event['tresc'])
        logger.info("Received " + str(len(self.weatherWarning)) + " warnings.")

    def PrintWarnings(self):
        for warning in self.weatherWarning:
            print(warning)
            print('//////////')

    def DrawWarnings(self,draw:ImageDraw.ImageDraw,fonts,x1:int,y1:int,x2:int,y2:int):
        if self.fetchFailed:
            draw.text((x1+5,y1+8),"• Brak danych o ostrzeżeniach",0,fonts['font18light'])
            return
        if len(self.weatherWarning) == 0:
            draw.text((x1+5,y1+8),"• Brak ostrzeżeń",0,fonts['font18light'])
            return

        font = fonts['font18light'] if len(self.weatherWarning) == 1 else fonts['font14light']

        # draw on a separate canvas so long warnings are cut off at the box edge
        # instead of spilling into the daily forecast below
        box = Image.new(draw._image.mode, (x2-x1-4, y2-y1-4), "white")
        boxDraw = ImageDraw.Draw(box)
        y = 6
        for warning in self.weatherWarning:
            wrappedText = imageHelper.WrappedText('• '+warning,font,x2-x1-10)
            bottom = boxDraw.multiline_textbbox((5,y),wrappedText,font=font)[3]
            # skip warnings that don't fit whole (the first one is always shown, clipped if needed)
            if bottom > box.height and y > 6:
                break
            # active warnings are shown in red
            boxDraw.text((5,y),wrappedText,imageHelper.RED,font)
            y = bottom + 6
        draw._image.paste(box,(x1+4,y1+4))


if __name__ == "__main__":
    myWarnings = WeatherWarnings()
    myWarnings.PrintWarnings()