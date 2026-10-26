# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
打造 Jarvis ， OpenClaw 很野，但 Agent  Studio 简直变态
腾讯程序员 2026 年 1 ⽉ 30 ⽇ 01 : 08⼴东原创 腾讯技术⼯程 990 ⼈
作者：kong
前⾔：每个⼈都想要⼀个  Jarvis
还记得《钢铁侠》⾥的  Jarvis 吗？⼀个随时在线、⽆所不能的  AI 助⼿ —— 它能帮你处理⼯作、
管理项⽬、分析数据、甚⾄还能和你闲聊⼏句。这不就是我们⼀直梦想的终极  AI 助⼿吗？
在  AI Agent 领域，有不少项⽬都在朝着这个⽅向努⼒。⽐如  OpenClaw （原名 clawdbot ），它
确实很 " 野 "—— 把  AI Agent 和  WhatsApp 、 Telegram 、 Discord 等消息应⽤打通，让你能在⼿机
上随时随地和  AI 对话。听起来很酷对吧？
但今天我要给你介绍⼀个更加 " 丧⼼病狂 " 的⽅案：Agent Studio。
实际上，在企业微信上招呼  AI ⼲活，已经是我的⽇常，在通勤路上，吃饭时间等⼏乎全天候在
与  AI 协同，全拜 Agent Studio ⽀撑。
场景对⽐：从⼿机访问你的  AI Agent
OpenClaw （原名 clawdbot ） 的⽅案
OpenClaw （原名 clawdbot ）的核⼼思路是：通过消息应⽤⽹关来访问  AI Agent 。
它⽀持多个平台：
📱  WhatsApp ( 通过  Baileys 协议 )
⼁  导语  OpenClaw （原名 clawdbot ）突然就⽕了，了解后发现多终端协同的⼈机协同⽅式
的 jarvis 正是⾃⼰的⽇常⼯作⽅式！在此之前，为了⽅便⾃⼰⽤  AI ，我基于  claude agent
sdk ⼿搓了⼀整套⼯具链，打造⾃⼰的  Jarvis ， IM 接⼊功能算是基操了。  本⽂带⼤家快速体
验⼀下  Agent Studio 在企业微信快速接⼊过程。
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
✈  Telegram (Bot API)
🎮  Discord (Bot API)
💬  iMessage ( 通过  imsg CLI)
🧩  Mattermost ( 插件⽅式 )
还有  Slack 、 Signal 、 MS Teams 、 Line 、 Matrix 等
作为⼀个成熟的开源项⽬（ 102k stars ），OpenClaw （原名 clawdbot ）  提供了强⼤的能⼒：
✅  功能完整： 100+ CLI 命令、 Cron 定时任务、多  Agent 路由、 WebSocket Gateway
✅  架构成熟：完整的协议设计、沙盒执⾏、⼯具系统
✅  平台⼴泛：⽀持  9+ 个主流消息平台
✅  社区活跃：⽂档完善，问题能得到快速响应
但它的定位是：为开发者提供⼀个强⼤、灵活的⼯具箱，适合技术团队搭建⾃⼰的  Agent 基础设
施。
这意味着：如果你有技术背景，愿意学习  CLI 配置，需要⽀持多个  IM 平台，OpenClaw （原名
clawdbot ）  是⾮常好的选择。
Agent Studio 的⽅案：企业微信⼀键接⼊
Agent Studio 的核⼼定位是：打造⼀套完整的个⼈  Agent ⼯作台。在众多功能中，IM 接⼊是⼀
个重要特性 —— ⽬前已接⼊企业微信机器⼈，钉钉、飞书、 discord 、 slack 等更多  IM 渠道已在
路上。
下⾯以企业微信机器⼈（腾讯内部版）为例，展⽰  Agent Studio 的  IM 接⼊体验，说明  Agent 如
何快速接⼊现有沟通⼯具并完成实际对话交互，帮助快速理解  Agent 从接⼊到使⽤的整体流程
（这⾥更多是基于实践总结的接⼊思路⽰例，重点在于⽅法和路径的启发，具体实现可根据各⾃
环境灵活调整）
Agent Studio 接⼊企微的完整流程（只需  5 分钟）
Step 1: 安装  Agent Studio
npm install -g agentstudio
agentstudio start
访问  http://localhost:4936/
如果你是  claude code 的⽤户，你会  0 门槛继续，跳过下⾯模型供应商设置这⼀步。
如 果 还 不是  claude code ⽤ 户 ，需 要 你 到：
https://localhost:4936/settings/suppliers 这⾥配置⼀个模型的供应商并把它设置
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
为默认供应商，才可以继续。除  claude 模型外，还⽀持  GLM 、 Minimax, Kimi, Deepseek 等国
产模型。
在进⼊下⼀步之前，最好先在  web 页⾯上（⾸页或项⽬管理点击⼀个项⽬进去），发个消息
agent ⼯作正常了：
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
Step 2: 启⽤隧道（让企微机器⼈可以调⽤你本地的  Agent ）
注：如果你部署在  devCloud 上，或者有固定的  IP ，是不需要隧道的。
访问  http://localhost:4936/settings/tunnel，使⽤  Tunely (WebSocket)  隧道，该
服务部署在司内⽤于连接企微和本地  Agent ，数据不出外⽹，不担⼼：  
1 . 点击  "Tunely (WebSocket)" 标签
2 . 配置隧道名称和服务器地址
3 . 点击  " 连接 "  按钮
4 . 连接成功后会显⽰隧道地址（如  https://kongjie.tunnel）
想要部署⾃⼰的隧道服务的可以联系我要⽅法。
Step 3: 进⼊项⽬管理，配置  IM 接⼊
1 . 访问  http://localhost:4936/projects
2 . 进⼊  " 项⽬管理 "
3 . 选择要接⼊的项⽬，点击  "A2A Protocol 管理 ", 倒数第三个图标
4 . 切换到  "IM 接⼊ " 标签
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
5 . 点击  " ⽣成接⼊命令 "，系统会⾃动：
✅  创建安全的  API 密钥
✅  检测⽹络状态（隧道或本地⽹络）
✅  ⽣成完整的企微机器⼈接⼊命令，形如  /ap my-project
http://kongjie.tunnel/a2a/xxxx-agent-id/messages --api-key your-
key
6 . 复制⽣成的命令
如果没有配置隧道，这⾥的  kongjie.tunnel 会使⽤所在机器的  IP 要址，同样的也可以⼯作的。但
如果下次地址换了，就得重新绑定了。
Step 4: 加⼊群聊，开始使⽤
1. 把  agent studio 加⼊你的企微群⾥
2. 在群⾥的推送通知中找到  "agent studio"  机器⼈，私聊它！
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
3. 发送刚才复制的命令，将项⽬添加到企微中
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
4. 机器⼈会回复确认信息，项⽬添加成功
5. 现在你可以直接和机器⼈对话，使⽤你的本地  Agent 了！
使⽤ /use 项⽬名  开始和 Agent 聊， /use 也可以⽤来切换不同的项⽬。
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
从此：
📱  在⼿机上随时向本地  Agent 发送任务
💻  Agent 在你的电脑上执⾏，结果通过企微返回
📊  ⽀持⽂件、代码、数据分析等各种⼯作场景
🔒  数据完全本地，不上传云端
对于 " 快速接⼊企微 " 这个场景：
配置体验： Agent Studio 图形化配置， 5 分钟完成；OpenClaw （原名 clawdbot ）需要通过
CLI 配置
企微集成深度： Agent Studio 专门优化了企微接⼊流程；OpenClaw （原名 clawdbot ）需要
⼿动配置  Channel
适合场景： Agent Studio 适合个⼈快速搭建；OpenClaw （原名 clawdbot ）适合团队⾃定义
部署
⽽且，对于腾讯内部或使⽤企业微信的团队，这个深度集成的体验是  Agent Studio 的⼀⼤亮点
—— 你不需要切换到  WhatsApp 或  Telegram ，就在⽇常⼯作的企微⾥，随时呼叫你的  AI 助⼿。
Agent Studio ：不⽌是  IM 接⼊
如果你以为  Agent Studio 只是  IM 接⼊那就太⼩看它了。这是⼀个  完整的本地  Agent ⼯作台。
⼀⾏命令，⽴即启动
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
npm install -g agentstudio && agentstudio start
访问  http://localhost:4936，你会看到⼀个完整的  Web ⼯作台：
🎨  现代化界⾯：精⼼设计的专业  UI
📁  ⽂件浏览器：对话的同时可以直接查看项⽬⽂件
🔍  可视化⼯具执⾏： AI 调⽤了什么⼯具、传了什么参数、返回了什么结果，⼀⽬了然
📊  项⽬管理：多项⽬⽀持，每个项⽬独⽴配置、独⽴记忆
四⼤核⼼功能：让  Agent Studio 成为真正的  Jarvis
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
1. 定时任务：让  AI 按计划⾃动⼯作
这是  Agent Studio 最 " 丧⼼病狂 " 的功能之⼀ ——让  AI Agent 按计划⾃动执⾏任务。  
你可以配置：
📊  每天早上  9 点，⾃动⽣成项⽬进度⽇报
🔍  每  2 ⼩时，检查代码仓库并提交审查意见
📝  每周五，⾃动整理本周会议纪要并归档
📈  每⽉  1 号，⾃动⽣成业务数据分析报告
⽀持的调度规则：
Cron 表达式  (0 22 * * *)
简单表达式  (每  30 分钟)
⼀次性任务  (2026/1/8 02:00:00)
执⾏历史和监控：
查看每次执⾏的成功 / 失败状态
查看执⾏⽇志和结果
⼿动触发⽴即执⾏
启⽤ / 暂停任务
这不就是  Jarvis 该做的事吗？你只需要设定好规则，它就会在后台默默⼯作，完全不需要你操
⼼。
2. ⾃定义  Agent ：打造专属的  AI 助⼿
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
Agent Studio 基于  Claude Agent SDK  构建，这意味着你不仅可以使⽤平台内置的  Claude
Code  作为默认  Agent ，还可以根据实际需求场景，全新定义属于⾃⼰的专属  Agent 。  
 ⾃定义能⼒包括：
🎯  定制系统提⽰词：为不同场景编写专门的  Agent ⼈格和能⼒描述
🔧  配置专属⼯具：为  Agent 添加特定领域的⼯具和  MCP 服务
🎨  定制  UI 组件：为特定任务设计专属的交互界⾯
📦  预设配置模板：快速创建常见类型的  Agent （如代码审查、⽂档写作、数据分析等）
基于  Claude Agent SDK 的优势：
✅  开箱即⽤：继承  Claude Code 的所有能⼒
✅  标准化接⼝：使⽤  Anthropic 官⽅  SDK ，升级⽆忧
✅  流式响应：原⽣⽀持流式输出，体验流畅
✅  ⼯具调⽤：完整的  Tool Use ⽀持，扩展性强
这就是  Agent Studio 的核⼼理念：不是给你⼀个固定的  AI 助⼿，⽽是给你⼀个可以打造任意  AI
助⼿的平台。
3. A2A 协议：多  Agent 协作⽹络
Agent Studio ⽀持  Agent-to-Agent (A2A) 协议，这不仅是⼀个通信协议，更是  Agent Studio 的
核⼼价值之⼀。
核⼼价值：统⼀的协同调度层
A2A 协议提供了⼀个统⼀的⽹关层，让不同来源、不同位置的  Agent 可以互相协作：
🔗  对内：平台内不同项⽬的  Agent 可以互相调⽤
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
🌐  对外：可以接⼊外部  Agent 服务（如远程开发机、云端服务）
📱  对  IM：作为  IM 渠道接⼊的统⼀⽹关（企业微信、钉钉等）
这个统⼀的协同层带来了强⼤的灵活性：
场景  1 ：秘书  Agent 模式
设置⼀个统⼀的秘书  Agent 接收所有任务
秘书根据任务类型，⾃动调度到对应的专属  Agent
你只需要和⼀个⼊⼝对话，背后是多个专业  Agent 协同⼯作
场景  2 ：分布式  Agent ⽹络
本地  Mac 上的  Agent ↔  远程  Linux 开发机上的  Agent
开发环境  Agent ↔  ⽣产环境  Agent
形成跨设备、跨环境的  Agent 协作⽹络
场景  3 ： IM 统⼀接⼊
企业微信、钉钉等  IM ⼯具通过  A2A ⽹关访问本地  Agent
你在⼿机上发消息  →  A2A 路由到本地  Agent →  执⾏任务  →  结果返回⼿机
数据完全本地，不上传云端
4. MCP Admin ： Agent Studio 的元操作能⼒
这是最 " ⿊科技 " 的功能 ——让  AI Agent 管理  Agent Studio 本⾝。
Agent Studio 提供了⼀个特殊的  MCP 服务：agentstudio-admin，包含  22 个管理⼯具：
list_projects get_project register_project / update_project
list_agents get_agent create_agent / update_agent
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
list_mcp_servers get_mcp_server add_mcp_server
list_scheduled_tasks / create_scheduled_task
... 等等
当你把这个  MCP ⼯具挂载到  Jarvis Agent 上时，会发⽣什么？
你的  AI Agent 可以⾃⼰管理  Agent Studio ！
举⼏个例⼦：
场景  1 ：动态创建项⽬
场景  2 ：⾃动配置定时任务
场景  3 ：智能  Agent 管理
这意味着：
🤖  Agent 可以⾃我管理：根据需要动态创建项⽬、 Agent 、任务
🧠  智能化配置：不需要你⼿动点界⾯， AI ⾃⼰完成配置
🚀  ⼯作流⾃动化：⼀句话描述需求， AI ⾃动完成所有配置
这就是真正的元操作能⼒—— 不仅是  AI 帮你做事，⽽是  AI 帮你管理  AI ⼯作台本⾝。
Agent Studio vs OpenClaw （原名 clawdbot ）：客观对⽐
先说在前⾯：OpenClaw （原名 clawdbot ）是⼀个成熟、强⼤的项⽬（ GitHub 102k stars ），它
提供了完整的⼯具箱，⽀持  9+ 个消息平台（ WhatsApp 、 Telegram 、 Discord 、 Slack 、 Signal 、
MS Teams 、 iMessage 等），拥有强⼤的  CLI 系统（ 100+ 命令）和成熟的  WebSocket Gateway
架构。
你： "Jarvis ，帮我创建⼀个新项⽬叫  my-blog ，路径是  ~/projects/my-blog" Jarvis ：调
⽤  register_project  ⼯具，⾃动创建项⽬并配置  Agent
你： "Jarvis ，每天晚上  10 点帮我总结今天的  Git 提交记录 " Jarvis ：调
⽤  create_scheduled_task  ⼯具，⾃动创建定时任务
你： "Jarvis ，创建⼀个专门处理  Python 代码的  Agent" Jarvis ：调⽤  create_agent  ⼯具，
配置合适的系统提⽰词和⼯具
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
Agent Studio 不是  OpenClaw（原名 clawdbot ）的替代品，⽽是差异化的选择—— 它更聚焦于
本地⼯作台和个⼈  Jarvis 场景。
维度 Agent Studio OpenClaw
核⼼定位 本地  Agent ⼯作台 全能消息平台⽹关
技术基础 Claude Agent SDK ⾃建  Agent 运⾏时
安装配置 ⼀⾏命令，图形化配置CLI 配置，灵活但需学习
界⾯ Web UI 为主 CLI 为主，可选  Web UI
⽬标⽤户 个⼈、⼩团队 开发者、技术团队
IM  平台 企业微信（已接⼊），更多渠道
开发中
9+ 平台（ WhatsApp 、 Telegram 、 Disco
rd 等）
定时任务 图形化配置，可视化管理Cron + CLI 配置
⾃定义 Age
nt ✅  图形化创建，基于  SDK ⚠  配置⽂件  + 模板
A2A  协议 ✅  统⼀⽹关  + IM 接⼊ ⚠  多  Agent 路由
MCP  Admi
n ✅  元操作能⼒ ❌
数据隐私 ✅  完全本地 ✅  完全本地
选择建议：
选  OpenClaw （原名 clawdbot ）：需要⽀持多个  IM 平台、团队协作、成熟度优先、愿意学习
CLI
选  Agent Studio：快速搭建个⼈  Jarvis 、图形化配置、基于  Claude SDK 的扩展性、企业微
信深度集成（更多  IM 渠道开发中）
⽴即开始
安装
npm install -g agentstudioagentstudio start
````

## PDF 第 17 页

[原页](RAW.pdf#page=17)

````text
访问
打开浏览器，访问：http://localhost:4936
安装为系统服务
使⽤  install 命令安装为系统服务，⽆需⼿动维护终端窗⼝，让  Agent 随系统启动。
agentstudio install
摊牌了：这是我的  Jarvis
说实话，Agent Studio 就是我在打造⾃⼰的  Jarvis 时顺便产品化的⼩玩具。
作为⼀个⼯程师，我深刻体会到：在这个  AI 时代，每个⼈都需要、并且有机会打造⾃⼰趁⼿的
Agent ⼯作台。⽽在  AI Coding 的加持下，这个成本已经低到令⼈难以置信。
我的建议是：拿起  AI ，和  AI ⼀起合作，尝试打磨更适合⾃⼰的  Agent ⼯作台。
不要等待完美的产品出现，因为只有你最了解⾃⼰的需求：
也许你需要⼀个专门处理财务报表的  Agent
也许你需要⼀个能⾃动整理会议纪要的助⼿
也许你需要⼀个能帮你写代码、审代码、部署代码的⼯程师
好消息是： Agent Studio 所有代码开源（ GPL v3 ）  : https://github.com/okguitar/agentstudio
如果你有兴趣⾃⼰部署企微服务、其他  IM 的渠道和⾃⼰的隧道服务，可以进⼀步了解技术细
节。https://github.com/jeﬀkit/as-dispatch/tree/feature/im-integration
你可以基于它改造出更适合⾃⼰的版本，也可以从零开始，⽤  AI 帮你写代码，快速搭建起⾃⼰
的  Jarvis 。
这不是科幻，这是现实。⽽且⽐你想象的要简单得多。
Agent studio 本是个⼈⾃搓⾃⽤的⼯具，难免有不完美，有问题 /bug 可以欢迎评论区讨论，也欢
迎⼀起完善它。
````

## PDF 第 18 页

[原页](RAW.pdf#page=18)

````text
阅读 1 . 5 万
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
留⾔ 8
Feng  Yu /g0 … 北京1 ⽉ 30 ⽇
腾讯技术⼯程作者1 ⽉ 30 ⽇
⽞殇宁 湖北1 ⽉ 30 ⽇
⾸评
写留⾔
8
⼜改名了？
3
是的
7
咋⼜改名了。 clawdbot 到 moltbot 。到 openclaw
````

## PDF 第 19 页

[原页](RAW.pdf#page=19)

````text
我是谁上海1 ⽉ 30 ⽇
jeff  kit⼴东1 ⽉ 30 ⽇
亮⼀⼀格物… 湖北1 ⽉ 30 ⽇
jeff  kit⼴东1 ⽉ 30 ⽇
北北 - 对企… ⼭⻄1 ⽉ 30 ⽇
1
Agent  studio  ⽀持操作浏览器不
4
⽀持 playwright  mcp 操作浏览器
不是企业微信的个⼈⽤户怎么办
2
其他渠道⻅⽂中链接
太震撼了！可以接 n1n . ai 的⼤模型接⼝就好了
````

