import requests
import json
import base64
import os
import logging
import speech_recognition as sr
from display import Print
#启动日志文件
 #设置日志级别   INFO事件级别
logging.basicConfig(filename="cache/log/vtt.log", level=logging.INFO)

def get_token():
    logging.info('开始获取token')
    #获取token
    baidu_server = "https://openapi.baidu.com/oauth/2.0/token?"
    grant_type = "client_credentials"
    client_id = "up7sdaBHdk09sbMk1l6ijszx"
    client_secret = "XmoFEcE4i8ErqBbnuSlgWb2B81AKXard"
    #拼url
    url = f"{baidu_server}grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}"
    res = requests.post(url)
    token = json.loads(res.text)["access_token"]
    return token

def audio_baidu(filename):
    logging.info('开始识别')
    print('ok')
    with open(filename, "rb") as f:
        speech = base64.b64encode(f.read()).decode('utf-8')
        f.close()
    size = os.path.getsize(filename)
    token = get_token()
    headers = {'Content-Type': 'application/json'}
    url = "https://vop.baidu.com/server_api"
    data = {
        "format": "wav",
        "rate": "16000",
        "dev_pid": "1536",
        "speech": speech,
        "cuid": "TEDxPY",
        "len": size,
        "channel": 1,
        "token": token,
    }
    req = requests.post(url, json.dumps(data), headers)
    result = json.loads(req.text)
    if result["err_msg"] == "success.":
        with open("cache/text","w") as t:
            t.write(result['result'][0])
            logging.info(result)
            t.close()
        Print()
        print(result['result'][0])
        return result['result']
    else:
        return -1


def Main_vtt():
    wav_num = 0     #缓冲文件编号
    max_num = 30    #最大缓冲文件数量
    while True:
        #录音文件保存路径
        path_wav = f"cache/wav/cache{wav_num}.wav"

        r = sr.Recognizer()
        #启用麦克风
        mic = sr.Microphone()
        print("Ready")
        logging.info('录音中')
        with mic as source:
            #降噪
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        with open(path_wav, "wb") as f:
            #将麦克风录到的声音保存为wav文件
            f.write(audio.get_wav_data(convert_rate=16000))
            f.close()
        if audio_baidu(path_wav) == -1:
            logging.info('fail')
            print('内容识别失败，请重试')
        wav_num += 1
        if wav_num >= max_num :
            wav_num=0
if __name__ == '__main__':
    Main_vtt()