/*
封装的WebSocketClient
*/
class WebSocketClient {
    constructor(url) {
        this.url = url;
        this.ws = null;
        this.keepAliveTimer = null;
        this.manualClose = false;
        this.connect();
    };

    connect() {
        this.ws = new WebSocket(this.url);

        this.ws.onopen = () => {
            // 连接建立时触发
            console.log("✅ WebSocket 已连接");
            this.ws.send("hi");
            // 防止重复定时（若断开重连）
            if (this.keepAliveTimer) clearInterval(this.keepAliveTimer);
            // 每隔秒发送一次“hi”
            this.keepAliveTimer = setInterval(() => {
                if (this.ws && this.ws.readyState === WebSocket.OPEN) {
                    this.ws.send("hi");
                    console.log("💓 心跳已发送");
                }
            }, 10000);
        };
        this.ws.onmessage = (event) => {
            // 客户端接收到服务器数据时触发
            // 心跳不执行解密
            if (event.data === "hi") {
                console.log("❤️ 心跳已收到");
                return null;
            };
            console.log('%cWS接收到的信息', 'padding: 3px; border-radius: 7px; color: rgb(255, 255, 255); background-color: rgb(0, 158, 61);', event.data)
            this.onmessageCallback(event);
        };
        this.ws.onclose = (e) => {
            // 关闭连接触发
            console.warn("⚠️ WebSocket 已关闭:", e);
            if (this.keepAliveTimer) clearInterval(this.keepAliveTimer);
            this.ws = null;
            if (!this.manualClose){
                setTimeout(() => {
                    console.log("重连中...");
                    this.connect()
                }, 500);
            }
        };
        this.ws.onerror = (err) => {
            console.error("❌ WebSocket 出错:", err);
        };
    };

    onmessageCallback(event){
        // 要操作的加密或解密方法 自己写
        console.log('%cWS接收到的信息执行处理', 'padding: 3px; border-radius: 7px; color: rgb(255, 255, 255); background-color: rgb(0, 158, 61);', event.data);
        const task = JSON.parse(event.data);
        const { task_id, ...args} = task;
        // ======== 加密逻辑 ========
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

    close() {
        this.manualClose = true;
        // 关闭连接
        this.ws.close();
    };
};
// 导出全局
window.WebSocketClient = WebSocketClient;

// $s_ws = new WebSocketClient('ws://localhost:8765?client_id=xiaomuge&project_type=tiktok');
