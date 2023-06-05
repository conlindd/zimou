# main方法 开始方法
import speech_recognition

from speechmodules.wakeword import PicoWakeWord
from speechmodules.speech2text import BaiduASR, OpenaiASR
# from speechmodules.speech2text import BaiduASR, AzureASR, OpenaiASR
from speechmodules.text2speech import BaiduTTS
# from speechmodules.text2speech import BaiduTTS, Pyttsx3TTS, AzureTTS, EdgeTTS
from chatmodules.openai_chat_module import OpenaiChatModule
# from chatmodules.openai_agent_module import OpenaiAgentModule
# import asyncio
import struct
import os
from speechmodules.music import MusicPlayer



# 参数填写
# os.environ["SERPER_API_KEY"] = ""  # 你的serper key
openai_api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # 你的openai key
PICOVOICE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # 你的picovoice key
keyword_path = './speechmodules/xxxxxxxxxxxx-pi_v2_2_0.ppn'  # 你的唤醒词检测离线文件地址(选树莓派)

#中文模型地址 porcupine_params_zh.pv下载地址 :https://github.com/Picovoice/porcupine/tree/master/lib/common
# model_path = './speechmodules/porcupine_params_zh.pv'  #如果你用中文唤醒词,把这个注释打开
Baidu_APP_ID = 'xxxxxx'  # 你的百度APP_ID
Baidu_API_KEY = 'xxxxxxxx'  # 你的百度API_KEY
Baidu_SECRET_KEY = 'xxxxxxxxxxxxxxxxx'  # 你的百度SECRET_KEY
# AZURE_API_KEY = ""  # 你的azure key
# AZURE_REGION = ""  # 你的azure region


import speech_recognition as sr





def run(picowakeword, asr, tts, openai_chat_module):
    print("请说 'hi xxxx'!")

    # 提示音
    player = MusicPlayer()
    player.play("resources/ding.wav")
    # player.quit()

    while True:  # 需要始终保持对唤醒词的监听
        audio_obj = picowakeword.stream.read(picowakeword.porcupine.frame_length, exception_on_overflow=False)
        audio_obj_unpacked = struct.unpack_from("h" * picowakeword.porcupine.frame_length, audio_obj)
        keyword_idx = picowakeword.porcupine.process(audio_obj_unpacked)
        if keyword_idx >= 0:
            picowakeword.porcupine.delete()
            picowakeword.stream.close()
            picowakeword.myaudio.terminate()  # 需要对取消对麦克风的占用!

            print("嗯,我在,请讲！")
            tts.text_to_speech_and_play("嗯,我在,请讲！")

            # 提示音
            player = MusicPlayer()
            player.play("resources/ding.wav")
            # player.quit()

            # asyncio.run(tts.text_to_speech_and_play("嗯,我在,请讲！"))  # 如果用Edgetts需要使用异步执行
            while True:
                try:
                    q = asr.speech_to_text()
                    print(f'recognize_from_microphone, text={q}')
                    res = openai_chat_module.chat_with_origin_model(q)
                    # res = openai_chat_module.chat_with_agent(q)
                    if res is None:
                        print("抱歉，我没有听清楚，请再说一遍。")
                    else:
                        print(res)
                        tts.text_to_speech_and_play('嗯' + res)
                        # 检查是否成功播放
                        if not tts.playback_successful:
                            print("无法播放回答，请检查播放设备设置和参数。")
                except speech_recognition.WaitTimeoutError:
                    print("等待超时，请再说一遍。")
                    continue
                # asyncio.run(tts.text_to_speech_and_play('嗯'+res))  # 如果用Edgetts需要使用异步执行
                # 提示音
                player = MusicPlayer()
                player.play("resources/ding.wav")
                # player.quit()


def Orator():
    picowakeword = PicoWakeWord(PICOVOICE_API_KEY, keyword_path)
    # picowakeword = PicoWakeWord(PICOVOICE_API_KEY, keyword_path,model_path) #如果你用中文唤醒词,把这个注释打开,上边的注释
    # 使用百度的语音识别
    asr=BaiduASR(Baidu_APP_ID,Baidu_API_KEY,Baidu_SECRET_KEY)
    tts=BaiduTTS(Baidu_APP_ID,Baidu_API_KEY,Baidu_SECRET_KEY)
    # asr = AzureASR(AZURE_API_KEY, AZURE_REGION)
    # tts = AzureTTS(AZURE_API_KEY, AZURE_REGION)
    # asr = OpenaiASR(openai_api_key)
    # tts = EdgeTTS()
    openai_chat_module = OpenaiChatModule(openai_api_key)
    # openai_chat_module = OpenaiAgentModule(openai_api_key)
    try:
        run(picowakeword, asr, tts, openai_chat_module)
    #     异常
    except KeyboardInterrupt:
        if picowakeword.porcupine is not None:
            picowakeword.porcupine.delete()
            print("Deleting porc")
        if picowakeword.stream is not None:
            picowakeword.stream.close()
            print("Closing stream")
        if picowakeword.myaudio is not None:
            picowakeword.myaudio.terminate()
            print("Terminating pa")
            exit(0)
    finally:
        # 本轮对话结束
        print('本轮对话结束')
        tts.text_to_speech_and_play('嗯' + '主人，我退下啦！')
        # asyncio.run(tts.text_to_speech_and_play('嗯'+'主人，我退下啦！'))  # 如果用Edgetts需要使用异步执行
        if picowakeword.porcupine is not None:
            picowakeword.porcupine.delete()
            print("Deleting porc")
        if picowakeword.stream is not None:
            picowakeword.stream.close()
            print("Closing stream")
        if picowakeword.myaudio is not None:
            picowakeword.myaudio.terminate()
            print("Terminating pa")
        # 嵌套调用 调用自己
        Orator()

if __name__ == '__main__':
    p = pyaudio.PyAudio()

# 设置采样率为 16000 Hz
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
    Orator()
