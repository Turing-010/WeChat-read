# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
⻢斯克说到做到：开源 X 平台核⼼推荐算法
腾讯程序员 Feb  12 , 2026 , 1 : 39  AM⼴东原创 腾讯技术⼯程 548  listened
作者：腾讯⼴告推荐技术团队，周超博⼠
1 . 结论
●  X 开源的是内容推荐( Feed  on  X )的召回、精排的在线请求视⻆的推理、策略/过滤代码，
未开源训练(含 Loss 设计、样本组织的代码）。
●  模型参数配置较⼩（例如⽤户⾏为序列是 32 ），应是实际部署代码的简化 Demo 版本。推
测开源核⼼⽬的是为了体现 X 的透明性，解除⼴告主与 X 的⽤户对 X 的 Feed 推荐策略受到⾮
内容因素⼲扰的担忧。
●  召回
    ○双塔模型，⽤户塔是双层的 Decoder - Only 的 Transformer ，采⽤ Causal  Attention ，
Output 是取所有位置的平均池化( mean  pooling )，再进⾏ L2 的归⼀化；内容塔是两层的
MLP ；采⽤ dot  product 进⾏检索(因⽤户、内容都做了 L2 归⼀化，等价于 cosine )。
    ○  输⼊：⽤户塔【⽤户特征，⽤户⾏为序列 S ⻓度】，内容塔是帖⼦标识+帖⼦作者
●  精排
    ○ 双层的 Decoder - Only 的 Transformer ，对于⽤户特征、⽤户⾏为序列是 Causal
Attention ，对于候选是 Candidate  Isolation 。
    ○ 输⼊：【⽤户特征，⽤户⾏为序列 S ⻓度，候选 1 ，...，候选 N 】
●  召回、精排的⽤户 ID 、作者 ID 、帖⼦ ID 都⽤ multi - hash 查询 embedding  table 。
1 ， X 开源内容推荐 Feed  on  X 召回、精排推理、策略代码。参数配置⼩应是简化版本。 
2 ，召回是双塔模型，⽤户塔输⼊是【⽤户特征， S ⻓度的⾏为序列】，内容塔是帖⼦标识
与帖⼦作者。⽤户塔是双层的 Causal  Attention 的 Decoder - Only 的 Transformer ， Output 取
所有位置的平均池化，进⾏ L2 归⼀化；内容塔是两层 MLP ；采⽤ dot  product 检索。 
3 ，精排采⽤双层 Causal  Attention 的 Decoder - Only 的 Transformer 。精排输⼊是【⽤户特
征， S ⻓度⾏为序列，候选 1 ~候选 N 】，对候选采⽤ Candidate  Isolation 。
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
2 .背景
●  X (原 twitter )的开源项⽬：GitHub - xai-org/x-algorithm: Algorithm powering the For
You feed on X
●  " For  You " feed  on  X （内容推荐）:
●  只开源了推理视⻆的模型（召回、精排）、策略/过滤代码，没有开源训练的代码
（ Loss 、样本等）。
●  来⾃ Elon  Musk 本⼈的点评： We  know  the  algorithm  is  dumb  and  needs  massive
improvements , but  at  least  you  can  see  us  struggle  to  make  it  better  in  real - time
and  with  transparency. No  other  social  media  companies  do  this .
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
3 .架构
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
●  Home  Mixer ：整体系统的名字。
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
●  Query  Hydration ，获取⽤户的近期的历史⾏为与 Metadata （例如关注列表）:
    ○  User  Action  Sequence ，⽤户⾏为序列
    ○  User  Features ，关注列表等
●  Candidate  Sourcing ，从 2 个候选池拉取帖⼦
    ○  Thunder , In - Network  Posts ，关注的账号的帖⼦
    ○  Phoenix  Retrieval ， Out - of - Network  Posts ，全局贴⼦⾥基于相似度找到的
●  Candidate  Hydration ，为每个候选补充数据【⽂档⾥描述，代码⾥没有使⽤这些信息】
    ○  帖⼦数据：⽂本、多媒体
    ○  作者信息：⽤户名称，认证状态
    ○  视频时⻓
    ○  订阅状态，区分是否是订阅才可看的帖⼦
●  前过滤：
    ○  去除重复的、⽼帖⼦、⾃⼰的帖⼦、屏蔽的作者的帖⼦、屏蔽的关键词的帖⼦、过去看
过的帖⼦、不是订阅状态不可⻅的帖⼦。
●  Scoring
    ○  Phoenix  Scorer：
        ■  Grok - based  transformer  model ，包括两阶段，召回与排序。
        ■  19 个⽬标打分， P ( like )、 P ( reply )、 P ( repost )、 P ( click )等
○  weighted  scorer ，多⽬标分数融合，得到⼀个最终分数【权重参数未开源】
○  Author  diversity  Scorer ，作者多样性评分。
○  OON  Score ：对于不在订阅列表的帖⼦调整分值。
    ●  Selection
○  基于 Final  Score ，选取 Top - K 的候选
    ●  后过滤
○  重复的 PostID
○  Meta 信息获取不全的帖⼦
○  超过时效性的⽼帖⼦
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
○  ⽤户⾃⼰的帖⼦
○  内容⼀致的帖⼦
○  ⽤户没有订阅的帖⼦
○  ⽤户已经阅读过的帖⼦【已经阅读的过滤】
○  ⽤户在同 Session 已经曝光过的帖⼦【重复曝光过滤】
○  ⽤户屏蔽关键词的帖⼦
○  ⽤户屏蔽作者的帖⼦
○  已经被删除、识别为 spam 、识别为暴⼒等帖⼦。
○  对来⾃同⼀个 twitter 下多次交互的 conversation 进⾏去重
Thunder ：
●  存储于内存⾥的，记录所有⽤户的近期的帖⼦的存储
●  从 Kafka ⾥，记录帖⼦的创建、删除事件。
●  维持每个⽤户的原创帖⼦、回复、转发、视频帖⼦。
●  在“ in - network "检索中，提供⽤户关注的账号列表的获取。
●  ⾃动删除过期的帖⼦。
其他关键设计：
●  Hash - Based  Embeddings ：使⽤了多个 hash 函数来做 embedding  lookup 。应该是为了
解决 hash 冲突。
●  No  Hand  Engineered  Features ：没有内容相关性的⼈⼯设计的特征。
●  Candidate  Isolation  in  Ranking ：候选之间不能互相 attention 。
●  Multi - Action  Prediction ：多⽬标预估，⽽不是单⼀的相关性分数。
4 . Phoenix -模型整体
●  代码：x-algorithm/phoenix at main · xai-org/x-algorithm · GitHub
    ○  recsys _ retrieval _ mdel . py  ： Retrieval 召回模型
    ○  run _ retrieval . py ：召回模型运⾏示例
    ○  test _ recsys _ retrieval _ model . py ：召回模型测试
    ○  recsys _ model . py  ： Ranking 排序模型
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
    ○  run _ ranker . py ： 排序模型运⾏示例
    ○  test _ recsys _ model . py ：排序模型测试
    ○  grok . py : Transformer 基础架构(基于 Grok - 1 在内容推荐场景改造)
    ○  runners . py ： 模型推理逻辑
●  两阶段：召回，排序。
●  应⽤于 Feeds 的内容推荐。
5 . Phoenix -模型-召回
●  双塔模型，应⽤于从⾮⽤户关注的账户⾥检索潜在感兴趣的帖⼦，百万级别候选，返回
千级别候选
●  User  Tower ：
    ○  【⽤户特征，⽤户历史⾏为 1 ，⽤户历史⾏为 2 ...，⽤户历史⾏为 S 】。
    ○  Decoder - Only  Tranformer , 异构序列的输⼊， Causal  Self - Attention ，每个位置可以
看到⾃⼰及之前的信息。
    ○  Output 是取所有位置的平均池化( mean  pooling )，再进⾏ L2 的归⼀化。【⾮ Next  Item
Prediction 】
●  Candidate  Tower ：
    ○  特征是候选帖⼦唯⼀标识+候选帖⼦作者标识
    ○  2 层 MLP ： Linear  ( x2  拉宽) -> SiLU 激活 -> Linear  ( projection )。
    ○  L2 归⼀化
●  Similarity  Search ：
    ○  通过 dot  product ，检索 Top  K 的结果。因为⽤户 Emb 已经经过 L2 归⼀化，等价于 cosine
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
similarity 。
●  ⽤户特征：
    ○  user _ hashed ：⽤户唯⼀标识，通过多个哈希函数映射, num _ user _ hashes
    ○  多个哈希查询的 embedding 进⾏拼接，再⽤可学习的权重矩阵 Projection 投影到 D 维
    ○  ⽆效的⽤户 padding 为 0
●  ⽤户历史交互⾏为，⻓度为 S ，每个对象的 Sideinfo 如下：
    ○  历史帖⼦的 TwitterID ，每个帖⼦有多个哈希函数, num _ item _ hashes
    ○  历史作者的 AuthorID ，每个作者有多个哈希函数, num _ author _ hashes
    ○  历史⾏为类型，⼀共 19 种。是经过投影矩阵得到。
    ○  产品界⾯ ID ，表达来⾃哪个界⾯。通过 one - hot 单热编码⽅式查表得到。
    ○  先 concatenate ，序列上每个位置，再⽤可学习的权重矩阵 Projection 投影到 D 维
    ○  序列⻓度不⾜ S 的， Padding 到 S 个
●  候选帖⼦特征：
    ○  候选帖⼦唯⼀标识，通过多个哈希函数映射， num _ item _ hashes
    ○  候选帖⼦作者标识，通过多个哈希函数映射, num _ author _ hashes
    ○  先 concatenate ，再⽤可学习的权重矩阵 Projection 投影到 D 维
    ○  候选不⾜ C 的， Padding 到 C 个
●  训练精度： BF16 + FP32
●  模型参数配置：
    ○  emb _ size  = 128
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
    ○  history _ seq _ len  = 32
    ○  candidate _ seq _ len  = 8
    ○  num _ user _ hashes  = 2
    ○  num _ item _ hashes  = 2
    ○  num _ author _ hashes  = 2
    ○  产品界⾯词表⼤⼩： 16
    ○  FFN 扩展因⼦： 2
    ○  注意⼒键维度： 64
    ○  Query 头数量： 2
    ○  Key / Value 头数量： 2
    ○  Transformer 层数： 2
    ○  注意⼒输出缩放系数： 0 . 125
6 . Phoenix -模型-排序
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
●  ⽤户特征：与 Retrieval ⼀致。
●  帖⼦特征：
    ○  在 Retrieval 基础上，多了⼀个上下⽂特征，候选帖⼦将在哪个产品界⾯展示给⽤户。
●  Transformer  with  Candidate  Isolation （候选隔离的注意⼒机制），⽤ special
attention  masking 来对候选进⾏屏蔽，使得候选帖⼦之间不会互相影响[ Candidate
Isolation ]。
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
    ○  基于代码来看，上述官⽹的示意图表述不准确，⽤户与⽤户⾏为序列是 Causal
Attention ，⾮ Full  Birectional  Attention 。
    ○  正确版本示意图如下：
○  模型输⼊：⽤户特征、⽤户历史⾏为序列、多个候选帖⼦
○  模型架构： Decoder  Only  Transformer
      ■  ⽤户特增、⽤户历史⾏为： Causal  Attention 。
      ■  候选->⽤户、⽤户历史⾏为、候选：
        ●  候选可以关注所有⽤户特征、⽤户历史⾏为
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
        ●  对候选是只能看到⾃⼰，不能看到其他候选
      ■  采⽤ Pre  Norm  + Post  Norm
      ■  FFN 采⽤ SwiGLU  FFN ： FFN  ⼤⼩ 2 . 67  ×  D （因为 SwiGLU  有两条路径）
    ■  抽取⽤户的 history 之后的候选位置的输出，该位置表达每个候选的 Output 。
    ■  乘以[ Hidden _ Dim , num _ actions ]形状的权重矩阵，得到每个候选帖⼦在每种 action 的原
始 logit
    ■  Logits  处理： Soft  Capping  ，⽤ tanh  将 logits  平滑压缩到 [- M , M ]
    ■  sigmoid 函数将原始 logit 转为[ 0 , 1 ]
    ■  RMSNorm
    ■  RoPE 位置编码， RotaryEmbedding
    ■  Grouped  Query  Attention：实现了能⼒，实际配置 KV 头数= Q 头数。 GQA 的例⼦如
下：
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
○  输出：
    ■ [ batch _ size , num _ candidates , 19 ]
    ■  使⽤其中 1 个 action 作为主排序。
●  模型参数
    ○  emb _ size  = 128
    ○  history _ seq _ len  = 32
    ○  candidate _ seq _ len  = 8 ，⼀次排序的最⼤候选
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
    ○  num _ user _ hashes = 2
    ○  num _ item _ hashes = 2
    ○  num _ author _ hashes = 2
    ○  widening _ factor = 2 , # FFN  扩展因⼦
    ○  key _ size = 64 ,# 注意⼒键维度
    ○  num _ q _ heads = 2 ,
    ○  num _ kv _ heads = 2 ,
    ○  num _ layers = 2 , # Transformer  层数
    ○  attn _ output _ multiplier = 0 . 125 , # 注意⼒输出缩放
●  Weighted  Scorer ，加权线性求和【权重未开源】
    ○  正向⾏为： like , repost , share
    ○  负向⾏为： block , mute , report
如对腾讯⼴告技术感兴趣
可以关注“腾讯⼴告技术”微信公众号
腾讯⼴告技术官⽅阵地，分享团队最新前沿成果及⼴告技术应⽤。
230 篇原创内容
腾讯⼴告技术
公众号
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
阅读 1 . 2 万
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
留⾔
还没有留⾔，来写⾸评
写留⾔
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
````

