# Template_OpenAI_API
一个类封装：大模型API的非流式调用、流式调用、单轮对话、多轮对话(有记忆)代码模板<br>
密钥位置：用txt文本保存密钥内容（当然可以选择你更喜欢/安全的方式）

## 免费API申请地址
**GPT_API_free 项目** <br>
ChatAnyWhere API申请：https://api.chatanywhere.org/v1/oauth/free/render<br>
Host 接口: https://api.chatanywhere.tech <br>
<br>
**FREE-CHATGPT-API 项目** <br>
FreeV36 API申请：https://free.v36.cm/oauth/github<br>
Host 接口: https://free.v36.cm/v1/<br>

## Template_OpenAI_API.py
定义了一个 GPTClient 类，用于通过自定义 API 接口与 LLM 进行交互，支持非流式和流式两种调用方式。该类通过构造包含系统命令、历史消息和用户指令的消息列表，实现了对话交互逻辑。

## Model_ChatAnyWhere.py
查看 **ChatAnyWhere** 项目目前可支持的免费模型（截止到2025年7月10日支持的模型）<br>
deepseek-chat<br>
deepseek-r1<br>
deepseek-r1-250528<br>
deepseek-v3<br>
gpt-3.5-turbo<br>
gpt-3.5-turbo-0125<br>
gpt-3.5-turbo-1106<br>
gpt-3.5-turbo-ca<br>
gpt-4.1<br>
gpt-4.1-mini<br>
gpt-4.1-mini-2025-04-14<br>
gpt-4.1-nano<br>
gpt-4.1-nano-2025-04-14<br>
gpt-4o<br>
gpt-4o-2024-05-13<br>
gpt-4o-ca<br>
gpt-4o-mini<br>
gpt-4o-mini-2024-07-18<br>
gpt-4o-mini-2024-07-18-ca<br>
gpt-4o-mini-ca<br>
text-embedding-3-large<br>
text-embedding-3-small<br>
text-embedding-ada-002<br>

查看 **FREE-CHATGPT-API** 项目目前可支持的免费模型（截止到2025年7月10日支持的模型）<br>
gpt-4o-mini<br>
gpt-3.5-turbo-0125<br>
gpt-3.5-turbo-1106<br>
gpt-3.5-turbo<br>
gpt-3.5-turbo-16k<br>
net-gpt-3.5-turbo<br>
whisper-1<br>
dall-e-2<br>
