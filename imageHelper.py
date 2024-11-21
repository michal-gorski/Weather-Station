from PIL import Image,ImageDraw,ImageFont
def DrawDottedHorizontalLine(draw:ImageDraw.ImageDraw,x1:int,y:int,x2:int,step:int):
    for x in range(x1,x2,step):
        draw.line((x, y, round(x+step/2), y), fill = 0)

def DrawDottedVerticalLine(draw:ImageDraw.ImageDraw,x:int,y1:int,y2:int,step:int):
    for y in range(y1,y2,step):
        draw.line((x, y, x, round(y+step/2)), fill = 0)

def DrawDots(draw:ImageDraw.ImageDraw,x1,y1,x2,y2,step):
    for x in range(x1,x2,step):
        for y in range (y1,y2,step):
            draw.point((x,y),fill = 0)

def WrappedText(text: str, font: ImageFont.ImageFont, line_length: int):
        lines = ['']
        for word in text.split():
            line = f'{lines[-1]} {word}'.strip()
            if font.getlength(line) <= line_length:
                lines[-1] = line
            else:
                lines.append(word)
        return '\n  '.join(lines)