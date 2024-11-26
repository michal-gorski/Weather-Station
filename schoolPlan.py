import json
import sys
import os
import requests
import urllib3

from PIL import Image,ImageDraw,ImageFont
import imageHelper
import myLogger


class SchoolPlan:
    planData = ''
    dayOfWeek = 0
    currentPlan = ''
    tests = ''

    def __init__(self) -> None:
        myLogger.Log("Getting plan data")
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(
            "https://michal-gorski.github.io/Weather-Station/plan.json", verify=False
        )
        self.planData = response.json()    
        self.tests = self.planData["sprawdziany"]

    def CurrentPlan(self):
        import datetime        
        dayOfWeek = datetime.datetime.today().weekday()
        time = datetime.datetime.now().hour
        
        if time > 12:
            dayOfWeek += 1

        if dayOfWeek >= 6:
            dayOfWeek = 0
        
        self.dayOfWeek = dayOfWeek
        myLogger.Log("Getting plan for current day: " + str(dayOfWeek))

        self.currentPlan = self.PlanForDay(dayOfWeek)
        return self.currentPlan

    def PlanForDay(self,day):
        if (day < 0 or day > 4):
            return self.planData['0']
        else:
            return self.planData[str(day)]

    def PrintPlan(self):    
        print(self.WordDay(),': ',self.currentPlan)
        for test in self.tests:
            print(test)

    def WordDay(self):
        if self.dayOfWeek == 0: return "poniedziałek"
        elif self.dayOfWeek == 1: return "wtorek"
        elif self.dayOfWeek == 2: return "środa"
        elif self.dayOfWeek == 3: return "czwartek"
        elif self.dayOfWeek == 4: return "piątek"
        elif self.dayOfWeek > 4: return "poniedziałek"
        else: return ''

    def DrawPlan(self,draw:ImageDraw.ImageDraw,fonts,x1:int,y1:int,x2:int,y2:int):
        
        header = round(y1+(y2 * 0.06))
        imageHelper.DrawDots(draw,x1,y1,x2,header,6)
        imageHelper.DrawDottedHorizontalLine(draw,x1,header,x2,4)

        draw.text((x1+15, round((y1+header)/2-9)), 'PLAN LEKCJI '+ self.WordDay().upper(), font = fonts["font16bold"], fill = 0)

        if self.currentPlan == '': self.CurrentPlan()
        
        position = 0
        lessonNumber = 0
        for lekcja in self.currentPlan:   
            planHour = self.planData["lekcje"][lessonNumber]    
            lessonNumber += 1    
            if lekcja != '':
                lessonPos = header + 8 + position * 30
                
                
                draw.text((x1+15, lessonPos-6), planHour, font = fonts["font14light"], fill = 0)
                draw.text((x1+60, lessonPos -6), lekcja, font = fonts["font14light"], fill = 0)
        
                imageHelper.DrawDottedHorizontalLine(draw,x1,lessonPos + 15,x2,4)
                position += 1
                
        #header 2 = y position of bottom line of SPRAWDZIANY header
        header2 = lessonPos + 15 + header - y1
        imageHelper.DrawDottedHorizontalLine(draw,x1,header2,x2,4)
        imageHelper.DrawDots(draw,x1,lessonPos + 15,x2,header2,6)
        draw.text((x1+15, header2 - 24), 'SPRAWDZIANY', font = fonts["font16bold"], fill = 0)

        position = 0
        for test in self.tests:            
            #many tests and lessons print just subject
            if len(self.tests)+len(self.currentPlan) > 9:
                testPos = header2 + position * 25
                
                imageHelper.DrawDottedHorizontalLine(draw,x1,testPos + 25,x2,4)     
                draw.text((x1+15, testPos + 4), test['data'], font = fonts["font14light"], fill = 0)
                draw.text((x1+60, testPos + 4), test["przedmiot"], font = fonts["font14light"], fill = 0)
                
                position += 1
            #less tests print topic as well
            else:
                testPos = header2 + position * 35
                
                imageHelper.DrawDottedHorizontalLine(draw,x1,testPos + 35,x2,4)     
                draw.text((x1+4, testPos + 6), test['data'], font = fonts["font14light"], fill = 0)
                draw.text((x1+60, testPos + 4), test["przedmiot"], font = fonts["font14light"], fill = 0)
                draw.text((x1+15, testPos + 19), test["zakres"], font = fonts["font14light"], fill = 0)
                
                
                position += 1
               

        