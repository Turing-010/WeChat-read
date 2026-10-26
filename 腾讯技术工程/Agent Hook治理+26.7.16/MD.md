# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
Agent  治理：⽤ Hook  堵住 LLM  的偷懒、越权与失忆
腾讯程序员 Jul  16 , 2026 , 2 : 52  AM⼴东原创 腾讯技术⼯程 423  listened
作者：xiangnzhang
引⼦：从两个真实案例说起
案例⼀：⽤户让 Agent  改⼀张核⼼表的 ETL —— 1200  多⾏的⻓ SQL 。 Agent  读完原⽂、开始
输出，写到⼀半"偷懒"了，中间跳过⼀⼤段逻辑写了句省略，然后若⽆其事地继续往下写。这
份带省略号的脚本⼀旦提交上线，下游⼏⼗张表当天的数据就会算错。
案例⼆： Agent  还在"⽅案设计"阶段、⽤户都没点头，就径直调了发布⼯具，把⼀张还在讨论
的表结构推上了⽣产。
这两个案例看似不相⼲，根因却是同⼀个——不是模型能⼒不够，⽽是它"图省事"或"⾃作主
张"。具体有三种表现：
1 . LLM  偷懒：处理⻓脚本（动辄上千⾏的 SQL  / Python  ETL ）时，模型会截断、占位略写
（输出 -- 其他字段 ...）、跳步骤、把⻓ SQL  "复印"式重写到 token  耗尽，最后剩⼀堆
残缺、不可执⾏的脚本。
2 . 越权操作：发布、回刷、冻结/解冻、终⽌实例这些写⽣产或不可逆的动作，模型⽆法区分
操作的可逆性——它把发布和查询视为同⼀类"完成任务的步骤"，可能不打招呼就直接调
了。
3 . 上下⽂失忆：模型改完表不去分析下游⻛险、 Python  产出图表不知告诉⽤户——「需要查
的就不查」。模型被训练成⽤最短路径完成任务——额外⼀次 tool  call  意味着多⼀步推
本⽂是 DECO （⼀个跑在⽣产上的数仓 Agent  引擎）实践系列之⼀，聚焦护栏层：怎么⽤
Agent  框架的 Hook  切⾯，把 LLM  处理⻓⽂本时的"偷懒"（截断、略写、残缺）、对⽣
产环境的"越权"（未确认发布、回刷）以及上下⽂传递中的"失忆"（改了表不查⻛险、产
出了物不知汇报），在代码层确定性兜底—— prompt  管不住的，框架来堵。
DECO  作为腾讯⼀站式数据⼯程 Agent  智能协作平台，以业务数仓知识库为基础，致⼒于
解决从需求到数据交付全过程，主要聚焦于数据问询、开发、同步、分析、运维五⼤环
节。希望帮助更多同学更轻松地获取数据、理解数据、应⽤数据，助⼒数据平权。
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
理，模型倾向于跳过"看起来不必要"的检查步骤。（此处⻛险分析为事后下游影响评估，⾮
改表前拦截——事前拦截由 HITL  Guard  负责。）
"在 prompt  ⾥多写⼏句 ⚠  禁⽌"根本管不住。 这不是 prompt  engineering （通过提示词约
束模型⾏为）能解决的问题——⻓ SQL  是物理上超出 token  预算，危险操作是模型⽆法区
分"查询"和"发布"的可逆性差异，被动探测是模型追求最短完成路径的⾃然倾向。唯⼀的解法
是在 Agent  框架层，让偷懒和越权的路径代码级强制⾛不通，让失忆的已知盲区确定性补⻬。
本⽂拆解这套机制——Hook  链（ Agent  框架的 Callback  切⾯）+ 挂在它上⾯的读写两侧
offload（⻓内容落盘、上下⽂仅留引⽤句柄）+ HITL  ⻔禁 + 上下⽂联动闭环。
⼀、背景：数仓  Agent 的任务开发流程
DECO  的数仓开发 Agent  帮⽤户把数据需求落成 US  平台上可运⾏的任务。先约定⼏个关键名
词：
⼆、 Hook 链：在关键切⾯挂载护栏逻辑
拦截这三类问题的切⼊⼝，是 Agent  框架普遍提供的Hook （或称 Callback ）机制：框架在
Agent  运⾏的每个关键节点（围绕"模型调⽤"和"⼯具调⽤"，各有执⾏前 / 后）暴露出切⾯。
我们把拦截逻辑挂载到这些切⾯上——到点框架⾃动回调，同⼀切⾯可挂多个、按序执⾏。⼀
次会话沿这条流⽔线跑下来：
本⽂主要⽤到下⾯⼏个切⾯：
切⾯ 触发时机 本⽂⽤它做什么
Before  Tool （befo
reTool）
⼯具真正执⾏前，可改⼊
参、可直接拦截
⻓脚本回写前从⽂件加载全⽂、危险
操作确认（ HITL  ⻔禁）
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
切⾯ 触发时机 本⽂⽤它做什么
After  Tool （afterT
ool）
⼯具执⾏后、结果回给 LLM
前，可改返回值 ⻓脚本拉取后把内容替换成引⽤句柄
Before  / After  Mod
el 每次请求 LLM  前 / 后 响应⽤户取消等
Before  / After  Age
nt 单个 Agent  运⾏前 / 后 对话持久化等
本⽂逐层拆解三个最重要的应⽤：⻓⽂本完整性护栏（ § 三，揪"偷懒"）、危险操作确认 HITL
（ § 四，封"越权"）、上下⽂联动闭环（ § 五，补"失忆"）。
三、长⽂本完整性护栏：让长脚本进出  LLM 都不出错
3 . 1  ⻓ SQL  在哪⾥被截断、略写
数仓任务开发会遇到两类⻓脚本，它们的偷懒形式不同：
修改场景：从 US  平台拉来的存量⻓ SQL，要在原脚本上局部改写后回写。⻛险集中在"拉
取—改写"环节。
新建场景： LLM  新⽣成的⽬标态⻓ SQL，通过 US  平台"保存/更新任务"⼯具的 scriptCo
ntent ⼊参提交。⻛险集中在"写回"环节。
⽆论哪种场景，⻓脚本都要经过拉取（ US  平台 →  LLM ）和写回（ LLM  →  US  平台）两段，
每段都有各⾃⾼频的偷懒形式：
阶段 偷懒形式 现象 后果
拉取 流式 token  ⾃截断
把⻓ SQL  塞进上下⽂
后，输出端重写时 token
预算耗尽
⽂件截断成残缺 SQL ，回
写即⽣产事故
拉取
view
（沙箱⽂件查看）后 c
reate_file（创建⽂
件）重写
读⻓ SQL  →  ⽤"创建⽂
件"⼯具把整段再吐⼀遍
（⽽⾮只改局部）
等于复印⼀遍，输出 toke
n  翻倍，此路径下⾃截断
概率接近 100 %
拉取 占位 / 略写 输出含 (SQL 略 )、-- 其
他字段 ... 落盘脚本不可执⾏
设计原则：基础设施和推理逻辑解耦—— Hook  切⾯上的逻辑独⽴运作，模型的 ReAct  循
环不⽤感知；新增 / 删除⼀个 Hook ，主流程⼀⾏代码都不⽤改。
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
阶段 偷懒形式 现象 后果
写回 scriptContent
 ⼊参⾃截断
拼回写⼯具⼊参时⻓ SQL
在 JSON  串⾥被截断
提交残缺脚本， US  平台
⽆校验
根治⽅案：让⻓ SQL  从 LLM  上下⽂⾥"消失"，全⽂⾛⽂件通道——这就是读写两侧 offload
要解决的问题。
3 . 2  框架层⽅案：读写两侧 offload  + 引⽤句柄
做法：整体思路是——LLM  永远不直接接触脚本全⽂。 两端都⽤ Hook  拦截 + 沙箱⽂件做"中
转站"：⻓内容全⽂留在沙箱， LLM  上下⽂⾥只有⼀句引⽤句柄， US  平台 ↔  沙箱 ↔  LLM  三
⽅各管⼀段， LLM  只⽤ str_replace ⼩步改写，最终通过⽂件路径⼊参把⼯作副本喂给回写
⼯具。
拉取侧： Offload  Hook （afterTool）
Hook  拦截到含 scriptContent 的响应后，将全⽂写⼊沙箱只读快照，响应中替换为引⽤句
柄。句柄明确告诉 LLM  "要改先 copy_file（把只读快照复制为可编辑⼯作副本），再 str
_replace"：
⼀句话定位：⻓产物的偷懒是结构性问题。解法是——把 LLM  必须接触的⻓内容降到最
少、每次接触的窗⼝压到最⼩、所有写⼊路径都做成"⼩步增量改 + 强制校验"。
下⽂为可读性将盘路径统称 /sandbox/，实际代码中只读快照在 /mnt/chat-offloa
d/，可编辑⼯作副本在 /mnt/user-data/。
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
<offloaded to /sandbox/{taskName}.remote.etl (read-only snapshot, length=N chars).
 To start editing, run copy_file(...) first, then str_replace.>
案例 · 同⼀个"拉取⻓ SQL "动作，治理前后 LLM  看到的东⻄（脱敏示意）：
# 治理前：约  3.8 万字符⻓  SQL 原样进上下⽂，复印重写到⼀半  token 耗尽
INSERT OVERWRITE TABLE dws_order_detail ...
SELECT ... FROM dwd_a UNION ALL
SELECT ... FROM dwd_b
-- 其他字段 ...                       ←  占位略写
（输出在此截断，下游  SQL  不完整）
# 治理后：上下⽂⾥只剩⼀句引⽤句柄，⻓  SQL 全⽂留在沙箱只读快照
<offloaded to /sandbox/order_detail.remote.etl (read-only snapshot, length=37814 chars
 To start editing, run copy_file(...) first, then str_replace.>
关键设计点：
响应形态适配：单条 Map  和数组都要⽀持；数组下每条 item  独⽴判定，任⼀落盘失败仅
该条降级，避免"⼀条出错让整批 SQL  全进上下⽂"。
失败降级：落盘失败 →  该条返回原 scriptContent，让 LLM  ⾄少拿到内容（承担⾃截断
⻛险），不阻断主流程。
写回侧： Onload  Hook （beforeTool）
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
同模式延展：表侧 Offload
上⾯详细拆解的是任务脚本的⻓⽂本护栏链路。同⼀套 Hook  链上，表侧也挂了完全对称的
Hook （⾯向宽表 200 – 500  列场景），⼼智模型与任务侧完全⼀致——读侧降级（落盘失败透
传）、写侧阻断（⽂件不存在抛异常）。
⼯具协议：scriptContent 与 scriptFilePath 互补参数
回写⼯具同时声明两个参数，scriptFilePath 是纯框架契约：
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
scriptContent  : 脚本内容。 ⚠推荐改⾛scriptFilePath让框架Hook⾃动加载，
                 避免⻓SQL拼⼊参时⾃截断；仅沙箱不可⽤时才直接传。
scriptFilePath :脚本的沙箱路径（强烈推荐）。框架OnloadHook会从沙箱读全⽂覆盖
                 scriptContent ，并在转发给本⼯具前剥离该字段；下游实现侧不消费它。
好处：下游⽆感知（协议不⽤改）、框架可独⽴演化（阈值/⽩名单/剥离规则升级都不影响下
游）、防御性⽇志兜底（下游对 scriptFilePath 留 log.warn——到达本⼯具时它本应已
被剥离，还在就是 Hook  失效信号）。
效果：修改任务时，模型不⽤再"吐"那⼏千⾏ SQL ——它只输出脚本路径，全⽂由框架在后台
对⻬。「⻓⽂本⾛⽂件路径，修改任务的⼯具调⽤输出 token  直接降约 90 %」的落地机制；
⻓ SQL  从此彻底从对话历史和 token  消耗⾥"隐身"。
3 . 3  多重防线全景（对应数仓四阶段）
这套护栏不是单点，⽽是贯穿 Skills  编排篇那条流⽔线的多重防线：
每⼀阶段的防线，正好对应 Skills  编排篇⾥那条数仓开发流⽔线（设计 → 拆解 → 执⾏ → 验证四
阶段）的各个阶段——Hook  在框架层做物理兜底。
3 . 4 ⻓⽂本护栏效果⼩结
把前⾯散落的数字汇成⼀张表（均为脱敏汇总）：
维度 / 指标 治理前 治理后
offload  策略 SQL  原样进出上下⽂
全量落盘
，所有 scriptContent  ⾃动换引
⽤句柄
图中隐含了两条关键分⽀，未直接绘出以保持主线清晰：
Onload  阻断（红线）：「 ⑤  →  Onload  Hook  加载⼯作副本」环节，若 scriptFileP
ath 不在⽩名单路径、身份缺失、⽂件不存在或内容为空 →  抛异常阻断⼯具调⽤，不
进⼊ C1  后续。
Offload  降级（橙线）：「 ①  Offload  Hook  落只读快照」环节，若 COS  落盘失败 →
该条原 scriptContent 透传给 LLM （承担⾃截断⻛险），不阻塞主流程。
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
维度 / 指标 治理前 治理后
修改任务⼯具调⽤输出 toke
n 每轮重传整段 SQL **直降约 90 %**（上下⽂仅留
引⽤句柄）
SQL  复印⾃截断 " view  →  重写"路径下概率
近 100 %
物理消除（只⾛ str_replac
e ⼩步改）
读侧失败（ Offload ，after
Tool） — 降级
透传，可重试，不污染⽣产
写侧失败（ Onload ，befor
eTool） — 阻断
⼯具调⽤，杜绝发布残缺脚本
3 . 5  ⾏业对⽐：哪些是现成的，哪些必须⾃研
和 HITL  不同—— HITL  是单点拦截决策，各框架⼏乎都有⼀⾏配置或⼀个中间件搞定。⻓⽂本
护栏是⼀个流⽔线问题（拉取 →  offload  →  编辑 →  onload  →  写回），没有哪个框架直接给⼀
个开箱即⽤的完整闭环。但" offload  + 引⽤句柄"这个模式本身，⾏业已有多种层级的实现：
⼯程 读侧策略 写侧策略 ⾃动化程度
ADKArtif
actServi
ce
save_artifact
 / load_artifact API  + LoadArti
factsTool，官⽅有 context_offl
oading_with_artifact 示例（ sav
e→ 摘要 →hook  注⼊ → 仅当前轮次可
⻅）
❌  需⼯具内⼿
动调 load_ar
tifact 再拼⼊
参
⚠  每个⼯具⼿
动调⽤ API ，⾮
Hook  层⾃动拦
截
LangGraph
 DeepAgen
ts
内置 " Large  Tool  Result  Offloading "
中间件：⼯具结果 > 20k  token  ⾃动落
盘，消息中只留引⽤指针；另有 Summa
rizationMiddleware 在 85 % 容量
时⾃动摘要压缩历史
❌  只做读侧 ✅  全⾃动，中
间件层透明
Anthropic
Claude  Co
de
Read
 默认 2000  ⾏、offset/limit 分⻚
Edit
 强制 str_rep
lace， Pre - rea
d  requirement
❌  ⽆ offload ，
内容全留上下⽂
两个关键结论：
注： DECO  使⽤ Java  ADK，其 Hook  API  与 Python  ADK  同构但接⼝名略有差异；以下
对⽐以 Python  ADK  为例说明设计思路差异，具体接⼝以 Java  ADK  ⽂档为准。
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
1 . ADK  和 LangGraph  都有内置的 offload  能⼒——如果 DECO  只需要"读⻓ SQL  时把全⽂
换成引⽤句柄"，⽤它俩的原⽣机制改造即可，不是从零发明。但这两者的 offload  都只做
到读侧（⼯具结果 offload ），没有写侧 onload ——因为⼤部分 Agent  场景不需要把⻓产
物再原样发回外部 API 。
2 . DECO  的数仓场景不同——有"写⻓ SQL "的保存⼯具，⻓产物要原样回写 US  平台。这意
味着必须两端对称 offload，并且写回时需要额外加固：
加固项 为什么框架原⽣覆盖不了
写侧 onload
（ beforeTool  加载全
⽂覆盖⼊参）
ADK  / LangGraph  的 offload  只做读侧，写侧需⾃⼰实现从⽂件读
回、覆盖 scriptContent、剥离 scriptFilePath
scriptFilePat
h 框架协议
⼯具声明两个互补参数，下层不感知， Hook  层独⽴演化—— ADK  Ar
tifacts  有 load  API  但没有这种"参数交换契约"
只读快照 / ⼯作副本
分离
防提前误改， LLM  必须显式 copy_file 才能开始编辑——这是 DE
CO  踩坑后的设计，不属于框架原⽣概念
注释块按字段名识别
+ 剥离
US  平台默认注释块和 LLM  调度块⽤相同分隔线，必须按字段名区
分——纯业务逻辑，框架不会内置
列级 offload
（ 3  个对称 Hook ）
宽表 200 – 500  列， DDL  正⽂ + columns  都要 offload —— ADK  /
LangGraph  的 offload  不区分"脚本"和"列"的语义
失败语义按代价差异
化
读侧降级、写侧阻断——框架的 offload  失败统⼀降级，不会根据操
作类型做差异化决策
四、危险操作确认（ HITL ）：⽤  beforeTool 卡住不可逆操作
4 . 1  通法：写操作不可逆，护栏要在框架层
prompt  是软约束，不是安全边界。任何"做了就回不去"的操作（发布、回刷、冻结/解冻、终
⽌），都必须有⼀道代码级强制确认：没拿到⽤户明确授权，⼯具就是不能执⾏。这道闸必须
在框架⾥。
HITL  本质是⼀个特殊的 beforeTool Hook ：⼯具真正执⾏前，判断"是不是危险操作、⽤户
授权了没"，没授权就阻断。它天然落在前⾯介绍的那套 Hook  体系⾥。
4 . 2  配置驱动的危险⼯具守卫
做法：危险⼯具守卫挂在 beforeTool 切⾯上，在 Hook  编排层统⼀调度。危险⼯具清单是
配置出来的，每个配⼀个授权标记（requiredState key ）和确认对话框：
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
deco:
  dangerous-tools:
    -name:packCommit
      required-state:confirm_pack
      hint:" 需要⽤户先选择发布⽅式 "
      confirmation:
        title:" 请确认发布⽅式 "
        options:
          -{id:direct,label:" 直接发布（免审批） ",value:direct}
          -{id:approval,label:"提交审批 ",value:approval,hasInput:true,inputPlaceholder:
          -{id:draft,label:" 保存草稿 ",value:draft}
          -{id:edit_more,label:" 我再改改 ",value:edit_more}
守⻔流程—— Agent  每次要调⼯具，框架都会先过⼀道「⻔卫」：
实际配置了多个危险⼯具，每个对应不同的授权标记：confirm_pack（发布提交）、co
nfirm_deploy（触发发布）、confirm_upsert_datasource（数据源变更）、confirm
_transfer_task_upsert（同步任务变更）。同⼀套 Guard  机制统⼀管控。
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
⽆论 Agent  是⾃作主张还是被诱导，只要没有⼈⼯确认这⼀步，packCommit / deployCommi
t 在框架层就物理⾛不通。 §4 . 3  配图展开与⽤户握⼿的完整时序。
4.3 ⼀次完整的确认过程：拦截  →  弹框  →  ⽤户选择  →  放⾏
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
⽤户点选项后，前端经 REST  API  把选择写进会话存储（session.state），再发起⼀次续跑
请求（复⽤引擎篇的续跑⼊⼝）重新驱动同⼀会话——这⼀轮 LLM  重调该⼯具时 state  已就
位，守卫放⾏。
确认框还⽀持带输⼊控件的选项（hasInput / inputPlaceholder / inputType），承
载"填审批⼈""填回刷⽇期"这类带参确认——不只是 yes / no 。
关键设计点：
必须框架层拦，不能信 LLM 。 这套机制就是从框架层阻断 LLM  绕过 prompt  直接调 pac
kCommit/deployCommit；确认动作只能由真实⽤户在前端触发。
4 . 4  ⾏业 HITL  全景与⾃研必要性
DECO  的 HITL  是在 ADK  较早版本上⾃研的。如今 HITL  已是主流 Agent  框架的标配能⼒
——开箱即⽤程度远超"从零实现"。先看⾏业全景：
框架 开箱程度 交互模式 配置驱动 暂停/恢复 变更预览
ADKToolC
onfirmat
ion
✅  布尔确认⼀⾏
配置；⾼级确认 r
equestConfirma
tion() 可带结构
化 payload
yes / no  + p
ayload （⽆
原⽣多选 U
I ）
❌  写在⼯
具代码⾥
✅  框架原
⽣ ❌
LangGrap
h
 HITL  Midd
leware
✅  声明式 inter
ruptOn 配置
approve  / e
dit  / reject
/ respond
✅  inter
ruptOn 映
射
✅  框架原
⽣ + check
pointer
❌
Claude  Co
dePreToo
lUse
✅  shell  脚本 + p
ermissionDecis
ion
deny  / allo
w  / ask
✅  setti
ngs.json
N / A （⽤户
侧脚本） ❌
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
框架 开箱程度 交互模式 配置驱动 暂停/恢复 变更预览
DECODang
erousToo
lGuard
❌  需⾃研
多选项 + 带
输⼊控件 +
变更预览
✅  appli
cation.y
aml
⾃研：事件
+ state  +
续跑
✅  COMMI
T_PREVIE
W
其中 ADK  的 ToolConfirmation（1.0.0 起内置，当前最新 1.4.0）与 DECO  的深度对
照：
维度 DECO  DangerousToolGuard（⾃研） ToolConfirmation
（ ADK  ≥1 . 0 . 0  原⽣）
触发⽅式beforeTool
 切⾯外部拦截
⼯具内部调 requestConfirmati
on()主动暂停
危险清单配置驱动
（ yaml ），⼯具⽆需改代码 ⼯具⾃身代码⾥声明
暂停/恢
复
发事件 + 阻断，靠 LLM  重试 + state  ke
y  放⾏
框架原⽣暂停 flow ，收到确认数据
后恢复
防循环 ⽤ requiredState key  标记"已授权" 框架⾃动清理中间事件 + 注⼊已确
认 call
前端交互 ⾃定义 INTERACTION_BOX（富交互框、
多选项、带输⼊）
FunctionResponse
 回填（布尔或 payload ，⽆原⽣多
选 UI ）
结论：如果只需要"调危险⼯具前问⼀声 yes / no "，直接⽤ ADK  原⽣ ToolConfirmation 即
可——⼀⾏配置，框架替你处理暂停/恢复和防循环，这恰是⾃研最易出 bug  处。但 DECO  的
场景要求更多：
1 . 发布前展示变更清单（COMMIT_PREVIEW）——⽤户不是盲选 yes / no ，⽽是先看改了什
么；
2 . 确认框带参数（选发布⽅式、填审批⼈、填回刷⽇期）——不是 yes / no ，是结构化表单；
3 . 危险⼯具清单配置驱动——不同租户/环境危险⼯具不同，不能写死在⼯具代码⾥；
4 . 和 SSE  流式协议⼀体——INTERACTION_BOX 是 CUSTOM 事件的⼦类型，确认框和⽂件事
件、阶段事件⾛同⼀条管道。
这四条， ADK  原⽣和 LangGraph  的 HITL  都不直接覆盖——它们的 HITL  是"⼯具级通⽤拦
截"， DECO  要的是"业务级集成确认"。⾃研的必要性不在于"框架没有 HITL "，⽽在于"框架的
HITL  不够业务化"。
五、上下⽂联动闭环：让  LLM 不再「需要查的就不查」
5 . 1  第三类问题： LLM  的「不作为健忘」
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
前两类——偷懒（⻓⽂本截断、略写）和越权（未确认发布、回刷）——都是 LLM 「做了不该
做的」或「该做好的没做好」。还有第三类更隐蔽：该做但没做的——
改了 DDL ，字段重命名了—— LLM  不会主动去分析下游哪些表会受影响（注：此处⻛险分
析为事后下游影响评估，⾮改表前拦截——事前拦截由 HITL  Guard  负责），因为它「觉
得」改表是⾃⼰的事、⻛险分析是额外的事；
Python  脚本跑完，产出物⽣成了⼀张图表—— LLM  不会主动告诉⽤户图在哪，除⾮⽤户追
问；
表结构变更了，字段元数据在上下⽂⾥已过时—— LLM  不会主动回查刷新，继续⽤旧信息
做决策。
这不是模型能⼒不够，⽽是「主动探测 = 额外⼀次 tool  call  = 多耗 token 」。模型天然追求以
最少 token  完成任务，不会主动给⾃⼰加检查步骤。
在⾏业坐标系中，这对应 ADK  官⽅ 8  ⼤ Hook  模式中的 # 2 动态状态管理——「在回调中读
写 state ，使 Agent  ⾏为可上下⽂感知，在步骤间传递数据」。 DECO  进⼀步把它拓展成了⼀
个闭环范式：Hook  采集事实 →  写 state  →  Attachment  注⼊下⼀轮 prompt。
5 . 2  范式： Hook  管「发⽣了什么」， Attachment  管「下⼀轮告诉模型什么」
这个范式的核⼼是把「副作⽤采集」和「上下⽂注⼊」解耦成两段，各管各的：
这样做的好处是双重的：
1 . 采集是确定性的：⼯具调⽤⼀定触发 Hook ， Hook  ⼀定做完检查——不靠 LLM 「记得去
查」；
2 . 注⼊是时机正确的：分析结果只在下⼀轮 prompt  ⾥才需要，不污染当前轮的上下⽂、不增
加当前轮的 token  消耗。
对⽐让 LLM  ⾃⼰「记得去查」的⽅案：
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
⽅案 可靠性 token  开销 LLM  偷懒⻛险
prompt  ⾥写「改表后记得分析
⻛险」 ❌  软约束 ⽆额外 ✅  ⾼—— LLM  可能
跳过
单独发⼀轮「请分析⻛险」 🟡  依赖调度
逻辑 额外⼀轮 ✅  中—— LLM  可能
敷衍
Hook  采集 →  state  →  Attac
hment  注⼊ ✅  确定触发 ⽆额外（结果复
⽤）
❌  零——不依赖 LL
M  ⾃觉
5 . 3  案例⼀： RiskAnalysisHook  —— 改表后⾃动注⼊⻛险分析
场景： Agent  在 DDL  设计或执⾏阶段调 upsertTable 改了⼀张表的字段结构。
LLM  的认知盲区：它把「改表」当⼀次成功的⼯具调⽤完成了，不会想到还要接着查改动影响
了谁——下游⼏⼗张 ETL  可能因为⼀个字段重命名⽽直接报错。（此处⻛险分析为事后下游影
响评估，⾮改表前拦截——事前拦截由 HITL  Guard  负责。）
治理做法：
判定「改表」语义：RiskAnalysisHook 挂在 afterTool 上，不从⼯具名硬判断——它看⼯
具调⽤⼊参：带了 tableId 参数的 upsertTable 就是改表（新建表不带 tableId）。新
建表语义直接跳过，不触发⻛险分析。
⻛险分析结果被 Attachment  注⼊后， LLM  在下⼀轮回复中⾃然输出类似提示：
⚠  ⻛险提示：刚刚修改了  dws_order_detail 表的字段，检测到下游影响：
- dws_channel_report (HIGH) — 依赖字段  order_amount
- ads_daily_summary (MEDIUM) — 依赖字段  order_status
建议检查这两张表的  ETL 是否需要同步调整。
关键设计点：
判定条件精确：带 tableId 才是改表，避免新建表误触发⻛险分析；
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
累积写⼊ state：⼀次会话多次改表，⻛险结论累积，下⼀轮⼀次性汇总注⼊。
5 . 4  案例⼆： PythonImageHook —— ⾃动发现并呈现⽣成产物
场景： Agent  调 Python  脚本做数据分析，脚本产出了⼀张可视化图表，但 LLM  的对话输出⾥
没有图——⽤户必须⾃⼰去沙箱⽬录⾥翻。
LLM  的认知盲区： LLM  调 Python  ⼯具时只知道脚本跑完了——它不知道脚本产出了什么新⽂
件，⾃然不会主动告诉⽤户「⽣成了 chart . png 」。等⽤户问「图呢」， LLM  要么已结束上下
⽂，要么需再调⼀次⼯具查⽂件列表。
治理做法：
前端渲染：Attachment  注⼊的不只是⽂本——预签名 URL  被写成结构化 JSON ，前端据此渲
染内联图⽚。⽤户⽆需点按钮、不必翻沙箱⽬录，图直接出现在对话流⾥。
关键设计点：
前后⽂件快照对⽐：beforeTool 加⽂件快照、afterTool 对⽐，⽐让 LLM  ⽤ bash l
s 查⽂件可靠得多；
只关⼼图⽚：仅关注 .png/.jpg/.svg 等图⽚格式，不处理脚本和数据⽂件——避免
state  ⾥塞⽆关⽂件列表；
累积写⼊：⼀次 Python  执⾏可能产出多张图，全部累积写⼊，⼀次注⼊。
5 . 5  为什么 prompt  管不住「⾃⼰查」？
§3 . 1  和 §4 . 1  已论证 prompt  管不住「⻓⽂本截断」（物理约束）和「未授权操作」（模型输
出不受限）。对「主动探测」类问题，前两条原因同样成⽴（模型追求效率、 prompt  是软约
````

## PDF 第 17 页

[原页](RAW.pdf#page=17)

````text
束、上下⽂⼲扰），但还有⼀个独有原因：
信息不对称： LLM  不知道 Python  脚本产出了什么⽂件——它是「瞎⼦」，只能靠⼯具返
回的 stdout / stderr  了解执⾏情况。如果返回⾥没提「⽣成了 chart . png 」， LLM  就不可能
知道。这不是"忘了查"，⽽是根本不知道有东⻄该查。
确定性兜底解法只有⼀个：不让 LLM 「决定要不要查」，⽽是框架在⼯具执⾏后强制采集、结
果⾃动注⼊下⼀轮 prompt。这正是 Hook  →  state  →  Attachment  闭环做的事。
5 . 6  ⾏业对⽐：谁在解决「上下⽂断裂」？
「跨轮次状态传递」不是 DECO  独有问题，各框架都有解法，但切⼊⻆度不同：
框架/⼯具 DECO  的差异
ADKArtifactService DECO  不依赖 artifacts ——采集 →  state  →  Attachment  是事件
驱动 + ⾃动注⼊，⽽⾮ LLM  主动 load
LangGraph
 checkpointer
DECO  state  更轻量，专⽤于「事实采集 →  上下⽂注⼊」，不承
载流程控制
Claude  Code
 SessionStart  / UserPro
mptSubmit
DECO  在⼯具调⽤后、下⼀轮 LLM  调⽤前注⼊，时效性更强
CrewAI
 TaskMemory DECO  单 Agent  内多轮，不涉及跨 Agent  协调
DECO  这套机制的特殊之处：它不是「存储 →  读取」的被动模式，⽽是「事件 →  采集 →  注
⼊」的主动流⽔线。 Hook  不是等着 LLM  来查 state ，⽽是主动把结论 push  进下⼀轮 prompt
——这意味着即使 LLM  完全不知道 state  ⾥有⻛险分析结果， Attachment  也会让它「看
到」。
````

## PDF 第 18 页

[原页](RAW.pdf#page=18)

````text
⼀句话： Hook  →  state  →  Attachment  闭环，把「 LLM  需要主动查」的操作降维为「框架主动
push 」—— LLM  不再是「需要查的就不查」，⽽是「不管想不想查都会被喂到嘴边」。
六、 Hook 全景：上⾯还挂着⼗余个横切逻辑
三、四两节纵深拆解了两个深度案例——⻓⽂本读写两侧 offload  和 HITL  ⻔禁。但同⼀套
Hook  链（beforeModel/afterModel/beforeTool/afterTool/onRunEvent 等切⾯）
上， DECO  实际挂了⼗余个 Hook，覆盖可观测、前端实时刷新、上下⽂联动、业务事件、沙
箱环境等横切关注点。这⼀节从纵深拉回横展，展现 Hook  体系的完整⽣态。它们都遵循同⼀
条原则：不改业务循环、不动⼯具实现，把横切逻辑挂在切⾯上。
分类 Hook 挂载点 职责
⻓⽂本护栏
TaskScriptOf
floadService
 / TaskScript
OnloadServic
e
afterTool  / before
Tool
ETL  脚本读写两侧全量 offload ，
治偷懒
TableColumns
OffloadServi
ce
 / DdlColumns
OnloadServic
e
afterTool  / before
Tool
宽表 columns  读写两侧 offload ，
⼏百列不经过 LLM  token
DdlBodyOfflo
adService afterTool DDL  正⽂⽆条件落盘 + 表元数据
⾃动拼接注释块头
危险操作护
栏
DangerousToo
lGuard beforeTool 危险⼯具拦截 + HITL  确认
````

## PDF 第 19 页

[原页](RAW.pdf#page=19)

````text
分类 Hook 挂载点 职责
⼯具返回处
理
LineageRespo
nseOffloadSe
rvice
afterTool ⾎缘原始响应 + slimGraph  写 ch
at - offload / lineage /
ToolResponse
Truncator afterTool
超⼤返回智能裁剪（超阈值触发 R
erank  重排优先保留与当前问题最
相关⽚段），截断前写 COS 、需
要时回捞
ToolResponse
Formatter afterTool ⼯具返回结构化格式化
可观测 & 持
久化
ToolCallLogH
ook before / afterTool
异步记录⼯具⼊参/出参/耗时/成
功率（toolName@threadId 配
对）
LoggingHook 多点 Agent  执⾏链路⽇志
Conversation
PersistenceH
ook
beforeAgent  / be
fore · afterTool  / o
nRunEvent
落库 USER / MODEL / TOOL ，超⻓
⼯具返回截断后⼊库
前端实时刷
新 & 业务事
件
SqlExecuteHo
ok beforeTool
execute_sql
 前先存盘并推 FILE_TREE_CHAN
GED
CopyFileHook afterTool
copy_file
 后按 version  判定 CREATED / UP
DATED  推⽂件树事件
ReleaseItemC
ollectorHook afterTool 收集发布条⽬，推 TASK_PLAN_C
REATED/TASK_PLAN_UPDATE
DocumentSave
Hook 阶段完成 把阶段产物⽂档从 state  落盘，剥
离 markdown  代码块
Hook→Atta
chment  联
动
RiskAnalysis
Hook afterTool 改表时算单表变更⻛险，写 state
供下轮 Attachment  注⼊
PythonImageH
ook before / afterTool 检测 Python  新产出图⽚，⽣成预
签名 URL  供 Attachment  注⼊
沙箱环境 EnvVarCaptur
eHook afterTool
从 bash export 提取环境变量写
⼊ .sandbox_env，重启后由 in
it.sh 恢复
6 . 1  ⾏业参照： ADK  总结的 8  种 Hook  模式 + Claude  Code  参照
````

## PDF 第 20 页

[原页](RAW.pdf#page=20)

````text
看完 DECO  钩⼦体系的全貌，再回看这套机制的⾏业坐标系。 ADK  官⽅总结了 8  种 Hook  设
计模式，这也是⾏业主流 Agent  框架普遍采⽤的分类：
模式 说明 DECO  对应
防护栏与策略执
⾏
before _ xxx  拦截，违规直接返回预设
响应 ✅  HITL  ⻔禁（ 4 . 2 ）
动态状态管理 回调中读写 state  做跨步骤传递 ✅  offload  元数据写 state
⽇志与监控 关键点埋结构化⽇志 ✅  ToolCallLogHook
缓存 before _ xxx  查缓存命中直返 ✅  反向模式：查⽂件缓存回填
请求/响应修改 修改 LlmRequest  或⼯具⼊参/出参 ✅  offload / onload  核⼼机制
条件跳过步骤 返⾮空结果阻⽌后续执⾏ ✅  Guard  返 Maybe.just
() 短路
认证与摘要控制 ⼯具级 auth 、跳过 LLM  摘要 —
⼯件处理 save / load  artifact ✅  COS  落盘 read - only  snaps
hot
结语
这⼀篇讲的都是横切护栏：不改业务循环、不动⼯具实现，全靠挂在 Hook  切⾯上的护栏逻
辑，把" prompt  管不住"的三类问题在框架层确定性地兜住——
⻓⽂本偷懒：读写两侧 offload  + 引⽤句柄 + 强制 str_replace + 失败语义⾮对称，
让"复印⻓ SQL ""提交残缺脚本"物理上不可能。
越权操作：配置驱动的 beforeTool 守卫 + 富交互确认框，让不可逆动作必须经真实⽤户
授权。
上下⽂失忆： Hook  采集 →  state  →  Attachment  注⼊闭环，让「需要查的」⾃动 push  到
LLM  眼前，不靠它⾃觉。
它们服务于 Skills  编排篇那条数仓流⽔线的每个阶段，也和引擎篇的扩展点共⽤同⼀套 Hook
机制。
⼀句话总结就是： prompt  定意图， Skill  定规矩，框架 Hook  定边界——能⽤确定性兜底的，
别交给模型。
````

## PDF 第 21 页

[原页](RAW.pdf#page=21)

````text
阅读 1 . 7 万
留⾔ 2
Hata⼴东 7 ⽉ 23 ⽇
⼼在远⽅⼴东 7 ⽉ 23 ⽇
写留⾔
1
Hook  是已知防已知的事后解决⽅案，不出事故你都不知道 hook  改防什么，要真的治理好，难
的是未知防未知
我参与 agent 项⽬开发时也经常会关注⼯具越权⾏为，危险命令操作确认。包括
AskUserQuestion ，⼤⼯具结果落盘⾏为
````

## PDF 第 22 页

[原页](RAW.pdf#page=22)

````text
````

