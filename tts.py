from tts import AipSpeech
from display import Print
import os
import threading

"""百度云tts"""
APP_ID='19984793'
API_KEY="yht42i6F0m0CD3ijxiAOHBnC"
SECRET_KEY="nlffHWSTkj1E5Eok3HZAMKj8EtxudoAR"

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

SPEAKER=0   # 发音人选择, 0为普通女声，1为普通男生，3为情感合成-度逍遥，4为情感合成-度丫丫
SPEED=2     # Speed, 0 ~ 15; 语速，取值0-15
PITCH=4     # Pitch, 0 ~ 15; 音调，取值0-15
VOLUME=15   # Volume, 0 ~ 15; 音量，取值0-15

def get_file_content(filePath):
        with open(filePath, 'rb') as f:
            return f.read()
text=get_file_content('cache/text')
#生成文件路径
file_name = 'cache/tts/tts_sound.mp3'
#获得返回信息
def tts(tts_text):
    tts_sound = client.synthesis(tts_text, 'zh', 1, {'per': SPEAKER, 'spd': SPEED, 'pit': PITCH, 'vol': VOLUME, })
   
    #写入返回文件
    if not isinstance(tts_sound, dict):
        print("文件名：" + file_name)
        with open(file_name, 'wb') as fp:
            fp.write(tts_sound)
            fp.close()

def Sound():
    os.system("mpg123 " + file_name)

s1 = threading.Thread(target=Sound)
p1 = threading.Thread(target=Print)
p1.start()
s1.start()

if __name__=='__main__':
    tts(text)