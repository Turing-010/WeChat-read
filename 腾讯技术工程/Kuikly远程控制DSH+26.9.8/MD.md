# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
我⽤腾讯 Kuikly ，把 DeepSeek  Harness 装进了⼝袋
腾讯程序员 Sep  8 , 2026 , 2 : 57  AM⼴东原创 腾讯技术⼯程 1231  listened
作者：腾讯程序员 yuki
DeepSeek Harness 跑⼀个任务，经常要⼏分钟甚⾄更久。中间它还会停下来等⼈处理审
批、补充信息或确认⽅向。只要⼈离开电脑，这⼀轮任务就可能卡在原地。
我想解决的不是「在⼿机上写代码」，⽽是让⼿机接住这些短⽽频繁的交互。通勤、开会或
排队时，可以看⼀眼任务进度，处理⼀次审批，回答  Agent 的追问，再让电脑继续跑。
于是我⽤  Kuikly 做了  DSH Mobile 。⼀套  Kotlin 代码覆盖  Android 、 iOS 和鸿蒙，按照
DSH 官⽅  Host 协议连接电脑上的  Harness 。 Agent 循环、⼯具执⾏和插件仍在电脑上运
⾏，⼿机负责连接、交互和渲染。
最省事的⽅案当然是套⼀层  WebView ，但这个  App 不只是把⽹⻚缩进⼿机。它要维持
WebSocket ⻓连接，处理锁屏、切后台和⽹络切换，还要在重连后补回遗漏事件。扫码、
SSH 隧道和本地缓存也都需要平台能⼒。做到这⾥，原⽣客户端反⽽更合适。
DSH App ⻚⾯功能演示：
DSH  这么好玩，但是只能在电脑上玩太可惜了，于是我⽤ Kuikly  框架做了⼀个 APP ，⼀码三
端的跨端原⽣ app ，按官⽅ Host  协议跟电脑上的 DeepSeek  Harness  对话。
00 : 4600 : 46
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
为什么使⽤  Kuikly
这个项⽬对跨端框架的要求并不抽象。
聊天正⽂是持续变化的  Markdown ，模型每吐出⼀个  chunk ，⻚⾯都要跟着刷新。⼯具调
⽤、审批卡、提问卡和后台任务会同时更新。底层还有  HTTP RPC 、两条  WebSocket 事件
流、扫码配对、 SSH 隧道和本地存储。三端不仅要⻓得接近，连接和恢复⾏为也要⼀致。
我选择  Kuikly ，最直接的原因是开发快。组件市场⾥已经有不少常⽤能⼒，找到合适的组
件，加上依赖就能在共享代码⾥使⽤，不需要先给  Android 、 iOS 、鸿蒙分别写⼀套。
Kuikly 的  AI 开发配套也⽐较实⽤。我在这个项⽬⾥⽤了  KuiklyUI-AI，它提供  Kuikly DSL
和  Kuikly Compose DSL 的开发规则，也提供组件使⽤、 Module 扩展、⽹络请求、响应式
状态、协程和多端资源等  Skills 。这些规则可以交给  CodeBuddy 、Cursor、 Claude
Code 等  AI 编程⼯具使⽤。 Agent 写⻚⾯、接组件或补原⽣桥接时，不⽤临时猜  Kuikly 的
API 和⼯程约定，⽣成的代码更容易直接落进项⽬。协议模型 、状态机和重复⻚⾯可以先
交给  Agent 完成，我主要检查交互、平台差异和真机表现。
组件市场： Markdown 和  WebView 快速接⼊
DSH Mobile ⾥直接⽤了两个现成组件KuiklyMarkdown  和  KuiklyWebview。
implementation("com.tencent.kuiklybase:KuiklyMarkdown:1.0.6-2.1.21")
implementation("com.tencent.kuiklybase:KuiklyWebview:1.0.1-2.0.21")
KuiklyMarkdown 省掉的⼯作最多。 AI 对话⾥的  Markdown 不是解析⼀次就结束，模型输
出⼀直在变，代码块、列表、引⽤和链接都要跟着刷新。如果从零开始做，需要先找⼀套三
端可⽤的解析器，再写  AST 到  UI 的映射，处理代码⾼亮、主题、列表缩进和流式更新。
KuiklyMarkdown 已经把这套⻣架做好了。它基于  intellij-markdown 解析⽂本，输出
Block 列表，并提供流式渲染状态。接⼊以后，我主要处理  DSH ⾃⼰的产品逻辑。已经结
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
束的  Block 保持不动，尾部内容继续更新；代码块暂时没有闭合时，在解析副本⾥补上闭合
标记；⻚⾯更新按  16 ms 合帧，避免每来⼀个⼩  chunk 就刷新⼀次。
这样⼀来，项⽬不需要⾃⼰维护  Markdown 语法解析、代码块渲染和三端基础样式，只需要
把精⼒放在流式场景上。⻓回答前半部分稳定后不会反复重建，尾部还能继续跟着模型输出
刷新。
KuiklyWebview  ⽤在  Markdown 链接和外部⻚⾯的  App 内打开。共享⻚⾯⾥直接放⼀个
WebView ，设置  URL ，再监听开始加载、进度、完成和失败事件就够了。刷新和返回逻辑
也写在同⼀份  Kotlin 中。没有这个组件，就要分别封装  Android WebView 、 iOS
WKWebView 和鸿蒙  Web 组件，再把事件桥接回共享层。
组件市场⾥还有  SQLite 、相机、图⽚选择、录⾳、定位、蓝⽛和  MMKV 等常⽤能⼒。这个
项⽬没有把它们全部接进来，但开发新功能时可以先找现成组件。对跨端项⽬来说，少写的
不是⼀个控件，⽽是同⼀项基础能⼒在三个平台上的接⼊、对⻬和后续维护。
原⽣桥接能⼒：差异下沉，共享层保持业务统⼀
跨端项⽬真正费时间的地⽅，通常不是⻚⾯，⽽是  WebSocket 、扫码、 SSH 和数据库这类
系统能⼒。
DSH Mobile 在  commonMain  定义统⼀的  Module 接⼝，把连接、发消息、收消息和断开
等业务语义固定下来。 Android 、 iOS 、鸿蒙分别接⾃⼰的系统实现。
拿  WebSocket 举例，三端底层分别是  OkHttp、NSURLSession、NetworkKit，但上层
⻚⾯只⾯对同⼀个  DshWebSocketModule。平台差异被收敛在最底层，聊天⻚、事件处
理、业务状态都不需要知道⾃⼰在哪个系统上。 SSH 隧道、扫码配对是同⼀套拆法。
这层下沉的收益会随协议变化放⼤， DSH 还没有完全稳定下来，往后每多⼀个  RPC 、改⼀
个事件，只需改共享层，三端⼀起⽣效，这⽐到时候再维护三个壳便宜得多。
⽬前项⽬约有  1.3 万⾏  commonMain Kotlin 代码由三端共享。 Android 、 iOS 、鸿蒙宿主各
有三四千⾏，主要⽤于接⼊系统能⼒和完成平台⼯程配置。组件能直接复⽤，协议和状态⼜
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
留在共享层，不⽤把相同功能在三个⼯程⾥各做⼀遍。
Kuikly 在三端同⼀⻚⾯的表现：
安卓、 iOS 、鸿蒙三端 UI 对⽐⻚⾯
不加中间层，直接接  Host 协议
DSH Mobile 没有在⼿机和电脑之间再放⼀套业务服务。它直接使⽤官⽅  Web 前端背后的
Host 协议。浏览器如何调⽤  DSH ， App 就沿⽤同⼀套⽅法和事件。
DSH 本身是基于  Cordis 的插件化  Agent 运⾏时。与移动端连接直接相关的部分可以简化
成三层。core/session、agent-loop  和  tools 负责会话、 Agent 循环与⼯具执⾏，
并产⽣相应事件。host/apiproxy  把内部能⼒整理成  RPC ⽅法表和两条下⾏事件流。
client/connection 再把这些接⼝接到本机的  3080 端⼝，对外提供
HTTP /api/...、 WebSocket /api/events.mux  和  /api/events.host。
电脑上的  Agent 继续读写⼯作区、调⽤⼯具和运⾏插件。 App 只连接最外层
的  client/connection，不需要理解或重新翻译  DSH 内部的插件结构。
发消息就是⼀次  HTTP RPC
DSH 把可调⽤能⼒登记在⼀张  RPC ⽅法表⾥。以  dsh-v0.1.1-rc.2  为例，表中有  52 个
⽅法。发送消息对应  session.prompt，请求路径是  POST /api/session.prompt。会
话列表、历史记录、⼯作区、模型、 Goal 和设置也都⾛同⼀条  RPC 通道。
⽅法的⼊参和返回值来⾃  TypeScript 函数签名，注册表负责把⽅法名映射到实际实现。
DSH Mobile 只实现当前需要的部分，没有为移动端另造⼀套接⼝。
完整⽅法表可以直接看  rpc-map.ts。 52 这个数字只对应⽂中使⽤的版本。 DSH 仍在快速迭
代，接⼊时最好锁定已经验证过的  tag ，不要默认  master 始终兼容。
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
两条  WebSocket ，各管⼀类状态
远程连接建⽴后， Host 会通过两条只下⾏的  WebSocket 向  App 推送事件。
/api/events.mux 负责当前会话中正在发⽣的事，包括模型输出、⼯具调⽤、审批、提
问、消息队列和后台任务。
/api/events.host 负责电脑这⼀侧的全局变化，包括会话增删、运⾏状态、⼯作区变更
和  Host 级错误。
两条流分开以后，会话正⽂和全局状态不会挤在同⼀个通道。 App 也可以按不同的⽣命周期
处理它们。聊天⻚⾯主要消费  mux ，⼯作区和会话列表更多依赖  host 。
有两个细节需要单独处理。
session/queue  和  session/jobs  推送的是完整快照，不是「⼜增加了⼀条」的增量事
件。它们不进⼊会话⽇志，重连时也不能只靠事件回放恢复，所以  App 收到新快照后会直接
覆盖本地状态。
session/projection.value  和  host/remote-event.args  在  carrier 层是宽类型。它
们的结构由各⾃业务包负责， App 不能假设所有帧都严格符合固定  data class 。这⾥需要保
留未知字段，并在解析失败时降级，⽽不是让整条事件流⼀起中断。
断线以后，先补事件，再对历史
移动⽹络⼀定会断。锁屏、切后台、进隧道、 Wi-Fi 与蜂窝⽹络切换都可能让连接失效。
DSH Mobile 重连后按下⾯的顺序恢复。
1. 重新建⽴  SSH 或  Relay 隧道。
2. 使⽤上次收到的序号补回遗漏的  session/event。
3. 请求⼀次  session.history，重新对⻬聊天记录。
4. 使⽤最新快照覆盖  queue 和  jobs 。
每次连接还带⼀个世代号。连接断开后，旧连接中迟到的  RPC 响应会被丢弃，不能再写进
新的会话状态。
如果  Agent 在断线期间仍在电脑上运⾏， App 重连后会重新订阅这⼀轮任务，⽽不是把⽤
户的  Prompt 再发⼀次。这个区别很重要。重连是恢复观察和控制，不是重新执⾏任务。
状态机位于共享层，因此三端采⽤同样的补⻬顺序和失效规则。平台代码只负责把底层连接
事件交给共享层。
DSH Mobile 的两种远程连接⽅式
DSH 默认监听  127.0.0.1:3080。这是应该保留的默认值，因为能访问这个端⼝的客户
端，可能通过  Agent 和⼯具获得很⾼的本机操作权限。 DSH Mobile 没有直接把  3080 开到
公⽹，⽽是提供  SSH 和扫码  Relay 两种连接⽅式。
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
有  SSH 就直接打隧道
SSH 模式在⼿机上建⽴本地端⼝转发，把  App 侧的⼀个  loopback 端⼝映射到电脑
的  127.0.0.1:3080。 HTTP RPC 和两条  WebSocket 都通过这条隧道传输。
这种⽅式没有改变  DSH 的认证逻辑。认证发⽣在  SSH 层， DSH 仍然只看到来⾃本机回环
的请求。已经有  SSH 主机和密钥配置时，这条路径最直接。
不想配  SSH ，扫个码也能连
⼿动填写地址、端⼝和密钥不适合普通移动端操作，所以我另外做了  dsh-scan-remote  插
件。
插件安装后， DSH Settings 中会出现  Remote Access ⻚⾯。电脑⽣成⼆维码，⼿机扫描
后完成配对。电脑端插件和  App 都主动连接  Relay ，再通过  sealed-tunnel-v1  转发
DSH 流量。
连接时， DSH 仍然只监听电脑上的  127.0.0.1:3080。 Host 插件从本机访问  DSH ，并主
动连接  Relay ；⼿机  App 也主动连接同⼀个  Relay 。两端完成配对后， App 发出的  HTTP
和  WebSocket 流量会经过密封隧道转发到  Host 插件，再由插件送到本机的  DSH 。整个过
程中， Relay 不需要直接访问  3080 端⼝，电脑也不需要把  DSH 服务开放到局域⽹或公
⽹。
⼆维码中的主密钥位于  URL fragment 中，正常  HTTP 请求不会把  fragment 发给  Relay 。
隧道数据经过密封后再转发， Relay 只负责连接双⽅和传递数据。
把⼿机作为决策节点⼊⼝
DSH Mobile ⽬前更适合短、轻、⾼频的交互。
Agent 运⾏时，可以在⼿机上查看流式回复和⼯具状态。遇到命令审批时，直接允许或拒
绝。 Agent 提问时，补⼀句信息让任务继续。后台  jobs 、 Goal 进度和会话状态也适合在碎
⽚时间⾥查看。
⻓  Prompt 、⼤段代码  Diff 和需要持续思考的修改仍然更适合桌⾯。⼿机屏幕和输⼊⽅式没
有因为接⼊  Agent 就突然变⼤。这个  App 的定位是远程控制⾯板，不是把完整  IDE 搬到⼿
机上。
这类产品现在已经越来越常⻅。Cursor 的  iOS 应⽤  可以启动云端  Agent ，也能通过
Remote Control 操作电脑上的  Agent 。ChatGPT 的桌⾯版说明是  Codex 已经进⼊
ChatGPT 移动应⽤可以继续  Mac 主机上正在运⾏的任务。Claude Code Remote
Control  也⽀持从⼿机接续本机会话。
⼏家的执⾏位置和数据路径并不相同，但它们都在处理同⼀个变化。具体编码⼯作交给
Agent 后，⼈更多是在任务节点上给意图、做判断和看结果。这些动作本来就不要求⼈⼀直
坐在电脑前。
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
DSH Mobile 下⼀步会先补输⼊能⼒。session.prompt 已经⽀持图⽚内容数组，可以在此
基础上增加图⽚上传和语⾳输⼊。通知能⼒也需要电脑端配合，单纯给  App 申请通知权限并
不能知道任务何时需要⼈处理。现阶段不会为了推送⽽私⾃增加官⽅协议之外的  RPC ，先把
连接和重连稳定性处理好。
这套客户端也不必永久绑定  DSH 。对多数  Agent Host 来说，移动端需要的基础能⼒很接
近，包括列出会话、下发消息、接收事件和处理审批。流式  Markdown 、⼯具卡⽚、断线状
态机与会话模型已经放在共享层。以后接其他  Agent 服务时，主要新增协议适配器，不需要
重新写三端界⾯。
快速跑起来
纸上得来终觉浅，绝知此事要躬⾏。说了这么多，还得是⾃⼰上⼿体验⼀下效果。
启动  DSH 和  Relay
本地扫码连接可以按四步完成。
1. 启动  Relay 。
2. 安装扫码插件并启动  DSH 。
3. 在⼿机上安装  DSH Mobile 。
4. 扫描  Settings 中的  Remote Access ⼆维码。
先让⼿机和电脑连接同⼀个可信  Wi-Fi 或热点。
# 终端  1 ，启动本地  Relay
git clone https://github.com/yukiykchen/dsh-scan-remote.git
cd dsh-scan-remote/relay
cp .env.example .env
npm ci
npm run build
HOST=0.0.0.0 PORT=8787 npm start
局域⽹试⽤时， Relay 需要监听⼿机能够访问的⽹络接⼝。HOST=0.0.0.0  会开放  8787 端
⼝到本机所有⽹络接⼝，请只在可信⽹络中使⽤，并检查系统防⽕墙设置。
然后安装插件并启动  DSH 。
# 终端  2 ，安装插件并启动  DSH
npx @deepseek-ai/dsh plugin --profile web add \
  "github:yukiykchen/dsh-scan-remote#v0.0.1"
export PUBLIC_RELAY_URL=http://192.168.1.10:8787
npx @deepseek-ai/dsh web
PUBLIC_RELAY_URL  要换成电脑当前的局域⽹地址。它会写进⼆维码，必须能从⼿机访
问。 DSH 启动后，打开  Settings ，再进⼊  Remote Access ⻚⾯。
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
下载和安装  App
Android 可以从  releases ⻚⾯  下载  APK 后安装。
iOS 需要使⽤  Xcode 打开  iosApp/iosApp.xcworkspace，配置⾃⼰的开发者签名后安装
到真机。鸿蒙端可⽤  DevEco Studio 打开  ohosApp  ⾃⾏构建。代码仓库链接：
deepseek-harness-mobile。
如果扫码后⼀直超时，先检查三件事。
⼿机能否访问  http:// 电脑局域⽹地址 :8787/health。
PUBLIC_RELAY_URL
  是否仍是电脑当前地址。
Relay 是否真的监听了⼿机可达的接⼝，防⽕墙是否允许  8787 端⼝。
电脑更换  Wi-Fi 或热点后，局域⽹地址通常会变化。此时需要更新  PUBLIC_RELAY_URL，
重启  DSH ，再扫描新⼆维码。
腾讯云上运⾏：让  Agent 不必依赖电脑在线
除在个⼈电脑本地运⾏外， DSH Mobile 也可以配合腾讯云轻量应⽤服务器使⽤。将
DeepSeek Harness 部署在轻量应⽤服务器上后， Agent 循环、⼯具执⾏、插件和⼯作区都
持续运⾏在云端；⼿机  App 仍然只负责连接、交互和渲染。
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
这样，⻓任务不再依赖个⼈电脑⼀直开机。即使⼈离开⼯位或合上电脑， Harness 也可以继
续执⾏；⽤户则可以在⼿机上查看流式输出和⼯具状态，在需要时处理审批、补充上下⽂或
确认下⼀步⽅向。
想继续开发，从这⼏个⼊⼝动⼿
如果只想扩展  App ，⼊⼝⽐较集中。
新增  Host ⽅法时，在  DshHostProtocol.kt 增加定义，然后复⽤现有  RPC 通道。只要不涉
及新的系统能⼒，三端不需要分别修改原⽣代码。
新增原⽣能⼒时，先在  commonMain  定义  Module ，再补三端实现。 Android
从  KuiklyRenderActivity  导出模块， iOS 实现放在  KuiklyExpand/Modules，鸿蒙实现放
在  kuikly/modules。
新增⻚⾯时，创建带  @Page  注解的⻚⾯类， KSP 会⽣成路由。
如果要让  DSH 内部的新事件出现在⼿机上，可以写⼀个  DSH 插件监听对应事件，并通
过  host/remote-event  转发。具体事件仍要加⼊  Host 侧允许转发的范围， App 端也要对宽
类型参数做容错。
注册新的官⽅  RPC ⽅法或替换整套传输层，就不再是单纯修改  App ，⽽是需要改  DSH 本
体。此类改动更适合按上游项⽬的⽅式提交和维护。
相关仓库与链接
Kuikly 框架
Kuikly 组件仓库
DSH Mobile
扫码插件与  Relay
KuiklyUI AI 开发规则与  Skills
腾讯云轻量应⽤服务器
DSH RPC ⽅法表
DSH 下⾏事件定义
DSH 仍处于  developer preview ，协议和包结构都可能发⽣破坏性变化。本⽂中的⽅法数
量、⽬录和事件名称对应  dsh-v0.1.1-rc.2。实际开发时应锁定已经验证过的版本，再逐步跟
进上游变化。
关于  Kuikly
Kuikly 是腾讯开源的⾼性能跨端框架，基于  Kotlin Multiplatform 技术，覆盖  Android 、
iOS 、 HarmonyOS 、 H5 、微信⼩程序、 Mac 六⼤平台，⽀撑业务⽇活⽤户超 5 亿。
当前 Kuikly 已经开源，有兴趣和有需要的产品，可以通过以下⽅式访问  Kuikly 仓库和⽂档，
欢迎 Star 、 Watch 与体验：
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
阅读 3 . 0 万
👉Github  仓库 | 📚官⽅⽂档
Kuikly 框架属于腾讯端服务联盟（ tds.qq.com ）的重要成员，欢迎关注及了解更多信息：
腾讯端服务官⽹：TDS  腾讯端服务
Kuikly官⽹：跨平台框架
留⾔
写留⾔
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
还没有留⾔，来写⾸评
````

