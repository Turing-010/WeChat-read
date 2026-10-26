# Agent 长程任务断点续传：从框架 Checkpoint 到跨进程恢复的完整实践：PDF文本转写

> 这是RAW.pdf的文本层转写，不是AI总结。页码为PDF物理页码；未恢复原版面、表格或代码缩进。文本框长行、缺图与未加载内容不能仅靠文字提取判定完整。

[原始PDF](RAW.pdf) · [外部AI总结](AI_长程任务断点续传.md) · [来源与质量](META.json)

## PDF 第1页

[查看RAW.pdf第1页](RAW.pdf#page=1)

> 本页含2个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
Agent ⻓程任务断点续传：从框架 Checkpoint 到跨进程恢复的完
整实践
原创 直播技术团队 ⼤淘宝技术 Sep 9, 2026, 2:41 AM 浙江 12 listened
本⽂介绍了针对 Agent ⻓程任务中断恢复需求的完整实践⽅案，旨在解决⽤户主动、⼯
具执⾏及系统级中断带来的稳定性问题。该⽅案采⽤“框架层 Checkpoint + 上层任务调
度”的两层架构，在不修改 Spring AI Alibaba 框架源码的前提下，通过扩展
InterruptableAction、利⽤ Hook 机制注⼊⾃定义逻辑（如关机信号检测、消息顺序
修正、多⼯具调⽤ Mock 返回及⼦图会话 ID 记录）来实现进程内的状态保存与恢复；同
时，上层调度通过 MQ 摘流防⽌关机机器消费新消息，并结合任务表与 MQ 消息队列协
调跨进程的任务恢复，有效覆盖了包括⼈机协作、多 Agent 协同及系统重启在内的多种
复杂中断场景，保障了 Agent 系统的稳定⻓期运⾏。
背景
▐ 1.1 业务场景
对于 Agent 系统⽽⾔，确保任务稳定可靠地执⾏是核⼼诉求。在Agent的 ReAct 循环执⾏过程
中，不同任务对中断恢复能⼒有着差异化的需求：
长程任务：例如在实际⽣产项⽬中，⼀次完整的业务流程涉及多个步骤，执⾏时间不可控，
需要从中断点恢复
A2A 协同任务：多 Agent 协同编排，偏向系统⾃治，是长程任务中的关键环节。这类任务中
断后⽆法依赖⽤户⼿动⼲预，同样需要中断恢复能⼒
⼈机协作场景（Human-in-the-loop）：执⾏过程中需要⼈⼯介⼊，如权限控制、问题澄清
等，任务暂停等待⼈⼯确认后继续执⾏，核⼼是安全可靠的中断机制
⽬前直播技术业务中，许多Agent服务对上述三类场景均有涉及，为保障系统稳定长期运⾏，对
系统的中断恢复能⼒提出了较⾼的要求。
```

## PDF 第2页

[查看RAW.pdf第2页](RAW.pdf#page=2)

> 本页含1个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
▐ 1.2 中断的分类与影响
长程任务的核⼼风险是中断。⽣产环境中的中断⼤致可分为三类：
⽤户主动中断和⼯具执⾏中断属于协作式中断，框架可通过 Hook 机制在节点执⾏前后检测并
保存 Checkpoint；系统级中断属于⾮协作式中断，需要上层调度配合 MQ 消息队列协调恢
复。
⻓程任务执⾏时间不可控、上下⽂状态庞⼤，中断后⽆法通过简单重试恢复，必须从断点续
传。同时，稳定的中断机制本身也是前提——若未在合适的拦截点将任务稳定中断，可能导致
状态不⼀致，恢复时⽆法判断已完成与待重试的步骤边界。
恢复策略需根据场景差异化设计：⼈机交互场景下由⽤户触发恢复，过程可⻅可控；多 Agent
协同场景下⽆法依赖⼈⼯⼲预，需要系统⾃动恢复。两层架构中，底层依赖框架层
Checkpoint 保存与恢复，上层根据场景选择恢复触发⽅式。
▐ 1.3 其他⽅案调研
通过基建层⾯解决⻓程任务中断问题的⽅案：
蓝绿发布 + 摘流等待⽅案：发布时对新旧机器做蓝绿切换，旧机器停⽌接收新流量，但保持
运⾏状态，等待其上所有⻓程任务执⾏完毕后再进⾏机器回收。该⽅案的核⼼思路是避免中断
发⽣，⽽⾮中断后恢复。
局限性：
⻓程任务执⾏时间不可控，发布周期受限、旧机器可能需要⻓时间保持运⾏，资源成本较
⾼
对于⾮发布场景的中断可能⽆法覆盖
因此本⽅案选择从应⽤层⾯实现断点续传，通过框架层 Checkpoint + 上层任务调度的两层架
构，以更低的成本覆盖更多中断场景。
```

## PDF 第3页

[查看RAW.pdf第3页](RAW.pdf#page=3)

> 本页含3个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
整体架构
图 1：断点续传整体架构。上层调度负责任务状态追踪与恢复协调，
框架层负责 Checkpoint 的保存与恢复。
框架层：Checkpoint 机制深度利⽤
▐ 3.1 框架 Checkpoint 机制分析
Spring AI Alibaba 框架（以下简称 SAA，当前使⽤版本 1.1.2.0）的 Checkpoint 机制的
保存时机如下：
```

## PDF 第4页

[查看RAW.pdf第4页](RAW.pdf#page=4)

> 本页含2个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
图 2：框架 Checkpoint 保存时序。每个节点正常执⾏完毕后都会⾃动保存 Checkpoint，唯⼀不保存的
是 __END__ 节点和异常场景。
▐ 3.2 关键设计决策：不改框架源码
⽅案的核⼼约束是完全基于框架已有能⼒实现断点续传，不修改任何框架源码。框架是公共依
赖，修改源码意味着维护私有 fork，后续升级成本极⾼。⽅案利⽤的框架能⼒：
▐ 3.3 关机信号检测：GraphEnvironmentMonitor
```

## PDF 第5页

[查看RAW.pdf第5页](RAW.pdf#page=5)

> 本页含0个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
新增轻量级⼯具类 GraphEnvironmentMonitor ，⽤于检测应⽤内的关机信号共享变量是
否被设置。
关机信号的触发链路如下：
1. 应⽤执⾏下线脚本，会调⽤到应⽤的下线脚本⽂件
2. 下线脚本在执⾏应⽤停⽌前，通过 HTTP 请求调⽤应⽤内的关机信号接⼝（如 /check/
shutdown/signal ）
3. 应⽤接收到该请求后，将内存中的共享变量置为下线状态
4. GraphEnvironmentMonitor.isShutdownSignalDetected() 检测到该变量被
设置，返回 true
正在执⾏的 Agent 任务会在当前节点完成后检测到关机信号，触发中断并保存 Checkpoint。
▐ 3.4 恢复时消息顺序问题（已修复）
断点续传场景中存在⼀个问题：恢复执⾏时，⽤户新发的消息可能被插⼊到消息列表的第⼀条
⽽ 不 是 最 后 ⼀ 条 ， 导 致 模 型 上 下 ⽂ 错 乱 。 这 是 框 架 的 ⼀ 个 bug （ 提 的
issue: https://github.com/alibaba/spring-ai-alibaba/issues/4662 ）。
该问题已在社区修复。 对于使⽤旧版本的场景，可以通过 ResumeMessageOrderHoo
k 在 BEFORE_MODEL 阶段拦截来实现：
1 @HookPositions({HookPosition.BEFORE_MODEL})
2 @Component
3 public class ResumeMessageOrderHook extends MessagesModelHook {
4 @Override
5 public AgentCommand beforeModel(List<Message> previousMessages, Ru
6 // 检测是否是恢复请求
7 Optional<Map<String, Object>> customInfoMap = ITool.getCustomI
8 if (customInfoMap.isEmpty()) {
9 return new AgentCommand(previousMessages, UpdatePolicy.REP
10 }
11 Object pendingUserMsgObj = customInfoMap.get().get("pendingUse
12 if (!(pendingUserMsgObj instanceof String pendingUserMsg) || p
13 return new AgentCommand(previousMessages, UpdatePolicy.REP
14 }
15 // 构造新消息列表：原有消息 + 追加⽤户消息到末尾
16 List<Message> newMessages = new ArrayList<>(previousMessages);
17 newMessages.add(new UserMessage(pendingUserMsg));
18 customInfoMap.get().remove("pendingUserMessage");
19 return new AgentCommand(newMessages, UpdatePolicy.REPLACE);
20 }
```

## PDF 第6页

[查看RAW.pdf第6页](RAW.pdf#page=6)

> 本页含1个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
21 }
建议：优先升级框架版本，避免引⼊额外的 Hook 组件。
▐ 3.5 多⼯具调⽤的 Checkpoint 限制
当模型返回多个⼯具调⽤（如 toolA、toolB、toolC）时，框架在⼀个 for 循环中顺序执⾏所
有⼯具，中间不保存 Checkpoint。
图 3：多⼯具调⽤场景的 Checkpoint 保存时机。
如果 toolA 执⾏完、toolB 执⾏中崩溃，恢复时三个⼯具全部重新执⾏。
框架在 AgentToolNode 中已内置部分⼯具恢复能⼒——它会检测哪些⼯具已经执⾏过，
只执⾏剩余的。但由于⽆法在 for 循环中间保存 Checkpoint，这个能⼒暂时⽆法被利⽤。
Tool Mock 返回与 Checkpoint 的配合
多⼯具调⽤中间⽆法保存 Checkpoint，但在中断场景下，通过 ToolRecordIntercepto
r 实 现 了 折 中 ⽅ 案 ： 当 检 测 到 任 务 被 中 断 时 ， 未 执 ⾏ 的 ⼯ 具 返 回 mock 响 应
（status="error"），该 mock 响应通过 Checkpoint 机制保存到状态中。
```

## PDF 第7页

[查看RAW.pdf第7页](RAW.pdf#page=7)

> 本页含1个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
图 4：Tool Mock返回与Checkpoint配合
效果：任务重新拉起时，框架能够识别哪些⼯具已有结果（包括 mock 响应），哪些需要重
试。已完成的⼯具不会重复执⾏，mock 的⼯具会在恢复时重新执⾏。这在多⼯具场景下显著
减少了重复⼯作。
⼯具执⾏循环的中断跳过机制
在中断场景下，如何让⼀次模型推理产⽣的多个⼯具调⽤链快速跳过？本⽅案借助异常机制 H
umanInterventionException 配合 ToolInterceptor 实现。
当某个⼯具执⾏过程中需要中断（如权限校验失败、Human-in-the-loop 需要⼈⼯确认），
ToolInterceptor 会抛出 HumanInterventionException 。 ObservationInt
erceptor 捕获该异常后执⾏以下操作：
1. 调⽤ agentInterruptManager.interrupt() 设置中断标记
2. 通过 SSE 发送中断通知（对话框弹窗或表单⻚⾯）
3. 返回 mock 的⼯具响应（status="error"）
中断标记设置后，后续⼯具的 ToolRecordInterceptor 在执⾏前会检测到该标记，直
接跳过⼯具执⾏并返回 mock 响应。这样，⼀次模型推理产⽣的多个⼯具调⽤链就被快速跳
过，⽆需等待每个⼯具逐⼀执⾏。
HumanInterventionException ⽀持多种中断场景：
```

## PDF 第8页

[查看RAW.pdf第8页](RAW.pdf#page=8)

> 本页含0个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
权限不⾜：抛出异常并携带权限申请链接
表单填写：携带表单协议信息 ，前端渲染表单⻚⾯
对话框确认：携带对话框协议信息，前端渲染确认弹窗
该机制的核⼼价值在于：通过异常快速跳出⼯具执⾏循环，配合中断标记让后续⼯具⾃动跳
过，最终通过 Checkpoint 保存完整的⼯具响应状态。恢复时，框架能够根据已有的⼯具响应
识别哪些需要重试。
▐ 3.6 框架层恢复机制
框架的 Checkpoint 恢复由 GraphRunnerContext 构造函数⾃动触发。当运⾏时
metadata检测到 checkPointId 或 HUMAN_FEEDBACK 标记时，⾃动进⼊ initiali
zeFromResume 分⽀，从持久化的 Checkpoint 中恢复执⾏状态：
1 GraphRunnerContext(initialState, config, compiledGraph)
2 │
3 ├── config 有 checkPointId 或 HUMAN_FEEDBACK ?
4 │ ├── 是 → initializeFromResume()
5 │ │ ├── 从 BaseCheckpointSaver.get(config) 获取 Checkpoint
6 │ │ ├── 恢复 overallState = initialState.input(checkpoint.
7 │ │ ├── 设置 nextNodeId = checkpoint.getNextNodeId()
8 │ │ └── 设置 resumeFrom = checkpoint.getNodeId()
9 │ └── 否 → initializeFromStart()
恢复时通过 RunnableConfig.threadId 关联 Checkpoint，⽆需额外传递 Checkpoint
ID。框架会根据 threadId 从 BaseCheckpointSaver 中查询最新的 Checkpoint 记录，
⾃动恢复完整的执⾏上下⽂（包括 state、消息历史、当前节点 ID 和下⼀节点 ID），从中断
点继续执⾏。
▐ 3.7 ⼦图会话 ID 后缀问题
在多 Agent 嵌套编排场景下，当⽗ Agent 内部调⽤⼦ Agent（以嵌套⼦图形式）时，⼦图中
的 RunnableConfig.threadId() 会被框架⾃动拼接后缀，导致中断恢复和状态查询时
出现不⼀致。
问题现象：
原始 threadId：
```

## PDF 第9页

[查看RAW.pdf第9页](RAW.pdf#page=9)

> 本页含0个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
1 plugin_xxx
进⼊⼦图后变成：
1 plugin_xxx_subgraph_SUB_AGENT_A
根本原因：
SAA 框架在执⾏嵌套⼦图时，为了确保状态隔离和可恢复性，会⾃动为⼦图的 threadI
d 添加后缀。核⼼代码位于框架的 ReactAgent.AgentToSubCompiledGraphNodeAd
apter 中：
1 // 当⽗图和⼦图使⽤同⼀个 CheckpointSaver 实例时触发
2 if (parentSaver.get() == subGraphSaver.get()) {
3 subGraphRunnableConfig = RunnableConfig.builder(config)
4 .threadId(config.threadId()
5 .map(threadId -> format("%s_%s", threadId, subGraphId(nodeI
6 .orElseGet(() -> subGraphId(nodeId)))
7 .nextNode(null)
8 .checkPointId(null)
9 .addMetadata("_AGENT_", subGraphId(nodeId))
10 .build();
11 }
触发条件是：⽗图和⼦图注册了同⼀个 CheckpointSaver 实例。
影响范围：
中断处理： AgentInterruptManager 使⽤ threadId 构建 RunnableConfi
g 调⽤ reactAgent.interrupt() ，如果传⼊的是带后缀的 ID，可能导致中断失效
状态恢复：从缓存/DB 中根据 conversationId 查询状态时，如果 key 不匹配则⽆
法恢复
⽇志追踪：⽇志中记录的会话 ID 与实际业务会话 ID 不⼀致，增加排查难度
解决⽅案对⽐：
```

## PDF 第10页

[查看RAW.pdf第10页](RAW.pdf#page=10)

> 本页含2个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
我们选择了⽅案⼆：在 CheckpointAgentHook.beforeAgent() 中将原始 threadId 记
录到 metadata，后续通过统⼀的⼯具⽅法 ITool.getActualThreadId() 获取。这样
既保留了⼦图的状态管理能⼒，⼜解决了 ID 不⼀致的问题。
1 // 在 Hook 中记录原始 threadId
2 @Override
3 publicCompletableFuture<Map<String, Object>> beforeAgent(OverAllState s
4 config.threadId().ifPresent(threadId ->
5 config.metadata().ifPresent(metadata ->
6 metadata.put(AgentConstants.ACTUAL_THREAD_ID, threadId)
7 )
8 );
9 // ... 其他逻辑
10 }
11 // 统⼀获取实际 threadId 的⼯具⽅法
12 staticOptional<String> getActualThreadId(RunnableConfig config) {
13 if (config == null) returnOptional.empty();
14 return config.metadata(AgentConstants.ACTUAL_THREAD_ID).map(String
15 }
优先级链路： ACTUAL_THREAD_ID → 请求对象中的 conversationId 。通过统⼀封
装，避免各处重复实现，同时加 try-catch 兜底，避免因获取失败导致中断等功能异常。
上层调度：跨进程的任务恢复
```

## PDF 第11页

[查看RAW.pdf第11页](RAW.pdf#page=11)

> 本页含0个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
框架层的 Checkpoint 解决了进程内状态保存的问题，但⽆法处理应⽤重启、机器下线等导致
Agent 被强制终⽌的场景。上层调度负责管理任务的跨进程状态——记录被中断的任务，并协
调恢复流程。
▐ 4.1 任务表设计
对于复杂的⻓程任务（如 A2A 多 Agent 协同场景），通过任务表（如 agent_task ）记录
任务的关键请求信息（如 Agent 类型、业务关联键、会话 ID 等），以及过程中的关键⽤户侧
数据，便于任务中断后恢复执⾏。简单的单轮 Agent 交互⽆需引⼊此表，直接依赖框架层
Checkpoint 即可。
▐ 4.2 MQ 摘流：防⽌关机机器消费新消息
上层调度通过 MQ 消息队列分发恢复任务。需要解决的关键问题是：如何保证即将关机的机器
不会消费到新的 MQ 消息？ 如果正在下线的机器消费了恢复任务但未执⾏就关机，任务会再
次成为"孤⼉"。
解决⽅案是在应⽤回调的下线脚本中，先摘流 MQ，再停⽌应⽤。核⼼逻辑如下：
1 offline_mq() {
2 # 检查本地 MQ 客户端管理端⼝是否在监听
3 check_mq=`(/usr/sbin/ss -ln4 sport = :${MQ_ADMIN_PORT}; /usr/sbin/
4 echo"try to offline mq..."
5 if [ $check_mq -ne 0 ]; then
6 echo"start to offline mq...."
7 # 调⽤ MQ 客户端本地管理接⼝，将本实例所有消费者下线
8 ret_str=`curl --max-time ${MQ_ONLINE_TIMEOUT} -s "http://local
9 ifecho"$ret_str" | grep "all clients in instance" &>/dev/null; then
10 echo"mq offline success."
11 return 0
12 else
13 echo"mq offline failed."
14 fi
15 fi
16 }
17 offline() {
18 echo"INFO: ${APP_NAME} try to offline..."
19 rm -f $STATUSROOT_HOME/status.ok # 摘除负载均衡流量
20 offline_rpc # 摘流 RPC 服务
21 offline_mq # 摘流消息队列
22 echo"INFO: ${APP_NAME} offline success"
```

## PDF 第12页

[查看RAW.pdf第12页](RAW.pdf#page=12)

> 本页含2个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
23 return $?
24 }
⼯作原理：
1. 应⽤收到下线信号后， offline() 函数被调⽤
2. 先调⽤ offline_mq() ，通过调⽤ MQ 客户端的 allConsumersOffline 接⼝
3. MQ Broker 会将该消费者从消费组中移除，后续消息不会再分发到这台机器
4. 摘流成功后，再执⾏后续的应⽤停⽌逻辑
效果：即将关机的机器不再消费新消息，这些消息会被消费组中的其他健康机器消费。对于摘
流后、关机前已消费但未来得及执⾏的消息，由于任务状态仍为 WORKING ，新实例启动后
会通过 MQ 重新消费该任务消息，触发恢复流程。
▐ 4.3 恢复流程
恢复由外部MQ消息队列触发：
图 5：恢复执⾏流程。核⼼思路：读 DB 状态 →
从 Checkpoint 恢复框架状态 → 从中断节点继续执⾏。
思考与规划
▐ 5.1 关键设计决策与可复⽤模式
```

## PDF 第13页

[查看RAW.pdf第13页](RAW.pdf#page=13)

> 本页含1个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
⽅案在多个关键决策点上做出了选择：不改框架源码以避免维护私有 fork，升级成本可控；对
于基于SAA框架的React Agent友好，可与原⼯作graph⼯作机制兼容，这些设计模式具有较
⾼通⽤性。
▐ 5.2 遇到的问题与解决⽅案
问题 1：恢复时消息顺序错乱（框架 bug，已修复）。 Checkpoint 恢复后，⽤户新消息被插
⼊到列表第⼀条⽽不是最后⼀条，导致模型上下⽂完全错乱。这是 Spring AI Alibaba 框架的
bug（issue: https://github.com/alibaba/spring-ai-alibaba/issues/4662 ）。社区已在
新版本中修复此问题，建议优先升级框架版本。如暂时⽆法升级，可通过 ResumeMessageO
rderHook 在 BEFORE_MODEL 阶段拦截来 workaround（详⻅ 3.4 节）。
问题 2：多⼯具调⽤中间⽆法保存 Checkpoint。 模型返回 3 个⼯具调⽤，执⾏到第 2 个时
崩溃，恢复后 3 个全部重跑。⽬前通过 ToolRecordInterceptor 在⼯具执⾏前检查中
断标记来缓解（已执⾏的⼯具结果保留，未执⾏的跳过），彻底解决需要框架侧改动。
问题 3：⼦图会话 ID 后缀导致中断失效。 在多 Agent 嵌套编排时，框架会⾃动给⼦图的
threadId 拼接 _subgraph_{agentName} 后缀，导致⽤原始 conversationId 查询中断
状态时找不到记录。解法是通过 Hook 在⼦图执⾏前将原始 threadId 记录到 metadata，后
续统⼀从 metadata 获取（详⻅ 3.6 节）。
▐ 5.3 后续
跟进框架侧多⼯具调⽤中间的 Checkpoint 保存问题，实现⼯具级粒度的断点续传（可能与
Agent scope结合）。此外，框架层⾯存在优化空间，例如 Human-in-the-loop（HITL）扩
展机制的完善（issue: https://github.com/alibaba/spring-ai-alibaba/issues/4091 ），
这类问题的修复将进⼀步提升断点续传场景下的⽀持能⼒。
参考资料
Spring AI Alibaba 框架源码：https://github.com/alibaba/spring-ai-alibaba
Spring AI Alibaba 社区⽂档：https://java2ai.com/
Spring AI Alibaba 框架消息顺序 bug issue：https://github.com/alibaba/spring-ai-
alibaba/issues/4662
```

## PDF 第14页

[查看RAW.pdf第14页](RAW.pdf#page=14)

> 本页含2个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
Spring AI Alibaba HITL 扩展机制 issue：https://github.com/alibaba/spring-
ai-alibaba/issues/4091
团队介绍
本⽂作者绍清，来⾃淘天集团-直播技术团队。团队专注于⽤技术连接直播内容与商业价值，
以 AI 深度发掘直播业务的场景价值。围绕直播运营智能体、直播数字⼈等⽅向，团队构建起
覆盖供需匹配、内容组织、运营决策到数字⼈⾃主开播的完整链路，并在业务与研发实践中持
续沉淀 AI Native 的系统能⼒，为直播经营提质提效，助⼒商家与主播释放直播势能。
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | ⾳视频技术
服务端技术 | 技术质量 | 数据算法
⼤淘宝技术
⼤淘宝技术官⽅账号
964篇原创内容
公众号
阅读 4425
留⾔
写留⾔
还没有留⾔，来写⾸评
```

## PDF 第15页

[查看RAW.pdf第15页](RAW.pdf#page=15)

> 本页含0个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
[本页未提取到文字；不据此判定原页为空白。]
```

