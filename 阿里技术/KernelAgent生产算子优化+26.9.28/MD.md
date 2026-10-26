# 从榜单走向真实业务负载：Kernel Agent 刷新 Qwen3.8–Max 核心推理算子性能：PDF文本转写

> 仅转写原PDF文本层，页码为物理页序。图表、代码版面、未加载区域的限制见AI笔记与META；文本提取为空不表示原页为空白。

[原始PDF](RAW.pdf) · [AI学习笔记](AI_KernelAgent生产算子优化.md) · [来源与核验](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

```text
从榜单⾛向真实业务负载：Kernel Agent 刷新 Qwen3.8-Max 核⼼
推理算⼦性能
原创 范睿博 阿⾥技术 2026年9⽉28⽇ 03:54 浙江 4⼈
这是2026年的第 64 篇⽂章
（ 本⽂阅读时间：约 15 分钟 ）
在 60 个真实 shape 上，AKA 三条关键算⼦线的平均时延均低于专家版本；较⽣
产/官⽅基线最⾼加速 1.55×。
关键词：GPU Kernel、Kernel Agent、FlashAttention-4、Gated DeltaNet、⽣
产级优化
01
从 benchmark 到⽣产：验证标准正在改变
过去⼀年，Kernel Agent 已成为 GPU 软件栈的研究热点。EvoKernel、CUDA-Agent、
NVIDIA AVO、KDA、CAKE 等⼯作，展示了 Agent ⽣成 Kernel、调⽤编译器与
profiler，并通过⻓周期迭代探索硬件性能上限的能⼒。
这些能⼒主要在公开 benchmark 上得到验证。KernelBench、SOL-ExecBench 等基准提
供统⼀、可复现的测试场景；Qwen3.8 也曾在 SOL-ExecBench 的 FlashInfer-Bench ⼦
集登顶。公开榜单证明了 Agent 能在给定题⽬上⽣成正确且⾼性能的 Kernel，但⽣产交付
要求回答另⼀个问题：它能否直接替换现有的推理框架已经集成的⾼性能实现，并获得更多
的性能收益？
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

```text
两者的区别不只是输⼊规模更⼤。Benchmark 通常围绕有限的 shape、数据类型和调⽤接
⼝；⽣产算⼦则必须同时覆盖真实shape 分布、混合精度的数据语义和 MTP 负载，并遵守
算⼦在推理模型结构上下游中既有的输⼊/输出协议。优化不能只对少数 case 有效，也不能
依赖特定输⼊分布或绕过必要计算；它需要在整组 workload 上保持精度、稳定性和总体收
益，任⼀⽅⾯失效都可能使其⽆法上线。
因此，从榜单成绩⾛向⽣产，不只是继续压低⼀次 benchmark 的耗时，⽽是要在完整软件
契约和⼯作负载约束下找到可以稳定部署的新执⾏路径。这也意味着，⾯向⽣产的 Kernel
Agent 必须同时具备结构搜索能⼒和⼯程验证闭环。Atrex Kernel Agent（AKA）正是⾯向
这⼀⽬标构建的⽣产级异构推理算⼦⽣成Agent，由阿⾥巴巴 TRE AI 系统⼯程团队研发，
通过编码 Agent、性能 Profiling、GPU 评测与正确性⻔禁形成持续优化闭环。
Qwen3.8-Max 真实业务负载上的优化结果
作为⾯向⼤规模在线服务的旗舰模型，Qwen3.8-Max 每⽇承载数以亿计的调⽤，注意⼒和
线性注意⼒算⼦位于每次推理的关键路径，单个 Kernel 的微秒级下降会在⾼并发流量中放
⼤为吞吐提升、成本下降和服务余量。此次，AKA 将验证对象从公开 benchmark 推进到真
实⽣产负载，并以⽣产/官⽅实现和专家⼿⼯优化版本为参照；在 FA4 （FlashAttention-
4）prefill、FA4 decode 和 GDN（Gated DeltaNet）prefill 三个关键算⼦、60 个代表业
务负载的真实 shape 上，AKA 的⼏何平均时延全部低于专家版本，相关 Kernel 已经开源
于atrex-kernels算⼦库｜https://github.com/alibaba/atrex-kernels。
三条算⼦线的⼏何平均时延均呈现同⼀排序：AKA 最快，专家其次，⽣产/官⽅基线最后。
图 1｜三条算⼦线完整 shape 集合的⼏何平均时延，数值越低越好。
加速⽐均为“基线时延 / AKA 时延”。
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

```text
图 2｜FA4 prefill、FA4 decode 和 GDN prefill 的最优搜索轨迹。
⽣产实现归⼀化为 1.00，虚线分别表示⽣产和专家⽔平；
02
三类实现：⽣产实现、专家版本与公开基线
三条算⼦线均在同⼀硬件、同⼀接⼝、同⼀组 shape 上⽐较⽣产/官⽅实现、专家版本和
AKA。候选先通过数值正确性⻔禁，再进⼊完整 workload 的性能复测；AKA 以现有最优开
源实现为起点进⾏增量优化。
• FA4 prefill 对⽐ FlashInfer-TRTLLM ⽣产路径（闭源）和 Atrex 专家⼿⼯实现；
• FA4 decode 对⽐公开 FlashInfer 和针对 Qwen decode 负载调优的 Atrex 专家实现；
• GDN prefill 对⽐ FlashInfer 官⽅ chunked 主⼲和独⽴的 Atrex M64 专家实现。
按时延严格⽐较，AKA 相对⽣产/官⽅基线分别有 30/30、19/20 和 10/10 个 shape 更
快；相对专家则分别有 25/30、12/20 和 10/10 个 shape 更快。decode 的决定性增益集
中在 q4 MTP。
图 3｜逐 shape 的基线/AKA 加速⽐分布。横线为 1.0× 持平线；点位⾼于 1 表示 AKA 更快。
03
三个案例：从结构重构到编译期特化
3.1 FA4 prefill：在常规单序列上重构持久化调度
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

```text
在 batch=1、Q=KV=4224 的常规单序列 self-prefill 上，AKA 的时延为 63.42 µs，相
对专家的 74.37 µs 加速 1.17×，相对⽣产的 94.60 µs 加速 1.49×。
这个 shape 使⽤ page64、16 个 Q head、1 个 KV head 和 256 维 head。AKA 与专家
都使⽤单个 2-CTA Kernel，因此性能差异不来⾃多 Kernel 切分，⽽来⾃对调度和内部流
⽔的进⼀步重构。
专家版本采⽤固定的 2-CTA tile 调度。AKA 则为 batch=1 的⼤ prefill 引⼊ persistent
grid：常驻 cluster 跨约 4 个 wave 连续处理多个逻辑 tile，复⽤ pipeline、TMEM 和
barrier 状态，将启动、分配、同步与退出开销摊到更多⼯作上。单请求没有跨请求的负载不
均，M-raster 还会将 causal attention 由轻到重的计算量交错分配给常驻 cluster。
数据通路也同步特化：原⽣ page64 TMA 直接按⻚搬运 K/V，避免通⽤路径的⻚⾯拼装；
load-and-reduce 加速⾏最⼤值计算；causal softmax 被拆成⽆ mask 前缀和有 mask
后缀，并在⾏最⼤值不变时跳过不必要的校正缩放；最终⽤合并写回和提前释放输出资源收
紧 epilogue。这些改动联合将专家已深度优化的单 Kernel 路径再加速 1.17×。这说明AKA
不仅搜索 tile，⽽是可以联合重构跨 tile 调度、数据搬运、softmax 和写回流⽔。
图 4｜FA4 prefill 常规单序列性能⽐较。
3.2 FA4 decode：原⽣适配 page128，q_len = 4 MTP 专项调度
在 q_len = 4 MTP 的 10 个 shape 上，AKA 全部领先专家，⼏何平均约 1.19×；相对⽣
产实现约 2.15×。
Qwen3.8-Max 的 decode 同时包含 q_len=1 单 token decode 和 q_len = 4 MTP 两种
负载。⽣产⻚表采⽤ page128，⽽上游通⽤⼊⼝主要围绕 page64 设计，接⼊时通常需要
由适配层将 KV 数据零拷⻉重解释为两个 page64，并同步重展开⻚表。AKA 让 Kernel 原
⽣接受 table_page_size=128，直接匹配⽣产布局，并把 q_len=1 与 q_len = 4 作为
两种不同的调度问题处理。
q_len = 4 路 径 采 ⽤ prediction_tile=2 、 sequence_tile=128 、
cluster_kv=2 等组合，配合 split/reduction 搜索；编译期 mask 特化、循环剥离和静
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

```text
态 trip count 则消除了通⽤路径中的边界分⽀。q_len=1 路径与专家基本持平，整体优势来
⾃最难的 q_len = 4 MTP 段。完整 20-shape 结果为相对⽣产 1.55×、相对专家
1.075×。
图 5｜FA4 decode 在 q_len = 1 与 q_len = 4 MTP 两类负载上的性能⽐较。
3.3 GDN prefill：AKA 发现新的流⽔设计
10 个 shape 的⼏何平均时延为：AKA 179.830 µs，专家 192.176 µs，FlashInfer core
229.604 µs。
这条线路从公开 FlashInfer chunked 主⼲启动，搜索期间没有向 Agent 提供专家 M64 源
码或策略；最终，AKA 在公开主⼲上独⽴⾛出另⼀条路径。GDN（Gated DeltaNet）是
Qwen 混合架构中的线性注意⼒算⼦，也是本次三条线路中⾃主搜索周期最⻓的⼀条。
两 条 M64 路 径 的 核 ⼼ 差 异 ， 是 并 ⾏ 问 题 和 标 量 流 ⽔ 都 被 重 新 设 计 。 专 家
⽤ cluster_shape_mnk=(1,2,1) 由 两 个 CTA 协 作 拆 分 value；AKA 保
持 cluster_shape_mnk=(1,1,1)，在问题描述层⾯把⼀个物理 value head 重述为两
组⾏块，让调度器直接分配。在 B=1、M64 的稳定路径上，专家采⽤ g2r 与 chunk
lookahead；AKA 则增加 scalar-TMA warp，将四个 head 的标量列合并搬⼊共享内存，
并配合静态 TMA 描述符与 q3/k4/v2/o1 流⽔。
在这⼀过程中，NCU 与内核级时间线 profiler（IKeT）的联合反馈定位了标量搬运和同步
等待问题，推动了 scalar-TMA warp、事件流与流⽔阶段的调整。
为了找到这⼀版，AKA 进⾏了 117 轮有效探索。AKA 为 179.830 µs，低于专家 192.176
µs 和 FlashInfer core 229.604 µs。
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

```text
图 6｜GDN prefill 的 117 轮⾃主搜索轨迹
三条线呈现出同⼀条路径：专家把既定接⼝内的空间调到极致，AKA 则把接⼝边界、Kernel
数量、计算分解和调度结构⼀起纳⼊搜索。FA4 prefill 的 batch-1 persistent grid、
decode 的 q1/q4 分治和 GDN 的 value ⾏块拆分，都是 Plan 先形成结构假设，再由
Agent 经过编译、正确性和完整 workload 性能验证得到的结果。专家优化“这个接⼝下怎
么最快”，AKA 进⼀步搜索“这个接⼝本身该⻓什么样”。
04
AKA 的系统设计
AKA 是⼀套持续运⾏的 GPU 性能⼯程闭环。⾸先通过 Atrex-Bench 将真实业务
workload 转化为算⼦契约和评测基线；Plan 结合 GPU Wiki、计算模式及硬件特性提出数
学变换、数据布局和流⽔线设计；编码 Agent 负责修改 Kernel 与运⾏时路由；Agate 提供
隔离、可复现的 GPU 执⾏和评测环境；NCU 与内核级时间线 profiler 提供性能反馈；
Supervisor 则机械化管理正确性⻔禁、完整 workload 复测、版本管理和失败回退。
真实业务 workload
↓
Atrex-Bench 契约与性能基线
↓
Plan + GPU Wiki 提出结构优化⽅案
↓
Agent 修改 Kernel 与运⾏时路由
↓
Agate：编译 → 正确性验证 → 全 shape 性能复测
↓
NCU / IKeT 反馈性能瓶颈
↓
Supervisor 晋级、回退并沉淀经验
└──→ 下⼀轮搜索
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

```text
4.1 ⽬标：Atrex-Bench 让真实 workload 成为优化对象
Atrex-Bench 的算⼦接⼝和 shape 来⾃百炼平台的真实部署 workload。Agent ⾯对完整
shape 集合、⽣产⻚表和既定 buffer 契约，⽽不是⼀个容易过拟合 的示例输⼊。它不仅
负责计时，也定义优化⽬标：真实流量中最昂贵、最值得优化的算⼦，获得更⾼的探索优先
级。
4.2 设计：Plan 在写代码之前完成结构推演
Plan 模块结合算⼦的接⼝范围、计算模式和硬件特性，先建⽴可搜索的设计空间，再让
Agent 编码实现。设计空间包括数学等价变换、tile 与 layout 重组、pipeline 和 warp
role 设计，以及主机端与设备端边界的移动。
4.3 反馈：从 NCU 指标到 Kernel 内部时间线
NCU 可以告诉 Agent 吞吐、occupancy、访存和 warp stall 的宏观状态；在最新架构
下，TMA、MMA、barrier 和 warp ⻆⾊之间的细粒度耦合，往往决定最后⼏个百分点。
AKA 在⼯作流中引⼊内核级时间线 profiler（如IKET），记录 warp role、pipeline
wait、TMA/MMA 与 barrier 的内部事件。
NCU 回答“哪⾥慢”，细粒度profiler可以进⼀步回答“哪个 warp 在什么同步点等待”。前述
GDN 案例中 scalar-TMA warp、事件流和流⽔阶段的改动，正是由这类反馈提出并验证的
结构假设。
4.4 验证：稳定更优的版本才会晋级
Supervisor 对预算、正确性、测量、晋级和回退负责。候选必须先通过正确性硬⻔，再接受
完整 workload 评测和独⽴复测；错误或回归版本⾃动回退，稳定更优的版本才会晋级。代
码、Profile、知识记忆和实验⽇志同步保留，使每个版本都可以复现、解释和回滚。
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

```text
05
Harness ⾃进化：把优化流程也纳⼊实验
AKA 正在实验性地把进化对象从 Kernel 扩展到承载优化流程的 harness。系统汇总优化轨
迹，从历次实验中提炼⾼价值上下⽂、有效 profiler 信号和成功操作序列，⽤于改进提示词
结构、知识路由、预算分配和复测策略。
进化前的 harness 在第 28 轮越过专家线，在第 48 轮达到 186.799 µs，再经过 55 轮探
索于第 103 轮突破到 184.268 µs。进化后 harness 的另⼀次 GDN 实验保留了 23 个已完
成 Attempt，并⾏运⾏两条 Trajectory。按 Excel 中“最终 Kernel”的权威延迟计算累计最
优值，第 11 个完成 Attempt 已越过专家线，第 22 个达到 187.299 µs。从 Token 成本
看，进化后 harness 约在 1.56 亿 tokens 越过专家线，约在 3.08 亿 tokens 达到
187.299 µs；进化前轨迹越过专家线⽤了约 7.30 亿已记录 tokens。这表明新 harness 更
早进⼊⾼性能区间；
图 7｜进化前后 harness 在 GDN prefill 上的合并轨迹。横轴统⼀为完成轮次：
左轴实线表示累计最优时延，右轴点线表示累计 Token ⽤量。
Harness ⾃进化的⽬标，是让同样的 token 和 GPU 预算覆盖更多⾼价值假设，并更早进⼊
有效搜索区间。AKA 不只优化算⼦，也开始优化寻找算⼦的流程。
06
结语：从“会优化”到“能交付”
Kernel Agent 的公开研究已经表明，Agent 可以在标准题⽬上⽣成并优化 GPU Kernel；
AKA 这次把问题推进到了⽣产契约：⾯对 Qwen3.8-Max 的真实关键算⼦、复杂调度约
束，以及专家已经深度优化过的实现，Agent 仍然找到了新的执⾏路径，并在三条独⽴算⼦
线的⼏何平均时延上全部低于专家版本。
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

```text
AKA 将反馈、设计和⽣产验证组织成⼀个可以持续运⾏的闭环，把专家经验之外的结构维度
纳⼊搜索，也把⼀次性能突破沉淀为下⼀次优化的系统能⼒。这是 Kernel Agent 从公开评
测⾛向⽣产算⼦的⼀次重要跨越。后续，这套闭环将继续扩展到更多 Qwen ⽣产算⼦、融合
路径和硬件形态，让“⽣产 workload → ⾃动优化 → 可复现验证 → ⼯程集成”成为 GPU 软
件栈的常规开发路径。
开源项⽬与快速体验
AKA ⽀持 NVIDIA、AMD 和 PPU 等硬件平台，适配 Claude、Qoder、Codex、Pi 等编
码 Agent，并覆盖 Triton、CuTe DSL、CUDA、FlyDSL、TileLang 等编程范式。⽆论是
公开 Benchmark 还是 Atrex-Bench 真实⽣产任务，AKA 都⽤同⼀套可复现、可审计、可
恢复的⼯程流程管理优化过程。
AKA 已正式开源：GitHub｜https://github.com/alibaba/atrex-kernel-agent。克隆仓
库后，可以在仓库根⽬录下启动 Claude Code、Codex 或 Qoder，直接描述⽬标算⼦、硬
件平台和优化预算，由 Agent 调⽤ AKA 的统⼀编排⼊⼝启动优化任务；完整环境准备、命
令示例和产物说明请参考仓库中的 Quick Start。同时，阿⾥巴巴 TRE AI 系统⼯程团队开
源其⽣产级异构算⼦库：GitHub｜https://github.com/alibaba/atrex-kernels。
如果你正在研发推理引擎、训练框架、GPU 软件栈或⾼性能算⼦，欢迎 Star、试⽤并通过
GitHub Issues 反馈问题；也欢迎共同贡献新的算⼦任务、硬件后端、编程范式与 GPU 优
化知识。
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

```text
欢迎留⾔⼀起参与讨论~
AI Native · ⽬录
上⼀篇 下⼀篇
代码⽣成越来越快，软件交付真正的瓶颈转向 AI Native 回忆录：稳定性前端 S1 实践复盘
了哪⾥？
阅读 1753
留⾔ 1
写留⾔
ॐ(cid:0)ॐ(cid:0)安然 云南 9⽉28⽇
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

```text
博博好棒
⾸评
```

