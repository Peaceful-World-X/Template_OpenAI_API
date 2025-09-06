# 作者：耗不尽的先生 Peaceful-World-X

import base64
import logging
import os
from typing import Dict, List, Union
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionMessageParam,           # 通用聊天消息类型，是用户/系统/助手消息的联合类型，用于类型标注
    ChatCompletionUserMessageParam,       # 表示用户发送的消息，role="user"，含 content 字段
    ChatCompletionSystemMessageParam,     # 表示系统设定的消息，role="system"，用于控制助手行为
    ChatCompletionAssistantMessageParam,  # 表示助手回复的消息，role="assistant"，可模拟历史对话或引导输出
)

def key(key_dir: str) -> str:
    """从文件或环境变量中获取API密钥。"""
    # 输入验证
    if not key_dir or not isinstance(key_dir, str):
        logging.warning('无效的密钥路径/名称：必须是非空字符串！')
        return ''
    # 文件路径处理
    if key_dir.lower().endswith('.txt'):
        try:
            with open(key_dir, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    logging.warning(f'密钥文件为空: {key_dir}')
                    return ''
                return content
        except Exception as e:
            raise RuntimeError(f'读取密钥文件 {key_dir} 失败: {str(e)}') from e
    # 环境变量处理
    else:
        value = os.environ.get(key_dir)
        if not value:
            logging.warning(f'环境变量不存在或为空: {key_dir}')
            return ''
        return value


class AIClient:
    """通用的OpenAI兼容API客户端，用于聊天完成。支持非流式和流式调用、单条指令、多轮对话、文本和图像输入以及自定义参数。"""

    def __init__(self, api_key: str, base_url: str, model: str):
        self._key = api_key             # API密钥
        self._url = base_url            # API接口
        self._model = model             # 模型名
        self.history: List[ChatCompletionMessageParam] = []  # 历史对话记录
        self.temperature = 0.8          # 采样温度
        self._update_client()           # 初始化OpenAI客户端

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, value: str):
        """设置新的API密钥并更新客户端。"""
        if value != self._key:
            self._key = value
            self._update_client()
        print(f'\033[31m\nAPI密钥已更新: {self._key[:4]}****\033[0m')

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str):
        """设置新的API URL并更新客户端。"""
        if value != self._url:
            self._url = value
            self._update_client()
        print(f'\033[31m\nAPI URL已更新: {self._url}\033[0m')

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, value: str):
        """设置新的API模型。"""
        if value != self._model:
            self._model = value
        print(f'\033[31m\nAPI模型已更新: {self._model}\033[0m')

    def _update_client(self):
        """使用当前密钥和URL更新OpenAI客户端。"""
        try:
            self.client = OpenAI(
                api_key=self._key,
                base_url=self._url
            )
        except Exception as e:
            print(f'客户端更新失败: {str(e)}')

    def _update_history(self, user: ChatCompletionMessageParam, ans: str):
        """更新对话历史记录。
        Args:
            user: 用户的消息。
            ans: 助手的回复。
        """
        if isinstance(user, dict) and 'content' in user and isinstance(user['content'], list):
            # 转换多模态消息为字符串，以兼容不支持列表content的模型
            user = {**user, 'content': '[多模态消息]'}
        assistant_message: ChatCompletionAssistantMessageParam = {'role': 'assistant', 'content': ans}
        self.history.extend([user, assistant_message])

    def _build_messages(
        self,
        user_command,
        system_command: str = '',
        history: List[ChatCompletionMessageParam] = []
    ) -> tuple:
        """为API调用构建消息列表。
        Args:
            user_command: 用户输入（字符串或字典用于多模态）。
            system_command: 可选的系统提示。
            history: 可选的对话历史。
        Returns:
            (消息列表, 处理后的user_command) 的元组。
        """
        messages: List[ChatCompletionMessageParam] = []
        if system_command:
            system_msg: ChatCompletionSystemMessageParam = {'role': 'system', 'content': system_command}
            messages.append(system_msg)
        if history:
            messages.extend(history)
        user_msg = user_command
        if user_command:
            if isinstance(user_command, dict):
                temp = []
                if user_command.get('txt'):
                    temp.append({'type': 'text', 'text': user_command['txt']})
                if user_command.get('img_url'):
                    temp.append({
                        'type': 'image_url',
                        'image_url': {'url': user_command['img_url']}
                    })
                if user_command.get('img_data'):
                    with open(user_command['img_data'], 'rb') as img_file:
                        img_base = base64.b64encode(img_file.read()).decode('utf-8')
                    temp.append({
                        'type': 'image_url',
                        'image_url': {'url': img_base}
                    })
                user_msg: ChatCompletionUserMessageParam = {'role': 'user', 'content': temp}
                messages.append(user_msg)
            else:
                user_msg: ChatCompletionUserMessageParam = {'role': 'user', 'content': user_command}
                messages.append(user_msg)
        return messages, user_msg

    def chat(
        self,
        user_command,
        system_command: str = '',
        history_flag: bool = False,
        history: List[ChatCompletionMessageParam] = []
    ) -> str:
        """执行非流式聊天完成。
        Args:
            user_command: 用户输入。
            system_command: 可选的系统提示。
            history_flag: 是否使用历史记录。
            history: 如果提供，则使用自定义历史。
        Returns:
            助手的回复。
        """
        temp_history = [] if not history_flag else (history if history else self.history)
        messages, user_command = self._build_messages(
            user_command, system_command, temp_history
        )
        completion = self.client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=self.temperature
        )
        ans = completion.choices[0].message.content or ''
        self._update_history(user_command, ans)
        return ans

    def chat_stream(
        self,
        user_command,
        system_command: str = '',
        history_flag: bool = False,
        history: List[ChatCompletionMessageParam] = []
    ):
        """执行流式聊天完成。
        Args:
            user_command: 用户输入。
            system_command: 可选的系统提示。
            history_flag: 是否使用历史记录。
            history: 如果提供，则使用自定义历史。
        Yields:
            助手回复的块。
        """
        temp_history = [] if not history_flag else (history if history else self.history)
        messages, user_command = self._build_messages(user_command, system_command, temp_history)
        completion = self.client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=self.temperature,
            stream=True
        )
        ans = ''
        for chunk in completion:
            if not hasattr(chunk, 'choices') or not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            if hasattr(delta, 'content') and delta.content:
                ans += delta.content
                yield delta.content
        self._update_history(user_command, ans)

# ======================================== 测试 ==============================================
if __name__ == '__main__':

    # key = key('API_GLM.txt')  # 方法1：解析txt文件
    api_key = key('OPENAI_API')  # 方法2：解析环境变量
    url = str(os.environ.get('OPENAI_URL'))
    model = 'ZhipuAI/GLM-4.5'
    gpt_client = AIClient(api_key=api_key, base_url=url, model=model)

    # =====================================================================================
    # <case 1> 非流式调用，单条指令
    print('================ <case 1> 非流式调用 ====================')
    # 1.1 输入：用户命令
    print('\033[32m---1.1 输入：用户命令\033[0m')
    use_command = '你是什么大模型？你的开发者是谁？'
    ans = gpt_client.chat(use_command)
    print(ans)

    # 1.2 输入：用户命令、系统命令
    print('\033[32m\n---1.2 输入：用户命令、系统命令\033[0m')
    sys_command = '回答内容请保持在20个字以内。'
    use_command = ('你是什么大模型？回答请包括模型名、你的开发者，该模型具体版本号、该模型最后的训练时间。')
    ans = gpt_client.chat(use_command, sys_command)
    print(ans)

    # 1.3 输入：用户命令、系统命令、历史对话
    print('\033[32m\n---1.3 输入：用户命令、系统命令、历史对话\033[0m')
    sys_command = '回答内容请保持在100个字以内。'
    use_command = '我第一次问你的是什么问题？复述一遍。'
    ans = gpt_client.chat(use_command, sys_command, history_flag=True)
    print(ans)

    # 1.4 输入：用户命令、系统命令、自定义历史对话
    print('\033[32m\n---1.4 输入：用户命令、系统命令、自定义历史对话\033[0m')
    history = []
    history.append({'role': 'user', 'content': '我是谁？'})
    history.append({'role': 'assistant', 'content': '你是李华。'})
    history.append({'role': 'user', 'content': '我从哪里来？'})
    history.append({'role': 'assistant', 'content': '你来自东土大唐。'})
    history.append({'role': 'user', 'content': '我要到哪里去？'})
    history.append({'role': 'assistant', 'content': '你要去西天取经。'})
    use_command = '我第二次问你的是什么问题？复述一遍。'
    ans = gpt_client.chat(use_command, sys_command, history_flag=True, history=history)
    print(ans)

    # 1.5 输入：在线图片
    print('\033[32m\n---1.5 输入：在线图片\033[0m')
    use_command = {}
    use_command['txt'] = '这张图描述了什么内容？表达了作者的什么感情？'
    use_command['img_url'] = ('https://bkimg.cdn.bcebos.com/pic/cf1b9d16fdfaaf51f3dec5bd8a0283eef01f3a29cc21')
    ans = gpt_client.chat(use_command)
    print(ans)

    # 1.6 输入：本地图片、系统命令
    print('\033[32m\n---1.6 输入：本地图片、系统命令\033[0m')
    sys_command = '回答内容请保持在100个字以内。'
    use_command = {}
    use_command['txt'] = '这张图描述了什么内容？表达了作者的什么感情？'
    use_command['img_data'] = 'img.jpg'
    ans = gpt_client.chat(use_command, sys_command)
    print(ans)

    # 1.7 输入：有图片的历史数据
    print('\033[32m\n---1.7 输入：有图片的历史数据\033[0m')
    use_command = '回顾聊天记录，我一共问了你几次问题？'
    ans = gpt_client.chat(use_command, history_flag=True)
    print(ans)

    # =====================================================================================
    # 使用过程中修改模型参数
    # gpt_client.model = 'ZhipuAI/GLM-4.5V'
    # gpt_client.temperature = 0.9
    # gpt_client.url = str(os.environ.get('OPENAI_URL'))
    # gpt_client.key = key('OPENAI_API')
    # gpt_client.history = []  # 清空对话历史记录

    # <case 2> 流式调用，多轮对话
    print('================ <case 2> 流式调用 ====================')
    # 2.1 输入：用户命令
    print('\033[34m---2.1 输入：用户命令\033[0m')
    use_command = '你是什么大模型？你的开发者是谁？'
    ans = gpt_client.chat_stream(use_command)
    for content in ans:
        print(content, end='')

    # 2.2 输入：用户命令、系统命令
    print('\033[34m\n---2.2 输入：用户命令、系统命令\033[0m')
    sys_command = '回答内容请保持在20个字以内。'
    use_command = ('你是什么大模型？回答请包括模型名、你的开发者、'
                   '该模型具体版本号、该模型最后的训练时间。')
    ans = gpt_client.chat_stream(use_command, sys_command)
    for content in ans:
        print(content, end='')

    # 2.3 输入：用户命令、系统命令、历史对话
    print('\033[34m\n---2.3 输入：用户命令、系统命令、历史对话\033[0m')
    sys_command = '回答内容请保持在100个字以内。'
    use_command = '我第一次问你的是什么问题？复述一遍。'
    ans = gpt_client.chat_stream(use_command, sys_command, history_flag=True)
    for content in ans:
        print(content, end='')

    # 2.4 输入：用户命令、系统命令、自定义历史对话
    print('\033[34m\n---2.4 输入：用户命令、系统命令、自定义历史对话\033[0m')
    history = []
    history.append({'role': 'user', 'content': '我是谁？'})
    history.append({'role': 'assistant', 'content': '你是李华。'})
    history.append({'role': 'user', 'content': '我从哪里来？'})
    history.append({'role': 'assistant', 'content': '你来自东土大唐。'})
    history.append({'role': 'user', 'content': '我要到哪里去？'})
    history.append({'role': 'assistant', 'content': '你要去西天取经。'})
    use_command = '我第二次问你的是什么问题？复述一遍。'
    ans = gpt_client.chat_stream(use_command, sys_command, history_flag=True, history=history)
    for content in ans:
        print(content, end='')

    # 2.5 输入：在线图片
    print('\033[34m\n---2.5 输入：在线图片\033[0m')
    use_command = {}
    use_command['txt'] = '这张图描述了什么内容？表达了作者的什么感情？'
    use_command['img_url'] = ('https://bkimg.cdn.bcebos.com/pic/cf1b9d16fdfaaf51f3dec5bd8a0283eef01f3a29cc21')
    ans = gpt_client.chat_stream(use_command)
    for content in ans:
        print(content, end='')

    # 2.6 输入：本地图片、系统命令
    print('\033[34m\n---2.6 输入：本地图片、系统命令\033[0m')
    sys_command = '回答内容请保持在100个字以内。'
    use_command = {}
    use_command['txt'] = '这张图描述了什么内容？表达了作者的什么感情？'
    use_command['img_data'] = 'img.jpg'
    ans = gpt_client.chat_stream(use_command, sys_command)
    for content in ans:
        print(content, end='')

    # 2.7 输入：有图片的历史数据
    print('\033[34m\n---2.7 输入：有图片的历史数据\033[0m')
    use_command = '回顾聊天记录，我一共问了你几次问题？'
    ans = gpt_client.chat_stream(use_command, history_flag=True)
    for content in ans:
        print(content, end='')
        print(content, end='')
