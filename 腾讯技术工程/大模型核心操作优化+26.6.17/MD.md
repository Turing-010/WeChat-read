# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
拆解⼤模型⼏项核⼼操作背后的数学与 Infra  优化逻辑
腾讯程序员 2026 年 6 ⽉ 17 ⽇ 02 : 33⼴东腾讯技术⼯程 43 ⼈
作者： binnnliu
本⽂将拆解⼤模型中⼏个核⼼操作（ RMSNorm 、 Softmax 、 Causal Mask 、 Sampling ）背后
的数学与  Infra 优化逻辑。看完你会发现， Infra 优化，本质上就是在⽤数学上的等价变换，或
者对精度的适度妥协，去换取更⾼的硬件利⽤率和极致的推理速度。
PS: 当然最核⼼的操作肯定是矩阵乘法，这个放到下⼀篇吧  《 AI Infra ⼊门：从矩阵乘法到
FlashAttentionV4 》～其他的还有 RoPE 和残差连接没有提及～
PS: to 已具备相关专业知识的读者， TL;DR 放在最后了，可以直接从⽬录跳转。
RMSNorm - 均⽅根归⼀化
⼤语⾔模型（ Transformer 结构）通常包含数⼗甚⾄上百个堆叠的隐藏层（如  Transformer 结
构）。输⼊张量（Tensor）在经过连续的矩阵乘法和加法操作后，其数值的分布范围会发⽣
剧烈的变化。
这种数值⼤⼩的不可控会导致两个严重的⼯程和算法问题：
1. 算法收敛困难：数值变得过⼤或过⼩会影响训练的稳定性：极端数值要么会落⼊激活函数
的饱和区导致梯度消失，要么会顺着⽹络不受控地放⼤引发梯度爆炸或硬件溢出。
2. 硬件层⾯的溢出与截断：在当前主流的  GPU 推理和训练中，为了追求极致的吞吐，底层
计算会在使⽤低精度浮点格式（如  FP16 或  BF16 ）。
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
img
对于  FP16，数值上限仅为  65504。如果未经处理的张量在层间传递时不断放⼤，容
易突破数值上限，引发   NaN（ Not a Number ）或   Inf  溢出。  即 FP16 精度⾼，但是
数值范围⼩。
对于  BF16 ，虽然不容易溢出，但它的尾数极短（仅  7 bit ）。如果数值⽅差过⼤、尺度
不⼀，在做加法时容易导致截断误差（即四舍五⼊，引发 “ ⼤数吃⼩数 ” 的问题）。即
BF16 精度低，但是数值范围⼤。
这两者都会导致模型输出乱码或训练彻底崩溃。为了保证⼤模型在深层⽹络中的数值稳定性，
研究⼈员在架构中引⼊了特征归⼀化（ Normalization ）机制（例如  LayerNorm 、
RMSNorm ）。其核⼼⽬的，是在数据的层间传递过程中，对其数值分布进⾏强制的缩放与平
移，将其约束在⼀个标准、安全的物理尺度内 , 防⽌⽅差膨胀引发的溢出。
⽽要对张量的数据分布进⾏量化约束，我们⾸先需要在数学上明确：如何精确衡量并计算⼀组
数据的波动范围？
离散度
在很久以前，⼈们只⽤平均数来描述⼀组数据。然⽽，平均数存在⼀个显著的局限性：它⽆法
反映数据内部的差异与真实的分布情况。举个例⼦：
城市  A 的⽓温：⼀年四季都是  20℃ 。（宜居）
城市  B 的⽓温：夏天  60℃ （热死），冬天  -20℃ （冻死）。
如果只算平均温度，两个城市都是  20℃ ，你会以为两个城市⼀样舒服。但实际上，城市  B 的
⽓温波动⾮常剧烈。为了量化这种波动（偏离平均值的程度），数学家们决定发明⼀个新的指
标：离散度。
强⾏缩放和平移原始数据，不会破坏原有的特征信息吗？这其实是因为归⼀化有⼀个重要
的底层前提：神经⽹络真正关⼼的并⾮数值的绝对⼤⼩，⽽是特征之间的相对差异。
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
⽅差
简单相加
如何计算波动呢？每天的温度减去平均温度，然后全部加起来？
城市  B 夏天：
城市  B 冬天：
加起来算总波动：
问题：  因为波动有⾼有低，正负值互相抵消了。算出来的总波动为  0 ？显然与事实不符。
绝对值
既然正负号会抵消，那最符合直觉的办法就是加绝对值。这就是平均绝对误差（ MAD ）。
夏天波动：
冬天波动：
平均波动： 。
这个指标挺好，完全符合⼈类直觉！但为什么最终没有使⽤呢？因为统计学需要⼤量⽤到微积
分（求导数）来寻找误差的最⼩值（⽐如著名的最⼩⼆乘法）。绝对值的图像是⼀个  “V” 字
型，它在底部尖端处是不平滑的（不可导）。当想要通过求导来寻找最优解时，绝对值会是巨
⼤的障碍。
image-20260419120202261
平⽅
既然绝对值没法求导，那还有什么⽅法能把负数变成正数？平⽅！
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
夏天波动：
冬天波动：
求平均：
是的，恭喜你发明了⽅差！因为平⽅函数的图像是⼀个平滑的 “U” 字型抛物线。抛物线求导数
只需⼀秒钟（ 的导数是   ）。由于在数学求导上的完美表现，⽅差（ Variance ）彻底统治
了统计学。
⼤⽩话定义：⽅差，就是每个数据与平均值之间距离的平⽅的平均数。它衡量的是数据整体偏
离中⼼的程度  - 离散程度。
⽅差的计算步骤：
1. 求均值：先算出这组数据的平均值（记作  ）。
2. 求偏差：把每个数据都减去平均值，看看每个数据偏离中⼼多远（即   ）。
3. 平⽅（消负号并放⼤误差）：把算出来的每⼀个偏差求平⽅（即   ）。
4. 求⽅差：把这些平⽅后的偏差全部加起来，再除以数据的个数   。
⽅差的公式（记作   ）：
⽅差的问题：单位和数值被扭曲了。
标准差
既然之前为了好算，把数值平⽅了，那最后把数值开个根号还原回来不就⾏了吗 ~
对⽅差开根号：℃。
标准差就这样诞⽣了！它既保留了⽅差在数学求导上的优势，⼜完美还原了真实数据的单位和
尺度，更符合⼈类⼤脑的直觉。
⼤⽩话定义：为了解决⽅差 “ 单位变了 ” 的问题，我们直接把⽅差开个根号，把它打回原形。这
就叫标准差。
标准差的公式（记作  ）：
⼏何意义
标准差本质上就是⾼维空间⾥的直线距离。想象我们把⼀组数据     看作⼀个  
  维空间⾥的⼀个点（或者叫向量  ）。同时，把均值也看作⼀个向量   。
我们想知道：数据向量     距离中⼼向量    到底有多远？
城市  B 的⽓温明明只上下波动了  40℃ ，但算出来的⽅差却是  1600 平⽅摄⽒度。
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
回忆⼀下初中学的勾股定理：在⼀个直⾓三⾓形⾥，怎么算两点之间的直线距离（斜边  ）？
公式是：
发现了吗？标准差的公式，和勾股定理⼏乎⼀模⼀样～
本质上，计算标准差，其实就是在多维空间⾥，计算原始数据点到平均值这个中⼼点的直线物
理距离！
开根号的作⽤：开根号，恰好把抽象的数据差异，还原成了⼈类⼤脑最熟悉的空间物理距离。
⼤脑在现实世界⾥看距离，看的就是那条直直的斜边（开完根号后的长度  ）。如果不开根
号，我们拿到的其实是斜边上那个正⽅形的⾯积（）。
基础特性
在统计学中，如果你把⼀组数据     ⾥的每⼀个数，都乘以（或除以）⼀个常数  ，那么新数
据的⽅差，等于原⽅差乘以    的平⽅。数学公式写成：
为什么常数提出来要加平⽅？  因为⽅差的定义本⾝就是距离的平⽅的平均值。  想象⼀下：
1. 如果⼀条线段的长度放⼤    倍，那么以这条线段为边长的正⽅形⾯积（即平⽅）会放⼤多
少倍？是    倍。
2. 同理，如果把数据的波动幅度（偏离均值的距离）放⼤了    倍，那么波动的平⽅⾃然就放
⼤了    倍。
Z-score  标准化
数组每个元素先减均值再除以标准差（即⽅差的开根号）后，新数组的⽅差会变为 1, 均值变
为 0 。
假设有⼀个数组（或随机变量）   ，它的⽅差为   。那么，它的⽅差的开根号（即标
准差）可以表⽰为：
根据⽅差的常数乘法性质，如果我们将数组中的每个元素乘上⼀个常数  ，新数组的⽅差会变
成原⽅差的     倍：
给数组的每个元素乘上了   （即除以标准差）。我们将    代⼊上⾯的公式：
由此可见，经过这样缩放后的新数组，其⽅差必然变为  1。在实际应⽤中，为了让不同维度的
数据具有可⽐性，我们通常不仅会除以标准差，还会先减去数组的均值（）。这就是著名
的  Z-score 标准化公式：
经过完整  Z-score 处理后的数组会具备两个⾮常优秀的统计特性：
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
均值为  0
⽅差为  1
标准正态分布   ：  这是⼀种平均值为  ，⽅差（和标准差 ) 为    的理想数据分布状
态。Z-score 标准化只保证均值为   、⽅差为  ，并不保证数据服从标准正态分布   。
只有当原始变量本⾝近似正态分布时，标准化后的变量才近似服从   。
LayerNorm (Layer Normalization)
为了解决开篇提到的数值溢出和梯度问题，深度学习直接把  Z-score 这个公式应⽤到了神经⽹
络。⽐如常见的  BatchNorm 或  LayerNorm ，本质就是利⽤  Z-score 强⾏把每⼀层的数据标准
化，将数值的尺度拉回安全范围，从⽽防⽌梯度异常并加速模型收敛。
LayerNorm 的核⼼思想是对同⼀个  Token 内的所有特征维度（ hidden size, ）进⾏标准化，
使其均值为  0 ，⽅差为  1 。
与 LayerNorm 对应的是 BatchNorm, LayerNorm/RMSNorm 是严格在  Token 级别（ Hidden
Size 维度）  闭环的。⽆论外部的  Batch Size 怎么变，⽆论旁边并⾏的请求是写诗还是写代
码，每⼀个  Token ⾃⾝的归⼀化结果不会发⽣变化。训推⼀致。⽽ BatchNorm 训练时会把
Batch 内不同请求的同⼀个特征维度⼀起算均值和⽅差，其实想想就不合理，⼀个请求竟然会
受到同⼀个批次的其他请求的影响，另外由于同批次的不同样本长度不⼀致需要来零值⼀起算
⽅差。在推理时，会使⽤训练积攒的全局历史均值（ Running Mean ），然⽽⼈类语⾔的上下⽂
千变万化，不存在⼀个能适配所有⽂本分布的全局平均值。全局历史均值会极⼤的降低模型的
表达能⼒。  另外训练与推理的机制割裂，训推不⼀致。因此当前语⾔模型基本不会使⽤
BatchNorm 。
数学公式
通过  Z-score （减去均值，除以标准差），主动剥离了那些毫⽆意义的 “ 绝对偏移 ” 和 “ 绝对
尺度 ” ，将张量还原为纯粹的“ 相对信号 ”。这不仅不会丢失信息，反⽽帮助模型排除了数
值⼤⼩的⼲扰，让每⼀层⽹络都能稳定、专注地处理特征之间的相对关系。
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
计算步骤 :
1. 计算均值（ Mean ）：
2. 计算⽅差（ Variance ）：
3. 标准化并做仿射变换（乘以可学习参数  ，加上偏置  ）。
额，这⾥不就是归⼀化么？为啥⼜要可训练参数、   呢？很多资料说是为了增强特征表
达能⼒，要我说就是实验恰好有效
Infra 视⾓
LayerNorm 是⼀个典型的  Memory-bound （访存密集型）  算⼦。它的计算包含了两次
Global Reduction （全局规约）操作。最致命的是数据依赖：你必须先完整遍历⼀次数据算出
均值  ，然后才能⽤    去遍历第⼆次算⽅差   。在  GPU 上，这意味着更复杂的线程同步，
或者在  Kernel 未极致融合时需要多次往返读写  HBM（显存），极⼤地浪费了宝贵的内存带
宽。
RMSNorm (Root Mean Square Normalization)
RMSNorm 的作者（ Biao Zhang 等⼈， 2019 ）通过实验发现： LayerNorm 之所以有效，主要
是因为缩放（ Scaling ，即除以标准差）的作⽤，⽽平移（ Mean-centering ，即减去均值  
）对模型收敛的贡献微乎其微。
既然均值没⽤，那就直接砍掉它。放弃了计算均值，只保留对向量  RMS 尺度的归⼀化。
数学公式
其中均⽅根（ RMS ）的计算：
其中   ，即代码默认值：eps = 1e-6，实际运⾏值：取决于具体模型的   config.rms_no
rm_eps  配置，通常为   1e-5  或   1e-6， eps 的作⽤是防⽌除以零，保证数值稳定性，其值⾮
常⼩，对最终计算结果的影响微乎其微。
当然也有说法： LayerNorm 强⾏减均值（取平均归零）这个动作，其实是在⼈为地阉割
模型的表达能⼒。
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
Infra 视⾓
1. 打破数据依赖： RMSNorm 不需要算  ，直接计算每个元素的平⽅和即可。这意味着只需
要⼀次单向的  Reduction 操作。
2. 极致的访存优化：  在编写  Triton 或  CUDA Kernel 时， RMSNorm 可以⾮常丝滑地在⼀个
Block 内完成数据加载  (SRAM) -> 平⽅求和  -> ⼴播  -> 缩放的流⽔线，中间变量极少。
3. 计算量减少：  省去了⼤量减法操作。主流模型在使⽤  RMSNorm 时，通常连后处理的偏
置项     也⼀并去掉了（即⽆  Bias 线性层），进⼀步减少了参数加载和  element-wise 加法
的开销。
这⾥值得注意的是：相对 LayerNorm  Bias 也被去掉了：  RMSNorm 常常只保留     ⽽去掉  ，
这不是数学上必然要求，⽽是现代  LLM 架构中的经验选择。它通常与⽆  bias Linear 、 Pre-
Norm 残差结构、 SwiGLU 等设计共同出现，整体上减少参数与访存，同时保持效果。    也有
类似说法： LayerNorm 包含减均值，因此后⾯跟着的线性层加  Bias 是有意义的。⽽
RMSNorm 砍掉了平移，只做纯粹的尺度缩放，如果它后⾯紧跟的  Linear 层仍保留  Bias ，就
破坏了  RMSNorm 抛弃绝对中⼼、只维持相对尺度的初衷。当今的主流开源⼤模型不仅仅
RMSNorm 去掉了  ，⽽是⼏乎所有的  Linear 层都去掉了  Bias ：
q_proj, k_proj, v_proj, o_proj 没有  Bias
MLP 的  gate_proj, up_proj, down_proj 也没有  Bias
对此有很多解释：
训练更稳定   "No biases were used in any of the dense kernels or layer norms. We found
this to result in increased training stability for large models."  - PaLM 论⽂
架构冗余： RMSNorm 后紧接  Linear 时， bias 的位移作⽤会被下⼀个  Norm 的     吸
收； SwiGLU 的门控本⾝也提供了类似  bias 的⾃由度。 bias 在现代架构⾥已被架构本⾝替
代。
Infra 友好：少⼀次  add 与  bias load
但是要我说，就是实验有效  + Infra 友好。专业的说法，哈哈：从⼯程视⾓看，这类设计往往
并⾮单⼀数学原则的必然结果，⽽是效果、稳定性、实现成本和硬件效率共同权衡后的经验选
择。
LayerNorm 但借助     公式与  Kernel 融合，可实现只需访问⼀次  HBM 。⽽
RMSNorm 进⼀步斩断了均值计算，压缩了  SRAM 占⽤和  ALU 指令周期。
LayerNorm 虽然理论上需要均值和⽅差两步。⾼性能实现中并不必然需要两次  HBM ，可以在
⼀次  HBM load 中同时累计     和   ，甚⾄使⽤  Welford 算法提升数值稳定性。但相较
RMSNorm ， LayerNorm 仍需要维护均值相关统计量，并在归⼀化阶段执⾏额外的减均值操
作，因此寄存器压⼒、规约状态、 ALU 指令数都更⾼。
RMSNorm 相对于  LayerNorm 的收益：
1. 减少了寄存器 /SRAM 的占⽤。
2. 节省了⼤量的  ALU （逻辑运算单元）指令，特别是消除了对全部元素的减法（减去均值，
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
其实在当今主流的  Fused CUDA/Triton Kernel 中，LayerNorm 也是可以做到单次  HBM 访存
（ 1 Pass ）的。在数学上，⽅差可以等价展开为：
在  GPU 寄存器 /SRAM 层⾯，我们在单⼀的⼀个  Block 遍历输⼊张量时，可以同时累计  
  和   。由于⼤模型的  Hidden Size （如  4096 或  8192 ）对应的字节数（约  8-16 KB ）完全
可以被塞进单个  SM 的  Shared Memory 中，因此⽆论  LayerNorm 还是  RMSNorm ，现代算
⼦在  HBM 层⾯都是只读⼀遍、写⼀遍。虽然     能实现  1-pass ，但在  FP16
或  BF16 精度下，如果     和    的值⾮常接近，相减容易引发灾难性抵消
（ Catastrophic Cancellation ），导致⽅差精度丢失甚⾄计算出负数（最后开根号出  NaN ）。因
此在实际的  Kernel （如  Apex 或  Triton 内部）中有时会采⽤  Welford 算法来兼顾  1-pass 和数
值稳定性，或者在累加时强制转换到  FP32 进⾏计算。 的推导
逻辑：假设数据的平均值为  （即   ）。⽅差的原始定义是：每个数减去平均值的平
⽅，再求平均。即：
根据   ，我们展开得到：
因：  =  ，⽽    = ，  所以    =  ，因为  
  是个常数，常数的平均值还是它⾃⼰！所以 =  。得：
⽽     就得到了最终的公式：
Post-Norm
ResNet 与  Transformer ⼀开始都是⽤的 Post-Norm
ResNet-v1 (2015 年 ) ： 。何恺明在残差相加之后，套了⼀个  ReLU
激活函数。
Transformer (2017 年 ) ： 。  Google 团队在残差相加之后，套了⼀个
LayerNorm 。
Post-Norm 说⽩了，就是先做⼦层计算，然后和输⼊     做残差相加，最后对整体结果做归⼀
化：   即：
计算残差分⽀：  
再对结果做归⼀化：  
在  Post-Norm 中，如果把整个⽹络展开   ，主⼲路径
被多个  Norm 层打断了。每次经过  Norm ，梯度都会被重新缩放，导致层数⼀深，梯度在传回
浅层时极容易消失或爆炸。
Transformer 采⽤了残差连接  + Post-Norm 发现堆到  12 层、 24 层（如  BERT ）时还可以，但
想要像  GPT-3 那样堆到  96 层时，训练容易崩溃。另外， Post-Norm 架构在模型初始化的早
期阶段，梯度每次沿着主⼲往下传，都必须穿过⼀次  LayerNorm ，⽽被其导数（反⽐于输⼊
⽅差）不断衰减。这就导致：靠近输出的深层⽹络会接收到未经衰减的巨⼤梯度，⽽靠近输⼊
的浅层⽹络梯度却严重消失。这种极度不平衡的巨⼤深层梯度，会在第⼀步引发巨⼤的参数更
新，导致深层的权重本⾝瞬间变⼤，最终在前向传播时引发激活值爆炸（  FP16 溢出）。为了
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
防⽌训练初期的梯度分布不平衡，引⼊了 Warm-up 机制。通过在训练的最开始阶段采⽤极⼩
的学习率来严格限制参数的更新幅度，等待⽹络权重和归⼀化层的统计量逐步调整到相对稳定
的分布空间后，再恢复正常的学习率。可以说，长周期的  Warm-up ，很⼤程度上就是为了给
Post-Norm 架构固有的梯度缺陷打补丁。
Pre-Norm
Pre-Norm 就是先对输⼊     做归⼀化，再送⼊⼦层计算 , 最后和原始的     计算残差：
在  ResNet 发表的第⼆年（ 2016 年），何恺明团队发表了⼀篇重要的论⽂《 Identity Mappings
in Deep Residual Networks 》（即 ResNet-v2）。他们发现，必须保证     所在的这条主路畅通⽆
阻，不能加任何操作。
ResNet-v2 (2016 年 ) ： ，把  BatchNorm 和  ReLU
全都挪到了残差⽀路⾥⾯。
Transformer-Pre-Norm (2020 年前后 ) ： ，把  LayerNorm 挪到残差
⽀路⾥。
在  Pre-Norm 中，如果把整个⽹络展开 ，主
⼲路径变成了纯粹的  ，梯度实现了⽆损回传， ResNet 可以轻松突破  100 层。（反向传播：
求导产⽣的那个  1 保证了⽆论⽹络有多深，深层的梯度都能原封不动地传回浅层，从⽽让深
层⽹络训练成为可能。）
Pre-Norm 治好了训练崩溃，让⼤模型的规模化（ Scaling up ）成为可能。因此， Pre-Norm 或
其变体成为了现代⼤模型的主流选择。
然⽽， Pre-Norm 并⾮完美，它是⽤前向传播的妥协换取了反向传播的稳定。
在前向传播中， Pre-Norm 随着层数加深，主⼲⼲路     累加的值越来越⼤（⽅差越来越⼤）。
⽽     这⼀项因为经过了  Norm ，输出的数值⼤⼩基本保持不变。这就导致越到深
层，⽹络新添加的特征相对于主⼲     来说就越微不⾜道。这被称为模型的表征坍塌
（ Representation Collapse ）。说⽩了，就是你没钱时，给你 100 块，你觉得很多。随着你的
钱越来越多，同样的 100 块，你看不上了。这导致了⼀个有趣的现象：如果我们强⾏把  Pre-
Norm 训练的⼤模型的最后⼏层直接砍掉（剪枝），模型的性能下降往往并不明显。
注：为了解决  Pre-Norm 的表征坍塌问题，微软曾提出  DeepNorm。它通过修改参数初
始化系数，重新让  Post-Norm 能够稳定训练，甚⾄⽀持将⽹络扩展到  1000 层。但当今
的主流⼤模型基本没有采⽤此⽅案。⼀⽅⾯， Scaling Laws 表明增加模型宽度和数据的
收益远超极端加深层数，在百层以内的⽹络中， Pre-Norm 的坍塌现象并不致命；另⼀⽅
⾯，业界已经形成了   Pre-Norm + RMSNorm 的标准，现有的  AI Infra 均针对该组合做了
极致的访存优化。引⼊  DeepNorm 意味着要放弃这些现成的⾼效算⼦，这也是理论算法
向⼯程效率妥协的典型案例。
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
历史总是惊⼈的相似。错误也在⼀直重复。⼤模型从  Post-Norm 演进到  Pre-Norm ，本质上
就是 NLP 领域，在时隔⼏年后，重新把 CV 领域  ResNet-v1 升级到  ResNet-v2 的路，⼜⾛了⼀
遍。
Softmax - 概率归⼀化
Softmax 的核⼼原理可以⽤⼀句话概括：将⼀组任意的实数（通常称为  Logits ），转化为⼀套
总和为  1 的概率分布，同时放⼤差异。
img
前⾯我们花了⼤篇幅探讨如何利⽤  RMSNorm 消除绝对偏移（均值），并通过约束⽅差来防⽌
隐藏层特征在层间传递时出现数值发散与溢出。然⽽，在  LLM 的整体计算链路中，⽅差膨胀
引发的稳定性风险并未完全消除。除了特征层⾯的归⼀化，  Softmax 同样对输⼊张量的数值尺
度极其敏感，⾯临的数值稳定性要求与浮点计算瓶颈，因此在⼯程实现上同样需要平移和缩
放。
从绝对分数（ Logits ）到概率
假设你训练了⼀个神经⽹络来识别图⽚是 “ 猫 ” 、 “ 狗 ” 还是 “ 鸟 ” 。⽹络的最后⼀层（通常叫线性
层）会给每个类别打分（这个原始得分在数学上叫  Logits）。⽐如⼀张猫的图⽚进去，机器可
能给出这样的得分：
猫：
狗：
鸟：
问题来了：这些得分有正有负，没有上限也没有下限。我们⼈类想看到的是： “ 这张图有  80%
的概率是猫， 15% 是狗， 5% 是鸟 ” 。我们怎样才能把这些乱七⼋糟的得分，转换成加起来等
于  （即   ），且每个都在    到     之间的概率分布呢？
这还不简单？把所有的分数加起来，算个百分⽐不就⾏了？⽐如：猫的概率 。
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
这种做法（线性归⼀化）有两个缺陷：
1. 分母可能为零或负数：因为原始得分⾥有负数（⽐如鸟是   ），加起来的情况不可控。
概率怎么能是负数呢？
2. 不够 “ 爱憎分明 ”：如果得分是     和   ，直接算⽐例⼤约是     和   。但实际
上，机器给出     已经⽐     ⾼出了整整     分，在许多任务中，我们希望模型对最⾼分
有更强的 “ 确信感 ” （即放⼤差距）。
Softmax 引⼊ 
为了完美解决上⾯的问题，数学家和计算机科学家们引⼊了   （关于常数  e 的由来，参见⽂
末附 1 ）。 Softmax 的核⼼公式是这样的（假设求第     个类别的概率）：
这个设计极其巧妙，它同时做到了三件事：
第⼀步：去负数（⾮负性）
⽆论输⼊的     是正是负，它的指数     永远是⼤于    的正数（⽐如   ）。这保
证了算出来的概率永远不可能为负。
第⼆步：求⽐例（归⼀化）
把所有类别的     加起来作为分母，这样所有类别的计算结果加起来绝对等于   。
第三步：放⼤差距，赢家通吃
指数函数    的增长是爆炸性的。如果猫的得分⽐狗⾼⼀点点，经过     放⼤后，猫的概率
会⼤幅度碾压狗。它在模拟⼀种 “ 硬最⼤值（ Hard Max ，即只要最⼤的那个，其他全为
0） ” 的效果，但⼜保留了其他类别的微⼩可能性。
⽐如对于对于   ： , 结果约为：
即： Softmax 只关⼼  logits 之间的差值，⽽不是绝对⼤⼩。   和    的
Softmax 完全相同。
第四步：平滑可导
如果直接⽤  Hard Max （输出  1, 0, 0 ），这个操作是不可导的，神经⽹络的反向传播算法就
⽆法更新参数。⽽    的导数是它本⾝，⾮常平滑，简直是为微积分量⾝定制的。
HardMax:如果输⼊是   ， Hard Max 输出是   。缺点：不可导（在
⾮最⼤值处导数为  0 ），⽆法通过梯度下降进⾏反向传播。
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
SoftMax :同样的输⼊   ， Softmax 输出约   。它保留了 “ 最⼤
值概率最⾼ ” 的特性，但没有把其他值杀死。这保证了全程可导，让神经⽹络能够学习
到 “ 第⼆好的选择 ” 以及类别之间的细微关系。
平移机制： Safe Softmax(-M)
在写  CUDA kernel 或优化算⼦时，不会直接照搬上⾯的公式，因为会有硬件层⾯的浮点数溢
出（ Overﬂow/Underﬂow ）的问题。
如果     很⼤（例如  1000 ），  会直接导致浮点数溢出  (NaN/Inf) 。
我们在计算前，先从所有输⼊中减去最⼤值   。即公式变为：
数学上结果不变。
⼯程上，  永远   。最⼤项变成   ，其余项是    到     之间的⼩数。彻底解
决了上溢出问题。（下溢出通常不影响训练稳定性，通常会被视为  0 ）。
Softmax 的核⼼特性是：它只关⼼数值之间的 “ 相对差值 ” ，根本不关⼼数值的绝对⼤⼩。
概念 核⼼公式 主要⽤途 包含关系
Safe Softmax 推理时获取概率分布纯粹使⽤  "-M" 技巧
Log-Sum-Exp
(LSE)
训练时计算  Loss / Log-
Softmax
LSE 是⼀个数学项，利⽤  "-M" 来
实现安全计算
缩放机制：为什么必须除以   ？
在  Attention 计算中， Softmax 计算的是当前  Token 对上下⽂中所有历史  Token 的『注意⼒权
重』。它的归⼀化操作是沿着序列长度（ Sequence Length ）维度展开的：即把单个  Query 与
所有历史  Key 算出的     个点积相似度得分（ Logits ），转化为⼀个总和为  1 的概率分布，以决
定当前词在⽣成时，应该向历史中的哪些词分配多少注意⼒。
然⽽，产⽣数值溢出和梯度消失风险的根源，并不在于参与归⼀化的序列有多长，⽽在于这  
  个  Logits 中的每⼀个，都是由长度为    的  Query 和  Key 向量经过    次乘积累加得到
的。如果不加⼲预，直接将⾼维点积的结果丢给  Softmax ，会导致梯度消失。问题的核⼼在
于：点积结果的⽅差，会随着维度    的增⼤⽽剧烈膨胀。
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
img
⽅差膨胀
我们可以从统计学⾓度直观且严谨地理解这⼀点。两个向量的点积，本质上是     个乘积项的
累加： 。
为了在数学上精确推导这个累加过程对⽅差的放⼤效应， Transformer 的原作者在论⽂中构建
了⼀个理想的统计假设：假设     和    向量中的每⼀个元素     和     都是相互独⽴的随机变
量，并且都满⾜均值为  0 ，⽅差为  1。
单个乘积项     的⽅差
在统计学中，已知两个独⽴变量乘积的⽅差公式为：
因为我们假设了均值    且   ，公式的后两项被直接抹零。公式简化为单纯的
⽅差相乘：
这意味着，每⼀对元素相乘后，得到的这⼀个 “ 乘积项 ” 本⾝的⽅差是  1 。
  个乘积项累加的总⽅差
在统计学中，任意两个独⽴变量和的⽅差，严格等于它们各⾃⽅差的累加：
公式最后的    代表协⽅差，由于我们假设各变量互相独⽴，协⽅差为  0 ，公式化简
为纯粹的加法。  因此，把     个互相独⽴的乘积项加起来，总⽅差就是：
这就是⽅差膨胀的数学真相：经过    次独⽴的累加，点积结果的⽅差直接变成了    倍。
不过这⾥有⼀个触及灵魂的问题：在真实的神经⽹络中，因为经过了     和    的线性映
射，且特征间具有⾼度的语义相关性，  和    不太可能满⾜的相互独⽴、均值为  0 、⽅差为
1 。
确实如此。那为什么这个基于假设推导出的   ，依然成为了⼤模型  Attention 的标准范式？
别那么认真，你就说实验效果变没变好吧，毕竟⼤模型本⾝就是个实验科学。  伟⼤的总设计
师曾经说过： “ 不管⿊猫⽩猫，能捉⽼⿏的就是好猫。 ”
不过这块业界也有解释：这个基于理想统计模型推导出的   ，虽然在现实⽹络中并不严格
成⽴，但它在模型初始化的第⼀步，完美地稳住了  Logits 的量级，让  Softmax 避免了开局即
死于梯度消失。⾄于训练中后期数据分布偏离了假设怎么办？不⽤担⼼，只要⼀开始稳住了起
步，神经⽹络强⼤的参数更新能⼒⾃⼰就会去适应这套缩放规则。这就是⼤模型中的⽞学，
  理论向⼯程妥协。
训练权重的初始化
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
都到这⾥了，不如我们看看  和     是怎么来的？它们的完整计算路径是：
经过  RMSNorm 处理后，输⼊向量    的均⽅根被强⾏拉到了  1 。这在数值上等价于：给
后续的线性映射提供了⼀个尺度被严格约束（近似⽅差为  1 ）的输⼊，但是均值肯定不为 0 。
（～～⼜是近似）
那为了训练开始时，尽可能满⾜  和    相互独⽴、均值为  0 、⽅差为  1 。我们应该如何初始化
权重呢？ Amazing ～开始有意思了
相互独⽴：
当框架（如  PyTorch ）调⽤   torch.nn.init.normal_() 去填充     和     时，矩阵⾥的每⼀个元
素   ，都是从正态分布中独⽴抽样（ Independently Sampled ）出来的。  ⽽⾼维空间中的两
个随机向量，绝⼤概率是近乎正交（垂直）的。
⽅差为 1:
1. 前⾯有  RMSNorm 兜底，强⾏把⽅差约束住了，所以   。
2. 此时，只要框架在初始化     和     时，严格遵循⽅差控制原理，使其权重分布的⽅差
为   （这⾥输⼊维度   ）。
权重初始化要求：要求前向传播时，每⼀层输出的⽅差应该与输⼊的⽅差保持⼀致，避免
梯度消失或爆炸
3. 根据前⾯的公式推导：
均值为 0:
1. 前⾯虽然经过了  RMSNorm ，但因为它刻意去掉了平移（减均值）操作，其均值⼤概率不
为  0 ，即   。
2. 此时，只要框架在初始化     和     时，强制使⽤完全对称的分布（如正态分布   mean=0.
0  或均匀分布   [-a, a]），严格将其权重分布的数学期望（均值）锁死在  0 ，即  
。
权重初始化要求：不管上⼀层传过来的数据偏成了什么样（），只要这⼀层的权重均
值是  ，乘积相加后，就能强⾏把数据的均值阻断并拉回到     附近（）。
3. 根据统计学中期望的线性性质与独⽴变量乘积法则公式推导，输出向量的均值瞬间被阻断
并归零：
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
额，完美～但是看到代码，天塌了。不是这么搞的
# 基础初始化策略（ PreTrainedModel._init_weights ）
std = self.config.initializer_range or 0.02  # 默认 std=0.02
init.normal_(module.weight, mean=0.0, std=std)  # 均值 0 ，标准差 0.02 
均值确实是 0 ，但是标准差写死的 0.02 ～  怎么说呢。 std = 0.02 是个经验值，有些⼤模型也是
⽤     覆盖  std 或者同⼀个数量级的其他数据，量级对了就⾏，这⾥咱们不需要严谨
的数学。
权重初始化伪代码：
if layer_name in ['o_proj', 'down_proj']:
    # 如果是残差分⽀的出⼝层
    # std = 0.02 / sqrt(2 * num_layers)
    scaled_std = self.config.initializer_range / math.sqrt(2.0 * self.config.num_hidden_l
    init.normal_(weight, mean=0.0, std=scaled_std)
else:
    # 其他普通的层  (q, k, v, up, gate 等 ) ，照常使⽤  0.02
    init.normal_(weight, mean=0.0, std=self.config.initializer_range)
然后你可能也看见了，对于残差分⽀的出⼝层还做了额外的缩放
，主要是为了防⽌ Transformer ⼏⼗上百层的残差连接
（ Residual Connection ）累加引发的⽅差爆炸。
梯度消失
⽤ Softmax 是因为 Softmax 缩放效果好 , 但是点积的⽅差会随维度     膨胀
维度⼩的时候（⽅差⼩）： Logits 是   ， Softmax 输出⼤概是  $[0.7, 0.2,
0.1] ，保留了  "Soft" 的特性。
维度⼤的时候（⽅差⼤，未缩放）： Logits 变成了   。此时  Softmax 的输
出会变成近似   （其实是     和⼀堆接近    的数）。
主⼲路径是   。在⼀个  80 层的  Transformer 中，每⼀层（ Layer ）包含  2 个
残差连接（⼀个过  Attention ，⼀个过  MLP/FFN ）。所以  80 层总共有     个残差⽀
流。
we scale the weights of residual layers at initialization by a factor of   where   is
the number of residual layers 。  * （引⽤⾃ GPT-2 论⽂）
````

## PDF 第 17 页

[原页](RAW.pdf#page=17)

````text
这种绝对值极⼤的  Logits 会让  Softmax 产⽣ “ 赢家通吃 ” 现象，从  "Soft" 彻底退化成了
"Hard" 。
这在模型训练时是致命的： Softmax 函数的导数与    成正⽐（  为输出概率）。如果  
  极度接近  1 或  0 ，导数就⼏乎为  0 。从⽽导致梯度消失。
  缩放
既然点积累加后的 ** ⽅差变成了   **，那么它的标准差就是   。
根据⽅差的性质   ，只要我们在传⼊  Softmax 之前，强⾏将点积结
果除以   ，就能完美地将  Logits 的⽅差重新缩放回  1 。通过这种优雅的数学⼲预，⽆论
Attention 的维度    变得多⼤， Logits 始终被锁定在  Softmax 梯度最饱满的舒适区内，从⽽
保证了深层⽹络训练的稳定，同时也保证了推理时注意⼒数值的分布稳定。
img
Causal Mask - 序列维度的因果约束
在⼤语⾔模型中，⽣成⽂本必须遵循严格的时间因果律：第     个  Token 只能看到它之前的历
史  Token ，绝不能 “ 穿越 ” 去获取第     个  Token 的信息。
假设不加⼲预，第     个  Query 向量与所有  Key 向量做完点积后，得到的  Logits 是⼀个长度为  
 的⽆界实数向量。为了让它对未来  Token （）的注意⼒权重绝对为  0 ，我们在这些特
定位置的  Logit 上强⾏加上⼀个负⽆穷（在⼯程中通常⽤⼀个极⼩的常数替代，如     或在
FP16 下的最负安全值）。
数学表达为（针对上三⾓区域，即   ）：
经过  Softmax 的⾮线性映射后：
````

## PDF 第 18 页

[原页](RAW.pdf#page=18)

````text
通过这种极端的数值平移，未来  Token 在分母累加和分⼦中都会被彻底抹零，不仅实现了物
理意义上的因果隔离，且依然保持了当前  Token 的局部概率和为  1 ，完美维系了概率单纯形的
约束。
过去 , 实现  Causal Mask 需要在显存中⽣成⼀个庞⼤的     掩码矩阵并与    相加 , 这在
长⽂本下会引发灾难性的访存瓶颈 (Memory-bound) 。
如今的  FlashAttention 等⾼性能算⼦直接在底层引⼊了块稀疏（ Block-Sparsity ）机制。它不
再在全局显存中⽣成掩码，⽽是在  Tile 调度层⾯根据当前分块（ Block ）的⾏列索引进⾏分类
处理：
1. 对⾓线以上的分块（严格的   ）：  完全跳过。既不执⾏矩阵乘法，也不从  HBM 搬运对
应的  K/V 。这直接把  Attention 的计算量和访存量砍掉了⼀半。
2. 对⾓线以下的分块（严格的   ）：  所有的  Key 都是合法的历史信息，直接正常计算，
不需要任何掩码指令的开销。
3. 横跨对⾓线的分块：  只有在这极少数的边界  Block 内部，才会在  SRAM/ 寄存器中实时判
定元素的精确索引，并对右上⾓部分写⼊   （在  FP16 下通常取最⼩安全值   -6550
4）。
这种底层调度让掩码本⾝的  HBM 访存开销归零（   矩阵），并将  attention 两次⼤矩阵
乘 (   和   )的计算量与访存量都降低了接近  50% 。
值得注意的是， Causal Mask 只在训练阶段和推理的  Preﬁll （⾸字⽣成 / 上下⽂处理）阶段  ⽣
效。  在推理的 Decode 阶段，当前的  Query 是⼀个长度仅为  1 的向量，⽽它需要与全局所有
的历史  KV Cache 进⾏点积。此时所有的  Key 都是过去式，因果关系天然成⽴，因此在底层
的  Decode 算⼦中，根本⽆需执⾏任何  Causal Mask 相关的指令开销。（ Speculative
Decoding / Medusa/Eagle 等多  Token 验证场景除外）
````

## PDF 第 19 页

[原页](RAW.pdf#page=19)

````text
在早期的推理系统中，为了将不同历史长度的  Request 组成  Batch 并⾏计算，需要将短请求
补齐（ Padding ），并在  Attention 时加上  Padding Mask  来屏蔽⽆效的占位符。⽽在现代如
vLLM 这样的架构中， Attention 的计算是严格保持在  CUDA Kernel 层⾯的  Request 级别隔离
（ Request-level isolation ）的。这意味着对于  Decode 阶段的纯  GEMV 访存操作，我们既不
需要在计算层⾯执⾏任何统⼀的掩码处理（屏蔽了  Causal 和  Padding 的逻辑），也不需要在
全局显存（ HBM ）层⾯去做任何张量展平或碎⽚的显式拼接搬运。每⼀个  Request 所在的
Kernel 线程块，顺着页表指针（ Block Table ），将离散的局部历史  KVCache 块直接从  HBM
即时拉取（ Gather ）到⽚上  SRAM 中完成计算。时序因果⾃然闭环。
Online Softmax
结合   缩放和 Causal Mask ， Attention 的公式变为：
在  算⼦开发中，如果按照上述公式进⾏朴素实现，需要对  Global Memory 中的数据进⾏  3 趟
读写（ 3 Passes ）：
1. Pass 1 （找最⼤值）：遍历输⼊向量  ，找到最⼤值   。
2. Pass 2 （算分母）：再次遍历  ，计算所有的指数和作为分母：。
3. Pass 3 （算结果）：第三次遍历  ，计算最终结果：。
在底层硬件（如  GPU ）上，每⼀次遍历都意味着需要从全局内存（ HBM ）中将数据读取到计
算单元，然后再写回。在算⼒远超显存带宽的今天，这种频繁的  HBM 访存（ Memory
Access ）会造成巨⼤的延迟，成为典型的带宽瓶颈。
尤其在⼤模型推理（尤其是长⽂本  Preﬁll 阶段） Attention 计算中，如果严格按照数学公式分步
执⾏，会在  GPU 的  HBM （全局显存）中产⽣庞⼤的中间矩阵  （注意⼒分数）和  
（ Softmax 概率），其    的内存访问量会严重影响性能，即所谓的内存墙问题。
怎么办呢？业界⽐较通⽤的算⼦优化办法有 Kernel 融合  (Kernel Fusion) 与  分块计算  (Tiling) ，
本质就是 IO Aware ，即多⽤寄存器和 SRAM ，少⽤ HBM 。有没有可能⽤上呢？不⾏，
Attention 计算时则⾯临⼀个致命的数学障碍： Softmax 操作需要知道全局的最⼤值和指数和才
能计算，这通常要求完整的中间矩阵驻留在显存中。
因为 Pass 2 依赖  Pass 1 的最⼤值，导致 Pass 1 和 Pass 2 必须串⾏，从⽽必须保存中间矩阵来
完成这个操作。那真没有办法让 Pass 1 和 Pass 2 并⾏么？搞不定这个问题， AI ⾏业就完蛋了。
死脑⼦，快想，哈哈哈～
有没有可能：维护局部的当前最⼤值（ Running Max ）和当前指数和（ Running Sum ），并在
读⼊新块时利⽤动态缩放因⼦（ Rescaling Factor ）对旧结果进⾏修正。  最终 1 Pass 就可以实
现  找最⼤值和找分母呢？  是的，这就是 Online Softmax 。
⽽ FlashAttention 则把这个 " 边⾛边修正 " 的思想从  softmax 内部推⼴到了整条  attention 流⽔
线：对每个  Q tile ，沿  K/V ⽅向做⼀次融合遍历，就同时完成   、 online softmax 、
以及    三件事。让中间矩阵     始终活在寄存器中、不写回  HBM—— 最后只把每
个  Q tile 的     和  LSE 写出去。
````

## PDF 第 20 页

[原页](RAW.pdf#page=20)

````text
Online Softmax 数学推导与执⾏流
假设我们正在遍历序列，当前处理到了第     个元素   。我们在寄存器中维护两个全局状态：
 ：到⽬前为⽌看到的最⼤值。
：到⽬前为⽌的指数累加和（基于当前最⼤值   ）。
当新元素    到来时（更新逻辑）：
1. 更新当前最⼤值：
2. 更新当前的指数累加和：
遍历完所有     个元素后，我们就同时得到了全局的真正最⼤值     和全局真正的分母   。最
后，只需要第⼆次遍历计算最终结果：
如果新的     没有打破记录（ ），缩放因⼦就是   ，直接累加即可；如果  
 创了新⾼，旧的局部和就会被乘以⼀个⼩于  1 的衰减系数，完美等价于从⼀开始就⽤全局最
⼤值来计算。
FlashAttention 的实现
在真实的⼤模型计算中， Attention 不仅要算  Softmax ，还要把  Softmax 的结果乘以  Value 矩
阵（即   ）。  为了把  Online Softmax 的 “ 边⾛边修正 ” 思想推⼴到整条
Attention 流⽔线上， FlashAttention 在  KV 维度上不停合并  Tile ，并在循环内部长驻⼀个 ** 未
归⼀化的状态三元组：** 。
操作名称数学公式逻辑说明  / ⽬的
Q-K Dot Prod
uct
查询 Query 和该请求所有 Key 的点积，注意⼒原始分数。 ->[query
_lens, num_heads, seq_lens]
Scale 对原始分数进⾏数值缩放（  为向量维度），防⽌  Softmax 函数进
⼊梯度极⼩的区域。
Mask 注⼊因果逻辑，通过加上掩码矩阵   （通常将未来位置设为  
），阻⽌模型 “ 看到 ” 未来的信息。
Softmax 将处理后的分数转化为总和为  1 的注意⼒权重（概率）。 ->[query
_lens, num_heads, seq_lens]
MatMul
根据注意⼒权重     对值向量（ Value ）进⾏加权求和，得到最终的
输出特征表⽰。
V 的 Shape 为[seq_lens, num_heads, head_dim]   -> [quer
y_lens, num_heads, head_dim]
每当读取到⼀个新的  KV Block ，计算出局部的点积结果     后，执⾏如下更新逻辑：
````

## PDF 第 21 页

[原页](RAW.pdf#page=21)

````text
for kv_block in KV_Cache:
    S_local = Q @ kv_block.K.T                  # 计算局部注意⼒得分  S
    m_new   = max(m_old, max(S_local))          # 寻找新的全局最⼤值
    
    scale   = exp(m_old - m_new)                # 核⼼：计算对历史数据的修正缩放因⼦
    
    # 1. 修正历史分⺟，并累加当前块的指数和
    ℓ _new   = ℓ _old * scale + Σ exp(S_local - m_new) 
    
    # 2. 修正历史输出  Õ ，并拿着【未归⼀化的权重】直接乘当前块的  V
    Õ_new   = Õ_old * scale + exp(S_local - m_new) @ kv_block.V 
    
    m_old   = m_new                             # 更新最⼤值记录
# 此时所有  KV 都看完了，我们拿到了真正的全局分⺟  ℓ  和全局  Õ
O_final = Õ_new / ℓ _new                         # O(1) 的标量 / 向量除法归⼀化
每⼀步都在做什么？
scale = exp(m_old - m_new)  把 " 基于旧  max" 的历史累加值校正到新  max 基准下；
  随新  tile 贡献增长；
  同步按   scale  收缩，再把新  tile 的     即 exp(S_local - m_new) @ kv_block.V 加进
去；
以上描述的逻辑主要是 FlashAttention v2 以及之后版本的实现。下⾯简要说下 FlashAttention
v1 到  FlashAttention v2 的进化逻辑。（当前 FlashAttention 已经进化到 V4 版本，详见附 2 ，本⽂
不再深⼊）
FlashAttention v1 （外  KV ，内  Q ）
在  FA1 中， kernel 的外层循环是  KV block 、内层循环是  Q block ，并且每个  (batch, head) 只
启动⼀个  CTA 。这带来两个问题：
1. 并⾏度不⾜： Grid 维度被限制在   ，即只有     个  CTA ；在长上下⽂（ Long
Context ）且  Batch/Head 较少的场景下， GPU 内部的⼤量  SM （流多处理器）会处于闲
置状态，根本跑不满。
2. Q 状态的  HBM round-trip ：外层每处理完⼀个  KV block ，当前  CTA 已经更新了所有  Q
block 的部分状态   。由于     很⼤、放不下全部  Q 状态，只能写回  HBM ；下
⼀个外层  KV 迭代再从 HBM 读回来继续累加。同理， Q 和  KV 本⾝也会被反复读⼊。
FlashAttention v2 （外  Q ，内  KV ）
FA2 将外循环改为遍历  Q blocks ，内循环遍历  KV blocks 。这意味着每个  CTA （线程块）只
需认领⼀个  Q tile ，就可以像流⽔线⼀样吞吐历史  KV blocks 。最终， Q 只在⼀切结束时向
HBM 写回唯⼀⼀次     和  LSE ，避免了  FA1 中的  HBM 读写中间态。
````

## PDF 第 22 页

[原页](RAW.pdf#page=22)

````text
Grid 维度的并⾏度提⾼，把    序列长度也加⼊了并⾏维度
gridDim = ( ⌈ seqlen_q / BLOCK_M ⌉ , batch_size, num_heads)
在  CTA 内部， FA2 沿着  Q 的  M ⽅向切分任务，让每个  Warp （线程束）独占⼀部分  Q ⾏
（例如   kBlockM / num_warps ⾏）。
在  GPU 底层的物理执⾏中， Tensor Core 执⾏  MMA （矩阵乘累加， ）指令
时，输出结果本来就会暂存在的  Warp 物理寄存器（ C-fragment ）  中。因为外层循环固定了
Q，这部分  Q 对应的未归⼀化状态     可以直接长驻于这些物理寄存器中。（其中   acc_
o  直接利⽤  MMA 指令的  C-fragment 累加）
随着内层循环源源不断地从  Shared Memory (SRAM) 搬⼊新的  K 和  V Block ， Warp 只需要利
⽤硬件指令，对着寄存器⾥的     进⾏原地累加  (In-place Accumulation) 。
直到该  Q tile 遍历完了所有的历史  KV ，这组长驻寄存器才会执⾏最后⼀次除以全局    的归⼀
化操作，然后⼀次性写回全局显存  (HBM) 。由于每个  Warp 处理的  Q 切⽚互不重叠，其输出
结果完全独⽴， Warps 之间不再需要通过  SRAM 进⾏结果拼接（ Reduce ），从⽽消除了底层
Barrier 同步的通信开销。
特别注意：在  FA2 中，每个被分配了不同  Q tile 的  CTA 都独⽴地去  HBM 遍历读取全量的  KV
cache 。这看起来会让  KV 的  HBM 流量相⽐  FA1 放⼤  num_q_blocks 倍，但实际测量中远没
有达到这个上界 —— 主要归功于  GPU 的  L2 cache 。同⼀  wave （调度波次）内的  CTA 会在
极短的时间差内访问相同的  KV block 。当第⼀个  CTA 把数据拉进全局  L2 时，后续  CTA 会命
中  L2 （带宽约为  HBM 的  4 倍， H100 下  ~12 TB/s vs ~3 TB/s ），在期望值意义上把物理
HBM 读次数压回接近   。但从体系架构视⾓看，这机制相当脆弱—— 它本质上依赖硬件⿊
盒调度器让相关  CTA 保持 " 齐步⾛ " 。⼀旦出现调度断层（ wave 间断层、 SM 占⽤不均），或
长上下⽂把  KV 挤出  L2 容量（ H100 仅  50 MB ，长  context 的  KV 是  GB 级），命中率会从
~99% 退化到  80% 以下，出现实测可见的性能拐点（不是悬崖式 " 爆炸 " ，是曲线劣化）。这也
是为什么顶级算⼦架构（ FA3/FA4 、 TRT-LLM 、 vLLM 的⾼性能  attention 后端）必须⾛两条
硬路：
1. Tile scheduler 主动编排访问顺序（flash_attn/cute/tile_scheduler.py）：在软件层让相邻
CTA 访问相邻  KV block 、按  L2 容量做  swizzle—— 这是不依赖新硬件、但也不完全是 " 碰
运⽓ " 的中间层；详见  §2.6.4.2 。
2. Persistent kernel + TMA multicast：
Persistent kernel 让  CTA 常驻  SM 、⾃⼰从全局  work queue 取任务，绕过硬件  CTA
调度器 —— 调度从硬件层下移到软件层，消除  wave 断层；
TMA multicast（ SM90+ ）让  cluster 内  N 个  CTA 共享⼀次  HBM 读，把  cluster ⼤⼩
内的  KV 重读从  L2 软期望升格为硬件合约（本仓库   hopper_helpers.py、blackwell_he
lpers.py  ⾥的  2CTA 指令）。
这两者叠加，把  L2 偶然命中的期望优化变成调度可控  + 多播确定的访存压榨 —— 从硬件调度
升级到软件定义调度。
````

## PDF 第 23 页

[原页](RAW.pdf#page=23)

````text
LSE 与  Online Softmax
上⾯提到了 FlashAttention 的返回值有 LSE ， LSE 是什么呢？
假设某⼀个  Query 与所有  Key 计算得到的原始点积得分（ Logits ）为向量  
。在数学上， Log-Sum-Exp 的原始定义是：所有元素指数和的对数：
但在⼯程上，直接算     会导致浮点数上溢（ NaN ）。因此我们要结合  Safe Softmax 的减
最⼤值技巧，令   。我们将    巧妙地拆解为   ：
\begin{align*}
\text{LSE}(z) &= \log \left( \sum_{j=1}^K e^{z_j} \right) &&\\
&= \log \left( \sum_{j=1}^K e^{z_j - m + m} \right) && \text{1. 引⼊最⼤值  $m$ ，凑出防溢出项 }
&= \log \left( e^m \cdot \sum_{j=1}^K e^{z_j - m} \right) && \text{2. 提取公共常数项  $e^m$} 
&= \log(e^m) + \log \left( \sum_{j=1}^K e^{z_j - m} \right) && \text{3. 根据对数乘法法则  $\l
&= m + \log\ell && \text{4. 化简  $\log(e^m)=m$ ，并代⼊局部和  $\ell$}
\end{align*}
⽽ Safe Softmax 的公式为： ，令分母为  ** ** （这正是  Online
Softmax ⾥的局部指数累加和）：
\begin{align*}
\text{Softmax}(z_i) &= \frac{e^{z_i - m}}{\sum_{j=1}^K e^{z_j - m}} && \text{1. Safe Soft
&= \frac{e^{z_i - m}}{\ell} && \text{2. 将分⺟替换为变量  $\ell$} \\
&= \frac{e^{z_i - m}}{e^{\log\ell}} && \text{3. 将分⺟强制改写为指数形式  $\ell = e^{\log\ell}
&= e^{(z_i - m) - \log\ell} && \text{4. 根据指数除法法则  $\frac{e^A}{e^B} = e^{A-B}$} \\
&= e^{z_i - (m + \log\ell)} && \text{5. 提取负号，组合出  $(m + \log\ell)$} \\
&= e^{z_i - \text{LSE}} && \text{6. 代⼊上⽅得出的  $\text{LSE} = m + \log\ell$ 结论 }
\end{align*}
所以公式变成了：
。额，这是在⼲嘛？这个公式有个⽑⽤？
事实上，利⽤  Online Softmax 机制存下     已经⾜以将    的全局读写降维⾄  
。但  FlashAttention 更进了⼀步：通过    的数学恒等代换，它将  2 个  FP32
变量进⼀步压缩为  1 个  FP32 标量（ LSE ）。
这个区区    ⼤⼩的单⼀变量数组，完美⽀撑了三⼤核⼼机制：反向传播时的     矩阵精准
重算（化除法为减法   ）、长⽂本推理时的  Split-K 局部归约合并，以及严格契合下游算
⼦（如  Cross-Entropy Loss ）的直接复⽤。这构成了  FlashAttention 空间复杂度优化的核⼼
基⽯。
为什么存  LSE （ log-sum-exp ）  ⽽不是分别存   ？
````

## PDF 第 24 页

[原页](RAW.pdf#page=24)

````text
Flash-Decoding 的  Split-K
在⾃回归的  Decode 阶段，参与计算的  Query 长度只有  1 。如果让单⼀  SM （流多处理器）
去独⾃处理长达⼏⼗万的历史  KV Cache ，会导致严重的算⼒闲置和极⾼的延迟。为了拯救
GPU 利⽤率， Flash-Decoding 引⼊了  Split-K （ KV 维度切分）技术：将长长的  KV Cache 切
⽚分发给多个不同的  SM （流多处理器）并⾏计算。
但不同  SM 算出来的局部  Softmax 是⽆法直接相加的，因为分母不同、局部最⼤值也不同。
各个  SM 独⽴计算后，向全局显存（ HBM ）写回⾃⼰的局部输出和局部状态。
⽽  LSE 的引⼊，使得各个  SM 只需要写回  1 个标量（ LSE ）⽽不是  2 个 ，将这部分
HBM 带宽开销砍半。 LSE (Log-Sum-Exp) 使得各个  SM 只需向全局内存写回⾃⼰这块碎⽚的
局部     和局部  LSE ，最后的  Reduction Kernel 就能利⽤  的数学特性，把不同  SM 的
结果完美缝合，最终形成全局真实的  Attention 输出。
反向传播中的重计算
在传统  Attention 的反向传播（求梯度）过程中，数学推导要求必须使⽤前向传播时算出的
Softmax 概率矩阵   。对于长⽂本来说，如果把这个庞⼤的    的     矩阵保存在全局显
存（ HBM ）⾥等反向传播⽤，显存会爆炸。  这⾥的 N 指的是序列长度。
但有了     这个公式， FlashAttention 可以⽀持：前向传播时，不存  
  矩阵，⽽是在 HBM 中存⼀个极度压缩的、⼤⼩仅为    的  LSE ⼀维数组。当反向传播需
要     时怎么办？直接在⽚上  SRAM 重算（ Recomputation ）。
我们只需要读取  Q 和  K 重算出局部点积  ，然后从  HBM 读出对应的  LSE 标量，做标量减法
和指数运算（），就精准还原出了。
如果没有 LSE ，我们需要从  HBM 读取   ，然后执⾏除法   。在  GPU 底层，除
法指令⽐较昂贵。但由于我们存的是  LSE 标量，重算公式变成了   。 LSE 利⽤对
数法则化除法为减法，虽仍需⼀次  SFU 指令计算指数，但省去了昂贵的除法指令，最重要的
是打破了  HBM 的带宽墙。
Sequence Parallelism (SP)
1. 省⼀半  HBM 写带宽： 1 个  fp32 vs 2 个  fp32 。前向出⼝每个  Q row 都要写⼀次，累
积起来不算⼩。
2. 恢复     更简洁： ，⼀条  FMA + exp2 ；若拆成     则要减  
  再乘   ，两步且需要两次加载。
3. 数学上等价、数值上稳定：因为    且     是实际的  running max ，
，  永远不会上溢。
假设  KV 被切成多个  shard ，每个  shard   得到局部输出     和局部  LSE ：  
全局  LSE 为： 最终输出不是简单相加，⽽是：  
````

## PDF 第 25 页

[原页](RAW.pdf#page=25)

````text
如今的⼤模型上下⽂长度动辄百万  Token 。当单卡显存⽆法容纳时，必须使⽤序列并⾏
（ Sequence Parallelism, SP ）或上下⽂并⾏（ Context Parallelism, CP ）。模型会被切⽚分发
给多张  GPU （甚⾄跨节点）计算。
⽐如在  Ring Attention ，在处理跨卡  Attention 时，若采⽤对局部输出     进⾏全局  Reduction
的⽅式，不仅通信模式难以流⽔线化，还引⼊昂贵的同步开销。因此， Ring Attention 选择在
环形拓扑中  P2P 传递  K 和  V 切⽚，每张卡保持本地  Q 不动。得益于  Online Softmax 的增量
修正机制，各卡只需维护极少的元数据（ LSE 标量），便能在接收到新  KV 切⽚时，本地完成  
 的⽆损在线更新，最终结果与全局  Attention 数值完全⼀致。这不仅避开了⾼昂的  All-
Reduce 通信，还实现了计算与  KV 传输的完美重叠（ Overlap ）。
Temperature ( ) 控制：Sampling  的  Softmax
LLM ⽣成时的   temperature 参数其实就是作⽤在  Softmax ⾥的：
 (低温 ): 差异被放⼤，分布变尖锐，模型更倾向于选概率最⾼的词（确定性⾼）。
 ( ⾼温 ): 差异被缩⼩，分布变平坦，模型更有可能选到低概率的词（创造性⾼）。
以上，通过  Softmax 算出的词表概率，加起来为  1 。我们要如何根据这个概率抽样？
⽬标：即已知⼀组概率   ，如果   ，那么有  80% 的概率抽到索引
1 。
Multinomial Sampling
常规做法（轮盘赌  / Multinomial Sampling ，即torch.multinomial）是⽣成⼀个    的均匀
随机数  ，然后去算    的累加和（ Cumulative Sum, 前缀和）。当累加到某个索引     时，总和
第⼀次超过了  ，就返回   。  问题：  在  GPU 上，要对长达  128,256 （ Llama3 词表⼤⼩）的
数组算前缀和，⾮常不利于极度并⾏的线程发挥，且存在显存同步开销。
Gumbel-Max Trick
背景知识
数学家证明了，只要给每个类别的对数概率     加上⼀个标准的  Gumbel 噪声，然后直
接取最⼤值（ argmax ），其结果与 Multinomial Sampling 在数学上是完全等价的！
那么，如何⽣成  Gumbel 噪声？最常见的⽅法是通过均匀分布   ：
````

## PDF 第 26 页

[原页](RAW.pdf#page=26)

````text
vLLM 中的 Gumbel-Max 的实现
为了兼顾硬件执⾏效率和数学严谨性， vLLM 使⽤了⼀个极其优雅的  Gumbel-Max Trick 变
体：
q = torch.empty_like(probs)
probs = logits.softmax(dim=-1)     # 1. 计算出概率分布
q.exponential_()                   # 2. ⽣成⼀个标准的指数分布噪声  q ~ Exp(1) 
probs.div_(q).argmax(dim=-1)       # 3. 将概率除以噪声，直接取  Argmax ！
img
由于对数函数     是单调递增的，求   argmax(p/q)  完全等价于求   argmax(ln(p/q))。将其展
开：
````

## PDF 第 27 页

[原页](RAW.pdf#page=27)

````text
标准指数分布     可以由均匀分布     通过     ⽣成。我们代⼊上式：
Amazing ，后半部分    恰好是前⾯提到的  标准  Gumbel 噪声！给对数概率加
上  Gumbel 噪声后再取最⼤值，在数学上已被严格证明等价于依据原概率分布进⾏采样。
这个数学转换在 Infra 视⾓上的价值是巨⼤的。它将 Multinomial Sampling 逻辑转化成适合
GPU 并⾏计算的操作：
1. q.exponential_(): 完全相互独⽴的随机数⽣成。
2. div_(): Element-wise （逐元素）的向量除法，没有任何数据依赖。
3. argmax(): 并⾏规约（ Reduction ）操作。
更近⼀步，通过这种做法，贪⼼采样（ Greedy ）和随机采样（ Random ）在代码执⾏流上被
彻底统⼀了：⽆⾮就是随机采样多做了⼀步除以噪声    的操作，最终全都是执⾏   argmax 寻
找最⼤值，消灭了底层  Kernel 的分⽀发散（ Branch Divergence ）。
在⼤模型词表动辄  128K~256K 的今天， vocab 通常会沿张量并⾏维度切分到多张  GPU 上。
此时如果⾛传统的  multinomial 采样路线，跨卡做⼀次全局采样代价并不⼩ —— 要么  all-
gather 整张  logits ，要么跨卡做  preﬁx-sum +   ⼆分查找，通信量和同步点都很难压下来。⽽
⼀旦换成  Gumbel-Max 形式的  argmax(logit + g) ，采样就退化成了⼀个满⾜结合律的  reduce
运算：每张卡只需在本地  shard 上算出局部最⼤值及其索引，再做⼀次廉价的  All-
Reduce(MAX with index) 即可拿到全局采样结果。通信量从  O(V) 直接降到  O(world_size) 。
TL;DR
其实本章⼀开始我是想放在开头的～但是我担⼼读者被吓跑，就移动到最后了。算是⼀个总结
吧。
深度学习模型中极⼤或极⼩的数值极易引发梯度问题或计算溢出，⽽神经⽹络真正关⼼的并⾮
数值的 “ 绝对⼤⼩ ” ，⽽是特征之间的 “ 相对差异 ” 。
1. LayerNorm 通过  平移（减去均值  ） + 缩放（除以标准差  ），将数据的均值归零，并将
数据的波动范围（⽅差）强⾏拉回  1 。
2. RMSNorm 则基于缩放⽐平移更关键的假设，去掉了平移，只保留对向量  RMS 尺度的归
⼀化，减少了⼤量的  element-wise 操作，还减半了  Reduce 的数据通信量和寄存器占⽤，
因此更适合极致的⾼性能  Kernel 实现。
Softmax 的核⼼原理是将⼀组任意的实数（通常称为  Logits ），转化为⼀套总和为  1 的概率分
布，同时放⼤差异。
argmax  返回的是⼀组数据中最⼤值所在的索引（位置下标），⽽不是最⼤数值本⾝。
````

## PDF 第 28 页

[原页](RAW.pdf#page=28)

````text
操作符 核⼼作⽤ 作⽤的物
理位置 作⽤的⽣命周期针对的维度
 ( 或   )
防⽌硬件层⾯的浮点
数上溢（ NaN ） -> s
afe
所有 Softma
x 训练  + 推理 硬件物理限制
 ( 上三⾓   )
因果掩码  (Causal M
ask)
仅  Attention
层
训练  + 推理 ( 仅 Preﬁll 阶
段， Decode 阶段不需
要显式  Causal Mask 因
为所有历史  KV 都应该
被看到 )
序列长度维度
 ( 乘以  scale 因
⼦ )
防⽌极值分布导致梯
度消失  -> soft
仅  Attention
层 训练  + 推理 隐藏层维度  ( )
 (Temperature)
控制⽣成⽂本的多样
性与随机性  -> soft
仅 Sampling
层 仅推理  ( ⽣成 ) 词表⼤⼩  ( )
Online Softmax
动态缩放修正
打破全局数据依赖，
将  3 Pass 访存降为
单次流式计算，极⼤
节省  HBM 带宽
底层  CUDA/
Triton Kerne
l
训练  + 推理
SRAM 缓存容
量约束下的分块
维度  (Block Til
e)
 ( 或    Gumbe
l 噪声 )
消除前缀和串⾏依
赖，将概率抽样转化
为  GPU 并⾏找最⼤
值
仅 Sampling
层 仅推理  ( ⽣成 ) 词表⼤⼩  ( )
Gumbel-Max ⽤加噪求最⼤值替代了传统的轮盘赌算法。它将原本需要串⾏计算前缀和的采
样过程，转化为完全独⽴的  element-wise 并⾏运算，打破了超⼤词表下的全局数据依赖。
⽆论是  Normalization 、 Softmax 还是 Gumbel-Max 相关操作，⼤模型推理底层优化的核⼼逻
辑始终如⼀：⽤数学等价变换、数值稳定重写、或经过验证的近似 / 架构简化，换取更好的访
存局部性、并⾏度和  kernel 融合空间。
总结
````

## PDF 第 29 页

[原页](RAW.pdf#page=29)

````text
img
以上，⼤模型的训练和结果输出都是不确定的，但是其数学原理是确定的。最近经常在想，当
前的 Transfomers 架构从效果上来说已经⾜够好 (Full Attention + MoE) ，  从⽽当今 AI Infra 主要
就是在不损失或者少损失效果的前提下做极致的性能优化。
⽐如上⽂提到的 online softmax 、 Gumbel-Max 、 RMSNorm ；
⽐如 FlashAttention 本质上是利⽤ IO Aware 、重计算提升计算强度；
⽐如 KV Cache 优化： MHA 、 MQA 、 GQA 、 MLA 、 KV Quant 、 SWA 、 DeepSeek V3.2-Exp 的
DSA （ Lightning Indexer + Top-K 稀疏选择）、 Linear Attention 、 TurboQuant 到 DeepSeek V4
的 CSA + HCA 这⾥的本质就是解决 1. 内存墙问题；  2. 显存容量问题； 3. 减少计算量；
⽐如 MoE  Scaling Law 模型不断增⼤，计算量随参数线性增⼤，⽽参数占⽐的⼤头⼜在 MLP
层，因此就把 MLP 层拆分，美其名⽈不同专家，每次执⾏仅激活部分参数 , 其本质就是在将现
有 FFN 层拆分成多个，然后增加路由，每次可以激活不同专家组，以减少计算量。
当前的⼤模型更多的是⼯程上的事情，⼤模型本⾝就是基于科学假设的实验科学。试错的速
度，往往决定了模型进化的速度。
当然这⾥的是试错不仅仅是训练，还包含 Test-Time Scaling: 在  AI 迈向  System 2 （慢思考）
和  Agent （智能体）的时代，推理不再是简单的单向吐字（ System 1 ），⽽是变成了复杂的搜
索、反思与⾃我进化过程。
（注：《 Tree of Thoughts (ToT) 》 - 来⾃姚顺⾬（腾讯  / 前  OpenAI / 普林斯顿博⼠  / 清华姚
班））
Reference
Online normalizer calculation for softmax
Root Mean Square Layer Normalization
````

## PDF 第 30 页

[原页](RAW.pdf#page=30)

````text
Flash-Decoding for long-context inference
Identity Mappings in Deep Residual Networks
Deep Residual Learning for Image Recognition
Understanding the difficulty of training deep feedforward neural networks
Language Models are Few-Shot Learners
Language Models are Unsupervised Multitask Learners
Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification
Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift
Efficient Memory Management for Large Language Model Serving with PagedAttention
Tree of Thoughts: Deliberate Problem Solving with Large Language Models
On Layer Normalization in the Transformer Architecture
Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters
OpenAI o1 System Card - System 1 -> System 2 Thinking
Ring Attention with Blockwise Transformers for Near-Infinite Context
Attention Is All You Need
FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness
FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning
FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision
FlashAttention-4: Algorithm and Kernel Pipelining Co-Design for Asymmetric Hardware Scaling
附 1: 常数  
常数  （约等于  2.71828 ）被称为欧拉数（ Euler's number ）或⾃然常数。与代表⼏何学中圆
的⽐例的    不同， 诞⽣于对“ 连续增长 ”这⼀概念的探索。要理解     是怎么来的，最经典、
最直观的例⼦就是复利计算。这个概念最早是由数学家雅各布 · 伯努利（ Jacob Bernoulli ）在
1683 年发现的。
1. 银⾏利息的极限（伯努利的发现）
假设有⼀家极其慷慨的银⾏，提供  100% 的年利率。你存⼊  1 元钱。
每年结算  1 次（单利）：
````

## PDF 第 31 页

[原页](RAW.pdf#page=31)

````text
⼀年后，你得到本⾦  1 元  + 利息  1 元  = 2 元。
公式：
每半年结算  1 次（复利）：
银⾏每半年给你  50% 的利息。
半年后：   元。
⼀年后：   元。
公式：
每季度结算  1 次：
每次利率为  25% ，⼀年结算  4 次。
公式：   元
每个⽉结算  1 次：
公式：   元
每天结算  1 次：
公式：   元
伯努利思考了⼀个问题：如果我们让结算利息的频率变得⽆限快（每⼩时、每秒、甚⾄是连续
不断的瞬间），最终的钱会⽆限增加吗？
答案是不会。随着结算次数     越来越⼤，最终的收益会逼近⼀个极限值，⽽这个极限值就是  
。
⽤严谨的数学微积分极限公式来表达就是：
2. 莱昂哈德 · 欧拉的贡献
虽然伯努利发现了这个常数，但真正赋予它灵魂的是伟⼤的数学家莱昂哈德 · 欧拉（ Leonhard
Euler ）。在  1720 年代，欧拉：
1. 正式命名了   **：他⽤字母     来代表这个常数（有⼈认为    代表  exponential （指数），也
有⼈认为只是他随便挑了⼀个没⽤过的字母）。
2. 证明了它是⼀个⽆理数：就像     ⼀样， 的⼩数部分是⽆限不循环的（
）。
3. 发现了计算    的新⽅法（泰勒级数）：
````

## PDF 第 32 页

[原页](RAW.pdf#page=32)

````text
欧拉发现，  可以通过⼀个⽆限连加的阶乘序列来极其精确地计算：
( 注：  和     都等于  1 ，所以开头是  1 + 1 + 1/2 + 1/6 + 1/24... 这种⽅法⽐复利公式收敛
得快得多。 )
3. 为什么     如此重要？
它的由来最经典的解释，源于  17 世纪数学家雅各布 · 伯努利（ Jacob Bernoulli ）对复利
（ Compound Interest ）的研究。
  在数学和科学中的地位，源于它在微积分中极其特殊的性质：指数函数    的导数，等于它
本⾝（）。
这意味着，当⼀个事物的增长率等于它当前的⼤⼩时（⽐如细胞分裂、⼈⼝增长、放射性物质
衰变、甚⾄是被热咖啡变凉的速度），它的⽣长轨迹就必然可以⽤     来描述。
简单来说： **   统治了圆和周期，⽽     统治了所有⾃然的、连续的增长与衰退。 **
附 2: FlashAttention 演进
技术维度
FlashAtte
ntion v1 (2
022)
FlashAttent
ion-2 (2023)
FlashAttention-3
(2024) FlashAttention-4 (2026)
⽬标硬件架
构
SM70/75/80
(Volta/Turin
g/Ampere)
SM80 (Amper
e) SM90 (Hopper) SM100/SM110 (Blackwell)
Grid 维度  /
⼤⼩
3D (batch_
size, num
_heads)
3D (num_m_
block, bat
ch_size, n
um_heads)
1D (num_sm,)，固
定  = SM 数（ H100
通常  132
1D (min(num_sm 对⻬  cl
uster_shape_m, total
_blocks_cluster · cl
uster_shape_m),)， B20
0 通常  = 148 ；持久化  + 1-C
TA / 2-CTA cluster ⾃适应对
齐
调度机制  (T
ile Schedul
ing)
传统  Grid/Bl
ock 静态映
射
改进的  Work
Partitioning
( 沿序列  M 维
切分 )
DynamicPersiste
ntTileScheduler
 / VarlenDynamicP
ersistentTileSc
heduler（ Persiste
nt + 动态分配，防尾
部效应）
**StaticPersistentTil
eScheduler**（ grid 限于
SM 数量的纯持久化内核）
循环遍历顺
序
外  K/V ，内
Q（ HBM 多
外  Q ，内  K/V 外  Q ，内  K/V 外  Q ，内  K/V （持久化  + 内
层  K/V 反向遍历  unroll=1 ）
````

## PDF 第 33 页

[原页](RAW.pdf#page=33)

````text
技术维度
FlashAtte
ntion v1 (2
022)
FlashAttent
ion-2 (2023)
FlashAttention-3
(2024) FlashAttention-4 (2026)
次写回中间
O）
矩阵乘指令
⼿写  HMMA
/ mma.syn
c PTX
CuTe mma.sy
nc (Ampere T
C)
WGMMA
 (wgmma.mma_asyn
c， Warp-Group
级， SS/RS 描述符 )
tcgen05.mma
 (Tensor Core Gen5) ，⽀持  *
*cta_group::1 / cta_gr
oup::2**（ 2-CTA cluster
协同， hdim=128 默认  2-CT
A）
数据异步搬
运 同步执⾏
cp.async
 (SMEM 流⽔
线 )
TMA ( 硬件异步传
输， producer warp
group 发起 )
TMA + 专属  Load Warp（ w
arp 14 单独承担  Q/K/V TM
A）
O 矩阵累加
位置
HBM ( 频繁
写回中间态 )
寄存器  (RF)
累积到底
寄存器  (RF) 累积到
底
TMEM
（张量内存，tmem_o_offs
et  每  q_stage 占  head_di
m_v_padded  列）
Softmax 归
约通信
依赖  SMEM
跨  Warp 同
步
寄存器内  __s
hfl_xor
寄存器内  __shfl_x
or
TMEM →  RF (tcgen05 t2r
copy) →  quad-wide warp_
reduction_max  →  RF →
TMEM (r2t copy) + fence_
view_async_tmem_stor
e
P 矩阵存储
位置 寄存器
寄存器  ( 编译
期  layout 变
换 )
寄存器  (RS 模式 ) 或
SMEM (SS 模式 )
TMEM
（tcgen05.OperandSour
ce.TMEM，直接作  PV-GEM
M 输⼊，免去  RF/SMEM 中
转）
Warp 任务
分配 同质化 同质化  ( 沿  M
维排布 )
**Warp-Group 级专
门化  (Producer / Co
nsumer)** ： 1 个  pro
ducer WG 发  TMA ，
1–2 个  consumer W
G 跑  WGMMA + soft
max
Warp 级专门化（逻辑  5 职  /
物理  6 组）
： MMA (warp 12) / Softmax
-0 (0–3) / Softmax-1 (4–7) /
Correction (8–11) / Epilogue
(13) / Load (14)
计算重叠流
⽔线 ⽆
Load/Comput
e 同⼀  Warp
内重叠
GEMM 间流⽔线
： PV (GEMM-II) 与
下⼀轮  QK (GEMM-I)
异步重叠； ping-pon
g 跨  WG
多级微架构流⽔线
：q_stage=2 Q 双缓冲  ∥
Softmax 双  warp 组并⾏处
理两条  Q 流  ∥  split_P  早
到机制（ P 写⼊  3/4 时  mbar
rier 提前  arrive ， PV-GEMM
与  softmax 尾段重叠）  ∥  C
orrection warp 异步修正先
前累加的  O
````

## PDF 第 34 页

[原页](RAW.pdf#page=34)

````text
附 3 ： SFU
在本⽂中，我们探讨了⼤模型推理中的两个核⼼数学操作： Normalization
（ LayerNorm/RMSNorm ）中的缩放因⼦   ，以及  Softmax 中的概率映射   。
从严谨的数学分类来看，⼆者属于完全不同的范畴：  属于代数函数（ Algebraic
Function ），因为它可以通过有限次的代数运算得出（满⾜多项式⽅程   ）；⽽  
  属于超越函数（ Transcendental Function ），它⽆法通过有限项的代数⽅程来表达，必须
依靠⽆限级数（如泰勒展开）来进⾏数学逼近。
然⽽，在  GPU 的底层体系架构中，芯⽚设计不遵循数学范畴的分类，⽽是以 “ 硬件指令的执
⾏复杂度 ” 为标准。
GPU 最核⼼的计算单元（ CUDA Core / Tensor Core ）针对矩阵与向量运算进⾏了深度定制，
其物理逻辑门主要⽤于执⾏极速的  FMA （ Fused Multiply-Add ，乘加融合）  指令。对于  
  这样的基础运算，标准  ALU 可以在⼀个时钟周期内完成吞吐。但是，⾯对开⽅
求倒数或计算⾃然指数这类⾮线性的复杂数学运算，标准的  ALU ⽆法在单⼀时钟周期内直接
计算得出。
为此， NVIDIA 在每个  SM （流多处理器）内部设计了专门的独⽴物理模块 ——SFU （ Special
Function Unit ，特殊函数单元）。在底层指令发射时，⽆论是代数函数层⾯的   ，还是
超越函数层⾯的   ，都会脱离常规的  ALU 乘加流⽔线，被分配给  SFU 来执⾏。
在物理实现上， SFU 并不进⾏真正的⽆限次级数展开，⽽是采⽤硬件查表（ Lookup Table,
LUT ）结合多项式插值（如⼆次逼近）的底层微架构。 Norm 层使⽤的快速平⽅根倒数指令
（如  CUDA 的   rsqrt）和  Softmax 使⽤的指数指令（如   exp2），都是通过  SFU 电路在有限
的⼏个时钟周期内直接逼近出⾼精度结果。
这种物理设计直接决定了模型算⼦的性能上限。由于⾮线性运算的电路⾮常消耗硅⽚⾯积，
NVIDIA 在每个  SM （流多处理器）内部署的  SFU 物理单元数量，远远少于普通的通⽤计算单
元（例如在  Hopper 和  Blackwell 架构中，每个  SM 有  128 个常规  FP32 单元，却仅仅只有
16 个  SFU ）。
RoPE cos_sin_cache
虽然不是矩阵乘法， sin/cos 属于超越函数，在  GPU 上由  SM 内的特殊函数单元（ SFU,
Special Function Unit ）执⾏。 SFU 的吞吐量通常仅为  FP32 ALU 的  1/4 。所以 VLLM 中不在
RoPE kernel 实时计算 sin/cos ，⽽是引擎初始化时按模型配置预计算好  cos_sin_cache ，
shape 为  [max_position_embeddings, rotary_dim] 。  RoPE kernel 运⾏时按  positions 索引出
对应的  cos/sin ⾏，与  Q/K 做逐元素乘加即可。本质是⽤⼀份⼩表（典型⼤⼩⼏  MB 到⼏⼗
MB ）换掉每次  forward ⼏百万次的  sin/cos 调⽤ —— 经典的空间换时间  / 访存换算⼒。
FlashAttention-4 软件模拟 exp
由于：
````

## PDF 第 35 页

[原页](RAW.pdf#page=35)

````text
1. FlashAttention 的出现提升了算术强度，缓解了内存墙问题，导致算⼒可以被充分利⽤ ( 特
别是 preﬁll 阶段逼近  Tensor Core 算⼒极限 ) ， SFU 需求同时上升；
2. SFU 物理单元数量本来数量就少， Blackwell 的  Tensor Core 算⼒翻倍飙升，但  SFU 却没
有获得同⽐例的扩展；
导致了⼀个反直觉的现象：算  Softmax ⾥    的耗时，竟然快赶上庞⼤的矩阵乘法（）
了！超越函数成为整条计算流⽔的瓶颈。
为了打破这⼀物理极限制约，最新的  FlashAttention-4 采取了软硬协同分流（ Partial
Emulation ）策略：既然硬件  SFU 算不过来，那就让通⽤  ALU 来分担：
FA4 在底层算⼦中，依然保留  75%~90% 的指令调⽤原⽣硬件  SFU （MUFU.EX2），但对于
溢出瓶颈的那  10%~25% 的数据， FA4 利⽤通⽤的  CUDA Core ，通过多项式逼近
（ Polynomial Approximation ）⽤最基础的乘加指令（ FMA ）模拟出    的结果。
为什么不  100% ⽤  ALU 软算？因为软件模拟会消耗宝贵的寄存器，全部软算会导致寄存
器溢出（ Spill ）从⽽反噬性能。 FA4 通过极其精准的⽐例调优，让  SFU 和  ALU ⾸次在超
越函数的计算上实现了完美的并⾏运转。
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
````

## PDF 第 36 页

[原页](RAW.pdf#page=36)

````text
阅读 5205
留⾔
还没有留⾔，来写⾸评
写留⾔
````

