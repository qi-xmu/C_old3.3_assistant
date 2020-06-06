from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106

import logging

import os
from PIL import ImageFont
from time import sleep
from multiprocessing import Process
import threading

logging.basicConfig(filename="cache/log/display.log", level=logging.INFO)

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)

#读取字体文件，转换成图片
def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)
#打印到屏幕上
def Print():
    print_text=""
    with open("cache/text","r") as f:
        lines =f.readlines()
        f.close()
    for line in lines:
        print_text += line.strip('\n')+' '
    font_size=48
    font = make_font("fzktjw.ttf", font_size)
    x=120
    count=1
    print('[',end='')
    speed=8    
    length = len(print_text)*font_size
    rest=(length+x)//speed//10
    while True:
        if count%rest==0:
            print("#",end='')
        with canvas(device) as draw:
            draw.text((x, 7), print_text, font=font, fill="white")
        x -= speed
        if x<-length :
            print(']')
            break
        count+=1
if __name__ == '__main__':
     Print()