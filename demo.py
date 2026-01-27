import json
import requests


# 示例一 ： get请求
url = "http://127.0.0.1:60001/encrypt_get"
params = {
    "client_id": "xiaomuge",  # 用户/客户端 （标识）
    "project_type": "tiktok", # 项目类型
    "types": "X-Bogus",
    "i": "msToken=x8XPnOSNCDk_Awa7ANfn96NYF7c0L5siXQ6imXu7bav_va_3fxg2RgyPqvzRwzGbALN6kn_eK1MmF-yQifjn5WS7bt2R0yM7aECyVORWMelbgdqcliJGSH0R2rO5GYm3LaCOYLRpfkM=",
    "t": "{}",
}
response = requests.get(url, params=params)
print(response.json())


# 示例二 ： post请求
url = "http://127.0.0.1:60001/encrypt_post"
params = {
    "client_id": "xiaomuge",       # 用户/客户端 （标识）
    "project_type": "tiktok",   # 项目类型
}
data = {
    "types": "X-Gnarly",
    "i": "msToken=x8XPnOSNCDk_Awa7ANfn96NYF7c0L5siXQ6imXu7bav_va_3fxg2RgyPqvzRwzGbALN6kn_eK1MmF-yQifjn5WS7bt2R0yM7aECyVORWMelbgdqcliJGSH0R2rO5GYm3LaCOYLRpfkM=",
    "t": "{}"
}
data = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
response = requests.post(url, params=params, data=data)
print(response.json())
