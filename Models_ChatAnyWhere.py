# 列出 ChatAnywhere 免费的模型
import requests

API_KEY = open("API_Chatanywhere.txt", "r", encoding="utf-8").read().strip()
url = "https://api.chatanywhere.tech/v1/models"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "User-Agent": "Apifox/1.0.0 (https://apifox.com)"
}
response = requests.get(url, headers=headers)
models = response.json().get("data", [])

# 使用集合去重并排序
unique_sorted_models = sorted(set(model.get("id") for model in models))

# 打印排序后的模型ID
for model_id in unique_sorted_models:
    print(model_id)

'''
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
'''

