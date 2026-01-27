### 简易版RPC，参数逆向调用临时使用
![Python Version](https://img.shields.io/badge/Python-3.12-blue)

### 1. 安装 *requirements.txt* 内的模块
### 2. 运行 *Server interface.py* 服务
`自定义修改ws的连接端口 和 API接口的端口号（接口端口号默认60001、ws端口号默认8765）`
### 3. 打开浏览器，对要逆向的参数位置打断点，当参数断住后，立马注入 *WebSocketClient.js*
### 4. 注入的时候需要修改一下回调函数里的加密逻辑方法
### 5. 注入完成后，放开debugger, 然后使用下面命令连接 ws 
```js
// client_id - 用户/客户端 （标识）
// project_type - 项目类型 （注册 - 支持一个用户注册多个项目类型）
$s_ws = new WebSocketClient('ws://localhost:8765?client_id=xiaomuge&project_type=tiktok');
```
### 6. 连接成功后, 可以通过浏览器或其他请求方式访问下面的连接地址，（如果有修改*Server interface.py* 服务，则需要根据路径访问）
```
// client_id - 用户/客户端（使用已注册过的）
// project_type - 项目类型 （使用已注册过的）
// types 、i、t 都属于自定义的传参内容
http://127.0.0.1:60001/encrypt?client_id=xiaomuge&project_type=tiktok&types=X-Bogus&i=msToken=x8XPnOSNCDk_Awa7ANfn96NYF7c0L5siXQ6imXu7bav_va_3fxg2RgyPqvzRwzGbALN6kn_eK1MmF-yQifjn5WS7bt2R0yM7aECyVORWMelbgdqcliJ&t={}
```
### 7.返回的数据
`{'status': 'ok', 'msg': 'DFSzswVLUHydUWXFCuJl7z/Rssy6'}`

`{'status': 'ok', 'msg': 'MC4tQC4uN9iMvo21zGKkpJofgT-9NBaXLjfvbc4Wft0gh1AzF5LLdVF8Yh14rnmzSjZ9jLJUuOkFSancg8GBrHbWclYE-7h7OL/pp-I4Nmbt0OItg/jHwpsjkoklzFAbkrKX98t1XRTU5j7SBbBdoApJ85B0GuUsFOT2Mu9E-lE0RIw8Y7jke-cpysePDiBDvyXK7nf/g0GC9N6u1kVzPxmDLahJ5vH8QdFcpBI29t3Z12ZsCGnoV5sqk0Z2BiDWdWKLtxektD-T'}`

### 8.操作如下
<img src="https://raw.githubusercontent.com/xiaomuge898/xiaomuge898/refs/heads/main/simplified-rpc-img/1.png" width="800" />
<img src="https://raw.githubusercontent.com/xiaomuge898/xiaomuge898/refs/heads/main/simplified-rpc-img/2.png" width="800" />
<img src="https://raw.githubusercontent.com/xiaomuge898/xiaomuge898/refs/heads/main/simplified-rpc-img/3.png" width="800" />
<img src="https://raw.githubusercontent.com/xiaomuge898/xiaomuge898/refs/heads/main/simplified-rpc-img/4.png" width="800" />
<img src="https://raw.githubusercontent.com/xiaomuge898/xiaomuge898/refs/heads/main/simplified-rpc-img/5.png" width="800" />
<img src="https://raw.githubusercontent.com/xiaomuge898/xiaomuge898/refs/heads/main/simplified-rpc-img/6.png" width="800" />
<img src="https://raw.githubusercontent.com/xiaomuge898/xiaomuge898/refs/heads/main/simplified-rpc-img/2026-01-27_19-31-08.gif" width="1200" />
