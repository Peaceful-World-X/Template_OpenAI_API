from openai import OpenAI

# stream=True
stream=False

KEY = "xxxxxxxxxxxxxxxxxxxxxxxxx"
URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
model = "MiniMax/MiniMax-M1-80k"
sys_message  = "回答内容请保持在100个字以内。"
user_message = "你是什么大模型?回答请包括模型名、你的开发者、该模型具体版本号、该模型最后的训练时间。"
client = OpenAI(api_key=KEY, base_url=URL)

# 流式输出
if stream:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system","content": sys_message},
            {"role": "user","content": user_message}
        ],
        stream=True
    )
    for chunk in response:
        if not hasattr(chunk, "choices") or not chunk.choices:
            continue
        message = chunk.choices[0].delta
        if hasattr(message, "content") and message.content:
            print(message.content)

# 非流式输出
else:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system","content": sys_message},
            {"role": "user","content": user_message}
        ]
    )
    print(response.choices[0].message.content)
