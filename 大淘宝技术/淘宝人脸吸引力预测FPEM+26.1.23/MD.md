# ICCV25 | 淘宝人脸吸引力预测算法FPEM：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_淘宝人脸吸引力预测FPEM.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
ICCV25 | 淘宝人脸吸引力预测算法FPEM
原创
音视频技术团队 2026年1月23日 00:31 浙江
大淘宝技术 3人
淘 天音视 频技术 团 队 与上 海 交
大合 作 论文 《 FPEM: Face Pri
or Enhanced Facial
Attractiveness Predicti
on for Live Videos with Face Retouching 》，被计算机视觉领域顶
级会议ICCV 2025（CCF A类顶会，录用率24.2%）成功收录。
论文含金量背景介绍
ICCV是由IEEE/CVF主办的计算机视觉领域的顶级
学术会议，也是中国计算机协会CCF推荐的
A类学术会议。该会议在世界范围每两年举办一次，其收录的论文涵盖了图像和视频领域的创
新技术和重大成果，是相关领域学术研究与
行
业发
展的风向标。ICCV 2025共收到创
纪录的
11,152篇有
效投稿，经过严格的同
行
评审，最终录用了2,702篇，整体录用率约24.2%。此篇
被收录论文属于人脸吸引力预测领域，由淘天音视频技术团队和上海交通大
学合作完成。
在淘宝，每天有数十万的直播间存在美颜需求，人脸的吸引力已成为影响直播用户整体视觉体
验的核心变量，通过实时监测确保美颜效果的稳定性，对保障主播和用户的双端体验至
关
重
要。对于电商平台而言，这一点尤为重要，因为它能显著影响人均观
看时长，甚
至直接
合图像和文
关系到
商品交易总额（GMV）。因此，淘天音视频技术团队自研了一种针对直播美颜场景下的人脸吸
引力预测模型——FPEM（Face Prior Enhanced Multi-modal Model），通过融
两
本
种模态，对人脸面部吸引力做量化预测。
论文下载链接：
https://openaccess.thecvf.com/content/ICCV2025/papers/Li_FPEM_Face_Prior_Enhanced
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
_Facial_Attractiveness_Prediction_for_Live_Videos_ICCV_2025_paper.pdf
论文背景
▐ 定义AI审美新标杆！淘宝直播自研FPEM模型，开启直播美颜“量化时代”
随着直播与短视频
行
业的蓬勃发
展，美颜技术已成为内容生态的底层标配。在追求极致视觉体
验的今天，如何客观量化人脸的感知质量，已成为驱动美颜技术进化与体验升级
的关键突破
口。在这一背景下，构建一套兼顾“清晰度”与“美学感受”的量化评价体系，不仅能助力平台实
时监控服务质量，更能精准追踪直播间的内容吸引力，从而实现体验的跨越式提升。
▐ 从“感知”到“量化”：LiveBeauty数据集重磅发布
美，能否被计算？淘天音视频技术团队给出了肯定答案。依托淘宝直播海量的真实应用场景，
团队重磅发布了业界领先的大规模直播人脸吸引力数据集——LiveBeauty。该数据集涵盖了
10,000张精选图像，不仅广泛覆盖了
不同的美颜算法参数、
光照条件与面部表情，更通过专业
的主观标注，获取了高达20万个主观分数标签，构建起目前业界最具代表性、标注最精细的
“直播审美坐标系
”。
▐ 技术突破：业界首个多模态人脸吸引力预测模型FPEM
在此 基 础 上 ， 团 队 推 出 了 业 界首 个针 对直 播场 景的人脸 吸 引力预 测 模 型 ——FPEM（ Face
Prior Enhanced Multi-modal Model）。通过将视觉图像与文本语义
深度融
合，FPEM模型
仿 佛 拥有了 “人类 审 美 直 觉 ”， 能 够 精 准
洞 察 复杂环 境 下 的面 部 魅力值 。在SCUT-
FBP5500[1]、
MEBeauty[2]等学术权威数据集上，FPEM凭借优秀
的性能表现全面霸榜，各项
指标（SR
OCC、PLCC、
KR
OCC）均超越现有SOTA方
案，标志着其在人脸美学吸引力评价领
域已
实现全
方位领跑。
▐ 业务赋能：科技驱动视觉交互体验升级
目前，FPEM模型已正式应用于淘宝直播业务。通过联动视频质量评价模型（MD-VQA[3]），
FPEM
实现了对
别优质内容，并有
大盘视觉体验的全天候监控。这种精准的“水位分层”能力，让平台能够快速识
效驱动美颜算法的迭代优化，为主播与用户提供更加自然、
高品质的交互体
验。
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
具体方法
为更好地适配淘宝直播平台的数据场景，我们基于淘宝直播平台的视频，构建了
大规模直播场
景下的人脸吸引力预测数据集LiveBeauty，包含10,000张图像，涵盖不同美颜算法参数、
光
照条件
、面部表情，并通过专业的主观标注，获取200,000个对应的主观分数的标注数据。与
此同时，我们自研了一种针对直播美颜场景下的人脸吸引力预测模型——FPEM（Face Prior
Enhanced Multi-modal Model），通过融
合图像和文本
两
种模态，来预测人脸面部吸引力的
高低。
▐ LiveBeauty 数据集
为了准确刻画直播视频中人脸吸引力的分布规律，我们从淘宝直播平台选取了较高页面浏览量
（Page View）的直播间回放，对每个直播间采样三次，随后利用SOTA的人脸检测模型 [4]
提取人脸区域的边界框。数据清洗时，剔除了包含动漫角色、虚拟头
像以及同一人物的重复样
本，以确保数据集的质量与多样性。最终，我们从 9,500 多个直播间中采集了 10,000 张图
像，确保涵盖 10,000 张互不相同的人脸。图 1 展示了
LiveBeauty 数据集中部分人脸图像的
示例。
图1. LiveBeauty数据集示例
在此基础上，我们组织了20名专家组成的主观测评团队，对上述10,000张人脸图像进
行
主观打
分，共生成200,000条主观分数的标注数据。然后，我们根据ITU-RBT.500-13[5]标准，将
标 注 数据 转 换为Mean Opinion Score （M
OS ） 分 数， 作 为人脸 吸 引力的ground-truth
（GT）数据。
我们也和学术界主流的人脸吸引力预测数据集进
了比
较，如表1所示。从表中可以看出，先前
行
的数据集闭源的较多，开源的数据集则规模偏小。我们构建的数据在数据规模上具有一定竞争
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
力，且考虑了直播中美颜算法的影响，同时更适合于电商直播场景。
表1. 主流人脸吸引力预测数据集比
较
▐ 模型设计
图2展示了所提出的FPEM模型的框架，该模型使用了两阶段训练策略，包含了3个核心模块：
PAPM模块、
MAEM模块和SFM模块。具体地，FPEM使用了图像和文本
两
种模态，有选
地融
择
合了人脸先验和美学语义信息来预测人脸面部吸引力的高低。在训练的第一阶段，PAPM模块
和MAEM模块独立训练；训练的第二阶段，冻结二者参数，利用SFM模块动态地整合二者提取
的人脸先验知
识和多模态美学语义信息。
图2. FPEM模型框架
PAPM 模块
Personalized Attractiveness Prior Module（PAPM）模块包含两个视觉特征提取模块
和 （FaceNet[6]）,分别提取多尺度的视觉特征和全局的人脸先验特征，随后通过一个交
叉注意力模块融
合后回归出一个预测分数 。这个过程的主要目的是整合low-level的视觉语
义信息和在百万级人脸图像上训练过的模型获取的人脸先验信息。
MAEM 模块
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Multi-modal Attractiveness Encoder Module (MAEM) 模块包含文本编码器 ，基于CLIP模型架构提取多模态的美学语义信息。在文本模态上，我们使用了5级
和图像编码器
的吸引力
标签 :
随后使用文本template：“a photo of a person with {a} attractiveness ” 可以构造5个候选的
文本描述。在回归时我们使用Similarity Regression（SR）模块进
行
相似度回归，得到一个预测
分数 。
SFM 模块
Selective Fusion Model (SFM) 模块通过一层Sq
ueeze Layer压缩PAPM和MAEM提取的特征，
并通过全连接层映射得到加权参数，在训练的第二阶段自适应地融
合二者表征的人脸先验知
识
和多 模 态 美学语 义 信 息 。在回 归时同 样使用 Similarity Regression（SR）模 块 进
相似 度 回
行
归，得到最终的预测分数 。
▐ 损失函数
在MAEM的训 练中， 我 们 引入了 2种 损 失 函 数：L1损 失 函 数 和Rank Loss Loss又分为两个部分Fidelity Loss 和 Two-direction Ranking Loss 。
对于保真度损失 ，给定一组图像对 ，根据其吸引力M
签（Binary Label）如下所示：
OS分真值 定义
。Rank
的二元标
根据瑟斯顿模型（Thurstone’s model），图像 被感知为比 更具吸引力的概率估计如下
所示，其中Ψ(⋅) 表示标准正态分布的累积分布函数（CDF），且其方差设定为 1。
随后，保真度损失可由如下公式计算得出：
对于Two-direction Ranking Loss ，给定图像 ，用表示其与第 j 个吸引力等级
之间的余弦相似度分数，并用 o 表示概率最高的吸引力等级
。由于人类对面部吸引力的感知
是
循序渐进的，且极少出现多个峰值（即多峰分布），我们通过确保吸引力等级
的概率分布仅呈
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
现单峰、并向左右两个方向递减，从而进一步获取
排序信息。据此，Two-direction Ranking
Loss 可由如下公式定义
。
实验论证与结果
我 们 在两 个公 开 的人脸 吸 引力预 测 数据 集 SCUT-FBP5500、
MEBeauty， 以 及 我 们自 建 的
LiveBeauty数据 集 上 ， 与现有SOTA方 法 进
了 对比
行
。我 们 使用 Spearman Rank Correlation
Coefficient（SR
OCC）Pearson Linear Correlation Coefficient（PLCC ）和 Kendall Rank Order
Correlation Coefficient（KR
OCC）作为指标进
对比
行
。更高的SR
OCC和KR
OCC表示样本间更
好的保序性，更高的PLCC表示与标注分数更好的拟合程度。结果如表2所示。
表2. FPEM与其它人脸吸引力预测SOTA模型在SCUT-FBP5500、
数据集上的性能比
较
MEBeauty和LiveBeauty
从表中可以看出，我们在3个数据集上的SR
OCC、PLCC和KR
OCC均超过了现有SOTA方法，
达到了先进性能。
此外，为了探索不同模块对模型性能的贡献，我们还进
行
了消融试验，如表3和表4所示。
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
表3. LiveBeauty 测试集上各个模块和损失函数对于模型性能的贡献比
似度回归策略； 代表
L1 Loss；
较。其中MS 指多尺度融
表示 Rank Loss。
合操作；SR 代表相
从表3可以看出，在PAPM中引入人脸先验和多尺度特征
均能有
效提升模型性能；在MAEM中，
零样本（zero-shot）CLIP 在人脸吸引力预测（FAP）任务中的泛化能力有限，且移除 SR
策
略后性能出现显著下降，这表明专门设计的回归策略对于 CLIP 适配回归任务至
关
重要。同
时，排序损失与回归损失的联合优化也进一步提升了 SR
OCC 指标；在所有模块的消融上，使
用两阶段训练和SFM
取得了最佳性能，证明了 SFM的
有
效性，即它能够自适应地将多模态美学
特征与全局人脸先验知
识进
行深度融
合。
表4. PAPM
、
MAEM和SFM模块在模型泛化性上的贡献。所有
实验均在LiveBeauty上训练，MEBeauty上测试
从表4可以看出，各个模块在模型泛化性上均
布和面部吸引力评分标准定义
有贡献。此外，指标整体偏低，这是由于数据分
的不同，影响了模型在不同数据集间的迁移能力。
总结与展望
为了弥补领域内现有数据集的空白，我们构建了
大规模人脸吸引力预测数据集LiveBeauty，这是
首个包含直播场景美颜效果的人脸数据集。该数据集采集自真实场景，兼具高质量与真实性，是
目前公开可用的规模最大的人脸吸引力预测数据集。此外，我们提出了一个多模态框架FPEM，能
够自适应地融
合
全局人脸先验与美学语义特征以量化人脸吸引力。大量实验表明，FPEM 的表现
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
优于目前最先进（SOTA）的方法。同时，LiveBeauty 数据集与 FPEM 框架亦可有
视频应用场景中的人脸美感预测
任务。
效推广至其他
在直播生态中，美颜并非简单
的“磨皮”，而是包含脸型、五官比例微调等复杂变换，这种“算法处
理后的美”已成为互联网上一种新的视觉常态。LiveBeauty数据集和FPEM模型的提出为这一审美
现象提供了新的研究视角和应用思路。然而，美感预测本质上具有高度的主观性。虽然模型在主
观
平
挑战。
均分预测上表现优异，但在不同文化背景、性别或族裔下的审美差异仍是该领域面临
的
深层
参考文献
1. Lingyu
Liang, L
uojun Lin, Lianwen Jin, Duorui Xie, and Mengru
Li. Scut-fb
p5500: A diverse
benchmark dataset for m
ulti-paradigm facial beauty prediction. In Proceedings of the IEEE
International Conference on Pattern Recognition, pages 1598–1603, 2018.
2. Irina Lebedeva, Yi Guo, and Fangli Ying. Mebeauty: a m
the-wild. Neural Comp
uting and Applications, pages 1–15, 2022.
ultiethnic facial beauty dataset in-
3. Zhang Z, Wu W, Sun W, et al. MD-VQA: Multi-dimensional q
uality assessment for UGC live
videos[C]In Proceedings of the IEEE International Conference on Pattern Recognition, pages
1746-1755, 2023.
4. Shifeng Zhang, Xiangyu Zhu, Zhen Lei, Hailin Shi, Xiaobo Wang, and Stan Z Li. Faceboxes: A
cp
u real-time face detector with high accuracy. In Proceedings of the IEEE International
Joint Conference on Biometrics, pages 1–9, 2017.
5. RECO
MMENDATION ITU-R BT. Methodology for the subjective assessment of the q
uality of
television pictures. International Telecomm
unication Union, 2002.
6. Florian Schroff, Dmitry Kalenichenko, and James Philbin. Facenet: A unified embedding for
face recognition and clustering. In Proceedings of the IEEE/CVF Conference on Comp
uter
Vision and Pattern Recognition, pages 815–823, 2015.
团队介绍
该工作主要由淘天音视频技术团队完成，该团队依托淘宝直播、逛逛、手淘首页信息流等内容业
务，致力于打造行业领先的音视频技术。团队成员来自海内外知名高校，先后在在MSU 世界编
码器大赛，NTIRE视频增强超分竞赛这样的领域强相关权威赛事上夺魁，并重视与学界的合作与
交流。
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
这项工作的合作方为上海交通大学翟广涛教授创办的多媒体实验室，隶属于上海交通大学电子信
息与电气工程学院电子系图像通信与网络工程研究所，是多媒体处理与传输及多媒体感知计算的
主要研究力量之一
。面向国家推动人工智能发展的战略，顺应内容生成智能化的发展趋势，近年
来开展的重点研究领域包括AIGC内容质量评价、三维数字人生成和驱动等。
¤
拓展阅读 ¤
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
大淘宝技术
大淘宝技术官方账号
967篇原创内容
公众号
阅读 3230
留言
写留言
还没有
留言，来写首评
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text

```
