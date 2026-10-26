# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
Agent 开始“⾃我进化”：会出题、会反思，还会⾃⼰⻓出新技能
腾讯程序员 2026 年 7 ⽉ 27 ⽇ 02 : 27⼴东原创 腾讯技术⼯程 619 ⼈
作者： horacebao 、 ashexie
⼀个完全⾃主、越⽤越强的  Agent ，有可能实现吗？本⽂聚合了现有的前沿探索⼯作，向⼤家
展现这⼀⽅向上的最新成果。话不多说，现就开启学习之旅吧 —— 本次⽂章覆盖⾃进化  Agent
的三⼤技术路线、代表⼯作详解、横向对⽐、关键洞察等话题。
01 ⾃进化  Agent 介绍
1.1 什么是⾃进化  Agent ？
⾃进化  Agent（ Self-Evolving Agent ）指的是⼀类能够在与环境 / ⽤户交互过程中⾃动积累经
验、提炼能⼒、并在后续任务中复⽤与提升的智能体。简单来讲：让  Agent ⾃⼰越⽤越聪
明，⽽不是每次都靠⼈⼯去喂数据、调提⽰词、改模型。
它的核⼼诉求可以拆成三件事：
能存：把交互过程中沉淀下来的有价值的东西（成功模式、失败教训、可迁移技能）存下
来；
能⽤：在新任务中能把之前存下来的东西检索 / 调⽤ / 内化进⾃⼰的决策；
能进化：经验本⾝是动态的，能更新、能合并、能淘汰，避免越攒越乱。
1.2 为什么这件事现在被重视起来了？
回到⼤模型本⾝的⼏个⽼⼤难问题：
当  Agent ⾃⼰会出题、⾃⼰会答题、还能把答错的经验沉淀成下⼀次的 " 技能包 "—— ⼀
个永远在长⼤的  Agent ，到底能⾛多远？⼗⼏篇论⽂反复啃读，从 " 存技能 " 到 " 训技能 " ，
再到 " 零数据⾃训 " ，我们终于摸清了⾃进化  Agent 这条赛道的脉络。本⽂将带你深⼊
Agent 的 " 经验⼤脑 "—— 从把经验写进⽂件，到把经验训进权重，再到完全⽆⼈⼯数据的
⾃我循环，⼀步步拆解研究路径。
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
静态知识：训练完成那⼀刻起，模型对世界的认知就被冻结了；
上下⽂有限：再长的上下⽂窗⼝也总有边界，多轮交互终究 " 断⽚ " ；
重复犯错：今天教会它的事，明天还会再犯⼀遍；
训练贵：每次想让模型变强⼀点，要么  SFT 要么  RL ，都得重新跑⼀遍。
⽽⾃进化  Agent 想要的正是绕开这些限制：让经验本⾝成为模型能⼒的延伸或更新通道。这
件事在学术上不算新概念（早期的强化学习 + 经验回放就是雏形），但在⼤模型时代被重新点
燃，本质是因为：
LLM 本⾝具备总结归纳的能⼒（⾃⼰能给⾃⼰写笔记了）；
Agent 形态的产品越来越多，长程交互场景终于有了真实需求；
⾼质量⼈⼯标注数据越来越贵，社区开始探索 " 少⼈⼯  / ⽆⼈⼯ " 路线。
1.3 三⼤技术路线⼀览
我们把⽬前调研到的⼯作按 "是否更新模型权重"和 "是否依赖⼈⼯数据" 两个维度划成了三类：
路线 是否更新模型
权重
是否依赖⼈⼯
数据 代表⼯作
第⼀类：经验 /Skill
存储型 ❌  不更新 ❌  依赖 AutoSkill 、 EvoSkill 、 MemSkill 、 CoEvoS
kills 、 SE-Agent 、 Hermes
第⼆类： RL 训练
型 ✅  更新 ❌  依赖 EvolveR 、 SAGE 、 SkillRL 、 SKILL0 、 Skil
lOS 、 AgentEvolver
第三类： 0 数据⾃
学型 ✅  更新 ✅  不依赖 Agent0 、 Tool-R0 、 Absolute Zero
简单⼀句话来理解三类⼯作的差异：
第⼀类像是给  Agent 配了⼀本 " ⼯作笔记 " ，模型本⾝不动，只在需要时翻阅；
第⼆类则是直接把 " ⼯作笔记 " 上的经验通过  RL 写进模型的权重⾥，让  Agent 真正 " 长本
事 " ；
第三类更激进 —— ⼲脆连 " ⽼师 " 都不要了，让  Agent 之间互相出题互相考试，⾃⼰跟⾃⼰
打。
下⾯分别展开。
02 第⼀类：经验 /Skill 存储型（不更新模型权重）
特征：不训练、跨会话保留上下⽂、⽂件式存储；核⼼是把经验沉淀为可检索 / 可复⽤的 " 技能
（ Skill ） " 。
类⽐来看，这类⼯作就像是给  Agent 配了⼀个 " 外挂⼤脑 " ，本体（ base LLM ）保持冻结，所
有的 " 成长 " 都发⽣在外挂⾥。
2.1 AutoSkill （ arXiv: 2603.01145 ）
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
TLDR：基础款，动态增删改查  Skill 来防⽌  Skill 库爆棚。
整体设计是⼀个⾮常经典的双环结构：
左环 —— 在线服务（⽤  Skill ）
查询重写：把⽤户原始问题改写成更适合检索的形式
混合技能检索：语义相似度（ Embedding ） + 词汇相关性（ BM25 ）双管齐下
技能注⼊⽣成：把检索到的技能渲染为外部记忆上下⽂，注⼊到提⽰词⾥
右环 —— 技能进化循环（更新  Skill ）
技能提取：从⽤户交互信号中抽取可重⽤的技能候选
候选技能管理：判断该  Add （新增） / Merge （合并） / Discard （丢弃）
版本化合并：语义并集更新，保留技能⾝份并更新版本号
评估数据集是  WildChat-1M ，但没有具体性能指标—— 论⽂⾥只看了抽出来的  skill 数量。这
其实是这⼀类⼯作最⼤的痛点：评估缺位。
2.2 EvoSkill （ arXiv: 2603.02766 ）
TLDR：让多个  Agent 分⼯协作 —— ⼀个执⾏、⼀个反思、⼀个落地 —— 把 " 失败 " 变成 " 新
Skill" ，并⽤  Pareto 前沿机制保证  Skill 库永远精⽽不滥。
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
EvoSkill 来⾃  Sentient  和弗吉尼亚理⼯的合作⼯作，主张是把传统  Agent " 失败即重试 " 的
笨办法改造成  " 失败即学习 " 的进化闭环。它的最⼤特点是把  Skill 当作⼀等公民来升级，⽽不
是只在  prompt / code 层⾯做⽂字游戏。
三  Agent 分⼯：
Executor Agent （执⾏者）：拿当前  Skill 库去跑任务，把失败案例完整记录下来 —— 失败
原因、轨迹、最终错误结果⼀起留档。这是后⾯所有进化的 " 原材料 " 。
Proposer Agent （反思者）：扮演 " 诊断医⽣ " 的⾓⾊。它读完  Executor 的失败记录后，会
先做根因分析（为什么失败？是缺技能？还是技能⽤错了？），再基于过往的反馈历史决定
新建⼀条  Skill还是修改已有  Skill—— 例如在⾦融⽂档  QA 任务⾥它会⾃动总结出  "data
extraction validation" （数据抽取校验）这样的可复⽤技能。
SkillBuilder Agent （落地者）：把  Proposer 的⾃然语⾔提案变成结构化的  Skill ⽂件夹
（含元信息、操作步骤、辅助脚本），并在⼩样本验证集上跑⼀轮单元化校验。
核⼼机制 ——Pareto Frontier 精英池：
新⽣成的  Skill 不是⽆脑⼊库，⽽是要跟已有  Skill 在多维指标上⽐较，只有在⾄少⼀个维度上
严格优于现有  Skill 的才会进⼊精英池，否则丢弃或合并。这套机制保证了  Skill 库随着规模增
长依然保持 " 精⽽不滥 "—— 这也是它跟  AutoSkill  那种 " 全量保留  + 版本化 " 做法最⼤的不
同。
评估亮点：
OﬃceQA 主任务：基于美国财政部公告（ 89K 页扫描财务⽂档）的复杂数值推理任务。
基线准确率  60.6% →  进化后  67.9% （ +7.3pp ），主要靠两条⾃学到的  Skill 撑场：
Data extraction validation —— 解决了之前表格解析时常见的 " 单元格错位 " 问题；
Quantitative analysis with checkpoints —— 在⾦融数值计算环节强制加⼊校验点。
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
跨任务迁移：在  SealQA 上学到的  search persistence protocol（搜索坚持协议）直接挪
到  BrowseComp 任务上，⽆需重新训练就带来  +5.3pp 的提升 —— 这点跟后⾯
CoEvoSkills 的 "transfer 不如⾃⼰  self-evo" 结论形成有趣对⽐，说明只要  Skill 抽象得⾜
够通⽤，是可以跨任务迁移的，但前提是抽象层级要选对。
2.3 MemSkill （ arXiv: 2602.02474 ）
TLDR：之前两个⼯作针对⽤户指令；MemSkill  只针对操作  Memory 的  Skill  做⾃进化。
这个⼯作有意思的地⽅在于它把组件拆得很细：
Retriever：基于  Qwen0.6B Emb 的相似度计算
Controller： MLP 结构，接受  RL 训练（注意这是这⼀类⾥少见的 " 有训练 " 环节）
Executor Designer Base LLM：全部冻住
它有两个并⾏的更新  Loop ：
Controller 更新： Retriever 抽取  Memory + 对话  →  Controller 选  Skill →  Executor 更新
Memory 库  →  ⽤下游  F1 / Success Rate 作为  reward 训练  Controller
Skill 库更新：训练中遇到的  Hard Case 交给  Designer 更新  Skill 库
亮点——Transfer Evaluation ：
在  LLaMA 上训练所得  Controller & Skill 迁移到  Qwen 上仍然有效；
在  LoCoMo 上训练所得  Controller & Skill 迁移到  LongMemEval 上仍然有效。
PS ：虽然叫 " 训练集 " ，但训练集只⽤来总结，不更新任何模型。评论：在第⼀类⼯作
⾥， EvoSkill 是 " ⼯程化程度 " 的中间档 —— ⽐  AutoSkill 多了精英池筛选机制，但⽐
Hermes 那种带  GEPA 反向进化的还差⼀截。它的真正价值在于把 " 失败 " 明确写进了进化
闭环，这也成了后续很多⼯作（包括  SkillRL 的  failure trajectory distillation ）的直接灵感
来源。
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
由于  Base LLM 不动，仍归为 " ⽆训练 " 类。但  MemSkill 给前⾯两篇⼯作（ AutoSkill / Hermes
Agent 没有性能评估）提供了⼀条参考思路：在训练集上构建  Skill ，在测试集 / 其他数据集的
测试集上评估。当然，这种做法下 " 喂给  Agent 的样本顺序 " 就变得很重要。
2.4 CoEvoSkills （ arXiv: 2604.01687v2 ）
TLDR：给每条新总结的  Skill 配⼀个 " 考官 " （ Veriﬁer ），⽣成的  Skill 必须先通过考试才能进
库；通不过就带反馈打回，让  Generator 重写 —— 这是把软件⼯程的 " 单元测试 " 理念搬到了
Skill 进化⾥。
CoEvoSkills 想解决的是前⾯⼏篇⼯作的⼀个⽼⼤难问题：Skill 总结出来到底靠不靠
谱？ AutoSkill / EvoSkill 都是 " ⽣成完了直接⼊库 " ，质量基本靠  LLM ⾃觉。 CoEvoSkills 的回
答是：不能靠⾃觉，得有验证闭环。
核⼼组件 ——Generator + Veriﬁer 双⼦星：
Skill Generator：从执⾏轨迹⾥提炼候选  Skill 。除了写出  Skill 本⾝（描述  + 步骤），还要
同步⽣成对应的单元测试（输⼊样例、期望输出、验证逻辑）。
Skill Surrogate Veriﬁer：在⼀个隔离的  sandbox 环境⾥跑  Generator 写的  Skill 与单元
测试，返回结构化验证反馈（不是简单的  pass/fail ，⽽是带 " 失败原因 " 和 " 建议修改⽅
向 " 的⾃然语⾔反馈）。
Co-Evolution Iteration （共进化迭代）： Skill 与  Test 同时进化—— 这跟传统软件开发
⾥ " 先写测试再写代码 " 的  TDD  有点像。如果  Skill 多次都过不了  Test ，可能是  Test 本⾝
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
写得不合理；反过来如果  Test 太宽松导致烂  Skill 也进库了，下游评估时就会暴露出来。
两者互相牵制，逐步收敛到 " ⾼质量  Skill + ⾼严谨度  Test" 的稳态。
两阶段验证：
1. Surrogate 验证（廉价）：内置的  Veriﬁer 直接给反馈，跑得快、能快速迭代；
2. Oracle 验证（昂贵但权威）：通过  Surrogate 的  Skill 还要在真实  LLM Agent （论⽂中⽤了
Claude Code / CodeX 等）上跑端到端任务， ** 只有真的解决了任务才算 " 进化成功 "** 。如
果  Oracle 测试失败，整条  Skill 直接打回。
亮点结论 ——Self-evo 优于  Cross-model Transfer：
论⽂做了⼀组很有意思的对照实验：把强模型（ Opus 4.6 ） self-evo 出来的  Skill 直接  transfer
到弱模型（ Haiku 4.5 、 Qwen3-Coder 、 DeepSeek V3 、 Mistral Large 3 ）上，跟让弱模型⾃
⼰  self-evo ⽐较 —— 结果是：
self-evo （强模型⾃⼰⽤⾃⼰的  Skill ）： Opus 4.6 从  30.6% →  71.1% （ +40.5 ）， GPT-5.2
从  29.6% →  69.8% （ +40.2 ）；
cross-model transfer：把  Opus 4.6 的  Skill 给到弱模型，提升从  +35.4 到  +44.1 不等，
但绝对值都明显低于让模型⾃⼰  self-evo（如  Mistral Large 3 才到  43.1% ）。
这个观察的含义是：Skill 跟模型本⾝的 " 风格 " 是耦合的—— 强模型⽣成的  Skill 在强模型⾃⼰
上效果最好；强迁到弱模型上，弱模型未必能完整地 " 读懂并执⾏ " 那些精巧的步骤。这点对⼯
程界的启⽰很⼤：与其花⼤钱让  GPT-5 / Claude 4.6 给你的产品蒸馏  Skill ，不如让产品⾃⼰
⽤的⼩模型来  self-evo—— 前者贵且效果未必更好。
2.5 SE-Agent （ arXiv: 2508.02085 ）
PS ：虽然有 " 信号 " ，但实际上不涉及训练，仅仅是驳回  Generator 创建的  Skill 。评论：
CoEvoSkills 的 " 测试驱动  Skill 进化 " 思路在第⼀类⾥独树⼀帜，本质上是把  Veriﬁer 当成
" 便宜的  reward model" ⽤ —— 这跟第⼆类⼯作⾥训练  Curator 的逻辑已经很接近了，只
差最后⼀步：把  Veriﬁer 也训起来。
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
TLDR：与其反复 " ⾃我反思 " 在同⼀条轨迹上⼩修⼩补，不如⼀次跑出多条轨迹，让它们之间
互相借鉴、互相打磨——SE-Agent 把  Agent ⾃进化从 " 单线程深度修补 " 切到了 " 多线程横向融
合 " 。
SE-Agent 来⾃  OPPO 的  OpenSearch-AGI 团队和复旦⼤学等机构，被收录于  NeurIPS
2025 。它瞄准的是前⾯所有  self-reﬁne / ReAct 类⼯作的共同短板 ——单轨迹反思的视野太
窄。当⼀条轨迹整体⾛偏的时候（例如⼀开始就选错了策略），⽆论怎么  reﬂection 都救不回
来；只有跳出当前轨迹，从多条不同策略的轨迹⾥学习，才能突破 " 局部最优 " 。
完整五阶段流程：
1. 多策略轨迹⽣成（ Multi-Strategy Generation ）：⽤不同的 " 性格 " 采样  N 条轨迹。论⽂⾥
给了  5 种典型策略 ——P-greedy（贪⼼快出）、P-tests-first（先写测试）、P-linter-aware
（关注代码风格）、P-defensive（防御式编程）、P-minimal（最⼩可⾏）。同⼀道题，每
种策略得到的轨迹完全不同，犯的错也不同。
2. 反思修订（ Revision ）：对每条轨迹独⽴做⼀遍传统  self-reﬁne—— 找到执⾏偏差点，针对
性修正。这⼀步是 " 纵向 " 的（深耕单条轨迹）。
3. 质量过滤（ Quality-based Filtering ）：⽤⼀个综合评分函数   Reward(t,T) = α·TaskCompleti
on(t) + β·ReasoningQuality(t) + γ·Efficiency(t)  给每条轨迹打分，把候选数从  10 条砍到  5
条。这避免了下⼀步重组时被低质量轨迹 " 污染 " 。
4. 跨轨迹重组（ Recombination ） ⭐ 核⼼创新：这⼀步是  SE-Agent 区别于所有  self-reﬁne
⼯作的关键。它对剩下的  5 条⾼分轨迹做两类操作：
Crossover （交叉）：把 " 轨迹  A 在步骤  5 的精确定位 " 嫁接到 " 轨迹  B 的全⾯测试覆
盖 " 上，合成出⼀条原本任何单条策略都达不到的混合轨迹；
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
Transfer （迁移）：把 " 防御式策略⾥学到的  try-except 异常处理 " 迁移到 " 贪⼼策略⾥缺
失异常处理 " 的位置；
Restructure （重构）：识别多条轨迹共有的全局模式（如 " 所有轨迹都漏掉了  type-
safe ⽐较 " ），统⼀抽象后做⼀次系统级重写。
5. 最终⽅案选取（ Final Solution Selection ）：从  10 个候选（ 5 原始  + 5 重组）中选最⾼分
的作为输出。整个流程可以迭代多轮（论⽂⾥给的  N=4 时已经收敛），每⼀轮的结果会再
喂给下⼀轮做新的多策略⽣成。
关键观察 —— 横向  vs 纵向：
它定义了三种轨迹层操作（与单条轨迹的  self-reﬁne 形成对照）：
修订（纵向）：找出错误步骤并纠正 —— 这是传统  self-reﬁne 在做的事；
重组（横向）：跨轨迹借⽤成功的⼦⽚段 —— 这是  SE-Agent 的真正创新；
精炼（横纵融合）：在重组后的轨迹上再做⼀轮纵向打磨。
跟其他⼯作的关键区别是总结的⽅向不同：其他第⼀类⼯作⼏乎全是纵向总结（基于单条历史
轨迹 / 对话）， SE-Agent 是横向总结（基于多次采样的多条轨迹）。这个 " 横向  vs 纵向 " 的概念
会贯穿全⽂ —— 它是后⾯我们讨论 " 研究空⽩ " 时的⼀个重要锚点。
评估：
主战场是  SWE-Bench Veriﬁed（ GitHub 真实代码修复任务）。 SE-Agent 让多个底层
LLM 都拿到了显著提升，最⾼⼀档实现了  +55% 相对改善—— 在这个领域属于很扎实的
提升。
跟  Claude Code 等⼯业级  Coding Agent 也做了对⽐，验证了 " 轨迹级进化 " 是⼀个与底层
模型选择正交的优化维度。
2.6 第⼀类总结：还是要训练数据的
写到这⾥，其实第⼀类⼯作有⼏个统⼀的特征值得提⼀下：
核⼼点  1. 看似不训练，其实仍要训练数据
不管是⼈为交互提供反馈，还是训练集提供反馈，本质都是训练数据，没有真的做到 " 零数
据 " 。
核⼼点  2. 核⼼是 " 存下经验 /Skill"
这⼀类⼯作的灵魂在于把交互的副产物沉淀下来，做成可检索的资产。
评论： SE-Agent 是第⼀类⾥思路最 " 野 " 的 —— 它没有  Skill 库这种长期记忆机制，但
⽤ " ⼀次性多采样  + 跨轨迹融合 " 的办法做到了类似的效果。某种意义上它跟第⼆类的
SAGE （ Sequential Rollout ）是镜像关系： SE-Agent 是横向采， SAGE 是横向⽤；前者
不训模型，后者⽤  RL 让模型学会⾃⼰横向沉淀。
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
核⼼点  3. 总结这⼀步，被严重低估
⼏乎所有⼯作都默契地把  Skill 总结这⼀步交给了 " 冻结的  base 或独⽴的  LLM"—— 按理说这
是整条  pipeline 最关键的环节，但针对总结去优化的⼯作⼏乎没有。这是⼀个值得深挖的空
⽩。
核⼼点  4. 横向  vs 纵向总结
纵向总结（其他⼯作）：根据历史对话 / 单条轨迹总结；
横向总结（ SE-Agent ）：根据多次采样的多条轨迹总结。
⼆者都是 " 存  skill" 的不同侧⾯。
03 第⼆类：基于  RL 的训练型⾃进化（这是重点）
特征：通过  RL 训练直接更新模型权重，让模型从根本上变强。这⼀类是当前学术界与⼯业界
的主流⽅向，本报告的重点也在这⾥。
3.1 EvolveR （ arXiv: 2510.16079 ）
TLDR：算是这⼀类的基础型，分两阶段。
离线阶段： Agent 跑完⼀批任务后，对所有轨迹做提炼，把具体的交互步骤抽象成更通⽤
的 " 策略原则 " ，存⼊原则库（策略原则可以视作⼀种  Skill ）。
在线阶段： Agent 在新任务⾥实时检索这些原则，指导⾃⼰的⾏动，同时⼜产⽣新轨迹反
哺下⼀轮蒸馏训练。
Reward 设计：最终结果  + 格式  reward 评估： Natural Questions 、 HotpotQA 、 TriviaQA 、
PopQA
3.2 SAGE （ arXiv: 2512.17102 ）
PS ：看起来很像 "RL by talking" ，但是仍然要靠标注数据集  Ground Truth 去训练的。也
就是  talking 的数据只⽤来蒸馏经验 /skill ，不⽤来当训练标签。
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
TLDR：提出  Sequential Rollout —— RL rollout 时序列化地跑⼀系列相似任务，后序任务训
练时就可以使⽤前序⽣成的  skill 。
这个思路很巧妙：每次  rollout 不是跑⼀个任务，⽽是让  Agent 依次跑⼀串相似的任务。跑早
期任务时积累下来的技能，在同⼀个  rollout ⾥的后续任务⾥就能直接⽤。这意味着在训练过
程中， ** 模型就被迫学会 " ⽣成技能 " 和 " 复⽤技能 "** ，不只是会完成任务。
除了任务完成的结果奖励， SAGE 还设计了  Skill-integrated Reward—— 额外的信号专门激
励技能的⽣成和调⽤。评估数据集是  AppWorld （ APP 交互数据集）。
3.3 SkillRL （ arXiv: 2602.08234 ） ⭐
来到本⽂重点关注的四篇⼯作之⼀。
核⼼主张：⽤强模型（ o3 ）蒸馏  Skill ，再通过  RL 训练弱模型学会使⽤，并递归进化技能库。
统⼀三⾓⾊梳理：
⾓⾊ 配置
训练题⽬来
源
官⽅数据集训练集： ALFWorld （ 7,500 条  SFT ）、 WebShop （ 2,400 条  SFT ）、 7 个搜
索  QA 数据集
出题者 ⽆独⽴出题者，直接使⽤数据集
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
⾓⾊ 配置
解题者 Qwen2.5-7B-Instruct ✅  训练
（ Cold-start SFT →  GRPO RL ）
Skill 总结者 OpenAI o3 ❌  不训练
Skill 总结机制：
成功轨迹  →  提取关键决策点与可迁移模式
失败轨迹  →  合成失败教训（失败点  + 错误推理  + 应对策略）
压缩⽐： 10–20×
总体流程：解题者交互  →  轨迹交给总结者总结  skill →  下⼀轮训练时使⽤。
主要实验结果：
基准 SkillRL GRPO 基线 提升
ALFWorld 89.9% 77.6% +12.3%
WebShop SR 72.7% 66.1% +6.6%
Search-QA avg 47.1% ~38.5% +8.6%
Skill 库增长： 55 →  100 条（通⽤  12 → 20 ，任务专属  43 → 80 ）。
核⼼设计哲学：强模型提炼知识，弱模型通过  RL 学会使⽤知识。
3.4 SKILL0 （ arXiv: 2604.02268 ） ⭐
核⼼主张：将  Skill 从推理时的 " 外挂上下⽂ " 内化到模型参数，实现零样本执⾏（每步  < 0.5K
tokens ）。
⾓⾊ 配置
训练题⽬来源直接继承  SkillRL 的  SkillBank （ ALFWorld WebShop Search-QA 官⽅训练集）
出题者 ⽆
解题者 Qwen2.5-VL-3B/7B-Instruct ✅  训练
（三阶段渐进课程）
评论：我们倾向于把这种归类于蒸馏，⽽⾮真正的进化。
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
⾓⾊ 配置
Skill 总结者 继承  SkillRL 的  o3 ， ❌  不训练
三阶段渐进课程：
阶段 Skill 数量 ⽬标
Stage 1 6 条 学会调⽤
Stage 2 3 条 减少依赖
Stage 3 0 条 完全内化
核⼼设计哲学：从 " 使⽤技能 " 到 " 内化技能 " 的范式转变  —— 消除推理时的检索成本、 Token
开销和噪声，把知识真正固化进模型权重。
> SKILL0 不关⼼  Skill 从哪⾥来，只关⼼如何内化。它本质上是  SkillRL 的 " 下游消费者 " 。
3.5 SkillOS （ arXiv: 2605.06614 ） ⭐⭐
这是四篇⾥我们认为最有启发性的⼀篇。
核⼼主张：训练⼀个专门的  Curator，通过  RL 学会如何增  改  删  SkillRepo，⽽不是直接学
如何使⽤  Skill 。
⾓⾊ 配置
训练题⽬来
源
Agentic （ ALFWorld 、 WebShop 官⽅训练集） + 推理（ DeepMath-103k 随机采样  33,00
0 条）；两步预处理： Gemini-2.5-Pro 标注属性标签  →  按相似度分组（ group_size=8 ）
出题者 Gemini-2.5-Pro ❌  不训练
，仅离线标注每个任务的技能相关属性
解题者
Executor ❌  冻结，不训练
；训练时⽤  Qwen3-8B ；测试时⽤  Qwen3-8B 32B Gemini-2.5-Pro / Gemini-3.1-Flash-
Lite ； ReAct （ Agentic 任务） + CoT （推理任务）
Skill 总结
者 Qwen3-8B Curator ✅  GRPO RL 训练
核⼼设计哲学： " 学会如何管理技能，⽽不是学会如何使⽤技能 " —— Executor 冻结，只训练
Curator ，通过长周期间接奖励信号学习  Skill 的增删改策略。
这篇⼯作给出了两个对后续研究极其重要的结论：
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
3.6 AgentEvolver （ arXiv: 2511.10395 ） ⭐
核⼼主张：完全⾃主的三环⾃演化框架  —— ⾃出题、⾃解题、⾃总结经验，全链路⽆需⼈⼯
标注。
结论  1 ：训练过的⼩模型总结者  > 冻结的⼤模型总结者在  SkillOS 的实验⾥， RL 训练过
的  Qwen3-8B 作为  Curator ，效果超过直接⽤冻结的  Gemini-2.5-Pro 作为  Curator 。这
说明 " 如何管理  skill" 本⾝是⼀项可被训练的能⼒，⽽且⼩模型经过专门训练后能压过⼤模
型直接使⽤。
结论  2 ：不动解题者，性能也能涨在  ALFWorld 上，仅训练  Curator 、解题者完全冻结的
情况下，整体性能仍能取得长⾜进步。这意味着 " 换  Curator" 是⼀条⽐ " 换  Executor" 更轻
量的优化路径。
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
⾓⾊ 配置
训练题⽬来源 环境探索⽣成（ Self-Questioning ）
，全⾃动
出题者 LLM ⾃⾝（与解题者同⼀模型）
  ✅
解题者 Qwen2.5-7B/14B-Instruct ✅  训练
Experience 总结
者
Experience Manager ❌  不训练
（论⽂中没明说是什么模型，扒代码发现是调  Qwen-MAX API ；本质上是阿⾥  Re
me 记忆管理机制）
Self-Questioning 四步流程：
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
1. 探索：⾼温  LLM ⼴度优先（ N_b 步） + 深度优先探索环境
2. 合成：从探索轨迹蒸馏  + ⽤户偏好约束  →  ⽣成任务  g 与参考解
3. 筛选：词法去重  + 语义相似度  + 可⾏性验证
4. 混合（可选）：
特点：出题与解题使⽤同⼀个  Qwen2.5-7B/14B ， RL 训练后形成出题质量与解题能⼒的双重
提升。
3.7 第⼆类总结
第⼆类⼯作⾛得⽐第⼀类更远 —— 把经验从 " 外挂 " 变成了 " 权重 " 。但仔细看仍能拎出⼏条共
性：
核⼼点  1. 仍然依赖训练集反馈（除  AgentEvolver 外）  核⼼点  2. 核⼼是  RL rollout 时继承 /
更新之前的  skill核⼼点  3. 不算严格意义的 "RL by talking" —— 因为反馈仍来⾃任务结果或
⼈⼯标签，⽽不是交互对话本⾝
04 第三类： 0 数据⾃学型
特征：完全不要⼈⼯标注的数据，靠  Agent 之间互相出题 / 解题闭环。
这⼀类的精神更激进：连数据集都不要， Agent ⾃⼰出题⾃⼰考⾃⼰。
4.1 Agent0 （ arXiv: 2511.16043 ）
TLDR：学习⼯具使⽤，⼀个  Agent 负责出题，⼀个  Agent 负责解题。
组件：
Curriculum Agent (RL) ：负责出题； reward = 答题  Agent 的不确定性  + ⼯具使⽤频率
Executor Agent (RL) ：负责解题； reward = 解题成功率
流程：
1. 出题  Agent 先  RL 训练（答题  Agent 冻住作为  reward model ）；
````

## PDF 第 17 页

[原页](RAW.pdf#page=17)

````text
2. 出题  Agent 冻住，给答题  Agent 出题做  RL 训练。
评估集：数学类为主（ GSM8K 、 AIME 等）。
4.2 Tool-R0 （ arXiv: 2602.21320 ）
TLDR：类似  Agent0 ，但做的是  general tool ⽽不是纯数学。
Reward 设计：
Generator Agent ：格式  reward + 合法性  reward （不能有幻觉  tool ） + 难度  reward （不能
太难太简单）
Solver Agent ：格式  reward + 准确性  reward
评估集： ToolAlpaca 、 SealTool 、 NexusRaven 。
4.3 Absolute Zero （ arXiv: 2505.03335 ）
TLDR：单个模型同时扮演出题⼈和解题⼈，⽤代码执⾏器作为唯⼀的验证来源，完全不碰任
何外部数据。
PS ：在解题成功率  reward 上有⼀个⽐较⼤的问题 —— 题⽬的答案是  Curriculum Agent
⾃⼰多采样投票选出来的  sliver answer 。
PS ：答案仍然是  Generator Agent ⾃⼰⽣成的  sliver answer 。
````

## PDF 第 18 页

[原页](RAW.pdf#page=18)

````text
组件：
出题  Agent ： reward = 1 − 答题  Agent 成功率；但成功率为  0 时  reward 也为  0 （避免出
太难的题）
答题  Agent ： reward = 解题成功率
出题流程：题⽬为  [ 输⼊ , 代码 , 输出 ] 三元组，随机删除⼀个让答题  Agent 猜测，以代码执⾏
器为最终判断标准。这是⼀个⾮常聪明的设计 —— 它把 " 判分 " 这件事完全外包给了⼀个绝对客
观的执⾏环境。
评估集：
代码： HumanEval 、 MBPP 、 LCB
数学： AIME24 、 AIME25 、 AMC 、 MATH-500 、 Minerva 、 Olympiad
4.4 第三类总结：真 · 不需要训练数据
通⽤流程：
出题  Agent 训练  → 出题构造数据集  → 解题  Agent 训练  → 出题  Agent 训练  …
核⼼点  1. 全靠出题的  Agent ⾃⼰
核⼼点  2. 准确率判断⼤多靠对照出题  Agent ⾃⼰给出的答案—— 这是个隐患， sliver answer
的可靠性需要打问号
核⼼点  3. 最好要有⾃动化的判断标准—— ⽐如  Absolute Zero ⽤的代码执⾏器
核⼼点  4. 出题难度很重要—— 太难学不懂，太简单学不到，这个  reward shaping 是核⼼难点
核⼼点  5. 评估很混乱—— 只有数学类的  benchmark 勉强出现了多次，其余⼏乎完全没有重
叠，可⽐性差
05 横向对⽐：四篇代表⼯作的 " 三⾓⾊ " 视⾓
第⼆类⾥  SkillRL →  SKILL0 →  SkillOS →  AgentEvolver 这四篇我们想专门拎出来横向对⽐，
因为它们最能反映长程  Agent ⾃进化的范式演进。
5.1 核⼼对⽐表
````

## PDF 第 19 页

[原页](RAW.pdf#page=19)

````text
论⽂ 训练题⽬来
源 出题者 解题者（训
练？）
Skill/Experience 总
结者（训练？）
SkillRL 官⽅数据集训
练集 — Qwen2.5-7B ✅
训练 OpenAI o3 ❌
SKILL0 官⽅数据集训
练集 — Qwen2.5-VL-3B/
7B ✅  训练 OpenAI o3 （继承） ❌
SkillOS 官⽅数据集训
练集
Gemini-2.5-Pro （仅
离线分组， ❌ ） Executor 冻结  ❌ Qwen3-8B Curator ✅
AgentEvolv
er 完全⾃动⽣成LLM ⾃⾝（与解题者
同⼀模型）
Qwen2.5-7B/14B
✅ Qwen-MAX API ❌
5.2 ⼀⾏式速记
SkillRL ：        [ 训练集 ❌ ] [ 解题者  ✅ ] [ 总结者  ❌ ]
SKILL0 ：         [ 训练集 ❌ ] [ 解题者  ✅ ] [ 总结者  ❌ ]
SkillOS ：        [ 训练集 ❌ ] [ 解题者  ❌ ] [ 总结者  ✅ ]   ←  唯⼀训练总结者的⼯作
AgentEvolver ：   [ 出题者 ✅ ] [ 解题者  ✅ ] [ 总结者  ❌ ]
5.3 强模型依赖程度
⽅法 依赖的强模型 ⽤途
SkillRL OpenAI o3 Skill 总结（核⼼）
SKILL0 OpenAI o3 （继承） Skill 总结（核⼼）
SkillOS Gemini-2.5-Pro （辅助） + Qwen3-32B （ Judge ） 标注分组  + 质量评估
AgentEvolver Qwen-MAX Experience 提取  + 总结
可以看到：总结这⼀步，⼏乎所有⼈都默契地外包给了⼤模型  / 闭源  API，这跟我们前⾯在第
⼀类总结⾥观察到的现象⾼度吻合。
5.4 数据依赖程度
⾼依赖外部数据  ← ─────────────────────────────────────────→ 完全⾃主
       │                                                      │
   SkillRL              SKILL0           SkillOS         AgentEvolver
（官⽅数据集）          （复⽤  SkillRL ）    （官⽅ + 分组）      （完全⾃⽣成）
5.5 范式演进脉络
SkillRL (2602.08234)
  强模型提炼知识  → 弱模型  RL 学会使⽤  → 递归演化技能库
       ↓
SKILL0 (2604.02268)
````

## PDF 第 20 页

[原页](RAW.pdf#page=20)

````text
  同样的技能库  → 渐进撤回  → 内化进参数  → 零样本执⾏（⽆检索开销）
       ↓
SkillOS (2605.06614)
  冻结执⾏者  → 训练  Curator → 学会如何管理技能（增 / 改 / 删）
       ↓
AgentEvolver (2511.10395)
  全链路⾃主  → ⾃出题  + ⾃解题  + ⾃总结  → 步骤级信⽤分配
06 关键洞察：被忽视的 " 总结者 "
6.1 总结者，是被严重低估的关键模块
把⼀三两类  + 四篇代表⼯作的 " 是否训练总结者 " 列在⼀起：
⼯作 Skill 总结者是否训练
AutoSkill ❌
EvoSkill ❌ （ Claude Code w/ Opus 4.5 ）
MemSkill ❌
CoEvoSkills ❌ （ Claude Code ）
SE-Agent ❌
EvolveR ❌ （ Qwen2.5 ）
SAGE ✅ （序列  rollout 中带  reward 总结）
SkillRL ❌ （ OpenAI o3 ）
SKILL0 ❌ （继承）
SkillOS ✅ （唯⼀专门训练）
AgentEvolver ❌ （ Qwen-MAX API ）
可以看到，针对总结者本⾝做训练的⼯作屈指可数——SAGE 算半个（在  RL 过程中有  skill
reward ）， SkillOS 才是真正完整地把  Curator 当成主训练对象。
⽽  SkillOS 给出的实验结论 ——训练后的  8B Curator 优于冻结的  Gemini-2.5-Pro Curator
—— 恰好印证了这件事的价值。
6.2 ⾃主性  × 总结质量的⼆维空间
把四篇代表性⼯作放到两个维度上看：
        总结者训练
            ▲
   SkillOS │
           │
           │
  ─────────┼────────── ►  题⽬⾃动⽣成
           │
````

## PDF 第 21 页

[原页](RAW.pdf#page=21)

````text
SkillRL/   │ AgentEvolver
SKILL0     │
右上⽅那个空⽩象限—— 既⾃动⽣成题⽬、⼜训练总结者 —— ⽬前没有⼀篇⼯作覆盖。这是当
前最显眼的研究空⽩。
6.3 横向  vs 纵向总结的融合空间
第⼀类⼯作⾥的  SE-Agent 是横向（多次采样）总结，其他都是纵向（历史对话）总结。这两
者在第⼆类⼯作⾥基本没有融合 ——SkillRL/SKILL0/SkillOS 仍以纵向为主。横向  + 纵向的融
合会不会带来更稳健的  Skill 库？是⼀个开放问题。
07 写在最后
这⼀年多⾃进化  Agent 的研究节奏其实⾮常快，从 " 存技能 " 到 " 训技能 " 、从 " 依赖⼈⼯数
据 " 到 " 零数据⾃训 " ，⼏乎每个⽉都能看到新⼯作冒出来。但仔细啃完之后会发现，还有⼤⽚
研究空⽩没⼈去碰—— 尤其是 " 总结者本⾝的训练 " 和 " 完全⾃主  + 训总结者 " 这条交叉路径。
回过头看，这条赛道的本质问题其实只有⼀个：
⽆论是把经验存进⽂件、训进权重，还是让  Agent 之间互相出题，所有路径都在回答这⼀个
问题的不同侧⾯。
附录  A ：论⽂索引
简称 arXiv 类别
AutoSkill 2603.01145 第⼀类
EvoSkill 2603.02766 第⼀类
MemSkill 2602.02474 第⼀类
CoEvoSkills 2604.01687v2 第⼀类
SE-Agent 2508.02085 第⼀类
EvolveR 2510.16079 第⼆类
SAGE 2512.17102 第⼆类
SkillRL 2602.08234 第⼆类
SKILL0 2604.02268 第⼆类
SkillOS 2605.06614 第⼆类
AgentEvolver 2511.10395 第⼆类
Agent0 2511.16043 第三类
Tool-R0 2602.21320 第三类
如何让  Agent 在没有⼈⼯⼲预的情况下，把交互的副产物转化为下⼀次更强的能⼒？
````

## PDF 第 22 页

[原页](RAW.pdf#page=22)

````text
简称 arXiv 类别
Absolute Zero 2505.03335 第三类
附录  B ：评估数据集索引
数据集 使⽤⼯作 类型
WildChat-1M AutoSkill ⽤户对话
OﬃceQA EvoSkill 办公图表
LoCoMo / LongMemEval MemSkill 长程对话记忆
SkillBench CoEvoSkills 技能
ALFWorld SkillRL SKILL0 SkillOS 具⾝ /Agentic
WebShop SkillRL SKILL0 SkillOS ⽹页购物
Search-QA SkillRL / SKILL0 检索问答
AppWorld SAGE APP 交互
NQ HotpotQA TriviaQA / PopQA EvolveR 检索问答
DeepMath-103k SkillOS 数学推理
GSM8K / AIME Agent0 数学
ToolAlpaca SealTool NexusRaven Tool-R0 ⼯具使⽤
HumanEval MBPP LCB Absolute Zero 代码
腾讯 PCG ⼤数据平台部
⭐⭐  新⼀代全链路数据 AI 助⼿ ——Dola ⭐⭐
Dola 是⼀款基于 Agentic AI 能⼒开发的全链路数据助⼿：⽤户只需要引⼊个⼈的数据表，就能
得到⼀枚专属的 AI 分析师
它不仅能够完成⽇常的取数、跑数等基础任务，还能⾃主规划并执⾏复杂场景的数据分析，例
如异动归因、画像对⽐分析、股票基⾦回测、房价预测等。 Dola 可以⾃⾏编写 SQL 、纠正 SQL
错误、执⾏查询、使⽤ Python 进⾏数据处理与可视化，并最终⽣成⼀份完整的分析报告。全
程⽆需编写⼀⾏代码，只需通过⾃然语⾔对话，你就能拥有⼀个全⾃动⼯作的 “ 数据⼩⿊⼯ ” 。
这⾥以 1 个股票回测的例⼦看看 dola 的效果：
````

## PDF 第 23 页

[原页](RAW.pdf#page=23)

````text
可以看到 dola 在接收到 “ ⾦叉买⼊法回测 ” 这个问题之后，⾸先能⾃⼰⽣成⼀个计划，包括了需
要进⾏的数据准备、策略实现、回测实现和结果分析等详细内容。
在按照⾃⼰的计划执⾏完毕后， dola 最终产出回测结果，完成可视化并进⾏深⼊分析总结，产
出⼀份完整的回测报告。
同时还可以将分析的报告做成⼀个美观的可视化插画 / 静态⽹页 / 看板，⼤⼤增加了报告的可读
性：
````

## PDF 第 24 页

[原页](RAW.pdf#page=24)

````text
（上图左为Dola⽣成的插画报告，右为静态⽹⻚。仅做样例展示参考，不构成分析建议）
这⾥只是以股票回测这样⼀个⽐较复杂的案例场景展开，⼤家应该可以想象到，在⼯作场景
中， Dola 对于⽇常数据分析⼯作的提效程度是显⽽易见的。
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
````

## PDF 第 25 页

[原页](RAW.pdf#page=25)

````text
阅读 1 . 6 万
````

## 采集与转写核验记录（非原文）

以下说明由本次核验添加；上方逐页文本保持文本层原样，图片与布局以PDF为准。

- PDF物理页 23,24：附录 Dola 案例图片区域在页图中出现空白/加载占位，图像细节无法核对；旁侧正文仍可读。
