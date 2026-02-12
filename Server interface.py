import asyncio
import json
import uuid
import websockets
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# 允许跨域（方便你浏览器连）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WSManager:
    def __init__(self):
        self.server_task = None
        self.port = 8765  # 设置ws端口
        self.connections = {}
        self.tasks = {}


    async def echo(self, websocket):
        client_id = getattr(websocket, "client_id", None)
        types = getattr(websocket, "project_type", [])
        print(f"✅ client_id 新连接: {client_id}")
        print(f"✅ project_type 项目: {types}")
        print(f"✅ 所有的用户项目: {self.connections}")
        try:
            async for message in websocket:
                print(f"[{client_id}] 说: {message}")
                if message == "hi":
                    await websocket.send("hi")
                    continue
                # 浏览器回传的消息应是 JSON 格式 {"task_id": "...", "result": "..."}
                data = json.loads(message)
                task_id = data.get("task_id")
                result = data.get("result")
                if task_id in self.tasks:
                    self.tasks[task_id].set_result(result)
        except websockets.ConnectionClosed:
            print(f"❌ 断开连接: {client_id}")
        finally:
            # 断开连接时删除记录
            if client_id in self.connections:
                del self.connections[client_id]

    async def process_request(self, path, request_headers):
        """握手阶段捕获 path 和 query 参数"""
        _path = request_headers.path[2:]
        assert _path, '必须设置用户昵称name和项目类型type'
        data = {p.split('=',1)[0]:p.split('=',1)[-1] for p in _path.split('&')}
        client_id = data.get('client_id')
        project_type = data.get('project_type')
        if not client_id or not project_type:
            # 如果参数不全，拒绝握手
            print("❌ 缺少 client_id 或 project_type 参数")
            return (
                400,
                [],
                b"Missing required parameters: client_id and project_type"
            )

        print(f"握手参数: client_id={client_id}, type={project_type}")
        path.client_id = client_id
        path.project_type = [project_type]
        if client_id not in self.connections:
            self.connections[client_id] = {}
        self.connections[client_id][project_type] = path

    async def send_task(self, websocket, data):
        """发送任务到浏览器并等待结果"""
        task_id = str(uuid.uuid4())
        future = asyncio.get_event_loop().create_future()
        self.tasks[task_id] = future
        payload = {"task_id": task_id, "data": data}
        if isinstance(data, dict):
            payload = {"task_id": task_id, **data}
        try:
            await websocket.send(json.dumps(payload))
            result = await asyncio.wait_for(future, timeout=10)  # 最多等待10秒
            self.tasks.pop(task_id, None)
            return result
        except asyncio.TimeoutError:
            return "浏览器处理超时"
        except Exception as e:
            return f"ws异常: {e}"
        finally:
            # ✅ 无论成功、失败、超时，都必须清理
            self.tasks.pop(task_id, None)

    async def run_server(self):
        async with websockets.serve(
            self.echo,
            "0.0.0.0",
            self.port,
            process_request=self.process_request
        ):
            print(f"✅ WS 服务已启动: ws://localhost:{self.port}")
            await asyncio.Future()

    async def start_background_server(self):
        # 在 FastAPI 启动时启动 WS 服务
        if not self.server_task:
            self.server_task = asyncio.create_task(self.run_server())

manager = WSManager()

@app.on_event("startup")
async def on_startup():
    """FastAPI 启动时自动开启 WebSocket 服务"""
    if not manager.server_task:
        await manager.start_background_server()

@app.get("/encrypt_get")
async def encrypt_get(request: Request, client_id: str, project_type: str):
    """外部 Python 客户端可以调用这个接口"""
    if not client_id in manager.connections:
        return {"status": "ok", "msg": f"该用户不存在【{client_id}】"}
    if not project_type in manager.connections[client_id]:
        return {"status": "ok", "msg": f"该用户不存在此项目【{project_type}】"}
    query_params = dict(request.query_params)
    result = await manager.send_task(manager.connections[client_id][project_type], query_params)
    return {"status": "ok", "msg": result}

@app.post("/encrypt_post")
async def encrypt_post(request: Request, client_id: str, project_type: str):
    """外部 Python 客户端可以调用这个接口"""
    if not client_id in manager.connections:
        return {"status": "ok", "msg": f"该用户不存在【{client_id}】"}
    if not project_type in manager.connections[client_id]:
        return {"status": "ok", "msg": f"该用户不存在此项目【{project_type}】"}
    try:
        data_dict = await request.json()
    except:
        return {"status": "ok", "msg": '请用 application/json 类型'}
    result = await manager.send_task(manager.connections[client_id][project_type], data_dict)
    return {"status": "ok", "msg": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Server interface:app", host="0.0.0.0", port=60001)
