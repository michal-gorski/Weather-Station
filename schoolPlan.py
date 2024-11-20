import json
import sys
import os
from PIL import Image,ImageDraw,ImageFont
import imageHelper


class SchoolPlan:
    planData = ''
    dayOfWeek = 0
    currentPlan = ''

    def __init__(self) -> None:
        planPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),'plan.json')

        with open(planPath, 'r') as file:
            self.planData = json.load(file)

    def CurrentPlan(self):
        import datetime        
        dayOfWeek = datetime.datetime.today().weekday()
        time = datetime.datetime.now().hour
        
        if time > 12:
            dayOfWeek += 1

        if dayOfWeek >= 6:
            dayOfWeek = 0
        
        self.dayOfWeek = dayOfWeek
        self.CurrentPlan = self.PlanForDay(dayOfWeek)
        return self.CurrentPlan

    def PlanForDay(self,day):
        if (day < 0 or day > 5):
            return self.planData['0']
        else:
            return self.planData[str(day)]

    def PrintPlan(self):    
        print(self.WordDay(),': ',self.CurrentPlan)

    def WordDay(self):
        if self.dayOfWeek == 0: return "poniedziałek"
        elif self.dayOfWeek == 1: return "wtorek"
        elif self.dayOfWeek == 2: return "środa"
        elif self.dayOfWeek == 3: return "czwartek"
        elif self.dayOfWeek == 4: return "piątek"
        else: return ''

    def DrawPlan(self,draw:ImageDraw.ImageDraw,x1:int,y1:int,x2:int,y2:int):
        
        header = round(y1+(y2 * 0.08))
        imageHelper.DrawDots(draw,x1,y1,x2,header,5)
        imageHelper.DrawDottedHorizontalLine(draw,x1,header,x2,4)

        