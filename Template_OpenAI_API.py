from openai import OpenAI

class GPTClient:
    def __init__(self,
                 api_key: str,
                 base_url: str,
                 model: str,
                 temperature: float = 0.5):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.temperature = temperature
        # 还需要模型的什么参数，自己加吧~

    def _build_messages(self, history: list, system_command: str, user_command: str) -> list:
        # 构造消息列表，先添加系统命令，再追加历史消息，最后添加当前用户命令
        messages = []
        if system_command:
            messages.append({"role": "system", "content": system_command})
        if history:
            messages.extend(history)
        if user_command:
            messages.append({"role": "user", "content": user_command})
        return messages

    def chat(self, history: list, system_command: str, user_command: str):
        # 非流式调用接口
        messages = self._build_messages(history, system_command, user_command)
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature
        )
        return completion.choices[0].message.content

    def chat_stream(self, history: list, system_command: str, user_command: str):
        # 流式调用接口
        messages = self._build_messages(history, system_command, user_command)
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            stream=True
        )
        # 使用 yield 逐块返回内容
        for chunk in stream:
            # 检查是否有 choices 数据
            if not hasattr(chunk, "choices") or not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            if hasattr(delta, "content") and delta.content:
                yield delta.content

if __name__ == '__main__':

    gpt_client = GPTClient(
        api_key=open("API_Chatanywhere.txt", "r", encoding="utf-8").read().strip(),
        base_url="https://api.chatanywhere.tech/v1",
        model="deepseek-v3",
        temperature=1
    )
    # 使用过程中，可以修改模型的参数
    gpt_client.model = "gpt-4o"
    gpt_client.temperature = 0.8

    # 非流式调用，单条指令
    history = []
    system_command = "回答内容在20个字到25个字之间"     # 系统级命令
    user_command = "你是什么大模型"              # 用户问题
    ans = gpt_client.chat([], system_command, user_command)
    print(ans)
    print("-" * 50)

    # 非流式调用，多条指令
    history.append({"role": "user", "content": user_command})
    history.append({"role": "assistant", "content": ans})
    user_command = "我刚刚问你什么问题？"
    ans = gpt_client.chat(history, system_command, user_command)
    print(ans)
    print("-" * 50)

    # 流式调用，单条指令
    system_command = "回答内容在30个字到35个字之间"  # 系统级命令
    user_command = "你模型训练的截止时间是什么时候"  # 用户问题
    ans = gpt_client.chat_stream(history, system_command, user_command)
    for content in ans:
        print(content, end="")
    print('\n'+"-" * 50)

    # 流式调用，多条指令
    history.append({"role": "user", "content": user_command})
    history.append({"role": "assistant", "content": ans})
    user_command = "我第2次问你什么问题，原话是什么？"
    ans = gpt_client.chat_stream(history, system_command, user_command)
    for content in ans:
        print(content, end="")
    print('\n'+"-" * 50)
