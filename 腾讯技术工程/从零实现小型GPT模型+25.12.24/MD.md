# 教你从零“手搓”一个大模型，别再只会调用API了

来源：[RAW.pdf](RAW.pdf)，capture-001。

这是PDF文本层按物理页码转写，不是AI总结。图片未嵌入；图内文字、截图、公式、表格及代码排版可能未提取或不可靠；源PDF中存在的右侧裁切不补写。实际复核范围详见META.json。

## PDF物理页 1

教你从零“⼿搓”⼀ 个 ⼤模型，别再只会调⽤              API了


原创 腾讯程序员  腾讯技术⼯程   2025年12⽉24⽇  01:36⼴东 2531⼈
















作者： yongzheng，patrickguo



  在⼤模型满天飞的今天，我们是⽢⼼做⼀个只会调⽤           OpenAI.chat.completions 的 API
  搬运⼯，还是想真正弄懂那个⿊盒⼦⾥到底发⽣了什么？本⽂将⽤最朴素的代码，完整的
  实现⼀个⼩型LLM。当你亲⼿写出 Attention 层的矩阵乘法，亲眼看到模型从输出乱码到
  学会说话，你会发现：⼤模型，其实也没那么可怕。


























RoadMap








  1. 引⾔

1.1 背景

## PDF物理页 2

在部门浓厚的AI技术探索氛围驱动下，为了将晦涩的理论转化为直观的⼯程触感，我们开展⼀
次略带“整活”性质的实践。希望通过从零“⼿搓”的⽅式，在满⾜⼯程师好奇⼼的同时，帮助⼤
家打破对⼤模型的神秘感，真正理解其底层的运⾏机制与实现原理。

1.2 内容说明

  简单但完整的模型结构，结构主要参考      GPT2，从零构建。

  介绍模型结构以及代码实现，尽量规避数学与复杂的算法。

  个⼈⾮科班的业余爱好者，靠各种碎⽚信息修炼的邪修，可能会对⼀些术语不了解，请见
  谅。

  适应⼈群 : 对于智商超群的算法同学来说可能有些幼稚，但对终⽇加班，⽬光涣散的开发
  苦哥们来说刚刚好。

  主要参考资料  : 《Build a Large Language Model (From Scratch)》 和 CS336: Language
  Modeling from Scratch 更多资料详见                           ⽂末。

1.3 模型结构概览




































                      Q DogBaby模型结构

现在看起来⼀头雾⽔没关系，接下来我们来逐步拆解模型，瞧瞧这些到底是怎么个事。

1.4 HelloWorld

⾸先，给我们的模型起个名字，然后做⼀个简单的逻辑，我们的第⼀个             LLM就诞⽣了。开发
嘛，实⽤优先  (⼜不是不能⽤  )

## PDF物理页 3

 class QdogBaby整活():

    def chat(self, text):

        if text.endswith('吗？'):

            return text.replace('吗？', '!')

        return text

 model = QdogBaby整活()

 print(model.chat('会说话吗？'))

 print(model.chat('是⼈⼯智能吗？'))






   会说话!
   是⼈⼯智能! -->


这个“⼈⼯”智能最⼤的问题在于：它不懂语义，只是在做字符替换。它⽆法理解“今天天⽓不
错”和“风和⽇丽   ”之间的联系，更⽆法                                           ⽣成它没见过的句⼦。

真正的 LLM 是⼀个概率模型。它不是在查找答案，⽽是在根据上⽂，预测下⼀个字最可能是
什么。

为了实现从“   逻辑处理  ”到“概率预测”   的转变，我们⾸先要解决第⼀个问题：如何把⼈类的语
⾔，翻译成模型能理解的语⾔？



 2. 编码Tokenizer

2.1 引⾔

正如我们第⼀部分所说，LLM        是⼀个概率模型，通过数学计算来进⾏下⼀个字的预测。然
⽽，计算机只认识数字（0和1），并不认识"今天"、"天⽓"或者"Today"这些单词。因此，想要
让计算机能够理解⼈类的语⾔，需要通过特定的编码机制将⾃然语⾔翻译成模型能运算的数字

## PDF物理页 4

序列。分词器（Tokenizer）是实现这⼀功能的核⼼组件，它能够将连续⽂本拆解为离散语义
单元（即  Token）并转换为唯⼀索引（    Token ID）⽤于模型输⼊。

所有 LLM 的输⼊都依赖 Tokenizer 的预处理结果。如果分词策略不合理，如拆分后丢失语义
或 Token 粒度过细，会直接影响模型对⽂本的理解能⼒。因此，⼀个设计优良的 Tokenizer 是
提升  LLM 性能的基础前提。

2.2 Tokenizer分类

根据切分粒度的不同，Tokenizer   可分为三⼤类：字符级      Tokenizer（Character-level）、词级
Tokenizer（Word-level）以及⼦词级  Tokenizer（Subword-level）。我们以句⼦  "Today  is
sunday." 为例，看看它们是如何⼯作的。

字符级  Tokenizer（Character-level）

核⼼：以单个字符作为最⼩语义单元进⾏拆分，不依赖词典或复杂规则。

分词结果：   [T, o, d, a, y, i, s, s,u, n, d, a, y, .]

优点：词汇表规模⼩，任何⽂本均能拆分，适配性强

缺点： Token序列长，信息密度低，碎                                                      ⽚化严重，解码效率偏低

词级  Tokenizer（Word-level）

核⼼：以单个词语为最⼩语义单元进⾏拆分，通常使⽤空格或者标点符号进⾏分隔。

分词结果：   [Today, is, sunday, .]

优点：单元语义完整，序列长度较短，信息密度⾼，模型⽆需学习字符组合关系。

缺点：词表规模庞⼤，训练成本升⾼。同时，若单词未出现在语料或词典中，会出现
OOV(out-of-vocabulary)的现象。

⼦词级  Tokenizer（Subword-level）

核⼼：介于字符级与词级之间，常见的词保留完整，不常见的词拆分成有意义的⽚段（词根、
词缀）  。

分词结果：   [To, day, is, sun, day, .]

优点：词汇表规模可控，序列长度介于两者之间，能学习词缀、词根之间的关联，平衡了信息
密度与计算效率，同时有效缓解了        OOV问题。

缺点：分词逻辑较上述两者复杂；对低频⼦词的拆分可能不够合理，需通过优化算法进⾏改
善。

⽬前， ⼦词级   Tokenizer 是 LLM 的主流选择                     。

2.3 BPE算法原理

## PDF物理页 5

⽬前最流⾏的⼦词分词算法是 BPE (Byte Pair Encoding)。它的核⼼逻辑与⼈类学习语⾔的过
程相似：先认字，再组词。从最⼩的字符单元出发，反复合并语料中频率最⾼的相邻单元对，
逐步扩展词汇表，直⾄达到预设词汇表⼤⼩或下⼀个⾼频出现的字符对频率为                       1时停⽌。

具体⽰例：

初始语料：    [apple, apple, banana, banana, grape, grape, grapes]

步骤1：预处理，为原始语料中的每个单词添加后缀                </w>作为分隔符，并将所有单词拆分为
字符作为初始分词单元。

   [a,p,p,l,e,</w>] (2次)

   [b,a,n,a,n,a,</w>] (2次)

   [g,r,a,p,e,</w>] (2次)

   [g,r,a,p,e,s,</w>] (1次)

步骤 2：初始化词汇表，此时词汇表仅包含独⽴字符与单词后缀。





 V = {a, b, e, g, l, n, p, r, s, </w>}


步骤 3：进⾏第⼀次合并。

步骤 3.1：统计所有相邻单元对及其频率，需要叠加单词重复次数。

   [a,p,p,l,e,</w>] (2次)：相邻对为(a,p)、(p,p)、(p,l)、(l,e)、(e,</w>) 各2次

   [b,a,n,a,n,a,</w>] (2次)：相邻对为(b,a)、(a,n)、(n,a)、(a,n)、(n,a)、(a,</w>) 各2
  次

   [g,r,a,p,e,</w>] (2次)：相邻对为(g,r)、(r,a)、(a,p)、(p,e)、(e,</w>) 各2次

   [g,r,a,p,e,s,</w>] (1次)：相邻对为(g,r)、(r,a)、(a,p)、(p,e)、(e,s)、(s,</w>) 各1
  次

各单元对出现的频率依次为：         5次(a,p)、4次(a,n) 、4次(n,a)、4次(e,</w>) 等。

步骤3.2：选择频率最⾼的相邻对进⾏合并，当前              (a,p)出现次数最多，因此把       ap作为⼀个新
元素加⼊词汇表，并进⾏词汇表的更新。





 新词汇表：V = {ap, a, b, e, g, l, n, p, r, s, </w>}


步骤 3.3：⽤合并后的词汇表重新进⾏单词的拆分。

   [ap, p, l, e, </w>] (2次)

   [b, a, n, a, n, a, </w>] (2次)

## PDF物理页 6

  [g, r, ap, e, </w>] (2次)

  [g, r, ap, e, s, </w>] (1次)

步骤4：依次类推，重新统计各元素出现的频率，重复步骤3进⾏合并，直⾄达到预设词汇表
⼤⼩或下⼀个⾼频出现的字符对频率为         1时停⽌。

最终分词逻辑：经过上述步骤得到词汇表后，按照              Token长度进⾏排序，优先匹配最长的
Token，如果匹配上则进⾏替换，直到                                单词的所有字符都被替换为词表中的Token为⽌。

2.4 编码

分词仅仅是第⼀步，计算机仍然不认识分词结果。我们需要将其转化为数字索引。在模型训练
前，我们会⽣成⼀个巨⼤的映射表，给每⼀个           Token 分配⼀个唯⼀的  ID。如：

 Token                          ID

 ...                            ...

 apple                          1023

 to                             1024

 is                             1025

 ...                            ...

 grape                          2045

 day                            2046

 sun                            2047

 ...                            ...

 banana                         8786

 ...                            ...


随后，我们可以对⽂本进⾏最后⼀步转换了。输⼊⽂本："today is sunday"，我们将其分为             ['t
o', 'day', 'is', 'sun', 'day']，查表映射，输出结果为[1024, 2046, 1025, 2047, 2046]。⾄此，我们
解决了⼈机交流的第⼀道障碍，⽂本已经变成了整齐的数字序列。

接下来，我们需要把这些数字喂给模型，让它开始真正的             "计算 "。


      腾讯技术⼯程
      腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
      689篇原创内容


 公众号


 3. 模型 LLM Model

3.1 引导: 单字处理的窘境

## PDF物理页 7

将字转化为token_id之后，我们终于可以对⽂字做计算了，于是乎我搞了⼀个翻译模型，这个
模型找到了汉字与单词之间的对应关系，会将给定的英⽂                token，转化为中                     ⽂token，⽐如:





 model = QdogBabyTranslate()

 print(model.translate("I like penguin"))

 print(model.translate("We all like penguin"))






   我喜欢⼩企鹅

   我们都喜欢⼩企鹅


我觉得很开⼼，于是我拿去⽤，发现          :





 print(model.translate("How are you"))

 print(model.translate("How old are you"))






   怎么是你

   怎么⽼是你


感觉哪⾥怪怪的，它把 'old' 翻译成了 '⽼'，完全没看 'How' 和 'are' 的脸⾊！也就是说我们现
在的每个字，只关注了他⾃⼰本⾝，却忽略了对话上下⽂，我们希望当前的⽂字可以注意到其
他的⽂字。

3.2 embedding

在建⽴字与字的关系之前，还需要解决⼀个问题: 数字本⾝是没有语义的。我们将“我喜欢⼩企
鹅”转换成了 [397, 2320, 3169, 2665, 1270]。但对模型来说，只是五个整数，它并不知道 397
（我）和 2320（喜欢）之间有什么关系。如果我们直接⽤这些整数去计算，模型会“懵圈”。
所以，我们要   给每个   Token ID 做⼀次升维，把⼀个                                           ⼲巴巴的整数，变成⼀个⾼维向量。

⾸先需要准备⼀个巨⼤的表格，⽐如词表⼤⼩是 6400，维度是 512，那就是⼀个 6400 x 512
的数字矩阵，然后我们就可以通过最简单的查表的⽅式，将                  Token ID 映射成⼀个⾼维向量。

## PDF物理页 8

此外，还有⼀个关键点：Transformer               是  “脸盲  ”的。它并⾏处理所有输⼊，如果不加特殊处
理，它⽆法区分         “我喜欢⼩企鹅        ”和 “⼩企鹅喜欢我        ”的区别（词都⼀样，只是顺序不同）。因
此，我们还需要⼀个位置映射表（                  Positional Embedding），把    “位置信息    ”也加到向量⾥去。





  from transformers import AutoTokenizer

  import torch



  tokenizer = AutoTokenizer.from_pretrained("./tokenizer")

  input = tokenizer.encode("我喜欢⼩企鹅", return_tensors='pt')

  print(input)



  tok_emb = torch.nn.Embedding(num_embeddings=tokenizer.vocab_size, embedding_dim=512)

  # 这⾥由于字在不同的位置，含义是不⼀样的，所以需要⼀个位置嵌⼊，来区分不同的位置

  pos_emb = torch.nn.Embedding(num_embeddings=512, embedding_dim=512)

  print(tok_emb(input)+pos_emb(torch.arange(input.shape[1])))






  tensor([[ 397, 2320, 3169, 2665, 1270]])

  tensor([[[-0.5469, -2.2388,  0.8119,  ...,  0.3477,  0.0979, -1.2581],
           [-0.3531, -0.4719, -0.0993,  ..., -2.6921, -1.4172,  0.4816],

           [-1.1212, -0.8914, -0.0145,  ..., -1.3678, -1.0177, -0.8076],

           [-0.1734,  1.6962, -2.1702,  ...,  0.1568,  1.6497, -0.1667],

           [-0.3965, -0.2542, -0.1799,  ...,  0.3170,  0.5109, -1.2761]]],

         grad_fn=<AddBackward0>)


你可以将这个操作理解为，将token在空间中展开，这样我们能更明显的感知到token之间的关
系

## PDF物理页 9

另外，在token向量化后，我们发现可以形象的对token进⾏计算了，某种意义上可以完成这样
的操作:

妈妈+哥哥=舅舅

国王-男+⼥=王后

巴黎-法国+意⼤利 =罗马






















3.3 Attention

coding start: 这部分会涉及到⼀些编码，可能会⽐较繁琐⽆聊，但我认为还是有必要的，其
他部分代码均有删减，但这部分保留了。

3.3.1 朴素的Attention

如何找到token与token之间的关系？回到我们刚刚embedding后的空间，如果我们在空间中建
⽴⼀个坐标系，会发现，当两个向量含义相近时，他们的点积会⽐较⼤，⽽两个向量没什么关
系时，它们的点积会是  0甚⾄负数 .

## PDF物理页 10

我们可以利⽤这个特性，将句⼦中的每个 Token 与其他所有 Token 进⾏点积运算(请注意这⾥
的token是⼀个多维度的向量        )，以此来                计算这两个词的关系"好不好"。

向量点积的本质是空间投影，但对被需求淹死了的开发哥们来说存在理解难度，因此我们拿出
初中知识，简单理解为离得近了            (⽅向 )点积⼤，离得远了      (⽅向  )点积⼩
















图中为序列 "Your journey starts with one step"中第⼆个token"journey"的计算过程 (这⾥使⽤
了原书中的例⼦，感兴趣的同学可以去阅读⼀下原书，讲解的⼗分详细                          )






















 inputs = torch.tensor(

   [[0.43, 0.15, 0.89], # Your     (x^1) - 第⼀个token的嵌⼊向量

    [0.55, 0.87, 0.66], # journey  (x^2) - 第⼆个token的嵌⼊向量

    [0.57, 0.85, 0.64], # starts   (x^3) - 第三个token的嵌⼊向量

    [0.22, 0.58, 0.33], # with     (x^4) - 第四个token的嵌⼊向量

    [0.77, 0.25, 0.10], # one      (x^5) - 第五个token的嵌⼊向量

    [0.05, 0.80, 0.55]] # step     (x^6) - 第六个token的嵌⼊向量

## PDF物理页 11

  )

  dim = inputs.shape[1]



  attn_scores = torch.empty(6, 6)



  # 计算注意⼒分数矩阵：遍历所有token对，计算它们之间的点积相似度

  # 外层循环：遍历每个token作为查询(query)

  for i, x_i in enumerate(inputs):

      # 内层循环：遍历每个token作为键(key)

      for j, x_j in enumerate(inputs):

          # 注意这⾥的token是⼀个多维度的向量，所以要展开计算

          dot_product = 0.0

          # 遍历向量的每个维度进⾏计算

          for k in range(len(x_i)):

              dot_product += x_i[k] * x_j[k]



          attn_scores[i, j] = dot_product


上⾯那⼀坨坨代码，可以写成下⾯这种矩阵相乘的形式，⼀⾏搞定。除了代码简化外，矩阵的
计算还可以充分利⽤显卡的并⾏计算能⼒

(感兴趣的⼩伙伴可以改⼀下这两段代                                                                           码，测⼀下性能差距)





  # inputs 形状: [seq_len, dim]

  # inputs.T 形状: [dim, seq_len]

  # 结果 attn_scores 形状: [seq_len, seq_len] -> 得到了⼀个 N*N 的关系矩阵

  attn_scores = inputs @ inputs.T # query @ key

  attn_scores






      tensor([[0.9995, 0.9544, 0.9422, 0.4753, 0.4576, 0.6310],

          [0.9544, 1.4950, 1.4754, 0.8434, 0.7070, 1.0865],

          [0.9422, 1.4754, 1.4570, 0.8296, 0.7154, 1.0605],

          [0.4753, 0.8434, 0.8296, 0.4937, 0.3474, 0.6565],
          [0.4576, 0.7070, 0.7154, 0.3474, 0.6654, 0.2935],

          [0.6310, 1.0865, 1.0605, 0.6565, 0.2935, 0.9450]])


经过这样的计算后，我们得到了⼀个代表了词与词之间关系的矩阵，接下来还需要做两步操
作: Softmax 归⼀化     和 加权求和    。

由于原始的数据点积数值范围⾮常⼤，直接使⽤会使我们的计算结果不稳定，Softmax 的作⽤
就是把这些乱七⼋糟的分数变成“百分⽐（”                  概率分布），让它们加起来等于 1。这样我们就得到
了每个词的权重，⽽加权求和则是真正的按这些权重，将我们需要的信息融合到⼀起。

## PDF物理页 12

 # 1. Softmax: 将分数转化为概率（权重），相当于分配注意⼒⽐例

 # ⽐如：[0.1, 0.8, 0.1] 表示主要关注中间那个词

 attn_weight = torch.softmax(attn_scores, dim=-1)

 # 2. MatMul: 根据权重，提取并融合信息

 # 权重⼤的向量会被更多地“吸取”进来，权重⼩的则被忽略

 context_vec = attn_weight @ inputs


3.3.2 增加权重
























我们⽤⼀个⼩例⼦来通俗的理解⼀下attention计算的整个过程: 我们现在有⼀个会议室，然后
来了⼏个token来开会，每个token在会议室门⼝根据会议室的规则(W_q, W_k, W_v)领到了三
个⾓⾊ :

Query: 提问者，当轮到他发⾔时，他会说出他需要的信息，⽐如"关于‘⼴告推荐架构’这个问
题，谁有经验？    "。

Key: 回答者, 当他被提问时，他会说出                                                他对外的标签，⽐如"运维、后端、算法、美术"。

Value: 信息本⾝，如果他被选中了，他会将⾃⼰的信息贡献出来。

会议开始后，⾸先Query和Key关于当前的问题进⾏沟通，得到需要信息的⽐例，⽐如                       "运维
0.2、后端 0.4、算法  0.4、美术 0"，对齐之后按照信息⽐例，把需要的Value          获取到并融合起

## PDF物理页 13

来。会议结束时，每个⼈都通过这种⽅式，从其他⼈那⾥吸收了⾃⼰需要的信息，完成了信息
的融合。

⽽⽤于讨论的会议室(W_q, W_k, W_v)，不是天然就存在的，需要我们使⽤我们训练的语料⼀
点⼀点的盖起来。





 dim = inputs.shape[1] # 词向量维度

 # 定义三个可训练的参数矩阵

 # 在实际 PyTorch 源码中，通常使⽤ nn.Linear 实现

 W_query = torch.nn.Parameter(torch.rand(dim, dim))

 W_key   = torch.nn.Parameter(torch.rand(dim, dim))

 W_value = torch.nn.Parameter(torch.rand(dim, dim))

 # 1. 线性变换：将输⼊映射为 Q, K, V

 querys = inputs @ W_query

 keys   = inputs @ W_key

 values = inputs @ W_value

 # 2. 计算注意⼒分数 (Scaled Dot-Product Attention)

 # [seq_len, dim] @ [dim, seq_len] -> [seq_len, seq_len]

 attn_scores = querys @ keys.T

 # 3. 缩放 (Scaling) 与 归⼀化 (Softmax)

 # 除以根号 dim，防⽌数值过⼤

 scale_factor = keys.shape[-1] ** 0.5

 attn_weights = torch.softmax(attn_scores / scale_factor, dim=-1)

 # 4. 加权求和得到上下⽂向量

 # [seq_len, seq_len] @ [seq_len, dim] -> [seq_len, dim]

 context_vec = attn_weights @ values


coding end: 到这⾥就可以愉快的继续看图了

3.4 mask 和 dropout

我们的模型还存在着⼀个明显的问题，就是"看答案"。对于⼀些⽂本处理类任务，⽐如相关性
计算、实体提取，会提前给定全部的语句，这种使⽤全部的token计算attention权重是没有问
题的，但我们的模型是要"说话"的，在说出下⼀个字之前，没⼈知道后⾯要说什么。因此在计
算权重时，我们要给当前词之后的词，都                "遮起来   "。

## PDF物理页 14

另外还有⼀种⼿段，会在计算过程中随机丢弃⼀些权重，可以防⽌模型过拟合，通俗的说就是
我们希望模型可以学到知识，⽽不是背课⽂。

PS: 早期 GPT-2 和 Qwen-14B 采⽤了这个⽅式，但最新的 qwen3 kimi-2   等模型均将此参数
设置为 0
























3.5 MultiHeadAttention

























这⾥为什么最后要加⼀层      linear将矩阵          转成原来的形状？因为我们要开始叠层了~

3.6 Transformer

我们参考  2017年的著名论⽂《   Attention Is All You Need》https://arxiv.org/abs/1706.03762

来设计我们的transformerblock，相对于论⽂原始结构，我们将           Norm层提前，这是⽬前
LLaMA、Qwen 等主流⼤模型普遍采⽤的结构，⽐原始 Transformer 的 Post-Norm 训练更稳
定。

## PDF物理页 15

3.6.1 Feed Forward





















  class FeedForward(nn.Module):

      def __init__(self, emb_dim, dropout):

          super().__init__()

          self.linear1 = nn.Linear(emb_dim, emb_dim * 4)

          self.linear2 = nn.Linear(emb_dim * 4, emb_dim)



      def forward(self, x):

          x = self.linear1(x)

          x = nn.GELU()(x)

          x = self.linear2(x)

          return x


这⾥的    FeedForward主要负责两件事情                 :

 1. 增加了⾮线性的激活函数                  GELU()

## PDF物理页 16

关于激活函数，不做过多展开，可以先简单理解为不加⾮线性函数的话，多层数学上就等价于
单层，层数就叠不起来。

2. 通过Linear将维度升为 4 * dim，假设          我们的模型维度为512，那么这⾥的维度就是2048。
  (这⾥的4倍有说法的，感兴趣的同学可                                                                以研究⼀下)

这⾥的主要⽬的还是提⾼模型参数，增加模型的拟合能⼒。

我们可以通俗的理解为: 我们前⾯加上参数的attention都是向量运算，⽽向量运算本质上是⼀
个向量空间向另⼀个向量空间的转化，所以这个操作本质上可以认为是将词向量从原始的语义
空间内拉扯到我们当前这句话的语义空间内，相当于让模型学了我们这⾥的⽅⾔。但学完了之
后模型还需要"思考"(或者"搜索")。因此在这⾥给模型更多的参数，让他充分的理解这块的⽅
⾔。

毕竟"学⽽不思则罔，思⽽不学则殆    "嘛，说明孔⼦在   2500年前已经领悟到 LLM的真谛。

以上为邪修猜想，当个乐⼦看。

3.6.2 Residual

我们训练的主要过程就是求梯度、求导，如果⽆脑叠层，很容易就给梯度整没了，所以这⾥给
原始的 input和我们计算过后的output连起来，保证梯度不消失，毕竟   "做模型嘛，不能忘本   "。






























在解决了这些问题之后，我们的模型就可以开始叠层了

## PDF物理页 17

3.7 LLM模型

⾄此，我们主要的模型结构就完成了，我们结合标注来再次复习⼀下                            :



































                                Q DogBaby模型结构




 import torch

 from torch import nn





 # ==========================================

 # 1. 配置清单 (相当于装修前的设计图纸)

## PDF物理页 18

# ==========================================

class QdogBabyLearnConfig():

    def __init__(self):

        self.model_name = "qdogbabylearn"

        self.version = "1.0.0"



        self.num_hidden_layers = 16# 盖多少层楼 (Transformer Block的数量)

        self.num_heads = 8           # 雇多少个专家同时看 (多头注意⼒的头数)

        self.emb_dim = 512           # 词向量的宽度 (每个词包含多少信息量)

        self.dropout = 0.0           # 随机扔掉多少神经元 (防⽌死记硬背)

        self.context_size = 512      # ⼀次能看多⻓的⽂章 (上下⽂窗⼝⼤⼩)

        self.vocab_size = 6400       # 字典⾥有多少个字 (词表⼤⼩)





# ==========================================

# 2. 模型主体 (QdogBabyLearn 机器⼈本体)

# ==========================================

class QdogBabyLearnLLM(nn.Module):

    def __init__(self, config: QdogBabyLearnConfig):

        super().__init__()

        self.config = config



        # ★ 查表升维：把离散的字变成向量

        self.tok_emb = nn.Embedding(config.vocab_size, config.emb_dim)

        # ★ 加⼊位置信息：让模型知道“我爱你”和“你爱我”顺序不同

        self.pos_emb = nn.Embedding(config.context_size, config.emb_dim)



        self.dropout = nn.Dropout(config.dropout)



        # ★ 叠罗汉：堆叠 16 层 Transformer Block

        self.transformer_blocks = nn.Sequential(

            *[TransformerBlock(config.emb_dim, config.num_heads, config.dropout, config.c

              for _ in range(config.num_hidden_layers)]

        )



        # 最后输出前的标准化

        self.norm = LayerNorm(config.emb_dim)

        # ★ 映射回字典：把向量变回预测下⼀个字的概率分数

        self.out = nn.Linear(config.emb_dim, config.vocab_size)



    def forward(self, x):

        # x 的形状: [batch_size, seq_len] (⽐如: [[1, 2, 3]])



        # 1. 查词表

        tok_embeds = self.tok_emb(x)

        # 2. 查位置表

        pos_embeds = self.pos_emb(torch.arange(x.shape[1], device=x.device))

## PDF物理页 19

        # 3. 信息融合 (词义 + 位置)

        x = tok_embeds + pos_embeds

        x = self.dropout(x)


        # 4. 经过 16 层“思考”

        x = self.transformer_blocks(x)



        # 5. 最终整理

        x = self.norm(x)

        x = self.out(x) # 输出形状: [batch_size, seq_len, vocab_size]

        return x





# ==========================================

# 3. Transformer Block (模型的⼤脑⽪层)

# ==========================================

class TransformerBlock(nn.Module):

    def __init__(self, emb_dim, num_heads, dropout, context_size):

        super().__init__()
        self.multi_head_attn = MultiHeadAttention(emb_dim, num_heads, dropout, context_si

        self.layer_norm1 = LayerNorm(emb_dim)

        self.feed_forward = FeedForward(emb_dim, dropout)

        self.layer_norm2 = LayerNorm(emb_dim)



    def forward(self, x):

        # --- 第⼀步：注意⼒机制 (词与词找关系) ---

        residual = x  # ★ 做模型不能忘本：先记住原始输⼊

        x = self.layer_norm1(x) # ★ 拉⻬起跑线

        x = residual + self.multi_head_attn(x) # 原始信息 + 新学到的关系



        # --- 第⼆步：前馈⽹络 (思考/记忆) ---

        residual = x  # ★ 再次记住当前状态

        x = self.layer_norm2(x) # ★ 拉⻬起跑线

        x = residual + self.feed_forward(x) # 原始信息 + 思考后的结果



        return x





# ==========================================

# 4. 多头注意⼒ (核⼼：我要啥、你有啥、我是啥)

# ==========================================

class MultiHeadAttention(nn.Module):

    def __init__(self, emb_dim, num_heads, dropout, context_size):

        super().__init__()

        self.emb_dim = emb_dim

        self.num_heads = num_heads

        self.head_dim = emb_dim // num_heads # 每个头负责的维度 (512/8 = 64)

## PDF物理页 20

        # 定义 Q, K, V 的映射层

        self.W_querys = nn.Linear(emb_dim, emb_dim) # 我要啥

        self.W_keys = nn.Linear(emb_dim, emb_dim)   # 你有啥

        self.W_values = nn.Linear(emb_dim, emb_dim) # 我是啥



        self.out = nn.Linear(emb_dim, emb_dim) # 信息汇总

        self.dropout = nn.Dropout(dropout)



        # ★ Mask (不让看答案)：创建⼀个下三⻆矩阵

        # 1 0 0

        # 1 1 0

        # 1 1 1

        self.register_buffer("mask", torch.tril(torch.ones(context_size, context_size)))



    def forward(self, x):

        batch_size, num_tokens, emb_dim = x.shape



        # 1. 线性变换⽣成 Q, K, V

        querys = self.W_querys(x)

        keys = self.W_keys(x)

        values = self.W_values(x)



        # 2. 切分成多头 (8个⼈分⼯合作)

        # 形状变换: [B, T, 512] -> [B, T, 8, 64]

        querys = querys.view(batch_size, num_tokens, self.num_heads, self.head_dim)

        keys = keys.view(batch_size, num_tokens, self.num_heads, self.head_dim)

        values = values.view(batch_size, num_tokens, self.num_heads, self.head_dim)



        # 3. 转置，把头(Head)放到前⾯，⽅便并⾏计算

        # 形状变换: [B, 8, T, 64]

        querys = querys.transpose(1, 2)

        keys = keys.transpose(1, 2)

        values = values.transpose(1, 2)



        # 4. 计算相似度 (我俩好不好)

        # Q @ K^T

        attn_score = querys @ keys.transpose(-1, -2)



        # 5. ★ Mask 操作 (不让偷看后⾯的词)

        # 把 mask 为 0 的位置填成负⽆穷⼤ (-inf)

        mask_bool = self.mask.bool()[:num_tokens, :num_tokens]

        attn_score = attn_score.masked_fill(mask_bool == 0, float('-inf'))



        # 6. 归⼀化 (概率化)

        # 除以根号dk是为了防⽌梯度消失

        attn_weight = torch.softmax(attn_score / (self.head_dim ** 0.5), dim=-1)

        attn_weight = self.dropout(attn_weight)

## PDF物理页 21

        # 7. 加权求和 (有你的我)

        # Weight @ V

        context_vec = attn_weight @ values



        # 8. 还原形状 (把8个头的结果拼回去)

        # [B, 8, T, 64] -> [B, T, 8, 64] -> [B, T, 512]

        context_vec = context_vec.transpose(1, 2).contiguous().view(batch_size, num_token



        # 9. 最终线性输出

        context_vec = self.out(context_vec)



        return context_vec





# ==========================================

# 5. 前馈⽹络 (发散思维 -> 收敛总结)

# ==========================================

class FeedForward(nn.Module):

    def __init__(self, emb_dim, dropout):

        super().__init__()

        # ★ 发散思维：维度放⼤ 4 倍 (512 -> 2048)

        self.linear1 = nn.Linear(emb_dim, emb_dim * 4)

        # ★ 收敛总结：维度变回原样 (2048 -> 512)

        self.linear2 = nn.Linear(emb_dim * 4, emb_dim)



    def forward(self, x):

        x = self.linear1(x)

        x = nn.GELU()(x) # ⾮线性激活 (增加脑回路的复杂度)

        x = self.linear2(x)

        return x





# ==========================================

# 6. 层归⼀化 (拉⻬起跑线)

# ==========================================

class LayerNorm(nn.Module):

    def __init__(self, emb_dim, eps=1e-5):

        super().__init__()

        self.eps = eps

        # 可学习的参数：缩放(scale) 和 平移(shift)

        self.scale = nn.Parameter(torch.ones(emb_dim))

        self.shift = nn.Parameter(torch.zeros(emb_dim))



    def forward(self, x):

        # 计算平均值

        mean = x.mean(dim=-1, keepdim=True)

        # 计算⽅差

        var = x.var(dim=-1, keepdim=True, unbiased=False)

## PDF物理页 22

         # 归⼀化公式：(x - 均值) / 根号(⽅差 + 极⼩值)

         norm = (x - mean) / torch.sqrt(var + self.eps)

         return norm * self.scale + self.shift




        腾讯技术⼯程
        腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
        689篇原创内容


 公众号

 4. 训练与⽣成

数据预处理和训练是⼀件⼗分庞⼤和耗时的⼯程，受限于篇幅，这⾥只对训练⽅式和推理做简
单介绍，不做展开。

4.1 模型的推理⽅式

在完成模型结构之后，我们先来尝试⼀下，看看模型到底会输出什么内容





 # ⾸先将输⼊⽂本进⾏编码

 # tokenizer.encode()⽅法将⽂本字符串转换为模型可理解的数字序列（token IDs）

 inputs = tokenizer.encode("QQ浏览器⼴告后台开发")

 print("编码后的token IDs:", inputs)



 # 将编码结果转换为PyTorch张量，并添加批次维度

 # torch.tensor([inputs])创建了⼀个形状为[1, sequence_length]的张量

 batch = torch.tensor([inputs])



 # 将批次数据输⼊模型进⾏推理

 # model(batch)返回模型的输出，通常是logits或概率分布

 output = model(batch)

 print("模型输出:", output)

 print("输出形状:", output.shape)



 # 使⽤argmax获取每个位置概率最⼤的token索引

 # dim=-1表示在最后⼀个维度（通常是词汇表维度）上取最⼤值

 predictions = torch.argmax(output, dim=-1)

 print("预测结果（token索引）:", predictions)



 # 将预测的token索引解码回⽂本

 # tokenizer.decode()将数字序列转换回可读的⽂本字符串

 print("解码后的⽂本:", tokenizer.decode(predictions[0]))

## PDF物理页 23

 编码后的token IDs: [51, 51, 586, 240, 6262, 1179, 5046, 799, 2507, 3158]

 模型输出: tensor([[[ 0.1939, -0.1545, -0.8574,  ...,  0.1755,  0.4264, -0.2223],

          [ 0.4136, -0.0892, -0.4605,  ...,  0.2929,  0.6576,  0.2146],

          [ 0.1227,  0.5149, -0.7861,  ..., -0.2095,  0.1483, -0.0575],

          ...,
          [-0.1255,  0.3100, -0.4338,  ..., -0.4569,  0.1680, -0.2783],

          [ 0.0123, -0.2317,  0.1034,  ..., -0.6657,  0.4466, -0.1969],

          [-0.0439, -0.2680, -0.8711,  ..., -0.8857,  0.7761,  0.2247]]],

        grad_fn=<ViewBackward0>)

 输出形状: torch.Size([1, 10, 6400])

 预测结果（token索引）: tensor([[1536, 1536,  738, 5155, 4507, 5155, 2857, 4672, 3506, 3283]]

 解码后的⽂本: 什什 R安排 similar安排软伴 diagnosonom




可以看到，输⼊        9 个 Token 后，模型对应输出了           9 个向量，每个向量的长度都等于词表⼤
⼩。这些数值可以理解为模型对词表中每个词的‘打分（’                       或者说概率，这⾥省略了            softmax处
理）。如果我们选取每个向量中数值最⼤的那个（即模型认为概率最⾼的词），并将其还原为⽂
字，就得到了模型最终的预测结果。

⽬前模型返回的数据还是毫⽆逻辑的token，因为我们还没进⾏训练，接下来我们就让他变聪
明些。

4.2 训练

4.2.1 数据构造

我们先要知道，我们期望模型返回的数据格式













对于输⼊的 "QQ浏览器⼴告后台开发", 我们期望模型整体前推⼀个字，即输出 "Q浏览器⼴告
后台开发组"，这⾥的"Q浏览器⼴告后台开发"，与我们的input相同，我们希望通过这种⽅式
让模型学习到语⾔模式，⽽第            n个字  "组"即是我们想要的字。





 # 原始语料数据 (假设这是分词后的 ID 序列)

 # 对应⽂本: Q   Q   浏   览   器   ⼴   告   后   台   开   发   组

 data = [51, 51, 586, 240, 6262, 1179, 5046, 799, 2507, 3158, 1335]

 data_tensor = torch.tensor(data)

 # 1. 构造输⼊ (Input): 取序列的前 N-1 个字

 # 也就是: "QQ浏览器⼴告后台开发"

 x = data_tensor[:-1]

## PDF物理页 24

 # x = [51, 51, 586, ..., 3158]

 # 2. 构造⽬标 (Target): 取序列的后 N-1 个字 (即每个位置对应的"下⼀个字")

 # 也就是: "Q浏览器⼴告后台开发组"

 y = data_tensor[1:]

 # y = [51, 586, 240, ..., 1335]

 print(f"输⼊⻓度: {len(x)}, ⽬标⻓度: {len(y)}")

 # 输⼊⻓度: 11, ⽬标⻓度: 11 (⼀⼀对应)

 # 3. 扔进模型计算

 logits = model(x.unsqueeze(0)) # 增加 batch 维度

 # 4. 计算 Loss (交叉熵损失)

 # 这⼀步是在问模型：

 # 当输⼊第1个'Q'时，你预测是第2个'Q'的概率⼤吗？

 # 当输⼊'浏'时，你预测是'览'的概率⼤吗？

 # ...

 # 当输⼊'发'时，你预测是'组'的概率⼤吗？

 loss = nn.cross_entropy(logits.view(-1, vocab_size), y.view(-1))

 loss.backward() # 反向传播，修正参数


这⾥有个反直觉的点：虽然我们在逻辑上是“预测下⼀个字”，但在训练时，模型是并⾏看到所
有输⼊的。它不需要等“浏”字⽣成了再算“览”字，⽽是⼀次性计算所有位置的预测误差(由于
3.4节 causal mask 的存在，模型不会发⽣      "看答案  "的情况  )。

通过这种⽅式，模型学会了：

  看到 "QQ浏览   "，⼤概率要接      "器"

  看到 "后台开    "，⼤概率要接     "发"

  看到 "开发   "，⼤概率要接     "组" (或者  "者"、"⼯程师  ")

这就是⼤模型    “学会说话   ”的根本原因。

4.2.2 预训练 与 SFT

## PDF物理页 25

这⾥补充说明⼀下       SFT 时的数据构造情况，我们通常会定义⼀些特殊的  Token                  （如
<|im_start|>）来告诉模型哪⾥是⼈说的，哪⾥是它该说的，因此我们构造的对话数据⼀般为
这种格式  :





 # SFT 数据构造示例

 sft_template = """

 <|im_start|>user

 请介绍⼀下QQ浏览器。<|im_end|>

 <|im_start|>assistant

 QQ浏览器是腾讯开发的⼀款...<|im_end|>

 """


在 SFT 阶段，我们只计算 assistant 回答部分的 Loss。这就好⽐考试评分：⽼师只给你的“答
案”打分，⽽不会因为你把“题⽬”抄写得好不好⽽扣分。 这样做的⽬的是让模型专注于学习“如
何根据问题给出正确回答       ”，⽽不是去                     死记硬背问题本⾝。

4.3 采样策略

在模型⽣成⽂本时，我们通常不希望每次都选择概率最⾼的词，这样会让输出变得过于确定和
单调。温度和    topk就是⽤来控制⽣成多样性的两个重要参数。

温度（  Temperature） 就像是给模型的    "创造⼒  "调个温：

  低温（如   0.1）：模型更保守，总是选择最可能的词，输出稳定但可能单调

  ⾼温（如   0.5-1.0）：模型更 "放飞⾃我  "，会尝试更多可能性，输出更有创意但可能不够准
  确

Top-k采样 则是另⼀种控制⽅式：

  只从概率最⾼的     k个候选词中选择，避免选择那些概率极低的词

  ⽐如  k=4，就只从前   4个最可能的词中                                随机选择

这两种⽅法可以单独使⽤，也可以结合使⽤，让模型在                "靠谱 "和"有趣  "之间找到平衡。





 # QQ浏览器⼴告后台开发 + ？？？

 # vocab: [霉, 苦, 组, 者, 钱]

 probas = torch.tensor([0.1145, 0.1245, 0.5130, 0.1887, 0.0694])

 print(torch.softmax(probas, dim=-1))

 temperature = 0.5

 print(torch.softmax(probas/temperature, dim=-1))

 temperature = 0.1

 print(torch.softmax(probas/temperature, dim=-1))

 print(torch.topk(probas, k=4, dim=-1))

## PDF物理页 26

tensor([0.1807, 0.1826, 0.2692, 0.1947, 0.1728])
tensor([0.1584, 0.1616, 0.3515, 0.1837, 0.1447])
tensor([0.0171, 0.0189, 0.9174, 0.0358, 0.0109])
torch.return_types.topk(
values=tensor([0.5130, 0.1887, 0.1245, 0.1145]),
indices=tensor([2, 3, 1, 0]))






















通过上⾯的例⼦我们发现       Temperature 系数实际上是在调整   Softmax 之前的 Logits 数值分
布。 T 减⼩ (冷却)：拉⼤ Logits 之间的差距，⾼的更⾼，矮的更矮。概率分布变得“尖锐”，
模型只敢选最有把握的词。 T 增⼤ (加热)：缩⼩ Logits 之间的差距，众⽣平等。概率分布变
得“平坦 ”，原本概率低的词也有机会被选中，模型开始          “胡⾔乱语  ”或“创意迸发  ”。



 5. 演⽰

预训练后的模型   :

























这是因为预训练模型本质上是⼀个⽂本续写机。它在海量⽂档中学习的是“下⼀个字是什么”的
概率分布。在它眼⾥，你输⼊的问题可能只是某本⼩说或新闻的开头，它并不知道这代表⼀次

## PDF物理页 27

“对话”的开始。它只是在尽职尽责地根据概率，顺着你的话继续往下编故事，⽽不是在回答你
的问题。

SFT后的模型     :

























通过  SFT，我们让模型学会了对话的模                                                                式，模型真正的完整回答问题。

TIPS: 由于⽹络环境         /资源等原因，演⽰模型没有对外部署，感兴趣的同学可以使
⽤  minimind 提供的数据集，配合             codebuddy  快速⽣成训练逻辑，训练出⼀个属于⾃⼰的
LLM。



  6. 参考资料

1. 《Build a Large Language Model (From Scratch)》


2. CS336: Language Modeling from Scratch


3. The Illustrated Transformer


4. The Illustrated GPT-2 (Visualizing Transformer Language Models)


5. The Big LLM Architecture Comparison


6. minimind


7. Visualizing A Neural Machine Translation Model (Mechanics of Seq2seq Models With Attention)


8. 《Hands-On Large Language Models》


9. Happy-LLM


中⽂数据集：

## PDF物理页 28

 1. MiniMind训练数据集


 2. 出门问问序列猴⼦开源数据集


 3. opencsg/chinese-ﬁneweb-edu-v2


 4. 匠数科技⼤模型    sft数据集



























         腾讯技术⼯程
         腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
         689篇原创内容


  公众号




















阅读 5.6万





留⾔  3  1


写留⾔

## PDF物理页 29

🥕   🐰浙江2025年12⽉24⽇                                        110
“看到这⾥的你已经成功⼿搓第⼀个模型了，下⼀个任务：⼲掉Gemini3pro🤓   👆🏻”


毅璐向前 ⼭东  2025年12⽉24⽇                                      33
进⼊我的收藏吃灰吧


明安 ⼴东 2025年12⽉24⽇                                         17
⼈家的 LLM是Large Language Modle，接下来我们⼿搓⼀个Little Language Modle吧


花开富贵 湖北  2025年12⽉24⽇                                      16
竟然试图教会我⼤模型


安曲 新疆 2025年12⽉24⽇                                          11
我现在备注⼤模型算法岗就在⾃⼰⼿搓⼤模型，技术路线居然和这篇⽂章不谋⽽合。昨天已经
⼿搓单头注意⼒机制了，明天⼿搓多头注意⼒机制。


北⽃之下 浙江  2025年12⽉24⽇                                       11
宝藏资料！引⽤的都是最近在看的！再推荐⼀个就是          karpethy github项⽬的nanoGPT


@⼩·边·边 内蒙古 2025年12⽉26⽇                                     9
《如何0基础⼿搓原⼦弹》


Xinn北京2025年12⽉24⽇                                          6
看完了，没学费，能不能来⼀个⼿把⼿教学


格⼼ 浙江 2025年12⽉24⽇                                          4
这使⽤了多少显存？硬件要求是怎么样的


爱做梦的 ⼤…  湖南  2025年12⽉24⽇                                   3
多写，爱看


李鸿儒 天津 2025年12⽉24⽇                                         2
你已经会本地训练⼩模型了，现在去训练⼀个        340B的⼤模型吧


⽥⽲⼦ 上海 2025年12⽉24⽇                                         2
写的很棒呀！逻辑清晰步骤明确 www，这段时间看的讲的最清楚的⼀篇⼿搓 llm 了


StackRising湖南2025年12⽉24⽇                                   1
这本书确实值得⼀读，写的很详细


CIA·兵⼴东 2025年12⽉24⽇                                        1
好棒啊


千的乐 海南 2025年12⽉24⽇                                         1




Reprise浙江2025年12⽉24⽇                                       1

## PDF物理页 30

可以，


星河 北京 2025年12⽉24⽇                                          1
感动了，真的太感动了，写得特别好


。 湖北 2025年12⽉24⽇                                           1
写的真好，可惜我看不懂


Kerwin的地盘 天津 2025年12⽉24⽇                                   1
⾥边的图⽤什么画的


ɢᴏʀɪᴛ湖北2025年12⽉24⽇                                         1
@元宝 总结⼀下


xz江苏 2025年12⽉24⽇                                           1
这个好啊！还有后续的教程吗


cutemurphy浙江2025年12⽉24⽇                                    1
AI会帮我写


bear四川2025年12⽉26⽇
从第⼆节开始就略过了


刘荣 ⼭东 2025年12⽉26⽇
头⼤，有点难


8 ⽉失败的  … 我⼴东  2025年12⽉24⽇
@元宝 总结⽂章，怎么做⼀个元宝出来


DK坚果壳 北京 2025年12⽉24⽇
喜欢这种，有时间⾃⼰写写试试


Good.⼴东2025年12⽉24⽇
点赞在看=学会了


yo.⼴东2025年12⽉24⽇
⻢上动⼿！


FireFliesʚ🐷ɞ上海2025年12⽉24⽇
收藏，晚点再看


Jenson北京2025年12⽉24⽇
今天就先看到1.4节，累了


付@软件开发  四川 2025年12⽉24⽇
⼿搓⼀个操作系统，⼀个编辑器，⼀个⼤模型。。

## PDF物理页 31


