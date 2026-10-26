# 800行代码实现 Open Claw 的 Tool、消息总线、子Agent管理架构：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_OpenClaw核心架构800行实现.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
800
行
原创
代码实现 Open Claw 的 Tool、消息总线
会员技术团队 2026年4月24日 01:29 浙江
大淘宝技术 7人
、子Agent管理架构
这篇文章记录对 Open Claw 中 Tool、消息总线和子 Agent 管理架构的研究学习，以
及一个最小可运
行实现。
本文想说明的技术观点是对于 Tool 调用、消息分发、子 Agent 管理这三类 Agent
系
统
里的核心组
件，优先采用薄抽象、显式控制流和贴
近模型 API 的实现方式，往往比引入
多层中间件更容易获得工程上的确定性。
系
统边界更清晰，运
行
路径更容易追踪，问题更
容易定位，也更适合作为后续扩展 Memory、调度和持久化能力的基础。
引言
这是一个基于 Anthropic Claude API 的 Agent 框架，用 TypeScript 编写，运
行
在单进程
Node.js 环境中。
本文记录其中四个核心模块的实现：工具系
统（Tool layer）、消息总线（MessageBus）、子
Agent 管 理 （ SubagentManager）、
REPL 主 循 环 。不 涉 及 上 层 Bot 接入层、持 久 化、
Context / Memory 系
统。
框架不依
赖
LangChain 或其他 Agent 框架，直接基于 Anthropic SDK 构建。选
择
路的原因很简单：中间层越薄，调试越容易，对 API
为的控制越精确。
行
这条
基础设施：Tool 抽象与 ToolRegistry
▐ Tool 抽象类
一个工具由四个要素组成：name、description、input_schema、execute。
1
2
3
export abstract class Tool {
abstract readonly name: string;
abstract readonly description: string;
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
4
5
6
7
8
9
10
11
12
13
abstract readonly input
_
schema: AnthropicTool["input
_
schema"];
abstract execute(args: Record<string, unknown>): Promise<unknown>;
toSchema(): AnthropicTool {
return {
name: this.name,
description: this.description,
input
_
schema: this.input
_
schema,
};
}
}
input
_
schema 的 类 型 直 接 取自 @anthropic-ai/sdk 的 Tool 类 型 定义
toSchema() 将实例转换为 Anthropic API 要求的 function calling schema。没有中间层转
换，SDK 类型就是唯一的 schema 定义
。
。
这里
有一个刻意的取舍：schema 使用运
行
时普通对象定义，而非 Zod 等库。好处是零额外
依
赖、直接对齐 SDK 类型。代价是没有
运
行
时参数校验——LLM 传入的参数如果类型不
对，
只能靠 execute 内部的 as 断言和实际调用时的错误来兜底。对于当前规模，这个取舍可
以接受。
▐ ToolRegistry
注册表本身是一个 Map<string, Tool>：
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
export class ToolRegistry {
private tools = new Map<string, Tool>();
register(tool: Tool) {
this.tools.set(tool.name, tool);
}
async execute(name: string, args: Record<string, unknown>) {
const tool = this.tools.get(name);
if (!tool) throw new Error(`Tool "${name}" not found`);
return tool.execute(args);
getToolDefinition(): AnthropicTool[] {
return Array.from(this.tools.values()).map((tool) => tool.toSchema
}
}
exclude(names: string[]): ToolRegistry {
const excludeSet = new Set(names);
const filtered = new ToolRegistry();
for (const [name, tool] of this.tools) {
if (!excludeSet.has(name)) {
filtered.register(tool);
}
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
21
22
23
24
}
return filtered;
}
}
exclude() 是为子 Agent 设 计 的。子 Agent 不 应 该持有
spawn （ 避免 递 归创建子
Agent）、
message （避免直接向用户发消息）等工具，所以需要从主 Agent 的工具集中排
除特定工具，生成一个受限子集。 exclude() 返回新的 ToolRegistry 实例，不
修改原
注册表。
内置工具一览
▐ 文件操作
ReadFileTool — 读取文件内容，动态 import("node:fs/promises") 加载模块。
WriteFileTool — 写入文件。写入前调用 mkdir(dirname(path), { recursive: true }) 自动创建
父目录，避免
因目录不存在而失败。
EditFileTool — 精确文本替换。核心逻辑：
1
2
3
4
5
6
7
8
const occurrences = content.split(oldText).length - 1;
if (occurrences === 0) {
return `Error: old
_
text not found in ${filePath}`
;
}
if (occurrences > 1) {
return `Warning: old
_
text found ${occurrences} times in ${filePath}.
}
const updated = content.replace(oldText, newText);
强制
唯一匹配：出现 0 次报错，超过 1 次拒绝写入并要求提供更精确的文本片段。这个设计是
为了防止 LLM 给出模糊
的替换目标，导致意外修改多处代码。
ListDirTool — 列出目录内容，对每个条目做 stat，用 [folder] 和 [file] 前缀区分类型。
▐ 命令执
行
ExecTool — 执
shell 命令。三层防护：
行
第一层，危险命令正则黑名单：
1 const DANGEROUS
_
PATTERNS: RegExp[] = [
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
2
3
4
5
6
7
8
9
/rm\s+(-[a-zA-Z]*f[a-zA-Z]*\s+)?(-[a-zA-Z]*r[a-zA-Z]*\s+)?\/($|\s)/,
/rm\s+-[a-zA-Z]*rf?\s+~($|\/|\s)/,
/mkfs\b/,
/dd\s+if=/,
/:\(\)\s*\{\s*:\|:\s*&\s*\}\s*;/, // fork bomb
/>\s*\/dev\/[sh]d[a-z]/, // 写入裸设备
/chmod\s+-R\s+777\s+\//,
];
覆盖 rm -rf /、fork bomb、写裸设备等高危模式。需要说明的是，正则黑名单是最低限度的防
线，不能替代沙箱隔离。
第二层，资源限制：默认30 秒超时，2MB maxBuffer。超时后进程被 kill，返回超时提示。
第三层，输出截断
。超过 10,000 字符时取首尾各 5,000 字符，中间用截断标记连接：
1
2
3
4
5
6
7
8
9
function truncateOutput(text: string): string {
if (text.length <= MAX
OUTPUT
_
_
LENGTH) return text;
const half = Math.floor(MAX
OUTPUT
_
_
LENGTH / 2);
return (
text.slice(0, half) +
`\n\n--- truncated (${text.length} chars total) ---\n\n
text.slice(-half)
`
+
);
}
保留首尾而非只取前 N 字符，是因为命令输出的末尾通常包含最有价值的信息（错误信息、统
计摘要等）。
▐ Web 能力
WebSearchTool — 封装 Brave Search API，返回结构化搜
索结果。参数 count 可选，默认 5
条，上限 10 条。
WebFetchTool — 抓取 URL 内容。针对 HTML 页面内置了纯正则实现的 htmlToText 转换：
1
2
3
4
5
6
7
8
9
10
function htmlToText(html: string): string {
return html
.replace(/<script[\s\S]*?<\/script>/gi,
"")
.replace(/<style[\s\S]*?<\/style>/gi,
"")
.replace(/<(br|\/p|\/div|\/li|\/tr|\/h[1-6])[^>]*>/gi,
.replace(/<[^>]+>/g,
"")
// HTML 实体解码...
.replace(/[ \t]+/g,
.replace(/\n{3,}/g,
.trim();
" ")
"\n\n")
"\n")
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
11 }
没有使用 DOM 解析库（如 cheerio、jsdom），纯正则处理。对于大
但对复杂嵌套结构可能丢失语义
。内容超过 20,000 字符时截断
。
多数常规网页足够用，
▐ 通信与调度
MessageTool — 出站方向的消息通道。通过构造时注入的 sendCallback 向外部发送消息：
1
2
3
4
5
6
7
8
9
10
11
12
export class MessageTool extends Tool {
constructor(private sendCallback: SendCallback) {
super();
}
async execute(args: Record<string, unknown>): Promise<string> {
const content = args.content as string;
const channel = (args.channel as string) ?? "repl";
const chatId = (args.chat
_
id as string) ?? "default";
await this.sendCallback({ channel, chatId, content });
return `Message sent to ${channel}:${chatId}`
;
}
}
REPL 场景下sendCallback 就是 console.log；Bot 场景下替换为向 Telegram、Discord 等平台
发送消息的函数。工具本身不
关
心消息最终去向。
CronTool + CronService — 定时任务管理，分为服务层和工具层。
CronService 基于 setInterval 实现，支持两
间隔）和 cron
_
expr（解析 cron 表
种定时方式：every_
seconds（直接转换为毫秒
达式为近似间隔）。
cron 表
达式的解析是简化版本：
1
2
3
4
5
6
7
8
9
10
11
12
13
private parseCronInterval(expr: string): number {
const parts = expr.trim().split(/\s+/);
if (parts.length !== 5) return 60
_
000;
const [minute, hour] = parts;
// */N * * * * → 每 N 分钟
if (minute?.startsWith("*/") && hour === "*") {
const n = parseInt(minute.slice(2), 10);
if (!isNaN(n) && n > 0) return n * 60
_
000;
}
// 0 */N * * * → 每 N 小时
if (minute === "0" && hour?.startsWith("*/")) {
const n = parseInt(hour.slice(2), 10);
if (!isNaN(n) && n > 0) return n * 3600
_
000;
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
14
15
16
17
18
19
}
if (minute === "*" && hour === "*") return 60
if (minute === "0" && hour === "*") return 3600
if (minute === "0" && hour === "0") return 86400
_
000; // 每分钟
_
000; // 每小时
_
000; // 每天
return 60
_
000; // 复杂表
达式
降
级为每分钟
}
只处理 */N、每小时、每天等常见模式。不支持"每周三 14:30"这类精确时间点的 cron 语义
——setInterval 本身也做不到这件事。复杂表
达式静默降
级为每分钟执
一次，这是一个已知
行
的精度妥协。
CronTool 对外暴露 add、list、remove 三个 action，作为 CronService 的 function calling 接
口。
MessageBus：入站消息总线
MessageBus 处理入站方向的消息流——从子系
统或外部流向主 Agent。
1
export class MessageBus {
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
private listeners = new Map<string, Set<MessageHandler>>();
private queue: InboundMessage[] = [];
subscribe(channel: string, handler: MessageHandler): () => void {
if (!this.listeners.has(channel)) {
this.listeners.set(channel, new Set());
}
this.listeners.get(channel)!.add(handler);
return () => { this.listeners.get(channel)?.delete(handler); };
}
async publish(message: InboundMessage): Promise<void> {
const handlers = this.listeners.get(message.channel);
if (handlers && handlers.size > 0) {
for (const handler of handlers) {
await handler(message);
}
} else {
this.queue.push(message);
}
}
drain(channel?: string): InboundMessage[] {
if (!channel) {
const msgs = [...this.queue];
this.queue = [];
return msgs;
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
26
27
28
29
30
31
}
const matched = this.queue.filter((m) => m.channel === channel);
this.queue = this.queue.filter((m) => m.channel !== channel);
return matched;
}
}
数据 结 构 InboundMessage 包 含四个字段： channel （ 消 息 通 道 ）、senderId （ 发送者 标
识）、chatId（关联会话，格式为 originChannel:originChatId）、content（消息内容）。
两
种消费模式：
1. subscribe— 注册实时回调。消息到达时立即调用 handler。适合常驻服务场景。
2. drain— 从队列中
取出并清空消息。适合轮询式的同步消费场景。
路由规则：有订阅者走回调，无订阅者入队列。消息只走一条路径，不会同时触发回调和入
队。
与 MessageTool 的关系需要明确：MessageTool 负责出站（Agent → 外部），MessageBus
负责入站（外部/子系
统 → Agent）。两者没有直接的代码耦合，方向相反
。
SubagentManager：后台子 Agent
▐ 架构
单进程并发模型。每个子 Agent 是一个 Promise，共享同一个 Node.js 事件循环。没有多进程、
没有 Worker。
每个子 Agent 拥有独立的 AgentLoop 实例，有自己的 ReAct 循环，没有历史上下文——每次从
零开始，处理完一个任务就结束。
子 Agent 的工 具 集 是主 Agent 的受 限子 集 。在 index.ts 中通 过 exclude 排 除 了 spawn、
message、edit
file、cron：
_
1 const subagentTools = tools.exclude(["spawn"
,
"message"
,
"edit
file"
_
,
"c
排除 spawn 防止子 Agent 递归创建子 Agent；排除 message 防止子 Agent 直接向用户发消
息（应该通过 MessageBus 回传给主 Agent 处理）；排除 edit
file 限制
_
子 Agent 的写入能
力；排除 cron 避免子 Agent 创建定时任务。
▐ 生命周期
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
1
2
3
4
5
6
7
8
9
10
spawn(params: { task: string; label?: string; ... }): string {
const id =
`
subagent-${++this.counter}`
;
const label = params.label ?? `Task ${this.counter}`
;
const promise = this.runSubagent(id, params.task, label, ...);
promise.finally(() => {
this.runningTasks.delete(id);
});
this.runningTasks.set(id, { id, label, promise });
return id;
}
流程：spawn( ) 分配自增 ID → 启动 runSubagent() 返回 Promise → 立即返回 ID。调用方
需要等待子 Agent 完成。
runSubagent 创建一个独立的 AgentLoop，buildMessages 只传入当前任务，不带历史：
不
1
2
3
buildMessages: (
_
history, userMessage) => [
{ role: "user" as const, content: userMessage },
],
子 Agent 最大迭 代 15 次（ 主 Agent 是 10 次） 。完成 后 通 过 bus.publish( ) 将 结 果 发送
到 system channel：
1
2
3
4
5
6
await this.bus.publish({
channel: "system"
,
senderId: "subagent"
,
chatId: `${originChannel}:${originChatId}`
,
content: `[Subagent "${label}" (${id}) completed]\n\n${result}`
,
});
成功和失败
中自动清理已完成的任务。
都走这条路径，只是 content 不同。promise.finally() 负责从 runningTasks Map
▐ SpawnTool
SpawnTool 是主 Agent 触 发子 Agent 的接口。LLM 通 过 function calling 调用 它， 传
入 task（任务描述）和可选的 label。返回值包含子 Agent ID 和当前运
行
中的子 Agent 数
量，让 LLM 对并发
状态有感知
。
REPL：入口与主循环
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
REPL （ Read-Eval-Print Loop ） 是整 个 Agent 处理后
输出回复，循环往复。
Agent 的终 端 交互入口。用 户 在终 端输
入文 本 ，
▐ 启动流程
index.ts 的初始化按以下顺序执
：
行
1. 创建 Anthropic 客户端和 MessageBus 实例。
2. 注册所有
工具到 ToolRegistry，区分主 Agent 工具集和子 Agent 受限工具集。
3. 初始化 CronService，触发回调通过 bus.publish() 写入 system channel。
4. 创建 SubagentManager，注册 SpawnTool（最后注册，因为依
赖
例）。
5. 构建 ContextBuilder，加载 skills 和 memory。
6. 创建 AgentLoop 实例，使用 readline/promises 启动交互循环。
SubagentManager 实
▐ 并发控制
核心问题：用户输
不能并发
修改。
解决
方式——布尔互斥锁 + 暂存队列：
入和子 Agent 回传结果都会触发 agent.run()，但 history 数组是共享的，
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
let processing = false;
const pendingSubagentResults: InboundMessage[] = [];
async function drainPendingResults(): Promise<void> {
while (pendingSubagentResults.length > 0) {
const msg = pendingSubagentResults.shift()!;
const systemContent = [
"[SYSTEM NOTIFICATION - Subagent Result]"
,
msg.content,
"Please summarize the above subagent result for the user.
].join("\n\n");
const reply = await agent.run(systemContent, history);
history.push({ role: "user"
, content: systemContent });
history.push({ role: "assistant"
, content: reply });
console.log(`\nBot > ${reply}\n
`);
"
,
}
}
async function tryDrainPending(): Promise<void> {
if (processing) return;
processing = true;
try {
await drainPendingResults();
} finally {
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
23
24
25
26
processing = false;
}
rl.prompt();
}
processing 布尔标志充当互斥锁。同一时刻只有一个 agent.run() 在执
行
。子 Agent 结果到达
时先 push 到 pendingSubagentResults 数组。tryDrainPending 只在 !processing 时进入，
避免并发写入 history。
用户输
1
2
3
4
5
6
7
8
9
10
11
12
13
入的处理流程：
rl.on("line"
, async (input) => {
// ...
processing = true;
try {
const reply = await agent.run(trimmed, history);
history.push({ role: "user"
, content: trimmed });
history.push({ role: "assistant"
, content: reply });
await drainPendingResults();
} finally {
processing = false;
}
});
rl.prompt();
用户交互完成后，在 finally 释放锁之前，先调用 drainPendingResults() 处理期间积攒的子
Agent 结果。这保证了子 Agent 结果不会无限滞
后。
▐ 消息订阅
1
2
3
4
bus.subscribe("system"
, (msg) => {
pendingSubagentResults.push(msg);
void tryDrainPending().catch(console.error);
});
system channel 是内部 消 息 的统一入口。子 Agent 完成、CronService 触 发，都通
过 bus.publish() 发送到这个 channel。handler 只做两件事：入队
、尝试消费。
每条子 Agent 结果被包装为 [SYSTEM NOTIFICATION] 格式注入 history，由主 Agent 总结
后
输出给用户。
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ MessageTool 的接
线
REPL 场景下，sendCallback 直接
输出到终端：
1
2
3
4
5
tools.register(
new MessageTool((msg) => {
console.log(`\n[Message → ${msg.channel}:${msg.chatId}] ${msg.conte
}),
);
如果 切 换到 数。工具系
Bot 场 景， 只 需 要 替 换这个回调为向 统和 Agent 逻辑不需要
任何改动。
Telegram、Discord 等 平 台 发送 消 息 的函
模块协作全景
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
终端 stdin
│
▼
REPL 主循环 (index.ts)
│ ┌──────────────────────── history (共享，互斥访问)
│ │
▼ ▼
AgentLoop.run() ──→ Tool 调用
│ ├── 文件/命令/网络工具 → 直接返回结果
│ ├── SpawnTool → SubagentManager.spawn()
│ │ └── 子 AgentLoop (独立 ReAct)
│ │ └── bus.publish("system
│ ├── MessageTool → sendCallback → stdout
│ └── CronTool → CronService
│ └── setInterval → bus.publish(
│
│ ◄── bus.subscribe("system") ◄── pendingSubagentResults 队列
│
▼
stdout 输出
数据流有两条主线：
同步路径：用户输
stdout。这是标准的 ReAct 循环。
入 → REPL → agent.run() → 工具调用 → 结果回传模型 → 最终回复 →
```

## PDF 第12页

[查看原页](RAW.pdf#page=12)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
异 步 路 径 ： SpawnTool / CronService → bus.publish("system") → handler 入 队
→ tryDrainPending() → agent.run() 处 理系
统 通知 → stdout。异 步 结 果 通 过 MessageBus
汇入主循环，由互斥锁保证不与同步路径冲突。
设计选
与局限
择
零框架依
。不依
赖
赖
LangChain 等 Agent 框架，直接基于 Anthropic SDK 构建。好处是完
全
控制 API 交互细节，调试时不需要穿透框架抽象层。代价是部分基础能力需要自己实现。
schema 定义
方式。运
时对象而非 Zod / JSON Schema 库。降
低了复杂度和依
行
赖数量，但
缺乏运
行
时校验。如果 LLM 传入了格式错误的参数，错误只能在执
阶段暴露。
行
子 Agent 无 持 久 记 忆 。 每次 spawn 从 零 开 始 ， 适 合一次性的并
行
算）。不适合需要跨任务积累上下文的场景。
任 务 （搜
索、分 析、计
CronService 的 cron 表
达式。近似实现，只支持常见的等间隔模式。复杂表
为每分钟执
行
，不会报错。如果需要精确的 cron 语义，应该引入 cron 解析库。
达式会静默降
级
MessageBus 无持久化。纯内存队列，进程重启
场景如果需要消息可靠性，需要接入持久化存储。
后队列消息丢失。对于 REPL 场景足够，Bot
ExecTool 安全
边界。正则黑名单只是最低防线
。LLM 可以通过变量展
方式绕过正则检测。生产环境应该使用容器沙箱或受限用户执
。
行
开
、别名、管道组合等
REPL 并发模型。布尔锁在单用户场景下足够。Node.js 的
线程模型保证了 processing 标
志不会出现竞态。但如果扩展到多用户（如 Bot 同时处理多个会话），需要每个会话独立的
history 和更完整的队列/锁机制
。
单
总结
这个框架的核心设计可以概括为四个部分：
1. Tool 抽象 + Registry 模式— 统一的工具注册和调用接口，通过 exclude() 实现能力隔离。
— 出站走 sendCallback（MessageTool），入站走 MessageBus，方向明
2. 双通道消息机制
确，互不耦合。
3. Promise 并发
果。
的子 Agent— 共享事件循环，独立 ReAct 循环，通过 MessageBus 回传结
4. 互斥锁驱动的 REPL 主循环— 布尔标志 + 暂存队列，保证 history 的一致性。
这些模块组合成一个可扩展的 Agent 运
行
（REPL → Bot）只需替换 sendCallback 和输
时。扩展新工具只需继承 Tool 并注册。切换接入层
入源。子 Agent 的能力边界通过 exclude() 控
制
。
```

## PDF 第13页

[查看原页](RAW.pdf#page=13)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
团队介绍
本文作者苏雄，来自淘天集团-会员技术团队。业务上，我们负责 88VIP、天猫积分、省钱
卡、大会员
、消费券等淘宝核心业务，同时支撑淘宝、
千问、闪购等阿里业务的账号互联互
通。技术上，我们深耕 AI 与业务融
合，为消费者带来全
新体验，为业务创造新增量。
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
大淘宝技术
大淘宝技术官方账号
967篇原创内容
公众号
阅读 5155
留言
写留言
还没有
留言，来写首评
```

## PDF 第14页

[查看原页](RAW.pdf#page=14)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text

```
