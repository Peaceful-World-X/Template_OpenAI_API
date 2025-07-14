<p align="center">
  <img width="250" height="250" alt="image" src="https://github.com/user-attachments/assets/553c81a8-eed7-4d8e-b03b-d605821b3e66"/>
</p>

<p align="center">
  <img src="https://img.shields.io/github/contributors/Peaceful-World-X/Template_OpenAI_API" alt="Contributors"/>
  <img src="https://img.shields.io/github/forks/Peaceful-World-X/Template_OpenAI_API" alt="Forks"/>
  <img src="https://img.shields.io/github/stars/Peaceful-World-X/Template_OpenAI_API" alt="Stars"/>
  <img src="https://img.shields.io/github/issues/Peaceful-World-X/Template_OpenAI_API" alt="Issues"/>
  <img src="https://img.shields.io/github/license/Peaceful-World-X/Template_OpenAI_API" alt="License"/>
  <img src="https://img.shields.io/badge/LinkedIn-Profile-blue" alt="LinkedIn"/>
  <img src="https://img.shields.io/github/downloads/Peaceful-World-X/Template_OpenAI_API/total" alt="Downloads"/>
</p>

<h1 align="center" style="font-size: 64px;">Template_OpenAI_API
  <a href="https://github.com/Peaceful-World-X/Template_OpenAI_API/archive/refs/heads/main.zip" download>模板点击下载⚡</a>
</h1>


🫠一个类封装：通用的OpenAI兼容API接口, 支持非流式和流式调用, 支持单条指令、多轮对话, 支持文字、图像输入等自定义参数<br>
```python
# 三行代码直接获取API结果
sys_command = "回答内容请保持在20个字以内。"
use_command = "你是什么大模型?回答请包括模型名、你的开发者、该模型具体版本号、该模型最后的训练时间。"
ans = gpt_client.chat(use_command, sys_command, history_True)
```

🔑密钥位置：用txt文本保存，或者环境变量（当然可以选择你更喜欢/安全的方式）<br>
🔥免费API统计：<a href="#lable">免费API申请地址(每月/每天免费刷新额度)</a>

## 1、文件介绍
- [Template_OpenAI_API.py](Template_OpenAI_API.py)：定义了一个 AIClient 类，支持非流式、流式，单条命令、多轮对话等调用方式。
- [Test_OpenAI_API.py](Test_OpenAI_API.py)：最精简的API调用模板。

## 2、API_KEY 命令行保存方法
- 方法一：txt文件
```bash
# 命令行写入txt密钥文件：
echo xxxxxxxx>>API_Chatanywhere.txt  # Windows cmd
echo "xxxxxxx">API_Chatanywhere.txt  # macOS/Linux
# 验证设置是否成功：
type API_Chatanywhere.txt            # Windows cmd
cat API_Chatanywhere.txt             # macOS/Linux
```
- 方法二：环境变量
```bash
# 命令行设置密钥环境变量：
set Chatanywhere_API_KEY=xxxxxxxx  # Windows cmd
export Chatanywhere_API_KEY="xxxx" # macOS/Linux
#验证设置是否成功：
echo %Chatanywhere_API_KEY%        # Windows cmd
echo $Chatanywhere_API_KEY         # macOS/Linux
```

## 3、AIClient 类使用示例
- 非流式调用
```python
# 1.1 输入用户命令
use_command = "你是什么大模型?你的开发者是谁？"
ans = gpt_client.chat(use_command)
print(ans)

# 1.2 输入用户命令、系统命令
sys_command = "回答内容请保持在20个字以内。"
use_command = "你是什么大模型?回答请包括模型名、你的开发者、该模型具体版本号、该模型最后的训练时间。"
ans = gpt_client.chat(use_command, sys_command)
print(ans)

# 1.3 输入用户命令、系统命令、历史对话
sys_command = "回答内容请保持在100个字以内。"   # 更新系统命令
use_command =  "我第一次问你的是什么问题？复述一遍。"
ans = gpt_client.chat(use_command, sys_command, history_True)
print(ans)

# 1.4 输入用户命令、系统命令、自定义历史对话
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
use_command = {}
use_command["txt"] = "这张图描述了什么内容？表达了作者的什么感情？"
use_command["img_url"] = "https://bkimg.cdn.bcebos.com/pic/cf1b9d16fdfaaf51f3dec5bd8a0283eef01f3a29cc21"
ans = gpt_client.chat(use_command)
print(ans)

# 1.6 输入本地图片、系统命令
sys_command = "回答内容请保持在100个字以内。"   # 更新系统命令
use_command = {}
use_command["txt"] = "这张图描述了什么内容？表达了作者的什么感情？"
use_command["img_data"] = "img.jpg"
ans = gpt_client.chat(use_command, sys_command)
print(ans)

# 1.7 输入有图片、文字的历史数据
use_command = "回顾聊天记录，我一共问了你几次问题？"
ans = gpt_client.chat(use_command, history_flag=True)
print(ans)
```
<img width="2534" height="936" alt="image" src="https://github.com/user-attachments/assets/8d77346c-beb1-4ce9-a135-977c9fb2f77a" />

- 流式调用
```python
# 2.1 输入用户命令
use_command = "你是什么大模型?你的开发者是谁？"
ans = gpt_client.chat_stream(use_command)
for content in ans:
    print(content, end="")

# 2.2 输入用户命令、系统命令
sys_command = "回答内容请保持在20个字以内。"
use_command = "你是什么大模型?回答请包括模型名、你的开发者、该模型具体版本号、该模型最后的训练时间。"
ans = gpt_client.chat(use_command, sys_command)
for content in ans:
    print(content, end="")

# 2.3 输入用户命令、系统命令、历史对话
sys_command = "回答内容请保持在100个字以内。"   # 更新系统命令
use_command =  "我第一次问你的是什么问题？复述一遍。"
ans = gpt_client.chat(use_command, sys_command, history_True)
for content in ans:
    print(content, end="")

# 2.4 输入用户命令、系统命令、自定义历史对话
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
use_command = {}
use_command["txt"] = "这张图描述了什么内容？表达了作者的什么感情？"
use_command["img_url"] = "https://bkimg.cdn.bcebos.com/pic/cf1b9d16fdfaaf51f3dec5bd8a0283eef01f3a29cc21"
ans = gpt_client.chat(use_command)
for content in ans:
    print(content, end="")

# 2.6 输入本地图片、系统命令
sys_command = "回答内容请保持在100个字以内。"   # 更新系统命令
use_command = {}
use_command["txt"] = "这张图描述了什么内容？表达了作者的什么感情？"
use_command["img_data"] = "img.jpg"
ans = gpt_client.chat(use_command, sys_command)
for content in ans:
    print(content, end="")

# 2.7 输入有图片、文字的历史数据
use_command = "回顾聊天记录，我一共问了你几次问题？"
ans = gpt_client.chat(use_command, history_flag=True)
for content in ans:
    print(content, end="")
```

<img width="2548" height="1064" alt="image" src="https://github.com/user-attachments/assets/aadbca75-e267-4280-a307-1800f28815e5" />

<span id="lable"></span>
## 4、免费API申请地址(每月/每天免费刷新额度，截止2025.07.13统计)
### 申请地址预览：
1. 智谱 GLM 官网：https://www.bigmodel.cn/usercenter/proj-mgmt/apikeys<br>
OpenAI API接口：https://open.bigmodel.cn/api/paas/v4<br>
2. 🔮Gemini 官网：https://aistudio.google.com/apikey<br>
OpenAI API接口：https://generativelanguage.googleapis.com/v1beta/openai/<br>
3. 🔮Github 官网：https://github.com/settings/personal-access-tokens/new<br>
OpenAI API接口：https://models.inference.ai.azure.com
4. Modelscope 魔塔社区：https://modelscope.cn/my/myaccesstoken<br>
OpenAI API接口：https://api-inference.modelscope.cn/v1/<br>
5. 硅基流动社区：https://cloud.siliconflow.cn/sft-0zitanxrpu/account/ak<br>
 OpenAI API接口：https://api.siliconflow.cn/v1/
6. OpenRouter 官网：https://openrouter.ai/settings/keys<br>
OpenAI API接口：https://openrouter.ai/api/v1<br>
7. GPT_API_free 项目：https://github.com/chatanywhere/GPT_API_free<br>
OpenAI API接口：https://api.chatanywhere.tech/v1
8. Free-ChatGPT-API 项目: https://github.com/popjane/free_chatgpt_api<br>
OpenAI API接口：https://free.v36.cm/v1/<br>

### 详细模型类型：
1. 智谱AI-GLM 官网：https://www.bigmodel.cn/usercenter/proj-mgmt/apikeys
   - OpenAI API兼容接口：https://open.bigmodel.cn/api/paas/v4
   - 可用模型类型（最新免费模型查看[智谱AI-GLM免费模型](https://www.bigmodel.cn/dev/activities/free/glm-z1-flash)）
   - glm-4.1v-thinking-flash(视频识别)
   - glm-4-flash-250414
   - glm-4-flash
   - glm-4v-flash(图像识别)
   - glm-z1-flash
   - cogview-3-flash(图像生成)
   - cogvideox-flash(视频生成)
2. 🔮Google Gemini 官网：https://aistudio.google.com/apikey
   - OpenAI API兼容接口：https://generativelanguage.googleapis.com/v1beta/openai/
   - 可用模型类型（最新免费模型查看[Google Gemini免费模型](https://ai.google.dev/gemini-api/docs/pricing)）
   - gemini-2.5-pro(图像识别、视频识别)
   - gemini-2.5-flash-lite-preview-06-17(图像识别、视频识别)
   - gemini-2.5-flash(图像识别、视频识别)
   - gemini-2.0-flash-lite(图像识别、视频识别)
   - gemini-2.0-flash(图像识别、视频识别)
   - gemini-1.5-flash-8b(图像识别、视频识别)
   - gemini-1.5-flash(图像识别、视频识别)
3. 🔮Github 官网：https://github.com/settings/personal-access-tokens/new
   - OpenAI API兼容接口：https://models.inference.ai.azure.com
   - 每日0.1美元调用，可用模型类型（最新免费模型查看[Github免费模型](https://github.com/marketplace/models)）
   - OpenAI GPT-4.1
   - OpenAI GPT-4o
   - OpenAI GPT-4.1-nano
   - DeepSeek-V3-0324
   - Grok 3
   - Llama 4 Scout 17B 16E Instruct
   - 等等50个模型
4. Modelscope 魔塔社区：https://modelscope.cn/my/myaccesstoken
   - OpenAI API兼容接口：https://api-inference.modelscope.cn/v1/
   - 每日2000次调用，可用模型类型（最新免费模型查看[Modelscope 免费模型](https://www.modelscope.cn/models?filter=inference_type&page=1&tabKey=task)）
   - Qwen/QwQ-32B
   - Qwen/Qwen3-235B-A22B
   - deepseek-ai/DeepSeek-R1-Distill-Qwen-7B
   - LLM-Research/Meta-Llama-3.1-8B-Instruct
   - 等等13283个模型
5. 硅基流动社区：https://cloud.siliconflow.cn/sft-0zitanxrpu/account/ak
   - OpenAI API兼容接口：https://api.siliconflow.cn/v1/
   - 免费模型无限制，可用模型类型（最新免费模型查看[硅基流动 免费模型](https://cloud.siliconflow.cn/sft-0zitanxrpu/models)）
   - THUDM/GLM-4.1V-9B-Thinking
   - THUDM/GLM-Z1-9B-0414
   - THUDM/GLM-4-9B-0414
   - THUDM/glm-4-9b-chat
   - Qwen/Qwen2.5-7B-Instruct
   - Qwen/Qwen2.5-Coder-7B-Instruct
   - Qwen/Qwen3-8B
   - Qwen/Qwen2-7B-Instruct
   - deepseek-ai/DeepSeek-R1-0528-Qwen3-8B
   - deepseek-ai/DeepSeek-R1-Distill-Qwen-7B
   - FunAudioLLM/SenseVoiceSmall
   - BAAI/bge-m3
   - BAAI/bge-reranker-v2-m3
   - BAAI/bge-large-zh-v1.5
   - BAAI/bge-large-en-v1.5
   - netease-youdao/bce-embedding-base_v1
   - netease-youdao/bce-reranker-base_v1
   - Kwai-Kolors/Kolors
   - internlm/internlm2_5-7b-chat
6. OpenRouter 社区：https://openrouter.ai/settings/keys
   - OpenAI API兼容接口：https://openrouter.ai/api/v1
   - 每日50次调用，可用模型类型（最新免费模型查看[OpenRouter免费模型](https://openrouter.ai/models?q=free&fmt=table)）
    - deepseek/deepseek-r1:free
    - deepseek/deepseek-v3-base:free
    - google/gemini-2.0-flash-exp:free
    - google/gemma-3-27b-it:free
    - meta-llama/llama-4-scout:free
    - qwen/qwen3-235b-a22b:free
    - thudm/glm-4-32b:free
    - thudm/glm-z1-32b:free
    - 等等60个模型
7. GPT_API_free 项目：https://github.com/chatanywhere/GPT_API_free
   - OpenAI API兼容接口：https://api.chatanywhere.tech/v1
   - 可用模型类型，输入Token小于4096（最新免费模型运行 [Models_ChatAnyWhere.py](Models_ChatAnyWhere.py) 查看）
   - deepseek-chat
   - deepseek-r1
   - deepseek-r1-250528
   - deepseek-v3
   - gpt-3.5-turbo
   - gpt-3.5-turbo-0125
   - gpt-3.5-turbo-1106
   - gpt-3.5-turbo-ca
   - gpt-4.1
   - gpt-4.1-mini
   - gpt-4.1-mini-2025-04-14
   - gpt-4.1-nano
   - gpt-4.1-nano-2025-04-14
   - gpt-4o
   - gpt-4o-2024-05-13
   - gpt-4o-ca
   - gpt-4o-mini
   - gpt-4o-mini-2024-07-18
   - gpt-4o-mini-2024-07-18-ca
   - gpt-4o-mini-ca
   - text-embedding-3-large
   - text-embedding-3-small
   - text-embedding-ada-002
8. Free-ChatGPT-API 项目: https://github.com/popjane/free_chatgpt_api
   - OpenAI API兼容接口：https://free.v36.cm/v1/
   - 可用模型类型（最新免费模型查看[Free-ChatGPT-API免费模型](https://github.com/popjane/free_chatgpt_api?tab=readme-ov-file#%E9%A1%B9%E7%9B%AE%E4%BB%8B%E7%BB%8D)）
   - gpt-4o-mini
   - gpt-3.5-turbo-0125
   - gpt-3.5-turbo-1106
   - gpt-3.5-turbo
   - gpt-3.5-turbo-16k
   - net-gpt-3.5-turbo
   - whisper-1
   - dall-e-2
