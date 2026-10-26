# MNN-Sana-Edit-V2：端侧运行的图像漫画风编辑大模型：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_MNN-Sana-Edit-V2端侧图像编辑.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
MNN-Sana-Edit-V2：端侧运
行
的图像漫画风编辑大模型
原创
Meta技术团队 2026年4月22日 02:02 浙江
大淘宝技术 1人
MNN-Sana-Edit-V2 是由淘宝 Meta 团队联合杭州电子科技大
学研发
的端侧图像漫画风编
辑大模型，基于 Sana 和 MetaQuery 学术成果创
新构建，采用 Qwen3-0.6B 作为冻结的
预训练 LLM，通过 Learnable
Query 和 Connector 模块桥接文本理解与图像生成，结合
Linear D
iT、
Deep Compressi
on Autoencoder 等高效架构设计，并依托 MNN 框架实现
4/8bit 量化部署，使全
部模型可在手机端本地运
行
；该模型在 iPhone 17 Pro 上仅需约 15
秒即可完成 512×512 图像的漫画风格转换，较云端方
案提速 2.5 倍，同时保障用户隐私与
推理效率，目前已集成至 MNN Chat 应用（支持 iOS/Andro
id），相关代码与模型权重已
在 GitHub、HuggingFace 及 ModelScope 全面开源。
前言
随着生成式人工智能技术的持续演进，端侧部署能力逐渐成为模型落地的重要考量。在图像编
辑领域，兼顾隐私安全与推理效率，一直是技术探索的重点方向。
MNN-Sana-Edit-V2 是淘宝业务技术 Meta 团队联合杭州电子科技大
学研发
的端侧图像编辑大
模型，该模型在参考 Sana 和 Metaquery 等学术界论文的基础上，基于文生图框架，创
新性地
增加了图像编辑功能，基于淘宝 MNN LLM 和 MNN D
iffusi
on 的端侧量化部署能力，做到了所
有模型本地运
行
，既能保护隐私，避免用户信息泄漏，又能做到快速运
行
，减少等待时间。通过
测试，在 iPhone 17 Pro 上，MNN-Sana-Edit-V2 模型能够在 15 秒内完成任
意图像的漫画风
格转换，相比 OpenAI 的图像编辑能力，提速 2.5 倍。目前该功能已经在 MNN Chat 应用中正
式上线，支持 Andro
id 平台和 iOS 平台，同时所有模型和推理代码已经在 MNN 仓库进
开
行
源，欢迎大家尝鲜使用。
MNN-Sana-Edit-V2 漫画风编辑效果
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
MNN Chat App下载地址：
iOS: https://apps.apple.com/us/app/mnn-chat/id6748348797
Andro
id (Google Play) :
https://play.google.com/store/apps/details?
id=com.alibaba.mnnllm.andro
id.release
MNN Chat Andro
id 和 iOS App 使用 MNN-Sana-Edit-V2 效果截图：
下面我们将从网络框架设计，核心技术详解，训练策略，MNN 端侧部署优化几个方面对这个工作
进
行介绍。
网络框架设计
▐ 系
统架构设计
MNN-Sana-Edit-V2 整体采用 Sana 图像生成模型的网络架构，同时为了更好地利用预训练
LLM 对 Prompt 的理解能力，我们结合 MetaQuery 论文中提出的 Learnable
Query 思想，利
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
用可学习的一组网络参数来桥接预训练 LLM 与图像生成与编辑过程。
具体来说，MNN-Sana-Edit-V2网络包括下面组
件：
1. 预 训 练 LLM 采用 Qwen3-0.6B， 使用 保 持 freeze 状 态 ， 参 数不 变 ，用 于更 好 地 理 解
Prompt
2. Learnable
Query: 256 维的可学习参数，用于桥接文本理解和图像生成
3. Connector 模块：负责将 LLM 的语义
表示对齐到 D
iT 的
入空间
4. Reference Image: 输
5. No
ise: 输
入的高斯噪声
入参考图像
6. D
iT 模块：将输
入的高斯噪声与参考图进
联合去噪声，得到编辑后的图像
输
行
核心技术详解
▐ Learnable Query: 连接理解与生成的桥梁
Learnable
Query是可学习的"问题"向冻结的 LLM "提问"，提取适合图像生成的条件。
具体实现上，Learnable
时，Learnable
Query 作为一组可学习参数，采用正态分布进
行
初始化。在提取条件
Query与 Text Embedding 一起输
入到 LLM 模型中。模型输出的最后 N 个
Hidden States 参数即为生成条件。
实际使用时我们选
择
N = 256 个 Learnable
Query 参数。
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ Connector 模块: 跨模态对齐
Connector 负责将 LLM 的语义
表示对齐到 D
iT 的
入空间，为图像生成过程中提供了强大的文
本理解能力。
网络设计上，Connector 模块包含 Connector 网络和 Projector 网络。Connector 网络采用
Transformer 结 构，用 来高 效 提取 信 息 ；Projector 网 络 采用 线 性层 作 为实 现 ，用 来将
Connector 网络输出的特征对齐到 D
iT 的维度。
输
Deep Compressi
on Autoencoder
传 统 的 AE 压 缩 倍 数大
F32C32），相比
的开销，适合端侧场景使用。
多 为 8 倍 ，而 Sana 网 络中采用 了 32 倍 的压 缩 设 计 （D
C-AE-
别的8x的AEs, latent token的数量大大减小，既加速了训练，又减少了推理时
Linear D
iT
线性注意力机制
是 Sana 论文中的关键创
文中将 D
iT 中的 Attenti
on 层都
新。传统注意力的计算复杂度为 O(N²)，而 Sana 论
修改为了 Linear Attenti
on， 计算复杂度为 O(N)，减少计
算量，加速推理，且通过实验验证，生图无质量损失。
Mix-FFN 模块在传统 FFN 的基础上，增加了 Depthwise 卷积，用于更好地捕捉局部信息。
具体来说，Mix-FFN 包含三个组
件：倒残差块、3×3 深度卷积、Gated Linear Unit。采用
Mix-FFN 的目的是去 掉 Positi
on Encoding，达 到 NoPE 的效 果 。NoPe 即 No
Positi
onal Encoding，也即移除位置编码。
▐ 文本编码器: Qwen3-0.6B
Sana 论文中采用选
择
Gemma-2 作为文本编码器具，我们的方
案
中，采用 Qwen3-0.6B 作
为预训练 LLM。
Qwen3-0.6B 相比 Gemma-2 的 2.6B，参数量更小，且文本理解能力更
强，尤其是在中文 Prompt 场景。
另外，训练稳定性也至
关
重要。Sana 发现，直接使用 Decoder-only LLM 的文本嵌
致 训 练不
稳 定 ， 原因 在于传 统 的生 图 算 法 采用 T5 等 模 型 ， Embedding Decoder-only LLM Embedding 层 权 重 较大， 直 接 沿用 之 前 的训 练方
入会导
层 数值 较小 ，而
案 ， 会导 致 数值 爆
炸。
为了 解决这个问题， 我 们 也 采用 Sana 中的方
案 ， 增 加 RMSNorm Embedding，同时引入小的可学习缩放因子，进一步稳定训练。
层 ， 归一化文 本
▐ Reference Latent
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
图像编辑需要原始图像作为输
入，在我们的方
案
中，我们通过 VAE Encoder 获取源图像的
Latent, 作为参考输
入 D
iT 生图网络，引导编辑过程，保持图像结构一致性，实现更精确的图
像编辑。
训练策略
三阶段训练
为了达到最佳的编辑效果，训练过程中我们分三个 Stage 来训练网络。
Stage 1 是预训练阶段，针对文本到图像
任务，目标是对齐预训练 LL
M 和图像生成任务。具
体 来说 ， 该阶 段 只 训 练Learnable Query 和 Connector 部 分 的权 重 ， 别的模 块 保 持 权 重 固
定。这个阶段，我们采用 2 M 的文本-图像对数据训练约 100K Step。
Stage 2 是图像生成微调
阶段，训练 Learnable Query，Connector以及图像生成 DiT 模块
的权重。基于内部收集的 60K 文本-图像对数据训练约 10K Step。
Stage3 是图像编辑微调
阶段，在 Stage2 的基础上，增加参考图像作为额外输
数同 Stage2。基于内部收集的 10K 图像编辑数据对训练约 100K Step。
入，可训练参
MNN 端侧部署优化
模型转换
在 Pytorch 中训 练 好 权 重 后 ， 我 们 先 将 Pytorch 模 型 转 换 为 ONNX 格式， 然 后 再 转 换 为
MNN 格式。由于 MNN 在长
期的迭代中已经支持了绝大部分的 ONNX 算子，因此模型转换部
分的流程比
较顺畅。更多转换细节请参考MNN文档。
量化技术
MNN-Sana-Edit-V2 推 理 流 程涉 及 多 个模 型 ， 包 括 预 训 练 的 LL
M ， VAE 的 Encoder 和
Decoder，以及去噪模型 DiT 等。通过合理的量化设置，能够显著减少模型内存占用，提高推
理速度，且不
对最终效果造成明显损失。
具体来说，对预训练的 LL
M 模型权重，我们采用了 4Bit 非对称量化，别的模型均采用 8Bit
非对称量化。这个配置能最好地平衡推理性能和生图效果。
真机速度测试
我们在真机上，测试了 512x512 配置下的图像编辑速度：
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
操作系
统 机器型号 芯片版本生成图片整体耗时(s)
iOS iOS iPhone 17 Pro （2025 年 9 月
发布）
iPhone 16 Pro （ 2024 年 10
月发布）
A19 Pro 14.7
A18 Pro 18
iOS iPhone 15 Pro （2023 年 9 月
A17 Pro 20
发布）
Android一加13 (2024 年 10 月发布) Snapdragon 8 Elite 45
Android Xiaomi 12 Pro （2021 年 12 月
发布）
Snapdragon 8 Gen 1 62
经测试，OpenAI 的吉卜力风格图像生成耗时 38s-45s，我们在 iPhone 17 Pro 上，以端侧
模型比云端模型的配置，做到了 2.5 倍的提速。
运
行要求
内存占用：5.5G
系
统要求：iOS A16 及以上版本，Android 骁龙 8
及以上版本
最优超参说明
入图像 尺寸 ： 建 议 使用 是以 正方 形 图片 作 为输
入，非 正方 形 图片生 成 效 果 可 能 会有下
降。
入图像 内容 ： 建 议输
入
张 正脸人像 ， 效 果 最 佳 ， 多人或者
非人场 景 效 果 可 能 会有下
降。
输出分辨率：目前模型输出分辨率固定为 512x512。
图像编辑提示词：本模型流程中已固定提示词，无需额外设置，修改提示词可能汇降
低效
果。
图像生成 step：建议使用 10 步，步数过低会有
增加运
耗时。
效果损失，步数增加效果无明显提升，且
行
输
输
单
源码和模型下载
源码：https://github.com/alibaba/MNN
文档：
https://github.com/alibaba/MNN/blob/master/apps/sana/README.md
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
模型权重：
huggingface: https://huggingface.co/taobao-mnn/MNN-Sana-Edit-V2
modelscope: https://modelscope.cn/models/MNN/MNN-Sana-Edit-V2
参考论文
SANA: Efficient High-Resolution Image Synthesis with Linear Diffusion Transformers
Transfer between Modalities with MetaQueries
团队介绍
本文作者蔚山，来自淘天集团-Meta技术团队。本团队目前负责面向消费场景的3D/XR基础技
术建设和创
新应用探索，创造以手机及XR 新设备为载体的消费购物新体验。团队在端智能、
端云协同、商品三维重建、真人三维重建、3D引擎、XR引擎等方面有着深厚的技术积累，先
后
发布深度学习引擎MNN、商品三维重建工具Object Drawer、3D真人数字人TaoAvatar、
端云协同系
统Walle等。团队在OSDI、MLSys、CVPR
、ICCV、NeurIPS、TPAMI等顶级
学
术会议和期
刊上发
表多篇论文。欢迎视觉算法、3D/XR引擎、深度学习引擎研发、终端研发等
领域的优秀人才加入，共同走进3D数字新时代。
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
大淘宝技术
大淘宝技术官方账号
967篇原创内容
公众号
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
阅读 2154
留言
写留言
还没有
留言，来写首评
```
