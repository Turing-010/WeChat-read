# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
DeepSeek  Harness 规模化踩坑实录：耗时、成本、失败到底该怎
么查
腾讯云⽇志服务 2026 年 8 ⽉ 24 ⽇ 02 : 36⼴东腾讯技术⼯程 129 ⼈
作者：trumphuang
⼀、导语
Agent  已经进⼊不少团队的⽇常研发流程。规模上来之后，使⽤⽅的关注点不再只是单次结果是否正确，还
包括三件事：耗时花在模型推理还是⼯具执⾏上； Token  消耗集中在哪些会话、哪些模型上；失败与中断发
⽣在哪⼀步，过程是否可以回溯。
DeepSeek  Harness （下⽂简称 DSH ）是 DeepSeek  开源的 Agent  框架，⾃带会话轨迹视图、 Session  事
件流落盘与⼯具调⽤检索，作⽤域是本机、单会话、实时；⼀旦要看⼀批任务的整体表现、⼀段时间的成本
分布，或复现⼏天前的⼀次失败，就需要跨会话、跨机器且可⻓期留存的结构化链路数据。
腾讯云 Agent  可观测在已有的 OneSuite Agent  观测能⼒基础上，提供了针对 DSH  的采集插件：以原⽣插
件形态挂载，将执⾏过程还原为结构化调⽤链，覆盖任务与推理轮次、模型调⽤、⼯具调⽤、会话关联，配
合链路检索、聚合分析与平台本身的告警仪表盘等能⼒，构成针对 DSH  的全景 Agent  可观测⽅案。
⼆、 DeepSeek  Harness  的运⾏原理
DSH  是⼀个开源的编码 Agent  框架，命令⾏名 dsh ，⽤于让⼤模型在受控环境中⾃主完成⼀个完整任务：
读写⽂件、执⾏命令、调⽤外部服务，并根据每⼀步的结果决定下⼀步动作。
组织⽅式上， DSH  采⽤ Cordis 微内核加全插件化：内核只负责按 profile  装配插件与管理⽣命周期，模
型适配器、⼯具集、沙箱策略、会话持久化等均为可插拔插件， web  / tui  / headless  三种形态共⽤同⼀个
内核，可观测能⼒同样挂载在这⼀层。
执⾏模型是 ReAct  循环：⼀次⽤户任务称为⼀个 turn ， turn  内的每⼀轮推理、调⽤⼯具、观察结果称为⼀
个 step。循环轮数与调⽤哪些⼯具由模型在运⾏时决定，因此执⾏结构在运⾏前⽆法确定。
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
图1 DSH 的分
层结构、⼀次 turn 的执⾏时序，以及对外的两条数据产出
2 . 1  DSH  ⾃带了什么
基于上述事件流与落盘数据， DSH  ⾃身提供了三项开箱即⽤的观测能⼒：
会话轨迹——浏览器内按轮次组织的执⾏记录表，可查看单条记录的 Token  ⽤量与耗时。
Session  事件流落盘——完整事件流以 zstd  压缩的 JSONL  落盘于 $ DSH _ HOME / sessions /，数据⽆
损。
⼯具调⽤检索——⼯具的调⽤参数与返回结果记录在事件流中，并⽀持会话全⽂检索。
 图2 DSH ⾃
带的会话轨迹视图 
2 . 2  为什么还需要在这份数据之上完善调⽤关系
DSH  的过程数据是按时间排列的会话事件序列，且保存在本机：⽬前暂时没有调⽤关系与各⾃的时间占⽤统
计，在实际业务部署规模扩⼤后随着机器数量增⼤，三个问题会变得突出：
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
实现这些能⼒的共同前提是把⼀次任务还原成⼀棵带⽗⼦关系与时间区间的调⽤树，并让数据可以跨会话、
跨机器汇聚与⻓期留存。
三、腾讯云 Agent  可观测提供了什么
基于⽬前已有的 OneSuite  Agent 能⼒基础上，提供⼀个 DSH  插件挂载在 DSH 能⼒插件层，对接运⾏时的事
件总线与流式管道，聚焦做三件事：
订阅——订阅⽣命周期事件，并在模型流式管道上包⼀层中间件，逐块观察⽽不改变数据，不插桩、不
改代码。
建模——在插件内维护状态树，把散落的事件还原成五层调⽤树，映射为符合 OpenTelemetry  GenAI
语义约定的 Span 。
上报——数据批量直传腾讯云 Agent  可观测，不经过 Collector  或常驻采集进程。
3 . 1  数据地基：五层调⽤树
插件上报的调⽤链路分成五个层级，与 DSH  的实际执⾏结构⼀⼀对应：⼀个 turn  对应⼀次任务， turn  内
有若⼲ step ， step  内有模型调⽤与⼯具调⽤。
 图3 五层
Span 模型与各层承载信息
⼀次 turn  ⼀条 trace——多轮对话通过 gen _ ai . session . id  横向关联，避免⻓会话产⽣⽆限膨胀的单条
链路。
重试不被合并——每次真实模型调⽤⽣成独⽴ chat  Span ，以 dsh . llm . attempt  标记序号。
中断也画完整——流未收尾、 step  先于⼯具结束、⽤户中断等场景均补发带错误码的 Span 。
各层属性均遵循 OpenTelemetry  GenAI  语义约定，便于与既有可观测体系对⻬，也便于后续接⼊其他
Agent  框架时保持同⼀套⼝径。
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
图4 整体技术架构与数据路径
Agent  的执⾏结构由模型在运⾏时决定，层级深度不固定，⽽链路数据要求⽗⼦关系明确、时间区间完整。
插件通过状态树与延迟发射处理这⼀差异构造整体采集上报能⼒。
图5 ⼀次 turn 的完整处理逻辑：事件流 →  状态树 →  Span 发射 →  批量上报
四、接⼊后腾讯云 Agent 可观测后能看到什么
接⼊后， DSH  的每⼀次任务都会形成⼀条完整链路，并按会话、模型、⼯具等维度汇总：
完整调⽤链—— entry  / agent  / step  / chat  / tool  五层逐层展开，⽗⼦关系与各层耗时占⽐清晰可⻅
耗时分布——端到端与单轮耗时、模型推理与⼯具执⾏各⾃的占⽤，以及⾸ Token  延迟与 P95  分位数
Token  与成本——输⼊、输出分别统计，可下钻到单次模型调⽤，也可按会话、模型聚合排⾏
调⽤明细——模型名称、结束原因与重试次数，⼯具名称、耗时、错误情况统计
失败定位——每层 Span  带独⽴状态并⽀持错误类型⾃定义，可⽤于区分模型侧失败、⼯具侧失败与循
环中断
检索与告警—— Traces  / Spans  / Sessions  三种视⻆，⽀持按 Trace  ID 、 Session  ID  与状态检索，并
可对耗时、失败率配置告警
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
下述为部分能⼒，更多能⼒可在 Agent 可观测控制台体验
图6 可观测⾯板 - Token消耗部分
图7 调⽤链⾯板 - ⼀次完整的DeepSeek Harness任务执⾏过程
五、接⼊实践
⽬前 tencentcloud - agentobs - sdk - dsh 已发正式版本，并已被 DSH  社区插件市场收录（当前版本⽀持 DSH
>= 0 . 1 . 0 - rc . 6  < 0 . 2 . 0 ，要求 Node . js  >= 22 . 19 . 0 ）
前提条件
已开通⽇志服务 CLS，并准备好具备⽇志写⼊权限的访问凭证，建议使⽤ CAM  ⼦账号或临时密钥。
已安装 DSH ，版本在 >= 0 . 1 . 0 - rc . 6  < 0 . 2 . 0  区间内；插件运⾏环境的 Node . js  为 18 . 0 . 0  或更⾼。
创建 Agent  可观测应⽤
1 .  登录⽇志服务控制台，在左侧导航栏中选择 Agent  可观测，单击 应⽤接⼊ 创建应⽤，接⼊⽅式选择
DeepSeek  Harness
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
2 .  进⼊应⽤详情，在⽇志主题列表中找到名称为 {应⽤名称}- trace - topic  的⽇志主题。
3 .  复制该⽇志主题 ID ，⽤于后续配置中的 CLS _ TOPIC _ ID  或 topicId 。
⽅式⼀：通过 Skill 安装+配置
复制以下提示词到 AI  ⼯具，让它在你的项⽬⽬录中完成 DeepSeek  Harness 接⼊。
⽅式⼆：⼿动安装+配置
前置依赖
全局安装 DeepSeek  Harness  CLI ：
安装插件
注意：安装或更新插件后，需要重启 DSH  服务才能⽣效。
pnpm  构建脚本问题
pnpm  v9 + 默认禁⽌依赖包运⾏ install  脚本。如果安装时遇到以下错误：
1
2
3
4
5
请使⽤腾讯云  Agent  可观测接⼊  Skill：
https://skillhub.cn/skills/tencentcloud-cls-agent-obs
帮我把当前  AI  应⽤接⼊腾讯云  Agent  可观测。
接⼊⽅式：DeepSeek Harness
Region： ap-guangzhou
1npm install -g @deepseek-ai/dsh
1
2
3
dsh plugin --profile web add tencentcloud-agentobs-sdk-dsh
dsh plugin --profile headless add tencentcloud-agentobs-sdk-dsh
dsh plugin --profile harness add tencentcloud-agentobs-sdk-dsh
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
在对应 profile  ⽬录执⾏⼀次即可（后续安装/更新不再需要）：
headless  / harness  profile  同理，将路径改为 ~/. dsh / profiles / headless  或 ~/. dsh / profiles / harness 。
配置连接信息
⽅式⼀：环境变量（推荐）
⽅式⼆：⼿动调整插件配置⽂件
编辑 $ DSH _ HOME / profiles /< profile >/ cordis . patch . yml ，未设置 DSH _ HOME  时默认为
~/. dsh / profiles /< profile >/ cordis . patch . yml ：
显式插件配置优先于环境变量。以及访问凭证属于敏感信息，建议通过环境变量或密钥管理⼯具注⼊，不
要将真实 SecretId  与 SecretKey  提交到代码仓库。
1
2
[ERR_PNPM_IGNORED_BUILDS] Ignored build scripts: protobufjs@6.11.6
Run "pnpm approve-builds" to pick which dependencies should be allowed t
1
2
3
cd ~/.dsh/profiles/web
echo "enable-scripts=true" >> .npmrc
pnpm install
1
2
3
4
5
6
7
export CLS_ENDPOINT=ap-guangzhou.cls.tencentcs.com
export CLS_TOPIC_ID=your-topic-id
export CLS_SECRET_ID=your-secret-id
export CLS_SECRET_KEY=your-secret-key
export CLS_SERVICE_NAME=dsh-agent    # 可选，⽤于区分实例或业务
 
dsh --profile web
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
- id: cls-observability
  config:
    endpoint: ap-guangzhou.cls.tencentcs.com
    topicId: your-topic-id
    secretId: your-secret-id
    secretKey: your-secret-key
    serviceName: dsh-agent
    captureContent: true
    batchMaxSize: 32
    flushIntervalMs: 5000
    debug: false
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
启动并验证
启动后发起⼀次测试任务，⾄少触发⼀次模型调⽤
卸载插件
关闭内容捕获
默认情况下， prompts 、 responses 、 tool  arguments / results  会附加到 span 。如需关闭：
或在插件配置中设置 captureContent : false 。
配置⽂件完整配置项
设置 默认值 说明
enabled true 禁⽤采集但不卸载插件
endpoint CLS _ ENDPOINT CLS  API  接⼊点
topicId CLS _ TOPIC _ ID CLS  ⽇志主题 ID
secretId CLS _ SECRET _ ID 腾讯云 SecretId
secretKey CLS _ SECRET _ KEY 腾讯云 SecretKey
serviceName deepseek - harness服务名
captureContent true 捕获 prompts / responses / tool  内容（设为 false  关闭）
contentMaxChars 128000 单个内容属性最⼤字符数
batchMaxSize 32 每批上报最⼤ span  数
maxQueueSize 2048 队列上限，超限丢弃最旧 span
flushIntervalMs 5000 定时刷新间隔（毫秒）
1dsh --profile web
1
2
3
dsh plugin --profile web remove tencentcloud-agentobs-sdk-dsh
dsh plugin --profile headless remove tencentcloud-agentobs-sdk-dsh
dsh plugin --profile harness remove tencentcloud-agentobs-sdk-dsh
1
2
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=false
dsh --profile web
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
retryTimes 3 上报重试次数
debug false 启⽤调试⽇志
六、腾讯云 Agent  可观测还提供哪些接⼊⽅式与能⼒
DSH  插件是接⼊形态之⼀。除此之外，腾讯云 Agent  可观测还提供以下上报⽅式，它们写⼊同⼀套数据模
型，可在同⼀个控制台内查看与横向对⽐：
⽬前接⼊⽣态正在持续丰富中，逐步⽀持通⽤ Agent 框架（如 langchain 、 OpenAI  Agent  SDK 等）和
Coding  Agent （如 CodeX 、 ClaudeCode 等）中
数据上报后，控制台侧已提供的分析能⼒：
应⽤列表——已接⼊应⽤、上报中应⽤、昨⽇写⼊量与昨⽇ Token  总数，以及各应⽤的地域、状态与接
⼊类型。
仪表盘——总览（请求数与错误数、模型调⽤次数、 Input / Output  Tokens 、 Agent  与模型 Top10 、平
均 TTFT ）、性能（耗时直⽅图与 P50 / P90 /P99 分位趋势、模型平均耗时 Top10 ）、成本 &
Token 、应⽤观测（按 generation  / tool  / chain  / agent  / retriever  / guardrail  / event  等类型分析调
⽤分布与耗时）。
调⽤链—— Traces  与 Span 两种视图，可按状态、错误类型（⼯具调⽤失败、 LLM  调⽤失败、 Root
span  状态码异常、 Agent  执⾏失败）、 Trace  ID 、 Session  ID  与耗时筛选，详情⻚提供调⽤树、节点
Input / Output  与错误根因定位。
会话——按 Session  聚合 Trace ，⽀持按会话时⻓、 Trace  数、 Token  与成本筛选，还原多轮对话上下
⽂。
告警能⼒——⽀持对常⽤指标⽐如可对耗时、失败率等异常情况配置告警
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
七、总结
DSH  原⽣的轨迹视图与事件流落盘，解决的是本机、单会话、实时的调试问题；本⽂⽅案在此基础上把同⼀
批运⾏时事件还原为结构化的五层调⽤链，补充跨会话聚合、跨机汇聚、⻓期留存与告警能⼒，帮助⽤户快
速搭建针对 DeepSeek  Harness 的运维观测体系。
项⽬ GitHub ：
https :// github . com / TencentCloud / tencentcloud - agentobs - sdk - dsh
相关接⼊指南：
Agent  可观测应⽤详情：
https :// cloud . tencent . com / document / product / 614 / 133517
接⼊ AI  Coding  Agent  数据（ Onesuite - Pilot ）：
https :// cloud . tencent . com / document / product / 614 / 135910
使⽤ Langfuse  SDK  上报 Trace  数据到 CLS ：
https :// cloud . tencent . com / document / product / 614 / 133518
有任何关于 Agent  可观测的问题和建议，欢迎⼊群交流 ⬇
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
阅读 1 . 7 万
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
留⾔
还没有留⾔，来写⾸评
写留⾔
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
````

