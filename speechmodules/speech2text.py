# # AipSpeech是百度AI平台提供的语音识别API
from aip import AipSpeech
# # 导入百度api
# pip install baidu-api
# # SpeechRecognition库是一个开源的Python语音识别库
import speech_recognition as sr
import requests
# 微软的语音识别库
# pip install azure-cognitiveservices-speech
# import azure.cognitiveservices.speech as speechsdk

# ################方法一:使用百度语音识别模块################
class BaiduASR:
    def __init__(self, APP_ID, API_KEY, SECRET_KEY):
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        self.r = sr.Recognizer()
    # 从麦克风收集音频并写入文件,最大频率16000
    def _record(self, if_cmu: bool = False, rate=16000):
        with sr.Microphone(sample_rate=rate) as source:
            # 校准环境噪声水平的energy threshold
            # r.adjust_for_ambient_noise(source,duration=1)
            print("您现在可以说话了")
            # 设置监听信息  监听时间是20秒 超过后边的就不录入了
            audio= self.r.listen(source,timeout=20,phrase_time_limit=4)

        # 设置录音文件保存位置和名字
        file_name="resources/speech.wav"
        with open(file_name,"wb")as f:
            f.write(audio.get_wav_data())

        if if_cmu:
            return audio
        else:
            # return self._get_file_content(file_name)
            return self._get_file_content(file_name)


    # # 从本地文件中加载音频  作为后续百度语音服务的输入
    # def _get_file_content(file_name):
    #     with open(file_name,'rb') as f:
    #         audio_data=f.read()
    #     return audio_data

    # 从本地文件中加载音频  作为后续百度语音服务的输入
    def _get_file_content(self, file_name):
        with open(file_name, 'rb') as f:
            audio_data = f.read()
        return audio_data


    def speech_to_text(self, audio_path: str = "test.wav", if_microphone: bool = True):
        # 麦克风输入  采集频率必须是八的倍数 这里使用16000和上面保持一致
        if if_microphone:
            audio=self._record()
            result = self.client.asr(audio, 'wav', 16000, {
                'dev_pid':1537  #识别中文普通话
            })
        #从文件中获取
        # result是云识别之后返回的结果
        else:
            result = self.client.asr(self._get_file_content(audio_path), 'wav', 16000, {
                'dev_pid':1537  #识别中文普通话
            })

        # 判断语音识别的返回数据中是否有err_msg自动,如果有输出识别识别
        if result["err_msg"]!="success.":
            return "语音识别识别:"+result(["err_msg"])
        else:
            # 如果识别成功则获取返回的识别的语音转文字信息
            return result['result'][0]


# # ################方法二:使用的微软的语音识别################
# class AzureASR:
#     def __init__(self, AZURE_API_KEY, AZURE_REGION):
#         self.AZURE_API_KEY = AZURE_API_KEY
#         self.AZURE_REGION = AZURE_REGION
#         self.speech_config = speechsdk.SpeechConfig(subscription=AZURE_API_KEY, region=AZURE_REGION)
#
#     def speech_to_text(self, audio_path: str = "test.wav", if_microphone: bool = True):
#         # 指定识别的声音是中文
#         self.speech_config.speech_recognition_language = "zh-CN"
#         audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
#         speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)
#         print("Speak into your microphone.")
#         speech_recognition_result = speech_recognizer.recognize_once_async().get()
#
#         if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
#             print("Recognized:{}".format(speech_recognition_result.text))
#             # 如果识别成功就从这里返回识别出来的文本
#             return speech_recognition_result.text
#         # 以下这些是识别错误的返回
#         elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
#             print("No speech could be recognized :{}".format(speech_recognition_result.no_match_details))
#         elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
#             cancellation_details = speech_recognition_result.cancellation_details
#             print("Speech Recognition canceled:{}".format(cancellation_details.reason))
#             if cancellation_details.reason == speechsdk.CancellationReason.Error:
#                 print("Error details:{}".format(cancellation_details.error_details))
#                 print("Did you set the speech resource key and region values?")
#         # return None

# openAi的合成
class OpenaiASR:
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY
        self.r = sr.Recognizer()

    # 从麦克风收集音频并写入文件
    def _record(self, if_cmu: bool = False, rate=16000):
        with sr.Microphone(sample_rate=rate) as source:
            print('您可以开始说话了')
            audio = self.r.listen(source, timeout=20, phrase_time_limit=5)

        file_name = "./resources/speech.wav"
        with open(file_name, "wb") as f:
            f.write(audio.get_wav_data())

        if if_cmu:
            return audio
        else:
            return self._get_file_content(file_name)

    # 从本地文件中加载音频 作为后续百度语音服务的输入
    def _get_file_content(self, file_name):
        with open(file_name, 'rb') as f:
            audio_data = f.read()
        return audio_data

    def _get_speech_text(self, audio_file):
        print('调用用语音识别')
        url = 'https://api.openai.com/v1/audio/transcriptions'
        headers = {
            'Authorization': 'Bearer ' + self.API_KEY
        }
        files = {
            'file': ('./resources/speech.wav', audio_file),
        }
        data = {
            'model': 'whisper-1',
        }
        response = requests.post(url, headers=headers, data=data, files=files)
        result = response.json()['text']
        # print(result)
        return result

    def speech_to_text(self, audio_path: str = "test.wav", if_microphone: bool = True):
        if if_microphone:
            result = self._get_speech_text(self._record())
        else:
            result = self._get_speech_text(audio_path)
        return result

# 测试使用语言识别
# if __name__ == '__main__':
#     # APP_ID = ''
#     # API_KEY = ''
#     # SECRET_KEY = ''
#     # baiduasr = BaiduASR(APP_ID, API_KEY, SECRET_KEY)
#     # result = baiduasr.speech_to_text()
#     # print(result)
#     # AZURE_API_KEY = ""
#     # AZURE_REGION = ""
#     # azureasr = AzureASR(AZURE_API_KEY, AZURE_REGION)
#     # azureasr.speech_to_text()
#     openai_api_key = ""
#     openaiasr = OpenaiASR(openai_api_key)
#     print(openaiasr.speech_to_text())
