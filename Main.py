from vtt import Main_vtt
from display import Print
from Ocr import Main_ocr
from Switch import listening

import RPi.GPIO as GPIO
import time
import logging
from multiprocessing import Process,active_children

logging.basicConfig(filename="cache/log/Main.log", level=logging.INFO)


if __name__ == '__main__':
    vtt_pro = Process(target = Main_vtt)
    gpio_pro= Process(target = listening)
    gpio_pro.start()
    vtt_pro.start()   # 启动进程
    vtt_pro.join()