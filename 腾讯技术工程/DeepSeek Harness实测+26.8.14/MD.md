# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
DeepSeek  Harness  实测 ｜ 模型之外的那⼀半，到底带来了什么
2026 年 8 ⽉ 14 ⽇ 18 : 30⼴东腾讯技术⼯程 143 ⼈
作者： osli 元宝产品经理；相关团队：元宝产品中⼼、元宝模型⼯程中⼼、元宝⼤模型应⽤
算法中⼼
DeepSeek-V4-Pro 正式版上线当天，DeepSeek Harness 也开源了。之前注册 Deepseek
Harness 公众号已经吵闹过⼀阵。 V4 Flash 发布报告的模型卡⾥只漏过⼀句  DSH，外界却
已经猜测了很久，可谓期待值拉满了。
源码摊开以后，预期和实物略有点对不上号。很多⼈等的是  DeepSeek 版  Codex 。当前开
源的这套东⻄更像还能继续造  Agent 的  runtime 。 Web coding agent 有，Headless、
Python SDK 、 ACP 和  JSON-RPC 也有。模型、⼯具、会话、权限、沙箱、 Agent Loop 和
UI ，都可以拆开再装。
我第⼀时间基于开源仓库，在本机把  npm 、 Web 、 Headless 和  Python SDK 都跑通了，拆
开默认配置和  session log ，⼜拿同⼀个  Kimi K3 对照  DSH 与  Kimi Code，最后让  V4
Pro 连续做⼀条带视觉产物的复杂任务。
跑完以后总体印象是： DSH 现在更像是⼀个开放的  Agent 平台脚⼿架，默认产品还带着预
览版的⽑边，留待社区的打磨。⼀切皆插件的理念挺新颖， Trajectory 的源码设计⼝碑不
错，值得学习。
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
图  1 　按插件树、可替换能⼒和追加式事件流绘制的概念图。该图由图像模型⽣成，不是产品界⾯。
DSH 仍处于  Developer Preview 。⽂中数字来⾃单次本机运⾏和公开⽤户反馈，⽤来看差
异和边界，不做产品排名。
社区从⼀开始就在看两样东⻄
知乎问题《如何评价在  8 ⽉  13 ⽇发布的  DeepSeek Harness 》下的反馈，⼤致分成两组。
⼀组⽤户等的是成熟  coding agent 。他们关⼼桌⾯  App 、终端体验、 Windows 、缓存命
中、⽇常编码效果，以及官⽅  Harness 能不能把  V4 Pro / Flash 再抬⼀截。
另⼀组内测者盯着插件、 Preset 、Trajectory 和运⾏时⾃修改。他们看⻅的是⼀个可以继
续开发  Agent 的平台。
两边都没看错。 DSH 同时有这两个身份，完成度却不对称。 runtime 已经很开放，默认产品
体验还没追上  Claude Code 、Codex、 Kimi Code 。
最稳的好评是  Trajectory
段⼩草把  Trajectory ⽐作  Agent 的  DevTools 。时间轴、每轮请求和⽇志都能看⻅，查上下
⽂压缩、 Skill 过多和模型犯错时很有⽤。
⼘寒兮也特别提到运⾏信息⾯板。缓存命中、输⼊  / 输出  token 和  token 速度都直接显示出
来。
这件事和源码对得上。 DSH 要求模型看⻅的内容必须已经记进⽇志， Trajectory 直接从
session event log 投影。它没有另埋⼀套监控数据，所以看⻅的轨迹更接近模型当时收到
的真实请求。
插件值钱的地⽅，是把  Agent 收窄
社区早期插件⾥有不少换肤和整活，更值得看的是领域  Agent 。
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
Kitt 在进化分享的  Data Agent 只保留  read 、 edit 、 write ，再⽤  sqlcmd 替换  bash 。模
型围着数据库执⾏结果转，同时不再带着和数据分析⽆关的⼯具与上下⽂。
这个例⼦把  Plugin 和  Preset 的分⼯讲清楚了。插件提供新能⼒， Preset 决定某类  Agent
能看⻅哪些能⼒。 DSH 真有⽣产价值时，往往落在删掉什么、替换什么。继续堆⼯具，只会
多耗  token ，也让模型更难选。
⻓任务能跑，账单也要⼀起看
Adam Platin⾃述⽤⼀周内测版管理机器学习竞赛。 Agent 读规则、跑脚本、推进实验并调
⽤浏览器， 89 步后收尾。
⽠⼦脸帅哥给出了另⼀条时间线。 DSH 将  Agent 接⼊微信，从需求到真机收到回复约  87.6
分钟，花费约  18 元。过程包含  SDK 调研、零依赖客户端、 mock server 、真实端点冒烟和
扫码绑定。
这两条都是⽤户⾃述，不能当  benchmark 。它们仍然给出⼀个很实⽤的尺度。⻓任务是否
做完只是⼀半，另⼀半是花了多少分钟、多少  step 、多少  token 、⼏次⼈⼯接管。
跑通不难，麻烦在上下⽂从哪进来
官⽅最快的路径是  npx @deepseek-ai/dsh web。 Node 需要  ^22.19.0 || >=24，启
动后填写  API Key 、选择⼯作区和  Agent Preset 就能⽤。源码安装还会碰到  pnpm 、构建
和  Git hooks ，更适合准备开发插件的⼈。
本机实际跑通了四条⼊⼝。
Web UI 能正常创建本地⼯作区与会话
Headless 能执⾏⼀次性任务，成功时只向  stdout 输出最终回复
Python SDK ⾃带捆绑运⾏时，不依赖系统  Node
--dump-config
  可以直接打印最终插件树
默认配置也能直接核对。 Web profile 组装出  129 ⾏插件配置， Headless 为  81 ⾏。默认模
型是  DeepSeek V4 Flash ，权限是  workspace-write + ask。不同模式不是界⾯开关，
它们加载的提示词和⼯具集合确实不同。
System Prompt 可以从⽇志还原
DSH 没有把运⾏时请求藏在内存⾥。 System prompt 由  persona 、⼯具说明和插件注册的
prompt sections 拼起来。发请求前，request/header  会记下  system 、 model 、
temperature 、 max tokens 与  tools ，request/context  记下  provider 和  context
window 。
官⽅  Python SDK 的  minimal composition 更容易看清这个结构。它把  persona 固定成⼀
句  You are a helpful software engineer assistant.，关掉  workspace prompt 、
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
Skills 与  compaction ，只留下  persistent bash 和  str_replace_editor。模型前缀被冻
住了，⼯具⾯带来的⼲扰也少很多。
Trajectory 底下是⼀条只能追加的事件流
会话以  zstd 压缩  JSONL 保存，每条记录都有统⼀外壳。
{"type": "tool/call", "seq": 31, "time": 1786632922876, "data": {}}
⼀次写⽂件任务在本机产⽣  61 条事件。⾥⾯有  turn/start、三个  step/start、⽤户消
息、请求头、 reasoning chunks 、两次  tool call / result 、 assistant message
和  turn/end。模型先  write ，再  read 核对，最后汇报。
所以  Trajectory 能同时回答三类问题。
1. 模型当时看⻅了什么
2. 哪⼀步调⽤了哪个⼯具
3. token 、缓存和结束原因怎样变化
四个字⺟的任务，⾸包也能吃掉⼀万三 Token
我⽤  DSH Headless 的默认配置做了⼀次最⼩测试，⽤户指令只有 “ 回复  PONG” 。尽管任务
很短，⾸轮请求仍包含约  13,467 个  input token 。继续检查⽇志后发现，主要开销来⾃默认
加载的系统提示、⼯具说明、仓库规则和  Skill 摘要
测试⽬录位于⼀个⼤仓库内部。 DSH 沿最近的  .git 找到仓库根，注⼊
了  AGENTS.md / CLAUDE.md，⼜扫到⽤户技能⽬录⾥的  27 条摘要。写⽂件任务后续  step
出现约  1.3 万  cache-read token 。这些固定前缀进了缓存，也说明它们确实进了模型请
求。
后来评测和敏感项⽬，我都会换独⽴  Git 根，显式设置独⽴
的  DSH_HOME  与  DSH_AGENTS_HOME。⽐较模型时⽤  minimal composition ，这样才能够
把上下⽂整理的⼲净⼀点。
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
图  2 　标准、 PTC 、极简、创造四种预设对应不同插件组合。
标准模式提供完整的编码⼯具，适合直接处理⽇常开发任务。 PTC 模式在此基础上允许模型
⽤  TypeScript 组合多步⼯具操作，极简模式只保留  bash 和⽂本编辑器，创造模式则增加
运⾏时检查、插件实验和⾃定义  Preset 所需的能⼒。
同⼀个  Kimi K3 ，换  Harness 后发⽣了什么
Kimi Code 与  DeepSeek Harness 都是国产、 MIT 开源、可接多模型的  coding agent /
Harness 。两边的出发点并不相同。
维度 DeepSeek Harness Kimi Code CLI
官⽅定
位 可重新组装的  Agent runtime 开箱即⽤的终端  coding agent
主要⼊
⼝ Web 、 Headless 、 Python SDK 、 ACP TUI 、-p、 ACP 、 Web
扩展⽅
式
Cordis Plugin 、 Preset 、 Patch 、 Skills 、
Hooks 、 MCP Plugins 、 Skills 、 Hooks 、 MCP 、 Subagents
Agent L
oop 作为插件注册，架构上可替换 v2 DI 中的  Agent-scope Service ，源码开放但属
于固定引擎主⼲
默认模
型 DeepSeek ，另有  pi-ai 多  Provider Kimi ，⽀持兼容  Provider
默认⼯
具
标准模式约  25 项，含⽂件、 Shell 、任
务、⼦代理、⼯作流、⽹⻚
Read 、 Write 、 Edit 、 Grep 、 Glob 、 Bash 、 We
b 、 Todo 、 Task / Subagent 等
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
维度 DeepSeek Harness Kimi Code CLI
权限 read-only / workspace-write / danger-fu
ll-access 常规审批、 yolo 、 auto
可观测
性
Session Event 、 Trajectory 、 token / cac
he 、可编程投影 stream-json 、 session export 、kimi vis
安装形
态 npm 需要  Node 22.19+ 官⽅单⽂件分发⽆需  Node ， npm 安装另需  Node
Kimi Code CLI  的仓库本身也是开放的。两边都开源，差别在运⾏时怎么组织。 Kimi Code
把可扩展能⼒围着⼀套终端产品转， DSH 把  loop 、 provider 、 session 和  UI 都放进同⼀种
插件组合模型。
公开反馈普遍认为同模型换  Harness 会改变产物，但任务、权限和上下⽂经常没有保持⼀
致。这⾥固定  Kimi K3 API 、提示词、⼯作区与隐藏验收，看两套产品怎样完成相同任务。
模型统⼀使⽤  kimi-k3
提示词、任务模板和隐藏验收相同
每次使⽤全新  Git ⼯作区与空技能⽬录
DSH 使⽤官⽅  minimal ⼯具⾯
Kimi Code 使⽤  0.35.0  ⾮交互模式
每题只有⼀次运⾏，因此只看轨迹
有⼀处我故意留了不同。 DSH 使⽤  minimal ，只暴露  persistent bash
与  str_replace_editor。 Kimi Code 使⽤默认⼯具。这样不适合⽐较谁的⼯具更少，适
合观察两套  Harness 怎样把同⼀个模型引向不同执⾏路径。若要⽐较默认产品能⼒，还得⽤
DSH standard 再跑⼀轮。
两道题分别是依赖批次规划与会话事件投影。每题有  7 个公开测试、 8 个模型看不⻅的隐藏
测试。
任务 Harness 验收 时间 轨迹单位 ⼯具调⽤
依赖规划 DSH minimal 15 / 15 112.2 秒 9 step 11
依赖规划 Kimi Code 15 / 15 48.9 秒 4 条  assistant 消息 5
会话投影 DSH minimal 15 / 15 111.3 秒 7 step 7
会话投影 Kimi Code 15 / 15 123.1 秒 5 条  assistant 消息 6
正确性没有拉开。两边四条轨迹全部通过  15 / 15 。第⼀题  Kimi Code 快约⼀分钟，第⼆题
DSH 快约⼗⼆秒，速度没有稳定赢家。
过程差得更清楚。
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
Kimi Code ⾸轮并⾏读取  README 、源码和测试，随后整⽂件  Write ，再⽤  Bash 验证。依
赖规划只⽤了  5 次⼯具调⽤。它的默认⼯具更丰富，系统提示也更偏向尽快完成⼀个编码任
务。
DSH minimal 主要在  persistent bash 与  str_replace_editor  之间来回⾛。依赖规划⽤
了  11 次⼯具调⽤，步骤更碎。换来的是模型前缀、⼯具⾯和请求⽇志更容易冻住， session
log 还给出完整  request 、 tool 与  usage 事件。
Kimi Code 的  stream-json  在本轮没有返回  token usage ，因此不⽐较成本。 DSH 两题
分别记录  7,593 / 5,082 input token ，以及  22,515 / 18,632 cache-read token 。
如果⽬标是⽇常终端编码， Kimi Code 的安装和默认⼯具更省事。如果⽬标是研究上下⽂、
替换  provider 、定制领域  Agent 或复现实验， DSH 的插件树与事件⽇志更好⽤。
源码层⾯，差别落在哪⾥
前⾯的轨迹差异，在源码⾥可以找到三组对应关系。
第⼀组是  Agent Loop 。 Kimi Code 当前默认使⽤  v2 引擎，把循环、⼯具调度和上下⽂管
理组织成⼀组  DI Service ， Plan 、 Swarm 等功能可以按需注⼊。 DSH 则
把  ReactLoopAgent  本身注册成  Cordis 插件， Loop 与模型  Provider 、⼯具等服务采⽤同
⼀种装卸⽅式。 Kimi Code 的重⼼是⼀款可扩展的终端  Agent ， DSH 留给开发者的改造范
围更⼤，连  Agent 怎样循环都可以替换。
第⼆组是会话记录。 Kimi Code v2 通过  wire.jsonl  保存  Agent 边界上的事件， DSH 也
⽤  Session Event 恢复状态和驱动界⾯。 DSH 还增加了⼀条运⾏时约束，模型看⻅的内容
必须已经写进⽇志。这就是  Trajectory 能还原请求、⼯具调⽤和  token 变化的原因。
第三组是⼯具与执⾏环境。 Kimi Code ⽤  Agent Profile 控制⼯具范围，再通过  KAOS 抽象
本地与  SSH 环境。 DSH ⽤  Preset 决定⼯具和提示词，再把⽂件系统、⼦进程和  sandbox
拆成可替换服务。两边都能换模型和执⾏位置， DSH 更强调更换这些底层服务时，上层⼯具
保持不动。
所以，两套项⽬都有插件、事件⽇志和环境抽象，差别主要在开放到哪⼀层。 Kimi Code 优
先把终端编码体验调好， DSH 则把更多运⾏时部件交给开发者重新组合。这也解释了同⼀个
Kimi K3 在两边都能过题，执⾏步骤和⽇志形态却明显不同。
同⼀个  V4 Pro ，两个  Harness 各做⼀款跳⼀跳
前⾯的两道⼩题适合看⼯具轨迹，还不⾜以观察  Harness 怎样影响完整产物。这⼀轮固
定  deepseek-v4-pro API 、 Prompt 和验收要求，让  DSH 与  Kimi Code 在两个独⽴⼯作
区⾥各做⼀款原创跳⼀跳游戏。
同⼀个  Kimi K3 最终都过题，⾛法已经明显不同。 Kimi Code 更像已经调好的成品。
DSH minimal 更容易冻住前缀、换掉⼯具和  provider 、把实验复现出来。
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
任务不只要求画出⼀个⽹⻚。玩家要能⽤⿏标、触摸和空格蓄⼒起跳，游戏要处理平台碰
撞、 Perfect 奖励、连击、失败与重开。项⽬还要带⼀个零依赖  Node.js 后端，提供排⾏
榜、统计、 JSON 持久化、输⼊校验和路径防护，并留下确定性测试接⼝。参考  VISTA  的思
路，最终验收同时看代码测试、真实浏览器⾏为和画⾯。
先看最终结果。 Kimi Code 做成了全屏  2.5D ⽅块舞台， DSH 做成了  2D 横向画布，右侧放
排⾏榜和操作说明。
图  3 　同⼀模型、同⼀  Prompt 的最终游戏界⾯。左侧为  Kimi Code ，右侧为  DSH ，均来⾃真实浏
览器运⾏态。
两个⻚⾯均为前端单⽂件版本，游戏可以直接运⾏；排⾏榜与统计功能仍需配套  Node 后
端。
我⾃⼰也各玩了⼏局。两个版本都不只是能打开，蓄⼒、落点和连续跳跃已经有了⼩游戏该
有的⼿感。 Kimi 版的舞台感更强， DSH 版更像⼀个带完整信息区的  Web 游戏。
两套  Harness 都完成了前端、后端、排⾏榜持久化和⾃动测试，过程却不⼀样。 DSH 分三
段  session 完成，合计约  25 分钟、 85 个  step 和  96 次⼯具调⽤，交付  19 项后端测试。
第⼀次运⾏中断后，它能够接着补⻬约  880 ⾏游戏逻辑和浏览器  smoke test 。
Kimi Code 初次⽣成约  14 分  30 秒，算上两轮修复约  21 分钟，交付  17 项后端测试。它的
初版已经有完整的  2.5D 视觉⻛格，后续根据真实浏览器反馈修复了  updateHUD 调⽤和遮
罩层显示问题。
这次评测留下三点印象。
第⼀，同⼀个模型和同⼀份  Prompt ，最终仍然⻓成了两种产品。 Kimi Code 更偏向全屏游
戏体验， DSH 更偏向带排⾏榜和说明区的完整⻚⾯。⼩样本⽆法证明这是稳定倾向，但⾜以
说明  Harness 会参与塑造产物。
第⼆，两边都能承载⼆⼗分钟左右、有前后端、有测试、需要中途修复的任务。 DSH 的固定
物理步⻓、 seeded PRNG 和原⼦写⼊， Kimi Code 的  2.5D 舞台与完整交互，都已经超过
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
⼀次性⻚⾯  Demo 。
第三，两边都出现过模型⾃测通过、真实浏览器失败。 DSH 的  canvas backing store 尺⼨
错误，画⾯只剩天空。 Kimi Code 先遇到函数归属错误，随后⼜被  CSS 覆盖了  hidden  属
性。问题反馈给  V4 Pro 后都修好了，也给各⾃的浏览器测试补上了回归检查。
这条共同的失败最值得记住。 Agent 写的测试很容易和实现共⽤盲点。 Harness 可以保留完
整轨迹，也能帮助模型继续修正，最终仍要靠独⽴浏览器、外部验收和⼈眼试玩来确认产物
真的可⽤。
DSH 也能驱动其他模型
DSH 同时提供  DeepSeek 直连适配器和基于  pi-ai 的多  Provider 适配器。本机分别使⽤
Kimi K3 、 GPT-5.6 Sol 和  Claude Opus 4.8 完成了⽂件写⼊、读回与⼯具调⽤。
这项冒烟只说明  provider 、 OpenAI-compatible 消息、 SSE 和⼯具协议可以⼯作，不⽤来
⽐较三种模型。实际接⼊仍应逐个验证⽂本、流式、⼯具调⽤、错误映射和⻓连接。
这些体验在源码⾥从哪来
仓库采⽤  TypeScript monorepo 。主⼲可以先压成这⼏层。
deepseek-harness/
├── apps/cli + apps/web        命令⾏与浏览器⼊⼝
├── packages/boot + bundle     Profile 与插件树组装
├── packages/core/
│   ├── agent-loop             Turn / Step 驱动
│   ├── session                追加式事件⽇志
│   ├── tools                  ⼯具注册与执⾏
│   └── system-prompt          Prompt ⽚段组装
├── packages/preset            每会话  Agent 组合
├── packages/llm               DeepSeek 与多  Provider 适配
├── packages/fs + sandbox      可替换执⾏能⼒
├── packages/code-runtime      PTC / Code Mode
└── vendor/cordis              插件⽣命周期底层
这张图能解释  DSH 的技术栈。 Cordis 管插件⽣命周期和服务依赖， DSH 在上⾯定义
Agent 领域的  session 、 loop 、 tools 、 LLM 、 sandbox 和  UI 。 KM 的运⾏时拆解对
Fiber 、 Preset 、 Code Mode 与⼯具遮蔽有更细的源码映射，这⾥只留和使⽤体验最相关的
五点。
⼀切皆插件，靠的是  Cordis 的可逆⽣命周期
代码⼊⼝在  vendor/cordis/src/context.ts、fiber.ts  与  service.ts。
插件通过  inject  声明依赖的服务。依赖没出现时， Fiber 停在  PENDING。服务出现后进
⼊  ACTIVE。提供⽅退出时，依赖组件先卸载，再回收⾃身  effect 。
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
每次注册服务、监听器或定时器，都要把  disposer ⼀起交给  ctx.effect()。卸载时按相
反顺序清理。 Agent Loop 能成为普通插件，前提正是底层已经能管住这种体量组件的加
载、依赖和退出。
这个机制也有明确边界。外部⽂件、⽹络消息和已经发⽣的业务动作不会⾃动回滚。依赖注
⼊也⽆法替代恶意代码沙箱。
Profile 与  Preset 分别控制进程和会话
代码⼊⼝在  packages/boot/app-boot/src/profile.ts  与  packages/preset/agent-
presets/src/。
Profile 从空列表开始叠  bundle ，再应⽤  profile 、 home 和命令⾏  patch 。 Web 与
Headless 因此是两棵不同的插件树。dsh --profile web --dump-config  使⽤同⼀套
patch 算法输出最终结果，配置展示和真实启动不会各维护⼀套逻辑。
Preset 再决定某个会话看⻅哪些⼯具、提示词和投影单元。同⼀个进程⾥可以同时跑
standard 、 minimal 或领域  Agent 。前⾯  Data Agent ⽤  sqlcmd 替换  bash ，就是这套作
⽤域落到产品上的例⼦。
模型看⻅的内容，必须能从⽇志重建
代 码 ⼊⼝在   packages/core/agent-loop/src/agent.ts 、
invariant.ts  与  packages/core/session/src/。
每⼀步请求都从  session 派⽣  messages 。请求发出前， invariant 会再⽐较当前请求
与  session.deriveMessages()，并核对模型、 system prompt 、 temperature 、 max
tokens 和  tools 。
const expected = session.deriveMessages()
if (JSON.stringify(options.messages) !== JSON.stringify(expected)) {
  fail('log-reconstruction desync')
}
这条约束解释了  Trajectory 为什么清楚，也解释了  fork 、恢复和  UI 为什么能共⽤同⼀条事
件流。它还带出⼀条隐私含义。上下⽂⼀旦注⼊模型，也会进⼊⽇志和数据边界。
Capability Seam 把⼯具与执⾏环境拆开
代码⼊⼝在  packages/fs/fs/src/types.ts、fs-local/、fs-sandbox/  与  tool-
str-replace-editor/。
⽂件系统先定义  FileSystem 、 opaque target 和  version ，再由  local / sandbox
provider 实现，最后由  read 、 write 、 editor 消费。把⽂件与⼦进程  provider 换到远程沙
箱时，上层⼯具不必跟着  fork 。
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
写⼊还⽀持  createIfAbsent  与  replaceIfVersion。模型读完⽂件以后，若⽂件已被
别⼈改过， provider 可以拒绝陈旧覆盖。并发安全因此落在⼯具下⽅，不必由每个编辑⼯具
再写⼀遍。
PTC ⽤代码减少⼯具往返
代码⼊⼝在  packages/code-runtime/。
PTC 让模型写⼀段  TypeScript 来组合多次⼯具调⽤。程序在  worker_threads  中执⾏，
⼯具请求通过消息通道回到宿主，仍然经过同⼀套  pre-execute 、审批、调度和  post-
execute 流⽔线。
中间数据可以留在运⾏环境⾥，不必每⼀步都塞回模型上下⽂。这⽐模型会写代码更要紧。
代价是执⾏模型⽣成的代码需要额外隔离， worker 仍不是完整安全边界。
现在谁值得花时间
做  Agent 基础设施的⼈值得⻢上看。 DSH 把  loop 、 session 、 provider 、⼯具和  UI 都摊在
能核对的源码⾥。
需要领域  Agent 的团队值得做⼩实验。先复制  minimal / standard preset ，再删⼯具、换
provider ，⽐迁移整套⼯作流更容易验证收益。
模型评测⼈员可以⽤  minimal composition 。同时锁定模型版本、推理档位、 endpoint 和
外部验收。
只想找⽇常编码⼯具的⼈可以先观望。 Kimi Code 、 Claude Code 、 Codex 等产品在终端体
验、桌⾯⼊⼝、 IDE 集成和默认⼯作流上更成熟。
⽣产接⼊要⾃⼰补治理。插件来源、配置  diff 、凭证边界、 Windows 验收、⽇志保留和数据
外发，都得部署⽅承担。
如果团队正在设计⾃⼰的  Harness ，还可以带⾛三个问题。
1. 运⾏时最终加载了什么，能不能⼀条命令打印出来
2. 模型实际看⻅了什么，能不能从⽇志完整重建
3. 换掉⽂件系统、沙箱或模型提供⽅时，有多少⼯具必须跟着改
这三个问题， DSH 已经给出能跑、能核对的答法。默认产品、插件质量和治理能不能追上这
套结构，是下⼀阶段的事。
资料汇总
官⽅与源码
DeepSeek Harness 源码
中⽂架构⽂档
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
Python SDK 最⼩  Agent 指南
Cordis 源码
时空可组合性论⽂
V4  Pro 0813 模型卡
Kimi Code CLI 源码
⽤户反馈与⽅法
知乎⽬标问题
⼀周内测与  89 步竞赛任务
默认⼯具与  token 开销估算
87.6 分钟接⼊微信记录
Data Agent 的  Preset 实践
VISTA 视觉  Web App Benchmark
本地复现材料
基础结果　working/eval/results.md
Kimi K3 对照　working/cross-model/harness-compare/
Kimi Code 源码快照　working/kimi-code/
多模型冒烟　working/cross-model/compat/
V4 Pro 跳⼀跳  Case 　working/jump-game/workspace/
知乎反馈摘录　working/eval/zhihu-feedback.md
KM 图⽚与  HTML 附件　output/attachments/
全部数字以  2026-08-14 的单次本机运⾏结果为界。
📦  完整复现材料获取⽅式：
关注「腾讯技术⼯程」公众号，在后台私信关键词 「 deepseek 」，即可获取。
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
阅读 1 . 6 万 修改于2026 年 8 ⽉ 15 ⽇
留⾔
还没有留⾔，来写⾸评
写留⾔
````

