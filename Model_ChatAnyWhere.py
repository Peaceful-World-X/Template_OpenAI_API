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
for model in models:
    print(model.get("id"))

'''
gpt-4o-mini-2024-07-18
gpt-4o-mini
text-embedding-3-large
gpt-3.5-turbo
gpt-3.5-turbo
gpt-4o-ca
gpt-4o-mini-ca
gpt-4o
gpt-4o-2024-05-13
deepseek-r1
gpt-3.5-turbo-ca
text-embedding-3-small
deepseek-v3
gpt-4o-mini-2024-07-18-ca
text-embedding-ada-002
gpt-3.5-turbo-0125
'''

