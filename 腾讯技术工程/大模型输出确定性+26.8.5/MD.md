# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
AI  Infra 进阶：如何让⼤模型输出确定的结果
腾讯程序员 Aug  5 , 2026 , 2 : 25  AM⼴东原创 腾讯技术⼯程 550  listened
作者：binnnliu
背景
你有没有发现跟⼤模型对话，同样的提示词每次结果都不⼀样。  这符合我们对于 “ ⼤模型的
本质就是个猜词器 ” 的⼀贯认知。
然⽽，可重复性是科学进步的基⽯。因此让⼤模型输出完全确定的结果是⼀个⾮常值得研究
的问题，特别是强化学习需要确定性的  Rollout ，来保证实验的可复现性和训练过程的稳定
性。
其实很多同学第⼀时间会想到：  同样的硬件，同样的提示词：
1. 是不是把  Temperature 设置为  0 ，关掉随机采样就好了？
2. 如果业务需要  Temperature > 0 ，那把随机数种⼦（ Seed ）锁死，是不是也能保证每次输出
⼀样？
我已经测试过了，环境：vllm serve Qwen/Qwen3-8B  答案：  是也不是。
是（ Run-to-run 确定性）：  同⼀时间，没有其他请求时，多次同样的提示词请求，回答是
⼀样的；
不是（ Batch Invariance / 批次不变性）：  同⼀时间，有其他请求时，多次同样的提示词请
求，回答是不⼀样的；
什么！难道不同的请求间会相互影响？不可能，不同请求间的注意⼒机制是严格物理隔离，
不存在上下⽂污染的问题。
其实这⼀切的根源是推理引擎底层的动态组批与算⼦调度策略引发了浮点加法的顺序变化，
⽽浮点加法不满⾜结合律：(a + b) + c ≠ a + (b + c)。
Reproducibility is a bedrock of scientific progress.
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
从系统设计的⻆度来看，导致结果波动的根本原因，不在于信息⼲扰，⽽在于系统为了掩盖
访存延迟，在底层触发了⾮确定性的硬件级并⾏优化（ Non-deterministic Hardware-
level Parallel Optimizations ）。
相对于定点数，浮点数的本质是科学计数法，主要是为了在有限的位数内（如仅仅  16 bit 或
32 bit ），实现动态的数值范围与绝对精度间的 trade-off 。指数越⼤能表示的数值范围也就
越⼤，同时因为尾数位数⻓度固定，指数越⼤能表示的绝对精度也就越低。绝对精度（即步
⻓）的计算公式为：ULP (x) = 2E - M，其中  E  是该浮点数的真实指数，M  是尾数位数。
根据  IEEE 754 标准， FP16 包含  1bit 符号位、 5bit 指数位和  10bit 尾数位。当数值为  2048
（即  211）时，其规格化表示为  1.00000000002 × 211。此时，相邻可表示数之间的步⻓
（ ULP ）增⾄  2 ，这意味着  FP16  的下⼀个可表示数为  2050 ，⽆法精确表示  2049 。当底
层硬件执⾏  2048 + 1  时，运算器内部会借助更宽的  GRS 扩展位（保护位、舍⼊位、粘滞
位）得出精确结果  2049 。但当结果需要写回  10 位尾数时，由于  2049 恰好位于  2048 与
2050 的正中间，系统触发了向偶数舍⼊（ Round to Nearest, ties to Even ）的规则，最终
结果被强⾏舍⼊回  2048 。
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
这⾥需要说明是：
这个例⼦只是为了说明 “ 浮点加法不满⾜结合律 ” 。在实际  推理过程中，  GEMM 是
FP16/BF16 输⼊、 FP32 累加； batch variance 依然存在，根因是  reduction topology 改
变，⽽不只是  FP16 存储精度低。
数值 规格化表示 真实指数 实际存储指数 物理尾数位  (10 bit) 累加拆解
0.5 1.00000000002 × 2-1 -1 14 (01110) 0000000000 2-1
1 1.00000000002 × 20 0 15 (01111) 0000000000 20
2 1.00000000002 × 21 1 16 (10000) 0000000000 21
2046 1.11111111102 × 210 10 25 (11001) 1111111110 210 + 29 + ⋯ + 21
2047 1.11111111112 × 210 10 25 (11001) 1111111111 210 + 29 + ⋯ + 20
2048 1.00000000002 × 211 11 26 (11010) 0000000000 211
2050 1.00000000012 × 211 11 26 (11010) 0000000001 211 + 21
那么问题⼜来了，都有哪些操作会改变浮点加法顺序呢？这个我们要从矩阵运算说起。
GEMM 的 Batch Invariance
GEMM 操作为啥会改变浮点加法顺序呢？这要从 GEMM 的优化策略说起。
GEMM 的优化策略
要理解这个问题，必须要先理解内存墙下  GPU GEMM 算⼦的演进路线。很多⼈可能会问：
不就是⼀个基础的矩阵乘法吗，怎么搞得这么复杂？
答案是：极其复杂，甚⾄整个  AI Infra 领域都在围绕它疯狂卷细节。  核⼼原因在于：现代
GPU 的计算单元（Tensor Core）算⼒增⻓太猛，远远甩开了显存带宽的增速。这就导致
GPU ⼤部分时间都在等数据搬运，计算单元由于未能及时获取输⼊数据，⼤量时间处于空闲
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
等待状态（即  Compute Bound 退化为  Memory Bound ）。这就是所谓的内存墙
（ Memory Wall ）。
for i from 0 to M:          // 外层：遍历  A 的⾏  ( 总共  M ⾏ )
    for j from 0 to N:      // 中层：遍历  B 的列  ( 总共  N 列 )
        for k from 0 to K:  // 内层：计算  A 第 i ⾏  和  B 第 j 列  的点积  ( ⻓度为  K)
            C[i,j] += A[i,k] * B[k,j]
Tiling - 分块矩阵乘法
如果单纯按照上述公式逐个元素去计算，每次乘加运算都需要从极其缓慢的全局显存
（ HBM ）中读取数据。由于完全没有利⽤到⽚上⾼速缓存（ SRAM / 共享内存）和寄存器
（ Registers ），这会导致海量的  HBM 重复读操作，使得算⼒⽆法的充分利⽤。
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
为了打破内存带宽的瓶颈，业界演化出了  IO-Aware （ I/O 感知）  的分块算法。其核⼼思想
是：化整为零，将⼤矩阵切分成适合放⼊缓存的⼩块。 调度时，将每个 CTA （ Cooperative
Thread Array/ Thread Block ）与结果矩阵  C  的⼀个特定⼩块  Cij  绑定，让该  CTA 全权负
责这个⼩块的计算。
⼀个  CTA 负责计算  Cij  的完整数据流转逻辑如下：
1. 初始化累加器
分配寄存器，专⻔⽤于存放⽬标分块  Cij  的中间累加结果。
2. 沿着 K 维度规约
沿着公共维度  K  步进扫描。在每⼀个步⻓（ Step p）内执⾏以下流⽔线：
3. Load (HBM → SRAM)：将当前计算所需的⼦块  Aip  和  Bpj  从缓慢的全局显存，⼀次性
批量搬运到速度更快的共享内存（ SRAM ）中。
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
4. Compute (Warp GEMM)
：各个  Warp 从  SRAM 中将数据提取⾄寄存器，交由  Tensor Core 执⾏极速的矩阵乘法。
5. Accumulate
：将本轮算出的乘积结果，就地与寄存器中的累加器相加。不写回显存。
1. 收尾与写回（ Epilogue ）
当  K 维度的循环全部跑完，寄存器中的累加器便得到了  Cij  的最终精确值。此时，再将其统⼀
写回全局显存（ HBM ）。
Split-K
基于我们刚刚梳理的逻辑：每个  CTA 负责输出矩阵  C  的⼀个  Tile ，并在内部沿着  K  维度串
⾏跑循环。
但现实中经常会遇到⼀种极端情况：假设  K  的维度极其庞⼤，⽽输出矩阵  C  （即  M  和  N  维
度）⾮常⼩，⼩到只能切出  4 个  Tile 。
此时， GPU 硬件调度器只会拉起  4 个  CTA 去⼲活。要知道，⼀块  NVIDIA H100 拥有  132
个  SM ，这就意味着有  128 个  SM 处于完全空闲的状态，都在等待那  4 个  CTA 在极其漫⻓
的  K  维度上苦哈哈地跑  Loop ， GPU 的算⼒也被极⼤的浪费了。
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
既然在空间维度（M, N）上切不出更多的任务，⽐如在  LLM 推理的  Decoding 阶段，
Batch Size 极⼩，M=1，如果强⾏只按空间切分，会导致  GPU 上⼤量核⼼⽆活可⼲，那能
不能在 K 维度拆分，分配给不同的 CTA 计算呢？ —— 这就是所谓的  Split-K 优化策略。它的核
⼼思想是：打破单个  CTA 独⾃计算整个  K  维度的逻辑，把  K  维度切分成多段（ Split_K ），
让多个不同的  CTA 同时处理同⼀个  Cij  块在不同  K  ⽚段上的局部乘积累加。
（特别注意：其实在普通的  Tiling 计算时，也是沿着  K  维度分段计算的。但两者有本质区
别：BLOCK_K  是时间上的串⾏，同⼀个  CTA 每次从全局显存搬运  BLOCK_K  ⼤⼩的数据，
在寄存器中按固定顺序累加；⽽  SPLIT_K  是空间上的并⾏，强⾏把任务分发给物理上独⽴
的多个  CTA 同时计算。）
如图所示，假设设置  Split-K = 2，不同颜⾊的  Tile 分别由两个独⽴的  CTA 并⾏处理，
算⼒利⽤率瞬间翻倍。最终通过 atomic_add 将结果累加到 C 的同⼀位置。  这⾥需要注意的
是： SPLIT_K 太⼤ , atomic_add 竞争增加 , 收益会递减。
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
当然除了 atomic_add 的⽅式，还有⼀种实现⽅式：  Workspace Reduction ，具体⼯作流
程：
1. 分配  Workspace （显存分配）：在 HBM 中额外分配⼀块⼤⼩为  [split_k, M, N]  的
临时内存缓冲区（ Workspace ）。
2. 执⾏  Partial GEMM Kernel: 启动主矩阵乘法  Kernel 。每个  Thread Block 负责计算  K
维度上的⼀个切⽚。计算完成后，不使⽤原⼦加，⽽是将局部结果直接写⼊到
Workspace 中属于⾃⼰的那个切⽚位置（即  workspace[k_idx, m, n]）。
3. 执⾏  Reduction Kernel ：主  Kernel 执⾏完毕并同步后，启动第⼆个独⽴的轻量级规约
Kernel 。这个  Kernel 负责沿着  split_k 维度，将  Workspace 中的局部结果相加，并将最
终的求和结果写⼊到⽬标输出矩阵  C 中。
GROUP_M - Swizzle L2 Cache
通过约束  CTA 在矩阵 C 中的调度顺序，避免了由于跨度过⼤的离散内存访问⽽导致的  L2
Cache 抖动（ Cache Thrashing ）和频繁的数据驱逐。它在逻辑上将多个独⽴的  CTA 重新
组合成⼀个维度为  GROUP_SIZE_M × N  的宏观调度矩阵。在这个被限定的连续执⾏区间
内，由于被调度的  CTA 集中处理空间上相邻的输出块，它们能够共享已加载⾄  L2 Cache
中的矩阵  A 和  B 的数据，从⽽最⼤化数据的时间局部性与  L2 Cache 的复⽤率。这何尝不
是另外⼀种维度的 Tiling 呢 ? 只是为了复⽤ L2 。⽽之前我们提到的 Tiling ，是为了复⽤
SRAM 和寄存器。更进⼀步Tensor Parallel(Column/Row Parallel) 其实也是更⾼维度的
Tiling 呢～
算⼦调优
前⽂探讨了  Tiling 、 Split-K 、 Swizzle 等旨在缓解访存瓶颈的核⼼优化策略。但在实际的
GPU 硬件执⾏层⾯，针对不同规模的输⼊张量（ Tensor Shape ），系统必须确定具体的并
⾏化切分配置：即矩阵分块的具体维度（BLOCK_M / BLOCK_N / BLOCK_K）以及  K  维度
的切分段数（SPLIT_K）。这些切分参数的选择，不仅直接决定了算⼦的访存效率与硬件利
⽤率（ Occupancy ），更关键的是 —— 分块参数的动态变化会重塑底层浮点数累加的归约拓
扑（ Reduction Tree ），这是导致⼤模型推理在不同批次下失去 Batch Invariance 的根本原
因。
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
为了解析推理引擎底层为何会根据输⼊特征动态变更这些调度参数，我们需要先回顾  GPU
算⼦的编程范式演进，并深⼊探讨现代编译器引⼊的⾃动调优（ AutoTune ）机制。
CUDA VS Triton
在之前的《 AI Infra ⼊⻔： GPU 是如何⼯作的》中，我们探讨了  CUDA 编程模型与  GPU 硬
件执⾏模型：  Grid 定义了内部 Thread Block 的组织形式 (gridDim) ； Thread Block 定义了内
部 thread 的组织形式 (blockDim) 。
然⽽，原⽣  CUDA 编程的⻔槛依然极⾼，开发者需要⼿动实现各种底层且繁琐的优化逻辑。
OpenAI Triton 的出现，彻底改变了这⼀现状。⼤幅降低了编写⾼性能  GPU 算⼦
（ Kernel ）的⻔槛，让开发者能以接近  Python 的⽣产⼒，写出接近  CUDA C++ 专家级性
能的代码。借助内核融合（ Kernel Fusion ）、 IO-Aware 等底层优化技术， Triton 不仅保证
了极致性能，还兼顾了极佳的硬件⽆关性。
两者核⼼思想的差异在于编程范式：
CUDA （以线程为中⼼）：开发者需要显式定义底层⽹格，例如  <<>> ，由底层⽣成  128 个线
程，硬件再将其划分为  4 个  Warp 调度执⾏。
Triton （以 Tiling/Block 为中⼼与⾃动调优）：开发者只需关注数据分块，并可通过
@triton.autotune 装饰器提供⼀个配置搜索空间（如不同的分块⼤⼩、测试  4 个或  8 个
Warp ）。 Triton 编译器不仅会在底层⾃动将需求（如  4 个  Warp ）精准映射为  4×32=128 个
线程以屏蔽硬件细节（即 <<>> ），更会在运⾏时⾃动进⾏基准测试，智能选出当前硬件下的
最优参数组合。
在  PyTorch 2.0 及更⾼版本中，引⼊了 OpenAI Triton 作为编译器：
1. 前端分析：当⽤户调⽤  torch.compile(model) 时， PyTorch 的前端（如  TorchDynamo ）会捕
获计算图。
2. 后端优化与代码⽣成：默认后端  TorchInductor 会分析图中可以被  Kernel Fusion 的操作，⽣
成  OpenAI Triton 代码。
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
3. JIT 编译与执⾏：最后，由  Triton 的  JIT (Just-In-Time) 编译器接管这些代码，将其编译成⼀
个为特定  GPU 硬件⾼度优化的、单⼀的融合内核（ Fused Kernel ），最终⾼效执⾏。
在这⼀⽣态体系下， PyTorch （借助  Inductor + Triton ）⾃动接管了过去需要  CUDA 专家耗
费⼤量精⼒才能完成的性能调优⼯作。尽管⾃动调优的  Inductor+Triton 在绝⼤多数场景下
都能带来巨⼤的性能⻜跃，但它本质上仍是⼀个通⽤型的⾃动化⽅案。当⾯对极其关键、对
性能压榨到极致的特殊算⼦时，纯⼿⼯的底层优化依然不可或缺。
当然，⽆论是让编译器⾃动调优，还是我们⼿动调优，都必须穿透抽象，理解  GPU 底层最
核⼼的物理边界与调优逻辑。
在硬件执⾏层，多个  Thread Block 可以共享同⼀个流多处理器（ SM ）。只要  SM 的物理资
源（寄存器、共享内存等）还没被占满，硬件调度器就会把更多的  Block 塞进同⼀个  SM ⾥
并发执⾏。然⽽，每个  SM 都有硬性的并发规格上限（例如最⼤线程数  2048 ，最⼤  Block
数  32 ）。
寄存器限制
A100/H100 每个  SM 的物理寄存器⽂件⼤⼩固定为  65536 个  32-bit 寄存器（ 256 KB ）。
每个硬件线程最多只能分配  255 个寄存器。  ⽽单个线程需要的寄存器数由两部分组成：
基础开销（ Base Overhead ）：每个线程私有的，⽤来存内存指针、循环计数器、 TMA 状
态等；
累加器分摊（ Accumulator Share ）：假设输出块⼤⼩，即 Accumulator 为  BLOCK_M ×
BLOCK_N ，这寄存器是被所有线程平摊的。每个进程的寄存器⽤量为： BLOCK_M ×
BLOCK_N / NUM_WARPS / 32 。如果 Tiling 变⼤，必须同步增加 num_warps, 否则会导致
Register Spilling ；
关联公式： (BLOCK_M * BLOCK_N) / (num_warps * 32) <= 255 通常需控制在  128 左右 ,
如果超过 255 ，num_warps  必须调⼤，或者  BLOCK  必须调⼩。
同⼀个 Thread Block 内的  Thread 可以通过共享内存（ Shared Memory ）进⾏数据交
换，并且可以进⾏同步（ __syncthreads() ）。
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
执⾏范式与共享内存限制
在传统的  CUDA 优化实践中，提升  Occupancy （占⽤率）以隐藏访存延迟是⼀项核⼼原
则。即线程级并⾏（ TLP ）隐藏延迟： SM 上驻留的活跃  Warp 数量越多（即  Occupancy
越⾼），硬件调度器（ Warp Scheduler ）在当前  Warp 因访存⽽阻塞（ Stall ）时，就越容
易找到其他处于就绪状态的  Warp 进⾏切换。通过这种零开销的上下⽂切换，系统使得计算
指令与内存访问在时间上相互重叠，从⽽有效隐藏了全局内存的物理延迟。
然⽽，在  Ampere / Hopper 架构中， Tensor Core 提供了极⾼的浮点吞吐量，但  HBM 的
物理访存延迟并未同⽐例缩减。在这种计算能⼒远超访存带宽的背景下，⾼  Occupancy 策
略的边际效益急剧衰减：即使  SM 上驻留了⼤量  Warp ，它们也会迅速耗尽当前计算任务，
并集体触发访存请求，导致所有  Warp 同时陷⼊阻塞。此时，单纯依靠线程级的上下⽂切换
已⽆法掩盖内存级别的物理延迟。
为维持  Tensor Core 的⾼吞吐率，现代  GPU 引⼊了硬件级异步内存拷⻉机制（如  Ampere
架构的  cp.async 和  Hopper 架构的  TMA 引擎）。 num_stages 的核⼼思想是利⽤多级缓
冲（ Multi-Buffering ）实现计算指令与数据搬运指令的异步并发。即 GEMM 的优化⽅向从⾼
并发掩盖访存延迟转向通过  Asynchronous Pipelining ( 异步流⽔线 )  来掩盖延迟。
若  num_stages 配置过⼩（如默认值  2 ），计算过程易因等待数据就绪⽽产⽣⽓泡
（ Pipeline Bubble ），导致总体吞吐量受限。若配置过⼤，除导致  SRAM 溢出触发编译失
败（ Out of Shared Memory ）外，管理多级流⽔线状态的指针还会消耗额外的寄存器资
源，造成性能倒退。在不同硬件架构（如  SRAM 容量更⼤的  H100 ）上进⾏⾼阶调优时，核
⼼痛点在于寻找能够最⼤化重叠率、且不触发资源溢出的最佳边界配置参数。
(BLOCK_M * BLOCK_K + BLOCK_N * BLOCK_K) * 字节数  * num_stages <= SMEM 物理上
限  ( 如  H100 是  228KB)
调优 Trade-Off
以  Llama-3-8B Q/K/V Linear Proj - Fused QKV 为例， hidden_size 为 4096 ，
qkv_proj_size 为 6144 ，如下：
⽬标
矩阵 计算公式 输⼊  X 维度 权重矩阵  Wqk
v  维度 输出结果维度 备注
Fuse
d QK
V
QKVou
t = X · Wqkv
[num_sched_t
okens, hidden
_size]
[hidden_siz
e,qkv_proj_s
ize]
[num_sched_to
kens, qkv_pro
j_size]
权重按列拼接，
执⾏单次宽矩阵
GEMM
4096 (Q) + 1024
(K) + 1024 (V) =
6144
即： M=num_sched_tokens,N=6144,K=4096 ，其中 BLOCK_K ⼀般设置为  16 、 32 或
64 。
BLOCK_M / BLOCK_N 的设置：
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
M 很⼤时（ M>4096) ，原则上我们希望提升计算强度， BLOCK_M × BLOCK_N 尽可能
的⼤，极⼤地复⽤ SMEM ，此时需要寻找  num_warps 的平衡点， num_warps 太⼩会导
致⼲活的线程少，单个线程分摊到的累加器寄存器过多，进⽽击穿单线程最多  255 个寄
存器的物理上限，触发 Register Spilling ；⽽ num_warps 太⼤会导致基础开销占⽐⼤，
⼀个 CTA 占⽤⼤量 SM 资源，从⽽导致 GPU Occupancy 降低。需要⼀个合适的
num_warps 来确保  BLOCK_M × BLOCK_N ⾜够⼤。
M 很⼩时  （ M<64 ），缩⼩  BLOCK_M 贴合  M ，为了充分利⽤  SM 的算⼒，可以  1. 适度
缩⼩  BLOCK_N 从⽽产⽣更多的 Tile 分发给不同的  SM ；  2. 开启  Split-K ，在  K 维度拉起
更多  CTA 并⾏计算。
指标
优化的
硬件⽬
标
核⼼作⽤与定义 Trade-Off
BLOCK
_M / BL
OCK_N
共享内
存  (SM
EM)
⼀级缓
存  (L1)
矩阵⾏与列⽅向的⼦块⼤⼩（如  12
8, 256 ），决定了每次读⼊共享内
存的数据⾯积。
如果太⼤，会导致每个线程消耗过多寄存
器，引发  Register Spilling （寄存器溢出到极
慢的  Local Memory ），导致性能雪崩。
BLOCK
_K
共享内
存  (SM
EM)
在维度  K  上每次累加的⻓度。 同上，通常设置为  32 或  64 。需与  M/N/num
_stages 配合计算总  SMEM 占⽤。
num_w
arps
寄存器
(Regist
ers)
并发度
(Occup
ancy)
每个  Thread Block 分配的  Warp
数量（ 1 Warp = 32 线程）。本质
是分⺟，⽤来稀释每个线程的计算
量。
太⼩：累加器撑爆单线程  255 个寄存器上
限，发⽣致命的  Register Spilling 。
太⼤：单个  Block 占⽤过多  Warp ，导致⼀个
SM ⾥装不下⼏个  Block ，并发度（ Occupan
cy ）暴跌。
num_st
ages
全局显
存  (HB
M)
延迟掩
盖
软件流⽔线级数。开辟多份缓存，
让计算单元在算当前块时，后台异
步去取后⾯的块。
太⼤会导致  SMEM 溢出
GROUP
_M 即 S
wizzle
⼆级缓
存  (L2
Cache)
将⼏个连续的⾏打包成⼀组，打破
默认的逐⾏扫描。
共享已加载⾄  L2 Cache 中的矩阵  A 和  B 的
数据，从⽽最⼤化数据的时间局部性与  L2 C
ache 的复⽤率
SPLIT_
K
流多处
理器  (S
M)
算⼒利
⽤率
将极⻓的  K  维度切分给不同的  Blo
ck 同时算，最后再做原⼦加法（ At
omic Add ）合并。
仅在  M  和  N  极⼩、K  极⼤的情况（⽐如 Flas
h-Decoding ）开启，能提⾼ SM 利⽤率。
Batch Invariance 的来源
前⽂探讨了诸多优化策略，那么具体是哪些参数的变动导致了浮点加法顺序的改变？
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
从数学本质来看，矩阵乘法  C = A × B（其中  A  为  [M, K]，B  为  [K, N]，C为  [M,
N]）中任意元素  Ci,j  的计算逻辑是恒定的 —— 即取  A  的第  i  ⾏与  B  的第  j 列进⾏点积：
Ci,j = Σk=0K-1 Ai,k × Bk,j
在  Triton / CUDA 的底层优化中，针对各项调度参数的动态调整，其对确定性的影响有着本
质区别：
BLOCK_M
  与  BLOCK_N（⽆影响）：分块逻辑为加载  Tile_A [BLOCK_M, BLOCK_K]  与
Tile_B [BLOCK_K, BLOCK_N]，并计算输出  Tile_C [BLOCK_M, BLOCK_N]。这仅仅是在做空
间维度的任务映射，决定了哪些元素被打包在⼀起独⽴计算，以及由哪个具体的  CTA (Thread
Block) 负责计算哪⼀块区域。对于输出矩阵  C  中的特定元素  Ci,j  ⽽⾔，⽆论它被分配给哪个
CTA 、与哪些相邻元素⼀起被计算，其底层的  K  维度点积逻辑并未改变。因此，改变这两个参
数不会影响浮点加法的顺序。
GROUP_M / Swizzle
（⽆影响）： Swizzle 本质上是改变了多个  CTA 在⽹格（ Grid ）级别的调度顺序，以此来提⾼
L2 Cache 的命中率。它决定的是先算哪⼀个空间块，后算哪⼀个，完全没有⼲涉某⼀个特定
分块内部的乘积累加过程。因此， Swizzle 同样不会破坏 Batch Invariance 。
BLOCK_K
（引⼊确定性误差）：定义了在规约维度（ Reduction Dimension ）上的步⻓。改
变  BLOCK_K  会直接改变单次循环中加载到寄存器中的数据量，进⽽改变  Tensor Core 内部
MMA 指令的累加树拓扑。这种改变会导致浮点加法顺序的变化（即不同  BLOCK_K  产⽣不同
结果，但同⼀  BLOCK_K  结果恒定）。
SPLIT_K
（引⼊⾮确定性误差）：将  K  维度强⾏切分给多个  CTA 并发执⾏。如果采⽤ Atomic Add 进⾏
结果合并，由于  GPU 硬件调度线程块的先后顺序是完全随机的，加法顺序是完全随机不可控
的。即便采⽤ Workspace Reduction ，SPLIT_K 段数的动态变化同样会改变累加树拓扑。
num_warps
  和  num_stages  的本质是硬件资源分配与流⽔线调度（决定分配多少个 cta 去算、开辟⼏份
缓存池做异步搬运）。并不改变宏观的矩阵点积计算逻辑和 Reduction Tree 拓扑。
综上所述，推理引擎在性能与确定性之间存在着固有的架构冲突，为了追求极致的访存复⽤
（动态调整  BLOCK_K）与并提升流多处理器（ SM ）的并发利⽤率（动态开
启  SPLIT_K），底层的启发式调度策略不可避免地改变了浮点运算的 Reduction Tree 拓
扑，这正是⼤模型在动态  Batch 下丢失 Batch Invariance 的根本原因。那么在真实的推理场
景中，该如何修补这个机制？接下来我们深⼊  vLLM 的实现，看看它是如何在底层硬件特性
和上层调度逻辑之间做  Trade-off 的。
vLLM 中 GEMM 的 Batch Invariance ⽀持
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
怎么解决呢？直觉上，只需要在推理引擎中全局禁⽤  Split-K  并锁死  BLOCK_K  即可。但
现实的⼯程实现远⽐这复杂。现代推理引擎（如  vLLM ）底层的  GEMM 操作的下发路径涉及
多层抽象与多种后端。实现严格的  Batch Invariance 并⾮单⼀配置的修改，⽽是需要针对特
定的软硬件运⾏环境，进⾏多维度的执⾏路径路由与参数约束。具体的 GEMM 执⾏路径决于
以下三个维度的组合：
硬件架构（ Architecture ）： SM80 (Ampere) 与  SM90/SM100 (Hopper/Blackwell) 的底层
GEMM 执⾏范式截然不同 ⸺ 前者靠  warp 级并发掩盖访存延迟，后者靠  TMA + WGMMA 的
异步流⽔线。执⾏范式不同，实现 Batch Invariance 的逻辑也会不同。
数据精度（ Data Type ）： bf16/fp16 由⽣态最成熟的  cuBLASLt 承接；⽽  fp8/fp4 等低精度会
转向  CUTLASS （乃⾄  DeepGEMM 等）专⽤  kernel 。不同后端控制逻辑也不⼀致。
算⼦⼊⼝（ API Backend ）：nn.Linear  ⾛的是  vLLM ⾃⼰的  dispatch ，可直接路由到定制
⾼性能内核；⽽裸  torch.mm / bmm  ⾛  PyTorch dispatcher → cuBLAS/cuBLASLt ，调度权
在框架和闭源库⼿⾥。
SM8x vs SM90/SM100
SM80: warp 维度的 tensor core(mma.sync) 调度  : 优化逻辑是提⾼占⽤率， warp 同时负责
搬运和计算。
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
4096 * 4096 ->CTA Tile （如 128*128 ）   -> Warp Tile （ 32 * 64 ）  -> mma 指令级 (16 * 8 * 16)
SM90/100 TMA 硬件单元的引⼊和  WGMMA 指令（ Warp Group 128 线程）促成了范式转
移通过 Asynchronous Pipelining ( 异步流⽔线 ) 来掩盖延迟。
4096 * 4096 -> CTA Tile ( 如  256 *128) -> Warp Group Tile (64 *128) -> wgmma 指令级  (64
对于⼤矩阵，由于  CTA 分配到的总体空间⾜够⼤，每个  Warp 都能分到⼀块⾜够⼤的专属
空间（例如  32x64 ）。然后直接把⼤  Tile 切成⼩  Tile 分给  Warp ，这样多个  Warp 之间交
替访存和计算从⽽掩盖内存延迟。⼤家都各⾃在  K 维度独⽴、串⾏执⾏到底，互不⼲涉，
run-to-run 是没问题的。
但是 batch-to-batch 情况下BLOCK_K的发⽣变化，因此会引发浮点加法顺序的波动？
实际上呢，也不⼀定，这取决于 warp level 的 K 是不是恒定的。⽐如启发式的 auto tune 可能
导致BLOCK_K从 32 变成 64 ，但是实际的底层执⾏以 K=16 为步⻓，依次处理 K 维度的 tile ，因
此就从底层消除了 Batch Variance 。那是不是就是说可以忽略BLOCK_K的影响，只关注
Split-K就⾏了。讲道理，这个在⼤矩阵上⼤概率是成⽴的。
对于⼩矩阵，⽐如 32*32 分配到⼀个 CTA （ K=4096 ），那每个 warp 可能只能分配很⼩的
Tile ，从⽽没有⾜够多的 Tile ，即 M/N 并⾏度不⾜ -> 活的 warp 少 , 占⽤率低 -> 这种情况下在 K
维度串⾏执⾏就⽆法充分利⽤隐藏延迟的特性。因此，系统被迫让所有  Warp 重叠在这同⼀
块  32 * 32 的矩阵上，强⾏在时间（ K ）维度上进⾏切分（ Warp-level K-Slicing ）。  多个
Warp 各算⼀段  K ，最后在共享内存⾥通过 Reduction Tree 合并。⼀旦  Batch 参数变动导致
K 切分段数改变，规约树形状就会改变，从⽽引发了浮点加法顺序的波动。
不过到了 SM90+, 降低了对传统⾼  occupancy 隐藏访存延迟的依赖，标准  WGMMA
mainloop 中，⼀个 warpgroup 共同维护分布式  accumulator ，并依次处理  K tile ，不需要
当然对于⼩矩阵， GEMM 库此时可能选择更⼩的  tile 、 GEMV/SIMT 、 persistent
kernel 、 warp-level K-slicing 、 CTA-level Split-K 或  Stream-K 等不同算法。
Warp-level K-slicing 会让多个  warp 分别计算同⼀输出  tile 的不同  K 分⽚，再在  CTA
内合并  partial results ；它可以增加单  CTA 内的有效  warp 数，但不能增加  grid 中的
CTA 数量。为了提升 SM 的利⽤率，通常需要  CTA-level Split-K 。
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
⽣成多个独⽴  warp partial result 后再做  CTA 内  reduction 。
所以我们可以看到代码注释： "Hopper (SM90) and Blackwell (SM100): the only source
of batch variance is split-k" ，  即在 SM90 Hopper / SM100 Blackwell 上，当前受⽀持和
测试的  FP16/BF16 PyTorch/cuBLASLt 路径，在禁⽌  Split-K batch invariant 。
这⾥需要特别说明的是， SM90/SM100 锁定Split-K可以获取 batch invariance ， SM8x 需
要同时锁定BLOCK-K和Split-K才能获取 batch invariance 都是基于测试的，因为
cuBLAS / cuBLASLt 是闭源的。
当然也有很多⼈误认为 Split-k 多 workspace 时，规约树是按顺序规约的，可以保证结果不
变，但是这个只是 run-to-run 维度的，⼀旦 K 变化，结果还是会变化。
说了这么多，其实呢，最终浮点数加法的顺序，不仅受 mainloop 的  BLOCK_K staging 决
定的（ CTA Tiling ），也受更低维度的 Warp Tiling/Warp Group Tiling （以及硬件原⼦指令
粒度）决定。但是呢，要解决这个问题却要从 CTA Tiling ⻆度来。
SM80 上 GEMM 的 Batch Invariance ⽀持
对于 SM80 要同时关注SPLIT_K和BLOCK_K。其实对于 Linear 层的 GEMM ⽆论 SM 是哪个版
本 / ⽆论是 eager 还是 compile mode ，都会⾛到 linear_batch_invariant ->
matmul_persistent 。
# class UnquantizedLinearMethod(LinearMethodBase):
def apply(
    self,
    layer: torch.nn.Module,
    x: torch.Tensor,
    bias: torch.Tensor | None = None,
) -> torch.Tensor:
    if envs.VLLM_BATCH_INVARIANT and current_platform.is_cuda_alike():
        return linear_batch_invariant(x, layer.weight, bias)
    return dispatch_unquantized_gemm()(layer, x, layer.weight, bias)
⽽对于⾮线性层的计算，⽐如代码中直接调⽤ torch.mm, 则还需要额外考虑。由于 SM80 在
cuBLASLt 上不⽀持禁⽤ BLOCK_K, 只能更换 Triton 实现，最终也会⾛到
matmul_persistent 。其中 matmul_persistent 是⼀个 persistent kernel 即
griddim=num_sm ，固定  K 顺序、固定  tile 、不切  SPLIT_K。
````

## PDF 第 17 页

[原页](RAW.pdf#page=17)

````text
if current_platform.is_device_capability_family(80):
    # SM80 (Ampere) cannot rely on cuBLASLt-only determinism; install the
    # triton persistent matmul overrides for mm/addmm/matmul/linear.
    _batch_invariant_LIB.impl("aten::mm", mm_batch_invariant, "CUDA")
    _batch_invariant_LIB.impl("aten::addmm", addmm_batch_invariant, "CUDA")
    _batch_invariant_LIB.impl("aten::matmul", matmul_batch_invariant, "CUDA")
    _batch_invariant_LIB.impl("aten::linear", linear_batch_invariant, "CUDA")
特别注意： compile mode 下 aten override 不⽣效，所以会⾛到原始的 aten::mm 。
matmul_persistent 是怎么做到确定性的
对于 bf16 和 fp16 ，所有 SM 版本的 SM 的  Linear ，⽆论是 eager 还是 compile mode ，最终都
落到  matmul_persistent  这个  Triton kernel 。当然 eager mode 下，  SM80 的裸  mm 的
也会⾛到matmul_persistent。（ compile mode 下 aten override 不⽣效，所以会⾛到原
始的 aten::mm ）
matmul_persistent  的实现逻辑很简单，相对于普通  GEMM 靠  @triton.autotune /
cuBLASLt 启发式按  shape 挑  config ，matmul_persistent  直接固定  config ，彻底关掉
autotune 。  每种  dtype ⽤⼀套硬编码的分块参数，特别是BLOCK_K，与输⼊的  M/N/K ⽆
关：
configs = {
    torch.bfloat16: {"BLOCK_SIZE_M": 128, "BLOCK_SIZE_N": 128, "BLOCK_SIZE_K": 64,
                     "GROUP_SIZE_M": 8, "num_stages": 3, "num_warps": 8},
    # fp16 / fp32 各⾃⼀套，同样是常量
}
SM90/SM100 上 GEMM 的 Batch Invariance ⽀持
对于， SM90/SM100 只需要关注 Split-K ，即禁⽌SPLIT_K拆分；
bf16 /fp16
上⾯已经提到了对于 Linear 层的 GEMM ⽆论 SM 是哪个版本，都会⾛到
linear_batch_invariant ，最终⾛到 matmul_persistent 。
这⾥要澄清⼀点：BLOCK_M/N/K、SPLIT_K  对  Triton autotune 来说都只是普通
constexpr ，⽽  split-k 本身是⼀种需要作者⼿写进  kernel 的实现模式（多⼀维  grid +
atomic/reduction ），并⾮  autotune 的⾃动优化策略。matmul_persistent 没有实
现  split-k ，所以它既不受  autotune 影响，也天然不存在  Split-K 乱序 —— 真正被写死
的就只有  BLOCK_K  这⼀个变量。
另外函数名⾥的 persistent 其实跟 batch invariance ⽆关，是说 grid 只
开  min(NUM_SMS, tile 数 )、每个  program 常驻  SM 循环吃多个  tile ），是为了避
免频繁  launch 开销， tile→CTA 的映射本就由固定  config 决定，与确定性⽆关。
````

## PDF 第 18 页

[原页](RAW.pdf#page=18)

````text
对于直接调⽤ torch.mm 的部分，当前的逻辑是仍然⾛ cuBLASLt ，只是依赖设置确保 Split-
K=1 。
设置了 preferred_blas_library(backend="cublaslt") 之后， GEMM 会优先⾛ cuBLASLt ，
通过设置 reduction mask ，确保了 bf16/fp16 Split-K=1 。
CUBLASLT_MATMUL_PREF_REDUCTION_SCHEME_MASK =
CUBLASLT_REDUCTION_SCHEME_NONE
reduced_precision_val = (
    (False, False) if is_torch_equal_or_newer("2.10.0") else False
)
torch.backends.cuda.matmul.allow_fp16_reduced_precision_reduction = (
    reduced_precision_val
)
torch.backends.cuda.matmul.allow_bf16_reduced_precision_reduction = (
    reduced_precision_val
)
torch.backends.cuda.preferred_blas_library(backend="cublaslt")
传统  cuBLAS 后端没有  reduction-scheme mask 这个能⼒ ,PyTorch ⾥⼀旦设了
allow_splitk=False ⼜没切到  cuBLASLt, 会直接  TORCH_CHECK 报错 :
TORCH_CHECK(reduction != DisallowReducedPrecisionDisallowSplitK,
"...allow_splitk=False) requires the cuBLASLt backend");
fp8
fp8 的⼊⼝是量化线性层⾥的  cutlass_scaled_mm，底层有  CUTLASS 与
cuBLASLt scaled_gemm  两条路。
选中  CUTLASS → 调它（ csrc if(batch_invariant) 锁  config 不随  M
cuBLASLt scaled_gemm → 由于 API 设置 mask 仅⽀持 bf16/fp16 ，对于 fp8 只能另外想办
法。怎么办呢？把 workspace 的限制到尽量⼩，⽽ split-k(COMPUTE/OUTPUT) 与
atomic(INPLACE) reduction 都需  workspace ，最终可选策略只剩不需  workspace 的
NONE ，即  split-k=1 ；但  scaled_gemm 没设置  reduction-mask ，⽆  API 级保证。
os.environ["CUBLASLT_WORKSPACE_SIZE"] = "1"
FlashInfer → DeepGEMM
fp4
````

## PDF 第 19 页

[原页](RAW.pdf#page=19)

````text
如果开启了 batch invariant ，⽆论  M 多⼤，都固定使⽤同⼀个配
置  sm100_fp4_config_default。另外就是选择 PersistentScheduler ，确保 K 维度不拆
分。
CUTLASS 3.x TileScheduler 的定义：
类型 调度⽅式 K 维度拆分
cutlass::gemm::PersistentScheduler持久化 data-parallel ，不拆  K
cutlass::gemm::StreamKScheduler持久化 拆  K （ stream-K/split-K ）
// Dispatch function to select appropriate config based on M
template <typename OutType>
void cutlass_fp4_gemm_dispatch(torch::stable::Tensor& D,
                               torch::stable::Tensor const& A,
                               torch::stable::Tensor const& B,
                               torch::stable::Tensor const& A_sf,
                               torch::stable::Tensor const& B_sf,
                               torch::stable::Tensor const& alpha, int64_t m,
                               int64_t n, int64_t k, cudaStream_t stream) {
  if (vllm::vllm_is_batch_invariant()) {
    using BiGemm = Fp4GemmSm100<sm100_fp4_config_default, OutType>;
    static_assert(
        cute::is_same_v<typename BiGemm::TileScheduler,
                        cutlass::gemm::PersistentScheduler>,
        "batch_invariant requires a persistent tile scheduler; stream-K or "
        "split-K would break numerical invariance");
    runGemm<BiGemm>(D, A, B, A_sf, B_sf, alpha, m, n, k, stream);
    return;
  }
  uint32_t const mp2 = std::max(static_cast<uint32_t>(16), next_pow_2(m));
  if (mp2 <= 16) {
    // m in [1, 16]
    runGemm<Fp4GemmSm100<sm100_fp4_config_M16, OutType>>(
        D, A, B, A_sf, B_sf, alpha, m, n, k, stream);
  } else if (mp2 <= 256) {
    // m in (16, 256]
    runGemm<Fp4GemmSm100<sm100_fp4_config_M256, OutType>>(
        D, A, B, A_sf, B_sf, alpha, m, n, k, stream);
  } else {
    // m in (256, inf)
    runGemm<Fp4GemmSm100<sm100_fp4_config_default, OutType>>(
        D, A, B, A_sf, B_sf, alpha, m, n, k, stream);
  }
}
````

## PDF 第 20 页

[原页](RAW.pdf#page=20)

````text
RMSNorm 的 Batch Invariance
RMSNorm - 均⽅根归⼀化
这个算⼦的输⼊是[num_tokens, hidden_size]，然后需要对于每个 token 的 hidden 做均
⽅根归⼀化，均⽅根归⼀化的公式如下：
y = (x)/(RMS(x)) ⊙ γ  ，其中均⽅根（ RMS ）的计算：RMS(x) = √((1)/(d) Σi=1d xi2 + ε)
要理解具体的执⾏过程和优化逻辑要对于 GPU 的体系架构有⼀定的了解，可以参考本⼈的
《 AI Infra ⼊⻔： GPU 是如何⼯作的》，这⾥就不在赘述了。
由于 RMSNORM 需要做 token 维度的均⽅根归⼀化，这⾥显⽽易⻅，要确保每个 token 的
hidden 分配到⼀个 thread block ，这样可以避免跨 thread block 的同步。
dim3 grid(num_tokens);
````

## PDF 第 21 页

[原页](RAW.pdf#page=21)

````text
那怎么定义 blockDim 呢？⾸先要明⽩ blockDim 意味着什么 , blockDim 本质是分配给这个
block 的并发 thread 。这个东⻄太⼤的话， block 内的规约和同步的成本都会变⾼；太低呢，
每个 SM ⼜有 max block 上限，导致 GPU Occupancy 低。
// For large num_tokens, use smaller blocks to increase SM concurrency.
const int max_block_size = (num_tokens < 256) ? 1024 : 256;
const int block_size = std::min(hidden_size / calculated_vec_size, max_block_size);
dim3 block(block_size);
⼀般情况下，任务⾜够做（即 num_tokens 够时），⽆论block_size⼤⼩，都能有很⾼的
占⽤率。这时候  block_size  ⼀般设置为  256 ，可以避开⼤  Block 带来
的  __syncthreads()  同步的问题，实现各个⼩  Block 之间的⾼效并发。（也有些场景⼩
Block 会导致 grid 层⾯的规约变多，但是由于 RMSNORM 是 token 维度的计算，只有 block 层
⾯的规约，因此没有这个问题）
⽽当 num_tokens 很少时，情况就变了。⽐如只有 2 个 token ，即 2 个 thread block ，那顶多
也就占⽤ 2 个 SM ，这时候完全不⽤考虑全局 Occupancy 的问题了。这时候要考虑的就是尽可
能充分利⽤ SM 的并发算⼒，即⾜够多的线程 /warp ，让 stride loop 次数变少，因此设置⼀个
较⼤的block_size即可。性能提升参考这个PR #2 7931 Kernel Optimize rms_norm
kernel。
````

## PDF 第 22 页

[原页](RAW.pdf#page=22)

````text
然⽽block_size则会影响 1. 每个线程本地累加的元素分组； 2. BlockReduce 树形归约的
形状（层数、 warp 分组）。从⽽导致浮点数加法顺序发⽣变化。
那怎么避免呢？
vLLM 中 RMSNorm 的 Batch Invariance ⽀持
以上可以看到 ,rms_norm 的算法与优化本身都很简单。但它的  dispatch 逻辑其实相当复杂 :
仅仅是确定 " 在多后端、多平台、 eager/ 编译等多种组合下该⾛哪个算⼦实现 ", 就要花费很⼤
⼒⽓。这⾥涉及 vLLM IR 、 CustomOp 、 Torch Inductor 3 层 dispatcher, 这⾥就不深⼊了，
后续深⼊⽂章再深⼊解读下。
Mo
de
res
idu
al
Batc
h Inv
arian
ce
dtype /
quant Path Terminal implementation
ea
ger
non
e off bf16/fp
16
forward_cuda
→forward_native
→IR[vllm_c, nati
ve]
CUDA
rms_norm → rms_norm_kernel<sca
lar_t, vec_size, tensor_rank, ha
s_weight>
ea
ger yes off bf16/fp
16
forward_cuda
→forward_native
→IR[vllm_c, nati
ve]
CUDA
fused_add_rms_norm → fused_add
_rms_norm_kernel<scalar_t, widt
h, has_weight>
ea
ger
non
e on bf16/fp
16
forward_cuda
→rms_norm_batch_
invariant
Triton
_rms_norm_kernel
ea
ger yes on bf16/fp
16
forward_cuda
→rms_norm_batch_
invariant→ops.f
used_add_rms_nor
m
CUDA
fused_add_rms_norm → fused_add
_rms_norm_kernel<scalar_t, widt
h, has_weight>; block pinned → 102
4
````

## PDF 第 23 页

[原页](RAW.pdf#page=23)

````text
Mo
de
res
idu
al
Batc
h Inv
arian
ce
dtype /
quant Path Terminal implementation
co
mp
ile
non
e
off / o
n
bf16/fp
16
forward_native
→IR[native] native aten → Inductor Triton
co
mp
ile
yes off / o
n
bf16/fp
16
forward_native
→IR[native] native aten (add+norm) → Inductor Triton
co
mp
ile
non
e /
yes
off
fp8 sta
tic per-
tensor
RMSNorm(+add) + s
tatic_scaled_fp8_
quant → fused
CUDA
rms_norm_static_fp8_quant / fus
ed_add_rms_norm_static_fp8_quan
t; block (num_tokens < 256) ? 102
4 : 256
co
mp
ile
non
e /
yes
off
fp8 dyn
amic p
er-toke
n
RMSNorm(+add) + d
ynamic_per_token
_..._quant → fuse
d
CUDA
rms_norm_dynamic_per_token_quan
t; block fixed 1024
co
mp
ile
non
e /
yes
off
fp8 blo
ck g12
8/64
RMSNorm(+add) + p
er_token_group_fp
8_quant → fused
CUDA
rms_norm_per_block_quant → rms
_norm_per_block_quant_dispatch;
block (num_tokens <= 256) ? 512 :
256
co
mp
ile
yes on
fp8 sta
tic per-
tensor
fused_add_rms_no
rm
 node + quant → fusio
n matches
CUDA
fused_add_rms_norm_static_fp8_q
uant; block pinned → 1024
co
mp
ile
yes on
fp8 dyn
amic p
er-toke
n
fused_add_rms_no
rm
 node + quant → fusio
n matches
CUDA
rms_norm_dynamic_per_token_quan
t; block fixed 1024 (BI-safe by constructi
on)
co
mp
ile
yes on
fp8 blo
ck g12
8/64
fused_add_rms_no
rm
 node + quant → fusio
n matches
CUDA
rms_norm_per_block_quant; bloc
k pinned → 512
co
mp
ile
non
e on fp8 (an
y)
rms_norm_batch_i
nvariant
 → Triton; quant stays
separate
Triton
_rms_norm_kernel + separate quant
op — not fused
⼀个有意思的对照 : eager mode ，有 residual 的情况下，⽆论是否开启 Batch Invariance 都
会⾛到 CUDA 实现torch.ops._C.fused_add_rms_norm。⽽⽆  residual 的普通
````

## PDF 第 24 页

[原页](RAW.pdf#page=24)

````text
rms_norm, 开启 Batch Invariance 时才必须换成专⻔的  Triton
kernel _rms_norm_kernel。
当然也可以通过如下指令调整 IR OP 优先级：
vllm serve meta-llama/Llama-3.2-1B \
  --ir-op-priority.rms_norm=vllm_c \
  --ir-op-priority.fused_add_rms_norm=vllm_c
eager mode 下 RMSNorm 的 Batch Invariance
eager mode 下开启 Batch Invariance 时 , ⽆论是有 residual 的
CUDA torch.ops._C.fused_add_rms_norm(blockDim=min(hidden,1024), 锁住
max_block_size 上限为  1024) 还是⽆  residual 的 Triton _rms_norm_kernel(
BLOCK_SIZE=1024), 都通过让  reduction 宽度与  num_tokens 解耦来固定归约结构 , 从⽽
保证浮点加法顺序不变、跨  batch bit-exact 。
如下以  _rms_norm_kernel为例：
def forward_cuda(
    self,
    x: torch.Tensor,
    residual: torch.Tensor | None = None,
) -> torch.Tensor | tuple[torch.Tensor, torch.Tensor]:
    if envs.VLLM_BATCH_INVARIANT:
        assert self.variance_size_override is None, (
            "Batch invariance is not supported for variance_size_override"
        )
        return rms_norm_batch_invariant(
            x,
            self.weight.data,
            self.variance_epsilon,
            residual=residual,
        )
    return self.forward_native(x, residual)
vLLM 中 _rms_norm_kernel 是⽤ Triton 实现的，逻辑很简单，不⽤@triton.autotune加
BLOCK_SIZE = 1024。
````

## PDF 第 25 页

[原页](RAW.pdf#page=25)

````text
编译场景下  RMSNorm 的 Batch Invariance
其实这⾥才最反直觉的地⽅，上⾯说了 CUDA 的实现、 Triton 的实现，实际上最终默认逻辑
还是⾛了 torch.compile ⾃动⽣成的 Triton kernel 。
在  TorchInductor 编译模式下 ,vLLM 的  CustomOp 默认禁⽤ (custom_ops 在  Inductor 后
端下默认为  none),RMSNorm 因此不⾛⾃定义  CUDA/Triton 实现 , ⽽是分发到
forward_native, 再经 ir.ops.rms_norm / fused_add_rms_norm 的  native provider( 编译
态优先级为  ["native"]) 。该纯  PyTorch 参考实现由  TorchDynamo 捕获为  FX 图 ,Inductor
对其中的类型转换、平⽅、按最后⼀维求均值 ( 归约 ) 与权重乘法执⾏算⼦融合 , ⽣成单个
Triton 归约  kernel 。
RMSNorm 的输⼊形状为  [num_tokens, hidden_size], 归约沿最后⼀维 (hidden_size, 模型
的编译期静态常量 ) 进⾏ ;num_tokens 是并⾏维 , 各⾏相互独⽴、不参与彼此的归约。因此
When PyTorch Inductor is used, 'none' is the default; otherwise 'all'.
````

## PDF 第 26 页

[原页](RAW.pdf#page=26)

````text
num_tokens 的取值只决定并⾏⾏数 , 不参与单⾏内对  hidden_size 的浮点累加顺序。这是该
算⼦在编译态可保持批不变的结构前提。
@register_op
def rms_norm(
    x: Tensor, weight: Tensor | None, epsilon: float, variance_size: int | None = Non
) -> Tensor:
    """Weighted root-mean-square layer normalization"""
    orig_dtype = x.dtype
    x = x.to(torch.float32)
    x_var = x if variance_size is None else x[..., :variance_size]
    variance = x_var.pow(2).mean(dim=-1, keepdim=True)
    x = x * torch.rsqrt(variance + epsilon)
    if weight is not None:
        x = x.to(weight.dtype) * weight
    return x.to(orig_dtype)
编译器⾃动⽣成的  Triton Kernel ，它是如何维持  Batch Invariance 的？这⾥的核⼼问题在
于编译器的  Split-Reduction （拆分规约）  优化。类似于  GEMM 中的  Split-K ，当规约维
度（hidden_size）较⻓，且并⾏维度（ Batch Size ，即  num_tokens）极⼩时，为避免
GPU 的  SM 空载， Inductor 会触发多段拆分逻辑：将同⼀⾏的  hidden_size 强⾏切⽚，
分发给多个  Thread Block 并发计算局部和，最终再执⾏全局规约合并。
⽽是否对归约做多段拆分 (split-reduction) 由  Reduction.num_splits 决定 , 其中 :
# torch/_inductor/ir.py::num_splits
reduction_numel_hint = sizevars.symbolic_hint(reduction_numel)   # hidden_size
numel_hint           = sizevars.symbolic_hint(sympy_product(ranges))  # num_tokens
if not (_is_static(reduction_numel_hint) and _is_static(numel_hint)):
    return ReductionHint.DEFAULT, 1     # 仅对  unbacked symint 成⽴
symbolic_hint 的⾏为是 : 对  backed 符号⽤代表值 (backed_var_to_val) 替换为具体整数 , 对
unbacked 符号保留符号。
vLLM 默认使⽤  torch._dynamo.mark_dynamic(backed)。因此 num_tokens
经  symbolic_hint被替换为其代表值 ,_is_static(numel_hint)为真 , 上述提前返回不触
发 , 后续启发式正常执⾏ , 可能选出  split > 1 。该提前返回 ( 即所谓保守路径 ) 仅在使⽤
mark_unbacked 时才⽣效。
@support_torch_compile(
    # mark_unbacked_dims={"input_ids": 0}, 
forward_native — used by default during compilation; batch-invariant
dispatching is absent here, so it is silently skipped. Instead we relied on
Inductor to generate a batch-invariant Triton kernel. Issue #4 06 2 8  RFC vLLM
IR: Batch Invariance Dispatching in vLLM IR
````

## PDF 第 27 页

[原页](RAW.pdf#page=27)

````text
    dynamic_arg_dims={
        "input_ids": {0: "b"},
        "positions": {0: "b"},
        "intermediate_tensors": {0: "b"},
        "inputs_embeds": {0: "b"},
    },
)
def mark_dynamic(arg, dim_shape_pairs):
    if ds_type == DynamicShapesType.UNBACKED:
        ...
        torch._dynamo.decorators.mark_unbacked(arg, dim, hint_override=..., shape_id=
        ...
    else:
        torch._dynamo.mark_dynamic(arg, dims)   # 默认  BACKED 路径
进⼊启发式后 ,reduction_split_factor 的判定为 :
# torch/_inductor/choices.py:reduction_split_factor
if numel_hint >= 2 * num_sm:      # ⼤  batch → 不  split
    return 1
if reduction_numel_hint <= 8192:  # hidden ≤ 8192 → 不  split( 对任意  num_tokens 都成⽴ )
    return 1
# 仅  hidden > 8192 且  numel_hint < 2*num_sm 才  split>1, 且  split 值随  numel_hint 变
由于当今⼤部分开源模型都满⾜ hidden_size ≤ 8192 ， reduction_split_factor 对该条件恒
返回  1, 与  num_tokens 代表值⽆关 , 归约保持单程 (single-pass) 。同时 vLLM 借助
TorchCompileWithNoGuardsWrapper 阻⽌特化与重编译， compile_ranges_endpoints
默认为  None,get_compile_ranges() 返回空 , 即对任意  batch size 只编译⼀份图。即便配
置多个  compile_ranges ⽣成多张图 , 对  hidden_size ≤ 8192, 上述条件使  split 恒为  1 ，从
⽽归约结构⼀致，保持  Batch Invariance 。
特别注意：在 hidden size ⼤于 8192 时，显式配置  compile_ranges=[512] 或
compile_sizes=[N] 。此时编译器将针对特定 range/ 尺⼨  N 独⽴⽣成静态形状图，
numel_hint 与 hidden_size 的乘积导致启发式阈值导致 split 可能发⽣变化，从⽽ Inductor
Split-Reduction 拆分归约发⽣变化，导致该静态图与动态图的累加树形态产⽣结构性突
变，破坏算⼦级别的数值⼀致性。
compiled = torch.compile(fn, dynamic=False)   # 每个  shape 各编⼀份
compiled = torch.compile(fn, dynamic=True)    # ⼀份图通吃所有  shape
compiled = torch.compile(fn, dynamic=None)    # 默认 : 先特化 ,shape ⼀变就转成动态
TorchCompileWithNoGuardsWrapper ：  从 JIT 到 AOT
在  PyTorch 2.11 的  JIT （即时编译）机制下，计算图的运⾏强依赖  Shape Guard 来进⾏合
法性检查。但在  LLM 推理场景中， Batch Size 的频繁波动易触碰边界条件（例如 s0 >= 2
的  Guard 验证失败），从⽽触发  JIT 引擎的在线重编译（ Recompilation ），导致端到端延
迟出现明显的⽑刺。
````

## PDF 第 28 页

[原页](RAW.pdf#page=28)

````text
为 了 彻 底 消 除  JIT 带来 的性能 隐 患 ， vLLM 引⼊
了  TorchCompileWithNoGuardsWrapper  结合  Piecewise Backend ，实现了纯  AOT （提
前编译）派发。在预热阶段，系统会针对不同的张量形状区间提前⽣成多张预编译图。进⼊
运⾏时后，该  Wrapper 会主动拦截并丢弃底层所有的  Dynamo Guard 验证，由  vLLM 框架
层根据输⼊形状，以纯静态的⽅式直接路由到对应的预编译图上。因此，这⼀机制本质上是
由  vLLM 统筹调度的预编译图派发（ Dispatch ）系统，⽽⾮简单地让 torch.compile 去维护
单张动态图。
在这种分段编译机制下，具体算⼦的代码⽣成（ Codegen ）逻辑需视配置⽽定。以
RMSNorm 为例，当  hidden_size <= 8192  时，其  reduction_split_factor  通常为
1 ，这使得单⾏归约（ Inner Reduction ）能够保持⾼效的  Single-pass 执⾏。但需要注意的
是：最终系统会切分出多少张图、每张图采⽤什么代表值（ Representative Value ），以及
不同的图是否会命中相同的  Codegen 策略，都⾼度依赖于  vLLM 的  Compile
Ranges/Sizes 设定、动态  Shape 的类型以及  PyTorch 的具体版本。因此，任何关于底层
算⼦⾏为的绝对保证，都必须严格限定在明确的软件版本与编译配置环境内。
Attention 的 Batch Invariance
Attention 计算
````

## PDF 第 29 页

[原页](RAW.pdf#page=29)

````text
这⾥就不详细介绍 Attention 的基本原理了，之前写过⼀篇⽂章《 AI Infra ⼊⻔：⼤模型是如
何⾼效推理的  》，我们直接从 FlashAttention 实现说起。
操作名称 数学公式 宏观 Shape 变化 Tiling - 微观
Q-K Dot Prod
uct S = Q × KT
Q: [query_lens, num_heads, head
_dim]
K: [seq_lens, num_kv_heads, hea
d_dim]
S: [query_lens, num_heads, seq_
lens]
Q: [BLOCK_M, head_d
im]
K: [BLOCK_N, head_d
im]
S: [BLOCK_M, BLOCK_
N]
Scale S = S / √(d) shape 不变 shape 不变
Mask S = S + M shape 不变 shape 不变
Softmax P = softmax
(S)
P: [query_lens, num_heads, seq_
lens]
P: [BLOCK_M, BLOCK_
N]
MatMul O = P × V
P: [query_lens, num_heads, seq_
lens]
V: [seq_lens, num_kv_heads, hea
d_dim]
O: [query_lens, num_heads, head
_dim]
P: [BLOCK_M, BLOCK_
N]
V: [BLOCK_N, head_d
im]
O: [BLOCK_M, head_d
im]
Q TIle 对应的就是本次⼀起处理的 Q 维度 Token 即[BLOCK_M, head_dim], 本质上就是将宏
观的 Q [query_lens, num_heads, head_dim]沿  M 轴按  BLOCK_M 将 query_len 切分成
query_len / BLOCK_M 个  Q tile 。  (num_heads 也变成并发维度了 )
然后每个 CTA 负责⼀个 Q Tile ，沿  K/V ⽅向做⼀次融合遍历处理所有的历史 KV ，同时完
成  S=QKT、 online softmax 、以及  O += PV  三件事。让中间矩阵  S, P  始终活在寄存器中、
不写回  HBM—— 最后只把每个  Q tile 的  O  和  LSE 写出去。
BLOCK_M 只是影响多少个 Q 维度的 token 并发（即 query_len 维度），所以完全不应影响浮
点加法的顺序；⽽ BLOCK_N 是 KV 维度的 token 并发（即 seq_len 维度），是规约轴，会影响
浮点加法的顺序。不同的 BLOCK_N 导致 Online Softmax 缩放维度不⼀致，即多个 KV token
计算⼀个局部的m new，  同时 BLOCK_N 在O = P × V中其实就是 GEMM 中的 BLOCK_K, 会规
约树发⽣变化，但是 QK 点积没影响，因为 QK 点积是 head_dim 维度规约。
FlashAttention 中， BLOCK_M 与  BLOCK_N 都是编译期常量 , 且它们的取值只由
(head_dim, causal/local, dtype, arch) 决定 , 与 batch 与  seqlen ⽆关 —— 它们决定是单个
CTA 内部怎么算最快  ( 即受每个  SM 固定的寄存器 /SMEM 预算约束 ,head_dim 是把  tile 换
算成资源消耗的基本单元 ), ⽽要跑多少个这样的  CTA 由  grid 与  num_splits 负责。因此⽆论
不管  batch 多⼤、 seqlen 多⻓ ,tile 都是同⼀个值 , 规约顺序在该  kernel 内完全固定 , 结果逐
bit 确定。真正改变浮点加法顺序的 , 是切分规约轴 (KV 轴 ) 的优化（ SplitKV / num_splits ） :
把  KV 规约轴切给多个  CTA 再由  combine 合并 , 规约树结构改变。且其⾃动启发式的输⼊
````

## PDF 第 30 页

[原页](RAW.pdf#page=30)

````text
total_mblocks = batch_size × num_head_kv × num_m_blocks 正⽐于  batch, 所以
batch 变化会经由  num_splits 破坏  batch 不变性。
chunked prefill
FlashAttention 计算时， BLOCK_M 是对于 query_len 微观层⾯的切分，  chunked prefill 则
可以理解为对 query_len 的宏观层⾯上的切分。两者本质相同 —— 都沿  query 轴 (M 轴 ) 切、
块间互不归约 , 所以都天然  batch-invariant-safe; 但切的是不同层级的 query_len 。上⾯已经
看到了，对于相同的 (head_dim, causal/local, dtype, arch) ， BLOCK_M 是确定的，⽽
chunked prefill 中 query_len 的切分是随 batch 会发⽣变化的，那这⾥的切分是否会改变改变
浮点加法顺序呢？
chunked prefill 是调度层的切分， scheduler 按  token 预算决定这⼀  step 处理哪些请求的
哪些  token; 当某请求的  prompt ⼀次算不完时 , 它就被跨  step 切开 , 每  step 喂进  kernel 的
query_len 即该  step 分到的  chunk ⼤⼩ (prompt 短、预算够时⼀步算完 , 并不会被切 ; 同⼀
step 通常还混着别的请求的  chunk / decode) 。
BLOCK_M 是  FA kernel 层的切分 :kernel 拿到本  step 的  query_len 后 , 沿  M 轴按
BLOCK_M 分成  query_len / BLOCK_M 个  Q tile 。
之所以 query_len 切分不会影响浮点加法顺序有两个原因：
query_len 维度 (M 轴 ) 上， attention 计算是：请求内不同  query token 之间的  attention 计
算是并⾏的、彼此不存在归约，计算的 query_len 的每个 token 与  seq_len 中的  K/V token
chunked prefill 的输出其实就是 FA kernel 的输⼊ ——chunk ⼤⼩即  kernel 拿到的
query_len 。这个输⼊不仅影响⼏个  Q tile, 还经  num_m_blocks = ⌈ query_len/64 ⌉  影
响  kernel 要不要  split-KV:chunk ⼤  → query_len ⼤  → 判 " 填满  SM"→ 不切
KV(prefill 常态 ,BI 友好 );chunk 退化到  decode 的  1 → 可能触发  split-KV 。
````

## PDF 第 31 页

[原页](RAW.pdf#page=31)

````text
的关系；  切  query_len 只决定哪些  token 这⼀步⼀起算 , ⽆论怎么切 , 它对应的  n_block 切
分与累加顺序逐块对⻬、完全⼀致。
causal mask 保证每个  token 只依赖它⾃⼰和它之前的  token 。  K/V 是逐  token 独⽴⽣成
的 ( 每个  token 的  key/value 只由它⾃⼰的输⼊经权重投影得到 , 跨  token 之间没有计算依
赖 ); ⽽  causal mask 在  attention 这⼀步把每个  token 的归约范围控制在它⾃⼰及之前的所
有  token 。因此 Attention 最终的输出取决于 query 向量对它⾃⼰及之前所有  token 的  K/V 做
softmax 加权和（归约轴是  KV ⽅向），与  query_len ⽆关； chunk 怎么切 , 单个  token 的
数学结果不变。
FlashDecoding - split-kv
前⾯提到了 chunked prefill 沿  query 轴（ M 轴）切，块间不归约，天然 batch
invariance 。但到了  decode 阶段，情况正好反过来：每步  query_len 退化为  1 （ M=1 ），
⽽  seq_len (KV ）  却可能极⻓。如果让⼀个  Q tile 独占⼀个  CTA 、沿  KV 串⾏计算，那么
batch 很⼩时就只能拉起⼏个  CTA ，绝⼤多数  SM 空转 —— 这⾥本质上跟 GEMM 中的 Split-K
要解决的问题是⼀致的，只不过这⾥被切的规约轴是  KV 。
FlashDecoding 的做法就是  split-KV ：根据  (batch, heads, seq_kv, num_sms)  动态
的，把⼀个  query 的  KV 区间切成 num_splits 段，交给多个  CTA 并⾏，各⾃算出⼀段的局
部  O  与局部  LSE （ log-sum-exp ），最后由⼀个  combine/reduce 步骤按  LSE 把这些局部
结果合并成最终输出。这⼀步在数学上等价于  online softmax 的跨段合并。
问题就出在切⼏段上： num_splits 是根据  batch/seqlen 动态决定的，⽬标是填满  SM 。
num_splits ⼀变， LSE 合并时的规约拓扑就变，浮点加法顺序随之改变 —— 于是⼜丢了
batch invariance 。同样，这跟 Split-K 的逻辑⼀致：固定段数时  combine 是有序的、 run-
to-run 确定；可⼀旦  batch 让段数发⽣变化，结果照样会变。
vLLM 中 Attention 的 Batch Invariance ⽀持
这⾥实现 Batch Invarianc 逻辑也很直接，强制不拆  KV ，即  num_splits = 1。 vLLM 在
FlashAttention 后端⾥，只要开了  VLLM_BATCH_INVARIANT  就把  split 写死为 1 ：
# vllm/v1/attention/backends/flash_attn.py
if envs.VLLM_BATCH_INVARIANT:
    max_num_splits = 1
...
````

## PDF 第 32 页

[原页](RAW.pdf#page=32)

````text
# 各处调⽤  flash_attn 时统⼀：
num_splits=1 if envs.VLLM_BATCH_INVARIANT else max_num_splits
MLA 的  prefill/decode 路径同理（num_splits = 1）。代价是  decode ⼩  batch 下  SM
利⽤率会下降，这是 “ 确定性  ↔ 吞吐 ” 间  的 trade off 在  Attention 侧的⼜⼀次体现：和
GEMM ⼀样，我们牺牲了⼀部分并⾏度，换回了浮点加法顺序的稳定。
NCCL 的 Batch Invariance
前⾯我们讨论的都是单卡内部微观算⼦的调度导致的结果偏差。随着现代⼤模型模型参数量
的爆炸，当单卡显存⽆法容纳整个模型时，系统通常需要引⼊模型并⾏。其中， Tensor
Parallelism (TP) 是⼀个常⽤的⽅案：将单个矩阵乘法沿特定维度切分到多张  GPU 上。从这
个⻆度看， TP 可以被视为⼀种跨设备的⾼维  Tiling ，只不过  Tile 之间不再共享同⼀块⽚上
存储，⽽是通过分布式通信交换中间结果。
分布式计算中，计算往往不是瓶颈，跨设备通信（如  All-Reduce ）才是拖慢整体吞吐量的元
凶。为了减少通信，我们需要⼀种矩阵切分策略，使得多个连续的线性层在计算过程中尽可
能保持独⽴，直到最后⼀刻才进⾏数据同步。这就是在  MLP 或 Attention 中，通常会采⽤ “ 列
并⾏  →  ⾏并⾏ ” 的组合策略：
Column Parallelism ( 列切分 ) ： Fused QKV 和  FFN 的  Fused Gate/Up 都是列切分。
例如  QKV 的权重维度在单卡上会变成  [hidden_size, qkv_proj_size /
TP_size]，输出也相应变成  [num_sched_tokens, qkv_proj_size / TP_size]。
Row Parallelism ( ⾏切分 ) ： O_Proj 和  FFN 的  Down_Proj 是⾏切分。权重变
为  [hidden_size / TP_size, hidden_size]。计算完成后[num_sched_tokens,
hidden_size]，通过  AllReduce  算⼦来聚合跨卡结果。
````

## PDF 第 33 页

[原页](RAW.pdf#page=33)

````text
在不考虑  Sequence Parallel 、 Late All-Reduce 和通信融合的经典的  Dense Transformer
TP 实现中，⼀个  Transformer Block 通常包含两次此类同步： Attention 的  O_Proj 之后⼀
次， MLP 的  Down_Proj 之后⼀次。每个  Row-Parallel Linear 本身只需要⼀次  All-
Reduce 。具体⽽⾔，在⾏并⾏线性层计算结束后，每张卡都会产⽣⼀个维度
为  [num_sched_tokens, hidden_size]  的局部偏和（ Partial Sum ）张量。 All-Reduce
(Sum) 操作将跨卡对⻬规约这些张量，操作完成后，集群中的每张卡都将拥有⼀份完全⼀致
的、全局求和后的完整输出张量（维度保持  [num_sched_tokens, hidden_size]  不
变），从⽽使各卡可以⽆通信地独⽴执⾏后续的残差连接（ Residual Add ）与归⼀化
（ LayerNorm ）。那么问题来了，这⾥的多卡加法的顺序是恒定的吗？
答案是：在默认情况下，不⼀定。这是由于 NCCL 库在吞吐和延迟间的 trade-off 。
对于固定消息⼤⼩，它通常是稳定的；但跨不同  Batch Size ， NCCL 并不保证采⽤相同的规
约算法、通道数和数据切分⽅式，因此规约顺序不⼀定保持不变。
业界经典的  Ring All-Reduce（  Reduce-Scatter + All-Gather  ）的优势是⾼吞吐，
但是同时延迟会随节点数线形增⻓。从逻辑依赖上看， Ring All-Reduce 需要  (N-1) 个
````

## PDF 第 34 页

[原页](RAW.pdf#page=34)

````text
Reduce-Scatter step 和  (N-1) 个  All-Gather step 。 NCCL 会通过  chunk pipeline 和
Multi-Channel 将不同数据块重叠执⾏，但单个  chunk 的依赖链⻓度仍随  rank 数近似线性
增⻓。因此在⼩消息、低  Batch 的  latency-bound 场景下， Ring 很难充分发挥其带宽优
势。
为了在不同负载下都能压榨出极限性能， NCCL 在  communicator 初始化阶段根据硬件拓扑
构造多种候选通信图，并建⽴  latency/bandwidth 性能模型；在每次  collective ⼊队时，再
根据消息⼤⼩、 rank 数、节点数和可⽤传输路径选择预计代价最低的算法、协议及  channel
配置。
上⾯已经提到，在  LLM 推理的动态组批（ Dynamic Batching ）过程中， All-Reduce 的
Message Size 是按  [num_tokens, hidden_size]  计算的。这意味着， Batch Size 的波
动，会直接导致单次通信负载的⼤⼩发⽣变化。当通信载荷跨越某个阈值时， NCCL 会在底
层切换规约拓扑：
Ring 算法：  采⽤环形传递，加法顺序是线性的。例如  GPU0 → GPU1 → GPU2 →
GPU3。
Tree / Double Binary Tree 算法：  采⽤树状层级规约，加法顺序是分治的。例
如  (GPU0 + GPU1) + (GPU2 + GPU3)。
但这还不是全部。除了宏观算法的切换， NCCL 在微观执⾏链路上的多通道并发（ Multi-
Channel ）切分机制也会导致 Batch Variance 。现代  GPU 节点内通常具有多条物理互联链
值得⼀提的是， Baidu Silicon Valley AI Lab 较早将  HPC 领域的  Ring All-Reduce 系
统性地应⽤并推⼴到深度学习分布式训练中，使这⼀算法成为数据并⾏训练中的经典⽅
案。 NCCL 也⻓期将  Ring 作为核⼼算法之⼀。
````

## PDF 第 35 页

[原页](RAW.pdf#page=35)

````text
路（如多条  NVLink 链路）。为了压榨双向物理带宽， NCCL 引⼊了  Channel 的抽象。
NCCL 的  Channel 是⼀条独⽴的逻辑通信流⽔线。在  GPU kernel 中，每个活跃  Channel
通常由⼀个  CUDA Thread Block 负责；每个  Channel 拥有⾃⼰的  Ring/Tree 连接关系和
chunk 流⽔线。它不⼀定与某⼀条物理  NVLink ⼀⼀对应，但多个  Channel 可以帮助并⾏
利⽤多条可⽤链路。
当触发⼀个较⼤的  All-Reduce 任务时， NCCL 会将总数据块进⾏切⽚，分发给多个
Channel 并发执⾏规约。这⼀机制引发  Batch Variance 的原因在于以下两点：
拓扑异构：
为了实现双向链路吞吐的最⼤化， NCCL 会为不同的  Channel 分配结构或⽅向完全不同的规
约拓扑。 NCCL 可以为不同  Channel 构造不同的  Ring 或  Tree 。
例如，在某些拓扑上，分配  Channel 0 执⾏正向  Ring ，加法顺序为  (((GPU0 + GPU1) +
GPU2) + GPU3)；同时分配  Channel 1 执⾏逆向  Ring ，加法顺序则变为  (((GPU0 + GPU3)
+ GPU2) + GPU1)。
数据切分边界的动态滑动：
在  LLM 推理的动态组批中， Batch Size 的波动会导致  All-Reduce 的总  Message Size 发
⽣改变。⼀旦总数据量变化， NCCL 内部的启发式策略就会重新计算分配给各个  Channel 的
数据切分边界。这就导致了：原本在  Batch Size = N  时被分配到  Channel 0 负责规约的某
⼀段内存数据，在  Batch Size = N+1  时，可能因为切分边界的微调被划定到了  Channel 1
的负责区域。
  # vllm/config/parallel.py
  if envs.VLLM_BATCH_INVARIANT:
      self.disable_custom_all_reduce = True
vLLM 的  Custom All-Reduce 是节点内  TP 的低延迟性能路径，但它内部同样包含随消息⼤
⼩切换的  1-stage/2-stage 算法，因此不能被视为严格  Batch Invariant 。开启
VLLM_BATCH_INVARIANT=1 后， vLLM ⾸先禁⽤  Custom All-Reduce 和  symmetric-
memory 路径，再将  NCCL All-Reduce 固定到  Tree + Simple ，并将  Channel 数锁定为
1 ，同时关闭  NVLS 、 CollNet 等可能引⼊其他规约拓扑的通信路径。
vLLM 的  Custom All-Reduce 是默认性能路径之⼀，但它并不是当前严格  Batch
Invariance 模式的解决⽅案。它内部也包含  1-stage 和  2-stage 两套算法： TP4 下通常以
512 KiB 为切换点， TP6/TP8 下通常以 256 KiB 为切换点。 1-stage 会在每个  rank 上按照
固定指针顺序完整规约所有元素； 2-stage 则先由不同  rank 负责不同输出分区，再执⾏
All-Gather ，⽽且每个分区的累加顺序以其  owner rank 为起点循环展开。当消息⼤⼩改变
了算法选择或分区  owner 时，同⼀逻辑元素可能经历不同的累加顺序。因此  vLLM 的 Batch
Invariant 模式会直接禁⽤ Custom All-Reduce 。
````

## PDF 第 36 页

[原页](RAW.pdf#page=36)

````text
Custom All-Reduce 是 vLLM 针对节点内  Tensor Parallel ⾼频、⼩中消息  All-Reduce 所增
加的⼀条低延迟快路径。将单节点  TP All-Reduce 简化成⼀个直接访问所有  peer GPU 显
存的  CUDA kernel 。通过  CUDA IPC 提前获得  peer pointer ，使⽤轻量级  GPU barrier 、
128-bit 向量化访存以及 1-stage/2-stage 专⽤算法，减少  NCCL 通⽤路径在⼩中型消息上
的固定延迟。
def override_envs_for_invariance():
    os.environ["VLLM_ALLREDUCE_USE_SYMM_MEM"] = "0" # 关闭  NCCL/Torch symmetric-memory
    os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
    # NCCL determinism settings
    os.environ["NCCL_LAUNCH_MODE"] = "GROUP"
    os.environ["NCCL_COLLNET_ENABLE"] = "0"
    os.environ["NCCL_NVLS_ENABLE"] = "0"
    os.environ["NCCL_P2P_NET_DISABLE"] = "1"
    os.environ["NCCL_MIN_NCHANNELS"] = "1"
    os.environ["NCCL_MAX_NCHANNELS"] = "1"      # 强制单通道通讯
    os.environ["NCCL_PROTO"] = "Simple"
    os.environ["NCCL_ALGO"] = "allreduce:tree"  # 强制使⽤ tree 算法  + simple 协议
    os.environ["NCCL_NTHREADS"] = "1"
    os.environ["NCCL_SOCKET_NTHREADS"] = "1"
    # torch.compile settings
    os.environ["VLLM_USE_AOT_COMPILE"] = "0"
VLLM_ALLREDUCE_USE_SYMM_MEM=0 关闭的是  vLLM 基于  PyTorch Symmetric
Memory 实现的  multimem/two-shot All-Reduce 后端，避免请求根据硬件能⼒进⼊另⼀
套规约  kernel 。
NCCL_COLLNET_ENABLE=0 禁⽌ NCCL 使⽤ CollNetDirect/CollNetChain 等⽹络侧
collective-offload 算法； NCCL_NVLS_ENABLE=0 则禁⽌  Hopper/Blackwell NVSwitch
系统使⽤ NVLink SHARP multicast/reduction 路径。⼆者都是为了将候选规约拓扑收缩到
普通  NCCL Tree 。即不允许⽹卡 / ⽹络  collective plugin/NVSwitch 参与规约，避免  All-
Reduce ⾛  CollNet 或⽹络侧聚合路径。
这与单卡算⼦的解决⽅式本质⼀致： GEMM 需要固定  Split-K 和  K 轴分块， Attention 需要
固定  Split-KV ，⽽分布式  All-Reduce 则需要固定跨  rank 的规约图、协议和数据切分⽅
式。它们解决的都是同⼀个问题 —— 阻⽌系统根据  Batch Shape 动态改变  Reduction
Topology 。
总结
以上，⼤模型在推理过程中导致 Batch Variance 的根本原因，在于底层算⼦为最⼤化硬件资
源利⽤率，动态调整了规约轴（如  GEMM 中的  Split-K 或  Attention 中的  KV 轴）的切分策
略，进⽽改变了浮点数累加树的拓扑结构。若要实 Batch Invariance ，就必须在算⼦调度层
⾯约束此类动态切分⾏为。
````

## PDF 第 37 页

[原页](RAW.pdf#page=37)

````text
PS ：受限于篇幅同时保证⽂章质量，本⽂还有 2 个地⽅没有展开讲：⼀个是  MoE 架构下特有
的  Batch Invariance 问题；另⼀个是  NCCL 更深层的通信拓扑与底层机制。这些内容后续
再单开⼀篇填坑。
然⽽，⼯程实现却复杂的多。想要做到知其所以然，我们需要向下深⼊  GPU 物理微架构与
算⼦执⾏范式（ Triton/CUDA ），向上解析框架层的计算图编译逻辑（ Inductor/IR ）。所谓
的  AI Infra ，本质上是在这多层技术抽象中，寻求系统性能与数学等价性之间的最优  Trade-
off 。
PS: 关于 torch.compile/cuda graph/vLLM IR 部分严重拖慢了笔者的节奏，下⼀篇可能会这
是这个⽅向吧。
PS: 本⽂是对于 thinking machines 的博客《 Defeating Nondeterminism in LLM
Inference 》和 vLLM(v0.25.1) 中 Batch invariance 实现的学习笔记。值得⼀提的是，在阅读
代码的过程中还顺⼿帮 vLLM 修改了 bug 。 [Fix batch invariance in RMSNorm kernels by
pinning block size]
Reference
Defeating Nondeterminism in LLM Inference
RFC vLLM IR: Batch Invariance Dispatching in vLLM IR
Perf Optimize batch invariant with fused rms norm, 2 .1% E2 E latency improvement
Kernel Optimize rms_norm kernel
BUG Batch invariance breaks with torch.compile and/or CUDA graphs on SM<90
Bugfix Fix batch invariance in RMSNorm kernels by pinning block size
Bringing HPC Techniques to Deep Learning
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
腾讯技术⼯程
````

## PDF 第 38 页

[原页](RAW.pdf#page=38)

````text
阅读 2 . 2 万
688 篇原创内容
公众号
留⾔
还没有留⾔，来写⾸评
写留⾔
````

