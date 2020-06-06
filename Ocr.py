import os
from aip import AipOcr
from picamera import PiCamera
from time import sleep
from tts import AipSpeech
from multiprocessing import Process
import logging

logging.basicConfig(filename="cache/log/ocr.log", level=logging.INFO)
"""百度云ocr"""
APP_ID = '20028694'
API_KEY = 'ejXo1yDopLNyj3KfAkxSeXHr'
SECRET_KEY = 'eQD6aDdXUOVGBkR1RalVna22QiarfPx3'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

imgpath = 'cache/img.png'
logging.info('start...')

def Main_ocr():
    """拍照"""
    def Shutter():
        file = "src/iphoneshutter.mp3"
        os.system("mpg123 " + file)
    def Camera():
        camera = PiCamera() 
        #图片的文件路径
        camera.capture(imgpath)
    #多进程
    shutter = Process(target=Shutter)
    takephoto = Process(target=Camera)
    #进程管理
    takephoto.start()
    shutter.start()
    #结束进程
    takephoto.join()
    shutter.join()

    ocr_text=''

    #获取图片
    def get_file_content(filePath):
        with open(filePath, 'rb') as f:
            return f.read()

    image = get_file_content(imgpath)

    #处理参数
    options = {}
    options["language_type"] = "CHN_ENG"#识别语言类型，默认为CHN_ENG。CHN_ENG：中英文混合；- ENG：英文；- POR：葡萄牙语；- FRE：法语；- GER：德语；- ITA：意大利语；- SPA：西班牙语；- RUS：俄语；- JAP：日语；- KOR：韩语；
    options["detect_direction"] = "true"#是否检测图像朝向
    options["detect_language"] = "true" #是否检测语言
    options["probability"] = "false"    #是否返回识别结果中每一行的置信度
    #获得返回信息
    message = client.basicGeneral(image, options)
    for item in message.get('words_result','None'):
        ocr_text +=item['words']+'\n'

    logging.info(ocr_text)

    #写入文件
    with open("cache/text", 'w+') as p:
        p.write(ocr_text)
        p.close()

if __name__ =='__main__':
    Main_ocr()