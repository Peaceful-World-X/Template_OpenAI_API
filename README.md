# Template_OpenAI_API
一个类封装：大模型API的非流式调用、流式调用、单轮对话、多轮对话(有记忆)代码模板<br>
密钥位置：用txt文本保存密钥内容（当然可以选择你更喜欢/安全的方式）

## 免费API申请地址
GPT_API_free 项目 <br>
[ChatAnyWhere API申请](https://api.chatanywhere.org/v1/oauth/free/render)<br>
Host 接口: https://api.chatanywhere.tech <br>
<br>
FREE-CHATGPT-API 项目 <br>
[free.v36 API申请](https://free.v36.cm/oauth/github)<br>
Host 接口: https://free.v36.cm/v1/<br>

## Template_OpenAI_API.py
定义了一个 GPTClient 类，用于通过自定义 API 接口与 LLM 进行交互，支持非流式和流式两种调用方式。该类通过构造包含系统命令、历史消息和用户指令的消息列表，实现了对话交互逻辑。

## Model_ChatAnyWhere.py
查看ChatAnyWhere项目目前可支持的免费模型（截止到2025年7月10日支持的模型）<br>
deepseek-chat
deepseek-r1
deepseek-r1-250528
deepseek-v3
gpt-3.5-turbo
gpt-3.5-turbo-0125
gpt-3.5-turbo-1106
gpt-3.5-turbo-ca
gpt-4.1
gpt-4.1-mini
gpt-4.1-mini-2025-04-14
gpt-4.1-nano
gpt-4.1-nano-2025-04-14
gpt-4o
gpt-4o-2024-05-13
gpt-4o-ca
gpt-4o-mini
gpt-4o-mini-2024-07-18
gpt-4o-mini-2024-07-18-ca
gpt-4o-mini-ca
text-embedding-3-large
text-embedding-3-small
text-embedding-ada-002

查看 FREE-CHATGPT-API项目目前可支持的免费模型（截止到2025年7月10日支持的模型）<br>
gpt-4o-mini
gpt-3.5-turbo-0125
gpt-3.5-turbo-1106
gpt-3.5-turbo
gpt-3.5-turbo-16k
net-gpt-3.5-turbo
whisper-1
dall-e-2
