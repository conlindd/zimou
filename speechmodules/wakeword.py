# 唤醒词管理模块

import struct
import pvporcupine
# 导入 pvporcupine模块
# 导入pyaudio模块 使用电脑麦克风
import pyaudio

class PicoWakeWord:
    # model_path=None 表示不配置唤醒词的语言
    # def __init__(self, PICOVOICE_API_KEY, keyword_path, model_path):
    def __init__(self, PICOVOICE_API_KEY, keyword_path, model_path=None):
        self.PICOVOICE_API_KEY = PICOVOICE_API_KEY
        self.keyword_path = keyword_path
        self.model_path = model_path
        self.porcupine = pvporcupine.create(
            # 设置key值
            access_key=self.PICOVOICE_API_KEY,
            # 配置唤醒关键词文件
            keyword_paths=[self.keyword_path],
            # 中文关键词的配置文件
            # model_path=self.model_path
        )
        self.myaudio = pyaudio.PyAudio()
        self.stream = self.myaudio.open(
#            input_device_index=0,
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )

    def detect_wake_word(self):
        audio_obj = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
        audio_obj_unpacked = struct.unpack_from("h" * self.porcupine.frame_length, audio_obj)
        keyword_idx = self.porcupine.process(audio_obj_unpacked)
        return keyword_idx


# # 循环  测试
# while True:
#     # 创建对象
#     audio_obj = stream.read(procupine.frame_length, exception_on_overflow=False)
#     audio_obj_unpacked = struct.unpack_from("h" * procupine.frame_length, audio_obj)
#
#     # 监听唤醒词
#     # 当监测到唤醒词就会返回一个keyword_idx
#     keyword_idx = procupine.process(audio_obj_unpacked)
#
#     #测试 当听到唤醒词时 keyword_idx >=0  会返回  然后输出我听到了
#     if keyword_idx >=0:
#         print("我听到了!")
# if __name__ == '__main__':
#     picowakeword = PicoWakeWord(PICOVOICE_API_KEY, keyword_path)
#     while True:
#         audio_obj = picowakeword.stream.read(picowakeword.porcupine.frame_length, exception_on_overflow=False)
#         audio_obj_unpacked = struct.unpack_from("h" * picowakeword.porcupine.frame_length, audio_obj)
#         # 监听唤醒词
#         # 当监测到唤醒词就会返回一个keyword_idx
#         keyword_idx = picowakeword.porcupine.process(audio_obj_unpacked)
#
#         #     #测试 当听到唤醒词时 keyword_idx >=0  会返回  然后输出我听到了
#         if keyword_idx >= 0:
#             print("我听到了！")


