### 简易版 RPC，导出浏览器内部方法临时使用
![Python Version](https://img.shields.io/badge/Python-3.12-blue)

### 项目作用
本项目用于把浏览器页面里的内部方法临时导出成 FastAPI 接口，方便本机或局域网直接调用浏览器运行时里的加密、解密、签名等函数。核心逻辑是在浏览器里注入 `WebSocketClient.js`，通过 `onmessageCallback` 判断 `types` 并调用页面内部方法，最后把处理结果返回给接口调用方。

### 通信流程
```text
参数 -> FastAPI 接口 -> ws send -> 浏览器 WebSocket 接收
-> onmessageCallback 判断方法类型并处理 -> 浏览器 ws 返回结果
-> FastAPI 返回接口响应 -> 调用方拿到浏览器内部方法处理后的结果
```

### 1. 安装 *requirements.txt* 内的模块
### 2. 运行 *server_interface.py* 服务
启动后会同时开启：
- FastAPI 接口服务：默认 `http://127.0.0.1:60001`
- WebSocket 服务：默认 `ws://127.0.0.1:8765`

如需修改端口，可以直接在 `server_interface.py` 里调整 API 端口和 ws 端口。

### 3. 打开浏览器，对要导出的内部方法位置打断点，并注入 *WebSocketClient.js*
例如加密、解密、签名参数生成位置。

### 4. 在 *WebSocketClient.js* 里修改导出逻辑
主要修改 `onmessageCallback` 里的处理逻辑，根据服务端传来的 `types` 调用浏览器页面内部方法。

这个函数就是自定义导出方法的位置。`types` 用来区分要调用哪个浏览器内部方法，`i`、`t` 等字段是从 FastAPI 接口传进来的自定义参数，处理完成后必须带着原来的 `task_id` 返回结果。

```js
onmessageCallback(event){
    // 要操作的加密或解密方法，按自己的项目逻辑修改这里
    console.log('%cWS接收到的信息执行处理', 'padding: 3px; border-radius: 7px; color: rgb(255, 255, 255); background-color: rgb(0, 158, 61);', event.data);
    const task = JSON.parse(event.data);
    const { task_id, ...args } = task;

    // ======== 自定义导出方法逻辑 ========
    var encrypted = null;
    if (args.types === 'X-Bogus'){
        encrypted = yn(args.i, args.t);
    } else if (args.types === 'X-Gnarly'){
        encrypted = bn(args.i, args.t);
    } else if (args.types === 'sign'){
        encrypted = Qd("mark=LP&version=1.0&expire_time=" + parseInt(+new Date() / 1000));
    }

    this.ws.send(JSON.stringify({ task_id, result: encrypted }));
}
```

### 5. 注入完成后，放开 debugger，然后连接 ws
```js
// client_id - 用户/客户端 （标识）
// project_type - 项目类型 （注册 - 支持一个用户注册多个项目类型）
$s_ws = new WebSocketClient('ws://localhost:8765?client_id=xiaomuge&project_type=tiktok');
```
### 6. 连接成功后，通过 FastAPI 调用浏览器内部方法
GET 示例：
```
// client_id - 用户/客户端（使用已注册过的）
// project_type - 项目类型 （使用已注册过的）
// types 、i、t 都属于自定义的传参内容
http://127.0.0.1:60001/encrypt_get?client_id=xiaomuge&project_type=tiktok&types=X-Bogus&i=msToken=你的参数&t={}
```

POST 示例见 `demo.py`，接口为：
```text
http://127.0.0.1:60001/encrypt_post?client_id=xiaomuge&project_type=tiktok
```

### 7. 返回的数据
`{'status': 'ok', 'msg': 'DFSzswVLUHydUWXFCuJl7z/Rssy6'}`

`{'status': 'ok', 'msg': 'MC4tQC4uN9iMvo21zGKkpJofgT-9NBaXLjfvbc4Wft0gh1AzF5LLdVF8Yh14rnmzSjZ9jLJUuOkFSancg8GBrHbWclYE-7h7OL/pp-I4Nmbt0OItg/jHwpsjkoklzFAbkrKX98t1XRTU5j7SBbBdoApJ85B0GuUsFOT2Mu9E-lE0RIw8Y7jke-cpysePDiBDvyXK7nf/g0GC9N6u1kVzPxmDLahJ5vH8QdFcpBI29t3Z12ZsCGnoV5sqk0Z2BiDWdWKLtxektD-T'}`

### 8. 注意事项
- `client_id` 和 `project_type` 必须和浏览器 ws 连接时注册的一致。
- `types` 是自定义方法标识，需要和 `WebSocketClient.js` 的 `onmessageCallback` 判断逻辑一致。
- 如果在局域网使用，请注意端口暴露风险；该工具默认没有鉴权，建议仅在可信环境里使用。

### 9. 操作如下
<img src="https://raw.githubusercontent.com/xiaomuge898/xiaomuge898/refs/heads/main/simplified-rpc-img/1.png" width="800" />
<img src="https://raw.githubusercontent.com/xiaomuge898/xiaomuge898/refs/heads/main/simplified-rpc-img/2.png" width="800" />
<img src="https://raw.githubusercontent.com/xiaomuge898/xiaomuge898/refs/heads/main/simplified-rpc-img/3.png" width="800" />
<img src="https://raw.githubusercontent.com/xiaomuge898/xiaomuge898/refs/heads/main/simplified-rpc-img/4.png" width="800" />
<img src="https://raw.githubusercontent.com/xiaomuge898/xiaomuge898/refs/heads/main/simplified-rpc-img/5.png" width="800" />
<img src="https://raw.githubusercontent.com/xiaomuge898/xiaomuge898/refs/heads/main/simplified-rpc-img/6.png" width="800" />
<img src="https://raw.githubusercontent.com/xiaomuge898/xiaomuge898/refs/heads/main/simplified-rpc-img/2026-01-27_19-31-08.gif" width="1200" />
