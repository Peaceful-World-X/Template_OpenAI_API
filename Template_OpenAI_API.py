from openai import OpenAI

history_False = False
history_True  = True

# 自动隐式解析API密钥 .txt保存、环境变量
def KEY(key_dir: str) -> str:
    import logging
    import os
    # 1. 输入验证
    if not key_dir or not isinstance(key_dir, str):
        logging.warning("无效的密钥路径/名称: 必须是非空字符串！"); return ''
    # 2. 文件路径处理
    if key_dir.lower().endswith('.txt'):
        try:
            with open(key_dir, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    logging.warning(f"密钥文件为空: {key_dir}"); return ''
                return content
        except Exception as e:
            raise RuntimeError(f"读取密钥文件 '{key_dir}' 失败: {str(e)}") from e; return ''
    # 3. 环境变量处理
    else:
        value = os.environ.get(key_dir)
        if not value:
            logging.warning(f"环境变量不存在或为空: {key_dir}"); return ''
        return value

# 通用的OpenAI兼容API接口, 支持非流式和流式调用, 支持单条指令、多轮对话, 支持文字、图像输入等自定义参数
class AIClient:
    def __init__(self, api_key: str, base_url: str, model: str):
        self._key = api_key             # API密钥
        self._url = base_url            # API接口
        self._model = model             # 模型名
        self.history = []               # 历史对话记录
        self.temperature = 0.8          # 采样温度
        self._update_client()           # 初始化OpenAI客户端

    @property
    def key(self) -> str: return self._key
    @key.setter
    # 设置新的 API 密钥并自动更新客户端
    def key(self, value: str):
        if value != self._key: self._key = value; self._update_client()
        print(f"\033[31m\nAPI 密钥已更新: {self._key[:4]}****\033[0m")  # 仅打印前4位，避免泄露完整密钥

    @property
    def url(self) -> str: return self._url
    @url.setter
    # 设置新的 API 接口并自动更新客户端
    def url(self, value: str):
        if value != self._url: self._url = value; self._update_client()
        print(f"\033[31m\nAPI 接口已更新: {self._url}\033[0m")

    @property
    # 获取当前使用的API模型
    def model(self) -> str: return self._model
    @model.setter
    # 设置新的 API 模型
    def model(self, value: str):
        if value != self._model: self._model = value
        print(f"\033[31m\nAPI 模型已更新: {self._model}\033[0m")

    # 更新API服务的URL或者模型名
    def _update_client(self):
        try:
            self.client = OpenAI(
                api_key=self._key,
                base_url=self._url
            )
        except Exception as e:
            print(f"客户端更新失败: {str(e)}")

    # 更新对话历史记录
    def _update_history(self, user, ans:str):
        self.history.append(user)
        self.history.append({"role": "assistant", "content": ans})

    """ 若需要模型的其他参数，自己加吧~ 具体参数查看 client.chat.completion 源代码参数
        # 可选参数 - 音频输入参数（用于语音识别任务）
        audio: Optional[ChatCompletionAudioParam] | NotGiven = NOT_GIVEN,
        # 可选参数 - 指定响应格式（如JSON对象）
        response_format: type[ResponseFormatT] | NotGiven = NOT_GIVEN,
        # 可选参数 - 频率惩罚（-2.0到2.0），减少重复内容
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        # 可选参数 - 函数调用设置（旧版函数调用）
        function_call: completion_create_params.FunctionCall | NotGiven = NOT_GIVEN,
        # 可选参数 - 可用函数列表（旧版函数调用）
        functions: Iterable[completion_create_params.Function] | NotGiven = NOT_GIVEN,
        # 可选参数 - token偏差调整（特定token的权重调整）
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        # 可选参数 - 是否返回token对数概率
        logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
        # 可选参数 - 仅控制完成部分的最大token数
        max_completion_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        # 可选参数 - 生成的最大总token数
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        # 可选参数 - 附加元数据（用于跟踪和分析）
        metadata: Optional[Metadata] | NotGiven = NOT_GIVEN,
        # 可选参数 - 支持的输入模态（文本/音频）
        modalities: Optional[List[Literal["text", "audio"]]] | NotGiven = NOT_GIVEN,
        # 可选参数 - 生成多个回复选项的数量
        n: Optional[int] | NotGiven = NOT_GIVEN,
        # 可选参数 - 是否允许并行工具调用
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        # 可选参数 - 预测内容参数（高级预测任务）
        prediction: Optional[ChatCompletionPredictionContentParam] | NotGiven = NOT_GIVEN,
        # 可选参数 - 存在惩罚（-2.0到2.0），鼓励新话题
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        # 可选参数 - 推理努力级别（平衡速度与质量）
        reasoning_effort: Optional[ReasoningEffort] | NotGiven = NOT_GIVEN,
        # 可选参数 - 随机种子（用于确定性输出）
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        # 可选参数 - 服务层级（优先级控制）
        service_tier: Optional[Literal["auto", "default", "flex", "scale", "priority"]] | NotGiven = NOT_GIVEN,
        # 可选参数 - 停止生成的token序列
        stop: Union[Optional[str], List[str], None] | NotGiven = NOT_GIVEN,
        # 可选参数 - 是否存储对话历史（用于合规/审计）
        store: Optional[bool] | NotGiven = NOT_GIVEN,
        # 可选参数 - 流式选项（控制流式响应行为）
        stream_options: Optional[ChatCompletionStreamOptionsParam] | NotGiven = NOT_GIVEN,
        # 可选参数 - 采样温度（0-2），控制输出随机性
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        # 可选参数 - 工具选择策略（新版工具调用）
        tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = NOT_GIVEN,
        # 可选参数 - 可用工具列表（新版工具调用）
        tools: Iterable[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
        # 可选参数 - 返回每个位置最可能token的数量
        top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        # 可选参数 - 核采样概率（0-1），控制输出多样性
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        # 可选参数 - 用户标识符（用于滥用检测）
        user: str | NotGiven = NOT_GIVEN,
        # 可选参数 - 网络搜索选项（启用实时网络搜索）
        web_search_options: completion_create_params.WebSearchOptions | NotGiven = NOT_GIVEN,
        # 可选参数 - 额外HTTP头（覆盖客户端设置）
        extra_headers: Headers | None = None,
        # 可选参数 - 额外查询参数（覆盖客户端设置）
        extra_query: Query | None = None,
        # 可选参数 - 额外请求体（覆盖客户端设置）
        extra_body: Body | None = None,
        # 可选参数 - 请求超时设置（秒）
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    """
    # =====================================================================================
    # 构造消息列表，先添加历史消息，再追加系统命令，最后添加当前用户命令
    def _build_messages(self,user_command, system_command: str='', history: list=[]):
        messages = []
        if system_command:
            messages.append({"role": "system", "content": system_command})
        if history:
            messages.extend(history)
        if user_command:
            if isinstance(user_command, dict):
                temp =[]
                if(user_command.get("txt")):
                    temp.append({"type": "text", "text": user_command["txt"]})
                if(user_command.get("img_url")):
                    temp.append({"type": "image_url", "image_url":{"url":user_command["img_url"]}})
                if(user_command.get("img_data")):
                    import base64
                    with open(user_command["img_data"], 'rb') as img_file:
                        img_base = base64.b64encode(img_file.read()).decode('utf-8')
                    temp.append({"type": "image_url", "image_url":{"url":img_base}})
                user_command = {"role": "user", "content": temp}
                messages.append(user_command)
            else:
                user_command = {"role": "user", "content": user_command}
                messages.append(user_command)
        return messages, user_command

    # 非流式调用接口
    def chat(self, user_command, system_command: str='', history_flag: bool = False, history: list = []):
        temp_history = [] if not history_flag else (history if history else self.history)
        messages,user_command = self._build_messages(user_command, system_command, temp_history)
        completion = self.client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=self.temperature
        )
        ans = completion.choices[0].message.content if completion.choices[0].message.content else ''
        self._update_history(user_command, ans)
        return ans

    # 流式调用接口
    def chat_stream(self, user_command, system_command: str='', history_flag: bool = False, history: list = []):
        temp_history = [] if not history_flag else (history if history else self.history)
        messages,user_command = self._build_messages(user_command, system_command, temp_history)
        completion = self.client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=self.temperature,
            stream=True
        )
        ans = ""
        for chunk in completion:
            if not hasattr(chunk, "choices") or not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            if hasattr(delta, "content") and delta.content:
                ans += delta.content
                yield delta.content
        self._update_history(user_command, ans)

# ======================================== 测试 ==============================================
if __name__ == '__main__':

    key   = KEY("API_GLM.txt")  # 获取方式一：解析txt文件
    # key = KEY("GLM_API_KEY")  # 获取方式二：解析环境变量
    url   = "https://open.bigmodel.cn/api/paas/v4"
    model = "glm-4v-flash"
    gpt_client = AIClient(api_key=key,base_url=url,model=model)

    # 使用过程中，可以随时修改模型的参数
    # gpt_client.model = "gemini-2.5-pro"
    # gpt_client.temperature = 0.2
    # gpt_client.url = "https://api.openai.com/v1"
    # gpt_client.key = KEY("API_Chatanywhere.txt")

    # =====================================================================================
    # <case 1> 非流式调用，单条指令
    print('================ <case 1> 非流式调用 ====================')
    # 1.1 输入用户命令
    print("\033[32m---1.1 输入：用户命令\033[0m")
    use_command = "你是什么大模型?你的开发者是谁？"
    ans = gpt_client.chat(use_command)
    print(ans)

    # 1.2 输入用户命令、系统命令
    print("\033[32m\n---1.2 输入：用户命令、系统命令\033[0m")
    sys_command = "回答内容请保持在20个字以内。"
    use_command = "你是什么大模型?回答请包括模型名、你的开发者、该模型具体版本号、该模型最后的训练时间。"
    ans = gpt_client.chat(use_command, sys_command)
    print(ans)

    # 1.3 输入用户命令、系统命令、历史对话
    print("\033[32m\n---1.3 输入：用户命令、系统命令、历史对话\033[0m")
    sys_command = "回答内容请保持在100个字以内。"   # 更新系统命令
    use_command =  "我第一次问你的是什么问题？复述一遍。"
    ans = gpt_client.chat(use_command, sys_command, history_True)
    print(ans)

    # 1.4 输入用户命令、系统命令、自定义历史对话
    print("\033[32m\n---1.4 输入：用户命令、系统命令、自定义历史对话\033[0m")
    history=[]
    history.append({"role": "user", "content": "我是谁？"})
    history.append({"role": "assistant", "content": "你是李华。"})
    history.append({"role": "user", "content": "我从哪里来？"})
    history.append({"role": "assistant", "content": "你来自东土大唐。"})
    history.append({"role": "user", "content": "我到哪里去？"})
    history.append({"role": "assistant", "content": "你将要去西天取经。"})
    use_command =  "我第2次问你的是什么问题？复述一遍。"
    ans = gpt_client.chat(use_command, sys_command, history_True, history)
    print(ans)

    # 1.5 输入在线图片
    print("\033[32m\n---1.5 输入：在线图片\033[0m")
    use_command = {}
    use_command["txt"] = "这张图描述了什么内容？表达了作者的什么感情？"
    use_command["img_url"] = "https://bkimg.cdn.bcebos.com/pic/cf1b9d16fdfaaf51f3dec5bd8a0283eef01f3a29cc21"
    ans = gpt_client.chat(use_command)
    print(ans)

    # 1.6 输入本地图片、系统命令
    print("\033[32m\n---1.6 输入：本地图片、系统命令\033[0m")
    sys_command = "回答内容请保持在100个字以内。"   # 更新系统命令
    use_command = {}
    use_command["txt"] = "这张图描述了什么内容？表达了作者的什么感情？"
    use_command["img_data"] = "img.jpg"
    ans = gpt_client.chat(use_command, sys_command)
    print(ans)

    # 1.7 输入有图片、文字的历史数据
    print("\033[32m\n---1.7 输入：有图片的历史数据\033[0m")
    use_command = "回顾聊天记录，我一共问了你几次问题？"
    ans = gpt_client.chat(use_command, history_flag=True)
    print(ans)


    # =====================================================================================
    # 使用过程中，可以随时修改模型的参数
    gpt_client.model = "glm-4.1v-thinking-flash"
    gpt_client.temperature = 0.9
    gpt_client.url = "https://open.bigmodel.cn/api/paas/v4"
    gpt_client.key = KEY("API_GLM.txt")
    gpt_client.history = []  # 清空历史对话记录
    # <case 2> 非流式调用，多轮对话
    print('================ <case 2> 非流式调用 ====================')
    # 2.1 输入用户命令
    print("\033[34m---2.1 输入：用户命令\033[0m")
    use_command = "你是什么大模型?你的开发者是谁？"
    ans = gpt_client.chat_stream(use_command)
    for content in ans:
        print(content, end="")

    # 2.2 输入用户命令、系统命令
    print("\033[34m\n---2.2 输入：用户命令、系统命令\033[0m")
    sys_command = "回答内容请保持在20个字以内。"
    use_command = "你是什么大模型?回答请包括模型名、你的开发者、该模型具体版本号、该模型最后的训练时间。"
    ans = gpt_client.chat(use_command, sys_command)
    for content in ans:
        print(content, end="")

    # 2.3 输入用户命令、系统命令、历史对话
    print("\033[34m\n---2.3 输入：用户命令、系统命令、历史对话\033[0m")
    sys_command = "回答内容请保持在100个字以内。"   # 更新系统命令
    use_command =  "我第一次问你的是什么问题？复述一遍。"
    ans = gpt_client.chat(use_command, sys_command, history_True)
    for content in ans:
        print(content, end="")

    # 2.4 输入用户命令、系统命令、自定义历史对话
    print("\033[34m\n---2.4 输入：用户命令、系统命令、自定义历史对话\033[0m")
    history=[]
    history.append({"role": "user", "content": "我是谁？"})
    history.append({"role": "assistant", "content": "你是李华。"})
    history.append({"role": "user", "content": "我从哪里来？"})
    history.append({"role": "assistant", "content": "你来自东土大唐。"})
    history.append({"role": "user", "content": "我到哪里去？"})
    history.append({"role": "assistant", "content": "你将要去西天取经。"})
    use_command =  "我第2次问你的是什么问题？复述一遍。"
    ans = gpt_client.chat(use_command, sys_command, history_True, history)
    for content in ans:
        print(content, end="")

    # 2.5 输入在线图片
    print("\033[34m\n---2.5 输入：在线图片\033[0m")
    use_command = {}
    use_command["txt"] = "这张图描述了什么内容？表达了作者的什么感情？"
    use_command["img_url"] = "https://bkimg.cdn.bcebos.com/pic/cf1b9d16fdfaaf51f3dec5bd8a0283eef01f3a29cc21"
    ans = gpt_client.chat(use_command)
    for content in ans:
        print(content, end="")

    # 2.6 输入本地图片、系统命令
    print("\033[34m\n---2.6 输入：本地图片、系统命令\033[0m")
    sys_command = "回答内容请保持在100个字以内。"   # 更新系统命令
    use_command = {}
    use_command["txt"] = "这张图描述了什么内容？表达了作者的什么感情？"
    use_command["img_data"] = "img.jpg"
    ans = gpt_client.chat(use_command, sys_command)
    for content in ans:
        print(content, end="")

    # 2.7 输入有图片、文字的历史数据
    print("\033[34m\n---2.7 输入：有图片的历史数据\033[0m")
    use_command = "回顾聊天记录，我一共问了你几次问题？"
    ans = gpt_client.chat(use_command, history_flag=True)
    for content in ans:
        print(content, end="")
