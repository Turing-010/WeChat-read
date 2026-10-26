# agent优化之GEPA——一种提示词自进化的优化方案：PDF文本转写

> 这是RAW.pdf的文本层转写，不是AI总结。页码为PDF物理页码；未恢复原版面、表格或代码缩进。文本框长行、缺图与未加载内容不能仅靠文字提取判定完整。

[原始PDF](RAW.pdf) · [外部AI总结](AI_GEPA提示词优化.md) · [来源与质量](META.json)

## PDF 第1页

[查看RAW.pdf第1页](RAW.pdf#page=1)

> 本页含2个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
agent优化之GEPA——⼀种提示词⾃进化的优化⽅案
原创 营销&交易技术 ⼤淘宝技术 2026年9⽉15⽇ 23:12 浙江 33⼈
本⽂基于GEPA（Genetic-Pareto，Reflective Prompt Evolution）[1]算法，设计并
实现了⼀套Prompt ⾃进化系统，解决当前Prompt优化依赖⼈⼯经验导致的盲⽬性⾼、
难以复制、缺乏权衡机制等痛点。该系统构建"推理→评分→反思→选择"的⾃动化闭环，
通过数据驱动的反思式变异机制，让LLM⾃动分析Badcase、归因⾄Prompt具体规则、
⽣成候选变体，并基于帕累托前沿 进⾏多⽬标择优，避免单点优化引发的指标对抗性退
化[1]。系统采⽤任务⽆关架构，⽀持⼆分类、多分类、评分等多种场景，通过零配置设计
实现⾃动数据集分析与配置推断，同时提供可解释的优化过程。GEPA将Prompt优化从
⼈⼯试错转变为有量化依据的⾃动化寻优，显著提升与⼈⼯标注及线上业务效果的对⻬能
⼒，为AI评估器提供可持续进化的技术底座。
背景：为什么要做这件事
▐ 1.1 现状痛点：prompt缺乏⾃进化的调优闭环
⽬前 LLM Judge / 被评测Agent 的 Prompt 优化主要依赖⼈⼯经验驱动，存在四个核⼼问
题：
盲⽬性⾼：⼈⼯修改 Prompt 缺乏数据⽀撑，优化⽅向靠直觉试错，⽆法量化验证
伪⾃动化：现有的 Prompt 优化（如⽤更强模型做静态扫描）本质是浅层迭代，缺乏深度
的"反思-修正"逻辑（Self-Reflection），⽆法形成真正的智能进化闭环
难以复制：调优经验沉淀在个⼈，没有标准化流程，⽆法规模化推⼴到多个业务场景
⽆权衡机制：诊断⽅向单向，缺什么补什么，补完往往⼀边好⼀边坏；单点改动缺乏多⽬
标博弈能⼒，⽆法在对抗指标间显式保留权衡⾯（Pareto Frontier）
▐ 1.2 业务挑战：评估器存在两⼤对齐难题
```

## PDF 第2页

[查看RAW.pdf第2页](RAW.pdf#page=2)

> 本页含1个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
在实际业务中，LLM Judge 作为“裁判”，其判断标准如果发⽣偏移，整个评测体系就会失
效。因此，我们⾯临两⼤核⼼对⻬⽬标：
评估器与⼈⼯标注对⻬ — LLM Judge 的输出要和⼈⼯标注的 Ground Truth ⼀致，确保
离线评测具备基本的准确性底座。
评估器与线上业务效果对⻬ — LLM Judge 的判断要和线上实际业务指标（CTR、转化率
等）⼀致，确保离线⾼分的 Prompt 上线后不会“翻⻋”。
这两⼤对⻬问题⼴泛存在于我们AI项⽬各场景中。若沿⽤1.1⼈⼯经验驱动范式执⾏对⻬，将陷
⼊以下困境：启发式盲调收敛效率极低；静态扫描⽆法弥合深层语义错位；单点修补易引发多
⽬标对抗性退化，顾此失彼；且专家经验难以跨域复⽤，新业务需反复经历试错循环。
▐ 1.3 技术调研：从论⽂到⽅案
基于上述痛点，我们深⼊调研了 Reflective Prompt Evolution 类前沿⼯作。其中，ICLR
2026 收 录 的 《 GEPA: Reflective Prompt Evolution Can Outperform Reinforcement
Learning》 提供了核⼼技术路径。该论⽂提出反思式变异（Reflective Mutation）机制，构
建持续进化闭环：LLM ⾃动分析 Badcase -> 归因⾄ Prompt 具体规则 -> ⽣成候选变体 -
> 基于帕累托前沿（Pareto Frontier）多⽬标择优[1]。其中，GEPA ⾪属于斯坦福⼤学提出
的 DSPy（Declarative Self-improving Python）[2] ⽣态，旨在将⼤模型应⽤开发从⼿⼯提
示⼯程转化为系统化的算法优化范式。
图1 GEPA迭代进化与帕累托采样流程[1]
该论⽂的启发：
1）⽤“数据驱动闭环”替代“经验盲调”
```

## PDF 第3页

[查看RAW.pdf第3页](RAW.pdf#page=3)

> 本页含2个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
GEPA的反思式变异机制表明，Prompt优化可以交由算法基于实测数据反馈，来⾃动归因与⽣
成变体，让我们将⼈⼯直觉试错，转化为有量化依据、可收敛的⾃动化寻优过程。
2）⽤“帕累托择优”弥补“⽆权衡机制”
传统单点修补容易导致指标振荡。如上图1所示，GEPA的帕累托采样机制表明，我们⽆需始终
选择表现最优的单⼀候选进⾏变异，以避免陷⼊局部最优，⽽是从各任务最优候选集中筛选采
样来确保多样性，在指标振荡中保留最优权衡⾯[1]。
3）如何实现从“学术原型”到“业务引擎”的⼯程跨越
原⽣的框架缺乏对复杂业务流的⽀持，这启示我们不能仅作浅层调⽤，必须构建和任务⽆关的
适配层，将诊断先验与通⽤接⼝沉淀为标准流⽔线，"每个场景都要写代码"变成"填配置就能
⽤"，解决规模化复⽤难题。构想如下：
图2 基于GEPA的prompt⾃进化架构图
⽬标
▐ 2.1 核⼼⽬标
给 AI ⼀条提示词和⼀份标注数据，它还你⼀条更好的提示词。
具体⽽⾔：
1. ⾃动化 — 建⽴标准化的 Prompt ⾃动迭代流程，替代⼈⼯调优
2. 通⽤性 — 任务⽆关（Task-agnostic）架构，覆盖⼆分类、多分类、评分、对⽐、聚类等
多种任务类型
```

## PDF 第4页

[查看RAW.pdf第4页](RAW.pdf#page=4)

> 本页含1个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
3. 零配置 — ⽤户只需提供标注数据 + 任务⽬标，系统⾃动推断配置
4. 可解释 — 每轮优化有明确的错误归因和改进⽅向，⾮盲⽬搜索
▐ 2.2 可覆盖的场景
常⻅任务类型举例如下（可拓展）：
任 务 类 对 ⻬ ⽬
场景举例 输出形式
型 标
⼈ ⼯ 标
内容安全审核 pass / block
注
⼆分类
⼈ ⼯ 标
客服意图识别 正确 / 错误
注
⼈ ⼯ 标
多分类 主题分类 服饰 / 数码 / ⻝品 / ...
注
⼈ ⼯ 标
评分 策略有效性评分 1-5 分
注
Rubric Judge（多维检查清 每条规则 pass / fail → 汇总裁决通过 ⼈ ⼯ 标
规则判定
单） 率 注
⼈ ⼯ 标
聚类 相似商品聚合 同类商品簇 ID
注
⼈ ⼯ 标
对⽐ Pairwise Judge chosen / rejected
注
整体架构设计
▐ 3.1 GEPA主循环系统架构总览
GEPA 的优化主循环由四个核⼼环节组成，形成"推理 → 评分 → 反思 → 选择"的闭环：
```

## PDF 第5页

[查看RAW.pdf第5页](RAW.pdf#page=5)

> 本页含1个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
图3 GEPA优化主循环示意图[1]
各环节详细说明：
① 种⼦提示词
职责：提供优化的起点
实 现 细 节 ： ⽤ 户 提 供 的 初 始 prompt ， 或 由 Inspector ⾃ 动 ⽣ 成 的
suggested_system_prompt。⽀持从⽂件加载或内联⽂本
② LLM 推理
职责：⽤当前 prompt 执⾏任务
实现细节：任务模型对训练集批量推理：将 system_prompt + user_message 发送
给 LLM，获取原始输出 raw_response[]。温度 = 0.0 保证结果可复现。⽀持批量并
发调⽤
③ 评分器
职责：量化输出质量
实现细节：先通过输出解析器提取结构化结果（JSON 字段提取 / 正则匹配），再按
任务类型选择评分函数计算得分，例如⼆分类⽤ Precision / Recall / F1，评分类⽤
Cohen's Kappa / Spearman 相关系数 / MAE，聚类⽤配对 F1 / 兰德系数 （ARI）
等
④ 反思与变异
职责：分析错误并⽣成改进 prompt
实现细节：分两步完成闭环：a) 错误归因：对错误样本调⽤ LLM Judge 做三维分
析，(1) 错误定位 (2) Prompt 归因 (3) 改进建议，⽣成结构化反馈⽂本；b) Prompt
变异：反思模型（建议⽐任务模型更强，温度 0.7）接收反思数据集（输⼊ + 输出 +
分数 + 反馈），分析错误模式并⽣成改进后的 prompt 候选，通过 Pareto 前沿选择
保留多⽬标最优解
什么是 Pareto 前沿选择？在 prompt 优化中，我们通常要同时优化多个指标（如精确率和召回
率）。假设有 4 个候选 prompt：GEPA 保留前沿上的所有候选（A、B、D），⽽不是只选“综
合得分最⾼”的⼀个，因为不同业务场景可能需要不同的权衡策略。
三个模型的⻆⾊分⼯：
```

## PDF 第6页

[查看RAW.pdf第6页](RAW.pdf#page=6)

> 本页含1个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
任务模型
默认模型：可选 · 温度=0.0
职责说明：⽤当前 prompt 执⾏任务（分类/评分/聚类），追求快速、确定性输出
Judge 模型
默认模型：可与任务模型相同或独⽴
职责说明：分析错误样本：(1) 错误定位 (2) Prompt 归因 (3) 改进建议。独⽴模型可
提供更客观的第三⽅视⻆
反思模型
默认模型：可选 · 温度=0.7
职责说明：接收所有反馈，⽣成改进后的 prompt 候选。建议⽐任务模型更强，⿎励创
造性变异
▐ 3.2 核⼼⼯作流设计（五步法）
最初我们为每个业务场景单独编写 Adapter，n个场景n套代码，每接⼊⼀个新场景，需要从零
写 Adapter（数据加载、输出解析、评分函数、反馈⽣成全部定制），⽆法复⽤。在2.0版
本，GEPA Service 将共性逻辑抽象为 n 种任务类型，通过配置驱动，不再需要为每个场景写
Adapter。具体⼯作流如下：
图4 GEPA使⽤流程示意
▐ 3.3 代码架构
分层设计思路：
层
职责 关键⽂件
级
配 回答"这个任务该怎么跑"。⽤ Pydantic 模型定义所有配 config.py — 定义 TaskC
置 置项，并通过 build_config() ⾃动对⻬输出 sche onfig 等配置模型
层 ma、答案提取⽅式、评分⽅式三者，避免⼿动配置出错 config_factory.p
y — build_config
```

## PDF 第7页

[查看RAW.pdf第7页](RAW.pdf#page=7)

> 本页含0个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
() 按任务类型⾃动⽣成完整
配置
engine.py — 对外⼊⼝，
暴露三个核⼼ API
回答"怎么把任务跑起来"。对外暴露三个核⼼函数（ r
引 adapter.py — Generic
un_optimize / run_evaluate / validate_con
擎 GEPAAdapter ，连接 GEPA
fig ），对内负责数据加载、适配器组装、模型构建的
层 框架和具体任务
编排
run.py — 内部编排，准备
数据和构建模型
parsers.py — 从 LLM 输
出中提取结构化结果
scorers.py — 各种评分
函数（精确匹配/F1/加权等）
feedback.py — ⽣成反馈
组 （规则层 + LLM Judge 深度
回答"具体怎么做每⼀步"。可插拔的功能模块，通过 Pr
件 层）
otocol 协议扩展，新场景只需实现对应接⼝
层 llm.py — 统⼀ LLM 调⽤
（批量/重试/多 Provider）
evaluate.py — 按任务类
型计算评估指标
inspector.py — ⾃动分
析数据集，推断任务配置
api.py — FastAPI HTTP
服务
服 jobs.py — 任 务 管 理 器
回答"怎么让⽤户⽤上"。提供多种使⽤⽅式：CLI 命令
务 （持久化到⽂件系统）
⾏、HTTP API、Claude Code Skill
层 progress.py — 实时进度
输出（JSONL，供 Claude 读
取）
具体代码架构如下所示：
1 gepa-service/
2 ├── SKILL.md # Skill 定义
3 ├── README.md # 项⽬⽂档
4 ├── CLAUDE.md # Claude Code 项⽬指引
5 ├── requirements.txt # Python 依赖
6 │
7 ├── .claude/
8 │ └── skills/gepa/SKILL.md → symlink → ../../SKILL.md
```

## PDF 第8页

[查看RAW.pdf第8页](RAW.pdf#page=8)

> 本页含1个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
9 │
10 └── scripts/ # 核⼼代码
11 ├── __init__.py # 公开 API 导出
12 ├── __main__.py # CLI ⼊⼝（python -m scripts）
13 │
14 │ ─── 配置层 ───
15 ├── config.py # Pydantic 配置模型（TaskConfig 等）
16 ├── config_factory.py # 安全配置构建器（build_config）
17 │
18 │ ─── 核⼼引擎层 ───
19 ├── engine.py # 核⼼引擎（run_optimize / run_evaluate
20 ├── adapter.py # GEPA 适配器（GenericGEPAAdapter，编排中
21 ├── run.py # 内部编排（数据准备 / 模型构建）
22 │
23 │ ─── 组件层 ───
24 ├── data.py # 数据加载 / 切分 / 格式化
25 ├── inspector.py # 数据集智能分析（零配置推断）
26 ├── llm.py # LLM 客户端（批量调⽤ / 重试 / 多 Provide
27 ├── parsers.py # 输出解析（JSON / 正则 / Schema 校验）
28 ├── scorers.py # 评分函数（精确匹配 / F1 / 加权 / 数值接近度
29 ├── evaluate.py # 评估指标计算（⼆分类 / 多分类 / 规则判定 /
30 ├── feedback.py # 反馈引擎（规则 + LLM Judge 深度分析）
31 ├── protocols.py # 扩展协议和基类（可插拔组件接⼝）
32 │
33 │ ─── 服务层 ───
34 ├── progress.py # 进度输出（JSONL ⽂件）
35 ├── jobs.py # 任务管理器（⽂件系统持久化）
36 └── api.py # FastAPI HTTP 服务
技术实现细节
按 3.3 的分层架构，逐层说明每层解决的关键问题与设计取舍。
▐ 4.1 配置层：让⼈“配不错”
4.1.1 配置模型（ config.py ）
配置顶层是 TaskConfig ，向下聚合各环节的⼦配置：
```

## PDF 第9页

[查看RAW.pdf第9页](RAW.pdf#page=9)

> 本页含0个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
配置模型 职责
TaskConfig 顶层配置，聚合所有⼦配置
ModelConfig LLM 模型配置（任务模型、反思模型、Judge 模型、API 端点）
DataConfig 数据配置（路径、格式、标注字段、切分策略）
PromptConfig 提示词配置（system_prompt、user_template）
InputConfig 输⼊配置（⽂本/多模态、图⽚字段）
OutputConfig 输出配置（schema 定义、答案提取⽅式）
ScoringConfig 评分配置（⽅法名、参数、批次/样本模式）
FeedbackConfig 反馈配置（Judge prompt、截断⻓度）
OptimizationConfig 优化配置（最⼤调⽤次数、停⽌条件、反思批量⼤⼩）
EvaluationConfig 评估配置（指标类型：binary/multiclass 等）
4.1.2 安全配置构建器（ config_factory.py ）
三者之间存在隐式耦合：输出 schema 的字段类型、答案提取⽅式、评分函数必须互相匹配。
我们不让⽤户逐项填，⽽是由 build_config() 按任务类型套预设，⼀次性把三者对⻬：
优化评分（GEP 对⻬指标（输出
任务类型 Schema 主字段 提取⽅式
A ⽬标） vs 标注）
Precision / Recal
result: boo
⼆分类 binary json_field / bool exact_match l / F1 / Accuracy
l
+ 混淆矩阵
Accuracy + 各类
多分类 multiclas result: str
json_field / str exact_match 别 Precision / Re
s （enum）
call / F1
MAE / RMSE / S
result: floa numerical_close pearman 秩相关
评分 scoring json_field / float
t ness / 加 权 Kappa
（QWK）
Accuracy + 分侧
result: str
对⽐ comparison json_field / str comparison 准确率 + 位置偏
（a / b）
差分数
聚类 clustering result: str json_field / str pair_f1 兰德系数（AR
（簇 ID） I）/ Cohen's Ka
```

## PDF 第10页

[查看RAW.pdf第10页](RAW.pdf#page=10)

> 本页含0个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
ppa + 配对 P / R
/ F1
▐ 4.2 核⼼引擎层：把任务跑起来
4.2.1 核⼼引擎（ engine.py ）
对外暴露三个核⼼ API：
API 功能 返回
OptimizeResult （best_pro
run_optimize(config, run_
执⾏完整的 prompt 优化循环 mpt、best_score、迭代次数
dir)
等）
run_evaluate(config, prom 评估指定 prompt 在某个数据 EvalResult （metrics、per_
pt, split) 切⽚上的表现 sample 详情）
validate_config(config) 只校验配置有效性，不跑优化 (valid, error_message)
run_optimize 的内部编排：准备数据（train/val/holdout）→ 组装适配器 → 构建反思模
型 → 设置停⽌条件（连续⽆提升 / 达到⽬标分数）→ 进⼊ GEPA 主循环 → 保存最优 prompt
→ 在 holdout 上复评泛化能⼒。
4.2.2 通⽤适配器（ adapter.py ）
适配器 GenericGEPAAdapter 是全流程的编排中枢，它把 GEPA 框架的⼀次“候选评估”
翻译成四步：
1. 批量推理 — 把候选 prompt（⾃动拼上输出格式指令）与⽤户消息发给任务模型
2. 解析输出 — 从原始回复中提取结构化答案（json_field / regex / full_text / ⾃定义）
3. 批次评分 — 计算批次级分数，这就是 GEPA 的优化⽬标
4. ⽣成反思轨迹（仅反思轮需要） — 逐样本打分，满分样本给⼀句确认，错误样本交给
LLM Judge 做深度归因
反思轨迹最终整理成 GEPA 能读的四元组——输⼊、模型原始输出、样本分数、反馈⽂本——
这也是反思模型改写 prompt 的全部依据。
4.2.3 内部编排（ run.py ）
```

## PDF 第11页

[查看RAW.pdf第11页](RAW.pdf#page=11)

> 本页含1个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
提供引擎层内部的三个构建函数：
函数 职责
加载数据集 → 校验格式 → 分层切分 → 模板格式化 → 返回 trai
prepare_data(config)
n/val/holdout
根据配置构建 LLMClient（任务模型 + Judge 模型）→ 组装 Ge
build_adapter(config)
nericGEPAAdapter
build_reflection_lm(co 构建反思模型的 callable（温度 0.7，⽀持 DashScope 特殊参
nfig) 数）
▐ 4.3 组件层：可插拔的六个模块
4.3.1 数据加载与切分（ data.py ）
流⽔线：加载（json / jsonl / csv）-> 按任务类型严格校验标注 -> 分层切分（train 50%
/ val 30% / holdout 20%）-> 模板格式化 -> 转成 GEPA 的 DataInst 格式。
两处细节值得⼀提：切分按标签分层（⼆分类按 true/false、多分类按各类别、连续值先分位
数分桶再分层），保证各切⽚分布⼀致；校验采⽤严格模式，在跑之前就发现数据问题。
4.3.2 零配置推断（ inspector.py ）
传统框架需要⽤户⼿动配置⼗余项参数，Inspector 能⾃动分析数据集结构。⼯作流程如下图
所示：
```

## PDF 第12页

[查看RAW.pdf第12页](RAW.pdf#page=12)

> 本页含0个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
图5 数据集智能分析示意⼯作流
它先给每个字段做画像（数据类型、唯⼀值数量、是否⼆值/分类/⻓⽂本/URL、平均⻓度、缺
失率），再据此并⾏推断三件事：哪个字段是标注、这是什么任务、哪些字段是输⼊，最后给
出⼀个置信度评估，产物是 DatasetProfile ，包含任务类型、字段划分、建议模板、建
议种⼦提示词、枚举值/分数范围等完整配置建议。
4.3.3 模型调⽤与输出解析（ llm.py / parsers.py ）
llm.py 基于 litellm 统⼀多 Provider 调⽤（按 api_base ⾃动识别 DashScope /
OpenAI / Anthropic / Moonshot / 智谱），并处理⼯程上的脏活：批量并发、指数退避重试
（2s → 4s → 8s，最多 3 次）、单请求失败不拖垮整批、每次调⽤都带结构化的 succes
s / error ⽽不静默吞异常。
parsers.py 负责把 LLM 的⾃由⽂本变成可⽐对的值：先清洗，再按配置选择 json_field /
regex / full_text / ⾃定义策略提取。若配置了 OutputSchema ，还会校验字段类型、
enum 范围、数值上下界；同时由 build_format_instruction() 从 schema 反向⽣
成输出格式说明，追加到 system_prompt 末尾，让「要求的格式」和「校验的格式」永远同
源。
4.3.4 评分函数与评估指标（ scorers.py / evaluate.py ）
评分分两级，服务两个不同⽬的：
样本级（给反思轨迹⽤，回答「这⼀条错在哪」）：如 exact_match、contains、
numerical_closeness（按误差线性/平⽅惩罚）、weighted_binary（对 FP / FN 不对
称惩罚）。
批次级（给 GEPA 当优化⽬标，回答“这个候选整体好不好”）：如 f1_score 做平衡优
化；precision_recall 做约束优化——精确率达标时直接返回召回率，未达标则乘以 (pr
ecision/target)² 惩罚，⽤来表达「精确率不低于 80% 的前提下最⼤化召回」这类
业务诉求。
evaluate.py 则按任务类型⾃动选指标体系：⼆分类⽤ Precision / Recall / F1 /
Accuracy；多分类叠加每类指标；评分任务⽤ MAE / RMSE / Spearman / Cohen's Kappa
（衡量与主观打分的⼀致性）；对⽐任务额外算位置偏差分数；聚类任务转成 pair-level 标签
后算 Pair P/R/F1 与兰德系数（ARI）等。
4.3.5 反馈引擎（ feedback.py ）
```

## PDF 第13页

[查看RAW.pdf第13页](RAW.pdf#page=13)

> 本页含0个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
反馈是驱动 GEPA 反思进化的燃料，采⽤双层设计：规则层⽤模板快速给出事实性反馈（正确
/ 解析失败 / 答错，各⾃附上模型输出与正确答案）；深度层只对错误样本调⽤ Judge 模型，
做三问归因：
1 你是 prompt 优化分析专家。分析以下 AI agent 的错误输出。
2 （输⼊：当前 System Prompt / 输⼊ / Agent 输出 / 正确答案，各⾃按上限截断）
3 ## 分析要求（200字以内）
4 1. 错误定位: agent 在哪个推理步骤出了问题？
5 2. Prompt 归因: 当前 prompt 的哪条规则导致或未能阻⽌这个错误？
6 3. 改进建议: prompt 应该如何调整？
关键在于第 2 问：它把“模型答错了”翻译成“prompt 的哪⼀条规则有问题”，让反思模型拿到
的是带归因的诊断⽽不是⼀堆错误样本，从⽽把盲⽬搜索变成定向改写。
4.3.6 扩展协议（ protocols.py ）
⽤ Python Protocol + ABC 基类为四个环节留出扩展位——数据准备（ DataPrepare
r ）、输出解析（ OutputParser ）、评分（ Scorer ）、反馈⽣成（ FeedbackGene
rator ）。遇到内置能⼒覆盖不了的场景，⽤户只需实现对应协议，在 config ⾥写上类路径
即可动态注⼊，不必改动引擎代码。
▐ 4.4 服务层：三种⽤法
同⼀套引擎对外提供三种⼊⼝：CLI（本地调试）、HTTP API（平台集成）、Claude Code
/ Qoder Skill（对话式使⽤）。
api.py 基于 FastAPI，围绕“任务”组织端点：提交、列表、查状态、看进度、取结果、取
消运⾏中的任务，另有⼀次性评估、配置校验、数据上传与健康检查。
jobs.py 的任务状态全部落在⽂件系统上，每个任务⼀个 runs/jobs/{job_id}/ ⽬
录，内含五个⽂件：
⽂件 内容
config.json 任务配置
job_state.json 运⾏状态（pending / running / completed / failed / cancelled）
progress.jsonl 实时进度事件
```

## PDF 第14页

[查看RAW.pdf第14页](RAW.pdf#page=14)

> 本页含1个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
best_prompt.txt 优化出的最优提示词
result.json 完整 GEPA 结果
状态外部化带来三个好处：任务可后台线程运⾏、可通过取消令牌中断、也可在运⾏中途或结
束后随时回查与追溯历史。
progress.py 把优化事件写成 JSONL 追加流，Skill 侧 tail ⼀下就能实时汇报进
度。
Skill 使⽤流程和提升效果
▐ 5.1 安装
1 # 1. 安装依赖
2 pip install -r requirements.txt -i xxx
3 # 2. 配置 API Key
4 export DASHSCOPE_API_KEY="your-key-here" # 或 OPENAI_API_KEY
▐ 5.2 执⾏⽰例
使⽤⽅式：Claude Code /qoder/codex等，直接对话，我想优化提示词，有标注数据，Skill
会引导你完成五步流程：
1. 收集信息 — 提供带标注的数据集 + ⼀句话任务⽬标
2. 分析数据 — Inspector ⾃动推断任务配置（任务类型、字段、模板）
3. 确认配置 — 调整评分⽅式和参数，确认数据切分⽐例
4. 执⾏优化 — 后台运⾏约 15-30 分钟，通过 JSONL 实时报告进度
5. 报告结果 — 展示得分提升、优化后提示词、与原始提示词的差异、后续建议
下⾯是输⼊部分和输出部分的示例，以某需求为例。
5.2.1 输⼊说明
GEPA 的输⼊分为两部分：需要准备的⽂件和交互式⽤户输⼊。⽤户需要准备的数据⾄少包括
raw/ ⽂件夹下的两个⽂件：数据集和提示词。模型解析后输出三类⽂件：jsonl 格式的数据集
```

## PDF 第15页

[查看RAW.pdf第15页](RAW.pdf#page=15)

> 本页含0个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
（data/），规范化后的提示词（prompts/）以及运⾏配置（config/）。
1. 带标注的数据集
数据集包含模型输⼊字段和正确答案。命名最好与提示词中的变量名对应。
数据集字段要求：
字 段 类
说明 示例
型
输 ⼊ 字
模型需要分析的⽂本/数值内容 title 、 content 等
段
答 案 字 answer 、 label 、 resul
正确标注（必须每条都有）
段 t 等
图 ⽚ 字
段 图⽚ URL，字段名含 image / img / url 时
imageUrl 、 skuImage 等
（ 可 ⾃动识别
选）
2. 初始提示词
初始提示词是优化的起点，也称为"种⼦提示词"。如果已有在⽤的 prompt，从它开始优化⽐
从零开始更快。如果没有提示词，GEPA 的 inspector 会根据数据集⾃动⽣成⼀个种⼦提示
词。
提示词需要包含两部分：
组成 组成 ⽂件示例
定义⻆⾊、规则、输出格式约 prompts/system_prompt.
system_prompt
束 txt
数据注⼊模板，⽤ {fieldN prompts/user_template.
user_template
ame} 占位 txt
3. 交互式⽤户输⼊
触发 Skill 后，系统会逐步收集以下信息：
```

## PDF 第16页

[查看RAW.pdf第16页](RAW.pdf#page=16)

> 本页含1个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
图6 和skill交互示意图
数据与任务
信息 说明 示例
JSONL/JSON/CSV ⽂ 件 路 tasks/my_task/data/dat
数据集路径
径
aset.jsonl
"判断两个商品 SKU 是否xxxx
任务⽬标 ⼀句话说明模型要做什么
x"
提示词与评判偏好
信息 说明 默认⾏为
已有的 system prompt ⽂件路 由 inspector ⾃动⽣成种⼦提
现有提示词
径 示词
误判和漏判哪个更严重，优化
评判偏好 使⽤ F1 平衡评分
准确率或者召回率
可选配置
信息 默认值 说明
```

## PDF 第17页

[查看RAW.pdf第17页](RAW.pdf#page=17)

> 本页含0个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
推理/反思模型：如 qwen3.6-f
模型名称 可替换为其他模型
lash
输⼊字段 inspector ⾃动检测 可⼿动指定使⽤哪些字段
是否包含图⽚ inspector ⾃动检测 ⽀持图⽂多模态
5.2.2 实际提升效果
优化完成后，GEPA 在 run_dir ⽬录下产出以下⽂件，示例：
1 runs/job_20260727_195205/
2 ├── best_prompt.txt # 最优提示词（纯⽂本）
3 ├── optimize_result.json # 完整优化结果（JSON）
4 ├── result.json # GEPA 引擎原始结果
5 ├── candidates.json # 所有候选提示词及评估详情
6 ├── candidate_tree.html # 候选树可视化（浏览器打开）
7 ├── progress.jsonl # 优化进度⽇志（JSONL，每⾏⼀个事件）
8 ├── run_log.txt # 运⾏⽇志（纯⽂本）
9 ├── run_log.json # 运⾏⽇志（JSON 格式）
10 ├── run_log_stderr.txt # 错误输出⽇志
11 ├── gepa_state.bin # GEPA 引擎状态⼆进制快照
12 └── generated_best_outputs_valset/ # 最优提示词在验证集上的逐条输出
13 ├── task_0/
14 │ └── iter_0_prog_0.json # 第 0 条数据的模型输出
15 ├── task_1/
16 │ └── iter_0_prog_0.json
17 └── ... # 每条验证集数据⼀个⽬录
并且在聊天框内输出简略报告结果：
```

## PDF 第18页

[查看RAW.pdf第18页](RAW.pdf#page=18)

> 本页含1个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
[本页未提取到文字；不据此判定原页为空白。]
```

## PDF 第19页

[查看RAW.pdf第19页](RAW.pdf#page=19)

> 本页含1个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
图7 优化完毕后模型会输出报告，包括验证集和测试集指标，后者⽤来反映泛化能⼒。模型还会输出提示词的主要优化
点，并提出后续建议。
▐ 5.3 评判偏好速查表
根据业务需求选择合适的评分策略举例：
分类任务：
⽤户表述 评分⽅式 参数
{"fp_penalty": 0.0, "f
"不要误判" / "准确率重要" 加权⼆分类
n_penalty": 0.5}
{"fp_penalty": 0.5, "f
"不要漏" / "召回率重要" 加权⼆分类
n_penalty": 0.0}
"F1 平衡" F1 分数 {}
"精确率到 80% 以上再说召 {"precision_target":
精确率-召回率
回" 0.8}
⽆特别偏好 精确匹配 {}
评分任务：
⽤户表述 评分⽅式 参数
"平均误差要⼩" 数值接近度 {"penalty": "linear"}
{"penalty": "quadrati
"⼤错不能犯" 数值接近度
c"}
对⽐任务：
⽤户表述 评分⽅式 参数
"准确率要⾼" 精确匹配 {}
"不能有位置偏差" 对⽐评估 {"check_bias": true}
聚类任务：
```

## PDF 第20页

[查看RAW.pdf第20页](RAW.pdf#page=20)

> 本页含1个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
⽤户表述 评分⽅式 参数
"⼀致性要⾼" Cohen's Kappa，ARI {}
{"focus": "precisio
"不能过度合并" 配对精确率
n"}
"不能漏合并" 配对召回率 {"focus": "recall"}
未来展望与思考
▐ 6.1 冻结区：不是所有内容都该被改
GEPA 默认将整段 prompt 交给反思模型重写，这意味着硬性约束、⼯具调⽤协议、输出
Schema 都处于可被改动的范围内。这带来⼀个反直觉的⻛险：有时候删掉⼀条约束往往能提
分。 约束的本质是限制⾏为空间，去掉它，模型就少犯⼀类"做多了"的错。若有⼈⼯标注兜
底，这类篡改尚能被发现；但在纯规则评分下，它本质上就是奖励⿊客（reward hacking）。
因此，正确的防御⽅式是从结构上禁⽌改动，⽽⾮事后靠扣分来补救。具体做法是将 prompt
划分为两个区域：
区 内容 参与变异
冻结区 硬性约束、⼯具调⽤协议、输出 Schema 否
可变区 判断优先级、决策倾向、异常处理、表达⽅式 是
GEPA ⽀持多 component 结构，让选择器只返回可变区，冻结段就不会进⼊反思上下⽂。
▐ 6.2 提⽰词膨胀：⽬标是"更准，且不更⻓"
反思模型有⼀种天然倾向：不断补充说明。⼗⼏轮迭代下来，prompt 从⼏百字膨胀到⼏千
字，⽽每⼀轮的分数都在涨，不会有任何信号提示你出了问题。真正的代价是隐性的：
关键约束被淹没：核⼼指令埋在冗⻓的补丁堆⾥，模型注意⼒被稀释；
推理成本线性上涨：token 数翻倍，延迟和费⽤同步翻倍；
⼈⽆法接管：prompt ⻓到读不懂，⼀旦需要⼈⼯回滚或调试，根本⽆从下⼿。
```

## PDF 第21页

[查看RAW.pdf第21页](RAW.pdf#page=21)

> 本页含2个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
抑制⼿段：可以把⻓度作为帕累托的第三个⽬标（⽽⾮加权惩罚，避免与主⽬标抵消），并设
硬上限⻔禁。
▐ 6.3 ⽆ Ground Truth 场景的prompt⾃进化
⼀开始我设想的GEPA定位是在judge align上，这部分对⻬标准靠⼈⼯标注。但真正值得优化
的往往是被评测 agent ⾃⼰的 prompt，难点在于部分agent做策略⽣成，没有正确答案，只
有事后的业务效果。我想到了两点：
变异⽅向：原⽣ GEPA ⾃由探索偏随机。接上离线评测指标/线上业务效果汇总的归因分析
作⽂本梯度，再补⼀层 prompt 结构缺陷诊断，把"业务上错在哪"翻译成"哪⼀段该改"，即
变为定向变异，⽅向更明确。
对错判据：⼀是⽤已有的离线评测指标当 judge，把候选跑出的结果算成分数，构造对抗
双⽬标（该做的没做 / 不该做的做了）；⼆是历史策略回溯预测，把候选决策溯源到历史
相似场景，对⽐同类最优历史的业务指标。回溯预测只⽤于排序与否决，不回流反思，否
则“改得越少 -> 匹配越多 -> 分越⾼”会把搜索拖向保守。
图8 双通道GEPA优化框架设想
参考⽂献
[1] AGRAWAL L A, TAN S, SOYLU D, 等. GEPA: Reflective Prompt Evolution Can
Outperform Reinforcement Learning[EB/OL]. arXiv:2507.19457,
2025. https://arxiv.org/abs/2507.19457.
[2] KHATTAB O, SINGHVI A, MAHESHWARI P, 等. DSPy: Compiling Declarative
Language Model Calls into Self-Improving Pipelines[EB/OL]. arXiv:2310.03714,
2023. https://arxiv.org/abs/2310.03714.
```

## PDF 第22页

[查看RAW.pdf第22页](RAW.pdf#page=22)

> 本页含2个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
团队介绍
本⽂作者诗咏，来⾃淘天集团-营销&交易技术团队。本团队承担淘天电商全链路交易技术攻
坚，致⼒于通过技术创新推动业务增⻓与⽤户体验升级。过去⼀年主导了多个⾼价值项⽬，包
括：⽀撑618、双11、春晚等亿级流量洪峰、构建业界领先的全⽹价格⼒体系、承接淘宝全⾯
接⼊微信⽀付、搭建集团最⼤的AI创新平台-ideaLAB，⽀撑淘宝秒杀等创新业务的⾼速增⻓。
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | ⾳视频技术
服务端技术 | 技术质量 | 数据算法
⼤淘宝技术
⼤淘宝技术官⽅账号
964篇原创内容
公众号
阅读 5893
留⾔
写留⾔
还没有留⾔，来写⾸评
```

## PDF 第23页

[查看RAW.pdf第23页](RAW.pdf#page=23)

> 本页含0个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
[本页未提取到文字；不据此判定原页为空白。]
```

