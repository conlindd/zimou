# 语音合成模块

# 感谢Linky小伙伴对于Windows版本运行说明以及代码的贡献!
# # 导入百度api
# pip install pygame
import pygame # 导入pygame，playsound报错或运行不稳定时直接使用
from aip import AipSpeech
# import pyttsx3

# 百度ai识别的api应用信息
from playsound import playsound

# 导入微软的语音合成库
# pip install azure-cognitiveservices-speech
# import azure.cognitiveservices.speech as speechsdk

# edge的语音合成
# from edge_tts import Communicate


# ################语音合成方法一:百度语音合成################
class BaiduTTS:
    def __init__(self, APP_ID, API_KEY, SECRET_KEY):
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        # 如果播放成功，设置状态为True，否则为False
        self.playback_successful = True  # 假设播放成功
    # # 一些配置
    # def baiduTTS(text=):
    #     # 合成中文
    #     result=client.synthesis(text,'zh',1),{
    #         'spd':4, #语速
    #         'vol':5, #音量大小
    #         'per':4 #发声人 百度丫丫
    #     } #得到音频的二进制文件
    #
    #     # 判定语音是否合成成功
    #     if not isinstance(result,dict):
    #         with open("resources/audio.mp3","wb") as f:
    #             f.write(result)
    #     else:
    #         print("语音合成失败",result)

    def text_to_speech_and_play(self, text=""):
        result = self.client.synthesis(text, 'zh', 1, {
            'spd': 5,  # 语速
            'vol': 5,  # 音量大小
            'per': 4  # 发声人 百度丫丫
        })  # 得到音频的二进制文件

        if not isinstance(result, dict):
            with open("resources/audio.mp3", "wb") as f:
                f.write(result)
        else:
            print("语音合成失败", result)
        # playsound('resources/audio.mp3')  # playsound无法运行时删去此行改用pygame，若正常运行择一即可
        self.play_audio_with_pygame('resources/audio.mp3')  # 注意pygame只能识别mp3格式

    def play_audio_with_pygame(self, audio_file_path):
        # 代码来自Linky的贡献
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()



# ################语音合成方法二:python库自带的语音合成################
# class Pyttsx3TTS:
#     # def __init__(self):
#     #     pass
#     def __init__(self):
#         self.engine = pyttsx3.init()  # 初始化 pyttsx3 模块
#         self.engine.setProperty('rate', 150)  # 设置语速，默认为 200
#
#     def text_to_speech_pyttsx3(self, text=""):
#         self.engine.say(text)
#         self.engine.runAndWait()

# ################语音合成方法三:使用微软的语音合成工具################
# 定义类
# class AzureTTS:
#     # 去微软他们的官网申请key
#     def __init__(self, AZURE_API_KEY, AZURE_REGION):
#         self.AZURE_API_KEY = AZURE_API_KEY
#         self.AZURE_REGION = AZURE_REGION
#         self.speech_config = speechsdk.SpeechConfig(subscription=AZURE_API_KEY, region=AZURE_REGION)
#         self.speech_config = speechsdk.SpeechConfig(subscription=AZURE_API_KEY, region=AZURE_REGION)
#         self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
#         # The language of the voice that speaks.
#         # 发音人小U
#         self.speech_config.speech_synthesis_voice_name = "zh-CN-XiaoyiNeural"
#         self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config,
#                                                               audio_config=self.audio_config)
#
#     # 定义函数 传入文字 合成声音
#     def text_to_speech_and_play(self, text):
#         # Get text from the console and synthesize to the default speaker.
#         speech_synthesis_result = self.speech_synthesizer.speak_text_async(text).get()
#
#         if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#             print("Speech synthesized for text [{}]".format(text))
#         elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
#             cancellation_details = speech_synthesis_result.cancellation_details
#             print("Speech synthesis canceled:{}".format(cancellation_details.reason))
#             if cancellation_details.reason == speechsdk.CancellationReason.Error:
#                 if cancellation_details.error_details:
#                     print("Error details :{}".format(cancellation_details.error_details))
#                     print("Didy you set the speech resource key and region values?")

# ################语音合成方法四:使用edge的语音合成工具################
# class EdgeTTS:
#     def __init__(self, voice: str = "zh-CN-XiaoyiNeural", rate: str = "+0%", volume: str = "+0%"):
#         self.voice = voice
#         self.rate = rate
#         self.volume = volume
#
#     async def text_to_speech_and_play(self, text):
#         # voices = await VoicesManager.create()
#         # voice = voices.find(Gender="Female", Language="zh")
#         # communicate = edge_tts.Communicate(text, random.choice(voice)["Name"])
#         communicate = Communicate(text, self.voice)
#         await communicate.save('resources/audio.mp3')
#         # playsound('./audio.wav') # playsound无法运行时删去此行改用pygame，若正常运行择一即可
#         self.play_audio_with_pygame('resources/audio.mp3')  # 注意pygame只能识别mp3格式
#
#
#     def play_audio_with_pygame(self, audio_file_path):
#         pygame.mixer.init()
#         pygame.mixer.music.load(audio_file_path)
#         pygame.mixer.music.play()
#         while pygame.mixer.music.get_busy():
#             pygame.time.Clock().tick(10)
#         pygame.mixer.quit()

#
# if __name__=='__main__':
#     # ################语音合成方法一: 使用百度语音合成################
#     APP_ID = "xxxxxxxx"
#     API_KEY = "xxxxxxxx"
#     SECRET_KEY = "xxxxxxxx"
#     baidutts=BaiduTTS(APP_ID,API_KEY,SECRET_KEY)
#     baidutts.text_to_speech_and_play('春天来了,每天的天气都很好!')

    # ################# 语音合成方法二:python库自带的语音合成################
    # pyttsx3=Pyttsx3TTS()
    # pyttsx3.text_to_speech_pyttsx3('这是pyttsx3的语音合成测试')

    # AZURE_API_KEY = ""
    # AZURE_REGION = ""
    # azuretts = AzureTTS(AZURE_API_KEY, AZURE_REGION)
    # azuretts.text_to_speech_and_play("嗯，你好，我是你的智能小伙伴，我的名字叫Murphy，你可以和我畅所欲言，我是很会聊天的哦！")
    # edgetts = EdgeTTS()
    # asyncio.run(edgetts.text_to_speech_and_play(
    #     "嗯，你好，我是你的智能小伙伴，我的名字叫Murphy，你可以和我畅所欲言，我是很会聊天的哦！"))


