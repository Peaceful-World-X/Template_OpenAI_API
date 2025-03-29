# Template_OpenAI_API
一个类封装：大模型API的非流式调用、流式调用、单轮对话、多轮对话(有记忆)代码模板
密钥位置：用txt文本保存密钥内容（当然可以选择你更喜欢/安全的方式）

## 免费API申请地址
[ChatAnyWhere API申请](https://api.chatanywhere.org/v1/oauth/free/render)<br>
[ChatAnyWhere 项目地址](https://github.com/chatanywhere/GPT_API_free)<br>
转发Host1: https://api.chatanywhere.tech (国内中转，延时更低)<br>
转发Host2: https://api.chatanywhere.org (国外使用)

## Template_OpenAI_API.py
定义了一个 GPTClient 类，用于通过自定义 API 接口与 LLM 进行交互，支持非流式和流式两种调用方式。该类通过构造包含系统命令、历史消息和用户指令的消息列表，实现了对话交互逻辑。

## Model_ChatAnyWhere.py
查看ChatAnyWhere项目目前可支持的免费模型（截止到2025年3月28日支持的模型）
gpt-4o-mini-2024-07-18<br>
gpt-4o-mini<br>
text-embedding-3-large<br>
gpt-3.5-turbo<br>
gpt-3.5-turbo<br>
gpt-4o-ca<br>
gpt-4o-mini-ca<br>
gpt-4o<br>
gpt-4o-2024-05-13<br>
deepseek-r1<br>
gpt-3.5-turbo-ca<br>
text-embedding-3-small<br>
deepseek-v3<br>
gpt-4o-mini-2024-07-18-ca<br>
text-embedding-ada-002<br>
gpt-3.5-turbo-0125
