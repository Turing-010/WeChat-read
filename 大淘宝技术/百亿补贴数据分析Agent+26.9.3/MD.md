# 淘宝百亿补贴数据分析助手 Agent 实战：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_百亿补贴数据分析Agent.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
淘宝百亿补贴数据分析助⼿ Agent 实战
原创 天猫技术团队 ⼤淘宝技术 2026年9⽉3⽇ 18:55 浙江 16⼈
bybt-data-analysis-assistant是⼀个数据分析智能体，它能将⾃然语⾔提问转化为完整的
数据分析流程，实现"你问它答"的智能化数据服务。该系统解决了传统数据分析中取数
慢、⼜径混乱、归因依赖⼈⼯和知识不沉淀等痛点，提供NL2SQL 取数、波动归因、⾎
缘溯源、Python分析等全⽅位能⼒。其核⼼技术采⽤多Agent协同架构，通过意图识
别、调度路由和ReAct推理循环实现智能决策，摒弃了简单的Text-to-SQL模式，创新性
地采⽤NL2MDL2SQL路径，确保SQL⽣成的准确性和⼜径统⼀。系统构建了六层知识体
系，从表结构到会话记忆分层管理，结合WrenAI 语义层和Hologres加速查询，实现了
从找表、写SQL、执⾏到深度分析的全流程⾃动化，⼤幅提升了数据分析效率和质量，
使业务⼈员能像对话⼀样获取数据洞察。
项⽬概述
▐ 1.1 它是什么
bybt-data-analysis-assistant 是⼀个数据分析智能体——你⽤⾃然语⾔提问，它⾃主完成
从找表、写 SQL、执⾏查询到深度分析的全流程：
1 "昨天 GMV 多少？" → 找表 → ⽣成 SQL → 执⾏ → 返回结果
2 "GMV 为什么跌了？" → 波动归因 → 逐层下钻 → 因果链报告
3 "这个指标怎么计算的？" → ⾎缘溯源 → 上游字段 → 计算逻辑
4 "各⾏业 GMV 做帕累托" → 取数 → Python 分析 → 图表
它不是简单的 Text-to-SQL，⽽是⼀个能思考、会选⼯具、能⾃我纠错的 Agent。
▐ 1.2 解决什么痛点
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 1.3 能⼒速览
快速上⼿
▐ 2.1 Web 平台
启动服务：
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
1 ./boot.sh
访问地址：
对话示例：
技术架构全景
▐ 3.1 架构全景图
1 ⽤户⾃然语⾔提问
2 │
3 ▼
4 ┌──────────────────────────────────────────────────────┐
5 │ 意图识别层 │
6 │ Intent Agent: LLM 单次调⽤ → JSON 意图参数包 │
7 │ (意图分类 + 时间解析 + 指标识别 + 维度推断) │
8 └──────────────────────┬───────────────────────────────┘
9 │
10 ▼
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
11 ┌──────────────────────────────────────────────────────┐
12 │ 调度路由层 │
13 │ Supervisor: ⽇期注⼊ + 语义计划 + 记忆召回 │
14 │ → 分发到对应专家 Agent │
15 └──────┬──────────┬──────────┬──────────┬───────────────┘
16 │ │ │ │
17 ▼ ▼ ▼ ▼
18 ┌────────┐┌────────┐┌────────┐┌────────┐
19 │ Query ││Analysis││ Ops ││ Other │
20 │ Agent ││ Agent ││ Agent ││ Agent │
21 │取数专家 ││分析专家 ││运维专家 ││ 兜底 │
22 └────┬───┘└────┬───┘└────────┘└────────┘
23 │ │
24 ▼ ▼
25 ┌──────────────────────────────────────────────────────┐
26 │ 保障层 │
27 │ SQL Validator Gate (后置校验) │
28 │ 答案净化 + SQL ⾃动暂存 │
29 │ SSE 流式输出给前端 │
30 └──────────────────────────────────────────────────────┘
31 │
32 ▼
33 ┌──────────────────────────────────────────────────────┐
34 │ 知识底座 │
35 │ MDL 语义层 │ SQL ⽚段库 │ 规则库 │ ⾎缘图谱 │ 会话记忆│
36 │ (WrenAI) │ (TisPlus3)│(TisPlus3)│(LightRAG)│(TisPlus3)│
37 └──────────────────────────────────────────────────────┘
▐ 3.2 技术栈⼀览
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
设计要点：不同环节⽤不同规格的模型——重活⽤ qwen-plus，轻活⽤ qwen-turbo，控制
成本和延迟。
▐ 3.3 核⼼设计决策
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Agent 架构设计
▐ 4.1 意图识别：入⼝层
意图识别是 Agent 的⼤脑前哨——在 Agent 执⾏前，先⽤⼀次 LLM 调⽤解析出标准化参数
包：
1 {
2 "intent_type":"attribution",
3 "confidence":0.95,
4 "metric_field":"gmv_amt",
5 "metric_name":"GMV",
6 "time_label":"昨天 vs 前天",
7 "curr":"2026-06-14",
8 "prev":"2026-06-13",
9 "scope":"all"
10 }
⼀次调⽤同时完成：
降级策略：LLM 调⽤失败时，⾃动回退到关键词匹配 + 规则解析。
多 意 图 检 测 ： ⼀ 个 问 题 含 多 个 意 图 时 ， 主 意 图 放 intent_type ， 次 要 意 图
放 secondary_intents 数组，⽀持组合如 table_meta + data_query （查表结构
+ 写查询）。
▐ 4.2 多 Agent 协同：调度层
Supervisor 根据意图识别结果，将问题分发到对应的专家 Agent：
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
为什么不⽤单 Agent：单 Agent 需要⼀个巨⼤的 system prompt 和⼏⼗个⼯具，导致⼯具选
择困难、prompt 膨胀、调⽤预算浪费。多 Agent 让每个专家只看⾃⼰相关的⼯具和指令，选
择更精准。
▐ 4.3 ReAct 推理循环：执⾏层
Agent 不是"⼀条命令出结果"，⽽是边想边做的 ReAct 循环。以"昨天 GMV 和前天⽐怎么
样？"为例：
1 Thought 1: 需要先找到 GMV 所在的表
2 Action 1: search_metrics(query="GMV")
3 Result 1: → ads_flow_sum_di, gmv_amt
4 Thought 2: 知道表了，查 SQL 规则确认⼝径
5 Action 2: rule_search(table="ads_flow_sum_di")
6 Result 2: → 必须加 WHERE activity_type=''
7 Thought 3: ⽣成 SQL 查昨天和前天
8 Action 3: build_sql(table="ads_flow_sum_di",
9 metrics=["gmv_amt"],
10 bizdate_start="2026-06-14",
11 compare_bizdate_start="2026-06-13")
12 Result 3: → SELECT ... (完整 SQL)
13 Thought 4: 执⾏ SQL
14 Action 4: odps_query(sql="...")
15 Result 4: → 昨天 XX亿，前天 XX亿，环⽐ -20%
16 Thought 5: ⽤户问了"怎么样"，需要分析环⽐
17 Action 5: python_analyze(code="df['环⽐'] = ...")
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
18 Result 5: → 环⽐下降 20%，主要受家电⾏业影响
19 Final Answer: 昨天 GMV 1.2 亿，环⽐下降 20%...
为什么⽤ ReAct ⽽不是固定流程：
ReAct 让 Agent ⾃主决定调什么⼯具、传什么参数、什么时候收敛。
▐ 4.4 安全守卫：保障层
Agent 有"刹⻋系统"（Harness ），防⽌失控：
此外，所有 Agent ⽣成的 SQL 都经过 SQL Validator Gate 后置校验，确保语法正确、表名
存在、字段合法。
NL2MDL2SQL：
从⾃然语⾔到正确 SQL
这是整个系统最关键的技术选型。
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 5.1 为什么不直接 Text-to-SQL
直接让 LLM 写 SQL 有三个致命问题：
1 直接 Text-to-SQL
2 │
3 ├── ❌ 幻觉字段：LLM 编造不存在的列名
4 ├── ❌ ⼝径错误：不知道某表的 WHERE 条件该加什么
5 └── ❌ 不可复⽤：每次从零⽣成，没有沉淀
LLM 不知道 ads_bybt_flow_sum_di 表必须有 activity_type = '百亿补贴' 这个
WHERE 条件。它会编造字段，会漏掉过滤条件，每次⽣成结果还不⼀样。
▐ 5.2 WrenAI MDL 语义层
WrenAI 引⼊了 MDL（Model Definition Language）——类似 dbt 的语义建模层：
1 ⽤户问题
2 │
3 ▼
4 WrenAI MDL 语义层
5 │
6 ├── mdl.json（模型定义⽂件） ← 表名、字段、关系、描述
7 ├── dry_plan（NL → SQL 预演） ← ⾃然语⾔转 SQL
8 ├── recall（查询历史召回） ← 记住之前问过什么
9 └── fetch_context（上下⽂召回） ← 给 LLM 补充表结构信息
10 │
11 ▼
12 ⽣成的 SQL 经过语义层校验
13 │
14 ▼
15 ✅ 字段存在 ✅ ⼝径正确 ✅ 可复⽤
▐ 5.3 MDL 模型结构
mdl.json 定义了每个表的结构化语义：
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
1 {
2 "models": [
3 {
4 "name": "ads_flow_sum_di",
5 "tableReference": { "table": "ads_flow_sum_di" },
6 "columns": [
7 { "name": "gmv_amt", "type": "decimal", "expression": "pay_amt"
8 { "name": "bizdate", "type": "date" }
9 ],
10 "description": "汇总⽇表"
11 }
12 ]
13 }
Agent 在⽣成 SQL 前会先从 MDL 获取表结构，确保只⽤真实存在的字段。
▐ 5.4 SQL 构建的三种模式
Agent 根据表类型⾃动选择 SQL 构建策略：
▐ 5.5 取数链路中的知识分层
4.3 节展示了 ReAct 的 Thought→Action→Result 机制。在取数场景中，这些⼯具调⽤可以
按知识层级归为四个阶段：
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Agent 在 ReAct 循环中⾃主决定调⽤顺序和是否需要每个阶段——简单取数可能跳过知识应
⽤，复杂分析可能多轮调⽤。
▐ 5.6 Hologres 外部表加速
数据分析场景涉及多次递归下钻查询，每次⾛ ODPS 执⾏ SQL 耗时 30-120 秒。当 Agent 需
要执⾏ 5-10 次 SQL 才能完成⼀次诊断时，总耗时可能超过 10 分钟。引⼊ Hologres 外部
表直读 ODPS，将单次查询加速到 3-10 秒。
为什么选 Holo 外部表⽽不是全量同步：
选择外部表直读：不需要 DBA 介⼊，onboard 新表⾃动挂载，第⼀次查询时⾃动创建外部
表，后续 LRU 缓存命中。
场景闸⻔——只在数据分析场景启⽤：
Holo 加速仅对 stream_analysis （多步分析编排器）⽣效，普通 NL2SQL、CLI 脚本、
运维查询⼀律⾛ ODPS。通过 contextvars.ContextVar 实现线程/协程安全的场景标
记：
执⾏链路：
1 LLM ⽣成 ODPSSQL
2 │
3 ▼
4 odps_query ⼯具（接⼝签名不变）
5 │
6 ├─ Step0: 场景闸⻔——HOLO_ROUTE_MODE=always 且 holo_scope=True？
7 │ 否 → 直⾛ Step7ODPS
8 │ 是 ↓
9 ├─ Step1: 变量替换（${bizdate} → 具体⽇期值）
```

## PDF 第12页

[查看原页](RAW.pdf#page=12)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
10 ├─ Step2: ⿊名单检测（GET_JSON_OBJECT/EXPLODE 等不兼容函数 → 直⾛ ODPS）
11 ├─ Step3: 抽取 SQL 中所有表名（sqlglot AST 解析）
12 ├─ Step4: ensure_foreign_tables——按需创建外部表
13 │ 检查 information_schema.foreign_tables 是否已存在
14 │ 不存在 → IMPORTFOREIGNSCHEMA <project> LIMITTO (<table>)
15 │ LRU 缓存 + 持久化 JSON，避免重复 DDL
16 ├─ Step5: sqlglot ⽅⾔转换（ODPS → PostgreSQL）
17 │ + 表名重写（bm_dw.xxx → public.xxx）
18 ├─ Step6: 通过 aistudio HTTP ⽹关执⾏
19 │ ├─ 成功 → 返回结果（标记 "via Hologres"）
20 │ └─ 失败 → Step7
21 └─ Step7: FallbackODPS（PyODPS execute_sql，原路径）
外部表⾃动管理：
不需要 DBA 预先 IMPORT 整个 project（上千表⼀次性 IMPORT 很贵）。⽽是拿到 SQL 后
⽤ sqlglot 抽出表名，按需创建。⾸次查某表多 1-3 秒建表开销，后续查 LRU 命中零开销。
1 # 进程内存缓存（set）+ 持久化⽂件（.holo_foreign_imported.json）
2 # 幂等去重，重启不丢失
3 # 外部表与 ODPS 表同名，默认 prefix/suffix 为空
切库⾃愈：
当 Hologres 实例切库（如重建实例）后，所有外部表丢失。此时查询会报 relation
"xxx" does not exist 。系统⾃动检测该错误，清空 IMPORT 缓存，重新 ensure 外部
表后重试⼀次。整个过程对 Agent 透明，最多增加 3 秒。
知识库体系
知识库是 Agent 的"记忆"。⼀个能正确取数、能深度归因的 Agent，背后必须有⼀套结构化的
知识体系⽀撑。本章从存储、采集、应⽤三个维度展开。
▐ 6.1 知识体系全景
1 ┌─────────────────────────────────────────────────────────────┐
2 │ 应⽤层 │
3 │ Agent ReAct 循环主动调⽤知识检索⼯具 │
4 │ search_metrics / cap_search / snippet_search / rule_search │
```

## PDF 第13页

[查看原页](RAW.pdf#page=13)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
5 │ lightrag_column_logic / parse_sql_lineage │
6 ├─────────────────────────────────────────────────────────────┤
7 │ 采集层 │
8 │ │
9 │ ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐ │
10 │ │ AST ⾎缘 │ │ 指标注册 │ │ Onboard 流⽔线 │ │
11 │ │ 解析引擎 │ │ 体系 │ │ (表接⼊) │ │
12 │ │ (6-Phase) │ │ (3 种公式) │ │ (5 步⾃动接⼊) │ │
13 │ └──────┬───────┘ └──────┬───────┘ └────────┬─────────┘ │
14 │ │ │ │ │
15 │ ▼ ▼ ▼ │
16 ├─────────────────────────────────────────────────────────────┤
17 │ 存储层 │
18 │ │
19 │ Layer 1: 表能⼒清单 + MDL 语义模型 │
20 │ Layer 2: SQL ⽚段库 (Snippet Store) │
21 │ Layer 3: SQL 规则库 (Rule Store) │
22 │ Layer 4: ⾎缘知识图谱 (LightRAG KG) + AST 实时解析 │
23 │ Layer 5: 指标注册表 (Metric Registry) │
24 │ Layer 6: 会话记忆 (Session Memory) │
25 └─────────────────────────────────────────────────────────────┘
▐ 6.2 六层存储体系
知识分为六层，每层有不同的粒度、变更频率和权威等级：
权威等级：
```

## PDF 第14页

[查看原页](RAW.pdf#page=14)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 6.3 AST ⾎缘解析引擎
⾎缘知识（Layer 4）的数据从哪来？答案是 AST ⾎缘解析引擎——⼀套基于 sqlglot 的 SQL
静态分析管线，从 ETL 源代码中⾃动提取字段级⾎缘。
为什么需要 AST 解析？
⾎缘关系是数据治理的核⼼：某张表的 GMV 字段来⾃哪⼏张上游表？经过了什么计算？
WHERE 条件是什么？这些信息分散在数百⾏的 ETL SQL 中，⼈⼯维护不可持续。
六阶段解析管线
1 原始 ETL SQL
2 │
3 ▼
4 Phase 0: Schema Registry ← 加载所有相关表的字段定义
5 │ (本地 JSON ⽂件 + DataWorks API 降级)
6 ▼
7 Phase 1: 预处理 (Preprocess) ← 全⻆标准化 / DDL 剥离 / 变量替换
8 │ 多 INSERT 拆分 / ⽅⾔兼容
9 ▼
10 Phase 2: AST 标准化 (Normalize) ← sqlglot 解析 SQL → AST
11 │ 展开 SELECT * 为显式列列表
12 ▼
13 Phase 3: 节点提取 (Extract) ← DFS 遍历 AST，按 scope 提取
14 │ CTE / ⼦查询 / UNION 分⽀ / 主查询
15 │ 每个.scope: 源表、输出列、JOIN、WHERE
16 ▼
17 Phase 4: 作⽤域解析 (Resolve) ← 符号表 + alias 消歧
18 │ CTE scope 隔离，拓扑序逐层解析
19 │ 裸列名 → schema 消歧定位
20 ▼
21 Phase 5: ⾎缘映射 (Map) ← resolved scopes → ⾎缘边 (Edge)
```

## PDF 第15页

[查看原页](RAW.pdf#page=15)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
22 │ direct: 上游列直传
23 │ computed: 表达式中的所有列引⽤
24 │ aggregated: SUM/COUNT 等聚合
25 ▼
26 Phase 6: 输出构建 (Output) ← ⽣成标准化 JSON
27 target_table / source_tables /
28 columns(含 depends_on) / joins /
29 where_conditions
两种使⽤模式
实时解析的降级链
1 Agent 需要查字段⾎缘
2 │
3 ├── 1. lightrag_column_logic(table, column) ← 先查 LightRAG KG
4 │ ↓ KG 未命中（表未 onboard）
5 ├── 2. dw_get_table_source(table) ← 取 ETL 源代码
6 │ ↓ 拿到 SQL
7 └── 3. parse_sql_lineage(sql, column) ← AST 实时解析
8 ↓ 返回字段映射、来源表、WHERE 条件
解析能⼒覆盖
引擎能处理复杂 ODPS SQL 语法，包括：
```

## PDF 第16页

[查看原页](RAW.pdf#page=16)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
准确性保障
内置 回归测试框架，覆盖 45 张真实表、296 个节点：
▐ 6.4 指标注册体系
指标注册表（Layer 5）是波动归因诊断的核⼼知识源——它定义了每个业务指标如何拆解。
为什么需要指标注册？
归因诊断的核⼼是"拆解"：GMV 跌了 20%，要拆成访客数 × 转化率 × 客单价，找出哪个因⼦
是主因。但"GMV 等于什么"这个知识从哪来？
如果靠 LLM ⾃⼰猜，它可能拆成"流量 × 客单价"——漏掉了转化率。如果写死在代码⾥，每
加⼀个指标都要改代码。
指标注册体系让指标定义成为声明式配置，运营同学通过 Web 向导就能接⼊新指标。
```

## PDF 第17页

[查看原页](RAW.pdf#page=17)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
三种公式类型
MetricDef 结构
以 GMV 为例，⼀个完整的指标定义：
1 metric_id: gmv
2 name: GMV
3 formula_type: multiplicative
4 description: ⽀付GMV，流量漏⽃拆解为 曝光UV × 转化率 × 客单价
5 total_col: pay_amt
6 factors:
7 - name: IPVUV
8 label: 曝光UV
9 type: column # 直接取列值
10 column: ipv_uv
11 - name: CVR
12 label: 转化率
13 type: ratio # 分⼦/分⺟
14 numerator: ord_cnt
15 denominator: ipv_uv
16 - name: AOV
17 label: 客单价
18 type: ratio
19 numerator: pay_amt
20 denominator: ord_cnt
21 source:
22 table: ads_sup_index_di
23 dimensions:
24 - dim_col: ind1_name
25 label: ⾏业
26 perspective: goods # 供给/商品类
27 axis: business
28 - dim_col: act_type
29 label: 活动类型
30 perspective: place # 渠道/流量类
```

## PDF 第18页

[查看原页](RAW.pdf#page=18)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
31 axis: traffic
32 aliases: [gmv_amt, 交易额, 成交额]
乘法型恒等式铁律：因⼦相乘后约分必须恰好等于 total_col。
1 GMV = IPVUV × CVR × AOV
2 = ipv_uv × (ord_cnt / ipv_uv) × (pay_amt / ord_cnt)
3 = pay_amt ✅
维度分类体系
每个指标关联⼀组可拆解维度，维度按两个正交轴分类：
AI 辅助接⼊流程
指标接⼊通过 Web 平台的"指标接⼊向导"完成，AI 辅助⽣成 MetricDef：
1 1. 选择 MDL 表 → 系统列出表结构和字段
2 2. AI ⽣成 MetricDef → LLM 根据 schema ⾃动推导公式类型和因⼦
3 3. 预览⽣成的公式 → 校验恒等式、维度分类
4 4. 确认⼊库 → 写⼊ metrics.yaml + formula_registry
5 5. ⾃动同步 → 刷新 metric_registry 缓存
```

## PDF 第19页

[查看原页](RAW.pdf#page=19)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
AI ⽣成时的容错机制：
perspective/axis 混淆⾃动修正（LLM 常把 axis 值填到 perspective）
Pydantic schema 逐条校验，不合法的标红但不阻断合法项
注⼊ table_profile 信息辅助 AI 理解 ROLLUP/CUBE 结构
指标与归因诊断的关系
指标注册表直接驱动归因诊断树（详⻅第七章）：
1 metrics.yaml (指标定义)
2 │
3 ▼
4 formula_registry (公式展开)
5 │ GMV → [漏⽃公式: IPVUV × CVR × AOV]
6 │ [加法公式: Σ(各⾏业 GMV)]
7 │ [⽐率公式: GMV / 总流量]
8 ▼
9 归因诊断引擎
10 │ 多路筛选 → 选最显著拆解
11 │ 递归下钻 → 沿主因⼦逐层拆
12 ▼
13 诊断树报告
▐ 6.5 知识在 ReAct 中的使⽤
Agent 在 ReAct 循环中会主动调⽤知识检索⼯具，每层知识对应不同的⼯具：
1 Agent 思考："⽤户问 GMV，我需要先找表"
2 → search_metrics("GMV") ← Layer 5: 指标定义 (找到 gmv_amt)
3 → cap_search("GMV ") ← Layer 1: 能⼒清单 (找到表)
4 → snippet_search(table="ads...") ← Layer 2: SQL 模板
5 → rule_search(table="ads...") ← Layer 3: 编写规则
6 → lightrag_table_lineage("ads...")← Layer 4: ⾎缘关系 (KG)
7 → parse_sql_lineage(sql="...") ← Layer 4: ⾎缘关系 (AST 实时)
▐ 6.6 采集与治理闭环
知识不是静态的，⽽是采集 → 沉淀 → 审核 → 复⽤的闭环：
```

## PDF 第20页

[查看原页](RAW.pdf#page=20)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
1 ┌─────────────┐
2 │ 采集⼊⼝ │
3 └──────┬──────┘
4 │
5 ┌────────────────┼────────────────┐
6 │ │ │
7 ▼ ▼ ▼
8 AST ⾎缘解析 对话产出 SQL 指标接⼊向导
9 (ETL 源代码) (⾃动暂存) (AI ⽣成)
10 │ │ │
11 ▼ ▼ ▼
12 LightRAG KG Staging 队列 metrics.yaml
13 (⾎缘图谱) (待审核⽚段) (指标定义)
14 │ │ │
15 └────────────────┼────────────────┘
16 │
17 ┌──────▼──────┐
18 │ ⼈⼯审核 │
19 │ (Web 平台) │
20 └──────┬──────┘
21 │
22 ┌──────▼──────┐
23 │ ⼊库复⽤ │
24 │ 下次 Agent │
25 │ 优先命中 │
26 └─────────────┘
27 │
28 表结构变更 → ⾃动 regenerate
29 → 更新规则/⽚段/AST ⾎缘
Web 平台提供完整的知识管理界⾯：
```

## PDF 第21页

[查看原页](RAW.pdf#page=21)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
分析能⼒深度解析
▐ 7.1 波动归因诊断（Analysis Agent）
⽤户视⻆：
“昨天 GMV 为什么跌了 20%？”
Agent ⾃动构建诊断树：
1 GMV 环⽐ -20%
2 │
3 ├── 漏⽃拆解：GMV = 访客数 × 转化率 × 客单价
4 │ ├── 访客数 +5% ← 不是原因
5 │ ├── 转化率 -22% ← ⭐ 主因！
6 │ └── 客单价 +3% ← 不是原因
7 │
8 ├── 转化率 -22% 按⾏业拆
9 │ ├── 家电 -45% ← ⭐ Top1 贡献
10 │ ├── 服装 -8%
11 │ └── ⻝品 +2%
12 │
13 ├── 家电转化率 -45% 指标拆解
14 │ ├── 下单量 -40% ← ⭐ 主因
15 │ └── 访问量 -8%
16 │
17 └── 结论：家电⾏业下单量骤降导致 GMV 下跌
技术实现五步法：
```

## PDF 第22页

[查看原页](RAW.pdf#page=22)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 7.2 ⾎缘溯源
⽤户视⻆：
“GMV 这个字段是怎么计算出来的？上游依赖哪些表？”
Agent 的⾎缘溯源有两条路径，形成 KG 优先、AST 降级的降级链：
1 # 路径 1: 查 LightRAG 知识图谱（local 模式）
2 lightrag_column_logic(table="ads_flow_sum_di", column="gmv_amt")
3 → gmv_amt = pay_amt (直接映射)
4 上游: dwd_ord_ent.pay_amt
5 过滤: WHERE activity_type =''
6 # 路径 2: KG 未命中时，AST 实时解析 ETL 源代码
7 dw_get_table_source(table="ads_flow_sum_di") → 拿到 SQL
8 parse_sql_lineage(sql_text="INSERT OVERWRITE TABLE ...", target_column=
9 → gmv_amt = pay_amt
10 source_columns: [dwd_ord_ent.pay_amt]
11 where_conditions: [activity_type ='']
12 # 查表的完整上游依赖（hybrid 模式）
13 lightrag_table_lineage(table="ads_flow_sum_di")
14 → 上游依赖 3 张表:
15 1. dwd_ord_ent (交易明细)
16 2. dim_activity_info (活动维表)
17 3. dws_flow_sum_h (⼩时汇总)
```

## PDF 第23页

[查看原页](RAW.pdf#page=23)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
KG 中的⾎缘数据由 AST 引擎在 onboard 时离线解析并灌⼊，实时解析作为降级补充。详⻅
6.3 节。
▐ 7.3 Python 数据分析沙箱
当 查 询 结 果 需 要 ⼆ 次 加 ⼯ 时 （ 帕 累 托 、 排 名 、 透 视 、 环 ⽐ 计 算 ） ， Agent 会 调
⽤ python_analyze ：
1 # Agent ⽣成的分析代码（沙箱内执⾏）
2 df['环⽐'] = (df['today'] - df['yesterday']) / df['yesterday']
3 df = df.sort_values('today', ascending=False)
4 df['累计占⽐'] = df['today'].cumsum() / df['today'].sum()
5 result = df[['industry', 'today', 'yesterday', '环⽐', '累计占⽐']].head(
6 print(result.to_markdown())
安全模型：
系统构建与部署
▐ 8.1 新表接入流程（Onboard）
新表接⼊是⼀个⾃动化的五步流⽔线：
1 1. 表结构同步 → ODPS schema → mdl.json + TisPlus3
2 2. 表类型探查 → A类(预聚合)/B类(普通) + 主键 + 维度
3 3. 规则抽取 → 下游⾎缘代码 → LLM 提取 WHERE 条件
4 4. SQL 模板⽣成 → B类表⾃动⽣成标准模板
5 5. ⼊库 → 规则/⽚段/能⼒清单写⼊ TisPlus3
```

## PDF 第24页

[查看原页](RAW.pdf#page=24)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
⽀持 Web 界⾯操作和 CLI 脚本两种⽅式。
▐ 8.2 项⽬结构
1 bybt-data-analysis-assistant/
2 ├── agent.py # CLI ⼊⼝ + Agent 构建
3 ├── agent_analysis.py # 模板分析⼊⼝
4 ├── config.py # 全局配置（ODPS/LLM/TisPlus3/...）
5 ├── boot.sh # ⽣产部署脚本
6 │
7 ├── agents/ # 多 Agent 架构
8 │ ├── supervisor.py # 路由调度器
9 │ ├── intent_agent.py # 意图识别 Agent
10 │ ├── base_expert.py # 专家 Agent 基类
11 │ ├── query_agent.py # 取数+⾎缘+元数据+源代码+SQL开发
12 │ ├── analysis_agent.py # 波动归因+数据分析
13 │ ├── ops_agent.py # 调度运维
14 │ ├── other_agent.py # 兜底寒暄
15 │ ├── harness.py # 运⾏时安全守卫
16 │ └── sql_validator_gate.py # SQL 后置校验
17 │
18 ├── tools/ # ⼯具集（Agent 的"⼿"）
19 │ ├── odps/ # ODPS 查询 + SQL 构建
20 │ ├── capabilities/ # 表能⼒清单检索
21 │ ├── snippets/ # SQL ⽚段检索
22 │ ├── rules/ # SQL 规则检索
23 │ ├── lineage/ # ⾎缘知识图谱
24 │ ├── analysis/ # Python 分析沙箱
25 │ ├── attribution/ # 归因诊断引擎
26 │ ├── dataworks/ # DataWorks API
27 │ ├── memory/ # 会话记忆
28 │ └── intent/ # 意图识别
29 │
30 ├── web/ # Web 平台
31 │ ├── api/ # FastAPI 后端
32 │ └── frontend/ # React 前端
33 │
34 └── wren_project/ # WrenAI MDL 语义模型
35 ├── target/mdl.json # 模型定义⽂件
36 └── .wren/memory/ # 向量索引
```

## PDF 第25页

[查看原页](RAW.pdf#page=25)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
评测体系
Agent 的「聪明」不能靠感觉判断，必须有可量化、可复现的评测体系。本章回答三个核⼼问
题：评什么（6D 维度）、怎么构造样例（Golden Dataset）、怎么打分（意图感知权重 +
节点归因）。
▐ 9.1 6D 评分维度
评测从 6 个维度对 Agent 的每次回答打分，每个维度 0-100 分：
▐ 9.2 意图感知权重
不同意图关注点不同——归因分析不关⼼ SQL 正确性（D5=0），取数不关⼼因⼦命中
（D1=0）。系统为每个意图配置了差异化权重：
```

## PDF 第26页

[查看原页](RAW.pdf#page=26)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
权重为 0 的维度显示为 -- ，不参与打分。权重可通过 Web 界⾯⾃定义调整
（scripts/eval/metrics_config.json ）。
▐ 9.3 Golden Dataset — 样例构造
评测样例存放在 scripts/eval/datasets/default.json ，当前覆盖 6 类意图、15
个⽤例：
```

## PDF 第27页

[查看原页](RAW.pdf#page=27)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
单个样例结构示例：
1 {
2 "id":"gmv_daily_attribution",
3 "question":"20260610 GMV波动分析",
4 "intent":"analysis",
5 "tags":["attribution","gmv","daily"],
6 "expected":{
7 "main_factor":["3C数码","坑产","平台出资","GMV_PER_ITEM"],
8 "main_factor_fuzzy":["3C","坑产","平台"],
9 "formula_used":["gmv.industry","gmv.supply","gmv_per_item.is_bt"],
10 "direction":"up",
11 "min_tree_depth":2,
12 "must_call_tools":["attribution_diagnose","attribution_explain"],
13 "must_not_call_tools":[],
14 "conclusion_must_contain":["贡献","主因","3C"]
15 }
16 }
样例设计原则：
expected 多层校验：不只看最终回答，还看中间过程（⼯具调⽤序列、SQL 内容、诊断
树结构）
模糊匹配兜底：main_factor_fuzzy 允许部分命中得 60 分，避免因措辞差异误判
意图覆盖：每类意图⾄少 2 个⽤例，边界⽤例覆盖错误输⼊场景
可扩展：通过 Web 界⾯「评测中⼼」可在线增删⽤例，⽆需改代码
▐ 9.4 评测执⾏流程
1 ⽤户提问
2 │
3 ▼
4 harness.run_case(question)
5 │ 调⽤ stream_supervised() 获取 SSE 事件流
6 │ 收集: tool_call / tool_result / token / routing / validation 事件
7 │ 解析: attribution_diagnose 返回的诊断树 JSON
8 │ 检测: HOLO fallback 标记
9 ▼
10 EvalTrace (结构化 trace)
11 │ events: 全部 SSE 事件
```

## PDF 第28页

[查看原页](RAW.pdf#page=28)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
12 │ tool_calls: ⼯具调⽤序列
13 │ tool_results: ⼯具返回结果
14 │ diagnosis_tree: 诊断树 JSON
15 │ final_answer: 最终回答
16 │ nodes: 7 个关键节点的状态
17 ▼
18 6D 打分 (scorers)
19 │ D1 factor_scorer → 严格匹配(100) / 模糊匹配(60) / ⽅向匹配(30) / 不
20 │ D2 tree_scorer → 深度 + 分⽀数 + ⽅向
21 │ D3 tool_scorer → must_call(40) + must_not_call(25) + orderin
22 │ D4 conclusion_scorer → LLM-as-Judge 按意图 Rubric 打分
23 │ D5 sql_scorer → 语法 + 表名 + 字段名 + WHERE + ⽩名单
24 │ D6 faithfulness_scorer → 规则检查 + LLM 幻觉检测
25 ▼
26 加权总分 = Σ(Di × Wi) → 意图感知权重
27 ▼
28 报告输出
29 ├── 终端彩⾊报告 (6D 分数 + 归因诊断)
30 ├── JSON 报告 → reports/eval_<timestamp>_<git_hash>.json
31 ├── Bad Case 归档 → badcases/ (总分<60 或任⼀维度=0)
32 └── 版本对⽐ → --compare old.json new.json
▐ 9.5 节点级归因诊断
评测不只给分数，还⾃动定位失败根因。Harness 从事件流中提取 7 个关键节点的状态：
当总分低于预期时，归因诊断会指出是哪个节点出了问题，例如：
1 根因: gate - validation_exhausted (重试 3 次未通过)
2 根因: tool_call - ⼯具返回错误: odps_query
```

## PDF 第29页

[查看原页](RAW.pdf#page=29)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
3 根因: quality - 各节点均成功，但回答质量未达预期
团队介绍
本⽂作者伯略，来⾃淘天集团-天猫技术团队。百亿补贴与聚划算是淘天⾯向价格敏感⽤户与
品牌商家的核⼼营销阵地，也是我们直⾯市场竞争最前沿的“主战场”；我们不断“刷新”技术能
⼒，以半托管、竞价与补贴系统的建设，⽀撑百亿补贴成为淘天近三年增⻓最快的业务。如今
我们正⽤ AI 重构从招商审核到补贴发放的运营全流程，推动“⼈⼯配置”向“AI ⾃治”演进，并
把研发链路重塑为需求分析、代码⽣成到测试上线的端到端 AI 原⽣范式。
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | ⾳视频技术
服务端技术 | 技术质量 | 数据算法
⼤淘宝技术
⼤淘宝技术官⽅账号
964篇原创内容
公众号
阅读 9127
留⾔
写留⾔
还没有留⾔，来写⾸评
```

## PDF 第30页

[查看原页](RAW.pdf#page=30)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
[本页未提取到文字；页面实际状态见META核验记录。]
```

