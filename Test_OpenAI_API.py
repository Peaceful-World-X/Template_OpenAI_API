from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyC3Rx_g_pQKZNmiYEYldN170JHJ2dVTmhA",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

response = client.chat.completions.create(
    model="gemini-2.5-flash-preview-tts",
    messages=[
        {"role": "system","content": "回答内容请保持在100个字以内。"},
        {"role": "user","content": "你是什么大模型?回答请包括模型名、你的开发者、该模型具体版本号、该模型最后的训练时间。"}
    ]
)

print(response.choices[0].message.content)
