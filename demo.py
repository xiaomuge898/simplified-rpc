import requests


API_BASE = "http://127.0.0.1:60001"

# client_id 和 project_type 用来定位已经连接到服务端的浏览器 WS 客户端。
# 这两个值必须和浏览器里 new WebSocketClient(...) 注册的一致。
CLIENT_PARAMS = {
    "client_id": "xiaomuge",
    "project_type": "tiktok",
}

# 示例业务参数：会被 server_interface.py 原样转发给浏览器 WS。
# 浏览器端 WebSocketClient.js 的 onmessageCallback 会根据 types 判断执行哪个内部方法。
TASK_PAYLOAD = {
    "types": "X-Bogus",
    "i": "msToken=你的参数",
    "t": "{}",
}


def encrypt_get_demo() -> dict:
    """GET 示例：把参数放在 URL query 中，适合简单获取类调用。

    GET 的重点是“获取结果”：参数会拼到 URL 后面，适合少量、简单、可读的参数。
    如果参数很长、结构复杂，或者包含授权/加密/解密所需的业务数据，优先使用 POST。
    """
    response = requests.get(
        f"{API_BASE}/encrypt_get",
        params={**CLIENT_PARAMS, **TASK_PAYLOAD},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def encrypt_post_demo() -> dict:
    """POST 示例：把业务参数放在 JSON body 中，适合传参给 WS 执行业务方法。

    POST 的重点是“传业务参数”：URL query 只放 client_id/project_type 用来找浏览器 WS，
    JSON body 放 types、i、t 等真实业务参数，用于触发浏览器内部的加密、解密或授权方法。
    """
    response = requests.post(
        f"{API_BASE}/encrypt_post",
        params=CLIENT_PARAMS,
        json={**TASK_PAYLOAD, "types": "X-Gnarly"},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    print("GET 获取结果示例:", encrypt_get_demo())
    print("POST 传参到 WS 示例:", encrypt_post_demo())
