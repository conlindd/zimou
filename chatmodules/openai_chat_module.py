# 调用open ai的接口

# pip install openai
import openai
# 调用
class OpenaiChatModule:
    # 传入open ai的key
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        #  openai 的代理服务器地址 可以直接访问的通
        openai.api_base = "https://api.openai-proxy.com/v1"
        # 将chatGpt的聊天记录保存到列表变量中,形成记忆上下文关联
        self.origin_model_conversation = [
                                # 初始值,给chatGpt一个身份的设定
                                {"role": "system", "content": "你是用户沐沐的好朋友，能够和沐沐进行愉快的交谈，你的名字叫兹哞."}
                            ]
    # 调用chatGpt原生接口调用
    def chat_with_origin_model(self, text):
        # 使用key
        openai.api_key = self.openai_api_key
        #   去除符号
        text = text.replace('\n', ' ').replace('\r', '').strip()
        # 如果传入的参数为0  则不向下进行
        if len(text) == 0:
            return
        print(f'chatGPT Q:{text}')
        self.origin_model_conversation.append({"role": "user", "content": text})
        # 使用的接口 openai.ChatCompletion  具备记忆功能
        response = openai.ChatCompletion.create(
            # 使用的模型 gpt3.5
            model="gpt-3.5-turbo",
            # model="gpt-4",
            # 传入历史聊天信息
            messages=self.origin_model_conversation,
            # 生成的回答的数量
            max_tokens=2048,
            # 回答的创造性
            temperature=0.3,
        )
        # 将新的回复加入到聊天历史列表,用于同时返回给chatgpt
        reply = response.choices[0].message.content
        self.origin_model_conversation.append({"role": "assistant", "content": reply})
        return reply



# if __name__ == '__main__':
#     openaichatmodule = OpenaiChatModule(openai_api_key)
#     print(openaichatmodule.chat_with_origin_model('你好，你叫什么?'))
#     print(openaichatmodule.chat_with_origin_model('天空为什么是蓝色的?'))