# 飞书连接与验收

## 复用现有接入

先确认 Gateway 实际启动入口、进程及最新日志。已有可用机器人就复用，不重复创建应用或重置凭证。

对照当前安装版本的飞书接入文档与实现。官方参考：[飞书开放平台](https://open.feishu.cn/)、[接收消息事件](https://open.feishu.cn/document/server-docs/im-v1/message/events/receive)。平台权限名称、向导功能和租户审批要求可能变化，部署时核实，不把本流程当作已验证的租户配置。

## 接入步骤

1. 使用现有应用或用户要求的新应用，开启机器人能力。凭证通过配置界面或本机安全输入，不写入对话或 Skill。
2. 安装版本支持时使用 `hermes gateway setup`。扫码创建会建立外部应用，只适用于用户要求的新建接入；修复时复用原应用。
3. 对工作站部署优先核对 WebSocket 长连接模式。Hermes 主动连接飞书，无需为此额外暴露本地知识库服务。
4. 配置接收消息事件 `im.message.receive_v1`。使用审批卡片按钮时，另核对回调配置中的 `card.action.trigger`。
5. 按私聊、群内 @、附件等实际用途核对最小权限。安装文档可能列出 `im:message`、`im:message:send_as_bot`、`im:resource`、`im:chat`、`im:chat:readonly`；按当前平台权限页、安装实现与 API 错误核实，勿把历史别名当作唯一正确名称。
6. 发布应用版本，完成租户要求的审批，确认可用范围；群聊时将机器人加入目标群。
7. 配置允许的用户和群策略，再验证连接与一条授权消息。

字段示意，所有占位符由用户在部署环境填写：

```dotenv
FEISHU_APP_ID=<YOUR_APP_ID>
FEISHU_APP_SECRET=<YOUR_APP_SECRET>
FEISHU_DOMAIN=feishu
FEISHU_CONNECTION_MODE=websocket
FEISHU_ALLOWED_USERS=<ALLOWED_OPEN_IDS>
```

通过运行进程与安装文档确定生效的配置根目录，不默认固定路径。不通过清空白名单或关闭 @ 要求解决拒收。

## 启动与检查

先检查已安装 CLI 的帮助和现有服务管理方式，再用其支持的命令启动。没有健康 Gateway 且用户任务需要启动时，可使用安装版本支持的 `hermes gateway start`。不无故创建第二个 Gateway。

如果部署已有桌面联动或守护脚本，先检查实际脚本及其用法；这类脚本不是本 Skill 提供的标准组件。保持原有启动依赖，不凭文件名假定存在或创建重复守护。

日志参考标记（版本可能不同）：

```text
Connected in websocket mode (feishu)
Gateway running with 1 platform(s)
Received raw message → inbound message → [真实检索与正文读取] → response ready → Sending response
```

按本轮时间窗口及会话/消息标识关联证据，对外报告隐藏真实标识。`Sending response` 只表示发送尝试，还需检查后续错误、发送结果及飞书显示或用户确认。工具调用可能在会话记录而非 Gateway 日志中。

## 排障顺序

| 现象 | 优先检查 |
| --- | --- |
| 无连接 | 真实进程、配置根目录、凭证是否配置、网络与 SDK 错误 |
| 已连接但不收消息 | 事件、发布状态、应用可用范围、权限、群内 @ 和白名单 |
| 收到消息但不查资料 | 实际 Profile、技能可见性、工具权限与模型工具能力 |
| 检索路径不可用 | 运行账号、执行后端、本机挂载与目录权限 |
| 已生成但无回复 | 发送 API 错误、发消息权限、目标会话及超时 |
| 状态 connected 但无进程 | 状态过期，结合新鲜日志判断 |

恢复只影响确认失效的 Gateway 链，不结束其他应用或清空聊天记录。需重置历史上下文时先说明影响，按用户授权执行。
