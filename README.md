# 随身Wifi 制作ChatGpt语音助手

![image-20230602201623896](https://s2.loli.net/2023/06/02/CRax1UwiukAtJY7.png)

## 0.效果展示



## 1.准备硬件材料

看下边地址:
https://jiuhuai.top/articke/chatgpt-suishenwifi-yinxiang0.html

## 2.准备第三方材料

### 1.申请百度语音识别api key

申请地址：https://developer.baidu.com/

### 2.申请open ai key

申请地址：https://openai.com/

### 3.申请picovoice语音唤醒词

申请地址：https://console.picovoice.ai/



## 3.系统环境准备

### 1.更新系统

```
sudo apt update
```

### 2.安装软件

#### 2.1安装PulseAudio

```
sudo apt-get install pulseaudio
```

使用以下命令启动PulseAudio

让 PulseAudio 守护进程在系统启动时自动启动，请执行以下步骤：

创建一个名为 pulseaudio.service 的文件，该文件应该位于 /etc/systemd/user/ 目录下。

```

sudo nano /etc/systemd/user/pulseaudio.service
```

在文件中输入以下内容：

```

[Unit]
Description=PulseAudio Daemon

[Service]
ExecStart=/usr/bin/pulseaudio --daemonize=no
Restart=on-failure

[Install]
WantedBy=default.target
```

保存并关闭文件。

启用并启动服务：

```
systemctl --user enable pulseaudio.service
systemctl --user start pulseaudio.service
```

现在，PulseAudio 守护进程将在系统启动时自动启动。

```
reboot
```

#### 2.2开启HUB模式

```
echo host > /sys/kernel/debug/usb/ci_hdrc.0/role
```

#### 2.3安装 `sox` 软件测试录音与播放功能

```python3
 sudo apt-get install sox
```

安装完成后运行 `sox -d -d` 命令，对着麦克风说话，确认可以听到自己的声音。

#### 2.4安装 python3 和pip 3

```
sudo apt install python3


sudo apt install python3-pip
```

## 3.克隆本项目,然后填写相关参数

### 3.1克隆项目

```
https://github.com/conlindd/zimou.git
```



### 3.2填写参数

```
# main方法 开始方法

# 参数填写
openai_api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # 你的openai key
PICOVOICE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # 你的picovoice key
keyword_path = './speechmodules/xxxxxxxxxxxx-pi_v2_2_0.ppn'  # 你的唤醒词检测离线文件地址(选树莓派)
Baidu_APP_ID = 'xxxxxx'  # 你的百度APP_ID
Baidu_API_KEY = 'xxxxxxxx'  # 你的百度API_KEY
Baidu_SECRET_KEY = 'xxxxxxxxxxxxxxxxx'  # 你的百度SECRET_KEY

```

## 4.启动项目

### 4.1在项目根目录使用pip安装requirements.txt中的模块

```
pip install -r requirements.txt
```

### 4.2启动项目

```
python3 main.py
```



## 5.聊天展示

![image-20230602201132083](https://s2.loli.net/2023/06/02/lopYrSVc8tFEG1A.png)





原作者仓库:https://github.com/MedalCollector/Orator