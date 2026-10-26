# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
AI  Infra ⼊⻔⼲货总结：⼤模型是如何⾼效推理的
腾讯程序员 2026 年 5 ⽉ 25 ⽇ 02 : 36⼴东原创 腾讯技术⼯程 626 ⼈
作者： binnnliu
看了很多的⽂章和视频，我以为我理解⼤模型的⼯作原理了，直到看了 vLLM 的代码，我
发现很多地⽅理解的太过表⾯。因此花了⼤概 2 个⽉的业余时间，深⼊阅读了 vLLM 的源
码，本⽂算是对于学习代码的⼀个总结。另外由于当前主流 LLM 都是  Decoder-Only 架
构，本⽂会聚焦 LLM ，不会像⽹络上其他介绍 Transformers 的⽂章从原始论⽂的
Encoder-Decoder 架构讲起。
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
在阅读  vLLM 源码的过程中发现，追踪推理过程中每⼀步的张量维度变化，对于理解⼤模型⼯
作原理⾮常有⽤。因此，本⽂将以  Llama 3 为例，介绍推理过程中的每个计算环节，在每个计
算环节都会标注 Tensor 的维度变化。
我们知道通过批处理可以提⾼ GPU 的利⽤率：本质是提升计算强度，即通过复⽤权重数据来
均摊内存访问开销；⽽减少 Kernel 启动开销与通过海量 warp 充分发挥隐藏延迟仅是随之⽽来
的次要优化。⽽批处理内的请求要步调⼀致，同时开始，同时结束。⽽对于 LLM 这类⽣成式任
务，其核⼼⽭盾在于每个请求的输出序列长度是不可预测且差异巨⼤的。那怎么办呢？
有没有可能将调度的从 request level 下沉到 token level 呢？  恭喜你发明了 continuous
batching 。
那每个请求的 KV Cache 显存申请是不是应该也是 token level ，不要⼀次申请所有的显存。搞
⼀个地址数组 (block table) 来维护每个请求的 KV Cache 地址就好？  恭喜你发明了Paged
Attention 。
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
没错，以上两个概念是当今⼤模型得以⾼性能运⾏的关键。
连续批处理  (Continuous Batching)
在 vLLM 调度器的视⾓中，不存在 Preﬁll 阶段和 Decode 阶段的区分。  每个请求主要关注：
num_computed_tokens ：已经计算过的  token 数（含  Preﬁx Cache 命中的部分）
num_tokens ：该请求当前总共拥有的  token 数（ prompt + 已⽣成的  output ）
每⼀步调度的⽬标就是：让num_computed_tokens追上num_tokens。差多少就调度多少 ——
当然要受限于  token 预算。
调度受 4 个硬性约束限制：
1. 最⼤并发请求数
self.max_num_running_reqs = scheduler_config.max_num_seqs 
2. token budget   单步最多计算多少  token （所有请求之和），控制  GPU 计算量上限
self.max_num_scheduled_tokens = (
    self.scheduler_config.max_num_scheduled_tokens       # 优先⽤这个
    if self.scheduler_config.max_num_scheduled_tokens
    else self.scheduler_config.max_num_batched_tokens    # fallback
)
3. 模型最⼤序列长度
self.max_model_len = model_config.max_model_len
4. 是否还有空闲的 KV Cache blocks
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
如上图所⽰， vLLM 的每轮推理都会基于 token level 调度，后续的执⾏的输⼊都是类似
input_ids 这种打平的 token 数组，即 Flattened 。 ( 这⾥的调度逻辑是在 Tokenize 之后 , 本⽂后续
的 num_sched_tokens 都对应上图中的 total_num_scheduled_tokens)
Paged Attention
vLLM 启动时会申请显存  kv_cache shape 为：[num_layers, 2, num_blocks, block_size, num_kv_
heads, head_dim]，每⼀层 key_cache 和 value_cache 的 shape 都是[num_blocks, block_size, nu
m_kv_heads, head_dim]。
block_table 会记录每个请求分配到的物理块 ID ， shape 为[max_num_reqs, max_num_blocks_pe
r_req]，请求 0 分配了块[5, 8, 12]，请求 1 分配了块[3, 7]
⽽推理过程中，通过 slot_mapping 告诉 kernel 把新产⽣的  KV 写到哪个  slot ，通过 block_table
告诉  kernel 去哪些物理  block 读取  KVCache 。
# slot_idx 对应 token 对应的最终存储位置 :  slot_idx = block_idx * block_size + block_offset
const int64_t slot_idx = slot_mapping[token_idx]; 
const int64_t block_idx = slot_idx / block_size;     // 计算块索引
const int64_t block_offset = slot_idx % block_size;  // 计算块内偏移
为什么   slot_mapping  和   block_table  不需要   num_layers  维度？如果⼀个请求的第  25
个  Token 被分配到了物理块  ID 为   8 的位置，那么在模型的第  0 层到第  31 层，这个
Token 的  KV 值都会被存储在物理块   8 的相同位置。
⽐如：block_size = 16（每个块存储 16 个 token ） , 请求 0 的 block_table 为： [5, 8, 12] ，
token 位置为 25 ，计算过程：
1. block_idx = 25 // 16 = 1 （属于第 1 个虚拟块）
2. block_idx = block_table[0, 1] = 8 （从页表查找物理块 ID ）
3. block_oﬀset = 25 % 16 = 9
4. slot_idx = 8 * 16 + 9 = 137
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
PagedAttention 的虚拟页表机制解决了显存碎⽚的问题，极⼤地提升了  GPU 的显存利⽤率，
是⽀撑  Continuous Batching ⾼性能推理的基础。
然⽽ PagedAttention 引⼊的  block_table 间接寻址机制，打破了⼀个请求在物理显存上的绝对
连续性。当  Attention Kernel 跨越  block 读取历史  KVCache 时，会触发离散访存
（ Uncoalesced Access ），这在底层对  Memory Controller 是⾮常不友好的，同时也会导致
L2 Cache 的命中率下降，带来⼀定的带宽折损。当然，系统设计从来都是  Trade-oﬀ 。
vLLM 通过设置合理的  block_size （默认通常是  16 ）来缓解这个问题：在⼀个  block 内部的
16 个  Token 的物理显存依然是连续的，能够保证⾼效率的合并访存。相⽐于因显存碎⽚导致
的 OOM ，牺牲少部分的访存带宽换取整个系统吞吐量（ Throughput ）的⼤幅跃升，在  LLM
推理的整体逻辑中是划算的。
LLM 推理流程
Tokenize
对⽤户输⼊提⽰词进⾏分词并转换为数字表⽰。⽬前主流  LLM ⼏乎全部使⽤  BPE（ Byte
Pair Encoding ）。
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
BPE 的词表训练⽅式如下：
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
Embedding Lookup
Embedding Lookup 本质上是⼀个查表操作，它将⼀维的  Token ID 数组[num_sched_tokens]
直接转化为   [num_sched_tokens, hidden_size] 的特征矩阵，作为进⼊⼤模型真正意义上的数学
输⼊。
理论实现
⽬标矩阵计算公式输⼊     维
度
权重矩阵  
  维度 输出结果维度备注
Embeddin
g
[batch_siz
e, seq_le
n]
[V, hidde
n_size]
[batch_size,
seq_len, hidd
en_size]
本质是索引取
值，⽽⾮矩阵
乘法
vLLM 中的实现
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
⽬标矩阵计算公式输⼊    
维度
权重矩阵  
  维度 输出结果维度备注
Embeddin
g
[num_sched
_tokens]
[V, hidden
_size]
[num_sched_toke
ns, hidden_siz
e]
Flattened
布局
将  Batch 中所有请求的有效  Token 拼接为⼀维长向量，彻底消除  Padding 。
Transformer Block
Attention Module ( 以标准 GQA + RoPE 为例 )
RMSNorm
为了保证⼤模型在神经⽹络中的数值稳定性，必须引⼊特征归⼀化（ Normalization ）机制。
与传统  LayerNorm 要求同时缩放与平移不同，为了提升计算效率，现代⼤模型⼴泛为采⽤了
RMSNorm ：砍掉平移操作，仅沿特征维度对数据进⾏尺度缩放，能够有效防⽌前向传播中的
⽅差膨胀与硬件数值溢出，从⽽极⼤缓解反向传播时的梯度异常（消失或爆炸）问题，为深层
⽹络的稳定训练提供基础保障。
⽬标矩阵计算公式输⼊     维度
权重
维
度
输出结果维度备注
RMSNor
m
[num_sched_
tokens, hid
den_size]
[hidden_
size]
[num_sched_
tokens, hid
den_size]
  是⼀维向量⽽⾮
矩阵，做的是逐通
道缩放⽽⾮  GEM
M
Q/K/V Linear Proj - Fused QKV
⽬标矩阵计算公式输⼊  X 维度 权重矩阵  
  维度 输出结果维度备注
Fused QK
V
[num_sched_
tokens, hid
den_size]
[hidden_si
ze,qkv_pro
j_size]
[num_sched_t
okens, qkv_p
roj_size]
权重按列拼
接，执⾏单次
宽矩阵  GEMM
4096 (Q) + 102
4 (K) + 1024 (V)
= 6144
Reshape & Cache
⽬标矩阵 Q, K, V Slice RoPE( 维度
不变 ) Multi-Head Reshape 备注
Query ( ) [num_sched_token
s, hidden_size]
[num_sched_tokens,num
_heads,head_dim]  前  4096 列
Key ( ) [num_sched_token
s, kv_channels]
[num_sched_tokens,num
_kv_heads,head_dim]  中间  1024
列
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
⽬标矩阵 Q, K, V Slice RoPE( 维度
不变 ) Multi-Head Reshape 备注
Value ( ) [num_sched_token
s, kv_channels]
[num_sched_tokens,num
_kv_heads,head_dim]  最后  1024
列
注： 是⼀个块对⾓旋转矩阵，实际实现中通过元素级  sin/cos 运算避免矩阵
乘法。
这个阶段的⼤概流程：  QKV 按列拆分  -> 对 Q 、 K 进⾏ RoPE 计算  -> Q 、 K 、 V Reshape 多头视
⾓   -> 然后 reshape_and_cache 按照 slot_mapping Scatter 写⼊ Paged KVCache 。
RoPE 的核⼼思想就是：⽤旋转的⾓度来代表  Token 的位置。  虽然不是矩阵乘法， sin/cos 属
于超越函数，在  GPU 上由  SM 内的特殊函数单元（ SFU, Special Function Unit ）执⾏。 SFU
的吞吐量通常仅为  FP32 ALU 的  1/4 。所以 VLLM 中不在  RoPE kernel 实时计算 sin/cos ，⽽是
引擎初始化时按模型配置预计算好  cos_sin_cache ， shape 为  [max_position_embeddings,
rotary_dim] 。  RoPE kernel 运⾏时按  positions 索引出对应的  cos/sin ⾏，与  Q/K 做逐元素乘
加即可。本质是⽤⼀份⼩表（典型⼤⼩⼏  MB 到⼏⼗  MB ）换掉每次  forward ⼏百万次的
sin/cos 调⽤ —— 经典的空间换时间  / 访存换算⼒。
Attention (FlashAttention, Scaled Dot-Product Attention)
  读取请求对应  KV Cache 进⾏
FlashAttention 计算。
感觉 Attention 的逻辑是整个 LLM 推理最复杂的地⽅了：
1. Attention 的数学逻辑并不复杂，但是为了提升计算强度，打破内存墙，业界在这⾥做了⾮
常多的优化，⽐如 FlashAttention ；
2. 其他阶段基本都是 Token 维度打平的，⽽ Attention 计算必须要在请求维度进⾏运算。
特别注意 : 在进⼊ Attention kernel 之前，需要从全局 Flattened 视⾓[num_sched_tokens, ...]切
换到请求维度视⾓[batch_size, ...]。这是因为 Attention 计算本质上是请求内部的操作，不同请
求的 KV Cache 不能交叉。 vLLM/FlashAttention 通过cu_seqlens（累积序列长度）数组来实现
这种变长序列的请求级隔离，⽽⽆需真正 Reshape 为[batch_size, ...]的规整张量。  这⾥的 K 和
V Shape 算⼦逻辑上为[batch_size, num_kv_heads, seq_len, head_dim]，⽽不同请求的 seq_len
肯定不⼀致。实际上在 cuda 算⼦层已经确保了不同请求不会分配到同⼀个  thread block ，即
保证这⾥的运算是请求维度隔离的。
Softmax 的核⼼原理可以⽤⼀句话概括：将⼀组任意的实数（通常称为  Logits ），转化为
⼀套总和为  1 的概率分布，同时放⼤差异。 ps: 这⾥的为 head_dim 。
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
K 的 Shape 为[seq_lens, num_kv_heads, head_dim]，包含当前请求所有历史的 KCache ，
seq_lens 是所有历史 KV 对应的 Token 长度，但物理上，由于 Paged Attention 机制，这些历史 K
Cache 并⾮连续存储，⽽是离散分布在 HBM 的物理块中（即底层实际 Shape 为 [num_blocks,
block_size, num_kv_heads, head_dim] ）。 Kernel 在执⾏时，会通过  block_table 动态间接寻
址，在⽚上 SRAM 中将其拼凑为逻辑上的连续序列参与计算。
V的 Shape 为[seq_lens, num_kv_heads, head_dim]，包含当前请求所有历史的 VCache
Q的 Shape 为[query_lens, num_heads, head_dim]， query_lens 是本次 Q 对应的 Token 长度
操作名称 数学公式 逻辑说明  / ⽬的
GQA 分组共
享
1 KV Head 映射
给  4 Q Head
把 KV 的 Shape 从[seq_lens, num_kv_heads, head_dim]变
为[seq_lens, num_heads, head_dim]
逻辑上等价于将 1 个 KV Head 的数据⼴播给 4 个 Q Head ；物理实现
中通过索引映射 kv_head_idx = q_head_idx // (num_heads // num
_kv_heads) 避免显存复制。
Q-K Dot Pro
duct
查询 Query 和该请求所有 Key 的点积，注意⼒原始分数。 ->[query
_lens, num_heads, seq_lens]
Scale 对原始分数进⾏数值缩放（  为向量维度），防⽌  Softmax 函数进
⼊梯度极⼩的区域。
Mask 注⼊因果逻辑，通过加上掩码矩阵   （通常将未来位置设为  
），阻⽌模型 “ 看到 ” 未来的信息。
Softmax 将处理后的分数转化为总和为  1 的注意⼒权重（概率）。 ->[quer
y_lens, num_heads, seq_lens]
MatMul
根据注意⼒权重     对值向量（ Value ）进⾏加权求和，得到最终的
输出特征表⽰。
V的 Shape 为[seq_lens, num_heads, head_dim]   -> [que
ry_lens, num_heads, head_dim]
Attention 的数学逻辑⾮常清晰，但在⼤模型推理（尤其是长⽂本  Preﬁll 阶段）中，如果严格
按照数学公式分步执⾏，会在  GPU 的  HBM （全局显存）中产⽣庞⼤的中间矩阵  （注意⼒
分数）和  （ Softmax 概率），其    的内存访问量会严重影响性能，即所谓的内存墙问
题。
为了打破这个瓶颈， vLLM 默认采⽤  FlashAttention 及其变体（如  Flash-Decoding ）。
FlashAttention 的核⼼思想是  Kernel 融合  (Kernel Fusion) 与  分块计算  (Tiling) 。但分块计算⾯
临⼀个致命的数学障碍： Softmax 操作需要知道全局的最⼤值和指数和才能计算，这通常要求
完整的中间矩阵驻留在显存中。 FlashAttention 巧妙地引⼊了  Online Softmax  算法，通过维
护局部的当前最⼤值（ Running Max ）和当前指数和（ Running Sum ），并在读⼊新块时利⽤
动态缩放因⼦（ Rescaling Factor ）对旧结果进⾏修正。
正是凭借  Online Softmax ， FlashAttention 成功解除了全局数据依赖，将从  Q-K 点积、
Softmax 到乘  V 的整个逻辑步骤，融合成了⼀个单⼀的  CUDA Kernel 。在物理执⾏上，它⼀
块⼀块地在  SRAM 中完成计算，彻底避免了将庞⼤的中间矩阵     和     读写  HBM ，从⽽⼤幅
打破了内存墙限制。
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
Preﬁll 阶段， seq_lens 和  query_lens 都是 num_prompt_tokens 。当前  Prompt 计算出的  KV
向量先被  reshape_and_cache_ﬂash 按  slot_mapping 写⼊  Paged KV Cache ，随后  attention
kernel 通过 block_table 从  cache 中读取  K/V 完成本层  attention 计算；这份写⼊同时也作为
该序列的  KV Cache ，供后续  decode 步骤复⽤。
Decode 阶段， seq_lens 为已计算的历史  token 总数，  query_lens 为 1 。
vLLM v0 中 preﬁll 和 decode ⾛两条独⽴分⽀： preﬁll 通过   attn_metadata.is_prompt == Tru
e 调   flash_attn_varlen_func， kernel 直接读临时的物理上连续的 HBM buﬀer ⾥的  K/V ，
不读  cache ； decode ⾛   paged_attention_v1/v2， K/V 全部从  cache 读。 v1 把两路统⼀
成⼀次   flash_attn_varlen_func 调⽤， K/V 全部⾛  paged cache + block_table ，代价是
preﬁll 多⼀次 " 写  cache →  读  cache" 的间接寻址，换来对  preﬁx cache / chunked preﬁll
的天然⽀持。只有 v0 版本  FlashAttention 不读 KV Cache ，因为  v0 没有  preﬁx cache /
chunked preﬁll 。
V1 中即便某些  backend （如  FlashInfer 、 MLA-sparse ）把混合  batch 物理拆分成 preﬁll /
decode 两个独⽴  kernel 调⽤ ,preﬁll 仍然从  paged cache 读  K/V - 因为  v1 需要⽀持
preﬁx cache 和  chunked preﬁll 。
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
对⽐ Preﬁll 和 Decode ，可以发现：
Preﬁll 阶段： QKV_Proj 、 Attention 、 O_Proj 、 MLP 本质上都是稠密矩阵乘法（ GEMM ），
其实就是通过请求内 token-level 计算复⽤模型权重，因此算术强度极⾼，使得  GPU 在
Preﬁll 阶段主要受限于  Tensor Cores 的物理算⼒峰值，属于计算密集型（ Compute-
bound ）。
Decode 阶段：由于⾃回归特性，每次只处理⼀个  Token （query_lens = 1），若⽆优化，
此时 QKV_Proj 、 Attention 、 O_Proj 、 MLP 全都退化为矩阵向量乘法（ GEMV ）。虽然计算
量不⼤，但需要把巨⼤的  KV Cache 和模型权重  从  HBM 搬运到  SRAM ，⾮常吃显存带
宽，因此 Decode 阶段是典型的访存密集型（ Memory-bound ）。
⽽  Continuous Batching 的价值在于在 Preﬁll 实现请求内复⽤模型权重的基础上，进⼀步通过
token-level 的调度让多个请求复⽤模型权重，将  QKV_Proj 、 O_Proj 、 MLP 重新变回矩阵乘
法，极⼤地摊薄了读取权重的显存开销。
但是 Attention 则⽐较特殊，由于每个请求必须读取⾃⼰独占的  KV Cache （⽆法跨请求共
享），⽽且 Decode 每次只处理⼀个  Token ， Attention 计算始终⽆法均摊访存开销。此外，由
于当前  Query 必须与所有历史  Key/Value 交互，哪怕有 KVCache 的存在，其计算与访存量也
是随着上下⽂长度     呈     线性膨胀。这⾥特别注意其实 Preﬁll 阶段每次处理
num_prompt_tokens 个 Token ， Attention 计算是可以均摊访存开销的。
ps: 所以其实我们⽇常所说的 Preﬁll 是 Compute-bound ， Decode 是 Memory-bound ，主要是基
于  1. 从  HBM 读取模型权重的访存摊销，  2. 从  HBM 读取模型 KV 的访存摊销。
Multi-Head Concatenation
操作名称 逻辑说明vLLM 输⼊维度输出结果维度备注
Concat / Fl
atten
消除多头维
度，恢复隐藏
层维度
[num_sched_to
kens, num_hea
ds, head_dim]
[num_sched_
tokens, hid
den_size]
物理内存通常已经是连续
的，这⾥本质上是⼀个改变  T
ensor View 的操作。  (hidden
_size = num_heads * head_d
im)
O_Proj - 线性融合  (Output Projection)
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
⽬标矩阵计算公式输⼊  
维度
权重矩阵  
  维度
输出结果维
度 备注
O_Proj
[num_sched
_tokens, h
idden_siz
e]
[hidden_si
ze, hidden
_size]
[num_sched
_tokens, h
idden_siz
e]
跨  Head 的信息交
互与融合。这也是
⼀次标准的稠密矩
阵乘法（ GEMM / G
EMV ）。
Residual Connection
不要推翻重来，⽽是在原有的基础上学习 “ 修正值 ” （ Delta ）。如果没有  ResNet 证明⽹络可以堆
到  100 层以上且不梯度消失，后来的  BERT (24 层 ) 和  GPT (96 层 +) 根本不敢设计得那么深。
它是 “Scaling Law” 在架构上的物理基础。
⽬标矩阵计算公式输⼊  
  维度
输⼊  
  维度
输出结果维
度 备注
Residual
Add
[num_sched
_tokens, h
idden_siz
e]
[num_sched
_tokens, h
idden_siz
e]
[num_sched
_tokens, h
idden_siz
e]
  是进⼊这⼀层  RMS
Norm 之前的原始输
⼊。将注意⼒机制提
取的新特征 “ 加回 ” 主
⼲数据流中。
实际 vLLM 中， Residual Add 会和下⼀步的 RMSNorm 融合成⼀个  CUDA kernel 。
FFN
RMSNorm
对     再进⾏⼀次归⼀化。在  vLLM 中，通常与上⼀层残差相加（ Residual Add ）融合，减少
HBM 读写。
Gate_Proj & Up_Proj
通常  intermediate_size 是  hidden_size 的  4 倍左右  ( 或  8/3 倍 ) 。
⽬标矩阵计算公式 输⼊  X 维度 权重  W 维度 输出维度
Gate Proj
[num_sched_toke
ns, hidden_siz
e]
[hidden_size, i
ntermediate_siz
e]
[num_sched_token
s, intermediate_s
ize]
Up Proj
[num_sched_toke
ns, hidden_siz
e]
[hidden_size, i
ntermediate_siz
e]
[num_sched_token
s, intermediate_s
ize]
vLLM ⼯程实现（ Fused Gate/Up ）
为了减少  GPU 核函数启动（ Kernel Launch ）次数并充分利⽤内存带宽， vLLM 在加载模型时
会将     和     按列拼接。这样原本两次中等规模的矩阵乘法，就变成了⼀次宽矩阵
GEMM 。
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
⽬标矩阵 计算公式 输⼊  X 维度 权重  Wgate_up
维度 输出维度
Fused Gat
e/Up
[num_sched_tok
ens, hidden_si
ze]
[hidden_size, 2
*intermediate_s
ize]
[num_sched_token
s, 2*intermediat
e_size]
Activation
SiLU(Gate) * Up。 vLLM 使⽤   silu_and_mul kernel 在⽚上（ SRAM ）直接输出点乘结果，极
⼤节省了显存带宽。
操作名称 数学公式 物理实现说明
Slice & Act   为     前⼀半，  为后⼀半。
Down_Proj
⽬标矩阵计算公式 输⼊     维度 权重     维度 输出结果维度
Down Pro
j
[num_sched_token
s, intermediate_
size]
[intermediate_s
ize, hidden_siz
e]
[num_sched_toke
ns, hidden_siz
e]
Residual Connection
x = x + FFN_Output
class LlamaMLP(nn.Module):
    def __init__(self, config):
        super().__init__()
        # 通常  intermediate_size 是  hidden_size 的  4 倍左右  ( 或  8/3 倍 )
        self.gate_proj = nn.Linear(self.hidden_size, self.intermediate_size, bias=False)
        self.up_proj   = nn.Linear(self.hidden_size, self.intermediate_size, bias=False)
        self.down_proj = nn.Linear(self.intermediate_size, self.hidden_size, bias=False)
        self.act_fn = nn.SiLU()
    def forward(self, x):
        # 1. Gate 和  Up 分别进⾏  Linear 变换
        # 2. Gate 经过  SiLU 激活
        # 3. 两者相乘  (Element-wise multiplication) -> 这就是  GLU (Gated Linear Unit)
        # 4. 最后经过  Down 投影回原维度
        return self.down_proj(self.act_fn(self.gate_proj(x)) * self.up_proj(x))
LM Head
将隐藏层特征映射到整个词表空间，输出未归⼀化的原始得分，即  Logits。
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
在前⾯的  Transformer Block 中， Preﬁll 阶段的   num_sched_tokens  是所有  Prompt 长度的总
和。但实际上 vLLM LM Head 只需要每个请求序列的最后⼀个  Token 的特征⽤来预测下⼀个
词，因此进⼊ LM Head 前会执⾏⼀次  Gather 操作。（ Speculative Decoding 、
prompt_logprobs 除外）
但是 vLLM 中最后⼀层还是⽼⽼实实把所有  query_lens 都算了⼀遍，本质上是⼯程与物理极限
的  Trade-oﬀ 。
RMSNorm
最后再来⼀次归⼀化（防⽌数值过⼤）。
Linear (LM Head)
⽬标矩阵计算公式输⼊  
  维度
权重矩阵  
  维度
输出结果
维度 备注
LM Head
[num_req
s, hidden
_size]
[hidden_s
ize, voca
b_size]
[num_req
s, vocab_
size]
num_reqs
  即当前  Batch 中的请求
数量。
以  Llama-3-8B 为例，vo
cab_size  ⾼达  12825
6 ，这是⼀个极庞⼤的矩
阵， vLLM 通常会使⽤张
量并⾏（ TP ）按列切分
该权重以加速计算。
Sampling
保存原始  Logprobs
如果⽤户请求了  logprobs （对数概率）， Sampler 会在任何处理之前，先对原始  logits 做⼀
次   log_softmax  快照保存。这样返回给⽤户的概率分布反映的是模型的真实输出，不受后续
penalties / temperature 等采样参数的⼲扰。
更近⼀步， Preﬁll 阶段 Transformer Block 的最后⼀层， attention 输出是
[num_sched_tokens, hidden_dim] ，但实际上只需要最后⼀个  token 的  hidden_state 来
做  logits 计算（因为之后没有更多的  layer 需要完整的  hidden_states 了）。所以理论上最
后⼀层的 MLP （以及  LayerNorm ）可以只对需要采样的  token 计算，节省⼤量计算。如
果只需要最后⼀个  token 的⽣成结果，那么在最后⼀层（ Last Layer ）：
1. 必须要算的部分：所有  token 的     和  （因为这层的  KV cache 要存下来，供后续
Decode 阶段使⽤）。
2. 理论上可以只算最后⼀个  token ： 的投影、 Attention 的计算（其实退化成了
Decode 阶段的  Flash-Decoding 计算）、 LayerNorm 、以及庞⼤的  MLP 。
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
  {                                                                                       
    "token": "Hello",          // 实际被选中的  token
    "logprob": -0.01523,       // 该  token 的对数概率  (log_softmax 的结果 )                  
    "bytes": [72, 101, ...],   // token 的  UTF-8 字节表示    
    "top_logprobs": [          // 概率最⾼的前  N 个  token ( ⽤户通过  logprobs=N 指定 )
      {
        "token": "Hello",
        "logprob": -0.01523    // ln(0.985) ≈ -0.015, 即  98.5% 概率
      },
      {
        "token": "Hi",
        "logprob": -4.32185    // ln(0.013) ≈ -4.32, 即  1.3% 概率
      }
    ]
  }
Logits Process
在得到原始  Logits 后、进⾏  Softmax 概率转化前，会经过⼀系列后处理操作，⽤于⼲预最终
的⽣成结果：
⽩名单过滤
结构化输出（ JSON schema ）：配合  grammar bitmask ，每⼀步动态计算当前合法的
token 集合。
情感分类：只允许输出   "positive" /  "negative" /  "neutral"  对应的  token 。
多选题：只允许输出   A B C D。
⿊名单过滤
Non-argmax-invariant Logit Processors
Repetition Penalty ( 重复惩罚 ): 根据历史  Token ，对已⽣成过的词汇扣除分数，防⽌模型变
成 “ 复读机 ” 。
采样
每个请求的采样策略可以是Greedy 或 Random ，由⽤户设置的   temperature  决定
@cached_property
def sampling_type(self) -> SamplingType:
    if self.temperature < 1e-5:       # < 0.00001 就是  greedy
        return SamplingType.GREEDY
    return SamplingType.RANDOM
1. Greedy 先⾏：在  temperature 缩放之前，先对当前  logits 执⾏⼀次   argmax，保存为   gre
edy_sampled。
````

## PDF 第 17 页

[原页](RAW.pdf#page=17)

````text
如果整个  batch 全是  greedy（所有请求的   ），到这⾥就直接返回，后续步骤全部跳
过。
这⼀步必须在  temperature 之前做，否则  greedy 请求的  logits 会被不必要地除以
temperature 导致精度损失。
2. Temperature Scaling ：Logits = Logits / Temperature。
3. Argmax-invariant Processors （如  min_p ）：
min_p 是⽬前唯⼀的  argmax-invariant 处理器。其规则为：概率不到 token 最⾼概率的
min_p 倍的  token ，全部淘汰。 > 公式：阈值  =  ，低于阈值的  token 得分设
为   。
模型很确定时（）：阈值  = 0.09 ，砍得多，⼏乎只剩最优解。
模型不确定时（）：阈值  = 0.008 ，砍得少，保留充分的探索空间。
4. Top-K 截断：只保留分数最⾼的     个  Token ，其余得分全部设为   。
5. Top-P  Masking ：按分数从⾼到低排序并累加  softmax 概率，保留累积概率刚好超过  
 的前若⼲  Token ，尾部  Token 得分设为   。
6. Softmax + Gumbel-Max 采样    确保结果的随机性          公式：   ，其中
Gumbel-Max ⽤加噪求最⼤值替代了传统的轮盘赌算法。它将原本需要串⾏计算前缀和的
采样过程，转化为完全独⽴的  element-wise 并⾏运算，打破了超⼤词表下的全局数据依
赖。
: 拉⼤分数差距。⾼分越明显，低分被压得更低。模型变得保守、确定。
: 缩⼩分数差距。分布趋向均匀。模型变得随机、有创造⼒（但也容易胡说⼋
道）。对于   的  greedy 请求，此处会⽤     跳过除法（避免除以零），它
们的最终结果由  Step 1 的   greedy_sampled  决定。
⽰例（min_p = 0.1， ，阈值  = 0.04 ）：
min_p 的核⼼价值在于⾃适应：最⾼概率的  token ⾃⾝永远不会被砍（因为  
），所以  argmax 结果不变。
````

## PDF 第 18 页

[原页](RAW.pdf#page=18)

````text
probs = logits.softmax(dim=-1) 
q.exponential_()
probs.div_(q).argmax(dim=-1)
7. 最终选择：逐请求按  temperature 决定使⽤哪个结果
 final = where(temperature < 1e-5,
            greedy_sampled,    # 该请求⽤贪⼼结果
            random_sampled)    # 该请求⽤随机结果
output 得到   Next Token ID，并将其追加到  Input 序列中，进⼊下⼀轮循环。
总结
是的，戛然⽽⾄。本⽂主要讲述了经典的⼤模型推理的全流程，想要真正理解⼤模型的推理流
程理解 shape 的变化真的很重要。笔者有意克制发散的思维，专注整个推理流程，很多的原理
和概念都没有提。后续可以围绕这个基础展开，
⽐如数学基础： Softmax 、 RMSNorm 原理、 RoPE
⽐如 Attention 计算遇到了内存墙问题
导致了  DeepSeek MLA/DSA 、线性注意⼒等的产⽣，本质是减少 KVCache 的读取；
导致了 FlashAttention 的产⽣的，本质上是利⽤ IO Aware 、重计算提升计算强度；
⽐如为什么要 MoE  scaling law 模型不断增⼤，计算量随参数线性增⼤，⽽参数占⽐的⼤头⼜
在 MLP 层，那就把 MLP 层拆分，美其名⽈不同专家，每次执⾏仅激活部分参数 , 其本质就是将
现有 FFN 层拆分成多个，然后增加路由，每次可以激活不同专家组。
⽐如模型太⼤了， TP 、 PP 、 DP 、 EP 、 SP 、 CP ，了解了本⽂的数据流 shape 变化， TP 理解就
变的相当容易。
Column Parallelism ( 列切分 ) ： Fused QKV 和  FFN 的  Fused Gate/Up 都是列切分。例
如  QKV 的权重维度在单卡上会变成   [hidden_size, qkv_proj_size / TP_size]，输出也相应变
成   [num_sched_tokens, qkv_proj_size / TP_size]。
Row Parallelism ( ⾏切分 ) ： O_Proj 和  FFN 的  Down_Proj 是⾏切分。权重变为   [hidden_
size / TP_size, hidden_size]。计算完成后，通过   AllReduce  算⼦来聚合跨卡结果。
````

## PDF 第 19 页

[原页](RAW.pdf#page=19)

````text
⽐如长上下⽂时，  chunked preﬁll 到  Flash-Decoding 到  SP 本质是不同维度的 prompt 的拆
分，不过是在解决不同问题， chunked preﬁll 避免超长  Prompt 的新请求影响其他请求，⽆论
是正在处理的  decode 请求还是待处理的其他  preﬁll 请求，  Flash-Decoding 通过  KV 维度的
切块（ Split-K ）提升了  Decode 阶段的  SM （流处理器）利⽤率， SP (Sequence Parallelism)
则是解决单卡显存塞不下超长上下⽂的问题。（ Flash-Decoding ， Sequence Parallelism 靠
Log-Sum-Exp 实现跨  SM 或者跨卡的归⼀化）
再来感叹⼀句，单从推理来看，⼤模型的原理其实真没那么⾼深莫测，最难的数学公式怕是要
数 RoPE 了。但是 AI Infra 的东西真的多～～  根本学不完，不像 agent ⽅向整天重命名上下⽂⼯
程 🐶 。（提⽰词⼯程、 function calling 、  rag 、 mcp 、 memory 、 agent 开发、 skills 、
openclaw 、上下⽂⼯程、 harness ⼯程、 hermes ）
附 1 ：模型配置参数
标准变量名 数值  (Llama-3-
8B) 物理含义说明
hidden_size 4096 隐藏层总维度，也是  Q 向量的总宽度。
num_heads/num_q_head
s 32 Query 的头数。决定了注意⼒机制的并⾏度。
num_kv_heads 8 Key/Value 的头数。 GQA 架构中⽤于压缩缓存。
head_dim/head_size 128 单个头的维度。公式     中的   。
kv_channels/kv_dim 1024 单侧（ K 或  V ）矩阵的总宽度  (num_kv_heads*he
ad_dim) 。
qkv_proj_size 6144 Fused QKV 层的输出总宽度  (hidden_size + kv
_channels*2) 。
intermediate_size 14336 FFN 内部升维后的维度（通常为   ）。
fused_ﬀn_size/gate_up_p
roj_size 28672 Fused Gate/Up 层的输出总宽度  (intermediate_
size*2) 。
````

## PDF 第 20 页

[原页](RAW.pdf#page=20)

````text
标准变量名 数值  (Llama-3-
8B) 物理含义说明
vocab_size 128256 词表⼤⼩。决定了  LM Head 的输出矩阵尺⼨。
num_hidden_layers 32 Transformer Block 的层数。
rope_theta 500000.0 RoPE 旋转位置编码的  base theta 值。
附 2 ：推理运⾏时变量
标准变量名 数值  (Llama-3-8
B) 物理含义说明
num_prompt_tokens 100 prompt 长度
num_tokens 105 prompt + 已⽣成  output
num_computed_tok
ens 105 已计算的历史  token 总数
num_sched_tokens 1 本次要计算  1 个新  token （ decode ），其实就是 ﬂatten
的 query_lens
seq_lens 106 KV Cache 总长度  = 105 + 1
query_lens 1 本次  Q 的长度
附 3 ：推理运⾏时变量
LLM 是有多层的，以Llama3 8B为例模型的权重组成如下：
组件 权重名称 参数量维度占⽐ 本质与说明
Embedding embed_tokens.weig
ht
[128256, 4
096] ~6.5% 查表矩阵
Attention q_proj
[4096, 409
6]
 (×32 层 )
~15.9%
4 个  Linear 矩阵，⽆  bias
。  由于  GQA ， K/V 矩阵⽐
Q ⼩很多。
k_proj, v_proj
[1024, 409
6]
 (×32 层 )
o_proj
[4096, 409
6]
 (×32 层 )
MLP gate_proj, up_pro
j
[14336, 40
96]
 (×32 层 )
~70.1%
3 个  Linear 矩阵，⽆  bias
， SwiGLU 激活。  这是模型
计算和参数量的绝对⼤头。
down_proj
[4096, 143
36]
 (×32 层 )
Input Norm input_layernorm.w
eight
[4096]
 (×32 层 ) < 0.01% RMSNorm 缩放⼀维向量。
````

## PDF 第 21 页

[原页](RAW.pdf#page=21)

````text
组件 权重名称 参数量维度占⽐ 本质与说明
Post-Attn N
orm
post_attention_la
yernorm.weight
[4096]
 (×32 层 ) < 0.01% RMSNorm 缩放⼀维向量。
Final Norm norm.weight [4096]
 (×1) < 0.01% 最终进⼊  LM Head 前的  RM
SNorm 向量。
LM Head lm_head.weight[128256, 4
096] ~6.5% 与  Embedding 维度⼀致，
但独⽴存在不共享。
MLP 层：参数占⽐  70% ，FLOPs  占⽐也约  70% ，是绝对的计算⼤头。
Attention 层：参数占⽐仅  16% ，但由于需要读取动态⽣长的  KV Cache ，它是访存带宽
的绝对⼤头。
附 4 ： vLLM 调度详细流程
````

## PDF 第 22 页

[原页](RAW.pdf#page=22)

````text
````

## PDF 第 23 页

[原页](RAW.pdf#page=23)

````text
````

## PDF 第 24 页

[原页](RAW.pdf#page=24)

````text
抢占（ Preemption)
当  KV Cache blocks 不够分配时，调度器会抢占最低优先级的  RUNNING 请求—— 释放其全
部  KV Cache 、将   num_computed_tokens  重置为  0 、放回  WAITING 队列。被抢占的请求下次
被调度时需要重新从头  Preﬁll。
def _preempt_request(self, request, ...):
    self.kv_cache_manager.free(request)       # 释放  KV Cache
    request.status = RequestStatus.PREEMPTED
    request.num_computed_tokens = 0           # 重置，下次需要重新计算
    self.waiting.prepend_request(request)     # 放回等待队列
为什么  RUNNING 阶段分配失败会抢占，⽽  WAITING 阶段直接终⽌？
这体现了调度器的核⼼原则：已在运⾏的请求优先级⾼于等待中的请求。
RUNNING 请求：已经占⽤了  KV Cache 、消耗了计算资源。如果因为内存不⾜⽆法继
续，调度器会牺牲优先级最低的  RUNNING 请求（释放其  KV Cache ）来保证其他请求能
继续推进。这是值得的，因为放弃⼀个已运⾏的请求代价很⾼。
v0 时代， vLLM 有两种  preemption 策略：
SWAP：把被抢占请求的  KV blocks 从  GPU HBM 搬到  host RAM 暂存，资源宽裕时
再  swap in 回  GPU 。
RECOMPUTE：直接释放  GPU blocks ，重新加⼊  waiting 队列⾛ preﬁll 重算⼀遍。
v1 把  SWAP 路径完全砍掉（LLM(swap_space=...)  已废弃并  warn ），Scheduler._preempt
_request  只保留  RECOMPUTE ⼀条路。原因：
PCIe 双向搬运  + host RAM 占⽤的开销，在  FA + ⼤  batch 下常常⽐重算⼀次  preﬁll
还贵
chunked preﬁll 让重算可以分多步 " 追上来 " ，摊平开销
架构上少⼀条路径， preﬁx caching / chunked preﬁll /continuous batching 的交互更
⼲净
````

## PDF 第 25 页

[原页](RAW.pdf#page=25)

````text
WAITING 请求：还没开始计算，没有沉没成本。如果内存不⾜，直接停⽌调度即可，下
⼀个  step 再尝试。
为什么抢占后跳过  WAITING 调度？
发⽣抢占意味着  KV Cache 已经⾮常紧张。此时不应该再引⼊新的  WAITING 请求，因为那会
进⼀步加剧内存压⼒，可能触发更多抢占，形成恶性循环。
Reference
Attention Is All You Need
Efficient Memory Management for Large Language Model Serving with PagedAttention
Orca: A Distributed Serving System for Transformer-Based Generative Models
Flash-Decoding for long-context inference
SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills
FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness
FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning
FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision
FlashAttention-4: Algorithm and Kernel Pipelining Co-Design for Asymmetric Hardware Scaling
AI and Memory Wall
How GPU Computing Works | GTC 2021
Roofline: an insightful visual performance model for multicore architectures
KV Caching in LLMs, explained visually
彻底搞懂 KV 缓存
KV Caching in LLMs, Clearly Explained
Neural Machine Translation of Rare Words with Subword Units
````

## PDF 第 26 页

[原页](RAW.pdf#page=26)

````text
阅读 2 . 4 万
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
留⾔
还没有留⾔，来写⾸评
写留⾔
````

## PDF 第 27 页

[原页](RAW.pdf#page=27)

````text
````

## 采集与转写核验记录（非原文）

以下说明由本次核验添加；上方逐页文本保持文本层原样，图片与布局以PDF为准。

- PDF物理页 11,12,17：p.11、12、17 各有图片加载占位，相关原图未保存；原 complete_with_limits 判定不成立，已改为 incomplete。笔记仅据可见文字与已保存图像说明。
- PDF物理页 22,23,24,26,27：p.22、27 为整页空白，与图片加载占位不同；p.26 是公众号结尾。p.23–24 跨页调度图已放大阅读。
- PDF物理页 14,16,18：代码片段只是示意：p.14 类示例未完整初始化所用属性，p.16 JSON 样例含注释/省略号；未执行或验证可运行性。
