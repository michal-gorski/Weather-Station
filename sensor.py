from PIL import Image,ImageDraw,ImageFont
import imageHelper

class Sensor:
    temperature = 24.1
    humidity = 38
    sensorName = 'Taras'

    def __init__(self) -> None:
        pass
    def PrintSensor(self):
        print('Sensor: '+ self.sensorName,'| Temperature: ',self.temperature,' | Humidity: ',self.humidity)

    def DrawSensor(self,draw:ImageDraw.ImageDraw,fonts,x1:int,y1:int,x2:int,y2:int):
        draw.text((x1+10,y1+5),'TARAS',0,fonts['font18'])
        draw.text((x1 +10,y1+18),str(self.temperature) + '°',font=fonts['font48bold'],fill=0)
        draw.text((x1 + 10,y1+65),str(self.humidity) + '%',font=fonts['font30bold'],fill=0)
        imageHelper.DrawDottedVerticalLine(draw,140,0,y2,4)

        draw.text((x1+150,y1+5),'SALON',0,fonts['font18'])
        draw.text((x1 +150,y1+18),'--°',font=fonts['font48bold'],fill=0)
        draw.text((x1 + 150,y1+65),'--%',font=fonts['font30bold'],fill=0)
        imageHelper.DrawDottedVerticalLine(draw,280,0,y2,4)