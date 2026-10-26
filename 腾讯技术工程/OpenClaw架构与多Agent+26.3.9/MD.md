# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
玩转 OpenClaw ，你需要了解的：核⼼架构、运作原理、 Agent 部署
步骤
腾讯程序员 2026 年 3 ⽉ 9 ⽇ 02 : 26⼴东原创 腾讯技术⼯程 631 ⼈
作者：冰以东
前⾔
（⼀） OpenClaw 到底有什么不同？
最近半年 AI 领域的产品层出不穷，在 OpenClaw 爆⽕之前⽐较类似的产品是 Claude 的 Happy( ⼀
款 Claude code ssh 软件 ) 。
喜欢使⽤ happy 的朋友经常问我的⼀句话是 :"OpenClaw 那么好玩吗？跟 Happy 有什么区别？ "
当初看到 OpenClaw 的功能之后我⽴马被吸引住，在⾯对这个问题后，我正好从抽象层⾯总结
⼀下 OpenClaw 的优势所在。
1 、 OpenClaw 技术框架不复杂，它的优势在于共识的推⼴
作为程序员，为了让⼤家直观理解 OpenClaw 的项⽬架构强度。  在看完 OpenClaw 框架后，我
先⽃胆做个类⽐，⼤概说⼀下 OpenClaw 的技术难度：  ⼤概就类似 AI Coding 诞⽣前，具备
「初级推荐算法的前后端通信 App 」的难度。
做过⼏年开发的同学都知道，这其实并不难，所以技术框架并不是 OpenClaw 的亮点。
OpenClaw 的优势在于共识的推⼴，举个具体的例⼦，在没有 OpenClaw 之间，我们基本⼈⼿
⼀个⾃⼰搭建的 Agent ，像我之前搭建的  L1~L5 5 层架构 Agent ：
建议有打算深⼊了解 OpenClaw 的同学优先看 OpenClaw 源码和官⽅⽂档，⽬前该项⽬正
在⾼频迭代中。本⽂重点从核⼼框架、通信机制进⾏介绍，争取让你看完本⽂后知道
OpenClaw 是怎么运作的，以及其能⼒边界在哪⾥。以及尤其希望⼤家注意的，是
OpenClaw 的安全风险，如果选择部署 OpenClaw ，就按最坏的打算 ( 数据全 Open) 去对待
⾃⼰机器上的数据。
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
相信每个搭 Agent 架构的同学，都得考虑 skills 管理、 Agent ⾝份赋予、 Agent 架构⾃进化、
memory-search 和 Session 管理这些。
这就导致⼀个问题：每次我跟朋友交流 Agent 之前，都是要先简单介绍⼀下各⾃ Agent 的架
构，然后再聊具体的落地 Case ， Session 、 memory 管理的⽅案，可能都得先聊半天。
但  OpenClaw 把 Agent 架构推⼴之后，我们基于 OpenClaw 搭建个⼈ Agent 后，就不⽤再介绍
Agent 架构是什么了，我们再聊的话题就是：怎么保活、怎么进⼀步替换 rag 算法库、怎么部
署多 Agent 、怎么应⽤ good case 。
简直丝滑爆了。
2 、多 Agent 的天然⽀持
熟悉 LLM 底层原理的同学都知道， LLM 成也 transformer ，⽬前卡脖⼦的地⽅，也在
transformer 。 Context 的瓶颈严格约束了单 Agent 智能的发挥。
传统 Prompt 定义 Agent ⾝份，再加上层出不穷的 skills ，正在⼀步⼀步蚕⾷ LLM 的 Context 窗
⼝。
为了更好使⽤ LLM ，专事专做似乎已经变成更好使⽤ Agent 的共识。
3 、做和 AI 能⼒正交的事情
AI 时代，选择不做什么事情和选择做什么事情⼀样重要。
⼀年前跟 Manus 的朋友聊天时，当时他就分享过⼀个观点：要做和 AI 能⼒正交的事情。
花时间精⼒打造和迭代⾃⼰的 Agent ，其实就是跟 AI 能⼒正交的⼀件事，跟培养⼀个⼈⼀样，
他可以是很聪明，但他认知世界和做事的能⼒，需要我们来教导他，这是千⼈千⾯的⼀个话
题。
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
当 AI 模型越来越聪明，我们只需要升级 Agent 使⽤的底层 LLM 即可，那些跟 AI 交互留下来的长
期数据，都将会变成我们未来更好驱动 AI 的私⼈宝贵数据。
（⼆）我想部署 OpenClaw ，必须要买机器吗？
买机器不是必须的，⽬前使⽤ OpenClaw 有 2 种主流⽅案：云机  和  ⾃部署。
下⾯我按顺序介绍⼀下。
1 、云机
腾讯云官⽹现在已经⽀持云机部署 OpenClaw ，也⼗分便捷。
如果能接受云机的操作习惯，这种⽅式是最合适的，不需要⽤实体机，数据也可以随时
download 下来。
2 、⾃部署
接下来介绍⼀下⾃部署，这可能是⼤家最关⼼的。
（ 1 ） Mac 和  Windows 怎么选？
OpenClaw 的部署和诸多⼯具，对 Mac 环境天然友好。如果可以，最好选 Mac 。Windows 当然
也可以部署，就是折腾⼀些，⽹上都有教程，这⾥就不展开说了。
（ 2 ） Mac 的配置怎么选？
因为 OpenClaw 部署之后基本就在本地运⾏着，所以 Mac 系列优先推荐 Mac Mini 。
其次关于  Mac Mini 的配置，这⾥主要涉及 3 个指标：芯⽚、内存和磁盘。
a. 芯⽚
从软件适配出发，既然都采⽤ Mac Mini 的⽅案了，那么⾄少要是 M 系列的芯⽚。
其次， M1~M4 ，要看部署时的诉求，如果平时不需要跑⽂⽣图、⽂⽣视频的本地模型，那么
M1 芯⽚是性价⽐最⾼的。 OpenClaw 运⾏时基本都只是调各种 api ，不怎么吃性能。
b. 内存
内存的诉求也是看是否需要本地部署⽂⽣图、⽂⽣视频的模型，如果需要部署模型，还是建议
24g 内存。
c. 磁盘
磁盘的诉求也是看是否需要本地部署⽂⽣图、⽂⽣视频的模型， ComfyUI 上的模型，动辄都是
30G 起步，所以如果⽤来跑本地模型，⾄少 256G 起步。
⽬前  Mac Mini M1 1TB 市场价 3K 左右， MacMini M4 512g ⼤概 7k 左右。
不成熟的建议就是：既然都打算部署本地模型了，建议多花 4K 玩个⼤满配，以后给家⾥⼩朋
友做⽂⽣图、⽂⽣视频，不⽤付费买 API ，还是很⾹的。
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
（三） OpenClaw 推荐使⽤哪个 IM ⼯具？
这是容易踩坑的地⽅，筛选 IM ⼯具，我总结下来有 3 个原则：安全性、可⽤性、易⽤性。
我这⾥不做推荐，只是建议⼤家从这 3 个原则⾥，明确下⾃⼰的诉求，来做决策。
1 、安全性
从数据隔离的⼤前提出发，⼀定要避免个⼈误操作发送了⼀些私密内容给 OpenClaw （注意：
千万不要把 OpenClaw 当成「⽂件传输助⼿」），以及严防习惯 OpenClaw之后忽略了其安全风
险，时刻提醒⾃⼰部署 OpenClaw 之后，就是在跟把机器⼈公开在⽹上没什么区别，按最坏的
情况去预估风险。
2 、可⽤性
这是最容易踩坑的⼀点，如果你只是部署单 Agent ，你会发现还是够⽤的。
但当你部署多 Agent 之后，你的 IM 调⽤额度会飞速消耗，我在部署 10 个 Agent 之后， IM 的额度
直接耗尽，原因是 OpenClaw 的⽹关机制中有⼀个定时快照的逻辑，
const healthInterval = setInterval(() => {
 void params.refreshGatewayHealthSanpshot({probe:true})…
})
该快照逻辑会 ping IM ， 60 秒⼀次，如果 Agent 很多， IM 额度将很快被消耗完。
所以如果你有多 Agent 的诉求，你需要选⼀个额度多 ( ⽆额度约束 ) 的 IM 。
3 、易⽤性
相⽐ OpenClaw 推荐的国外 IM 软件，国内的软件易⽤性还是⾼⼀些。
（四） OpenClaw 的配置⿇烦吗？
如果只是把⼯程 run 起来  + 配置 IM 机器⼈，半⼩时⾜矣。
但如果是配多 Agent ，配不同 Agent 的任务分配、调试 Skills 、定制 Agent ⾝份、调试定时任
务、⾃部署模型，那还是⽐较耗时的，根据  个⼈经验 + ⽹上交流经验 + ⾝边⼩伙伴配置  的经
验，⼤概需要 2-3 天的时间。
（五）折腾 OpenClaw ，我能有什么收益？
1 、技术层⾯的收益
完整搭建完这套流程后，对 Skills 的理解、对多 Agent 的理解、对⾃部署模型的理解、对
memory-search 原理的理解、对 Agent 经典架构的理解，都可以上⼀个层次。
⽐如这些问题：
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
”如果让你设计⼀个 Agent ，它的长短期记忆链路你打算怎么设计？”
“如果让你设计⼀个多 Agent 架构，你会设计哪些通信⽅式？”
“中⼤型项⽬中，怎么对多 Skills 的情况进⾏管理，怎么避免多 Skills 、低质 Skills 爆炸的问
题？”
“memory-search ⽅案的原理是什么，⼀个完整的 LLM 对话是怎么在 transformer 框架中流转
的 ?”
都可以在折腾 OpenClaw 中⾃⼰摸索到，更进⼀步的，⾯对当前各种 Vibe 的 Agent 项⽬，可以
⽐较清晰的看出这类项⽬的含⾦量和⽣命周期，这对我们在 AI 时代做技术⽅向的判断，都是⾄
关重要的。
2 、个⼈ Jarvis
这个是搭建⼯具之后，通过发挥个⼈创意可为⾃⼰带来的增益。
简单来说，就是你拥有了个⼈ Jarvis ，你可以⽤他定制任何你想让它进⾏的任务，本⽂会在
「三、 Good Case 分享」分享⼏个我⾃⼰实际⽤下来不错的 case 。
⼀、 OpenClaw 多 Agent 部署
（⼀） OpenClaw 的 quick-start
1 、快速完成 OpenClaw 的部署⼯作
（ 1 ）部署前需要提前准备的
[1] 选择你的 IM 平台
不同 IM 平台有不同的配置⽅式，这⾥按个⼈喜好选择就好。
[2] 选择你的 LLM Model
LLM Model 越聪明， OpenClaw 发挥就会越好、越稳定。
（ 2 ）本机部署 OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
使⽤如上命令安装 OpenClaw 后，会⾃动启动  openclaw onboarding ，即进⼊ OpenClaw
main Agent 的配置阶段，配置阶段按导引进⾏配对即可，其中 conﬁg skills 的部分可以跳过，
后续⾃⼰专门配置即可。
注意：
⼗分不建议使⽤ Claude Code 来进⾏ OpenClaw 的配置， CC ⽬前对 OpenClaw 项⽬配置的了解
还有偏差，极⼤可能出现 ”it works,but it also broke” 的情况，导致⼯程后续极难维护，建议还
是阅读 OpenClaw 官⽅⽂档，使⽤ OpenClaw 的官⽅指令配置 Agent 。
不过，使⽤ CC 来辅助 Debug OpenClaw 还是很⾼效的，推荐流程：
Download OpenClaw 源码到本地  →  让 CC 先学习下 OpenClaw 的源码  →  再让 CC 针对本地
OpenClaw 的配置进⾏ debug 。
给够 CC 充⾜源码语料后，交付的⽔平会⼤幅提升。
（⼆） OpenClaw Agent 核⼼架构介绍
1 、 Agent 的核⼼配置项
每个 Agent 都有其对应的 workspace ，如图是⼀个 Agent 最核⼼的配置⽂件。其各⽂件的含义
如下：
AGENTS.md ： Agent 职责声明，决定⼯具权限
SOUL.md ：个性化提示词，注⼊ system prompt
TOOLS.md ：⼯具⽩名单 / ⿊名单，安全边界
IDENTITY.md ：身份标识（ name/avatar ），通道展示
USER.md ：⽤户偏好，上下⽂先验
HEARTBEAT.md ：定时任务配置（可选）
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
BOOTSTRAP.md ：⾸次 onboarding 引导（⼀次性消费）
MEMORY.md ：⽤户记忆⽂档（ RAG 源）
通过查看 OpenClaw 的源码，我们可以找到这么⼀个⽅法：
src/agents/workspace.ts:498-555
exportasyncfunction loadWorkspaceBootstrapFiles(dir: string): Promise<WorkspaceBootstrapF
const entries = [
    { name: "AGENTS.md", filePath: path.join(resolvedDir, "AGENTS.md") },
    { name: "SOUL.md", ... },
    { name: "TOOLS.md", ... },
    { name: "IDENTITY.md", ... },
    { name: "USER.md", ... },
    { name: "HEARTBEAT.md", ... },
    { name: "BOOTSTRAP.md", ... },
  ];
// + 动态检测  MEMORY.md / memory.md
for (const entry of entries) {
    const loaded = await readWorkspaceFileWithGuards({...});
    // openBoundaryFile ：检查 inode/dev/size/mtime ，防⽌路径穿越
  }
}
⽂件顺序即优先级。 AGENTS 定义能⼒边界， SOUL 注⼊灵魂， TOOLS 划定禁区，这 8 个⽂件
构成 Agent 的完整⼈格。
在这⾥，我⼤⼒推荐朋友们阅读  AGENTS.md  这个⽂件 ⭐⭐⭐ ，这个⽂件详细介绍了⼀个
Agent 的启动、 memory 管理的流程，⾃我感觉堪称 OpenClaw 最核⼼的 Prompt ⽂件。
2 、 Agent 的启动流程
Agent 不是常驻进程，⽽是 per-session 的瞬态实例。每个对话都是⼀次完整的加载 - 执⾏ - 销毁
循环。
通过查看 OpenClaw 的源码，我们可以找到这么⼀个⽅法：
src/agents/pi-embedded-runner/run/attempt.ts:1-116
import { createAgentSession, SessionManager } from"@mariozechner/pi-coding-agent";
// 1. 加载 bootstrap 上下⽂
const bootstrap = await resolveBootstrapContextForRun({...});
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
// 2. 创建 SessionManager （封装 Pi Agent 的 session 持久化）
const sessionManager = await prepareSessionManagerForRun({
  sessionKey,
  workspaceDir,
  ...
});
// 3. 构建 system prompt （注⼊ workspace ⽂件内容）
const systemPrompt = buildEmbeddedSystemPrompt({
bootstrapFiles: bootstrap.files,
  ...
});
// 4. 创建 agent session
const agentSession = await createAgentSession({
  model,
  systemPrompt,
  sessionManager,
tools: createOpenClawCodingTools({...}),
  ...
});
可以看到， System Prompt 是动态⽣成的，即每次 run 都会重新读取 workspace ⽂件，确保配
置实时⽣效。
（三） OpenClaw Agent 的记忆⼒机制
了解 OpenClaw Agent 的记忆⼒机制，对于我们后续精细化对 Agent 优化、管理 skills 、学习
Agent 记忆⼒机制设计⽅式，都有很⼤的帮助。
和 OpenClaw 记忆⼒机制相关的配置有三个：
// 会话信息
.openclaw/agents/ceo/sessions/xxxx.jsonl
// 按天记录的 memory
.openclaw/workspace-ceo/memory/YYYY-MM-DD.md
// LLM 精练后的 memory
.openclaw/workspace-ceo/MEMORY.md
通过查看  .openclaw/agents/ceo/sessions/xxxx.jsonl  ⽂件，我们可以发现该 .jsonl ⽂件记
录了会话的记录。
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
但这时我们会产⽣如下问题：
1 、 Session 是怎么实现会话按需加载的？
正如我们前⾯所说的，不同的会话有其对应的.jsonl 。
（ 1 ） Session Header
在.jsonl ⽂件中， Session Header 是  JSONL ⽂件的第⼀⾏元数据，结构如下：
{
    type: "session",
    id: "session-uuid",           // sessionId
    cwd: "/path/to/workspace",    // ⼯作⽬录
    timestamp: 1234567890,
    parentSession?: "parent-id"   // 可选， fork 时存在
  }
我实际捞⼀个 Session ，可见其 Header 内容如下：
{"type":"session","version":3,"id":"fd292408-168e-4c7b-9f2a-ff7ec0a7c492","timestamp":"20
（ 2 ） Agent 的  Session 加载
Session 的加载也是懒加载机制，当消息到达路由到  SessionKey 之后， OpenClaw 会查找
sessions.json 获取当前  SessionId ，将  SessionId 对应的.jsonl 加载到 Agent 中。
2 、 Session 太长，是不是就挤爆 LLM Context 了？  是怎么优化的？
（ 1 ） LLM 感知  Session 的完整流程
OpenClaw 显然是不会将全量的 Session 加载进 LLM 中，那么它做了什么优化呢？
在 Session 加载  →  LLM 感知阶段，按如下流程进⾏ load ：
1.  加载  JSONL ⽂件
2. SessionManager 解析为  messages 数组
3.  应⽤过滤 / 裁剪策略
4.  发送给  LLM
这⾥最有意思的就是【 3. 应⽤过滤 / 裁剪策略】
（ 2 ） Session 应⽤过滤 / 裁剪策略
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
A. Compaction （压缩）  - 持久化
当对话太长时，旧消息会被  总结  成⼀个  summary 。
⽐如：
压缩前发送给 LLM ：
[user1, assistant1, user2, assistan2, … ,user100,assistant100]
压缩后发给 LLM ：
[compaction_summary, user80, assistant80, … ,user100, assistant100]
            ↑
         firstKeptEntryId 来控制 compaction 程度
进⾏该  compaction 压缩后，会写⼊  JSONL ⽂件（也即进⾏了持久化）。
下次对话继续使⽤的就是压缩后的历史。
B. Session Pruning （修剪） - 临时
在发送给  LLM 之前，临时裁剪旧的  tool 结果。
⽐如：
修剪前  JSONL ⽂件中：
[user1, assistant1, toolResult1(10KB), user2, assistant2, toolResult2(5KB)]
修剪后发送给 LLM 的内容：
[user1, assistan1, "[Old tool result cleared]", user2, assistant2, toolResult2(5KB)]
            ↑  旧的  tool 结果被替换
该修剪策略不修改  JSONL ⽂件，仅仅是内存级别的操作。
C. History Limit （历史限制）  - 可选
OpenClaw 源码中，可以看到该⽅法：
getHistoryLimitFromSessionKey(sessionKey)
// 可以限制发送的消息数量
3 、 Agent 是怎么通过对话 (session) 的⽅式迭代 Memory.md 的？
Agent 通过⽂件系统⼯具（ fsWrite/fsAppend ）更新  Memory.md  。
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
当  Session 接近  context 上限时， OpenClaw 会⾃动提⽰  Agent 写⼊ Memory ，然后再压缩
Session 。
4 、 Agent 是怎么决策使⽤ Memory 的？
看图就好，这张图⾮常清晰了。
（三）单 Agent 架构会出现什么问题？
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
Transformer 架构和原理想必⼤家都已清楚，单 Agent 的架构不仅有可能导致 Context 的快速消
耗，还会错误 search 导致交付质量降低。
举⼀个我⾃⼰遇到过的例⼦：
先构建⼀个 RAG tutor Agent ，让它来强化我们 Flutter 的技能。
当我中途和该 Agent 讨论过 C++ 的内容，那么因为 memory 机制的问题，
后续和该 Agent 多轮对话过程中，它都会带着 C++ 相关的记忆，
让它提供 Demo 示例时，它不会提供 Flutter 相关，⽽提供了 C++ 相关的示例。
尤其是涉及复杂任务时，即使现在业内针对 Context 上限约束做了很多⽅案，在交付⽔平和运
⾏速度上都差强⼈意。
所以如果我们明确了 Agent 的专属任务，最好还是让 Agent 专事专做，效果会更好。
（四） OpenClaw 多 Agent 部署
接下来，我们将介绍多 Agent 的部署流程。
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
接下来为了⽰例和⼤家理解，我们新增 2 个 Agent ： ceo 、 iostutor 。
新增 Agent 的指令：
openclaw agents add iostutor
使⽤ OpenClaw 指令新增 Agent 的好处，就是可以按 openclaw onboading 的初始化流程配置
Agent ，整个过程对应的填上 [IM bot API] 和 [LLM API] 即可，流程并不⿇烦。
（五）多 Agent 通信，协同⼯作
多 Agent 配置完毕后，我们接下来要配置 Agent 的协同⼯作，才能更⼤价值发挥多 Agent 架构的
效果。
在 OpenClaw 中， Agent 之间的调⽤有两种⽅式：sessions_send 和  sessions_spawn。
1 、 sessions_send 和  sessions_spawn 的区别是什么？
（ 1 ） sessions_send   向已经存在的  session 发消息
简单来说，当 Agent 之间的通信，需要被写⼊各⾃的 memory 时，就建议使⽤  sessions_send
的⽅式。
拿公司举例：给同事发消息，他在⾃⼰⼯作的上下⽂中处理，这种情况就很适合使⽤
sessions_send 。
（ 2 ） sessions_spawn: 在独⽴环境中运⾏任务
sessions_spawn 采⽤ SubAgent 的⽅式，通过调起⼦ Agent+ 传⼊内容的⽅式，让其完成交
付。
sessions_spawn 更像是在雇佣临时⼯，给他⼀个独⽴的任务，完成后进⾏汇报。
⽐如：
ceo ⾓⾊说  : " 让 iostutor 写⼀个  Swift 的⽹络请求封装类， 30 分钟内完成 ”
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
即， A 如果能指挥 B ⼲活，那么 B 就是 A 的 SubAgent 。
2 、 sessions_send 和  sessions_spawn 应该分别怎么配置？
sessions_send 和  sessions_spawn 都在  openclaw.json ⽂件下进⾏配置。
（ 1 ）配置 sessions_send
没配置前：
配置过程：
  "tools": {
      "agentToAgent": {
        "enabled": true,
        "allow": ["ceo", "iostutor"]
      },
      "sessions": {
        "visibility": "all"   <- 这个特别容易漏，记得⼀定要配上了
      }
  },
配置成功后：
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
如图所⽰， ceo →  iostutor 的会话，已经写⼊ iostutor 的 session 中， Agent 之间可以互相进⾏通
信了。
（ 2 ）配置  sessions_spawn
配置  sessions_spawn 也不负责，⽐如我们需要让  iostutor 成为  ceo 的 SubAgent ，那么我们
就这么配置：
      {
        "id": "ceo",
        "name": "ceo",
        "workspace": "/Users/blinblin/.openclaw/workspace-ceo",
        "agentDir": "/Users/blinblin/.openclaw/agents/ceo/agent",
        "model": "openai-codex/gpt-5.3-codex",
          "subagents": {
            "allowAgents": ["iostutor"].  <- 新增这个
          }
      }
3 、 sessions_send 和  sessions_spawn 怎么安排？
具体应该怎么安排 Agent 之间的关系，关于这块的思考我参考了组织中⾼效运作的⼏个原则。
1. 扁平化  2. 达成⽬标是最终⽬的，层级只是达成⽬标的⽅式。
所以基于这两个原则，假设我们的 Agent 是公司的员⼯，那么员⼯之间要做到的就是要互通有
⽆，⾼效沟通时最重要的，所有 Agent 均可进⾏ sessions_send 互通：
      "agentToAgent": {
        "enabled": true,
        "allow": ["ceo", "iostutor"].  <- 要把所有 Agent 都加进来
      },
其次，为了达成集体的⽬标，在有需要时，每个 Agent 都有义务帮助另⼀个 Agent ，所有每个
Agent ，都是另外⼀个 Agent 的 SubAgent ：
      {
        "id": "iostutor",
        "name": "iOSTutor",
        "workspace": "/Users/blinblin/.openclaw/workspace-iostutor",
        "agentDir": "/Users/blinblin/.openclaw/agents/iostutor/agent",
        "model": "openai-codex/gpt-5.3-codex",
        "subagents": {
          "allowAgents": ["ceo"] <- 这⾥要加上除了⾃⼰之前的其他所有 Agent
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
        }
      },
      {
        "id": "ceo",
        "name": "ceo",
        "workspace": "/Users/blinblin/.openclaw/workspace-ceo",
        "agentDir": "/Users/blinblin/.openclaw/agents/ceo/agent",
        "model": "openai-codex/gpt-5.3-codex",
        "subagents": {
          "allowAgents": ["iostutor"] <- 这⾥要加上除了⾃⼰之前的其他所有 Agent
        }
      }
当然了，这⾥的设定都是按能对公司 OKR 起到明确贡献的 Agents 的通信⽅式。
如果有⼀个 Agent 的职责只是类似前台的⾓⾊，那么只需要控制单向数据传输 SubAgent 即可。
4 、 sessions_send 和  sessions_spawn 的决策机制
问题：当我们配置了 A 和 B Agent 互为 SubAgent ，且允许 AgentToAgent 时， Agent 是怎么决定
调⽤ sessions_send 还是  sessions_spawn 的？
这取决于 LLM ⾃⼰的判断，⽐如我们配置了  ceo 和  iostutor 允许 sessions_send ，也配置了
ceo → iostutor sessions_spawn 。
这时我们给 ceo 发送⼀条消息： “ 让 iostutor Agent ⽣成⼀个⽂章发给我 ”
LLM 会理解为：
1. 这是⼀个新任务（⽣成⽂章）  2. 需要  iostutor 执⾏任务并返回结果  3. 不是跟  iostutor 的某个
现有对话继续聊天
但，如果我们说： " 继续跟  iostutor 的那个⽂章讨论 ” ，这种有明确上下⽂指向的指令，就会使
⽤  sessions_send 。
5 、 AgentToAgent 团队 Agent 遗忘问题
有的朋友打通这⼀步之后，过了⼏天再让 iostutor 去找 ceo ， iostutor 就完全不知道怎么进⾏
AgentToAgent 的通信了。
这是因为我们上⾯的配置，让 Agent 之间的通信是⽤ session 来记忆，它能记住我们会话⾥说的
Agent 是⼯程⾥的⾓⾊（因为我们给它发送了这么⼀句话： ” 使⽤  sessions_send ⼯具，参数：
sessionKey="agent:ceo:main", message=" 测试  agent-to-agent 通信 ", timeoutSeconds=60”
）。
但当短期记忆遗忘后，它就忘记了这个指令，所以为了解决这个问题，我们需要在
workspace/agent_xx/AGENTS.md 进⾏配置，明确告诉它不同 Agent 分别是谁， such as ：
````

## PDF 第 17 页

[原页](RAW.pdf#page=17)

````text
## AgentToAgent 通信
当你需要其他⻆⾊的意⻅或具体执⾏时：
- **iOS 问题 ** → `@iostutor` 获取技术评估
使⽤  `callAgent("iostutor")`来直接通信。
注：AGENTS.md  内容会被注⼊到  system prompt 中。
6 、 sessions_send 通话的内容过期机制如何？
A Agent 和 B Agent 使⽤  sessions_send 通话后，间隔 6 ⼩时后， A 和 B 还能基于 6 ⼩时以前的
session 继续沟通吗？会新开启⼀个 session 吗？还是复⽤之前的 session 呢？
结果是：会复⽤之前的 session 。
session_send 不创建新的 session ，它只向已存的 session 发消息。
6⼩时前  A 和  B 通过  sessions_send 通话时：
A 的  session （⽐如  agent:ceo:internal:main ）
B 的  session （⽐如  agent:iostutor:internal:main ）
（六）多 Agent 应⽤实战经验
1 、公司要扁平化，不要部署太多 Agent
太多的 Agent 管理起来会⽐较复杂，尤其是多层级的汇报关系，是⾮常不建议的。
2 、要信任公司成员，尽量保持 Agent 的双向沟通
如上⽂所述，建议 Agent 同时配置  sessions_send 和  sessions_spawn 。
3 、要设⽴核⼼成员边界，控制核⼼ Agent 数量
如果是⽐较明确的⼯具 Agent ，⽐如：专门对 Markdown 格式进⾏排版的 Agent 。
那么建议这种 Agent 就只配置 SubAgent 即可，它不需要记住太多上下⽂，专⼼把交付的事情处
理完即可。
⼆、 OpenClaw 精细化管控
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
````

## PDF 第 18 页

[原页](RAW.pdf#page=18)

````text
⼆次强调：不要⽤ CC 来操作 OpenClaw ，如果⼀定要⽤ CC ，记得先把  OpenClaw 源码爬下
来，让 CC 学⼀下，再去操作 OpenClaw 。
（⼀） Skills 管控
1 、 Agent 加载 Skills 的流程
⾸先我们要明确⼀个概念， Skills 不是每个⽂档的完整注⼊，只是注⼊列表。（这并不是
OpenClaw 的专属操作，是所有⽀持 Skills 能⼒的基础操作）
与  AGENTS.md 等⽂件不同， Skills 采⽤按需加载机制：
System prompt 只注⼊  skill 列表（名称、描述、路径）
Agent 需要时⽤  read ⼯具读取完整的  SKILL.md
（ 1 ）注⼊流程：
Skills 来源（ 3 个位置，按优先级）
1. workspace-xxx/skills/ ←  最⾼优先级（ per-agent ）
2. ~/.openclaw/skills/ ←  中等优先级（ shared ）
3. bundled skills (npm 包内 ) ←  最低优先级（内置）
（ 2 ）过滤
检查每个  skill 的  requires.bins/env/conﬁg
跳过不满⾜条件的
skill 的  requires.bins/env/conﬁg ，可以配置执⾏ skill 要求的基础条件，⽐如最简单的
Weather ：
name: weather
description: "Get current weather and forecasts via wttr.in or Open-Meteo. Use when: user 
homepage: https://wttr.in/:help
metadata: { "openclaw": { "emoji": " 🌤 ", "requires": { "bins": ["curl"] } } }
（ 3 ）⽣成 Skills 注⼊列表
<available_skills>
<skill>
<name>healthcheck</name>
<description>...</description>
<location>~/.openclaw/skills/healthcheck/SKILL.md</location>
</skill>
````

## PDF 第 19 页

[原页](RAW.pdf#page=19)

````text
...
</available_skills>
（ 4 ）注⼊ Agent system Prompt 和使⽤
Agent 看到列表，需要时⽤  read 读取完整内容
2 、精细化 Skills 注⼊
Skills 太多会给 Agent 造成 Context 负担，甚⾄错误的 Skills 会导致 Agent 错误调⽤⼯具。
所以我们要对 Agent 进⾏精细化的管控，把每个 Agent 的 skills 加载配置成：
【基础通⽤能⼒ Skills + 专属 Skills 】
⽐如  brave_search 这个 skill ，属于让 Agent 进⾏⾼效的联⽹检索，它就应该属于基础通⽤
SKill 。
⼜⽐如 Weather 这个 skill ，我只让「 Family Agent 」进⾏定时天⽓汇报，那么 Weather 就应该属
于「 Family Agent 」的专属 Skill 。
3 、 Skills 延迟加载问题
在你修改完 Skills 架构之后，你⼤概率会遇到⼀个问题， Agent 并没有加载最新的 skills 配置，
⽐如我们这⾥调整 skills 之后，咨询 Agent skills 情况会发现还是使⽤旧的 skills ：
````

## PDF 第 20 页

[原页](RAW.pdf#page=20)

````text
这是因为 OpenClaw 在 session 启动时会创建 skills 快照，并在整个 session 期间复⽤。
重启 gateway 后，旧 session 仍然使⽤旧的快照。
这时我们删除对应的  session ，再重新咨询  Agent 的 skills 情况，就会发现新加的 skills 已经被
更新出来了：
````

## PDF 第 21 页

[原页](RAW.pdf#page=21)

````text
4 、关于 Skills 的其它⼩技巧
（ 1 ） Clawhub
Clawhub 是针对  OpenClaw 的  Skills Market ，可以使⽤ Clawhub 的指令对 OpenClaw skills 进
⾏管理。
 # 语义搜索  Skills
clawhub search "calendar management"
# 安装指定  Skill
clawhub install <skill-slug>
# 列出已安装的  Skills
````

## PDF 第 22 页

[原页](RAW.pdf#page=22)

````text
clawhub list
# 更新所有已安装的  Skills （谨慎使⽤， skill 建议都做成离线的）
clawhub update --all
# 同步并备份本地  Skills
clawhub sync
推荐⼏个⽐较好⽤的 Skills ：
1. Find-skills 
https://clawhub.ai/JimLiuxinghai/find-skills
2. Summarize 
https://clawhub.ai/steipete/summarize
3. self-improving-agent 
https://clawhub.ai/pskoett/self-improving-agent
4. brave-search 
https://clawhub.ai/steipete/brave-search
5. frontend-design 
https://clawhub.ai/ivangdavila/frontend
（ 2 ） Skills 的定期管理
Skills 的添加过于简单，导致⾮常容易出现 Skills 膨胀、低质扩散的情况。
所以推荐定期使⽤⾼阶模型对 skills 进⾏扫描  ：清理低质量 skill 、冲突 skill 、不必要的 skill 。
（⼆） OpenClaw 的版本控制问题
OpenClaw 存了太多本地重要数据，且 OpenClaw 的配置⾮常容易被搞挂。
所以我们需要对 OpenClaw 进⾏版本管理，但⼜不能全量进⾏  add 操作。
⽬前关于 OpenClaw 的版本管理，没有统⼀的⽅案，⾃⼰ diy 也不是很复杂，这⾥补充两个需要
注意的点。
1 、 memory 的切割
Session 、  memory/xxx.md 、 memory.md 存储了我们的对话信息，这部分信息不建议上云，
可以在 .gitignore 中进⾏配置。
2 、密钥的动态注⼊
````

## PDF 第 23 页

[原页](RAW.pdf#page=23)

````text
openclaw.json  ⽂件中同时存储了「密钥」和「 OpenClaw 核⼼ conﬁg 」，我们要做的是对
「 OpenClaw 核⼼ Conﬁg 」进⾏配置，所以建议「密钥」部分通过注⼊的⽅式进⾏管理，避免
「密钥」的泄露。
三、 Good Case 分享
1. Daily_paper
AI 时代消息太多，推荐  https://huggingface.co/papers 的 daily_paper ，可以通过 Agent 进⾏每
⽇论⽂的抓取，让它快速提炼论⽂要点，让我们从源头了解 AI 的前⾔信息。
注： Agent 直接获取  https://huggingface.co/papers  容易失败，可以考虑 jina.ai 这个⼯具。
2. Summary
这个没什么好说的， Agent 必备能⼒，通过获取 Subscribe 的博主，定期分析内容，评分，提
取⾼质量信息。
3. deepResearch
DeepResearch 也是 Agent 的核⼼能⼒之⼀，当我们需要深⼊研判⼀个消息时，可以让 Agent
启动  DeepResearch 能⼒，对消息进⾏分析。
注： DeepResearch 的交付质量受限于 LLM 的能⼒，更好的 LLM 能显著交付质量更⾼的内容。
4. RAG tutor
通过在  Workspace/Agent_xx/Memory/xxx.md ⽬录下配置学习资料，我们可以让 Agent 成为
我们垂直领域的专属 tutor ，借助 OpenClaw 的能⼒，⽤最快的⽅式实现⼀套 RAG tutor 。
````

## PDF 第 24 页

[原页](RAW.pdf#page=24)

````text
5. ComfyUI 本地⽂⽣图 / ⽂⽣视频
⽬前调⽤⽂⽣图、⽂⽣视频的 api 接⼝都是要付费的，当我们⾃部署 OpenClaw 之后，可以通过
ComfyUI 在本地部署「⽂⽣图、⽂⽣视频」接⼝，这样我们的 Agent 就可以通过调⽤本地模型
进⾏内容的⽣成。
6. tts 语⾳本地部署
本机部署了  qwen3-tts 的模型⽤来进⾏语⾳合成，搞⼀个学英语，读新闻的定时任务还是不
错的。
https://github.com/kapi2800/qwen3-tts-apple-silicon
````

## PDF 第 25 页

[原页](RAW.pdf#page=25)

````text
````

## PDF 第 26 页

[原页](RAW.pdf#page=26)

````text
````

## PDF 第 27 页

[原页](RAW.pdf#page=27)

````text
7. 家庭助理
可以配置家庭专属 Agent ，进⾏完 Memory 隔离后，可以⼀家⼈都在 IM 群⾥，家庭的⼀些定时
任务，⽐如 ”xxx 清理和替换 ” 、 ” 提醒⽗母吃药 ” 等等，可以极⼤提升家庭幸福感。
说在后⾯
1. Model 的选择
在预算 OK 的情况下，建议使⽤ SOTA 模型，落后的 LLM 会影响使⽤者的⼼智判断。
在交付不及格的情况下，很容易就做出 ”AI 能⼒还不⾏，解决不了我这个事情 ” 的判断。实际⼤
概率是因为 LLM 还不够 SOTA ， use SOTA model ﬁrst 。
另外不建议按「年」对专⼀某个模型进⾏订阅，模型迭代速度很快，专⼀模型的订阅可能⼏个
⽉就不能⽤了。
2. OpenClaw 还有很多可以玩的
⽐如替换 OpenClaw 的  memory-search 底层算法，⼜⽐如重写 AGENTS.md 构建更复杂的
Agent 关系，喜欢折腾 OpenClaw 的朋友可以在评论区多多沟通，⼀起通宵捉龙虾。
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
````

## PDF 第 28 页

[原页](RAW.pdf#page=28)

````text
阅读 4 . 6 万
留⾔
还没有留⾔，来写⾸评
写留⾔
````

## 采集与转写核验记录（非原文）

以下说明由本次核验添加；上方逐页文本保持文本层原样，图片与布局以PDF为准。

- PDF物理页 25：p.25整页空白，无法判断是否导出留白或原内容缺失；保留完整性待复核
- PDF物理页 7,8,9,14,15,16,18：源码/JSON包含省略号、截断签名、箭头标注或异常标点；按说明片段阅读，不声明可直接运行
