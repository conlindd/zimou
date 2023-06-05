import pygame
# 回答前的提示音
class MusicPlayer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

    def play(self, file_path):
        try:
            pygame.mixer.music.load(file_path) # 加载音频文件
            pygame.mixer.music.play() # 播放音频
        except:
            print("无法播放音频文件！")

        while pygame.mixer.music.get_busy(): # 等待音频播放完毕
            pass

    def quit(self):
        pygame.quit()

# play_music("../resources/ding.wav")
# play_music("../resources/shuisheng.wav")
# play_music("../resources/xishuai.wav")
# play_music("../resources/niaojiao.wav")

# player = MusicPlayer()
# player.play("../resources/ding.wav")
# player.quit()