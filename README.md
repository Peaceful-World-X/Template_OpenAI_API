# Template_OpenAI_API
🫠一个类封装：通用的OpenAI兼容API接口, 支持非流式和流式调用, 支持单条指令、多轮对话, 支持文字、图像输入等自定义参数<br>
🔑密钥位置：用txt文本保存，或者环境变量（当然可以选择你更喜欢/安全的方式）<br>
🔥免费API统计：[免费API申请地址(每月/每天免费刷新额度)](https://github.com/Peaceful-World-X/Template_OpenAI_API/tree/main?tab=readme-ov-file#4%E5%85%8D%E8%B4%B9api%E7%94%B3%E8%AF%B7%E5%9C%B0%E5%9D%80%E6%AF%8F%E6%9C%88%E6%AF%8F%E5%A4%A9%E5%85%8D%E8%B4%B9%E5%88%B7%E6%96%B0%E9%A2%9D%E5%BA%A6))

## 1、文件介绍
- Template_OpenAI_API.py：定义了一个 AIClient 类，支持非流式、流式，单条命令、多轮对话等调用方式。
- Test_OpenAI_API.py：最精简的API调用模板。

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
history.append({"role": "assistant", "content": "你来自中国。"})
history.append({"role": "user", "content": "我到哪里去？"})
history.append({"role": "assistant", "content": "你将要去外国。"})
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
history.append({"role": "assistant", "content": "你来自中国。"})
history.append({"role": "user", "content": "我到哪里去？"})
history.append({"role": "assistant", "content": "你将要去外国。"})
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

## 4、免费API申请地址(每月/每天免费刷新额度)
1. 智谱AI-GLM 官网：https://www.bigmodel.cn/usercenter/proj-mgmt/apikeys
   - OpenAI API兼容接口：https://open.bigmodel.cn/api/paas/v4
   - 可用模型类型（截止2025.07.13统计，最新免费模型查看[智谱AI-GLM免费模型](https://www.bigmodel.cn/dev/activities/free/glm-z1-flash)
   - glm-4.1v-thinking-flash(视频识别)
   - glm-4-flash-250414
   - glm-4-flash
   - glm-4v-flash(图像识别)
   - glm-z1-flash
   - cogview-3-flash(图像生成)
   - cogvideox-flash(视频生成)
2. 🔮Google Gemini 官网：https://aistudio.google.com/apikey
   - OpenAI API兼容接口：https://generativelanguage.googleapis.com/v1beta/openai/
   - 可用模型类型（截止2025.07.13统计，最新免费模型查看[Google Gemini免费模型](https://ai.google.dev/gemini-api/docs/pricing)
   - gemini-2.5-pro(图像识别、视频识别)
   - gemini-2.5-flash-lite-preview-06-17(图像识别、视频识别)
   - gemini-2.5-flash(图像识别、视频识别)
   - gemini-2.0-flash-lite(图像识别、视频识别)
   - gemini-2.0-flash(图像识别、视频识别)
   - gemini-1.5-flash-8b(图像识别、视频识别)
   - gemini-1.5-flash(图像识别、视频识别)
3. GPT_API_free 项目：https://github.com/chatanywhere/GPT_API_free
   - OpenAI API兼容接口：https://api.chatanywhere.tech/v1
   - 可用模型类型，输入Token小于4096（截止2025.07.13统计，最新免费模型运行 Models_ChatAnyWhere.py 查看）
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
4. Free-ChatGPT-API 项目: https://github.com/popjane/free_chatgpt_api
   - OpenAI API兼容接口：https://free.v36.cm/v1/
   - 可用模型类型（截止2025.07.13统计，最新免费模型查看[Free-ChatGPT-API免费模型](https://github.com/popjane/free_chatgpt_api?tab=readme-ov-file#%E9%A1%B9%E7%9B%AE%E4%BB%8B%E7%BB%8D)
   - gpt-4o-mini
   - gpt-3.5-turbo-0125
   - gpt-3.5-turbo-1106
   - gpt-3.5-turbo
   - gpt-3.5-turbo-16k
   - net-gpt-3.5-turbo
   - whisper-1
   - dall-e-2
