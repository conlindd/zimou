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
import pyaudio
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
                q = asr.speech_to_text()
                print(f'recognize_from_microphone, text={q}')
                res = openai_chat_module.chat_with_origin_model(q)
                print(res)
                tts.text_to_speech_and_play('嗯' + res)

                # 提示音
                player = MusicPlayer()
                player.play("resources/ding.wav")
                # player.quit()

                # asyncio.run(tts.text_to_speech_and_play('嗯'+res))  # 如果用Edgetts需要使用异步执行
                # try:
                #     q = asr.speech_to_text()
                #     print(f'recognize_from_microphone, text={q}')
                #     res = openai_chat_module.chat_with_origin_model(q)
                #     # res = openai_chat_module.chat_with_agent(q)
                #     if res is None:
                #         print("抱歉，我没有听清楚，请再说一遍。")

                #         # 提示音
                #         #player = MusicPlayer()
                #         #player.play("resources/ding.wav")
                #         # player.quit()

                #     else:
                #         print(res)
                #         tts.text_to_speech_and_play('嗯' + res)

                #         # 提示音
                #         #player = MusicPlayer()
                #         #player.play("resources/ding.wav")
                #         # player.quit()

                #         # 检查是否成功播放
                #         if not tts.playback_successful:
                #             print("无法播放回答，请检查播放设备设置和参数。")
                # except speech_recognition.WaitTimeoutError:
                #     print("等待超时，请再说一遍。")
                #     continue
                # # asyncio.run(tts.text_to_speech_and_play('嗯'+res))  # 如果用Edgetts需要使用异步执行
                # # 提示音
                # player = MusicPlayer()
                # player.play("resources/ding.wav")
                # # player.quit()


# 接收所有模块的变量
# def run(picowakeword, asr, tts, openai_chat_module):
#     print("请说 '嘿 兹哞'!")
#     # 死循环  听到唤醒词就执行
#     while True:  # 需要始终保持对唤醒词的监听
#         try:
#             audio_obj = picowakeword.stream.read(picowakeword.porcupine.frame_length, exception_on_overflow=False)
#         except Exception as e:
#             print(f"读取音频流时出现异常：{e}")
#             break
#         audio_obj_unpacked = struct.unpack_from("h" * picowakeword.porcupine.frame_length, audio_obj)
#         # 识别到唤醒词就返回>=0的符号
#         keyword_idx = picowakeword.porcupine.process(audio_obj_unpacked)
#         if keyword_idx >= 0:
#             # 唤醒
#             # 取消对麦克风占用 然后在以后用户就能使用麦克风
#             picowakeword.stream.close() #先关闭音频流
#             picowakeword.myaudio.terminate()  # 需要对取消对麦克风的占用! 关闭音频对象
#             picowakeword.porcupine.delete()
#
#             print(" 嗯,我在,请讲！")
#             tts.text_to_speech_and_play("嗯,我在,请讲！")
#             # asyncio.run(tts.text_to_speech_and_play("嗯,我在,请讲！"))  # 如果用Edgetts需要使用异步执行
#             while True:  # 进入一次对话session
#                 picowakeword.stream.close()
#                 picowakeword.myaudio.terminate()
#                 try:
#                     # 获取识别到的文本
#                     q = asr.speech_to_text()
#                     print(f'recognize_from_microphone, text={q}')
#                     print("用户输入的:"+q)
#
#                     # 加上退出条件,避免死循环
#                     print(f"当前输入文本：{q}，退出条件：退下吧 or 退出")
#                     if "退出" in q or "退出。" in q or "退下吧" in q or "退下吧。" in q:
#                         print("退出当前对话，等待唤醒词...")
#                         tts.text_to_speech_and_play("好的，退出当前对话，等待唤醒词...")
#                         picowakeword.stream.close()
#                         picowakeword.myaudio.terminate()
#                         picowakeword.porcupine.delete()
#                         break
#
#                     res = openai_chat_module.chat_with_origin_model(q)
#                     # 调用open ai 对文本进行回答 并返回
#                     # res = openai_chat_module.chat_with_agent(q)
#
#                     if res is None:
#                         print("抱歉，我没有听清楚，请再说一遍。")
#                         tts.text_to_speech_and_play("抱歉，我没有听清楚，请再说一遍。")
#                         # asyncio.run(tts.text_to_speech_and_play("抱歉，我没有听清楚，请再说一遍。"))  # 如果用Edgetts需要使用异步执行
#                         continue
#                     print(res)
#                     # 将获取到的回答 用语音合成模块进行播放
#                     tts.text_to_speech_and_play('嗯' + res)
#                     # asyncio.run(tts.text_to_speech_and_play('嗯'+res))  # 如果用Edgetts需要使用异步执行
#                     # 检查是否成功播放
#                     if not tts.playback_successful:
#                         print("无法播放回答，请检查播放设备设置和参数。")
#
#                     picowakeword.porcupine.delete()
#                 except speech_recognition.WaitTimeoutError:
#                     print("没有听到任何声音，程序即将退出。")
#                     tts.text_to_speech_and_play("没有听到任何声音，程序即将退出。")
#                 except Exception as e:
#                     print(f"删除唤醒词检测对象时出现异常：{e}")
#                     break
#             print("请说 '嘿 兹哞'!")

def Orator():
    picowakeword = PicoWakeWord(PICOVOICE_API_KEY, keyword_path)
    # 使用百度的语音识别
    asr = BaiduASR(Baidu_APP_ID, Baidu_API_KEY, Baidu_SECRET_KEY)
    tts = BaiduTTS(Baidu_APP_ID, Baidu_API_KEY, Baidu_SECRET_KEY)
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
        # if picowakeword.porcupine is not None:
        #     picowakeword.porcupine.delete()
        #     print("Deleting porc")
        # if picowakeword.stream is not None:
        #     picowakeword.stream.close()
        #     print("Closing stream")
        # if picowakeword.myaudio is not None:
        #     picowakeword.myaudio.terminate()
        #     print("Terminating pa")
        # 嵌套调用 调用自己
        Orator()


if __name__ == '__main__':
    Orator()
