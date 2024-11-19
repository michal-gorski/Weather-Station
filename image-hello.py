#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

from PIL import Image,ImageDraw,ImageFont

import logging
import time

logging.basicConfig(level=logging.DEBUG)

try:
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Roboto-Medium.ttf')
    font24 = ImageFont.truetype(path, 30)
    #font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    #font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)


    # Drawing on the Horizontal image
    logging.info("Drawing on the Horizontal image...")
    Himage = Image.new('1', (800, 480),255)  # 255: clear the frame
    
    draw = ImageDraw.Draw(Himage)
    draw.rectangle(xy = (50, 50, 150, 150), 
               fill = 255, 
               outline = 0, 
               width = 5) 
    
    draw.circle(xy = (50, 50, 150, 150),  
            fill = 255, 
            outline = 0,
            radius = 50, 
            width = 5) 
    
    draw.text(xy=(25, 160), 
          text="Hello, Geeks!", 
          font=font24, 
          fill=0) 
    
    ratio = 800/480
    for x in range(0,Himage.size[1],3):        
        draw.line((0, x, Himage.size[0]-(x*ratio), Himage.size[1]), fill=0)   

    for x in range(0,Himage.size[0],5):        
        draw.line((x, 0, Himage.size[0], Himage.size[1]-(x*ratio)), fill=0)   

    Himage.show()
    
    draw.text((10, 0), 'hello world', font = font24, fill = 0)
    draw.text((10, 20), '7.5inch e-Paper', font = font24, fill = 0)
    draw.text((150, 0), u'微雪电子', font = font24, fill = 0)
    draw.line((20, 50, 70, 100), fill = 0)
    draw.line((70, 50, 20, 100), fill = 0)
    draw.rectangle((20, 50, 70, 100), outline = 0)
    draw.line((165, 50, 165, 100), fill = 0)
    draw.line((140, 75, 190, 75), fill = 0)
    draw.arc((140, 50, 190, 100), 0, 360, fill = 0)
    draw.rectangle((80, 50, 130, 100), fill = 0)
    draw.chord((200, 50, 250, 100), 0, 360, fill = 0)
    
    Himage.save('image.png')

    # '''4Gray display'''
    # # The feature will only be available on screens sold after 24/10/23
    # logging.info("4Gray display--------------------------------")
    # epd.init_4Gray()
    
    # Limage = Image.new('L', (epd.width, epd.height), 0)  # 255: clear the frame
    # draw = ImageDraw.Draw(Limage)
    # draw.text((20, 0), u'微雪电子', font = font35, fill = epd.GRAY1)
    # draw.text((20, 35), u'微雪电子', font = font35, fill = epd.GRAY2)
    # draw.text((20, 70), u'微雪电子', font = font35, fill = epd.GRAY3)
    # draw.text((40, 110), 'hello world', font = font18, fill = epd.GRAY1)
    # draw.line((10, 140, 60, 190), fill = epd.GRAY1)
    # draw.line((60, 140, 10, 190), fill = epd.GRAY1)
    # draw.rectangle((10, 140, 60, 190), outline = epd.GRAY1)
    # draw.line((95, 140, 95, 190), fill = epd.GRAY1)
    # draw.line((70, 165, 120, 165), fill = epd.GRAY1)
    # draw.arc((70, 140, 120, 190), 0, 360, fill = epd.GRAY1)
    # draw.rectangle((10, 200, 60, 250), fill = epd.GRAY1)
    # draw.chord((70, 200, 120, 250), 0, 360, fill = epd.GRAY1)
    # epd.display_4Gray(epd.getbuffer_4Gray(Limage))
    # time.sleep(2)
    

       
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    exit()
