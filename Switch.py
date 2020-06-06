import RPi.GPIO as GPIO
import time
import logging
from display import Print
from Ocr import Main_ocr

logging.basicConfig(filename="cache/log/Switch.log", level=logging.INFO)

def listening():
    # 采用BCM引脚编号
    GPIO.setmode(GPIO.BCM)
    # 关闭警告
    GPIO.setwarnings(False)
    # 输入引脚
    channel = 18
    # 设置GPIO输入模式, 使用GPIO内置的上拉电阻, 即开关断开情况下输入为HIGH
    GPIO.setup(channel, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    # 检测HIGH -> LOW的变化
    GPIO.add_event_detect(channel, GPIO.FALLING, bouncetime = 200)
    num=0
    try:
        while True:
            # 如果检测到电平FALLING, 说明开关闭合
            if GPIO.event_detected(channel):
                Main_ocr()
                Print()
                num+=1
                logging.info(f'succeed_gpio_start:00{num}')
                print(f'succeed_gpio_start:00{num}')
            # 可以在循环中做其他检测
            time.sleep(0.5)     # 500毫秒的检测间隔
    except Exception as e:
        print(e)
if __name__ == '__main__':
    listening()

GPIO.cleanup()